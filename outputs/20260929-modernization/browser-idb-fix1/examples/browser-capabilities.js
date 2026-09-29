import { probeIndexedDbWrite } from './idb-core.js';
export async function detectBrowserStorageCapabilities() {
    const testedWrite = await probeIndexedDbWrite();
    const nav = typeof navigator !== 'undefined' ? navigator : undefined;
    const storage = nav?.storage;
    const estimate = typeof storage?.estimate === 'function';
    const persist = typeof storage?.persist === 'function';
    let persisted = 'unknown';
    if (typeof storage?.persisted === 'function') {
        try {
            persisted = await storage.persisted();
        } catch  {
            persisted = 'unknown';
        }
    }
    const objectStoreProto = typeof IDBObjectStore !== 'undefined' ? IDBObjectStore.prototype : undefined;
    return {
        indexedDb: testedWrite ? estimate || persist ? 'modern' : 'core' : 'unavailable',
        testedWrite,
        estimate,
        persist,
        persisted,
        getAll: !!objectStoreProto && 'getAll' in objectStoreProto,
        getAllKeys: !!objectStoreProto && 'getAllKeys' in objectStoreProto,
        getAllRecords: !!objectStoreProto && 'getAllRecords' in objectStoreProto,
        transactionDurability: typeof IDBTransaction === 'undefined' ? 'unknown' : 'durability' in IDBTransaction.prototype,
        databases: typeof indexedDB !== 'undefined' && typeof indexedDB.databases === 'function',
        broadcastChannel: typeof BroadcastChannel !== 'undefined',
        locks: !!nav && 'locks' in nav,
        serviceWorker: !!nav && 'serviceWorker' in nav,
        backgroundSync: typeof ServiceWorkerRegistration !== 'undefined' && 'sync' in ServiceWorkerRegistration.prototype,
        opfs: !!storage && typeof storage.getDirectory === 'function',
        workerIdb: typeof Worker === 'undefined' ? 'unknown' : true,
        storageBuckets: !!nav && 'storageBuckets' in nav,
        privateModeLikely: await inferPrivateModeWeakSignal(estimate)
    };
}
async function inferPrivateModeWeakSignal(canEstimate) {
    if (!canEstimate) return 'unknown';
    try {
        const { quota } = await navigator.storage.estimate();
        if (!quota) return 'unknown';
        return quota < 100 * 1024 * 1024;
    } catch  {
        return 'unknown';
    }
}
export function chooseCapabilityTier(c) {
    if (c.indexedDb === 'unavailable' || !c.testedWrite) return 0;
    if (!c.estimate) return 1;
    const hasLargeValueStore = c.opfs || typeof caches !== 'undefined';
    const hasCoordination = c.broadcastChannel && c.locks;
    const hasWorker = c.workerIdb === true;
    if (hasWorker && hasLargeValueStore && hasCoordination) return 3;
    return 2;
}
