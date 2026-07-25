# Failure, Load, And Deprecation Contract

Use this file whenever a task adds or changes an outbound call between Ala services, a retry, a
timeout, a connection pool, an ingress admission decision, or the lifecycle of any contract surface
this skill defines.

This file owns the **Ala numbers and the wire behaviour**. It does not own the doctrine: why a timeout
exists, how to shape a backoff curve, what a circuit breaker is for, or how to run an error budget all
belong to `/alaa-reliability-sla` (`$alaa-reliability-sla` in Codex). Read that skill for the reasoning
and this file for the values a service must actually ship. Load `$alaa-data-layer` for pool mechanics
inside a driver, and `$alaa-async-messaging` for broker prefetch, acknowledgement, and DLQ mechanics.

The event and code names used below are owned by `20-operational-and-observability-contract.md`. The
metric families are owned by `21-alaa-platform-observability-directive.md`. Do not restate either here.

## Request deadline

Every Ala service computes one request-scoped deadline at ingress and honours it for the whole request.

- The deadline is `now + route_budget_ms`, computed inside `RequestObservabilityMiddleware` (Laravel) or
  the equivalent top-level middleware, and stored in the same request-scoped context that already
  carries `request_id` and `trace_id`.
- The default `route_budget_ms` is `5000` for a public product route, `2000` for a trusted internal
  route, and `5000` for `/api/ready`. A route that needs a different budget declares it in the route
  definition; a service must not raise a budget by editing a global default.
- `remaining_ms` is the deadline minus now. Every outbound call passes a per-attempt timeout that is the
  smaller of its own default below and `remaining_ms`.
- When `remaining_ms` is smaller than the next attempt's timeout, the caller stops, does not attempt the
  call, and returns `503` with code `DEPENDENCY_UNAVAILABLE` and event `dependency.unavailable`.
- An unbounded outbound call is a contract violation even when the dependency is healthy. Every HTTP
  client, database driver, cache client, and broker client is constructed with an explicit timeout.

## Outbound timeout defaults

These are the Ala defaults for an internal service-to-service hop. They are configurable per service
through env with the same key names, validated at startup, and a service that raises one records the
reason in its own repository docs.

| Hop | Connect | Per-attempt total | Retries |
|---|---|---|---|
| Backend -> backend internal HTTP | `1000 ms` | `3000 ms` | per the retry budget below |
| Backend -> `auth` trusted identity API | `1000 ms` | `2000 ms` | per the retry budget below |
| Gateway -> `authz-sidecar` / `entitlement-spoa` `HEAD /internal/authz/check` | `200 ms` | `200 ms` | none |
| `authz-sidecar` -> OpenFGA `check` | `200 ms` | `500 ms` | none |
| Service -> RabbitMQ publish, waiting for the broker acknowledgement | `1000 ms` | `5000 ms` | per the retry budget below |
| Service -> one `/api/ready` dependency probe | `500 ms` | `2000 ms` | none |
| Service -> Redis, single command | `500 ms` | `1000 ms` | none |

Two hops carry no retry deliberately. The gateway authorization hop is on the critical path of every
protected request and already fails closed with `503 AUTHZ_SERVICE_UNAVAILABLE`, so a retry there
multiplies latency during exactly the incident it would be trying to survive. A readiness probe that
retries reports a dependency as up when it is flapping, which defeats the purpose of the probe.

## Retry budget

- Attempt at most `3` times in total: the first attempt plus at most `2` retries.
- Back off exponentially with full jitter: attempt `n` waits a uniformly random duration between `0` and
  `min(100 ms * 2^(n-1), 2000 ms)`. Never retry with a fixed delay, and never retry with no delay.
- Retry only these outcomes: TCP connect failure, per-attempt timeout, `502`, `503`, `504`, and a
  RabbitMQ publish nack or a closed channel.
- Retry `429` only when the response carries `Retry-After`, and wait exactly that long. Never retry any
  other `4xx`.
- Stop retrying when `remaining_ms` no longer covers another attempt, even if attempts remain in the
  budget. The deadline outranks the attempt count.
- Emit `dependency.call.failed` with code `DEPENDENCY_CALL_FAILED` for each failed attempt, and
  `dependency.unavailable` with code `DEPENDENCY_UNAVAILABLE` once when the budget is exhausted.
