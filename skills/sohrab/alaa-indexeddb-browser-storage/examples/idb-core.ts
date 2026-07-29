/**
 * Minimal IndexedDB helpers. Examples for agents to adapt, not a required library.
 * Requires TypeScript >= 5.2 for `IDBTransactionOptions` in `lib.dom`.
 * Rules enforced here: references/50-transactions-performance-and-query-patterns.md
 */

export type UpgradeHandler = (
  db: IDBDatabase,
  tx: IDBTransaction,
  oldVersion: number,
  newVersion: number | null,
) => void;

export function requestToPromise<T>(request: IDBRequest<T>): Promise<T> {
  return new Promise((resolve, reject) => {
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error ?? new Error('IndexedDB request failed'));
  });
}

/** Resolve on transaction completion, never on request success. */
export function txDone(tx: IDBTransaction): Promise<void> {
  return new Promise((resolve, reject) => {
    tx.oncomplete = () => resolve();
    tx.onabort = () => reject(tx.error ?? new DOMException('Transaction aborted', 'AbortError'));
    tx.onerror = () => reject(tx.error ?? new Error('Transaction failed'));
  });
}

export function isQuotaExceededError(error: unknown): boolean {
  return error instanceof DOMException && error.name === 'QuotaExceededError';
}

/** The failure classes of references/31-quota-exceeded-and-cleanup.md, as a discriminant. */
export type StorageFailureClass =
  | 'quota-exceeded'
  | 'constraint'
  | 'transaction-inactive'
  | 'aborted'
  | 'unavailable'
  | 'unknown';

export function classifyStorageFailure(error: unknown): StorageFailureClass {
  if (!(error instanceof DOMException)) return 'unknown';
  switch (error.name) {
    case 'QuotaExceededError':
      return 'quota-exceeded';
    case 'ConstraintError':
      return 'constraint';
    case 'TransactionInactiveError':
      return 'transaction-inactive';
    case 'AbortError':
      return 'aborted';
    case 'NotSupportedError':
    case 'InvalidStateError':
    case 'SecurityError':
      return 'unavailable';
    default:
      return 'unknown';
  }
}

/** Only these two are worth a single retry. See references/31, class 4. */
export function isRetryableStorageFailure(kind: StorageFailureClass): boolean {
  return kind === 'quota-exceeded' || kind === 'unknown';
}

export interface OpenOptions {
  name: string;
  /**
   * Omit the version in a service worker: it must never initiate an upgrade.
   * references/41-multitab-versionchange-and-locks.md
   */
  version?: number;
  upgrade?: UpgradeHandler;
  onBlocked?: () => void;
  onVersionChange?: () => void;
  onClose?: () => void;
}

export async function openIndexedDb(options: OpenOptions): Promise<IDBDatabase> {
  if (!('indexedDB' in globalThis)) {
    throw new DOMException('IndexedDB is not available', 'NotSupportedError');
  }

  const request =
    options.version === undefined
      ? indexedDB.open(options.name)
      : indexedDB.open(options.name, options.version);

  // A throw inside the event handler escapes into event dispatch. Capture it and
  // reject the open explicitly instead of relying on an incidental abort.
  let upgradeError: unknown;
  request.onupgradeneeded = (event) => {
    try {
      const tx = request.transaction;
      if (!tx) throw new Error('Missing IndexedDB upgrade transaction');
      options.upgrade?.(request.result, tx, event.oldVersion, event.newVersion);
    } catch (error) {
      upgradeError = error;
      request.transaction?.abort();
    }
  };

  request.onblocked = () => options.onBlocked?.();

  let db: IDBDatabase;
  try {
    db = await requestToPromise(request);
  } catch (error) {
    throw upgradeError ?? error;
  }
  if (upgradeError) {
    db.close();
    throw upgradeError;
  }

  // Close first, unconditionally. Any prompt happens after, or the upgrade in the
  // other context stays blocked for as long as the user ignores it.
  db.onversionchange = () => {
    db.close();
    options.onVersionChange?.();
  };
  db.onclose = () => options.onClose?.();

  return db;
}

/**
 * The callback must be synchronous: an await inside an open transaction makes it
 * go inactive. Returning a Promise aborts rather than failing later and elsewhere.
 */
export async function withTransaction<T>(
  db: IDBDatabase,
  stores: string | string[],
  mode: IDBTransactionMode,
  fn: (tx: IDBTransaction) => T,
  txOptions?: IDBTransactionOptions,
): Promise<T> {
  const tx = createTransaction(db, stores, mode, txOptions);
  const result = fn(tx);

  if (result && typeof (result as PromiseLike<unknown>).then === 'function') {
    tx.abort();
    throw new Error('IndexedDB transaction callback must not return a Promise');
  }

  await txDone(tx);
  return result;
}

function createTransaction(
  db: IDBDatabase,
  stores: string | string[],
  mode: IDBTransactionMode,
  txOptions?: IDBTransactionOptions,
): IDBTransaction {
  try {
    return txOptions ? db.transaction(stores, mode, txOptions) : db.transaction(stores, mode);
  } catch {
    // Older engines reject the options argument. Fall back to the engine default.
    return db.transaction(stores, mode);
  }
}

/**
 * Bounded read. O(log n + count) via getAll, or O(log n + count) via cursor where
 * getAll is unavailable. Never unbounded: references/50, complexity budgets.
 */
export async function getAllBounded<T>(
  source: IDBObjectStore | IDBIndex,
  query?: IDBValidKey | IDBKeyRange,
  count = 100,
): Promise<T[]> {
  if (count <= 0) throw new RangeError('getAllBounded requires a positive count');

  if ('getAll' in source && typeof source.getAll === 'function') {
    return requestToPromise(source.getAll(query as never, count)) as Promise<T[]>;
  }

  return new Promise<T[]>((resolve, reject) => {
    const results: T[] = [];
    const request = source.openCursor(query as never);
    request.onerror = () => reject(request.error ?? new Error('Cursor failed'));
    request.onsuccess = () => {
      const cursor = request.result;
      if (!cursor || results.length >= count) {
        resolve(results);
        return;
      }
      results.push(cursor.value as T);
      cursor.continue();
    };
  });
}

/** The range that selects every record under one account prefix. references/50. */
export function accountRange(accountKey: string): IDBKeyRange {
  return IDBKeyRange.bound([accountKey], [accountKey, []]);
}

/** Tier-0 detection: the global existing is not evidence the store works. */
export async function probeIndexedDbWrite(dbName = '__idb_probe__'): Promise<boolean> {
  if (!('indexedDB' in globalThis)) return false;

  try {
    const db = await openIndexedDb({
      name: dbName,
      version: 1,
      upgrade(database) {
        if (!database.objectStoreNames.contains('probe')) {
          database.createObjectStore('probe', { keyPath: 'id' });
        }
      },
    });

    await withTransaction(db, 'probe', 'readwrite', (tx) => {
      tx.objectStore('probe').put({ id: 'ok', value: true, updatedAt: new Date().toISOString() });
    });

    db.close();
    indexedDB.deleteDatabase(dbName);
    return true;
  } catch {
    // Private mode, a blocking policy, or a full disk. All mean the same to the caller.
    return false;
  }
}
