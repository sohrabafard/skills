# Reading records back, and purging them

Two paths, one premise: **a record read out of IndexedDB is untrusted input.** It may be stale, from a
schema you no longer ship, or written by an attacker who had script execution in this origin an hour ago
and no longer does. Validation on read is what makes that earlier compromise non-persistent.

## Validation on read

Every read validates before use, including reads inside cleanup jobs.

```ts
function parseLearningState(value: unknown): LearningStateRecord | null {
  if (!isObject(value)) return null;
  if (value.schema !== LEARNING_STATE_SCHEMA) return null;   // wrong or absent version
  if (typeof value.id !== 'string') return null;
  if (typeof value.accountKey !== 'string') return null;
  // ... every field the caller will read
  return value as LearningStateRecord;
}
```

- **A `schema` field on every record, checked on every read.** An older-schema record is migrated
  (`40-schema-and-migrations.md`) or discarded. Never used as-is.
- **A record whose `accountKey` differs from the current session is not read.** It is deleted.
- **A validation failure deletes the record and continues.** A poisoned record that survives to be read
  again is a permanent failure; a deleted one is transient.
- **Never interpolate a cached value into HTML.** A cached string reaching `v-html` or `innerHTML` is
  stored XSS with a persistence layer the product built itself.
- **Verify the server revision before using a cached value for anything the user acts on.** A stale price,
  entitlement or deadline is worse than a spinner.

## Third-party scripts

Every script in the origin reads and writes this database. Keep third-party scripts off routes that read
`user_generated_unsynced` or `pii_moderate_high` data. Ship a Content Security Policy, and Trusted Types
where the framework allows — the policy itself is `/alaa-security-review` (`$alaa-security-review`) ground.
Audit tag managers: a tag manager is arbitrary script execution granted to whoever holds its console.
Isolate untrusted content in a sandboxed or cross-origin iframe, which gets its own storage partition.

## The logout and account-switch purge

A security operation. Two properties make it correct.

### It must be atomic, or journalled

A purge run as several independent transactions leaves the previous account's records readable if the tab
crashes, the browser is killed, or the device sleeps between them.

**One transaction across every user-scoped store** — correct and simple when the counts are small:

```ts
const tx = db.transaction(userScopedStores, 'readwrite');
for (const name of userScopedStores) deleteAccountRangeIn(tx.objectStore(name), accountKey);
await txDone(tx);
```

**Or a journalled purge**, when the counts are large enough that one transaction would block the UI. Write
the intent first, purge, then clear it:

```ts
await putMeta('logoutPurgePending', { accountKey, startedAt: nowIso });  // own transaction, before anything
// purge each store, chunked, each in its own transaction
await deleteMeta('logoutPurgePending');                                   // only after every store reports done
```

**On the first app open after a session whose purge did not complete, delete every record whose
`accountKey` differs from the current session before rendering any user-scoped view.** The
`logoutPurgePending` marker detects it, and the boot sequence in `32-eviction-and-recovery.md` checks it.
Emit the deferred-purge event so the incidence is measurable.

### It must be bounded

Every user-scoped store carries an index whose first segment is `accountKey`, and the purge cursors
`IDBKeyRange.bound([accountKey], [accountKey, []])` — `O(matching + log n)` per store. A purge that
full-scans is `O(n)` per store and on a device with a large cache may not finish before the device changes
hands. A store without that index is not ready to hold user-scoped data
(`50-transactions-performance-and-query-patterns.md`).

### The sequence

1. Stop every sync loop and cancel in-flight flushes. 2. Write `logoutPurgePending`. 3. Purge each
user-scoped store by the `accountKey` range. 4. Clear in-memory caches and reactive stores. 5. Broadcast
`logout-purge` so other tabs do the same (`41-multitab-versionchange-and-locks.md`). 6. Clear
`logoutPurgePending`. 7. **Verify**: a ranged count on each store for the previous `accountKey` returns
zero. If it does not, the purge failed and the marker stays set.

### Unsynced drafts

A draft the user has not submitted is never deleted silently by the purge. Either ask before discarding, or
bind it to a stated retention policy the user has seen. Silent deletion of unsent work is the one data-loss
case this pack treats as never acceptable.

### Account deletion

Deletion at the server does not reach the device. The next open — with a session for that account, or with
none — must find and remove the data. That is the same deferred-purge path, which is why the boot check
runs before any user-scoped view renders rather than lazily on first read.

## What is reported

Stores touched, counts removed per store bucketed, and whether a deferred purge was detected and completed.
Names are `/alaa-services-contract` (`$alaa-services-contract`); level and gate are
`/alaa-observability-soc` (`$alaa-observability-soc`). Never log the `accountKey` or any record content.
