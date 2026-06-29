# Schema versioning, migrations, and concurrency

## Non-negotiable migration rules

- All object store and index creation/deletion happens inside `onupgradeneeded` / upgrade transaction.
- Database version is a positive integer. Do not use semantic strings directly as IndexedDB versions.
- Migrations must be deterministic, idempotent where possible, and tested from every supported old schema.
- Do not perform network calls during upgrade transactions.
- Do not run long application logic in upgrade transactions.
- Never split a destructive migration into “clear in one transaction, refill in another” unless the empty state is acceptable after crash. Prefer a single transaction or a recoverable shadow-copy pattern.
- Keep old connections cooperative: close on `versionchange`; handle new open `blocked` event with UI or reload prompt.

## DB naming policy

Prefer one app DB per origin/app family, with account/project keys inside records:

```text
DB name: alaa-client-storage
DB version: integer
Record namespace: accountKey = projectId:userId or anonymous-session
```

Benefits:

- Fewer DBs to upgrade.
- Less risk of many stale per-user DBs.
- Easier global cleanup and telemetry.

Use separate DBs only when there is a concrete reason:

- Strong deletion boundary per user.
- Third-party library owns its own schema.
- Very large independent storage domain with separate lifecycle.

## Object store naming

Use stable, plural, domain-specific names:

```text
meta
storage_items
capabilities
api_cache_entries
learning_state
wa_outbox
drafts
upload_resume_state
notification_state
sync_cursors
migration_journal
```

Avoid generic names like `data`, `cache`, or `items` unless scoped by a DB used by one feature only.

## Schema metadata

Keep a `meta` store:

```ts
type DbMeta = {
  key: string;
  value: unknown;
  updatedAt: string;
};
```

Suggested keys:

- `schemaVersion`
- `appBuildId`
- `lastSuccessfulOpenAt`
- `lastMigrationFrom`
- `lastMigrationTo`
- `lastCleanupAt`
- `capabilitySnapshot`

## Upgrade pattern

Use explicit old-version branches:

```ts
request.onupgradeneeded = (event) => {
  const db = request.result;
  const tx = request.transaction!;
  const oldVersion = event.oldVersion;

  if (oldVersion < 1) {
    db.createObjectStore('meta', { keyPath: 'key' });
    db.createObjectStore('learning_state', { keyPath: 'id' });
  }

  if (oldVersion < 2) {
    const outbox = db.createObjectStore('wa_outbox', { keyPath: 'id' });
    outbox.createIndex('byStatusRetryAt', ['status', 'retryAt']);
  }

  if (oldVersion < 3) {
    const drafts = db.createObjectStore('drafts', { keyPath: 'id' });
    drafts.createIndex('byAccountUpdatedAt', ['accountKey', 'updatedAt']);
  }
};
```

## Data migration strategy

### Safe additive migration

Best case:

- Create new store/index.
- New code writes new fields.
- Old records are migrated lazily when read or during background maintenance.

### Shadow-copy migration

For risky schema changes:

1. Create new store.
2. Copy/transform records in chunks after open, not necessarily inside upgrade.
3. Mark migration status in `migration_journal`.
4. Switch reads after successful copy.
5. Delete old store in a later schema version after telemetry confirms success.

### Lazy migration

For non-critical fields:

- On read, detect old record shape.
- Transform in memory.
- Write back normalized shape in a short transaction.
- Track migration count and errors.

## Multi-tab/versionchange handling

Every connection must attach:

```ts
db.onversionchange = () => {
  db.close();
  notifyUserOrReload('A new version is available. Please refresh.');
};

db.onclose = () => {
  markStorageUnavailableOrReopen();
};
```

Open requests should attach:

```ts
request.onblocked = () => {
  showUpgradeBlockedMessage();
};
```

Use `BroadcastChannel` where available:

```text
channel: alaa-storage
messages:
- db-upgrade-starting
- db-upgrade-blocked
- db-upgrade-complete
- storage-cleared
- logout-purge
```

Fallback to `storage` events or polling only when necessary.

## Transaction lifetime discipline

IndexedDB transactions auto-commit when control returns to the event loop and there are no pending requests. Some engines, especially WebKit/Safari, are stricter about transaction inactivity. Therefore:

- Do not hold a transaction open across unrelated `await`s.
- Do not call network, timers, crypto import, compression, or UI APIs inside an active transaction and then resume using it.
- Gather data before opening a transaction.
- Queue all IDB requests synchronously inside the transaction scope.
- Await transaction completion after scheduling requests.

Bad:

```ts
const tx = db.transaction('drafts', 'readwrite');
const store = tx.objectStore('drafts');
await fetch('/api/user');
store.put(record); // may throw TransactionInactiveError
```

Good:

```ts
const user = await fetchUserBeforeTransaction();
const tx = db.transaction('drafts', 'readwrite');
tx.objectStore('drafts').put({ ...record, userId: user.id });
await txDone(tx);
```

## Concurrency and locking

IndexedDB serializes conflicting transactions, but application-level invariants still need design.

Rules:

- Use one transaction for related writes across stores.
- Use idempotency keys for outbox writes.
- Use monotonic revision or `updatedAt` for conflict detection.
- Avoid read-modify-write across separate transactions when correctness matters.
- For cross-tab singleton sync jobs, use `navigator.locks` if available, otherwise a lease record with expiry and owner ID.

Lease record example:

```ts
type StorageLease = {
  key: string;
  ownerId: string;
  expiresAt: number;
  heartbeatAt: number;
};
```

## Upgrade tests

For every schema version:

- Fresh install opens successfully.
- Upgrade from previous version succeeds.
- Upgrade from oldest supported version succeeds.
- Upgrade with a second tab open triggers `blocked` UX.
- Old tab receives `versionchange` and closes.
- Failed migration leaves recoverable state.
- User reload during migration does not corrupt critical data.
- Private mode and quota-limited mode fail gracefully.
