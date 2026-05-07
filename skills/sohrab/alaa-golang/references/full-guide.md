# Alaa Golang Full Guide

## Table of contents

- Service profile
- Framework stance
- Architecture stance
- Data and cache stance
- Testing stance
- Observability and security stance
- Validation baseline
- Routing heuristics

## Service profile

This skill is optimized for Go services that are:

- high-concurrency and latency-sensitive
- security-sensitive and correctness-sensitive
- built behind a trusted gateway or reverse proxy
- expected to meet strict SLA targets, including `99.99%+` services
- deployed to Kubernetes, OpenShift, Docker, or Swarm
- backed by PostgreSQL, Redis, ClickHouse, queues, or service-to-service APIs

## Framework stance

Framework choice follows evidence:

- explicit user choice wins
- existing repo framework wins
- raw small/simple HTTP services should use chi
- raw large/high-concurrency/SLA-heavy HTTP services should use Fiber and `$alaa-golang-fiber`

Use `30-http-api-framework-choice.md` before choosing a framework.

## Architecture stance

For DB-backed services, repository pattern is mandatory.

Keep boundaries clear:

- transport packages own chi or Fiber details
- use cases own business flow
- domain packages own domain rules
- repositories own persistence
- platform packages own clients, logging, metrics, tracing, and infrastructure adapters

Do not pass framework types into domain, use case, repository, worker, or cache packages.

Read `60-service-architecture-patterns.md` for the default service shape.

## Data and cache stance

- Prefer `pgx` plus `sqlc` for PostgreSQL services that own SQL directly.
- Keep transactions explicit at use case boundaries.
- Treat Redis as a cache layer unless the repo explicitly defines another role.
- Use cache-aside Redis by default.
- Make TTL, key design, invalidation, stampede protection, and cache error behavior explicit.
- Do not use cache values to bypass authorization or revocation rules.

Read `61-redis-cache-layer.md` before changing cache behavior.

## Testing stance

Behavior-changing work must be test-driven:

1. write or update a failing test
2. implement the smallest passing change
3. refactor after tests pass

Use table-driven tests with `t.Run` for behavior matrices. Add `go test -race ./...` for shared state, caches, goroutines, and workers. Add fuzz tests for parsers, codecs, validators, and untrusted input.

Read `63-tdd-and-testing-discipline.md` before implementation.

## Observability and security stance

- Use `log/slog` as the default logging baseline.
- Use OpenTelemetry for traces where the platform supports it.
- Use Prometheus metrics for service signals.
- Keep health, readiness, startup, and shutdown explicit.
- Do not trust client-supplied identity, tenant, profile, or authorization headers.
- Consume trusted gateway headers only where the platform contract says they are trusted.
- Do not add local JWT verification to every service unless that service owns an auth boundary.
- Never log secrets, tokens, passwords, credentials, or sensitive trusted headers.

## Validation baseline

Use the narrowest checks that match the task:

- `go test ./...` for basic behavioral confidence
- `go test -race ./...` for shared state, cache, goroutines, or workers
- `go vet ./...` for built-in static checks
- `golangci-lint run` when lint ownership matters
- `govulncheck ./...` after dependency changes and before release-sensitive work
- benchmarks and profiles only when performance is the real decision surface

For HTTP services, also validate:

- framework-specific handler tests
- middleware order
- request IDs and trace propagation
- health/readiness behavior
- graceful shutdown
- error contracts and status mapping

## Routing heuristics

- Modernize Go code: use `golang-modernize` ( `$golang-modernize` ) and often `golang-lint` ( `$golang-lint` ).
- Design or review a service: use `golang-project-layout` ( `$golang-project-layout` ), `golang-design-patterns` ( `$golang-design-patterns` ), `golang-error-handling` ( `$golang-error-handling` ), `golang-observability` ( `$golang-observability` ), and local architecture references.
- Build or review Fiber: load `alaa-golang-fiber` ( `$alaa-golang-fiber` ).
- Build or review chi: read `31-chi-api-guide.md`.
- Debug concurrency or leaks: use `golang-concurrency` ( `$golang-concurrency` ), `golang-context` ( `$golang-context` ), `golang-safety` ( `$golang-safety` ), and `golang-troubleshooting` ( `$golang-troubleshooting` ).
- Build or audit GraphQL: use `golang-graphql` ( `$golang-graphql` ).
- Choose packages: read `40-production-ready-package-catalog.md`, then route to the narrow vendor skill if one exists.
- Change platform behavior, CI, contracts, trust boundaries, or deployment: add the relevant companion skill from `20-sohrab-companions.md`.
