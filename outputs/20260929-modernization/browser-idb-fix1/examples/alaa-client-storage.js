import { openAlaaClientStorage, USER_SCOPED_STORES } from './migration-pattern.js';
import { txDone, accountRange, classifyStorageFailure } from './idb-core.js';
export const LEARNING_STATE_SCHEMA = 1;
export function parseLearningState(value) {
    if (typeof value !== 'object' || value === null) return null;
    const r = value;
    if (r.schema !== LEARNING_STATE_SCHEMA) return null;
    if (typeof r.id !== 'string' || typeof r.accountKey !== 'string') return null;
    if (typeof r.contentId !== 'string' || typeof r.updatedAt !== 'string') return null;
    return r;
}
export class AlaaClientStorage {
    onWriteFailure;
    runCleanup;
    openDatabase;
    durable = true;
    dbPromise = null;
    constructor(onWriteFailure = ()=>{}, runCleanup = async ()=>{}, openDatabase = openAlaaClientStorage){
        this.onWriteFailure = onWriteFailure;
        this.runCleanup = runCleanup;
        this.openDatabase = openDatabase;
    }
    db() {
        this.dbPromise ??= this.openDatabase();
        return this.dbPromise;
    }
    async get(key) {
        const db = await this.db();
        const tx = db.transaction('learning_state', 'readonly');
        const request = tx.objectStore('learning_state').get(key);
        let value;
        request.onsuccess = ()=>{
            value = request.result;
        };
        await txDone(tx);
        return parseLearningState(value) ?? undefined;
    }
    async set(key, record) {
        try {
            await this.writeOnce(record);
        } catch (error) {
            const kind = classifyStorageFailure(error);
            if (kind !== 'quota-exceeded') {
                this.onWriteFailure({
                    kind,
                    userMustBeTold: false
                });
                throw error;
            }
            await this.runCleanup();
            try {
                await this.writeOnce(record);
            } catch (retryError) {
                this.onWriteFailure({
                    kind: 'quota-exceeded',
                    userMustBeTold: true
                });
                throw retryError;
            }
        }
    }
    async writeOnce(record) {
        const db = await this.db();
        const nowIso = new Date().toISOString();
        const tx = db.transaction([
            'learning_state',
            'storage_items'
        ], 'readwrite');
        tx.objectStore('learning_state').put(record);
        tx.objectStore('storage_items').put({
            id: `learning_state:${record.id}`,
            store: 'learning_state',
            accountKey: record.accountKey,
            dataClass: 'user_private_low_risk',
            bytesApprox: roughBytes(record),
            createdAt: record.createdAt,
            updatedAt: record.updatedAt,
            lastAccessedAt: nowIso,
            refetchable: true
        });
        await txDone(tx);
    }
    async delete(key) {
        const db = await this.db();
        const tx = db.transaction([
            'learning_state',
            'storage_items'
        ], 'readwrite');
        tx.objectStore('learning_state').delete(key);
        tx.objectStore('storage_items').delete(`learning_state:${key}`);
        await txDone(tx);
    }
    async clear() {
        const db = await this.db();
        const tx = db.transaction([
            'learning_state',
            'storage_items'
        ], 'readwrite');
        tx.objectStore('learning_state').clear();
        tx.objectStore('storage_items').clear();
        await txDone(tx);
    }
    async deleteByAccount(accountKey) {
        const db = await this.db();
        const tx = db.transaction([
            ...USER_SCOPED_STORES,
            'storage_items'
        ], 'readwrite');
        let removed = 0;
        let failure;
        let aborting = false;
        const done = new Promise((resolve, reject)=>{
            tx.oncomplete = ()=>resolve();
            tx.onabort = ()=>reject(failure ?? tx.error ?? new DOMException('Purge aborted', 'AbortError'));
        });
        const abort = (cause)=>{
            if (aborting) return;
            aborting = true;
            failure ??= cause;
            try {
                tx.abort();
            } catch  {}
        };
        try {
            const indexes = [
                ...USER_SCOPED_STORES,
                'storage_items'
            ].map((name)=>{
                const store = tx.objectStore(name);
                const indexName = name === 'storage_items' ? 'byAccount' : accountIndexFor(name);
                if (!store.indexNames.contains(indexName)) {
                    throw new Error(`${name} has no ${indexName}; schema upgrade required`);
                }
                return {
                    index: store.index(indexName),
                    countsData: name !== 'storage_items'
                };
            });
            for (const { index, countsData } of indexes){
                const request = index.openCursor(accountRange(accountKey));
                request.onerror = ()=>abort(request.error);
                request.onsuccess = ()=>{
                    const cursor = request.result;
                    if (!cursor) return;
                    try {
                        const deletion = cursor.delete();
                        deletion.onerror = ()=>abort(deletion.error);
                        if (countsData) removed += 1;
                        cursor.continue();
                    } catch (cause) {
                        abort(cause);
                    }
                };
            }
        } catch (cause) {
            abort(cause);
        }
        await done;
        return removed;
    }
}
function accountIndexFor(storeName) {
    switch(storeName){
        case 'drafts':
            return 'byAccountTargetUpdatedAt';
        case 'wa_outbox':
            return 'byAccountCreatedAt';
        default:
            return 'byAccountUpdatedAt';
    }
}
function roughBytes(value) {
    try {
        return new Blob([
            JSON.stringify(value)
        ]).size;
    } catch  {
        return 0;
    }
}
