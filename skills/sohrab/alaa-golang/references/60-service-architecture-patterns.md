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

## Completion check

Before finishing architecture work, confirm:

- handlers are thin
- repositories are isolated
- framework types do not cross into domain/use case/repository packages
- behavior has tests
- shutdown and context propagation are explicit
