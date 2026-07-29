# Multi-tab, service-worker, and lock coordination

One database, several writers: every tab, every worker, and the service worker. This file owns that
intersection. The service worker's own lifecycle, registration, routing and Cache API behaviour belong to
`/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`), `references/30-service-worker-excellence.md`.

## What the engine guarantees, and what it does not

**Guaranteed.** Two `readwrite` transactions with overlapping scopes are serialised. A transaction is
atomic: on abort nothing it wrote is visible.

**Not guaranteed.** Anything spanning two transactions. Read-modify-write across a transaction boundary is
a race the engine will not stop: two contexts read version 4, both write version 5, one update is lost, no
error anywhere. Every invariant wider than one transaction needs an application-level lock.

## Every connection carries these three handlers

```ts
db.onversionchange = () => {
  db.close();                       // unconditional, first, before any UI
  notifyThisContextToReload();
};
db.onclose = () => markStorageUnavailableAndReopenOnNextUse();
openRequest.onblocked = () => showUpgradeBlockedUx();   // "Close other tabs, then reload."
```

`db.close()` runs **before** the notification. A prompt awaited first holds the connection open, and the
upgrade in the other tab stays blocked for as long as the user ignores it — with no error and no timeout on
either side.

## The service-worker-versus-tab seam

A service worker is a fourth writer with three properties no tab has, each breaking an assumption that
holds between tabs.

**1. It has no UI, so it cannot participate in a blocked-upgrade prompt.** A tab that blocks can show
"close other tabs". A service worker holding an old connection blocks with nothing to show. Rule: **the
service worker opens the database with no version argument** — `indexedDB.open(name)` opens whatever
version exists and never triggers an upgrade — **and closes on `versionchange` immediately and
unconditionally.** The window owns the version integer; the service worker follows it.

```ts
// In the service worker. No version argument: never initiate an upgrade.
const request = indexedDB.open(DB_NAME);
request.onsuccess = () => {
  const db = request.result;
  db.onversionchange = () => db.close();   // no prompt, nothing to negotiate
};
```

A service worker that opens with a version integer will, on the first deploy that raises it, run the
migration with no user, no progress UI, and a lifetime the browser may end mid-transaction.

**2. It outlives every tab and can run with none open.** A `push` or `message` event wakes it, it writes,
and no tab observes the write. Rule: **every write it makes to a store a tab also reads is announced on the
shared `BroadcastChannel` after the transaction completes**, so an open tab is not left holding a stale
in-memory copy.

**3. The browser may terminate it between events.** Rule: **it never holds a claim across an event
boundary.** Anything it marks in progress must be recoverable by a reaper with a staleness threshold —
`71-browser-outbox.md` — because the context that made the mark may simply cease.

**The concurrent-write case.** A download runs in or through the service worker while tabs are open and
producing drafts and outbox rows. Three rules make it safe:

- **Disjoint store scopes wherever possible.** If the service worker only writes `api_cache_entries` and
  `offline_assets` and tabs only write `drafts`, `learning_state` and `wa_outbox`, the engine's own
  serialisation is the whole answer. Design for this first; it is the cheapest correct answer.
- **A named Web Lock for every store both write**, held across the read-modify-write, not merely across the
  transaction.
- **No context assumes exclusivity from being the only one running.** The service worker can wake at any
  time.

**The reciprocal pointer `alaa-quasar-app-vite-v3` should carry** in
`references/30-service-worker-excellence.md`:

> A service worker that writes IndexedDB opens the database with no version argument and closes on
> `versionchange` without prompting; the window owns the version integer. Concurrency between a
> service-worker write and a tab write, the shared `BroadcastChannel` vocabulary, and the Web Locks
> discipline are `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`),
> `references/41-multitab-versionchange-and-locks.md`.

## Web Locks

Baseline for this fleet — Chrome 69+, Firefox 96+, Safari 15.4+, caniuse 94.21%, read 2026-07-28 —
available in windows, workers and service workers. Use it for every cross-context singleton job: outbox
flush, cleanup sweep, chunked migration copy, offline download.

```ts
await navigator.locks.request('alaa:outbox-flush', { ifAvailable: true }, async (lock) => {
  if (lock === null) return;        // another context holds it; this pass does nothing
  await flushOutbox({ db, send, policy });
});
```

- `ifAvailable: true` is the right default for a periodic job: skip this pass rather than queue behind the
  other context and run twice in a row.
- A lock releases when the callback settles **and when the holding context dies**. That is why it beats a
  lease record: no expiry to tune, no stranded claim.
- Bound how long a caller waits with an `AbortSignal`. The timeout value is `/alaa-reliability-sla`
  (`$alaa-reliability-sla`).
- `steal: true` is almost always wrong here — it preempts a holder that may be mid-transaction.

**The lease-record fallback**, only for a runtime the probe reports without `navigator.locks`. It needs all
four fields or it is unimplementable:

```ts
type StorageLease = {
  key: string;          // the job name
  ownerId: string;      // per-context random id, regenerated every page load
  acquiredAt: number;
  expiresAt: number;    // acquiredAt + leaseTtlMs
};
```

`leaseTtlMs` default **30,000**; renewal every **10,000**, one third of the TTL so two missed renewals are
tolerated. Both are configuration named in `/alaa-services-contract` (`$alaa-services-contract`).
**Renewal**: the holder rewrites `expiresAt` each interval in a `readwrite` transaction. **Takeover**: only
when `now > expiresAt`, and only by a compare-and-set inside one transaction — read the row, verify
`expiresAt` is unchanged, write your own `ownerId`. A read-then-write across two transactions hands the
lease to two contexts. **Release**: delete the row on completion; a crash leaves it to expire, which is the
cost of not having Web Locks.

## `BroadcastChannel`

Baseline — Chrome 54+, Firefox 38+, Safari 15.4+, caniuse 94.82%, read 2026-07-28. Do not ship a
`storage`-event or polling fallback for it.

```text
channel: alaa-storage
messages:
  db-upgrade-starting  { toVersion }      db-upgrade-blocked  { toVersion }
  db-upgrade-complete  { version }        storage-cleared     { reason }
  store-written        { store, accountKey, origin: 'window' | 'service-worker' }
  logout-purge         { accountKey }
```

The message **names** are `/alaa-services-contract` (`$alaa-services-contract`). Two properties bind
regardless of the names: **a message is a hint that a store changed and never carries the record itself** —
the receiver re-reads — and **`logout-purge` is acted on before any user-scoped view renders**
(`62-poisoning-and-purge.md`).

## Concurrency rules

One transaction for related writes across stores. An idempotency key on every outbox write, so a duplicate
flush is harmless. A monotonic `updatedAt` or `serverRevision` on every record another context may write,
so a lost update is at least detectable. Never a read-modify-write across a transaction boundary where
correctness depends on it — hold the lock, do it in one transaction, or accept last-write-wins and say so
in the record's comment.
