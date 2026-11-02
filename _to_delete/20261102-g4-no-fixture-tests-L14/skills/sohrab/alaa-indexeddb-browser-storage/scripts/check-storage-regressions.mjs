#!/usr/bin/env node
// Node 24+. Real example functions with bounded IDB doubles; not browser or fake-indexeddb proof.
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { stripTypeScriptTypes } from 'node:module';

const cache = new Map();
async function sourceUrl(name) {
  if (cache.has(name)) return cache.get(name);
  let source = stripTypeScriptTypes(
    await readFile(new URL(`../examples/${name}.ts`, import.meta.url), 'utf8'), { mode: 'transform' },
  );
  for (const match of [...source.matchAll(/from\s+['"]\.\/([^'"]+)['"]/g)]) {
    source = source.replace(match[0], `from '${await sourceUrl(match[1])}'`);
  }
  const url = `data:text/javascript;base64,${Buffer.from(source).toString('base64')}`;
  cache.set(name, url);
  return url;
}
const { claimNextOutboxBatch, DEFAULT_OUTBOX_POLICY } = await import(await sourceUrl('outbox-pattern'));
const { reapOrphanedOutboxRows } = await import(await sourceUrl('outbox-reaper'));
const { AlaaClientStorage } = await import(await sourceUrl('alaa-client-storage'));
const { openIndexedDb } = await import(await sourceUrl('idb-core'));

// Only the compound string keys used in these scenarios. [] is an upper sentinel here.
const compare = (a, b) => {
  for (let i = 0; i < Math.min(a.length, b.length); i++) {
    if (Array.isArray(a[i])) return Array.isArray(b[i]) ? 0 : 1;
    if (Array.isArray(b[i])) return -1;
    if (a[i] !== b[i]) return a[i] < b[i] ? -1 : 1;
  }
  return Math.sign(a.length - b.length);
};
globalThis.IDBKeyRange = { bound: (lower, upper) => ({ lower, upper }) };
const rows = new Map();
const db = {
  transaction() {
    const tx = {
      objectStore: () => ({ index: () => ({ openCursor(range) {
        const request = {};
        let after = null;
        const advance = () => {
          const row = [...rows.values()]
            .sort((a, b) => compare([a.status, a.nextAttemptAt, a.id], [b.status, b.nextAttemptAt, b.id]))
            .find(item => {
              const key = [item.status, item.nextAttemptAt];
              return compare(key, range.lower) >= 0 && compare(key, range.upper) <= 0
                && (!after || compare([...key, item.id], after) > 0);
            });
          let continued = false;
          request.result = row ? {
            value: { ...row },
            update: value => rows.set(row.id, value),
            continue() {
              continued = true;
              after = [row.status, row.nextAttemptAt, row.id];
              queueMicrotask(advance);
            },
          } : null;
          request.onsuccess();
          if (!continued) setImmediate(() => tx.oncomplete?.());
        };
        queueMicrotask(advance);
        return request;
      } }) }),
    };
    return tx;
  },
};
for (const id of ['a', 'b', 'c']) rows.set(id, {
  id, status: 'queued', nextAttemptAt: '2020-01-01T00:00:00.000Z', attempts: 0,
});
const policy = { ...DEFAULT_OUTBOX_POLICY, batchSize: 2 };
assert.equal('sending' > 'queued', true);
assert.deepEqual((await claimNextOutboxBatch(db, '2021-01-01T00:00:00.000Z', policy)).map(r => r.id), ['a', 'b']);
assert.deepEqual((await claimNextOutboxBatch(db, '2021-01-01T00:00:00.000Z', policy)).map(r => r.id), ['c']);
assert.deepEqual(await claimNextOutboxBatch(db, '2021-01-01T00:00:00.000Z', policy), []);
const reaped = await reapOrphanedOutboxRows({ db, now: () => new Date('2021-01-01T00:10:00.000Z') });
assert.equal(reaped.reaped, 3);
assert.equal(reaped.inFlight, 0);
assert.equal((await reapOrphanedOutboxRows({ db })).reaped, 0);

let writes = 0, cleanups = 0;
const failures = [];
const facade = new AlaaClientStorage(
  failure => failures.push(failure), async () => { cleanups++; },
  async () => ({ transaction() { writes++; throw new DOMException('fixture', 'QuotaExceededError'); } }),
);
await assert.rejects(facade.set('a', { id: 'a' }), { name: 'QuotaExceededError' });
assert.equal(writes, 2); assert.equal(cleanups, 1);
assert.deepEqual(failures, [{ kind: 'quota-exceeded', userMustBeTold: true }]);

const sequence = [];
const connection = { close() { sequence.push('close'); } };
globalThis.indexedDB = { open() {
  const request = { result: connection };
  queueMicrotask(() => request.onsuccess());
  return request;
} };
const opened = await openIndexedDb({ name: 'fixture', onVersionChange() { sequence.push('notify'); } });
opened.onversionchange();
assert.deepEqual(sequence, ['close', 'notify']);
console.log('PASS: bounded claims/reaping, quota cleanup and exactly one retry, close-before-notify; IDB double only');

// Control-flow proof: no engine atomicity claim. Browser harness tests real commit/rollback.
const stores = ['learning_state', 'wa_outbox', 'drafts', 'upload_resume_state', 'storage_items'];
function purgeFixture(missingIndex = false) {
  let openedCursors = 0, aborted = 0, deletions = 0;
  const requests = [];
  const tx = {
    abort() { aborted++; queueMicrotask(() => tx.onabort()); },
    objectStore(name) { return {
      indexNames: { contains: () => !(missingIndex && name === 'storage_items') },
      index(indexName) {
        if (name === 'storage_items') assert.equal(indexName, 'byAccount');
        return { openCursor(range) {
          assert.equal(typeof tx.oncomplete, 'function', 'completion registered before cursor work');
          assert.equal(typeof tx.onabort, 'function');
          assert.deepEqual(range, { lower: ['gone'], upper: ['gone', []] });
          openedCursors++;
          const request = {};
          requests.push(() => {
            request.result = { delete() { deletions++; return {}; }, continue() {
              request.result = null; queueMicrotask(() => request.onsuccess());
            } };
            request.onsuccess();
          });
          return request;
        } };
      },
    }; },
  };
  const database = { transaction(names, mode) {
    assert.deepEqual(names, stores); assert.equal(mode, 'readwrite'); return tx;
  } };
  return { facade: new AlaaClientStorage(undefined, undefined, async () => database), tx,
    runCursors: () => requests.forEach(run => run()), counts: () => ({ openedCursors, aborted, deletions }) };
}
const missing = purgeFixture(true);
await assert.rejects(missing.facade.deleteByAccount('gone'), /schema upgrade required/);
assert.deepEqual(missing.counts(), { openedCursors: 0, aborted: 1, deletions: 0 });
const purge = purgeFixture();
const pendingPurge = purge.facade.deleteByAccount('gone');
let purgeSettled = false; pendingPurge.then(() => { purgeSettled = true; });
await new Promise(resolve => setImmediate(resolve));
purge.runCursors(); await new Promise(resolve => setImmediate(resolve));
assert.equal(purgeSettled, false, 'success must wait for transaction commit');
purge.tx.oncomplete();
assert.equal(await pendingPurge, 4, 'metadata must not inflate data-row count');
assert.deepEqual(purge.counts(), { openedCursors: 5, aborted: 0, deletions: 5 });
console.log('PASS: all-store preflight, immediate completion observation, metadata cursor/count, commit wait; control-flow double only');
