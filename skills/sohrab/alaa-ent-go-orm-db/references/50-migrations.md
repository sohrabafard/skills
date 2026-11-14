# Migration planning, rollout, and recovery

This file owns the rollout and recovery of schema, index and data changes. [Indexes](40-index-design.md) owns selection; [runtime verification](70-runtime-testing.md) owns testing. The main skill owns execution authority.

## Baseline and plan

Inspect the migration history and checksums, the runner, the Ent, Atlas and PostgreSQL versions, the schema configuration, and the target revision. Assign one owner per object. Preserve framework and generated-code conventions, and verify locks and transaction boundaries. Block dependent work if target, baseline, ownership, or required tooling is unknown.

Use versioned production migrations; keep schema mutation out of production startup. Reserve `client.Schema.Create(ctx)` for disposable development and tests. Append-only behavior still locks. Resolve diffs instead of enabling WithDropColumn or WithDropIndex as a shortcut.

Use pinned project tools; route toolchain changes to [generation](10-go-and-generation.md). Prefer replay and diff on a verified disposable PostgreSQL that matches the target major version, extensions, schema, and collation. Never use production as the dev database, because replay and diff may reset or mutate it.

Adapt existing Ent and Atlas configuration or this command shape only after verifying the dev database:

```bash
atlas migrate diff contents_active_page \
  --dir "file://ent/migrate/migrations" \
  --to "ent://ent/schema" \
  --dev-url "$ENT_DEV_DATABASE_URL"
```

Exclude secrets, and verify the installed Atlas edition's capabilities. Review renames, rewrites, casts, requiredness, uniqueness and FKs, locks, index order and predicates, tenancy, and unrelated deletion. Match schema and migration state. An empty diff can mean wrong paths or omitted external objects.

Preserve the runner's format. After changing an unapplied Atlas migration, run `atlas migrate hash --dir "file://ent/migrate/migrations"`. Never rewrite applied history to hide drift. Keep schema changes separate from data changes; prefer historical SQL unaffected by later Go generation.

## Staged changes

Use the smallest rollout in which the old and new application versions stay compatible. Stage only when needed; empty tables need no automatic phase sequence.

| Phase | Required decision |
| --- | --- |
| Expand | Add compatible objects and temporary null and default semantics that coexist with old readers and writers. Preserve storage keys for code renames. |
| Backfill | Use bounded batches, stable progress keys, restartable predicates, concurrent-write protection, short transactions, and resumable progress. Set rate, lock, lag and failure limits. |
| Validate | Check population, duplicates, nulls and orphans, constraints, index validity, and query behavior. Application prechecks do not prove database enforcement. |
| Contract | Wait until all compatible application versions stop using old paths. State irreversible data effects and backup or forward-repair needs. |

For eligible CHECK and FK constraints, consider NOT VALID followed by validation. New and changed rows are checked while old rows await validation; validation still scans and locks. A validated `CHECK (col IS NOT NULL)` may avoid a second SET NOT NULL scan. Keep the proof constraint through the command that needs it; verify the server's supported path. UNIQUE differs: verify eligibility before attaching a concurrent unique index as a constraint.

Use a dedicated migration connection with bounded lock and statement waits. Keep lock timeout below a nonzero statement timeout when both apply. Never hold transactions across human waits or long application backfills.

## Concurrent indexes

Evaluate concurrent creation on busy tables: less write blocking costs additional work and waits. Check storage, long transactions, replication impact, timeouts, and recovery. Ent annotations do not enable concurrency.

CREATE INDEX CONCURRENTLY must run outside transaction blocks. For Atlas, use a separate file:

```sql
-- atlas:txmode none

CREATE INDEX CONCURRENTLY contents_active_page_idx
ON public.contents (tenant_id, status, created_at DESC, id DESC)
WHERE deleted_at IS NULL;
```

Inspect the file and runner configuration; an outer transaction still invalidates it. Verify `diff.concurrent_index` availability before relying on it. Check the target-version partition strategy; do not assume concurrent parent-index creation works.

Allow one concurrent build per table. After failure, inspect the actual index identity and definition, constraints, `pg_index.indisvalid`, and `indisready`. Invalid indexes can retain write overhead; failed concurrent unique indexes can still enforce uniqueness. IF NOT EXISTS proves neither matching definition nor validity. Identify the cause and the object before an approved drop and rebuild or a supported concurrent reindex. Do not retry DDL blindly.

## External objects and recovery

Assign desired-state ownership for composite FKs, expression indexes, native enums, extensions, views, triggers, RLS, domains, and composite types. [Advanced integration](80-advanced-ent.md) owns representation choices. Prevent competing owners and preserve external definitions in later diffs. Ent-only desired state can propose dropping replayed external objects; resolve ownership instead of accepting deletion.

The Ent functional-index composite-schema and RLS guides describe Atlas Pro dependencies. Check current entitlements before selecting that path. If unavailable, use an approved SQL workflow or supported extension that retains external objects. Do not initiate a login, purchase or publication to bypass a dependency. If tooling cannot represent or retain a required object, deliver SQL and mark integration blocked; preserve the invariant.

Separate rollback from nontransactional partial success. Inspect revisions and actual schema; identify committed and remaining statements. Preserve evidence and use documented runner recovery. Never advance revisions just to hide failure.

Verify relevant upgrades from a fresh database and from the current revision, negatives, nontransactional failures, and staged application compatibility through runtime verification. Return files and SQL, the exact target and revision, lock and data effects, dependencies and edition, checks run or skipped, and recovery limits. Distinguish prepared, tested, approved, and applied. Claim applied only after verified execution; stop at the requested authorized state.

Consult [Ent versioned migrations](https://entgo.io/docs/versioned-migrations/), [data migrations](https://entgo.io/docs/data-migrations/), and [Atlas transaction modes](https://www.atlasgo.io/versioned/apply) when adapting the runner. Use target-version [ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html) and [CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html) for lock, validation and concurrency restrictions. Refresh [functional-index](https://entgo.io/docs/migration/functional-indexes/) and [RLS](https://entgo.io/docs/migration/row-level-security/) prerequisites before those integrations; [source policy](00-sources.md) governs unavailable evidence.
