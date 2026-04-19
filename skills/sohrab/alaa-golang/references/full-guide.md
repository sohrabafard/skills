# Alaa Golang Full Guide

## Table of contents

- Service profile
- Version policy
- Core engineering stance
- HTTP API stance
- Data and messaging stance
- Observability and security stance
- Validation baseline
- Routing heuristics

## Service profile

This skill is optimized for services that look like this:

- Go services deployed to Kubernetes or OpenShift, with local Docker for development and sometimes Docker Swarm for smaller environments
- high-concurrency traffic with strict latency expectations
- security-sensitive boundaries, especially around identity, trusted gateway headers, and downstream authorization
- observability-sensitive systems where logs, metrics, traces, and health endpoints are part of the feature, not an afterthought
- Redis, PostgreSQL, and ClickHouse in the platform baseline

## Version policy

- Go has no LTS branch. Support follows the latest two major releases.
- Verify the current release state from `https://go.dev/doc/devel/release` before making version-sensitive claims.
- As of `2026-04-19`, `go1.26.2` is the latest stable release and `go1.25.9` is the previous supported line.
- Apply Go 1.26-specific rewrites only when `go.mod`, `go.work`, or file build constraints require Go 1.26 or later.

### Go 1.26 features worth checking

- `errors.AsType[T](err)` instead of the older `errors.As` target-variable pattern
- `new(expr)` instead of one-off pointer helper functions
- `go fix ./...` and targeted fixers such as `go fix -newexpr ./...`
- newer analyzers surfaced by `gopls` and `golangci-lint`

## Core engineering stance

- start stdlib-first
- justify every dependency by fit, maintenance, and operational cost
- keep binaries in `cmd/`, private service code in `internal/`, and exported packages intentionally small
- keep transport thin and business logic outside handlers, CLI callbacks, and queue consumers
- centralize config parsing and validation instead of scattering `os.Getenv` across the codebase
- every goroutine needs an owner, a cancellation story, bounded fan-out, and a deterministic exit path
- prefer manual DI by default; add a DI library only when the graph is large enough to justify it

## HTTP API stance

For this pack, prefer `net/http` plus `chi` for new HTTP APIs.

Why `chi` is the default here:

- it stays inside the standard `net/http` model
- it composes cleanly with `otelhttp`, `promhttp`, standard middleware, and standard testing
- it keeps request context, timeouts, shutdown, and reverse-proxy behavior predictable
- it is easier to reason about in trusted-gateway and observability-heavy systems

Use `fiber` only when the repo already uses Fiber or when a measured requirement justifies its `fasthttp`-oriented model.
Read `30-http-api-framework-choice.md` before making that call.

## Data and messaging stance

- prefer `pgx` for PostgreSQL
- prefer `sqlc` when the service owns SQL directly and wants type-safe generated query code
- choose migrations intentionally: `goose` for simple incremental SQL, `Atlas` when schema planning and drift controls matter
- prefer `go-redis` for Redis
- prefer `clickhouse-go/v2` first for ClickHouse and move to `ch-go` only for specialized hot paths
- for RabbitMQ, use `amqp091-go`
- for Kafka, use `franz-go`
- design retries, backoff, idempotency, and DLQ behavior explicitly; do not hide them behind library defaults

## Observability and security stance

- use `log/slog` as the logging baseline
- use OpenTelemetry for traces and cross-service context propagation
- use Prometheus client packages for service metrics
- make health, readiness, and shutdown behavior explicit and testable
- trust gateway-derived identity only where the system contract says you may trust it
- do not add JWT verification code to every service just because the platform uses JWT somewhere
- when a service must verify OIDC or JWT itself, use dedicated libraries and explicit key-management rules

## Validation baseline

Use the narrowest checks that match the task.

- `go test ./...` for basic behavioral confidence
- `go test -race ./...` when shared state, goroutines, or channels are involved
- `go vet ./...` for native static checks
- `golangci-lint run` when lint ownership matters
- `go fix ./...` or targeted `go fix` passes when modernization is the point
- `govulncheck ./...` before releases and after dependency changes
- profiles and benchmarks only when performance is the real decision surface

For HTTP and gRPC services, also validate:

- timeouts and context cancellation
- middleware or interceptor ordering
- request IDs and trace propagation
- health, readiness, and graceful shutdown behavior
- error contracts and status-code mapping

## Routing heuristics

- If the task is “modernize this Go codebase”, start with `golang-modernize` ( `$golang-modernize` ) and often `golang-linter` ( `$golang-linter` ).
- If the task is “design or review a service”, start with `golang-project-layout` ( `$golang-project-layout` ), `golang-design-patterns` ( `$golang-design-patterns` ), `golang-error-handling` ( `$golang-error-handling` ), `golang-observability` ( `$golang-observability` ), and this local guide.
- If the task is “debug concurrency or leaks”, load `golang-concurrency` ( `$golang-concurrency` ), `golang-context` ( `$golang-context` ), `golang-safety` ( `$golang-safety` ), and `golang-troubleshooting` ( `$golang-troubleshooting` ).
- If the task is “choose packages”, read `40-production-ready-package-catalog.md` and then use the narrow vendor skill if one exists.
- If the task changes platform behavior, CI, cluster objects, contracts, or trust boundaries, add the relevant companion skill from `20-sohrab-companions.md`.
