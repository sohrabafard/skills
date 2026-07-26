# Octane full guide — mechanics

Invariants 1 to 3 (values that may never be retained, sites that may never retain them, the three
reset mechanisms) are in `SKILL.md` and are not repeated here.

## Where an SDK's own per-request scope belongs

An SDK that keeps its own per-request scope — an error reporter, a tracer — is reset by mechanism 3
in `SKILL.md` (a `RequestTerminated` listener), because the container cannot flush state the SDK
holds internally. Whether that reset is required, and at what level, is owned by
`/alaa-observability-soc` (`$alaa-observability-soc`) `references/60-sentry-and-profiling.md`.

## Request-scoped tenant context

Tenant identity is derived, never read from a client-supplied field; derivation is owned by
`/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`). This section governs only how the derived
value is held.

- The current-tenant holder is a `scoped` binding — never a `singleton`, `static`, or provider
  property.
- **The classic cross-tenant leak** is an Eloquent global scope, a builder macro, or a validation
  rule registered once at boot whose closure resolves the tenant holder. The closure lives for the
  worker's life; if it captured a resolved holder, every later request on that worker filters by
  request 1's tenant. Register the closure once, but resolve the holder **inside the closure body on
  each call**, so a flushed `scoped` binding is re-resolved.
- Every cache, memoization, lock, rate-limit and `Octane::table()` key holding tenant-specific data
  includes the trusted tenant identifier. This is the only place in this skill stating that rule;
  key *shape* is owned by `alaa-data-layer references/50-redis-laravel-octane.md`
  (`/alaa-data-layer`, `$alaa-data-layer`).
- Postgres RLS session variables set by middleware are request state living on a **connection** that
  outlives the request. If the repo uses RLS, reset the variable in a `RequestTerminated` listener
  on every connection the request touched, not only the default one; otherwise the next request on
  that worker inherits the previous tenant's row visibility.

## Driver detection and the three drivers

`config('octane.server')` returns `swoole`, `roadrunner`, or `frankenphp`. All three are in scope.
Only Swoole provides `Octane::concurrently()`, `Octane::table()`, the `octane` cache store, ticks
and intervals; guard every use behind the driver check.

- Code outside a runtime adapter uses Laravel, PSR and Symfony abstractions only. Swoole APIs,
  coroutine assumptions and task-worker dispatch live behind one adapter the driver check selects,
  so a driver change is one file.
- **FrankenPHP**: a PHP warning or notice emitted during request startup can shut the worker down.
  Fix the warning; never suppress it with `@` or by lowering `error_reporting`.
- **Do not read superglobals.** `$_GET`, `$_POST`, `$_SERVER`, `$_FILES`, `$_COOKIE` are not
  reliably populated under any worker driver. Read the `Request`.
- Exact syntax, configuration keys, Caddyfile and `.rr.yaml` details: upstream
  `octane-development/SKILL.md` and the vendor docs in `source-map.md`. Not owned by this
  repository; on any retention rule this skill wins.

## Configuration under a worker

Configuration is resolved **before** the application is bootstrapped, so low-level worker boot code
must not call `config()`, `app('config')`, or resolve any container service, and must never assume
`php artisan config:cache` has run. Resolve configuration after boot, inside the consuming class.
Validate Octane's knobs once per worker in a provider `boot()` — driver matches the guarded code
paths, a recycle limit is set, worker counts fit the container CPU quota
(`references/load-and-backpressure.md`) — so a wrong knob fails the worker at boot instead of
degrading under load.

## `Octane::concurrently()` and Swoole tables

Both Swoole-only; guard the driver first.

- **Non-serializable capture is the failure mode.** A `concurrently()` closure is serialized for a
  task worker, so capturing a `PDO` connection, an Eloquent model, an open stream, or `$this` throws
  a serialization error. Pass scalar identifiers and re-fetch inside the closure. Results arrive in
  input order; catch exceptions inside the closure when you must transform or log before Octane
  rethrows.
- **Swoole tables** are pre-sized at boot as `'name:maxRows'`, cannot be resized, and writing past
  the maximum **may fail silently** — check the write result rather than assume it landed. Contents
  are lost on worker restart, so a table is never the only copy of business truth. Use `incr()` and
  `decr()` for counters; there are no transactions and a read-then-write pair is not atomic.

## The three cache tiers

Pick the tier from the lifetime the data is allowed to have.

| Tier | Mechanism | Lifetime | Use for |
| --- | --- | --- | --- |
| Per request | `Cache::memo()` — a scoped binding, flushed each request | one request | repeated reads of one value in one request |
| Cross request, cross replica | Redis, with an explicit TTL | until invalidated or expired | derived data shared between requests and instances |
| Per server | `octane` store and `Octane::table()`, Swoole only | until worker or server restart | host-local, high-frequency, non-authoritative data |

- A `static` or global used as "a free cache" is not a tier; it is the bug class.
- `once()` on an object the worker resolved once caches for the worker's life, not the request's —
  see the named upstream override in `SKILL.md`.
- The per-server tier never substitutes for shared Redis in a multi-replica deployment: replicas
  disagree and every entry vanishes on restart.
- What to cache, key shape, TTL, invalidation, stampede control, and the repository-pattern gate
  that must pass before any caching is added: `alaa-data-layer
  references/50-redis-laravel-octane.md`.

## Redis and database connections under long-lived workers

A connection lives as long as the **worker**, not the request. **Verified as of 2026-07** against
the versions in `references/source-map.md`. Re-check trigger: on any `laravel/octane` upgrade, any
Redis-client change, and any edit to the listener list in `config/octane.php`, re-run the
`connected_clients` check below before keeping or removing the listener, and record here the version
at which it stopped reproducing.

