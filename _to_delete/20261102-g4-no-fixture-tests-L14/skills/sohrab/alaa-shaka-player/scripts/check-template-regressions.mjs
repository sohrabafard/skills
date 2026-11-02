#!/usr/bin/env node
// Node 24+ with --experimental-vm-modules. Runs real template functions against doubles;
// proves orchestration and queue ownership, not Vue rendering, media playback or networking.
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { stripTypeScriptTypes } from 'node:module';
import { SourceTextModule, SyntheticModule } from 'node:vm';

const deferred = () => {
  let resolve, reject;
  const promise = new Promise((ok, fail) => { resolve = ok; reject = fail; });
  return { promise, resolve, reject };
};
const tick = () => new Promise(resolve => setImmediate(resolve));

async function template(name, modules = {}) {
  const path = new URL(`../assets/templates/${name}.ts`, import.meta.url);
  const source = stripTypeScriptTypes(await readFile(path, 'utf8'), { mode: 'transform' });
  const module = new SourceTextModule(source, {
    identifier: path.href,
    importModuleDynamically: async specifier => modules[specifier],
  });
  await module.link(specifier => {
    assert.ok(modules[specifier], `Unexpected import: ${specifier}`);
    return modules[specifier];
  });
  await module.evaluate();
  return module.namespace;
}

async function synthetic(exports) {
  const module = new SyntheticModule(Object.keys(exports), function () {
    for (const [key, value] of Object.entries(exports)) this.setExport(key, value);
  });
  await module.link(() => { throw new Error('Unexpected synthetic import'); });
  await module.evaluate();
  return module;
}

async function playerFixture({ attach, destroy, onSessionEnd } = {}) {
  const callbacks = {};
  const counts = { attach: 0, destroy: 0, unload: 0, load: 0 };
  const players = [];
  let videoOwner = null;
  class Player {
    constructor() { this.listeners = new Map(); players.push(this); }
    emit(type) { for (const listener of this.listeners.get(type) ?? []) listener({}); }
    static isBrowserSupported() { return true; }
    async attach() { counts.attach++; videoOwner = this; await attach?.promise; }
    async destroy() { counts.destroy++; await destroy?.promise; this.emit("unloading"); videoOwner = null; }
    async unload() { counts.unload++; this.emit("unloading"); }
    async load() { counts.load++; this.emit("unloading"); this.emit("loading"); this.emit("loaded"); }
    configure() {}
    addEventListener(type, listener) {
      if (!this.listeners.has(type)) this.listeners.set(type, new Set());
      this.listeners.get(type).add(listener);
    }
    removeEventListener(type, listener) { this.listeners.get(type)?.delete(listener); }
    getStats() { return {}; }
  }
  const vue = await synthetic({
    ref: value => ({ value }), readonly: value => value,
    onMounted: callback => { callbacks.mount = callback; },
    onBeforeUnmount: callback => { callbacks.unmount = callback; },
    watch: (_source, callback) => { callbacks.change = callback; },
  });
  const shaka = await synthetic({ default: {
    Player, polyfill: { installAll() {} },
    util: { Error: { Code: {}, Severity: { RECOVERABLE: 1 } } },
  } });
  const { useShakaPlayer } = await template('useShakaPlayer', {
    vue, 'shaka-player/dist/shaka-player.ui.js': shaka,
  });
  const handle = useShakaPlayer({ source: { value: 'first' }, videoEl: { value: {} }, onSessionEnd });
  callbacks.mount();
  await tick();
  return { handle, callbacks, counts, players, videoOwner: () => videoOwner };
}

const { createQoeSink } = await template('playbackQoe');
const gate = deferred();
const sent = [];
const sink = createQoeSink(async batch => { sent.push(batch); if (sent.length === 1) await gate.promise; }, 2);
const a = { id: 'a' }, b = { id: 'b' }, c = { id: 'c' };
sink.enqueue(a); sink.enqueue(b);
const flushing = sink.flush();
sink.enqueue(c); // evicts a while [a,b] is being sent
await sink.flush(); // no second concurrent send
assert.equal(sent.length, 1);
gate.resolve(); await flushing; await sink.flush();
assert.deepEqual(sent, [[a, b], [c]]);

const sameGate = deferred();
const repeated = [];
const sameSink = createQoeSink(async batch => {
  repeated.push(batch); if (repeated.length === 1) await sameGate.promise;
}, 1);
sameSink.enqueue(a);
const first = sameSink.flush();
sameSink.enqueue(a); // a new queue entry, even though the record object is identical
sameGate.resolve(); await first; await sameSink.flush();
assert.deepEqual(repeated, [[a], [a]]);

let attempts = 0;
const retrySink = createQoeSink(async batch => {
  attempts++; assert.deepEqual(batch, [a]); if (attempts === 1) throw new Error('offline');
});
retrySink.enqueue(a); await retrySink.flush(); await retrySink.flush();
assert.equal(attempts, 2);
assert.throws(() => createQoeSink(async () => {}, 0), RangeError);

const destroy = deferred();
const fixture = await playerFixture({ destroy });
await fixture.callbacks.change(null, 'first'); await tick();
assert.equal(fixture.counts.unload, 1);
await fixture.callbacks.change('second', null); await tick();
assert.equal(fixture.counts.load, 2);
const disposal = fixture.handle.dispose();
assert.equal(fixture.handle.dispose(), disposal);
assert.equal(fixture.counts.destroy, 1);
let settled = false;
disposal.then(() => { settled = true; });
assert.equal(fixture.callbacks.unmount(), undefined); // the hook promises no blocking
await tick(); assert.equal(settled, false);
destroy.resolve(); await disposal;