- A retry loop nested inside another retry loop for the same logical call is forbidden: when a client
  library already retries, set the library's retry count to `0` or set this budget to `0`, and record
  which one owns the retry in the calling code.

## Idempotency of a retried call

A call is retried only when repeating it cannot produce a second effect. There is no third option.

- `GET`, `HEAD`, `PUT`, and `DELETE` on an internal route are idempotent by contract and may be retried
  within the budget above.
- An internal `POST` may be retried only when the request carries `Idempotency-Key`: a lowercase UUIDv7
  that is generated once per logical operation and reused byte-for-byte on every retry of it. A new key
  per attempt is a defect, not a retry.
- A receiver of `Idempotency-Key` stores the key with the operation result for at least `24 hours` and
  returns the stored result for a repeat key instead of performing the work again. A receiver that does
  not store keys must reject `Idempotency-Key` with `400`, event `input.validation.failed`, and a code from
  its stable validation code family, rather than accept the header and ignore it.
- A route that cannot be made idempotent records `idempotent: false` in its OpenAPI or route
  documentation, and every caller of it sets its retry budget to `0`. An undocumented route is treated
  as non-idempotent, so it is not retried.
- Notification commands already carry `idempotency_key` inside the canonical envelope; see
  `27-notification-service-contract.md`. Do not add a second idempotency mechanism beside it.

## When a dependency is unreachable

### `auth` unreachable

- A request that only needs the gateway-injected trusted headers continues normally. The backend does
  not call `auth` for identity it already received.
- A request that needs a live `auth` call fails with `503`, code `DEPENDENCY_UNAVAILABLE`, and event
  `dependency.unavailable`. It must not fall back to a local user projection for the answer.
- A local user projection or an immutable request snapshot serves display data only. Using either as an
  authorization or entitlement input while `auth` is unreachable is forbidden, because a stale snapshot
  cannot represent a revocation.
- `/api/ready` reports `auth` as a dependency check only when the service cannot serve any product route
  without it. A service that serves most traffic from trusted headers keeps `auth` out of readiness so a
  transient `auth` failure does not remove the service from rotation.

### `authz-sidecar`, `entitlement-spoa`, or OpenFGA unreachable

- The gateway fails closed with `503` and the `AUTHZ_SERVICE_*` codes in
  `26-request-time-authorization-openfga.md`. The backend is not called.
- A backend must not compensate. It must not call OpenFGA directly, must not allow the request because
  the check could not be reached, and must not cache a previous allow decision to serve a later request.
- The only service permitted to cache an authorization decision is `authz-sidecar`, through its own
  short-TTL decision cache. That cache is not extended to survive an OpenFGA outage.

### The notification broker unreachable

- A producer must not drop the command, must not call `notification` over business HTTP, and must not
  block the user-facing response on broker recovery.
- The producer writes the fully-built canonical envelope to its own durable outbox row in the same
  database transaction as the business change, and a retrying worker publishes from that outbox. This is
  the only approved store-and-forward path.
- Publishing from the outbox uses the retry budget above and then leaves the row for the next worker
  pass. An outbox row is never deleted before the broker acknowledges the publish.
- When the outbox write itself fails, the outcome depends on how the route classifies the notification,
  and the route must classify it: a route documented as `notification: required` fails with `503` and
  code `DEPENDENCY_UNAVAILABLE`; a route documented as `notification: deferred`, which is the default
  when the route says nothing, returns its normal success response and emits `queue.publish.failed` with
  code `QUEUE_PUBLISH_FAILED`.

### Redis, ClickHouse, or another optional dependency unreachable

- A dependency marked `required: false` in the `/api/ready` envelope must not fail a product request when
  it is unreachable. The service serves the request without it and emits `dependency.call.failed`.
- A cache miss caused by an unreachable cache is served from the origin, bounded by the same request
  deadline. A cache outage must not turn into an unbounded origin stampede: at most one origin
  computation per cache key is in flight per instance, and later callers for the same key wait for it
  until the deadline rather than starting their own.

## Concurrency and load

### Bounded connection pool

Every service bounds its database pool explicitly. An unbounded or default-unbounded pool is a contract
violation, because the shared Ala Postgres in `15-deployment-and-runtime-contract.md` is a shared
resource and one service's burst becomes every service's outage.

