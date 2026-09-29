import { expect, test } from '@playwright/test';
const PROBE_DB = '__playwright_idb_probe__';
test.beforeEach(async ({ page })=>{
    await page.goto('/');
});
test.afterEach(async ({ page })=>{
    await page.evaluate((name)=>indexedDB.deleteDatabase(name), PROBE_DB);
});
test('a real engine opens, upgrades and writes', async ({ page })=>{
    const result = await page.evaluate(async (name)=>{
        if (!('indexedDB' in globalThis)) return {
            ok: false,
            reason: 'missing'
        };
        const request = indexedDB.open(name, 1);
        request.onupgradeneeded = ()=>request.result.createObjectStore('items', {
                keyPath: 'id'
            });
        const db = await new Promise((resolve, reject)=>{
            request.onsuccess = ()=>resolve(request.result);
            request.onerror = ()=>reject(request.error);
        });
        const tx = db.transaction('items', 'readwrite');
        tx.objectStore('items').put({
            id: 'ok',
            value: true
        });
        await new Promise((resolve, reject)=>{
            tx.oncomplete = ()=>resolve();
            tx.onerror = ()=>reject(tx.error);
            tx.onabort = ()=>reject(tx.error);
        });
        const read = db.transaction('items', 'readonly').objectStore('items').get('ok');
        const value = await new Promise((resolve, reject)=>{
            read.onsuccess = ()=>resolve(read.result);
            read.onerror = ()=>reject(read.error);
        });
        db.close();
        return {
            ok: true,
            value
        };
    }, PROBE_DB);
    expect(result.ok).toBe(true);
    expect(result).toMatchObject({
        value: {
            id: 'ok',
            value: true
        }
    });
});
test('a real engine raises QuotaExceededError, and the error is named', async ({ page })=>{
    test.slow();
    const result = await page.evaluate(async (name)=>{
        const request = indexedDB.open(name, 1);
        request.onupgradeneeded = ()=>request.result.createObjectStore('blobs', {
                keyPath: 'id'
            });
        const db = await new Promise((resolve, reject)=>{
            request.onsuccess = ()=>resolve(request.result);
            request.onerror = ()=>reject(request.error);
        });
        const before = (await navigator.storage?.estimate?.())?.usage ?? 0;
        const chunk = new Uint8Array(8 * 1024 * 1024);
        const MAX_RECORDS = 4096;
        for(let i = 0; i < MAX_RECORDS; i += 1){
            try {
                const tx = db.transaction('blobs', 'readwrite');
                tx.objectStore('blobs').put({
                    id: `b-${i}`,
                    data: chunk
                });
                await new Promise((resolve, reject)=>{
                    tx.oncomplete = ()=>resolve();
                    tx.onerror = ()=>reject(tx.error);
                    tx.onabort = ()=>reject(tx.error);
                });
            } catch (error) {
                const after = (await navigator.storage?.estimate?.())?.usage ?? 0;
                db.close();
                return {
                    threw: true,
                    name: error instanceof DOMException ? error.name : 'not-a-DOMException',
                    writtenRecords: i,
                    grewBy: after - before
                };
            }
        }
        db.close();
        return {
            threw: false,
            writtenRecords: MAX_RECORDS
        };
    }, PROBE_DB);
    test.skip(!result.threw, `Wrote ${result.writtenRecords} records without hitting quota; this runner cannot bound the quota path.`);
    expect(result.name).toBe('QuotaExceededError');
    expect(result.writtenRecords).toBeGreaterThan(0);
});
test('storage estimate returns two approximate numbers, or is honestly absent', async ({ page })=>{
    const result = await page.evaluate(async ()=>{
        if (!navigator.storage?.estimate) return {
            supported: false
        };
        const estimate = await navigator.storage.estimate();
        return {
            supported: true,
            usage: estimate.usage,
            quota: estimate.quota
        };
    });
    if (!result.supported) {
        expect(result.supported).toBe(false);
        return;
    }
    expect(typeof result.usage).toBe('number');
    expect(typeof result.quota).toBe('number');
    expect(result.quota).toBeGreaterThan(0);
    expect(result.usage).toBeLessThanOrEqual(result.quota);
});
test('a second connection that ignores versionchange blocks the upgrade', async ({ page })=>{
    const blocked = await page.evaluate(async (name)=>{
        const first = indexedDB.open(name, 1);
        first.onupgradeneeded = ()=>first.result.createObjectStore('items', {
                keyPath: 'id'
            });
        const held = await new Promise((resolve, reject)=>{
            first.onsuccess = ()=>resolve(first.result);
            first.onerror = ()=>reject(first.error);
        });
        return await new Promise((resolve)=>{
            const second = indexedDB.open(name, 2);
            let sawBlocked = false;
            second.onblocked = ()=>{
                sawBlocked = true;
                held.close();
            };
            second.onsuccess = ()=>{
                second.result.close();
                resolve(sawBlocked);
            };
            second.onerror = ()=>resolve(sawBlocked);
        });
    }, PROBE_DB);
    expect(blocked).toBe(true);
});
