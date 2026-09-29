import { txDone } from './idb-core.js';
import { DEFAULT_OUTBOX_POLICY } from './outbox-pattern.js';
export const DEFAULT_REAPER_POLICY = {
    staleAfterMs: 120_000
};
export function validateReaperPolicy(reaper, outbox = DEFAULT_OUTBOX_POLICY) {
    if (!Number.isFinite(reaper.staleAfterMs) || reaper.staleAfterMs <= 0) {
        throw new RangeError('staleAfterMs must be positive');
    }
    if (reaper.staleAfterMs <= outbox.sendTimeoutMs * 2) {
        throw new RangeError('staleAfterMs must exceed twice sendTimeoutMs, or the reaper races a live send');
    }
    return reaper;
}
export async function reapOrphanedOutboxRows(options) {
    const policy = options.policy ?? DEFAULT_OUTBOX_POLICY;
    const reaper = validateReaperPolicy(options.reaper ?? DEFAULT_REAPER_POLICY, policy);
    const now = options.now ?? (()=>new Date());
    const nowMs = now().getTime();
    const nowIso = new Date(nowMs).toISOString();
    const result = {
        reaped: 0,
        inFlight: 0
    };
    const tx = options.db.transaction(policy.storeName, 'readwrite');
    const index = tx.objectStore(policy.storeName).index(policy.indexName);
    const range = IDBKeyRange.bound([
        'sending'
    ], [
        'sending',
        []
    ]);
    await new Promise((resolve, reject)=>{
        const request = index.openCursor(range);
        request.onerror = ()=>reject(request.error ?? new Error('Reaper cursor failed'));
        request.onsuccess = ()=>{
            const cursor = request.result;
            if (!cursor) {
                resolve();
                return;
            }
            const item = cursor.value;
            const startedMs = item.sendingSince ? Date.parse(item.sendingSince) : 0;
            const stale = !Number.isFinite(startedMs) || nowMs - startedMs >= reaper.staleAfterMs;
            if (stale) {
                const attempts = item.attempts + 1;
                cursor.update({
                    ...item,
                    status: 'queued',
                    sendingSince: undefined,
                    attempts,
                    nextAttemptAt: new Date(nowMs + policy.nextDelayMs(attempts)).toISOString(),
                    lastError: 'reaped',
                    updatedAt: nowIso
                });
                result.reaped += 1;
            } else {
                result.inFlight += 1;
            }
            cursor.continue();
        };
    });
    await txDone(tx);
    return result;
}
export const NEVER_DELETE_TO_UNSTICK = true;
