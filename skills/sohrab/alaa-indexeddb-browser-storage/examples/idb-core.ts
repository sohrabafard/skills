/**
 * Minimal IndexedDB helpers.
 * These are examples for agents to adapt, not a required library.
 */

export type UpgradeHandler = (db: IDBDatabase, tx: IDBTransaction, oldVersion: number, newVersion: number | null) => void;

export function requestToPromise<T>(request: IDBRequest<T>): Promise<T> {
  return new Promise((resolve, reject) => {
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error ?? new Error('IndexedDB request failed'));
  });
}

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

export async function openIndexedDb(options: {
  name: string;
  version: number;
  upgrade: UpgradeHandler;
  onBlocked?: () => void;
  onVersionChange?: () => void;
  onClose?: () => void;
}): Promise<IDBDatabase> {
  if (!('indexedDB' in globalThis)) {
    throw new DOMException('IndexedDB is not available', 'NotSupportedError');
  }

  const request = indexedDB.open(options.name, options.version);

  request.onupgradeneeded = (event) => {
    const db = request.result;
    const tx = request.transaction;
    if (!tx) throw new Error('Missing IndexedDB upgrade transaction');
    options.upgrade(db, tx, event.oldVersion, event.newVersion);
  };

  request.onblocked = () => options.onBlocked?.();

  const db = await requestToPromise(request);

  db.onversionchange = () => {
    db.close();
    options.onVersionChange?.();
  };

  db.onclose = () => options.onClose?.();

  return db;
}

export async function withTransaction<T>(
  db: IDBDatabase,
  stores: string | string[],
  mode: IDBTransactionMode,
  fn: (tx: IDBTransaction) => T,
  txOptions?: IDBTransactionOptions,
): Promise<T> {
  const tx = createTransaction(db, stores, mode, txOptions);
  const result = fn(tx);

  // Transaction callbacks must be synchronous. Await external work before
  // creating the transaction; then queue IDB requests inside the callback.
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
    // Older browsers may not accept transaction options.
    return db.transaction(stores, mode);
  }
}

export async function getAllBounded<T>(
  source: IDBObjectStore | IDBIndex,
  query?: IDBValidKey | IDBKeyRange,
  count = 100,
): Promise<T[]> {
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

export async function probeIndexedDbWrite(dbName = '__idb_probe__'): Promise<boolean> {
  if (!('indexedDB' in globalThis)) return false;

  try {
    const db = await openIndexedDb({
      name: dbName,
      version: 1,
      upgrade(db) {
        if (!db.objectStoreNames.contains('probe')) {
          db.createObjectStore('probe', { keyPath: 'id' });
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
    return false;
  }
}
