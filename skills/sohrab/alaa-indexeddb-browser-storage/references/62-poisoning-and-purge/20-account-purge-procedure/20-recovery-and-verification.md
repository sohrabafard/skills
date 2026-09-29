# Recovery and verification

**On the first app open after a session whose purge did not complete, delete every record whose
`accountKey` differs from the current session before rendering any user-scoped view.** The
`logoutPurgePending` marker detects it, and the boot sequence in `../../32-eviction-and-recovery.md` checks it.
Emit the deferred-purge event so the incidence is measurable.

## It must be bounded

Every user-scoped store carries an index whose first segment is `accountKey`, and the purge cursors
`IDBKeyRange.bound([accountKey], [accountKey, []])` — `O(matching + log n)` per store. A purge that
full-scans is `O(n)` per store and on a device with a large cache may not finish before the device changes
hands. A store without that index is not ready to hold user-scoped data
(`../../50-transactions-performance-and-query-patterns.md`).

## The sequence

1. Stop every sync loop and cancel in-flight flushes. 2. Write `logoutPurgePending`. 3. Purge each
user-scoped store, including orphan metadata, by the `accountKey` range. 4. Clear in-memory caches and reactive stores. 5. Broadcast
`logout-purge` so other tabs do the same (`../../41-multitab-versionchange-and-locks.md`). 6. Clear
`logoutPurgePending`. 7. **Verify**: a ranged count on each store for the previous `accountKey` returns
zero. If it does not, the purge failed and the marker stays set.

## Unsynced drafts

A draft the user has not submitted is never deleted silently by the purge. Either ask before discarding, or
bind it to a stated retention policy the user has seen. Silent deletion of unsent work is the one data-loss
case this pack treats as never acceptable.

## Account deletion

Deletion at the server does not reach the device. The next open — with a session for that account, or with
none — must find and remove the data. That is the same deferred-purge path, which is why the boot check
runs before any user-scoped view renders rather than lazily on first read.

## What is reported

Stores touched, counts removed per store bucketed, and whether a deferred purge was detected and completed.
Names are `/alaa-services-contract`; level and gate are
`/alaa-observability-soc`. Never log the `accountKey` or any record content.
