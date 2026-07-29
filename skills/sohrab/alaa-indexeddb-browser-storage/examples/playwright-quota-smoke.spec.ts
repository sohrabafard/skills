/**
 * Level 4 (local smoke) in /alaa-testing-strategy ($alaa-testing-strategy)'s ladder.
 * references/80-testing-and-proof-levels.md
 *
 * This lane exists to prove a REAL engine raises what the unit tests' injected error
 * only simulates. It induces an actual QuotaExceededError rather than asserting that
 * a returned object has a property, which cannot fail.
 *
 * Requires `use: { baseURL }` in playwright.config.ts, or replace page.goto('/') with
 * an absolute URL. Slow by design: keep it out of the per-commit lane.
 */
import { expect, test } from '@playwright/test';

const PROBE_DB = '__playwright_idb_probe__';

test.beforeEach(async ({ page }) => {
  await page.goto('/');
});

test.afterEach(async ({ page }) => {
  await page.evaluate((name) => indexedDB.deleteDatabase(name), PROBE_DB);
});

test('a real engine opens, upgrades and writes', async ({ page }) => {
  const result = await page.evaluate(async (name) => {
    if (!('indexedDB' in globalThis)) return { ok: false as const, reason: 'missing' };
    const request = indexedDB.open(name, 1);
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

    const read = db.transaction('items', 'readonly').objectStore('items').get('ok');
    const value = await new Promise<unknown>((resolve, reject) => {
      read.onsuccess = () => resolve(read.result);
      read.onerror = () => reject(read.error);
    });
    db.close();
    return { ok: true as const, value };
  }, PROBE_DB);

  // Asserts the outcome, not merely the shape of the outcome.
  expect(result.ok).toBe(true);
  expect(result).toMatchObject({ value: { id: 'ok', value: true } });
});

test('a real engine raises QuotaExceededError, and the error is named', async ({ page }) => {
  test.slow();

  const result = await page.evaluate(async (name) => {
    const request = indexedDB.open(name, 1);
    request.onupgradeneeded = () => request.result.createObjectStore('blobs', { keyPath: 'id' });
    const db = await new Promise<IDBDatabase>((resolve, reject) => {
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });

    const before = (await navigator.storage?.estimate?.())?.usage ?? 0;
    // 8 MiB per record. Stop the moment the engine refuses, or at the ceiling.
    const chunk = new Uint8Array(8 * 1024 * 1024);
    const MAX_RECORDS = 4096;

    for (let i = 0; i < MAX_RECORDS; i += 1) {
      try {
        const tx = db.transaction('blobs', 'readwrite');
        tx.objectStore('blobs').put({ id: `b-${i}`, data: chunk });
        await new Promise<void>((resolve, reject) => {
          tx.oncomplete = () => resolve();
          tx.onerror = () => reject(tx.error);
          tx.onabort = () => reject(tx.error);
        });
      } catch (error) {
        const after = (await navigator.storage?.estimate?.())?.usage ?? 0;
        db.close();
        return {
          threw: true as const,
          name: error instanceof DOMException ? error.name : 'not-a-DOMException',
          writtenRecords: i,
          grewBy: after - before,
        };
      }
    }

    db.close();
    return { threw: false as const, writtenRecords: MAX_RECORDS };
  }, PROBE_DB);

  // A CI runner with an enormous disk may not reach the limit. That is a SKIP, not
  // a pass: exit-2 semantics. Never report a bound the run did not observe.
  test.skip(
    !result.threw,
    `Wrote ${result.writtenRecords} records without hitting quota; this runner cannot bound the quota path.`,
  );

  expect(result.name).toBe('QuotaExceededError');
  expect(result.writtenRecords).toBeGreaterThan(0);
});

test('storage estimate returns two approximate numbers, or is honestly absent', async ({ page }) => {
  const result = await page.evaluate(async () => {
    if (!navigator.storage?.estimate) return { supported: false as const };
    const estimate = await navigator.storage.estimate();
    return {
      supported: true as const,
      usage: estimate.usage,
      quota: estimate.quota,
    };
  });

  if (!result.supported) {
    // Tier below 2. The product must not offer a measured budget here.
    expect(result.supported).toBe(false);
    return;
  }

  expect(typeof result.usage).toBe('number');
  expect(typeof result.quota).toBe('number');
  expect(result.quota).toBeGreaterThan(0);
  expect(result.usage).toBeLessThanOrEqual(result.quota as number);
});

test('a second connection that ignores versionchange blocks the upgrade', async ({ page }) => {
  const blocked = await page.evaluate(async (name) => {
    const first = indexedDB.open(name, 1);
    first.onupgradeneeded = () => first.result.createObjectStore('items', { keyPath: 'id' });
    const held = await new Promise<IDBDatabase>((resolve, reject) => {
      first.onsuccess = () => resolve(first.result);
      first.onerror = () => reject(first.error);
    });
    // Deliberately do not close on versionchange: this is the defect being reproduced.

    return await new Promise<boolean>((resolve) => {
      const second = indexedDB.open(name, 2);
      let sawBlocked = false;
      second.onblocked = () => {
        sawBlocked = true;
        held.close(); // what the reload UX does in the application
      };
      second.onsuccess = () => {
        second.result.close();
        resolve(sawBlocked);
      };
      second.onerror = () => resolve(sawBlocked);
    });
  }, PROBE_DB);

  expect(blocked).toBe(true);
});