- Reuse across requests is the intended performance win.
- **Do not add a per-request disconnect** unless `connected_clients` on the Redis instance rises
  monotonically with worker process uptime while request rate is flat. That observable is the only
  thing that authorises a connection-lifecycle change, and the remedy is the listener below — never
  a `disconnect()` in a request handler, which discards the reuse and pays a TCP and AUTH handshake
  per request.
- Known upstream defect `laravel/octane#1094`: Octane can leave Redis connections lingering after
  request termination. When the observable above is present, register an `OperationTerminated` /
  `RequestTerminated` listener that disconnects the Redis manager, mirroring the commented-out
  database disconnect in `config/octane.php`.
- **Never capture a `Redis` connection or a `Cache` store instance inside your own singletons**
  (Invariant 2). Resolve through the facade or manager at each use, so the client's retry and
  reconnect logic applies after a drop or a recycle.
- Use phpredis with `persistent` plus `persistent_id`, so worker recycling (`--max-requests`) does
  not pay a fresh TCP and AUTH handshake per recycle.
- Configure client resilience in `config/database.php`: `max_retries` with `backoff_algorithm`
  (`decorrelated_jitter`), explicit `timeout` and `read_timeout`, so a worker holding a dead
  connection recovers on the next call rather than hanging. Doctrine: `/alaa-reliability-sla`
  (`$alaa-reliability-sla`); every value: `alaa-services-contract
  references/22-failure-load-and-deprecation-contract.md`.

**Connection-count ceiling.** `workers × connections per worker` — cache, session, queue and lock
connections each count — must stay under the Redis server's `maxclients`, summed across every
service and replica sharing that instance. The per-container database pool maximum is a platform
value in `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`. This is
the only place in this skill stating the arithmetic; `references/load-and-backpressure.md` points
here before a worker count is raised.

**Redis unreachable.** A worker must boot and serve with Redis down, so **providers must not read
cache, sessions or `Redis::` in `register()` or `boot()`** — under a worker that turns a Redis
outage into a crash-loop before one request is served. Provider discipline:
`/alaa-laravel-architecture` (`$alaa-laravel-architecture`). Failover store, decorator fallback and
the fail-open versus fail-closed decision per call site: `alaa-data-layer
references/50-redis-laravel-octane.md`. Acceptance check, run in the target environment: stop
Redis, run `octane:start`, confirm workers boot and requests degrade instead of 500-looping.

## Hot-path cost under a long-lived worker

Boot cost is amortised across requests. **Per-request cost is not.** "The worker is warm" is never a
reason to skip eager loading, widen a query, or accept an extra round trip. Complexity budgets,
structure choice and the whole N+1 family: `/alaa-algorithms-data-structures`
(`$alaa-algorithms-data-structures`). Specific to a long-lived worker:

- Anything allocated and left reachable from a long-lived object is held for the worker's life, so a
  one-off allocation becomes a permanent floor in worker RSS.
- Stream large datasets with `cursor()`, `lazy()` or a generator instead of materialising an array,
  so the peak stays transient. `memory_get_peak_usage()` reports the peak since process start under
  a worker; call `memory_reset_peak_usage()` to open a per-request measurement window.
- Encode and decode at the boundary once per request; validate a payload's schema once.
- Reuse one `DateTimeImmutable` rather than constructing per iteration, and keep reflection and
  `__get`/`__call` dispatch out of hot paths: under a worker these costs are paid per request, not
  once per process.

## Transactions and lost updates

- **Read-modify-write on a row concurrent requests can touch loses updates.** Do not read a value,
  compute in PHP, then write it back. Use one atomic statement (`increment()`, `decrement()`, an
  `update()` with a `DB::raw` expression), or take the row with `lockForUpdate()` inside
  `DB::transaction()`.
- Keep `DB::transaction()` bodies short and free of external IO. A transaction held open across an
  HTTP call occupies both a database connection and one unit of the concurrency ceiling
  (`references/load-and-backpressure.md`).

## Async offload

Offload slow or IO-heavy work rather than blocking a request worker, because the worker is the
concurrency unit. Idempotency, retries, DLQ and outbox mechanics: `/alaa-async-messaging`
(`$alaa-async-messaging`), and `/alaa-laravel-job-rabbitmq` (`$alaa-laravel-job-rabbitmq`) for
RabbitMQ consumers. Octane-specific rule: a job serialized from inside a request must not carry a
request-scoped object — pass scalar identifiers and re-resolve in `handle()`, for the same reason
`concurrently()` closures must.

## Operations documentation requirement

A change to the driver, worker or task-worker count, `max_requests`, the `flush` list, a reset
listener, or connection lifecycle updates the repository's existing operations document — whichever
of `docs/` or the repo-local `AGENTS.md` the repository already uses; do not create a second. The
entry records: driver and version and which code paths are driver-guarded; worker and task-worker
counts and the CPU quota they were derived from; `max_requests` and the RSS measurement that
selected it (`references/worker-observability.md`); the deploy and reload sequence actually used
(`references/worker-lifecycle-and-failure.md`); what a worker crash and a memory eviction look like
in logs and which signal fires; and the behaviour a caller sees while Redis is unreachable. A
changelog entry that says what changed but not how the service is operated and how it fails does not
satisfy this.

## Output contract

Plan files and phasing: `/alaa-workflow` (`$alaa-workflow`). Proof strength for risky operations:
`/alaa-controlled-ops` (`$alaa-controlled-ops`). This skill adds three required statements to any
report: which of the three reset mechanisms each new or changed binding uses, the observable that
selected any tuning value, and the exact commands run in the target environment. Never claim a suite
green without having executed it there. Never auto-commit.
