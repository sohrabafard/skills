# Schema & migration safety checklist

## Phased rollout discipline (default)
Prefer additive, reversible steps:
1) Add new nullable column / new table / new index (online-safe when possible)
2) Backfill in batches (idempotent, resumable)
3) Add constraints (`NOT VALID` + validate), then `SET NOT NULL`
4) Switch reads/writes to new path
5) Remove old columns/paths last (optional)

## Large tables and lock avoidance
- Use `CREATE INDEX CONCURRENTLY` for large tables (cannot run inside a transaction).
    - If your migration runner wraps migrations in a transaction, isolate this migration or use a raw SQL runner that does not wrap.
- Prefer `ADD CONSTRAINT ... NOT VALID` then `VALIDATE CONSTRAINT` to reduce lock impact.
- Avoid table rewrites in peak time (e.g., type changes that rewrite the table).
- Keep transactions short; never do network IO inside a transaction.
- If you need a backfill:
    - batch by PK / created_at window
    - use small batches + sleep/jitter
    - ensure restartability (store progress cursor)

## Partitioning (optional, only when justified)
Partitioning can help with very large, time-series-like tables, but increases ops complexity.
Only propose it if:
- retention/archival is required, OR
- a single table is demonstrably the bottleneck and partition pruning solves it.

# Multi-tenant patterns (choose and apply consistently)
Pick one strategy and stick to it:
1) Tenant column (`tenant_id` / `project_id`) on every tenant-owned row + composite indexes (recommended default)
2) Separate schemas/databases per tenant (ops-heavy, strong isolation)
3) RLS (Row Level Security) with a session variable set by middleware (strong isolation; use only if repo already does this)

Minimum rule: every query must be tenant-scoped.

## Index patterns (tenant column strategy)
Tie indexes to real query shapes (WHERE + ORDER BY):
- Feeds/time-ordered: `(tenant_id, created_at DESC)` (or ASC, matching query)
- Lookups: `(tenant_id, <business_key>)`
- Uniqueness/invariants: `UNIQUE (tenant_id, <business_key>)`
- Active rows: partial index (e.g., `WHERE deleted_at IS NULL`)
- If you must cover extra columns, consider `INCLUDE (...)` (Postgres) rather than widening the key.

## RLS notes (only if used)
If the repo uses RLS:
- Policies must be explicit and tested.
- Every request/transaction MUST set tenant context (e.g., `SET LOCAL app.tenant_id = ...`).
- Failure to set tenant context must fail closed (no cross-tenant reads).
