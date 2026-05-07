# Production Readiness

Use this file for Fiber services that must be secure, observable, high-concurrency, and SLA-ready.

## Health, readiness, and startup

Expose separate probes:

- liveness: process is alive
- readiness: service can handle useful traffic
- startup: service completed startup initialization

Readiness should fail when critical dependencies such as DB, Redis required for contract-critical paths, required queues, or required config are unavailable.

For ordinary cache-aside Redis, decide readiness by endpoint contract:

- if Redis is only a performance cache, Redis failure should usually degrade to DB reads and emit logs/metrics
- if Redis is required for rate limits, idempotency, sessions, locks, or another correctness path, readiness should fail when it is unavailable
- document the decision so operators know whether Redis is critical or degradable

## Graceful shutdown

Shutdown must:

- mark readiness false before draining
- stop accepting new work
- let in-flight requests finish within a timeout
- cancel background work
- close DB pools, Redis clients, queues, and telemetry exporters
- log the shutdown result once

## Timeouts and cancellation

- Every outbound call needs a timeout.
- Every DB and Redis operation should receive context.
- Avoid unbounded retries.
- Retry only idempotent operations unless the business flow explicitly supports replay.

## High concurrency

For high-concurrency Fiber services:

- size DB and Redis pools deliberately
- bound goroutines and worker pools
- add backpressure for expensive work
- avoid global locks on hot paths
- protect cache misses from stampedes
- measure before optimizing JSON or allocation behavior

## Observability

Add always-on signals:

- structured logs with request ID and trace ID
- request latency, error, and saturation metrics
- DB and Redis latency/error metrics
- cache hit/miss/error metrics
- OpenTelemetry traces where the platform supports them
- profiler endpoints only when protected by platform policy

Use `$alaa-observability-soc` when metric names, trace fields, log schemas, alert rules, or SOC routing must match the wider Alaa platform.

## Security

- Do not trust client-supplied identity, tenant, profile, or authorization headers.
- Consume trusted gateway headers only behind the trusted gateway contract.
- Do not cache authorization decisions unless TTL, invalidation, and revocation behavior are explicitly designed.
- Do not log secrets, tokens, cookies, passwords, connection strings with credentials, or sensitive trusted headers.
- Return stable public errors, not internal failures.

## SLA checklist

Before calling a Fiber service ready for `99.99%+` use:

- config validation fails fast
- readiness covers critical dependencies
- shutdown is tested
- request timeouts exist
- DB and Redis pools are bounded
- cache failure behavior is tested
- race tests pass for shared state
- validation and error contracts are covered
- alerts can detect latency, error rate, saturation, and dependency failures
