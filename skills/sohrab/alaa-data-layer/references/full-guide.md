# Purpose
Make data-layer changes safe, fast, and operable under high concurrency, while remaining auditable and minimal-diff:

- Postgres schema + migrations + indexing tied to real query patterns
- Truth-first OLTP design (core tables in 3NF/BCNF when easy; integrity enforced in DB)
- Large-table migration safety (lock avoidance, phased rollout, rollback discipline)
- Multi-tenant boundary enforcement and index strategies
- Concurrency patterns (`FOR UPDATE SKIP LOCKED`, idempotency via unique constraints)
- Connection pooling (PgBouncer) + timeouts to protect the DB
- PgBouncer transaction-pooling guardrails (session-state hazards, prepared statements, `SET LOCAL`)
- Read-models/projections (VIEW/MATERIALIZED VIEW/summary tables) that do not corrupt the write-model truth
- Audit/append-only history for business-critical facts (avoid silent overwrites)
- Redis patterns (cache-aside, key design, invalidation, locks, rate limiting, memory/eviction safety)

This skill is Laravel-friendly but applies to raw SQL too.

# When to use
- Designing/changing schema, constraints, migrations
- Adding/optimizing indexes for hot queries
- Troubleshooting slow endpoints / background jobs (p95/p99, CPU/IO, lock waits)
- Planning pooling/timeouts and concurrency strategies
- Enforcing multi-tenant boundaries (tenant isolation correctness)
- Designing read-models / projections / derived aggregates (counts, last_state, summaries)
- Designing Redis cache keys/invalidation, locks/idempotency, rate limits, or debugging eviction/memory pressure

# Hard constraints
- Do NOT introduce a new datastore (e.g., MongoDB) unless the user explicitly requests it.
- Prefer minimal diffs; avoid unrelated refactors.
- Every index MUST be justified by a concrete query pattern.
- Every migration MUST be reversible, OR explicitly documented as non-reversible with rationale + mitigation.
- Never commit secrets (DB/Redis passwords, certs, connection strings).
- If Redis is used as a queue backend with Horizon, use `alaa-async-messaging` for worker/Horizon ops; this skill focuses on safe primitives.

# Postgres design policy (Production, Multi-Tenant)

## A) Core principle — write-model is the source of truth
- Design core OLTP tables in 3NF (or BCNF when it is easy and doesn’t harm clarity).
- Avoid duplicate “editable” truth:
    - If a value can be edited, keep exactly one authoritative column for it in the write-model.
- Denormalization is forbidden in core truth tables unless:
    - you can point to measured query patterns proving it is necessary, AND
    - the exception is documented as a deliberate design trade-off.

## B) Enforce integrity in the DB (not only in code)
Use DB constraints to encode invariants:
- `NOT NULL`, `FK`, `UNIQUE`, `CHECK`
- Prefer explicit referential actions and document intent:
    - `ON DELETE RESTRICT` / `CASCADE` / `SET NULL`
    - `ON UPDATE RESTRICT` / `CASCADE`

Rule of thumb: default to `RESTRICT` unless the business/domain model clearly requires cascades.

## C) Multi-tenant boundary (must be enforced)
Baseline rules:
- Every tenant-scoped table MUST include `tenant_id` (NOT NULL). Any row without `tenant_id` is a bug.
- Any uniqueness rule MUST be tenant-aware:
    - use `UNIQUE (tenant_id, ...)` unless global uniqueness is explicitly required.
- Frequent query indexes MUST lead with `tenant_id` to prevent cross-tenant scans.
- Every query MUST be tenant-scoped by default (`WHERE tenant_id = ?`).
    - Cross-tenant access requires an explicit, audited “system/admin” path (not an accidental code path).

Tenancy strategy:
- Use ONE clear strategy and document it:
    - default: shared schema + `tenant_id` (recommended)
    - if using RLS: define policies and require `SET LOCAL` tenant context per request/transaction

## D) Read performance without corrupting truth
- Build read-models explicitly:
    - `VIEW` / `MATERIALIZED VIEW` / summary tables (CQRS-light)
- Separate truth tables vs projections:
    - truth tables are normalized and authoritative
    - projections are derived, rebuildable, and may be eventually consistent

Derived fields (counts, last_state, aggregates):
- Must have a defined update strategy:
    - async/outbox consumer updates (preferred for scale)
    - controlled triggers (only if proven safe; document overhead and locking)
- Updates must be idempotent (at-least-once safe).

## E) Audit & operations
- Prefer append-only/audit tables for history.
- Do not overwrite business-critical facts without an audit trail.
- Indexing must match real query patterns; migrations must be lock-safe and rollback-aware.

