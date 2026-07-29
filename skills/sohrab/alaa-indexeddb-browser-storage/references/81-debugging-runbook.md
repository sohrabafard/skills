# Debugging runbook

You are holding a live symptom. Find it, take the first action, escalate if it does not resolve.

## Data the application wrote is missing

1. **Is the whole origin gone, or one store?** Check whether Cache API entries also vanished. Both gone is
   eviction (`32-eviction-and-recovery.md`). One store gone is a schema fault.
2. **Is `meta.lastSuccessfulOpenAt` present?** Absent, with a prior session recorded outside IndexedDB, is
   eviction or the WebKit seven-day truncation.
3. **Does the record's `accountKey` match the session?** A mismatch means the account switched and the
   purge worked. Not a defect.
4. **Did the schema change?** Compare `meta.schemaVersion` with the code's version. A store created in a
   branch the user never ran does not exist for them.
5. **Is the index empty rather than the store?** Query the store directly by key. Record present but index
   empty means the key path names a field the record does not carry (`40-schema-and-migrations.md`). This
   is silent by design and is the highest-yield check on this list.
6. **Did cleanup delete it?** Check the cleanup event and the `dataClass` the record was written with. A
   record written with one taxonomy while cleanup reads another is either never cleaned or cleaned first.
7. **Is this private mode?** Read the persisted capability tier.

## `TransactionInactiveError`

1. **Find the `await` inside the transaction.** There is one — a `fetch`, a timer, a crypto call, a dynamic
   import, or an await on a promise that resolves in a later task.
2. **Is it Safari or iOS only?** WebKit ends an idle transaction sooner than Chromium, so the same code
   passes on Chrome. That is the spec's timing being enforced, not a bug to work around.
3. **Fix:** gather every input before opening the transaction, queue every request synchronously, await
   only `txDone` (`50-transactions-performance-and-query-patterns.md`).

## The upgrade never completes

1. **Did `blocked` fire?** Another connection holds the old version.
2. **Which contexts are open?** Count the tabs — **and the service worker**, the one invisible in the tab
   list that blocks just as hard.
3. **Does the service worker open with a version argument?** It must not
   (`41-multitab-versionchange-and-locks.md`).
4. **Does every connection close on `versionchange` before showing UI?** A prompt awaited before
   `db.close()` holds the upgrade for as long as the user ignores it.
5. **Fix:** broadcast `db-upgrade-starting`, close every other connection, retry, show the reload prompt if
   it stays blocked. **Never delete the database to resolve it.**

## `QuotaExceededError`

`31-quota-exceeded-and-cleanup.md`, class 1: estimate, identify the data class, free refetchable data in
the stated order, retry once, drop a tier — and tell the user if the write was their unsent work.

## A route is slow, and it was fast in staging

1. **Count the transactions the route opens.** More than one per rendered view is the N+1 family.
2. **Find the unbounded read** — `getAll()` with no count, or a cursor continuing past what it needs.
3. **Check the record count on the affected account.** Staging accounts are new; production accounts have
   two years of history. The bound, not the measurement, is what predicts this.
4. **Count the indexes on the store being written.** Every index is maintained on every `put`; a write path
   that slowed after an index was added has its answer here.
5. **Is a migration running?** A lazy migration rewriting records on read makes the first visit after a
   deploy slow. Check `migration_journal`.

## The outbox stops draining

1. **Count rows by status.** Rows piling in `sending` is the orphan class — run the reaper
   (`71-browser-outbox.md`). Rows in `queued` with `nextAttemptAt` in the past means no flush trigger
   fired.
2. **Is the scheduling index returning anything?** An empty batch on a non-empty queue is the empty-index
   defect: check `['status', 'nextAttemptAt']` names real fields.
3. **Is a 401 loop burning attempts?** A 401 must pause the flush without incrementing `attempts`. Rows
   reaching `abandoned` shortly after a session expiry means the classification is wrong.
4. **Is the Web Lock held by a dead context?** It is not — a lock releases when its context dies. If
   nothing flushes, the trigger is missing, not the lock.
5. **Are rows `abandoned` with no report?** Every abandonment is reported; silence there is the defect.

## An offline download is not playable

1. **Is the record `downloadState: 'storing'`?** A partial download — restart it; there is no resume API
   (`72-offline-media-store.md`).
2. **Does the player's own store still list the asset?** If not it was evicted: delete the local record,
   tell the user, fall through to online playback.
3. **Was persistence ever granted?** Read the stored `persisted()` answer. A best-effort download that
   disappeared is behaving as documented, not failing.
4. **Anything about the player itself** — track selection, licences, manifest, progress — is
   `/alaa-shaka-player` (`$alaa-shaka-player`).

## Two tabs disagree about what is stored

1. **Is the write broadcast after the transaction completes?** A message sent before commit tells the other
   tab to read data that is not there yet.
2. **Does the message carry the record?** It must not — it carries the store name and the receiver
   re-reads.
3. **Is there a read-modify-write across a transaction boundary?** A lost update, with no error raised.
   Hold the named lock, or do it in one transaction.
4. **Did the service worker write?** It is the writer nobody remembers
   (`41-multitab-versionchange-and-locks.md`).