const attach = deferred();
const pending = await playerFixture({ attach });
const pendingDisposal = pending.handle.dispose();
let pendingSettled = false;
pendingDisposal.then(() => { pendingSettled = true; });
await tick(); assert.equal(pendingSettled, false);
attach.resolve(); await pendingDisposal;
assert.equal(pending.counts.destroy, 1);
assert.equal(pending.counts.load, 0);

const failedDestroy = deferred();
const rejected = await playerFixture({ destroy: failedDestroy });
rejected.callbacks.unmount();
failedDestroy.reject(new Error('fixture teardown failure'));
await tick();
assert.deepEqual(rejected.handle.error.value, { kind: 'playback-failed', code: null });
console.log('PASS: queue-cap/send concurrency, repeated entries, retry retention, null-source unload, shared disposal, pending attach, hook rejection');

// Initial attach and obsolete cleanup share the video until destruction completes.
const firstAttach = deferred(), staleDestroy = deferred();
const race = await playerFixture({ attach: firstAttach, destroy: staleDestroy });
race.callbacks.change('latest', 'first'); await tick();
assert.equal(race.counts.attach, 1, 'new attach must wait for the old attach');
firstAttach.resolve(); await tick();
assert.equal(race.counts.destroy, 1);
assert.equal(race.counts.attach, 1, 'new attach must wait for stale destruction');
staleDestroy.resolve(); await tick(); await tick();
assert.equal(race.counts.attach, 2);
assert.equal(race.counts.load, 1);
assert.equal(race.videoOwner(), race.players[1]);
assert.equal(race.handle.ready.value, true);
await race.handle.dispose();

for (const reason of [null, undefined, false, 'cleanup failed', new Error('cleanup failed')]) {
  const blockedAttach = deferred(), blockedDestroy = deferred();
  const blocked = await playerFixture({ attach: blockedAttach, destroy: blockedDestroy });
  blocked.callbacks.change('replacement', 'first'); blockedAttach.resolve(); await tick();
  blockedDestroy.reject(reason); await tick(); await tick();
  assert.equal(blocked.counts.attach, 1, 'failed stale cleanup must prevent a new video owner');
  assert.deepEqual(blocked.handle.error.value, { kind: 'playback-failed', code: null });
  // Initialization has settled and left the pending set before this late disposal.
  const late = blocked.handle.dispose();
  assert.equal(blocked.handle.dispose(), late, 'late disposal must remain one shared promise');
  const outcome = await late.then(() => ({ status: 'resolved' }), cause => ({ status: 'rejected', cause }));
  assert.equal(outcome.status, 'rejected', 'known cleanup failure must not become teardown success');
  assert.equal(outcome.cause, reason, 'preserve even null or undefined rejection reasons');
  assert.equal(blocked.handle.dispose(), late, 'settled disposal must retain its promise');
  assert.equal(blocked.counts.destroy, 1, 'late disposal must not restart failed destruction');
}

let snapshots = 0;
const session = await playerFixture({ onSessionEnd: () => { snapshots++; } });
assert.equal(snapshots, 0, 'initial empty unloading is not a session');
session.callbacks.change('second', 'first'); await tick();
assert.equal(snapshots, 1);
const end = session.handle.dispose();
assert.equal(snapshots, 2, 'final snapshot precedes listener removal');
assert.equal(session.handle.dispose(), end); await end;
assert.equal(snapshots, 2, 'destroy must not emit a duplicate snapshot');
for (const listeners of session.players[0].listeners.values()) assert.equal(listeners.size, 0);

let reentrantDisposal;
const reentrant = await playerFixture({ onSessionEnd: () => { reentrantDisposal = reentrant.handle.dispose(); } });
const shared = reentrant.handle.dispose();
assert.equal(reentrantDisposal, shared, 'observer reentry must share the same disposal');
await shared; assert.equal(reentrant.counts.destroy, 1);

for (const raw of [null, undefined, 'failure', 7, false]) {
  const destruction = deferred();
  const unknown = await playerFixture({ destroy: destruction });
  unknown.callbacks.unmount(); destruction.reject(raw); await tick();
  assert.deepEqual(unknown.handle.error.value, { kind: 'playback-failed', code: null });
}
const observer = await playerFixture({ onSessionEnd: () => { throw null; } });
await observer.handle.dispose();
assert.equal(observer.counts.destroy, 1);
assert.deepEqual(observer.handle.error.value, { kind: 'playback-failed', code: null });

const issues = [];
let deliver = false;
const diagnostics = createQoeSink(async () => { if (!deliver) throw { secret: 'never publish' }; }, 1,
  status => { issues.push(status); throw new Error('observer failed'); });
diagnostics.enqueue(a); diagnostics.enqueue(b); await diagnostics.flush();
assert.deepEqual(diagnostics.status(), { pendingDepth: 1, inFlight: false, evictedCount: 1, sendFailureCount: 1 });
assert.equal(issues.length, 2);
assert.deepEqual(Object.keys(issues[0]).sort(), ['evictedCount', 'inFlight', 'pendingDepth', 'sendFailureCount']);
deliver = true; await diagnostics.flush();
assert.equal(diagnostics.status().pendingDepth, 0);
const asyncObserver = createQoeSink(async () => { throw null; }, 1, async () => { throw null; });
asyncObserver.enqueue(a); await asyncObserver.flush(); await tick();
assert.equal(asyncObserver.status().sendFailureCount, 1);
console.log('PASS: serialized initial attach/stale cleanup, exactly-once final snapshot, unknown rejection classification, bounded private delivery diagnostics, observer isolation');
