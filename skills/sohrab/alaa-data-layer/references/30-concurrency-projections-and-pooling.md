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
