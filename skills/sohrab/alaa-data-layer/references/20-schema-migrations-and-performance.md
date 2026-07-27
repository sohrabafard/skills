# Schema and migration safety

Every migration is reversible, or it records inside the migration why it is not, together with the mitigation.
Reason: a migration that cannot reverse turns a rollback into an incident, and the moment you need that fact is
the moment nobody has time to work it out.

Whether the pipeline proves reversibility, and the rollback window a release must survive, are
`/alaa-cicd-laravel-postgres` (`$alaa-cicd-laravel-postgres`) and `alaa-services-contract`
`references/22-failure-load-and-deprecation-contract.md` respectively. This file owns what a safe migration does.

## Phased rollout — the default shape

Expand, then migrate, then contract. Each step ships and is observed before the next begins:

1. Add the nullable column, the new table, or the new index.
2. Backfill in batches that are idempotent and resumable.
3. Add constraints as `NOT VALID`, then `VALIDATE CONSTRAINT`, then `SET NOT NULL`.
4. Switch reads and writes to the new path.
5. Remove the old column or path in a later release, after the artifact that stopped using it has outlived the
   rollback window.

Reason for the split: steps 1 to 4 leave the previous release able to run against the new schema, which is what
makes a rollback survivable. A drop in the same release as the code change removes that property.

## Large tables and lock avoidance

- `CREATE INDEX CONCURRENTLY` for any table with production row counts. It cannot run inside a transaction, so
  isolate it in its own migration or run it through a raw runner that does not wrap. A migration runner that wraps
  every migration in a transaction will fail this statement at execution, not at review.
- `ADD CONSTRAINT … NOT VALID` followed by `VALIDATE CONSTRAINT` shortens how long the lock is held; it does
  not lower the lock mode. Measured on PostgreSQL 16.13 this session, `ADD FOREIGN KEY` takes
  `SHARE ROW EXCLUSIVE` on the referenced table with or without `NOT VALID` — what `NOT VALID` removes is the
  referencing-table scan inside that window, not the mode. `VALIDATE CONSTRAINT` then runs under
  `SHARE UPDATE EXCLUSIVE` and does not block writes. Split the statement to shorten the hold, never in the
  belief that it takes a gentler lock, because a plan built on the gentler-lock belief will schedule the
  change into a window that cannot absorb it. A partitioned parent adds further constraints and a version
  gate: `/alaa-partitioned-table-fk-audit` (`$alaa-partitioned-table-fk-audit`)
  `references/20-lock-safety-and-the-fix.md` owns them.
- Do not run a table rewrite at peak. A type change that rewrites the table holds an `ACCESS EXCLUSIVE` lock for
  the length of the rewrite, and every reader queues behind it.
- Keep transactions short, and perform no network I/O inside one.
- Backfills: batch by primary key or by a `created_at` window, keep batches small with a pause between them, and
  store a progress cursor so a restart resumes rather than repeats.

On `alaa-go-chi`, migrations run on the migrate lane, which is capped at two connections — one for the advisory
lock and one for the sequential migration or seed (`pgkit/pool.go:25-28`). A migration that expects concurrency on
that lane will serialize instead. Runtime traffic stays on `RuntimePool`.

## Partitioning

Partitioning helps a very large, time-ordered table and costs ongoing operational complexity. Propose it only when
retention or archival is a requirement, or when one table is demonstrably the bottleneck and partition pruning is
what resolves it. A foreign key pointing into a partitioned parent has its own failure class, SQLSTATE 42830 —
`/alaa-partitioned-table-fk-audit` (`$alaa-partitioned-table-fk-audit`) owns it, and a migration that hits
"no unique constraint matching given keys" is that bug.

## Multi-tenant strategy

Pick one and apply it consistently across the service:

1. A tenant column on every tenant-owned row plus composite indexes. This is the default.
2. Separate schemas or databases per tenant: strong isolation, heavy operations.
3. Row-level security with a session variable set per request: strong isolation, and adoptable only where the
   repository already runs it.

Every query is tenant-scoped regardless of which is chosen; the boundary rules are in
`10-postgres-design-and-tenant-boundaries.md`.

## Index patterns for the tenant-column strategy

Tie every index to a real query shape — its `WHERE` and its `ORDER BY` together:

- Time-ordered feeds: `(tenant_id, created_at DESC)`, in the direction the query actually uses.
- Lookups: `(tenant_id, <business_key>)`.
- Invariants: `UNIQUE (tenant_id, <business_key>)`.
- Active-row queries: a partial index, for example `WHERE deleted_at IS NULL`.
- Extra columns needed only for projection: `INCLUDE (…)` rather than widening the key, so the key stays small
  enough to stay cheap.

The index a paginated route needs follows the ordering tuple that `/alaa-keyset-pagination`
(`$alaa-keyset-pagination`) derives; build it here, derive it there.

## Row-level security notes

If the repository uses RLS:

- Policies are explicit and tested; an untested policy is an assumption.
- Every request or transaction sets the tenant context, and failing to set it fails closed with no cross-tenant
  read.
- **RLS is not adoptable on the Go kit's runtime lane today.** Setting per-transaction tenant context requires a
  `SET`, which `linttools/pooledlane` forbids on `pgkit.RuntimePool` — see the rule and its positive replacement in
  `30-concurrency-projections-and-pooling.md`. Proposing RLS for a kit consumer is a kit change request through
  `/alaa-go-chi-development` (`$alaa-go-chi-development`), not a service-local workaround.