- Ala defaults per application container: `10` maximum connections for a Laravel or PHP-FPM/Octane app
  container, and `25` maximum open plus `25` maximum idle for a Go service.
- Go services also set `ConnMaxLifetime` to `30m` and `ConnMaxIdleTime` to `5m` so a rolling infra change
  drains old connections instead of holding them.
- Across a whole service, `replicas * max_connections_per_container` must stay at or below `60%` of the
  target Postgres `max_connections`. When a scale-up would breach that ceiling, lower the per-container
  maximum in the same change instead of raising replicas alone.
- A request waits at most `1000 ms` to acquire a pooled connection, then fails with `503`, code
  `DEPENDENCY_UNAVAILABLE`, and event `dependency.unavailable`. An unbounded acquire wait converts a slow
  database into an exhausted worker pool.
- Worker and queue-consumer containers count against the same ceiling and get their own explicit pool
  maximum. A consumer that inherits the HTTP default silently doubles the fleet's connection footprint.
- `alaa_db_pool_in_use` and `alaa_db_pool_idle` are already mandatory in
  `21-alaa-platform-observability-directive.md`. A service that bounds its pool without exporting them
  has no way to prove the bound is right.

### Shed versus queue at ingress

One rule decides: **synchronous ingress sheds, asynchronous work queues.** A service never holds a
user-facing request waiting for capacity, and never discards work that has to survive.

- Each service sets a maximum number of in-flight product requests per container. The Ala default is the
  container's worker count, which means no application-level queue beyond the runtime's own accept
  backlog.
- When in-flight requests are at the maximum, a further product request is shed immediately with `503`,
  header `Retry-After: 1`, and event `request.shed` with code `REQUEST_SHED`. It is not queued, and it
  does not wait.
- `/api/health` and `/api/ready` are never shed. Shedding readiness makes an overloaded service look
  dead to the orchestrator and turns load into a restart loop.
- Work that must not be lost under load is converted to a queued job and acknowledged before the
  response returns, so the response reports acceptance rather than completion. Never make a product
  request wait on a queue in order to avoid shedding it.
- `alaa_http_requests_in_flight` is the observable that proves the limit is set correctly, and
  `alaa_queue_backlog` is the observable for the queued path. Both are already mandatory.
- Consumer-side prefetch, concurrency, and DLQ behaviour belong to `$alaa-async-messaging`. Set them
  there; do not restate them in a service repository.

## Deprecating a contract surface

A contract surface is a route, a header name, an event name, a machine-readable code, a response or
envelope field, a metric name, a permission name, a queue name, or a routing key that this skill
defines. Removing or renaming one follows this procedure. There is no informal path.

1. **Announce and date it in one change.** In the reference file of this skill that owns the surface, add
   `Deprecated <YYYY-MM-DD>, removed after <YYYY-MM-DD>` beside the surface, and add the replacement
   surface next to it. A deprecation with no recorded removal date is not a deprecation.
2. **Keep the old surface working for the whole window.** Both surfaces are served, and every first-party
   producer switches to the replacement inside the window.
3. **Window minimums, measured from the announcement date.** `90 days` for a surface a public client can
   observe: a public route, a public response field, a public header, or a public error code. `30 days`
   for a surface only first-party services observe: a trusted header, an event or code name, a metric
   name, a queue name, a routing key, or an envelope field alias. `0 days` for a surface this skill marks
   `reserved`, because no production consumer is wired to it yet.
4. **Notify these three, in the same change as step 1.** The owning reference file in this skill; the
   owning repository's release notes through the `service-ci-kit` semantic-release path, marked as a
   deprecation; and an issue in every consuming repository named for that surface in the service map in
   `10-core-service-contract.md` or in the per-service matrix in `27-notification-service-contract.md`.
5. **Remove only when both conditions hold.** The window has ended, and every consumer named in step 4
   emits or consumes the replacement. Removal deletes the old surface together with its compatibility
   code, tests, docs, and API artifacts in one change; leaving compatibility code behind after removal is
   the defect this step exists to prevent.
6. **Extending a window rewrites the recorded date.** Update the removal date in the owning reference
   file and say why. A window that passes silently with the surface still present is contract drift and is
   reported as a blocker.

Emergency removal for a security defect skips the window, and only the window. Steps 1, 4, and 5 still
apply, and the recorded removal date is the date of the change.
