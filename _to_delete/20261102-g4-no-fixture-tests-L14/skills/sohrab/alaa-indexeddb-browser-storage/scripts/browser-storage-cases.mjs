// Execute only in an isolated local origin. Real IndexedDB, synthetic non-user records.
import { openAlaaClientStorage, USER_SCOPED_STORES } from './examples/migration-pattern.js';
import { AlaaClientStorage } from './examples/alaa-client-storage.js';

const check = (condition, message) => { if (!condition) throw new Error(message); };
const request = req => new Promise((resolve, reject) => {
  req.onsuccess = () => resolve(req.result); req.onerror = () => reject(req.error);
});
const completion = tx => new Promise((resolve, reject) => {
  tx.oncomplete = resolve; tx.onabort = () => reject(tx.error ?? new Error('aborted'));
});
const rows = (db, name) => request(db.transaction(name).objectStore(name).getAll());
const open = name => openAlaaClientStorage({ config: { dbName: name, dbVersion: 4 } });

async function legacy(name, version) {
  const req = indexedDB.open(name, version);
  req.onupgradeneeded = () => {
    const db = req.result;
    for (const [store, keyPath] of [['meta', 'key'], ['migration_journal', 'id'], ['capabilities', 'key'], ['storage_items', 'id']]) {
      db.createObjectStore(store, { keyPath });
    }
    req.transaction.objectStore('storage_items').createIndex('byDataClassLastAccessedAt', ['dataClass', 'lastAccessedAt']);
    if (version === 3) {
      for (const name of USER_SCOPED_STORES) {
        const store = db.createObjectStore(name, { keyPath: 'id' });
        const [index, path] = name === 'drafts' ? ['byAccountTargetUpdatedAt', ['accountKey', 'targetType', 'targetId', 'updatedAt']]
          : name === 'wa_outbox' ? ['byAccountCreatedAt', ['accountKey', 'createdAt']] : ['byAccountUpdatedAt', ['accountKey', 'updatedAt']];
        store.createIndex(index, path);
        if (name === 'learning_state') store.createIndex('byContent', ['accountKey', 'contentId']);
        if (name === 'wa_outbox') store.createIndex('byStatusNextAttemptAt', ['status', 'nextAttemptAt']);
      }
    }
  };
  const db = await request(req);
  const tx = db.transaction(['meta', 'storage_items'], 'readwrite'); const done = completion(tx);
  tx.objectStore('meta').put({ key: 'survivor', value: true });
  tx.objectStore('storage_items').put({ id: 'legacy-orphan', accountKey: 'gone', updatedAt: 't' });
  await done; return db;
}

async function seed(db) {
  const facade = new AlaaClientStorage(undefined, undefined, async () => db);
  for (const accountKey of ['gone', 'keep']) {
    await facade.set(`learning-${accountKey}`, { id: `learning-${accountKey}`, schema: 1, accountKey,
      contentId: 'content', syncStatus: 'local', createdAt: 't', updatedAt: 't' });
  }
  const tx = db.transaction([...USER_SCOPED_STORES, 'storage_items'], 'readwrite'); const done = completion(tx);
  for (const name of USER_SCOPED_STORES.filter(name => name !== 'learning_state')) {
    for (const accountKey of ['gone', 'keep']) tx.objectStore(name).put({ id: `${name}-${accountKey}`,
      accountKey, createdAt: 't', updatedAt: 't', targetType: 'lesson', targetId: 'example' });
  }
  for (const accountKey of ['gone', 'keep']) tx.objectStore('storage_items').put({ id: `orphan-${accountKey}`, accountKey, updatedAt: 't' });
  await done; return facade;
}

async function snapshot(db) {
  return JSON.stringify(await Promise.all([...USER_SCOPED_STORES, 'storage_items'].map(name => rows(db, name))));
}