## F) Identifier naming policy (mandatory)
- For PostgreSQL-first repositories, new persistence identifiers MUST default to lower_snake_case:
    - tables, columns, indexes, constraints, sequences, join tables, foreign-key names, and check-constraint names
- Do not introduce new mixed-case identifiers that require double quotes in PostgreSQL.
- Do not treat ORM convenience as a reason to mirror camelCase API or PHP names into schema identifiers.
- If a repository already has quoted mixed-case identifiers, treat them as explicit legacy debt:
    - prefer a planned cleanup or rebuild path over extending the mixed-case surface
    - document any temporary compatibility layer and the exact removal path
- When using Doctrine DBAL, Laravel schema tooling, or raw SQL together, choose one canonical unquoted identifier spelling and keep it stable across migrations, models, tests, and docs.

# Postgres performance principles (performance-first)
- Prefer simple, predictable queries and stable indexes.
- Avoid OFFSET pagination on large tables; use keyset pagination.
- Avoid N+1; fetch in batches and/or eager-load deliberately.
- Indexes speed reads but slow writes; keep the minimum effective set.
- Prefer constraints (PK/FK/UNIQUE/CHECK) to encode invariants; they are also an optimization tool.

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

# Concurrency patterns

## Claim/work-queue pattern (Postgres)
For “claim one row for processing” tables:
- Use `FOR UPDATE SKIP LOCKED` to reduce contention.
- Keep the transaction short and update status atomically.

Example claim pattern:
```sql
WITH cte AS (
  SELECT id
  FROM jobs
  WHERE status = 'pending'
  ORDER BY created_at
  FOR UPDATE SKIP LOCKED
  LIMIT 1
)
UPDATE jobs
SET status = 'processing', started_at = now()
WHERE id IN (SELECT id FROM cte)
RETURNING *;
```

## Idempotency (DB-backed)
Assume at-least-once execution for consumers/jobs:
- Prefer DB unique constraints for dedupe keys.
- Use insert-if-not-exists semantics:
    - `INSERT ... ON CONFLICT DO NOTHING`
- Do not rely on “exactly once”.

# Read-models / projections (CQRS-light)

## When to introduce a projection
Use projections when:
- the read query is expensive or frequent
- you need aggregates (counts, summaries) at scale
- you need different shapes optimized for reads without polluting truth tables

## Projection types
- View: cheapest to maintain, may still be expensive at runtime
- Materialized view: rebuild/refresh strategy must be defined
- Summary table: updated by async consumer (preferred) or controlled trigger

## Update strategies (choose and document)
1) Async/outbox consumer (recommended):
- write-model transaction commits
- outbox/event processed at-least-once
- projection updates idempotently (dedupe keys / unique constraints / upserts)
2) Controlled triggers (use sparingly):
- document locking overhead, failure modes, and how to disable/rollback safely

# Query optimization workflow (deterministic)
1) Capture the exact query + parameters (as executed).
2) Run:
- `EXPLAIN (ANALYZE, BUFFERS)` and inspect:
    - sequential scans on big tables
    - mis-estimates (stats) → consider `ANALYZE`, extended stats, or better predicates
    - sort/hash memory pressure
    - lock waits / row count explosions
3) Add the minimum effective index; re-check the plan.
4) Only if necessary:
- rewrite query for sargability (avoid functions on indexed columns in WHERE)
- move heavy aggregates to projections/materialized paths (with explicit invalidation/refresh)

# Connection management (pooling + timeouts)
- Prefer PgBouncer for pooling under high concurrency (especially with many app workers).
- Avoid “just increase max_connections”; size with pooling.
- Baseline safety timeouts (tune per environment and workload):
    - `statement_timeout`
    - `lock_timeout`
    - `idle_in_transaction_session_timeout`
- Ensure app worker counts + pool sizes do not exceed DB capacity.

## PgBouncer transaction-pooling guardrails (high-leverage)
If PgBouncer uses **transaction pooling**, treat DB connections as non-sticky:
- Do NOT depend on session state across transactions:
    - avoid temp tables spanning multiple transactions
    - avoid `LISTEN/NOTIFY` for app logic
    - avoid advisory locks that assume session affinity
    - avoid relying on per-session `SET` values
- Prefer `SET LOCAL ...` inside transactions and avoid `SET ...` that assumes a session.
- Prepared statements:
    - transaction pooling can break server-side prepared statements depending on PgBouncer/client behavior
    - safest default is to avoid relying on server-side prepares unless explicitly validated
    - treat prepared-statement strategy as an environment-level decision and load-test it under realistic concurrency
- With transaction pooling, write SQL and app behavior as if each transaction may land on a different server connection.

