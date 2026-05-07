# Fiber v3 Core

Use this file for app construction, context safety, config, listen behavior, and lifecycle.

## Version and import

- Fiber v3 import path: `github.com/gofiber/fiber/v3`.
- Fiber v3 requires Go 1.25 or newer.
- Fiber is built on `fasthttp`; do not assume full `net/http` semantics.

## Context safety

Values returned from `fiber.Ctx` are handler-lifetime values unless detached.

Rules:

- Use request values inside the handler.
- Copy strings, byte slices, params, headers, and body data before storing or passing to goroutines.
- Use app helpers such as `GetString` or `GetBytes` where they fit the current Fiber behavior.
- Enable `Immutable` only when the safety tradeoff is worth the performance cost.
- Do not pass `fiber.Ctx` into repositories, use cases, workers, or background jobs.

## App construction

Build the app after config and dependencies are ready:

```go
app := fiber.New(fiber.Config{
    ErrorHandler:     httpErrorHandler,
    StructValidator: validator,
    BodyLimit:       cfg.HTTP.BodyLimit,
})
```

Keep construction order explicit:

1. parse and validate config
2. create logger, metrics, and tracer
3. create DB, Redis, and external clients
4. create repositories
5. create use cases or services
6. create Fiber app
7. register middleware
8. register routes
9. start app and wait for shutdown

## Config rules

- Configure `ErrorHandler` for stable JSON errors.
- Configure `StructValidator` if handlers use Fiber binding validation.
- Set body limits intentionally.
- Use custom JSON encoders only after measurement or a strong compatibility reason.
- Configure trusted proxy settings only with known proxy IPs or ranges.
- Fail fast on invalid config.

## DB and Redis construction

For new services, prefer `pgx/v5` for PostgreSQL and `github.com/redis/go-redis/v9` for Redis. Keep both clients in infrastructure or platform packages, then expose only repository/cache interfaces to use cases.

Construction rules:

- create DB and Redis clients before repositories
- validate required DSNs, pool sizes, and timeouts during startup
- pass `context.Context` to every DB and Redis operation
- keep SQL and Redis commands out of Fiber handlers
- close clients during graceful shutdown

## Listen and shutdown

Use `ListenConfig` for listener options such as TLS or listener network. Register lifecycle hooks before shutdown.

For long-running services:

- run the listener in a supervised goroutine or lifecycle manager
- listen for `SIGINT` and `SIGTERM`
- call shutdown with a timeout
- close DB pools, Redis clients, queues, and telemetry exporters
- make readiness fail before shutdown drains traffic

## Hooks

Use startup and shutdown hooks for lifecycle events, not business logic.

- startup hooks: startup message, diagnostics, metadata
- pre-shutdown hooks: mark service not ready, stop accepting work
- post-shutdown hooks: log shutdown result and close remaining exporters

## Custom context

Use custom Fiber context only when it removes real duplication at the transport edge. Do not use it to smuggle business dependencies into handlers. Constructor injection is still the default for dependencies.
