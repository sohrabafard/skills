# Concurrency, projections, query tuning, pooling, and Postgres failure behaviour

## Concurrency patterns

### Claim/work-queue pattern (Postgres)

For a table whose rows are claimed for processing:

- Claim with `FOR UPDATE SKIP LOCKED` so a second worker skips a locked row instead of blocking on it.
- Keep the claiming transaction short and set the status in the same statement, so a crash between claim and
  update cannot leave a row claimed by nobody.

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

The kit's outbox relay uses the same shape — `DELETE FROM outbox WHERE id IN (SELECT id FROM outbox ORDER BY id
FOR UPDATE SKIP LOCKED LIMIT $1) RETURNING …` at `outboxkit/queries.go:3-11` — and commits the delete only after
the publish is acknowledged (`outboxkit/doc.go:4-6`). It runs on the runtime lane, because `InTx` exists on
`pgkit.RuntimePool` and not on `MigratePool` (`pgkit/tx.go:21`). Relay tuning, retry behaviour, DLQ, and replay
are `/alaa-async-messaging` (`$alaa-async-messaging`); what this file owns is the claim query and the index that
serves it.

### Idempotency (DB-backed)

Assume at-least-once execution for every consumer and every job.

- Encode the dedupe key as a unique constraint and let the database reject the duplicate. Reason: a check-then-act
  in application code has a window between the check and the act, and at production concurrency that window is hit.
- Use `INSERT … ON CONFLICT DO NOTHING` or `DO UPDATE` for insert-if-absent semantics.
- Do not design for exactly-once delivery. It does not exist; idempotent handling is what replaces it.
- Whether a given path is idempotent is proven by a run-twice test — principle P7 in
  `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) for Go, and the idempotency doctrine
  is `/alaa-reliability-sla` (`$alaa-reliability-sla`) `references/60-idempotency.md`.

## Read-models and projections (CQRS-light)

### When to introduce a projection

Introduce one when the read query is expensive or frequent, when an aggregate is needed at scale, or when the read
shape differs enough from the write shape that serving it from truth tables would denormalize them. Do not
introduce one to avoid writing an index.

### Projection types

- View: cheapest to maintain, and still pays the full query cost at read time.
- Materialized view: needs a stated refresh strategy and a stated staleness bound before it ships.
- Summary table: updated by an async consumer, or by a trigger whose locking overhead is measured and documented.

### Update strategies

1. Async consumer off the outbox: the write-model transaction commits, the event is processed at least once, and
   the projection update is idempotent through a dedupe key, a unique constraint, or an upsert. This is the
   default.
2. Trigger: state the locking overhead, the failure mode, and how it is disabled and rolled back. A trigger runs
   inside the writer's transaction, so its cost is paid by every write.

How much staleness the read may carry is a consistency budget owned by `/alaa-system-design`
(`$alaa-system-design`) `references/30-data-and-consistency.md`. Bring it the freshness requirement; it decides.

## Query optimization workflow

1. Capture the exact query and its parameters as executed, not as written in the ORM.
2. Run `EXPLAIN (ANALYZE, BUFFERS)` and read it for sequential scans on large tables, row-estimate errors, sort or
   hash memory pressure, and lock waits.
3. Add the minimum effective index and re-run the plan. Buffers, not the plan text, decide whether it worked.
4. Only then rewrite the query for sargability — no function call wrapped around an indexed column in `WHERE` —
   or move the aggregate into a projection with an explicit refresh path.

When the loop count grows with tenants, rows, or history, `/alaa-algorithms-data-structures`
(`$alaa-algorithms-data-structures`) owns which of the four resolutions applies and the maximum the batch must
carry; this file owns the query and index shape the resolution lands on.

## Connection management

- Size the pool; do not raise `max_connections`. The shared Postgres is shared, and one service's burst becomes
  every service's outage.
- Pool ceilings, the per-container maxima, the fleet-wide percentage of `max_connections`, and the acquisition
  wait before a request fails are `alaa-services-contract`
  `references/22-failure-load-and-deprecation-contract.md`. The env keys and defaults for the data-store timeouts
  are `60-configuration-and-kit-gaps.md`. This file states neither.
- On the kit, `pgkit` runs two lanes: `RuntimePool` for request and worker traffic, and `MigratePool` capped at
  two connections — one for the advisory lock and one for the sequential migration or seed
  (`pgkit/pool.go:15-28`). Do not run request traffic on the migrate lane; its ceiling of two will serialize it.

### PgBouncer transaction-pooling guardrails

PgBouncer is in the path by default: `PG_SCALE_TIER` resolves blank to `small`, and `small`, `medium`, and `large`
all set `PgBouncer: true` (`pgkit/tier.go:26-29,34-35`). The scaffolded `pgbouncer.ini` runs `pool_mode =
transaction` (`scaffold/templates.go:4530,4538`). Write every query as though each transaction lands on a
different server connection, because under transaction pooling it can.

- Do not depend on session state across transactions: no temp table spanning transactions, no `LISTEN`/`NOTIFY`
  for application logic, no session-scoped advisory lock, no reliance on a per-session `SET` value.
