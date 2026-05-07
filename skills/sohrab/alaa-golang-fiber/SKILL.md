---
name: alaa-golang-fiber
description: "Use this skill for production Go services that use Fiber or should use Fiber: Fiber v3 APIs, gofiber projects, high-concurrency HTTP services, Fiber middleware, routing, validation, testing, error handling, trusted proxy setup, health/readiness, graceful shutdown, observability, security, or Fiber v2-to-v3 migration. Also use when `github.com/gofiber/fiber/v3` or older Fiber imports appear, when the user explicitly chooses Fiber, or when `$alaa-golang` routes a raw large/high-concurrency Go service to Fiber."
---

# Alaa Golang Fiber

## Purpose

Use this skill to build, review, test, and harden Fiber v3 services for Alaa-style production systems.

It assumes high concurrency, strict correctness, security-sensitive request handling, observability, graceful shutdown,
and `99.99%+` SLA expectations.

## When NOT to use

- Do not use for non-Go work.
- Do not use for a chi, `net/http`, gRPC, or CLI task unless the work is a framework comparison or migration review.
- Do not choose Fiber for a small raw service when chi is simpler and no high-concurrency requirement exists.
- Do not use Fiber to avoid clean architecture, tests, repository boundaries, or service contracts.

## Framework routing

Use Fiber when:

- the repository already uses Fiber
- the user explicitly asks for Fiber
- a raw service is expected to be large, high-concurrency, latency-sensitive, or SLA-heavy
- the team accepts Fiber's `fasthttp` model and has a real reason to prefer it

If the repository already uses chi, preserve chi. If a raw service is small or simple, route back to `$alaa-golang` and its chi guide.

## Fast path

1. Read `references/full-guide.md` for the production baseline.
2. Read `references/10-fiber-v3-core.md` for Fiber v3 app, context, config, and lifecycle rules.
3. Read `references/20-routing-middleware-errors.md` for routing, middleware order, errors, CORS, limiter, and proxy rules.
4. Read `references/30-validation-testing.md` before changing request contracts or behavior.
5. Read `references/40-production-readiness.md` before shipping, reviewing, or hardening a service.
6. Read `references/SOURCES.md` when Fiber version, API behavior, or docs freshness matters.

## Mandatory rules

- Keep handlers thin: bind, validate, call a use case, map result or error, and return.
- Do not put SQL, Redis, queue clients, or business rules directly in handlers.
- Do not store values from `fiber.Ctx` beyond the handler lifetime unless you copy them or intentionally enable immutable behavior.
- Keep domain, use case, and repository packages free of Fiber types.
- Use repository pattern for DB-backed services.
- Treat Redis as a cache layer unless the repository explicitly defines another role.
- Write or update a failing test before behavior-changing implementation.
- Run focused tests after the change and `go test ./...` before calling the work done.
- Add `go test -race ./...` for cache, shared state, goroutines, workers, or high-concurrency code.
- Preserve trusted-gateway and service-contract rules. Do not trust client-supplied identity, tenant, or authorization context.

## Production shape

For new Fiber services, prefer this boundary:

- `cmd/<service>/main.go`: config, dependency construction, app start, shutdown
- `internal/transport/http`: Fiber app, routes, middleware, DTOs, error mapping
- `internal/usecase` or `internal/service`: application behavior and transaction/cache decisions
- `internal/domain`: domain rules and value objects
- `internal/repository`: persistence contracts and implementations
- `internal/platform`: logger, metrics, tracing, clients, and infrastructure adapters

## Reference map

- `references/00-topic-map.md` - choose the smallest file to read next
- `references/full-guide.md` - complete Fiber service baseline
- `references/10-fiber-v3-core.md` - Fiber v3 core, context, config, listen, hooks
- `references/20-routing-middleware-errors.md` - routes, middleware, errors, CORS, limiter, proxy
- `references/30-validation-testing.md` - binding, validation, tests, TDD, fuzzing
- `references/40-production-readiness.md` - high concurrency, SLA, security, observability
- `references/SOURCES.md` - official Fiber and Go source map

## Maintenance rules

- Keep this `SKILL.md` compact.
- Put examples and detailed policies in `references/`.
- Keep Fiber v3 claims tied to official docs.
- Keep the skill ASCII-only unless a source path or product name requires otherwise.
