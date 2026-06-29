/**
 * Example shape for unit tests. In a real repo, install/configure fake-indexeddb
 * in the test setup rather than importing it here blindly.
 */
import { describe, expect, it } from 'vitest';
import { openIndexedDb, withTransaction, requestToPromise } from './idb-core';

describe('IndexedDB storage pattern', () => {
  it('opens, writes, and reads a record', async () => {
    const dbName = `test-db-${crypto.randomUUID()}`;
    const db = await openIndexedDb({
      name: dbName,
      version: 1,
      upgrade(db) {
        db.createObjectStore('items', { keyPath: 'id' });
      },
    });

    await withTransaction(db, 'items', 'readwrite', (tx) => {
      tx.objectStore('items').put({ id: 'a', value: 1 });
    });

    const tx = db.transaction('items', 'readonly');
    const item = await requestToPromise(tx.objectStore('items').get('a')) as { id: string; value: number };
    expect(item.value).toBe(1);
    db.close();
    indexedDB.deleteDatabase(dbName);
  });
});
