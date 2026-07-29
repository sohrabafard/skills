/**
 * Application-level storage facade.
 * references/95-alaa-integration-playbook.md, references/62-poisoning-and-purge.md
 *
 * It implements the same KeyValueStore interface as the Tier 0 MemoryStore, so a
 * caller at tier 0 substitutes one for the other without branching.
 */
import { openAlaaClientStorage, USER_SCOPED_STORES } from './migration-pattern';
import { txDone, accountRange, classifyStorageFailure, type StorageFailureClass } from './idb-core';
import type { KeyValueStore } from './fallback-memory-store';

/** dataClass values come from assets/data-classification-policy.yaml, not from prose. */
export type DataClass =
  | 'public_cache'
  | 'user_private_low_risk'
  | 'user_generated_unsynced'
  | 'analytics_outbox';

export interface LearningStateRecord {
  id: string;
  schema: 1;
  accountKey: string;
  contentId: string;
  courseId?: string;
  positionSeconds?: number;
  progressPercent?: number;
  serverRevision?: string;
  syncStatus: 'local' | 'synced' | 'pending';
  createdAt: string;
  updatedAt: string;
}

export const LEARNING_STATE_SCHEMA = 1;

/**
 * The cleanup-metadata record. The byDataClassLastAccessedAt index in
 * migration-pattern.ts is built over ['dataClass', 'lastAccessedAt']; both are
 * declared here, so the index is populated. An index over a field the record does
 * not carry is silently empty and never errors.
 */
export interface StorageItemMeta {
  id: string;
  store: string;
  accountKey: string;
  dataClass: DataClass;
  bytesApprox: number;
  createdAt: string;
  updatedAt: string;
  lastAccessedAt: string;
  expiresAt?: string;
  refetchable: boolean;
}

/** A record read out of IndexedDB is untrusted input. references/62. */
export function parseLearningState(value: unknown): LearningStateRecord | null {
  if (typeof value !== 'object' || value === null) return null;
  const r = value as Record<string, unknown>;
  if (r.schema !== LEARNING_STATE_SCHEMA) return null;
  if (typeof r.id !== 'string' || typeof r.accountKey !== 'string') return null;
  if (typeof r.contentId !== 'string' || typeof r.updatedAt !== 'string') return null;
  return r as unknown as LearningStateRecord;
}

export interface StorageWriteFailure {
  kind: StorageFailureClass;
  /** True when the caller must tell the user rather than failing silently. */
  userMustBeTold: boolean;
}

export class AlaaClientStorage implements KeyValueStore<LearningStateRecord> {
  readonly durable = true;
  private dbPromise: Promise<IDBDatabase> | null = null;

  constructor(
    private readonly onWriteFailure: (failure: StorageWriteFailure) => void = () => {},
    private readonly runCleanup: () => Promise<void> = async () => {},
  ) {}

  private db(): Promise<IDBDatabase> {
    this.dbPromise ??= openAlaaClientStorage();
    return this.dbPromise;
  }

  async get(key: string): Promise<LearningStateRecord | undefined> {
    const db = await this.db();
    const tx = db.transaction('learning_state', 'readonly');
    const request = tx.objectStore('learning_state').get(key);
    let value: unknown;
    request.onsuccess = () => {
      value = request.result;
    };
    await txDone(tx);
    return parseLearningState(value) ?? undefined;
  }

  /**
   * Quota-aware write. On QuotaExceededError: free refetchable data, retry once,
   * then report. references/31, class 1. A draft that silently failed to save is
   * worse than one that never existed, because the user believes it is safe.
   */
  async set(key: string, record: LearningStateRecord): Promise<void> {
    try {
      await this.writeOnce(record);
    } catch (error) {
      const kind = classifyStorageFailure(error);
      if (kind !== 'quota-exceeded') {
        this.onWriteFailure({ kind, userMustBeTold: false });
        throw error;
      }

      await this.runCleanup();
      try {
        await this.writeOnce(record);
      } catch (retryError) {
        // The write is user-generated state: the user is told, not the log alone.
        this.onWriteFailure({ kind: 'quota-exceeded', userMustBeTold: true });
        throw retryError;
      }
    }
  }

  private async writeOnce(record: LearningStateRecord): Promise<void> {
    const db = await this.db();
    const nowIso = new Date().toISOString();
    // Both stores in one transaction: the record and its cleanup metadata are
    // written atomically, or neither is.
    const tx = db.transaction(['learning_state', 'storage_items'], 'readwrite');
    tx.objectStore('learning_state').put(record);
    tx.objectStore('storage_items').put({
      id: `learning_state:${record.id}`,
      store: 'learning_state',
      accountKey: record.accountKey,
      dataClass: 'user_private_low_risk',
      bytesApprox: roughBytes(record),
      createdAt: record.createdAt,
      updatedAt: record.updatedAt,
      lastAccessedAt: nowIso,
      refetchable: true,
    } satisfies StorageItemMeta);
    await txDone(tx);
  }

  async delete(key: string): Promise<void> {
    const db = await this.db();
    const tx = db.transaction(['learning_state', 'storage_items'], 'readwrite');
    tx.objectStore('learning_state').delete(key);
    tx.objectStore('storage_items').delete(`learning_state:${key}`);
    await txDone(tx);
  }

  async clear(): Promise<void> {
    const db = await this.db();
    const tx = db.transaction(['learning_state', 'storage_items'], 'readwrite');
    tx.objectStore('learning_state').clear();
    tx.objectStore('storage_items').clear();
    await txDone(tx);
  }

  /**
   * The logout purge, in ONE transaction across every user-scoped store.
   * Independent transactions leave the previous account's records readable if the
   * tab dies between them, and that is a security failure, not a performance one.
   *
   * Complexity: O(matching + log n) per store, via the accountKey-prefixed index.
   * A full-store scan here is O(n) per store and may not finish before the device
   * changes hands. references/62, references/50.
   *
   * For counts large enough that one transaction would block the UI, use the
   * journalled form: write meta.logoutPurgePending first, purge in chunks, clear
   * it last, and check it on boot.
   */
  async deleteByAccount(accountKey: string): Promise<number> {
    const db = await this.db();
    const stores = USER_SCOPED_STORES.filter((name) => db.objectStoreNames.contains(name));
    const tx = db.transaction([...stores, 'storage_items'], 'readwrite');
    let removed = 0;

    await Promise.all(
      stores.map(
        (name) =>
          new Promise<void>((resolve, reject) => {
            const store = tx.objectStore(name);
            const indexName = accountIndexFor(name);
            if (!store.indexNames.contains(indexName)) {
              reject(new Error(`${name} has no ${indexName}; it is not ready for user-scoped data`));
              return;
            }
            const request = store.index(indexName).openCursor(accountRange(accountKey));
            request.onerror = () => reject(request.error ?? new Error(`Purge failed on ${name}`));
            request.onsuccess = () => {
              const cursor = request.result;
              if (!cursor) {
                resolve();
                return;
              }
              cursor.delete();
              removed += 1;
              cursor.continue();
            };
          }),
      ),
    );

    await txDone(tx);
    return removed;
  }
}

function accountIndexFor(storeName: string): string {
  switch (storeName) {
    case 'drafts':
      return 'byAccountTargetUpdatedAt';
    case 'wa_outbox':
      return 'byAccountCreatedAt';
    default:
      return 'byAccountUpdatedAt';
  }
}

function roughBytes(value: unknown): number {
  try {
    return new Blob([JSON.stringify(value)]).size;
  } catch {
    return 0;
  }
}
