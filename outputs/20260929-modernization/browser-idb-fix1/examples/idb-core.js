export function requestToPromise(request) {
    return new Promise((resolve, reject)=>{
        request.onsuccess = ()=>resolve(request.result);
        request.onerror = ()=>reject(request.error ?? new Error('IndexedDB request failed'));
    });
}
export function txDone(tx) {
    return new Promise((resolve, reject)=>{
        tx.oncomplete = ()=>resolve();
        tx.onabort = ()=>reject(tx.error ?? new DOMException('Transaction aborted', 'AbortError'));
        tx.onerror = ()=>reject(tx.error ?? new Error('Transaction failed'));
    });
}
export function isQuotaExceededError(error) {
    return error instanceof DOMException && error.name === 'QuotaExceededError';
}
export function classifyStorageFailure(error) {
    if (!(error instanceof DOMException)) return 'unknown';
    switch(error.name){
        case 'QuotaExceededError':
            return 'quota-exceeded';
        case 'ConstraintError':
            return 'constraint';
        case 'TransactionInactiveError':
            return 'transaction-inactive';
        case 'AbortError':
            return 'aborted';
        case 'NotSupportedError':
        case 'InvalidStateError':
        case 'SecurityError':
            return 'unavailable';
        default:
            return 'unknown';
    }
}
export function isRetryableStorageFailure(kind) {
    return kind === 'quota-exceeded' || kind === 'unknown';
}
export async function openIndexedDb(options) {
    if (!('indexedDB' in globalThis)) {
        throw new DOMException('IndexedDB is not available', 'NotSupportedError');
    }
    const request = options.version === undefined ? indexedDB.open(options.name) : indexedDB.open(options.name, options.version);
    let upgradeError;
    request.onupgradeneeded = (event)=>{
        try {
            const tx = request.transaction;
            if (!tx) throw new Error('Missing IndexedDB upgrade transaction');
            options.upgrade?.(request.result, tx, event.oldVersion, event.newVersion);
        } catch (error) {
            upgradeError = error;
            request.transaction?.abort();
        }
    };
    request.onblocked = ()=>options.onBlocked?.();
    let db;
    try {
        db = await requestToPromise(request);
    } catch (error) {
        throw upgradeError ?? error;
    }
    if (upgradeError) {
        db.close();
        throw upgradeError;
    }
    db.onversionchange = ()=>{
        db.close();
        options.onVersionChange?.();
    };
    db.onclose = ()=>options.onClose?.();
    return db;
}
export async function withTransaction(db, stores, mode, fn, txOptions) {
    const tx = createTransaction(db, stores, mode, txOptions);
    const result = fn(tx);
    if (result && typeof result.then === 'function') {
        tx.abort();
        throw new Error('IndexedDB transaction callback must not return a Promise');
    }
    await txDone(tx);
    return result;
}
function createTransaction(db, stores, mode, txOptions) {
    try {
        return txOptions ? db.transaction(stores, mode, txOptions) : db.transaction(stores, mode);
    } catch  {
        return db.transaction(stores, mode);
    }
}
export async function getAllBounded(source, query, count = 100) {
    if (count <= 0) throw new RangeError('getAllBounded requires a positive count');
    if ('getAll' in source && typeof source.getAll === 'function') {
        return requestToPromise(source.getAll(query, count));
    }
    return new Promise((resolve, reject)=>{
        const results = [];
        const request = source.openCursor(query);
        request.onerror = ()=>reject(request.error ?? new Error('Cursor failed'));
        request.onsuccess = ()=>{
            const cursor = request.result;
            if (!cursor || results.length >= count) {
                resolve(results);
                return;
            }
            results.push(cursor.value);
            cursor.continue();
        };
    });
}
export function accountRange(accountKey) {
    return IDBKeyRange.bound([
        accountKey
    ], [
        accountKey,
        []
    ]);
}
export async function probeIndexedDbWrite(dbName = '__idb_probe__') {
    if (!('indexedDB' in globalThis)) return false;
    try {
        const db = await openIndexedDb({
            name: dbName,
            version: 1,
            upgrade (database) {
                if (!database.objectStoreNames.contains('probe')) {
                    database.createObjectStore('probe', {
                        keyPath: 'id'
                    });
                }
            }
        });
        await withTransaction(db, 'probe', 'readwrite', (tx)=>{
            tx.objectStore('probe').put({
                id: 'ok',
                value: true,
                updatedAt: new Date().toISOString()
            });
        });
        db.close();
        indexedDB.deleteDatabase(dbName);
        return true;
    } catch  {
        return false;
    }
}