export async function runStorageCases() {
  const results = [];
  const prefix = `skill-idb-review-${crypto.randomUUID()}`;
  async function test(label, operation) {
    const name = `${prefix}-${results.length}`;
    try { await operation(name); results.push({ label, status: 'PASS' }); }
    catch (error) { results.push({ label, status: 'FAIL', error: error instanceof Error ? error.message : 'unknown failure' }); }
    // No database deletion: isolated synthetic fixtures remain inspectable on this origin.
  }
  await test('fresh v4 schema and lower configured-version rejection', async name => {
    const db = await open(name);
    try {
      check(db.version === 4, 'wrong version');
      check(db.transaction('storage_items').objectStore('storage_items').indexNames.contains('byAccount'), 'missing account index');
      let rejected = false;
      try { await openAlaaClientStorage({ config: { dbName: name, dbVersion: 3 } }); } catch (e) { rejected = e instanceof RangeError; }
      check(rejected, 'lower configured version accepted');
    } finally { db.close(); }
  });
  for (const version of [1, 3]) await test(`v${version} to v4 preserves rows and indexes legacy metadata`, async name => {
    const previous = await legacy(name, version);
    if (version === 3) await seed(previous);
    const before = version === 3 ? await snapshot(previous) : null;
    previous.close(); const db = await open(name);
    try {
      check((await rows(db, 'meta')).some(row => row.key === 'survivor'), 'legacy meta lost');
      const found = await request(db.transaction('storage_items').objectStore('storage_items').index('byAccount').getAll(['gone']));
      check(found.some(row => row.id === 'legacy-orphan'), 'existing metadata not indexed');
      if (before) check(await snapshot(db) === before, 'v3 user data or metadata changed');
    } finally { db.close(); }
  });
  await test('blocked v3 upgrade, versionchange and old-v3 VersionError', async name => {
    const held = await legacy(name, 3); let changed = false, blocked = false;
    held.onversionchange = () => { changed = true; };
    const db = await openAlaaClientStorage({ config: { dbName: name, dbVersion: 4 },
      onBlocked: () => { blocked = true; held.close(); } });
    db.close(); check(changed && blocked, 'missing upgrade notifications');
    let downgraded = false;
    try { (await request(indexedDB.open(name, 3))).close(); } catch (e) { downgraded = e.name === 'VersionError'; }
    check(downgraded, 'old explicit v3 opener unexpectedly succeeded');
  });
  await test('aborted additive upgrade preserves v3 and its rows', async name => {
    const previous = await legacy(name, 3); previous.close(); const req = indexedDB.open(name, 4);
    req.onupgradeneeded = () => {
      req.transaction.objectStore('storage_items').createIndex('byAccount', ['accountKey']); req.transaction.abort();
    };
    let aborted = false; try { await request(req); } catch (e) { aborted = e.name === 'AbortError'; }
    check(aborted, 'upgrade did not abort'); const db = await request(indexedDB.open(name, 3));
    try { check(db.version === 3 && (await rows(db, 'storage_items')).length === 1, 'abort lost v3 data'); }
    finally { db.close(); }
  });
  await test('production versionchange handler closes before notifying', async name => {
    let notified = false, closed = false;
    const db = await openAlaaClientStorage({ config: { dbName: name, dbVersion: 4 }, onVersionChange: () => {
      notified = true;
      try { db.transaction('meta'); } catch (e) { closed = e.name === 'InvalidStateError'; }
    } });
    const req = indexedDB.open(name, 5);
    const next = await request(req); next.close();
    check(notified && closed, 'production helper did not close before notification');
  });
  await test('missing account index fails before any deletion', async name => {
    const db = await legacy(name, 3);
    try {
      const facade = await seed(db); const before = await snapshot(db);
      let failed = false; try { await facade.deleteByAccount('gone'); } catch { failed = true; }
      check(failed, 'missing metadata index silently accepted');
      check(await snapshot(db) === before, 'preflight failure mutated data');
    } finally { db.close(); }
  });
  await test('purge all stores, orphan metadata, other account, data count and repeat', async name => {
    const db = await open(name);
    try {
      const facade = await seed(db); check(await facade.deleteByAccount('gone') === 4, 'count must exclude metadata');
      for (const name of [...USER_SCOPED_STORES, 'storage_items']) {
        const remaining = await rows(db, name);
        check(remaining.length > 0 && remaining.every(row => row.accountKey === 'keep'), `purge failed in ${name}`);
      }
      check(await facade.deleteByAccount('gone') === 0, 'repeat was not idempotent');
    } finally { db.close(); }
  });
  await test('forced abort after delete request rolls back every store', async name => {
    const db = await open(name); const original = IDBCursor.prototype.delete;
    try {
      const facade = await seed(db); const before = await snapshot(db); let deletes = 0;
      IDBCursor.prototype.delete = function () {
        const req = original.call(this); deletes++;
        if (deletes === 2) this.source.objectStore.transaction.abort();
        return req;
      };
      let failed = false; try { await facade.deleteByAccount('gone'); } catch { failed = true; }
      check(failed && deletes >= 2, 'failure was not injected after a delete');
      check(await snapshot(db) === before, 'partial purge committed');
    } finally { IDBCursor.prototype.delete = original; db.close(); }
  });
  return results;
}
