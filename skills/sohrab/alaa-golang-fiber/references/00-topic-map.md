# Alaa Golang Fiber Topic Map

Use this file after `alaa-golang-fiber` triggers. Read only the smallest reference that matches the task.

## Start here

- Read `full-guide.md` for the complete Fiber service baseline.

## If the task is about app setup or Fiber v3 basics

- Read `10-fiber-v3-core.md`.
- Use it for import path, Go version, `fiber.Ctx`, app config, listen config, hooks, and shutdown.

## If the task is about HTTP behavior

- Read `20-routing-middleware-errors.md`.
- Use it for route groups, middleware order, custom errors, recover, request IDs, CORS, limiter, and trusted proxy rules.

## If the task changes request contracts or behavior

- Read `30-validation-testing.md`.
- Use it for binding, validation, handler tests, TDD, race tests, and fuzz tests.

## If the task is production readiness or review

- Read `40-production-readiness.md`.
- Use it for health, readiness, startup probes, observability, high concurrency, security, and SLA checks.

## If a detail may be version-sensitive

- Read `SOURCES.md` and verify against official Fiber or Go docs.

## Reading policy

- Do not load every reference by default.
- Keep domain and use case code free of Fiber types.
- Route architecture, Redis cache, repository pattern, clean code, and broad Go testing guidance back through `$alaa-golang`.
