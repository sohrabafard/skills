# Plan, review, and apply migrations safely

Read for PostgreSQL schema, index, external-object, or data migrations. This file owns planning, rollout, and recovery. Use [40-index-design.md](40-index-design.md) for index choice and [70-runtime-testing.md](70-runtime-testing.md) for runtime/testing. Follow main-skill execution authority.

## Contents

- [Resolve ownership and baseline](#resolve-ownership-and-baseline)
- [Generate a reviewable plan](#generate-a-reviewable-plan)
- [Expand, backfill, validate, contract](#expand-backfill-validate-contract)
- [Build indexes concurrently](#build-indexes-concurrently)
- [Manage external database objects](#manage-external-database-objects)
- [Recover and accept](#recover-and-accept)

## Resolve ownership and baseline

Inspect migration history, runner, checksums, Ent/Atlas versions, schema configuration, PostgreSQL version, and target revision. Assign each changed object to Ent or another migration owner. Preserve the working framework unless requested otherwise. Verify transaction boundaries and locks. Follow the repository convention for committing generated Ent code.

Prepare versioned production migrations; do not add schema mutation to every application startup. Reserve `client.Schema.Create(ctx)` for disposable development/tests. Append-only behavior does not prevent locking or operational harm. Resolve diffs deliberately instead of enabling `WithDropColumn(true)` or `WithDropIndex(true)` as a shortcut.

A migration request permits local planning under main-skill authority. It does not automatically approve production DDL, data deletion, installation, privilege changes, or paid provisioning. Prepare exact SQL, target, effects, validation, and recovery before required approval. Block dependent work when target, baseline, ownership, or tooling cannot be verified.

Sources: [Ent versioned migration](https://entgo.io/docs/versioned-migrations/), [automatic migration](https://entgo.io/docs/migrate/).

## Generate a reviewable plan

Use pinned project tools. Read [10-go-and-generation.md](10-go-and-generation.md) for generation or module/toolchain changes. Verify versions instead of copying tutorial Go, database images, or global CLI versions.

Prefer replaying history on disposable PostgreSQL matching the relevant target major, extensions, schema, and collation. Verify its identity first. Never use production as the dev database; replay/diff can reset or mutate it.

For existing Ent/Atlas workflows, adapt this command shape after verifying the dev database:

```bash
atlas migrate diff contents_active_page \
  --dir "file://ent/migrate/migrations" \
  --to "ent://ent/schema" \
  --dev-url "$ENT_DEV_DATABASE_URL"
```

`ENT_DEV_DATABASE_URL` must name an approved disposable database. Adapt paths or reuse existing environment configuration. Exclude secrets from committed configuration/output. Verify installed Atlas edition capabilities.

Review renames, rewrites, casts, requiredness, uniqueness, FK validation, locks, index order/predicates, tenant boundaries, and unrelated deletion. Confirm schema and migration describe the same state. Empty diffs can reflect wrong paths or missing external objects; investigate before declaring correctness.

Retain runner-compatible format. After editing an unapplied Atlas migration, run `atlas migrate hash --dir "file://ent/migrate/migrations"` to update `atlas.sum`. Do not rewrite applied history to hide drift. Separate data changes from schema changes. Prefer stable historical SQL; later Go generation must not change migration meaning.

Sources: [Ent diff workflow](https://entgo.io/docs/versioned-migrations/), [Ent data migrations](https://entgo.io/docs/data-migrations/), [Atlas apply and transaction modes](https://www.atlasgo.io/versioned/apply).

## Expand, backfill, validate, contract

Use the smallest rollout preserving old/new application compatibility. Apply these phases where staging is needed, not automatically for an empty table:

1. **Expand:** Add compatible objects with explicit temporary null/default semantics. Make new reads/writes coexist with the previous version. Preserve storage keys for code-only renames.
2. **Backfill:** Use bounded batches, stable progress keys, restartable predicates, and short transactions. Protect concurrent writes. Define rate, lock, lag, and failure limits. Save resumable progress; one giant transaction is not a recovery strategy.
3. **Validate:** Check population, duplicates, nulls, orphans, index validity, and query behavior. Verify database constraints separately from application prechecks.
4. **Contract:** Remove old paths only after every compatible application version stops using them. Obtain required destructive-work approval. State irreversible data effects and backup/forward-repair requirements.

For eligible CHECK/FK constraints, consider `NOT VALID` followed by validation. Adapt this rollout shape to existing names, data, and lock budgets:

```sql
ALTER TABLE public.contents
  ADD CONSTRAINT contents_duration_nonnegative
  CHECK (duration_ms >= 0) NOT VALID;

ALTER TABLE public.contents
  VALIDATE CONSTRAINT contents_duration_nonnegative;
```

New/changed rows are checked while old rows await validation. Validation still scans and locks. Verify the server-supported NOT NULL path. A validated `CHECK (col IS NOT NULL)` can avoid a second scan during SET NOT NULL. Keep that check through the command needing its proof. UNIQUE uses a different path: verify eligibility for attaching a concurrent unique index as a constraint.

Bound lock waits and operations on a dedicated migration connection. Keep lock timeout shorter than nonzero statement timeout when both matter. Avoid holding transactions across human waits or long application backfills.

Sources: [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html), [client timeouts](https://www.postgresql.org/docs/current/runtime-config-client.html), [Ent data migrations](https://entgo.io/docs/data-migrations/).

## Build indexes concurrently

For busy tables, evaluate concurrent creation against deployment constraints. It reduces write blocking but adds work/waits. Check storage, long transactions, replication impact, lock timeout, and recovery. Ent annotations do not make migrations concurrent.

Run `CREATE INDEX CONCURRENTLY` outside transaction blocks. For Atlas, use a separate file with this directive:

```sql
-- atlas:txmode none

CREATE INDEX CONCURRENTLY contents_active_page_idx
ON public.contents (tenant_id, status, created_at DESC, id DESC)
WHERE deleted_at IS NULL;
```

Inspect file and runner configuration; an outer transaction still invalidates this operation. Verify availability before relying on Atlas `diff.concurrent_index` planning. Choose a version-specific partition strategy; do not assume concurrent parent-index creation works.

Allow one concurrent index build per table; expect load and waits. Inspect catalogs/constraints after failure. Invalid indexes can retain write overhead; failed concurrent unique indexes can still enforce uniqueness.

Read index identity/definition and `pg_index.indisvalid`/`indisready`. `IF NOT EXISTS` proves neither matching definition nor validity. Identify cause and exact object before planning approved drop/rebuild or supported concurrent reindex. Follow the main skill's retry bound; do not retry DDL blindly.

Sources: [PostgreSQL CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html), [Atlas transaction directive](https://www.atlasgo.io/versioned/apply), [Atlas concurrent diff planning](https://www.atlasgo.io/versioned/diff).

## Manage external database objects

Give composite FKs, functional indexes, enums, extensions, views, triggers, RLS, domains, and composite types explicit desired-state ownership. Use [80-advanced-ent.md](80-advanced-ent.md) for representation/integration. Assign one owner per object; prevent competing creation/deletion.

Ent's functional-index composite-schema and RLS guides document Atlas Pro requirements. Refresh exact entitlements before use. Without paid features, use an approved SQL workflow or supported extension retaining external objects during diffs. Do not initiate login, purchase, or publication to bypass missing dependencies.

Document externally owned definitions and retention during future diffs. Ent-only desired state can propose deleting replayed external objects. Resolve ownership rather than accepting such deletion. If the runner cannot represent/retain a required object, deliver SQL and report blocked integration. Preserve its invariant.

Sources: [Ent functional indexes](https://entgo.io/docs/migration/functional-indexes/), [Ent RLS](https://entgo.io/docs/migration/rls/), [Ent multi-schema migration](https://entgo.io/docs/multischema-migrations/).

## Recover and accept

Separate rollback from nontransactional partial success. Inspect revisions and actual schema before recovery. Never advance revisions merely to hide failure. Identify committed and remaining statements. Preserve evidence and follow documented runner recovery.

Use [70-runtime-testing.md](70-runtime-testing.md) for relevant empty/current-revision upgrades, data/constraint negatives, and nontransactional partial failures. Check staged application compatibility. Verify PostgreSQL-specific behavior on PostgreSQL with target extensions; SQLite smoke tests cannot prove it.

Return SQL/files, target/revision, lock/data effects, dependencies/edition, observed/unrun checks, and recovery limits. Distinguish prepared, tested on a disposable database, approved, and applied states. Claim applied only after verified execution. Stop at the requested authorized state; preparation does not imply production execution.
