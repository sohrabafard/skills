import { openIndexedDb } from './idb-core';

export const ALAA_DB_NAME = 'alaa-client-storage';
export const ALAA_DB_VERSION = 3;

export async function openAlaaClientStorage(): Promise<IDBDatabase> {
  return openIndexedDb({
    name: ALAA_DB_NAME,
    version: ALAA_DB_VERSION,
    upgrade(db, tx, oldVersion) {
      if (oldVersion < 1) {
        db.createObjectStore('meta', { keyPath: 'key' });
        db.createObjectStore('storage_items', { keyPath: 'id' })
          .createIndex('byDataClassLastAccessedAt', ['dataClass', 'lastAccessedAt']);
      }

      if (oldVersion < 2) {
        const learning = db.createObjectStore('learning_state', { keyPath: 'id' });
        learning.createIndex('byAccountUpdatedAt', ['accountKey', 'updatedAt']);
        learning.createIndex('byContent', ['accountKey', 'contentId']);

        const outbox = db.createObjectStore('wa_outbox', { keyPath: 'id' });
        outbox.createIndex('byStatusRetryAt', ['status', 'nextAttemptAt']);
        outbox.createIndex('byAccountCreatedAt', ['accountKey', 'createdAt']);
      }

      if (oldVersion < 3) {
        const drafts = db.createObjectStore('drafts', { keyPath: 'id' });
        drafts.createIndex('byAccountTargetUpdatedAt', ['accountKey', 'targetType', 'targetId', 'updatedAt']);

        const meta = tx.objectStore('meta');
        meta.put({ key: 'schemaVersion', value: 3, updatedAt: new Date().toISOString() });
      }
    },
    onBlocked() {
      // Surface a reload/close-other-tabs message in the real app.
      console.warn('IndexedDB upgrade is blocked by another open tab.');
    },
    onVersionChange() {
      // The old connection has been closed. The app can prompt the user to reload.
      console.warn('IndexedDB version changed; this tab should reload.');
    },
  });
}