- **Do not write `SET` or `SET LOCAL` into SQL on the runtime lane.** `linttools/pooledlane/pooledlane.go:16`
  forbids `LISTEN`, `NOTIFY`, `pg_advisory_lock`, `pg_advisory_unlock`, and any `SET <identifier>` on
  `pgkit.RuntimePool`, and its regex matches `SET LOCAL` as well — `pgkit/testdb/fence_test.go:39` uses
  `SET LOCAL statement_timeout = '1s'` as a negative fixture. The positive replacement is to carry the value as a
  bound query parameter and to bound the query with `context.WithTimeout`, which pgx honours. When the service
  genuinely needs a transaction-scoped GUC, that is a kit change request through `/alaa-go-chi-development`
  (`$alaa-go-chi-development`), not a rewrite that evades the check.
- `pg_advisory_xact_lock` is not matched by that regex and is permitted: it releases at commit, so it is safe
  under transaction pooling.
- **A clean `alaa_pooledlane` run is not proof that the lane is clean.** Detection is narrow by construction: the
  analyzer inspects only a string literal passed to `Exec`, `Query`, or `QueryRow` on an identifier declared
  `*pgkit.RuntimePool` in the same function (`pooledlane.go:36-58,83-113`). SQL held in a `const`, built with
  `fmt.Sprintf`, or executed through a repository wrapper is never examined. Read the SQL.
- **Server-side prepared statements are the platform default, not something to avoid.** `PG_PGBOUNCER_COMPAT`
  defaults to `"false"` (`configkit/keys.go:102`), which selects `pgx.QueryExecModeCacheStatement`
  (`pgkit/pool.go:72`) — prepares are cached on the server behind the transaction pooler, made safe by
  `max_prepared_statements = 200` in the scaffolded `pgbouncer.ini` (`scaffold/templates.go:4543`). Setting
  `PG_PGBOUNCER_COMPAT=true` switches to `pgx.QueryExecModeExec` (`pgkit/pool.go:70`), which sends the SQL text on
  every execution and costs a parse and a plan per call. Change the key only alongside a load test at realistic
  concurrency and a recorded reason, because the cost lands on every query in the service.
- `linttools` ships `alaa_structtag`, `alaa_metricname`, and `alaa_pooledlane` as analyzers, plus `uuiddefault`
  and `textnorm` as libraries rather than analyzers. Running the analyzers is necessary and is not sufficient.

## Postgres failure behaviour

Postgres is the source of truth, so it has no fallback. A request that cannot reach it fails; the question this
section answers is how it fails and what it holds while failing. The status code, the error code, and the event
name for each case are `alaa-services-contract` (`/alaa-services-contract`, `$alaa-services-contract`); the
doctrine of degrading rather than hanging is `/alaa-reliability-sla` (`$alaa-reliability-sla`)
`references/50-degradation.md`. What this file states is the mechanic and what it obliges in the repository.

- **Pool exhaustion.** `pgxpool.Acquire` blocks until the context deadline. A repository call made with a context
  that carries no deadline therefore waits without bound and the request occupies a worker while it waits. Every
  request-path query carries a deadline derived from the request context. The acquisition ceiling and the response
  it produces are the contract file's.
- **Deadlock, SQLSTATE `40P01`.** Postgres kills one of the two transactions and returns the error to it. Retry it
  only when the whole unit of work is idempotent; otherwise surface the failure. Prevention is a consistent lock
  ordering across every writer of the same tables, which is a design property and not a runtime setting.
- **Serialization failure, SQLSTATE `40001`.** Only under `REPEATABLE READ` or `SERIALIZABLE`. This one is
  designed to be retried, so a transaction using those levels ships with its retry path, not without.
- **Statement timeout, SQLSTATE `57014`.** Reaching the request-path deadline cancels the query; this is the
  intended behaviour and not an error to swallow. The server-side backstop does not exist on the kit yet —
  `60-configuration-and-kit-gaps.md` states the key, the default, and the change request.
- **Lock timeout, SQLSTATE `55P03`, and idle-in-transaction termination, SQLSTATE `25P03`.** Both need a server
  setting the kit does not expose today; same file, same change request.
- **Rollback is unbounded today.** `pgkit/tx.go:28,33` rolls back with `context.WithoutCancel(ctx)`, so a rollback
  against a wedged server holds its pooled connection with no ceiling and the exhaustion above follows. The
  ratified `PG_ROLLBACK_TIMEOUT` is not implemented. Keep transactions short and do no network I/O inside one; that
  is the only control available in a service today.
- **A degraded database is not a cache miss.** Do not add a fallback that serves business truth from Redis when
  Postgres is unreachable. Reason: it converts an outage the operator can see into silent stale answers the
  operator cannot.

Which proof level each of these needs before shipping is `/alaa-testing-strategy` (`$alaa-testing-strategy`)
`references/40-proof-strength.md`. The claim query and the deadlock ordering are provable at level 2 with a fake;
pool exhaustion and lock behaviour are level 6, against a real Postgres.
