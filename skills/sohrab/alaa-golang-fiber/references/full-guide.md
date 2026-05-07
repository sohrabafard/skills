# Fiber v3 Production Guide

## Table of contents

- Service stance
- Framework fit
- Service boundaries
- Request lifecycle
- Testing and TDD
- Production readiness
- What to avoid

## Service stance

Fiber is a good fit when a Go HTTP service is large, high-concurrency, latency-sensitive, or already standardized on Fiber.
Use it deliberately. Fiber is built on `fasthttp`, so some `net/http` assumptions do not apply.

For small raw services, chi is usually simpler. Route that case back to `$alaa-golang`.

## Framework fit

Use Fiber when one of these is true:

- the repo already imports Fiber
- the user explicitly chooses Fiber
- the service is expected to handle very high concurrency or strict latency requirements
- the team accepts Fiber's context and middleware model

Do not migrate a chi or `net/http` service to Fiber as routine cleanup. Treat framework migration as architecture work.

## Service boundaries

Keep Fiber at the transport edge:

- handlers bind and validate request DTOs
- handlers call use cases or services
- handlers map domain errors to HTTP responses
- use cases own business flow
- repositories own persistence
- Redis cache access is wrapped behind cache/repository/use case abstractions

Do not pass `fiber.Ctx` into domain, use case, repository, worker, or cache packages.

## Data and cache defaults

For new DB-backed Fiber services, keep the same data rules as `$alaa-golang`:

- PostgreSQL client default: `pgx/v5`.
- SQL ownership default: `sqlc` when query shape benefits from generated typed code.
- Redis client default: `github.com/redis/go-redis/v9`.
- Redis pattern default: cache-aside through a cache abstraction.
- Truth default: PostgreSQL remains the source of truth.

Use `$alaa-golang` with `references/60-service-architecture-patterns.md` and `references/61-redis-cache-layer.md` when the task needs deeper repository, transaction, or cache-invalidation design.

## Request lifecycle

Fiber handler values are optimized for speed and may be reused after the handler returns. Copy request-derived values before storing them in goroutines, caches, logs that outlive the handler, or background jobs.

Every request path must have:

- context or cancellation strategy
- validation
- stable error mapping
- request ID or trace correlation
- metrics for latency and failures
- no leaked internal error detail

Route platform-specific response envelopes, metric names, trace conventions, trusted gateway identity contracts, and service-to-service headers through `$alaa-services-contract`, `$alaa-observability-soc`, and `$alaa-trust-gateway-auth`.

## Testing and TDD

For behavior changes, follow Red, Green, Refactor:

- Red: write or update a failing test first
- Green: implement the smallest passing change
- Refactor: clean the design after tests pass

Unit-test domain and use case code without Fiber. Test Fiber handlers with `app.Test`. Add integration tests only when real DB, Redis, proxy, or middleware behavior matters.

## Production readiness

Before shipping or approving a Fiber service, check:

- liveness, readiness, and startup probes
- graceful shutdown and startup failure behavior
- request and dependency timeouts
- DB and Redis pool sizing
- bounded goroutines and workers
- structured logs, metrics, and traces
- trusted proxy and gateway header policy
- CORS and rate-limit safety
- no secrets or internal errors in responses or logs

For ordinary cache-aside Redis, degraded cache reads should usually fall back to PostgreSQL and emit logs/metrics. If Redis is contract-critical for an endpoint, readiness and error mapping must say so explicitly.

## What to avoid

- SQL in handlers
- Redis calls in handlers
- long-lived references to `fiber.Ctx` values
- business logic in middleware
- global mutable dependencies
- unbounded goroutines
- cache-based authorization shortcuts
- wildcard CORS with credentials
- trusting forwarded headers without trusted proxy config
