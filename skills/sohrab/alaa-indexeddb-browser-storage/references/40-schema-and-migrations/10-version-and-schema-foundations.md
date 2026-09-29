## Non-negotiable rules

- **Every object store and index is created or deleted inside `onupgradeneeded`.** No other transaction can.
- **The database version is a positive integer.** A semantic string is coerced, and not as you meant.
- **Every migration is idempotent: running it twice against the same database leaves the same state as
  running it once.** If one cannot be, it writes a `migration_journal` record with `nonIdempotent: true`
  naming the approver recorded in the feature's ADR, and that ADR is what review checks.
- **No network call, timer, crypto operation or application logic runs inside an upgrade transaction.** The
  transaction goes inactive while you wait and the upgrade fails on the far side of the await.
- **A destructive migration is never split into "clear in one transaction, refill in another".** A crash
  between them leaves the empty state permanently. One transaction, or the [shadow-copy strategy](./20-upgrade-and-migration-strategies.md#migration-strategies).
- **Every branch is `if (oldVersion < N)`**, never `switch` with fallthrough or equality. A user who has not
  opened the app since version 1 must run every branch in order.


## Names, and who owns them

**The database name, the version integer, and every object-store and index name are values, and values are
`/alaa-services-contract`.** Register the name before the code that creates it
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
