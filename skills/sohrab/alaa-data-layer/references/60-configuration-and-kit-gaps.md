# Data-store configuration: keys, defaults, and the gaps in the kit

Read this when choosing a data-store timeout, pool size, or retry count, and when the knob you need turns out to
have no environment key.

## The rule this file exists to enforce

Every data-store runtime value is settable per service through an environment key and carries a platform default
when that key is unset. Reason: two services sharing one Postgres and one Redis do not have the same latency
budget, and a value compiled into the kit forces a kit change request for a decision that belongs to the
deployment. A value that is neither an env key nor a documented default is an undocumented compile-time constant,
and nobody discovers it until an incident.

This file is the one place in the fleet that states an environment key name and a default for a **data-store**
knob. Every other platform value — request deadlines, outbound HTTP timeouts, retry budgets, page sizes,
application pool ceilings — lives in `alaa-services-contract`
`references/22-failure-load-and-deprecation-contract.md` (`/alaa-services-contract`, `$alaa-services-contract`).
Why a timeout, retry, backoff, breaker, backpressure, or degradation mechanism exists at all, and how to shape it,
is `/alaa-reliability-sla` (`$alaa-reliability-sla`). This file states keys and defaults only.

## The data-store keys and their defaults

| Key | Default | What `alaa-go-chi` does today | What that obliges |
|---|---|---|---|
| `REDIS_DIAL_TIMEOUT` | `1s` | no key; folded into the single 250 ms constant at `rediskit/config.go:15,87` | file a kit change request: the key is absent **and** the value is wrong |
| `REDIS_CALL_TIMEOUT` (read, write, pool wait) | `250ms` | no key; `DefaultCallTimeout = 250 * time.Millisecond` applied to ReadTimeout, WriteTimeout and PoolTimeout at `rediskit/config.go:88-90` | file a kit change request for the key; the value already agrees |
| `REDIS_MAX_RETRIES` | `-1` (disabled) | no key; `opts.MaxRetries = -1` at `rediskit/config.go:91` | file a kit change request for the key; the value already agrees |
| `REDIS_POOL_SIZE` | `32` | no key; `DefaultPoolSize = 32` at `rediskit/config.go:20`, always injected at `:54` | file a kit change request for the key; the value already agrees |
| `PG_STATEMENT_TIMEOUT` | `30s` on the runtime lane, `0` on the migrate lane | absent; `pgkit` sets no `statement_timeout` anywhere | file a kit change request |
| `PG_LOCK_TIMEOUT` | `3s` | absent | file a kit change request |
| `PG_IDLE_IN_TX_TIMEOUT` | `10s` | absent | file a kit change request |

A change request goes through `/alaa-go-chi-development` (`$alaa-go-chi-development`)
`references/20-change-request-workflow.md`. Do not add a local `replace` directive, a service-local Redis client,
or a service-local pool constructor to work around a missing key. Reason: the kit owns one timeout policy for the
whole fleet so that a single incident review can change every service at once, and a service-local copy is
invisible to that review.

## Why these numbers and not others

**A 250 ms dial budget is wrong; a 250 ms read and write budget is right.** Dialling covers DNS resolution, the TCP
handshake, and TLS where it is enabled, and on a cloud network that routinely exceeds 250 ms. Folding dial into the
command budget therefore fails the first request after every worker recycle, pod start, and connection reap; the
symptom looks like a random burst of cache errors and reproduces only under load. A read or a write on an
already-open connection is one round trip, and the fallback when it misses the budget is a Postgres query the
request could already afford, so 250 ms is a correct ceiling there.

**Retries stay disabled at the command layer.** Inside a 250 ms budget, behind a decorator whose miss path already
falls through to Postgres, a command retry only doubles latency before arriving at the same fallback. Retry belongs
at dial, where a fresh connection can succeed where the last one failed, and `rediskit/config.go:94` already sets
`DialerRetries = 1` there. `rediskit/config.go:84-85` states the kit's own position: the timeout, retry, and
connection budgets are kit invariants and a deployment URL must not silently weaken them — which is why weakening
them needs a key and a change request rather than a URL query parameter.

**`PG_STATEMENT_TIMEOUT` is a backstop, not a request budget.** A repository on the request path still passes a
tighter per-query deadline with `context.WithTimeout`, which pgx honours by cancelling the query. The server-side
statement timeout exists to kill a query whose caller has already gone — a detached background job, a connection
whose client crashed — so 30 s sits far above any request-path query and far below the time a runaway sequential
scan needs to exhaust the pool. The migrate lane gets `0` because `CREATE INDEX CONCURRENTLY` and a large backfill
legitimately run for hours, and a timeout there aborts a migration mid-flight.