# Redis patterns (cache, locks, rate limiting) for high throughput
Use Redis deliberately for caching, rate limiting, and distributed coordination.
Redis is fast, but memory is finite; design keys and TTLs as a first-class schema.

## Cache key design (mandatory)
Use namespaced, tenant-aware keys. Recommended shape:
- `{app}:{env}:{tenant}:{resource}:{id}:{version}`
  Example:
- `comment-service:prod:project_123:thread:01J...:v1`

Rules:
- Always include tenant in multi-tenant caches.
- Always include a version segment (`v1`, `v2`) to enable safe “version bump” invalidation.
- Normalize high-cardinality inputs (avoid raw URLs/user agents as-is).

## TTL discipline (mandatory)
- Every cache key MUST have an explicit TTL.
- Prefer short TTLs for volatile data.
- If correctness is strict, prefer event-driven invalidation (below) over long TTLs.
- Never rely on in-process globals for caching under Octane; caching must be explicit and key-based.

## Invalidation strategy (prefer event-driven)
- Keep invalidation rules close to the write path:
    - On write: emit domain event → invalidate relevant keys.
- Avoid global flushes in production.
- If tags are used (when available), document tag semantics and tenant isolation.
- Prefer “version bump” invalidation for wide fan-out keys when precise invalidation is too expensive:
    - move `:v1` → `:v2` in the key schema and let old keys expire.

## Locks (baseline)
Use Redis locks for short critical sections, not for long workflows.
- `SET key value NX PX <ttl_ms>`

Mandatory:
- TTL = worst-case critical section time + buffer
- retry with backoff + jitter
- define behavior on failure (return error vs queue retry)

Failure modes to document:
- lock not acquired (contention)
- lock expires mid-work (TTL too low)
- process crash (lock released via TTL)

## Idempotency keys (edge dedupe)
For “exactly-once-like” behavior at the edge:
- Write a dedupe key with TTL:
    - `SET idempo:<key> <result_ref> NX EX <seconds>`
      But for critical side effects (money/legal/audit):
- also enforce dedupe with a DB unique constraint (preferred)

## Rate limiting
Prefer token bucket or sliding window.
Rules:
- limits must be tenant-aware (and user-aware if required)
- use atomic operations (Lua script or known atomic patterns)
- document:
    - scope (per IP / per user / per tenant)
    - window/refill rate
    - reject behavior (HTTP status + stable internal error code)

## Memory and eviction safety
- Monitor:
    - `maxmemory` and eviction policy
    - hit rate, evictions, key cardinality, top memory keys
- Avoid storing large payloads; store IDs and fetch from DB when needed.
- Avoid unbounded key growth:
    - add TTL
    - normalize keys
    - cap lists/sets by trimming

Operationally useful commands (examples):
- `INFO memory`
- `MEMORY STATS`
- `SCAN 0 MATCH <pattern> COUNT 1000` (sampling, not full scan in prod peak)
- `SLOWLOG GET`

# Verification / Definition of Done
When applying this skill, output (at minimum):
1) Truth vs projection decision:
- which tables are truth, which are projections (if any)
- any intentional denormalization and the measured query evidence for it
2) The exact query patterns driving indexes (or a short list of endpoints/jobs).
3) Proposed schema/index/constraint changes + why (tie each to a query/invariant).
4) Migration-safe steps (online/lock notes; phased rollout; rollback).
5) If projections/derived fields exist:
- update strategy (async/outbox vs trigger)
- idempotency/dedupe strategy
- rebuild/refresh strategy (if materialized)
6) If PgBouncer is used:
- pool mode (session vs transaction) and any session-state hazards
- prepared-statement stance (validated or avoided)
7) If Redis is involved:
- key formats + TTL choices
- invalidation hooks (which writes/events invalidate which keys)
- lock/rate-limit patterns + timeouts
- failure modes + what to monitor
8) How to verify:
- Postgres: `EXPLAIN (ANALYZE, BUFFERS)` (and `pg_stat_statements` if available)
- Redis: hit rate/evictions/key growth signals from your ops tooling

# Anti-patterns
- Adding speculative indexes “just in case”.
- Denormalizing truth tables without measured evidence and documentation.
- OFFSET pagination on large tables.
- Unbounded Redis keys (no TTL).
- Cache keys that omit tenant identifier (cross-tenant leakage risk).
- Non-tenant-scoped queries in multi-tenant systems.
- Cross-tenant reads/writes through non-audited code paths.
- Long transactions that include network IO.
- `CREATE INDEX CONCURRENTLY` inside a transaction.
- Using Redis alone for idempotency on critical side effects without DB dedupe.
- Using Redis locks for long workflows (lock TTL will betray you).
