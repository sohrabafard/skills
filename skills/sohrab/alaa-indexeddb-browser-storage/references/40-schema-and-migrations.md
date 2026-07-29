# Schema versioning and migrations

## Non-negotiable rules

- **Every object store and index is created or deleted inside `onupgradeneeded`.** No other transaction can.
- **The database version is a positive integer.** A semantic string is coerced, and not as you meant.
- **Every migration is idempotent: running it twice against the same database leaves the same state as
  running it once.** If one cannot be, it writes a `migration_journal` record with `nonIdempotent: true`
  naming the approver recorded in the feature's ADR, and that ADR is what review checks.
- **No network call, timer, crypto operation or application logic runs inside an upgrade transaction.** The
  transaction goes inactive while you wait and the upgrade fails on the far side of the await.
- **A destructive migration is never split into "clear in one transaction, refill in another".** A crash
  between them leaves the empty state permanently. One transaction, or the shadow copy below.
- **Every branch is `if (oldVersion < N)`**, never `switch` with fallthrough or equality. A user who has not
  opened the app since version 1 must run every branch in order.

## Names, and who owns them

**The database name, the version integer, and every object-store and index name are values, and values are
`/alaa-services-contract` (`$alaa-services-contract`).** Register the name before the code that creates it
merges. `95-alaa-integration-playbook.md` lists what the `client` repository has already fixed.

One database per application family per origin, with `accountKey` on every user-scoped record.
`accountKey` is a storage partition for cleanup and cache isolation — not identity, not project authority,
not entitlement (`61-authority-boundary.md`). Open a second database only when a third-party library owns
its own schema, or a domain's lifecycle must be independent, or a deletion boundary must be enforceable by
deleting a whole database.

## The `meta` store

```ts
type DbMeta = { key: string; value: unknown; updatedAt: string };
```

Keys: `schemaVersion`, `appBuildId`, `lastSuccessfulOpenAt`, `lastMigrationFrom`, `lastMigrationTo`,
`lastCleanupAt`, `capabilitySnapshot`, `logoutPurgePending`.

**`schemaVersion` is written at the end of every upgrade, outside any version branch.** Writing it inside
the newest branch means the next author who adds a branch and forgets leaves it stale, and nothing detects
that.

## The upgrade shape

```ts
request.onupgradeneeded = (event) => {
  const db = request.result;
  const tx = request.transaction!;
  const oldVersion = event.oldVersion;

  if (oldVersion < 1) {
    db.createObjectStore('meta', { keyPath: 'key' });
    db.createObjectStore('migration_journal', { keyPath: 'id' });
  }

  if (oldVersion < 2) {
    const outbox = db.createObjectStore('wa_outbox', { keyPath: 'id' });
    // Both segments must be declared fields on the record type.
    outbox.createIndex('byStatusNextAttemptAt', ['status', 'nextAttemptAt']);
  }

  tx.objectStore('meta').put({
    key: 'schemaVersion', value: event.newVersion, updatedAt: new Date().toISOString(),
  });
};
```

**An index whose key path names a field the record does not carry is silently empty.** IndexedDB does not
error: records lacking the key path are simply not indexed, so the query that index exists for returns
nothing forever. `BrowserOutboxItem` carries `nextAttemptAt`; an index over `['status', 'retryAt']` against
it would return an empty batch on every flush and the outbox would never drain, with no error anywhere.
**Before creating any index, read the record type and confirm every segment of the key path is a declared
field on it.** `scripts/capability_contract_conformance.py --check-indexes` asserts this across the pack's
examples.

## Migration strategies

**Additive — the default.** Create the new store or index; new code writes the new fields; old records are
transformed on read. Nothing rewrites the store during upgrade, so the upgrade stays short and a crash
during it costs nothing.

**Lazy — for non-critical fields.** On read, detect the old shape, transform in memory, write the
normalised shape back in a short transaction outside the read. Count transformations and failures in
`migration_journal`; a lazy migration that never converges is one nobody is measuring.

**Shadow copy — for a change that cannot be additive.** Version `N` does only steps 1–3.

1. Create the new store in the upgrade transaction. Do not touch the old one.
2. After the open resolves, copy and transform in chunks outside the upgrade transaction, yielding between
   chunks.
3. Record progress in `migration_journal` after each chunk, so an interrupted copy resumes rather than
   restarts.
4. Switch reads to the new store only once the journal records the copy complete.
5. Delete the old store in version `N+1`, after telemetry shows the switch held.

A crash at any point leaves both stores intact and the journal states which is authoritative. That is the
property the split-transaction rule protects.

## Migration journal

```ts
type MigrationJournalEntry = {
  id: string;              // `${fromVersion}->${toVersion}:${step}`
  fromVersion: number;
  toVersion: number;
  step: string;
  status: 'started' | 'chunk-complete' | 'complete' | 'failed';
  processedCount: number;
  lastKey?: IDBValidKey;   // resume point for a chunked copy
  nonIdempotent?: true;
  approver?: string;       // required when nonIdempotent is true
  error?: string;
  updatedAt: string;
};
```

The journal is what makes an interrupted migration recoverable instead of ambiguous. Teaching shadow copy
without a journal is teaching half a pattern.

## What an upgrade owes other contexts

An upgrade blocks every other connection to the same database, including one held by the service worker.
`41-multitab-versionchange-and-locks.md` holds that sequence; do not design an upgrade without reading it.

## Upgrade tests

Eight, every version. Lanes are in `assets/browser-test-matrix.yaml`; proof levels are
`/alaa-testing-strategy` (`$alaa-testing-strategy`).

1. Fresh install opens at the current version. 2. Upgrade from the previous version. 3. Upgrade from the
oldest supported version, running every branch. 4. A second tab open fires `blocked` and the UX appears.
5. The old tab receives `versionchange` and closes. 6. A migration that throws leaves the previous
version's data readable. 7. A reload during a chunked copy resumes from the journal. 8. An upgrade under a
quota-limited profile fails without corrupting the previous version.