## What the kit actually exposes today

`configkit/keys.go` owns the env surface. For the data lanes it is exactly:

- Postgres runtime: `PG_DSN`, or the components `PG_HOST`, `PG_PORT`, `PG_USER`, `PG_PASS`, `PG_DATABASE`,
  `PG_SSLMODE`; the matching `PG_MIGRATE_*` set for the migrate lane; `PG_SCALE_TIER` (default `small`),
  `PG_PGBOUNCER_COMPAT` (default `false`), `PG_MAX_CONNS` (default `20`).
- Redis: `REDIS_URL`, `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASS`, `REDIS_DB` (`configkit/keys.go:40-44`). That is the
  whole list — every timeout, retry, and pool value above is compile-time.
- ClickHouse: `CLICKHOUSE_ADDR`, `CLICKHOUSE_DATABASE`, `CLICKHOUSE_USER`, `CLICKHOUSE_PASSWORD`,
  `CLICKHOUSE_DIAL_TIMEOUT`. A blank `CLICKHOUSE_ADDR` means the lane is absent.
- Outbox: `OUTBOX_BATCH` (default `100`) and `OUTBOX_TICK` (default `500ms`), `outboxkit/config.go:10-14`. That is
  the whole outbox env surface.

`PG_SCALE_TIER` selects a band in `pgkit/tier.go:26-29`: `direct` runs without PgBouncer, and `small`, `medium`,
and `large` all run with it. A blank tier resolves to `small` at `pgkit/tier.go:34-35`, so **the default deployment
has PgBouncer in the path**, layered under a per-pod pgxpool. `scaffold/templates.go:4530,4538` emits a real
`pgbouncer.ini` with `pool_mode = transaction`. Treat PgBouncer as present unless the service sets
`PG_SCALE_TIER=direct`; the transaction-pooling consequences are in `30-concurrency-projections-and-pooling.md`.

## Postgres session parameters have no kit surface

`pgkit` writes exactly one `RuntimeParams` entry, `application_name` (`pgkit/pool.go:76`). It sets no
`statement_timeout`, no `lock_timeout`, and no `idle_in_transaction_session_timeout`, and `configkit` carries no key
for any of them.

One composition path exists today, and it is a deployment change rather than a code change: `PG_DSN` is an explicit
key that `configkit` passes through unchanged when set, overriding the component keys
(`configkit/keys.go:221-227`, proven by `configkit/dsn_test.go:157-158`), so a DSN carrying
`options=-c%20statement_timeout%3D30000` reaches pgx. Its cost is that the DSN becomes one opaque secret string:
the component defaults for port and SSL mode stop applying, and the option value needs URL escaping that is easy to
get wrong and produces a connection failure at boot rather than a warning.

Use that path only while an incident record is open that names the missing backstop, record it in the service's
deployment documentation with the change-request identifier beside it, and remove it when the key lands.
Otherwise run without the backstop and bound each query with `context.WithTimeout`, which is the request-path
budget in any case.

## Ratified but not implemented — do not treat as available

- `PG_ROLLBACK_TIMEOUT` was ratified as decision D-13 on 2026-07-22 and does not exist in code. `pgkit/tx.go:28,33`
  rolls back with `context.WithoutCancel(ctx)`, an unbounded rollback: against a wedged server it holds the pooled
  connection with no ceiling. Ratified is not implemented. Write code against source, never against a decision log.
- `outboxkit` has no publish timeout, no attempt counter, no backoff, and no quarantine.
  `outboxkit/relay.go:100-109` retries a failing publish forever on the tick loop. The additions that would change
  this (`OUTBOX_PUBLISH_TIMEOUT`, `OUTBOX_MAX_CONCURRENCY`, and the rest) are absent from code. Relay behaviour,
  DLQ, and replay belong to `/alaa-async-messaging` (`$alaa-async-messaging`); what this file records is that the
  knobs do not exist, so no service may be configured as though they do.

## Divergences to reconcile, not to resolve locally

Where a value here and a value in `alaa-services-contract` `references/22-failure-load-and-deprecation-contract.md`
disagree, that contract file is the fleet registry and the reconciliation is a change to it, filed through
`/alaa-services-contract`. Two are open today, both observed rather than inferred:

1. `22-…` records the service-to-Redis single-command hop as `500 ms` connect and `1000 ms` per attempt with no
   retries, while `rediskit` compiles `250 ms` for every phase. The command budgets agree in intent and differ in
   number; the dial budget differs in both.
2. `22-…` records `25` maximum open connections for a Go service, while `configkit/keys.go:39,103` defaults
   `PG_MAX_CONNS` to `20`.

Do not pick a side inside a service. Record which value the service runs on, and file the reconciliation.
