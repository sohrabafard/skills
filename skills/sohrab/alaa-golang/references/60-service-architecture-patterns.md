# Service Architecture Patterns

Use this file for DB-backed Go services, HTTP APIs, workers, and service refactors.

## Default layout for new services

Use existing repo conventions first. For raw services, prefer:

```text
cmd/<service>/main.go
internal/config
internal/domain
internal/usecase
internal/repository
internal/transport/http
internal/platform
```

## Layer ownership

- `cmd/<service>`: config loading, dependency construction, lifecycle start/stop
- `internal/config`: typed config and validation
- `internal/domain`: domain rules, value objects, domain errors
- `internal/usecase`: application behavior, transaction decisions, cache decisions
- `internal/repository`: persistence interfaces and implementations
- `internal/transport/http`: chi/Fiber app, DTOs, middleware, handlers, error mapping
- `internal/platform`: logger, metrics, tracing, DB, Redis, queues, external clients

## Repository pattern is mandatory

For DB-backed services:

- define small repository interfaces near the use cases that consume them
- put SQL implementation behind those interfaces
- pass `context.Context` to every method
- return domain or persistence errors that use cases can map
- keep SQL out of handlers
- keep framework types out of repository interfaces
- keep cache implementation behind use case or repository decorators

## Handler rule

Handlers may:

- read route params, query params, headers, and body
- bind into DTOs
- validate DTOs
- call one use case method
- map result or error to HTTP

Handlers must not:

- execute SQL
- call Redis directly
- decide business rules
- start unowned goroutines
- contain transaction logic
- leak chi or Fiber types into use cases

## Use case rule

Use cases own:

- business flow
- repository calls
- transaction boundaries
- cache read/write/invalidation decisions
- idempotency decisions
- authorization checks delegated from trusted context

Use cases should be easy to unit-test with fakes.

## Dependency construction

Prefer manual constructor injection:

```go
repo := postgres.NewUserRepository(pool)
cache := rediscache.NewUserCache(redisClient)
svc := usercase.NewService(repo, cache, clock, logger)
handler := httpapi.NewUserHandler(svc)
```

Route to DI skills only when the repo already uses them or graph complexity justifies the tool:

- `golang-google-wire` ( `$golang-google-wire` )
- `golang-uber-dig` ( `$golang-uber-dig` )
- `golang-uber-fx` ( `$golang-uber-fx` )
- `golang-samber-do` ( `$golang-samber-do` )

## Production backend patterns index

A production-grade Alaa Go service composes patterns owned across this pack. Do not re-derive them here — route to the
owner and keep the boundaries above. This index is what makes the service survive real traffic.

| Pattern | Where it is owned |
| --- | --- |
| Transactional outbox; state + outbox + audit in one transaction; facts leave via a relay | `$alaa-golang-clean-code-principles` P6 · `$alaa-async-messaging` |
| Idempotency keys / receipts; run-twice proof | `$alaa-golang-clean-code-principles` P7 · `$alaa-data-layer` |
| Two-lane DB access (pooled runtime DSN + direct migration/admin DSN); pgBouncer transaction pooling | `$alaa-data-layer` · `$alaa-golang-clean-code-principles` P10 |
| UUIDv7 public ids; snake_case JSON wire tags | `$alaa-golang-clean-code-principles` P8 |
| Keyset (cursor) pagination; locking; tenant-scoped access | `$alaa-data-layer` · `$golang-database` |
| `FOR UPDATE SKIP LOCKED` job queues; worker pools; backpressure | `$golang-concurrency` · `$alaa-async-messaging` |
| RabbitMQ consumers: ack-after-commit, publisher confirms, DLQ, reconnect with backoff + jitter | `$alaa-async-messaging` · `$alaa-golang-clean-code-principles` P6/P9 |
| Rate limiters, circuit breakers, retry/timeout wrappers | `$golang-design-patterns` · `$golang-concurrency` |
| Trusted-gateway identity, permission bitmap, TOTP step-up, `X-Access` projection | `$alaa-trust-gateway-auth` · `$alaa-golang-clean-code-principles` P3 |
| Health/readiness with required/degraded checks; response envelopes; error codes | `$alaa-services-contract` · `$alaa-golang-clean-code-principles` P2/P4 |
| OTel traceparent across HTTP + AMQP; Prometheus low-cardinality; slog JSON; SigNoz; Sentry for panics only | `$alaa-observability-soc` · `$golang-observability` · `$alaa-golang-clean-code-principles` P11 |

## Completion check

Before finishing architecture work, confirm:

- handlers are thin
- repositories are isolated
- framework types do not cross into domain/use case/repository packages
- behavior has tests
- shutdown and context propagation are explicit
