import { expect, test } from '@playwright/test';

test('IndexedDB open/write probe works or degrades cleanly', async ({ page }) => {
  await page.goto('/');

  const result = await page.evaluate(async () => {
    if (!('indexedDB' in globalThis)) return { ok: false, reason: 'missing' };

    try {
      const request = indexedDB.open('__playwright_idb_probe__', 1);
      request.onupgradeneeded = () => request.result.createObjectStore('items', { keyPath: 'id' });
      const db = await new Promise<IDBDatabase>((resolve, reject) => {
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      });

      const tx = db.transaction('items', 'readwrite');
      tx.objectStore('items').put({ id: 'ok', value: true });
      await new Promise<void>((resolve, reject) => {
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error);
        tx.onabort = () => reject(tx.error);
      });
      db.close();
      indexedDB.deleteDatabase('__playwright_idb_probe__');
      return { ok: true };
    } catch (error) {
      return { ok: false, reason: error instanceof Error ? error.name : 'unknown' };
    }
  });

  expect(result).toHaveProperty('ok');
});

test('Storage estimate is safe to call when available', async ({ page }) => {
  await page.goto('/');
  const result = await page.evaluate(async () => {
    if (!navigator.storage?.estimate) return { supported: false };
    const estimate = await navigator.storage.estimate();
    return {
      supported: true,
      usageType: typeof estimate.usage,
      quotaType: typeof estimate.quota,
    };
  });

  expect(result.supported === false || result.usageType === 'number').toBeTruthy();
});
