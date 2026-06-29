import { openAlaaClientStorage } from './migration-pattern';
import { requestToPromise, txDone } from './idb-core';

export interface LearningStateRecord {
  id: string;
  schema: 1;
  accountKey: string;
  courseId?: string;
  setId?: string;
  contentId: string;
  lessonId?: string;
  positionSeconds?: number;
  progressPercent?: number;
  serverRevision?: string;
  syncStatus: 'local' | 'synced' | 'pending';
  createdAt: string;
  updatedAt: string;
}

export class AlaaClientStorage {
  private dbPromise: Promise<IDBDatabase> | null = null;

  private db(): Promise<IDBDatabase> {
    this.dbPromise ??= openAlaaClientStorage();
    return this.dbPromise;
  }

  async saveLearningState(record: LearningStateRecord): Promise<void> {
    const db = await this.db();
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
      lastAccessedAt: new Date().toISOString(),
      refetchable: true,
    });
    await txDone(tx);
  }

  async getLearningState(accountKey: string, contentId: string): Promise<LearningStateRecord | undefined> {
    const db = await this.db();
    const tx = db.transaction('learning_state', 'readonly');
    const index = tx.objectStore('learning_state').index('byContent');
    const record = await requestToPromise(index.get([accountKey, contentId])) as LearningStateRecord | undefined;
    await txDone(tx);
    return record;
  }

  async clearUserData(accountKey: string): Promise<void> {
    const db = await this.db();
    const stores = ['learning_state', 'wa_outbox', 'drafts', 'upload_resume_state'].filter((name) =>
      db.objectStoreNames.contains(name),
    );

    for (const storeName of stores) {
      await deleteByAccountKey(db, storeName, accountKey);
    }
  }
}

async function deleteByAccountKey(db: IDBDatabase, storeName: string, accountKey: string): Promise<void> {
  const tx = db.transaction(storeName, 'readwrite');
  const store = tx.objectStore(storeName);

  // Prefer account indexes in production. This fallback scans when no suitable index exists.
  await new Promise<void>((resolve, reject) => {
    const request = store.openCursor();
    request.onerror = () => reject(request.error ?? new Error(`Failed to scan ${storeName}`));
    request.onsuccess = () => {
      const cursor = request.result;
      if (!cursor) {
        resolve();
        return;
      }
      const value = cursor.value as { accountKey?: string };
      if (value.accountKey === accountKey) cursor.delete();
      cursor.continue();
    };
  });

  await txDone(tx);
}

function roughBytes(value: unknown): number {
  try {
    return new Blob([JSON.stringify(value)]).size;
  } catch {
    return 0;
  }
}
