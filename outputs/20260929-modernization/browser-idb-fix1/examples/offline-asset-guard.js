import { txDone, accountRange } from './idb-core.js';
import { getStorageEstimateSummary, requestPersistentStorageAfterUserIntent } from './quota-manager.js';
export const OFFLINE_ASSET_SCHEMA = 1;
export const DEFAULT_OFFLINE_STORE_CONFIG = {
    storeName: 'offline_assets',
    accountIndexName: 'byAccountUpdatedAt',
    maxTotalBytes: 4 * 1024 * 1024 * 1024,
    freeSpaceSafetyFactor: 1.25
};
export async function decideDownloadStart(options) {
    const config = options.config ?? DEFAULT_OFFLINE_STORE_CONFIG;
    if (options.currentOfflineBytes + options.expectedBytes > config.maxTotalBytes) {
        return {
            ok: false,
            reason: 'over-device-cap'
        };
    }
    const estimate = await getStorageEstimateSummary();
    if (!estimate.supported || estimate.availableBytes === undefined) {
        return {
            ok: false,
            reason: 'no-estimate'
        };
    }
    if (estimate.availableBytes < options.expectedBytes * config.freeSpaceSafetyFactor) {
        return {
            ok: false,
            reason: 'insufficient-space'
        };
    }
    return {
        ok: true,
        persistence: await requestPersistentStorageAfterUserIntent()
    };
}
export async function markDownloadStarting(db, record, config = DEFAULT_OFFLINE_STORE_CONFIG) {
    const nowIso = new Date().toISOString();
    const tx = db.transaction(config.storeName, 'readwrite');
    tx.objectStore(config.storeName).put({
        ...record,
        schema: OFFLINE_ASSET_SCHEMA,
        downloadState: 'storing',
        updatedAt: nowIso
    });
    await txDone(tx);
}
export async function reconcileOfflineAssets(options) {
    const config = options.config ?? DEFAULT_OFFLINE_STORE_CONFIG;
    const stored = new Set(await options.listStoredUris());
    const verdicts = [];
    const tx = options.db.transaction(config.storeName, 'readonly');
    const index = tx.objectStore(config.storeName).index(config.accountIndexName);
    await new Promise((resolve, reject)=>{
        const request = index.openCursor(accountRange(options.accountKey));
        request.onerror = ()=>reject(request.error ?? new Error('Offline asset cursor failed'));
        request.onsuccess = ()=>{
            const cursor = request.result;
            if (!cursor) {
                resolve();
                return;
            }
            const record = cursor.value;
            if (record.downloadState !== 'complete') {
                verdicts.push({
                    state: 'partial',
                    record
                });
            } else if (!record.offlineUri || !stored.has(record.offlineUri)) {
                verdicts.push({
                    state: 'evicted',
                    record
                });
            } else {
                verdicts.push({
                    state: 'playable',
                    record
                });
            }
            cursor.continue();
        };
    });
    await txDone(tx);
    return verdicts;
}
export async function forgetEvictedAsset(db, id, config = DEFAULT_OFFLINE_STORE_CONFIG) {
    const tx = db.transaction(config.storeName, 'readwrite');
    tx.objectStore(config.storeName).delete(id);
    await txDone(tx);
}
