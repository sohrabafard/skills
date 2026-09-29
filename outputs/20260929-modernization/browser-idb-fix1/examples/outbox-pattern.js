import { txDone } from './idb-core.js';
export const DEFAULT_OUTBOX_POLICY = {
    storeName: 'wa_outbox',
    indexName: 'byStatusNextAttemptAt',
    batchSize: 25,
    sendTimeoutMs: 15_000,
    maxAttempts: 10,
    nextDelayMs: (attempts)=>Math.min(3_600_000, 2 ** attempts * 1000)
};
export function validateOutboxPolicy(policy) {
    if (!Number.isInteger(policy.batchSize) || policy.batchSize < 1) {
        throw new RangeError('batchSize must be a positive integer');
    }
    if (!Number.isInteger(policy.maxAttempts) || policy.maxAttempts < 1) {
        throw new RangeError('maxAttempts must be a positive integer');
    }
    if (!Number.isFinite(policy.sendTimeoutMs) || policy.sendTimeoutMs <= 0) {
        throw new RangeError('sendTimeoutMs must be positive');
    }
    return policy;
}
export async function enqueueOutboxItem(db, item, policy = DEFAULT_OUTBOX_POLICY) {
    if (item.status !== 'queued') throw new Error('An enqueued item must be queued');
    const tx = db.transaction(policy.storeName, 'readwrite');
    tx.objectStore(policy.storeName).put(item);
    await txDone(tx);
}
export async function claimNextOutboxBatch(db, nowIso, policy = DEFAULT_OUTBOX_POLICY) {
    const tx = db.transaction(policy.storeName, 'readwrite');
    const index = tx.objectStore(policy.storeName).index(policy.indexName);
    const range = IDBKeyRange.bound([
        'queued',
        ''
    ], [
        'queued',
        nowIso
    ]);
    const items = [];
    await new Promise((resolve, reject)=>{
        const request = index.openCursor(range);
        request.onerror = ()=>reject(request.error ?? new Error('Outbox cursor failed'));
        request.onsuccess = ()=>{
            const cursor = request.result;
            if (!cursor || items.length >= policy.batchSize) {
                resolve();
                return;
            }
            const item = cursor.value;
            const claimed = {
                ...item,
                status: 'sending',
                sendingSince: nowIso,
                updatedAt: nowIso
            };
            cursor.update(claimed);
            items.push(claimed);
            cursor.continue();
        };
    });
    await txDone(tx);
    return items;
}
async function writeOutcome(db, policy, id, mutate) {
    const tx = db.transaction(policy.storeName, 'readwrite');
    const store = tx.objectStore(policy.storeName);
    const request = store.get(id);
    request.onsuccess = ()=>{
        const item = request.result;
        if (item) store.put(mutate(item));
    };
    await txDone(tx);
}
export function classifyResponse(status) {
    if (status >= 200 && status < 300) return {
        kind: 'sent'
    };
    if (status === 401) return {
        kind: 'pause',
        error: 'http_401'
    };
    if (status === 403) return {
        kind: 'abandon',
        error: 'http_403'
    };
    if (status === 409) return {
        kind: 'conflict',
        error: 'http_409'
    };
    if (status === 429 || status >= 500) return {
        kind: 'retry',
        error: `http_${status}`
    };
    return {
        kind: 'abandon',
        error: `http_${status}`
    };
}
export async function flushOutbox(options) {
    const policy = validateOutboxPolicy(options.policy ?? DEFAULT_OUTBOX_POLICY);
    const now = options.now ?? (()=>new Date());
    const batch = await claimNextOutboxBatch(options.db, now().toISOString(), policy);
    const result = {
        sent: 0,
        retried: 0,
        conflicted: 0,
        abandoned: 0,
        paused: false
    };
    for (const item of batch){
        if (options.signal?.aborted || result.paused) {
            await requeue(options.db, policy, item.id, now);
            continue;
        }
        const timeout = new AbortController();
        const timer = setTimeout(()=>timeout.abort(), policy.sendTimeoutMs);
        let outcome;
        try {
            const response = await options.send(item, timeout.signal);
            outcome = classifyResponse(response.status);
        } catch (error) {
            outcome = {
                kind: 'retry',
                error: error instanceof Error ? error.name : 'network_error'
            };
        } finally{
            clearTimeout(timer);
        }
        await applyOutcome(options.db, policy, item, outcome, now, result);
    }
    return result;
}
async function applyOutcome(db, policy, item, outcome, now, result) {
    const nowIso = now().toISOString();
    switch(outcome.kind){
        case 'sent':
            await writeOutcome(db, policy, item.id, (current)=>({
                    ...current,
                    status: 'sent',
                    sendingSince: undefined,
                    updatedAt: nowIso
                }));
            result.sent += 1;
            return;
        case 'pause':
            await requeue(db, policy, item.id, now, outcome.error, false);
            result.paused = true;
            return;
        case 'conflict':
            await writeOutcome(db, policy, item.id, (current)=>({
                    ...current,
                    status: 'conflict',
                    sendingSince: undefined,
                    lastError: outcome.error,
                    updatedAt: nowIso
                }));
            result.conflicted += 1;
            return;
        case 'abandon':
            await writeOutcome(db, policy, item.id, (current)=>({
                    ...current,
                    status: 'abandoned',
                    sendingSince: undefined,
                    lastError: outcome.error,
                    updatedAt: nowIso
                }));
            result.abandoned += 1;
            return;
        case 'retry':
            {
                const attempts = item.attempts + 1;
                const exhausted = attempts >= policy.maxAttempts;
                await writeOutcome(db, policy, item.id, (current)=>({
                        ...current,
                        attempts,
                        status: exhausted ? 'abandoned' : 'queued',
                        sendingSince: undefined,
                        nextAttemptAt: new Date(now().getTime() + policy.nextDelayMs(attempts)).toISOString(),
                        lastError: outcome.error,
                        updatedAt: nowIso
                    }));
                if (exhausted) result.abandoned += 1;
                else result.retried += 1;
                return;
            }
    }
}
async function requeue(db, policy, id, now, lastError, incrementAttempts = false) {
    const nowIso = now().toISOString();
    await writeOutcome(db, policy, id, (current)=>({
            ...current,
            status: 'queued',
            sendingSince: undefined,
            attempts: incrementAttempts ? current.attempts + 1 : current.attempts,
            lastError: lastError ?? current.lastError,
            updatedAt: nowIso
        }));
}
