# Production-Ready Go Package Catalog for This Stack

## High-level overview of your environment

This catalog is tuned for a specific style of Go system:

- high-concurrency backend services
- security-sensitive and observability-sensitive production workloads
- SLA-minded delivery, with graceful shutdown and explicit failure handling
- HTTP APIs behind a trusted gateway
- Redis cache and coordination, PostgreSQL OLTP, ClickHouse analytics
- deployment on Kubernetes or OpenShift, with local Docker and sometimes Docker Swarm

This is not a generic “cool Go packages” list. It is a production-first shortlist for your stack.

## How this catalog was prepared

This catalog was prepared with these rules:

- standard library first
- official Go, package, and framework docs before blog-post opinions
- current Go release state and current package major versions taken into account
- `awesome-go` used only as a discovery surface, not as the final authority
- strong bias toward libraries that fit trusted-gateway, observability-heavy, and platform-driven services
- strong bias against dependencies that add abstraction without reducing real complexity

## How to use this file

- treat **default** as the first package to reach for
- treat **conditional** as a good choice under clear conditions
- treat **avoid by default** as a package family to resist unless the repo already standardized on it or the use case is unusually strong

## HTTP API and edge-facing services

### `github.com/go-chi/chi/v5` - default

Use when you are building a new HTTP API in this pack.

Why:

- stays inside `net/http`
- easy to test with `httptest`
- easy to instrument with `otelhttp` and Prometheus
- fits trusted gateway and reverse-proxy environments well

### `github.com/gofiber/fiber/v3` - conditional

Use when the repo already uses Fiber or when you have a measured reason to accept its `fasthttp`-oriented model.

Do not use it just because it feels more like Express.

### `github.com/go-chi/cors` - conditional

Use when a `chi` service needs explicit CORS middleware.

Important: mount it as top-level middleware, not deep inside a route group.

### `github.com/go-chi/httprate` - conditional

Use when you want simple HTTP-level rate limiting inside a `chi` service.

Use it for service-local concerns. For shared or global limits across many services, the gateway or a Redis-backed limit strategy is often the right place.

### `golang.org/x/time/rate` - default for in-process limiting

Use when you need token-bucket rate limiting inside handlers, client code, or worker flows without HTTP-specific middleware.

## Config, logging, and service foundation

### `github.com/caarlos0/env/v11` - default for env-first services

Use when config should come mainly from environment variables and map cleanly into structs.

Good fit for containerized services.

### `github.com/knadh/koanf/v2` - conditional

Use when configuration must come from multiple sources such as env, files, flags, Vault, or remote providers.

Prefer it over Viper when you need a richer config story but still want a relatively clean dependency surface.

### `log/slog` - default

Use as the logging baseline.

Do not add a third-party logger by default in new services.

### `github.com/samber/slog-*` - conditional bridge packages

Use only during migration when a repo still depends on Zap, Logrus, or Zerolog and you need a temporary bridge.

## Validation and request contracts

### `github.com/go-playground/validator/v10` - default for HTTP DTO validation

Use when request structs need field and cross-field validation at the transport edge.

It is a strong default for JSON request validation in HTTP APIs.

### `buf.build/go/protovalidate` - default for protobuf-first contracts

Use when request validation belongs in `.proto` schemas and the service is already protobuf-driven.

Prefer it over duplicating protobuf validation logic in hand-written Go.

## HTTP clients and outbound calls

### `net/http` plus a tuned `http.Client` - default

Use by default.

Most production services do not need a third-party HTTP client. They need explicit timeouts, a reusable transport, retries only where safe, and clear observability.

### `resty.dev/v3` - conditional

Use when the service makes many structured HTTP API calls and you want ergonomic request building, retries, and hooks.

Do not adopt it for one or two simple outbound calls.

### `github.com/sony/gobreaker/v2` - conditional

Use when a downstream dependency needs a real circuit breaker and retries plus timeouts are no longer enough.

Keep the policy explicit. Do not hide breaker semantics inside random helpers.

## PostgreSQL

### `github.com/jackc/pgx/v5` - default

Use as the default PostgreSQL driver and toolkit.

Why:

- high-performance driver
- PostgreSQL-specific features
- clean pool support with `pgxpool`
- can still adapt to `database/sql` if needed

### `github.com/sqlc-dev/sqlc` - default when the service owns SQL

Use when you want type-safe generated query code from hand-written SQL.

This is the best default for PostgreSQL services in this stack when you do not want a heavyweight ORM.

### `github.com/pressly/goose/v3` - default for simple migration flows

Use when you want straightforward incremental SQL migrations with low ceremony.

Good fit for service-local migrations that do not need advanced schema planning.

### `atlas` - conditional for governed schema workflows

Use when you need schema planning, migration review, drift detection, or stronger CI controls around database changes.

This is the better choice when database change management is part of platform governance, not just app startup.

### ORM note

Avoid ORM-first design by default in this stack. Prefer `pgx` plus `sqlc`, or `pgx` plus explicit repository code.

## Redis

### `github.com/redis/go-redis/v9` - default

Use as the default Redis client.

Use it for:

- cache lookups
- short-lived coordination
- rate-limit state when the service owns that concern
- distributed locks only when you have explicit correctness rules

After dependency updates, run `govulncheck` because Redis client vulnerabilities do happen.

## ClickHouse

### `github.com/ClickHouse/clickhouse-go/v2` - default

Use first for ClickHouse access.

Why:

- official high-level client
- supports native interface and `database/sql`
- easier operational fit for most services

### `github.com/ClickHouse/ch-go` - conditional for hot ingest paths

Use when you have a specialized high-throughput path and have already proven that the higher-level client is the bottleneck.

Do not make `ch-go` the default just because it is lower level.

## Messaging and async delivery

### `github.com/rabbitmq/amqp091-go` - default for RabbitMQ

Use as the default RabbitMQ client. It is maintained by the RabbitMQ core team.

Keep retries, backoff, confirms, idempotency, and dead-letter strategy in your design instead of assuming the client solves them for you.

### `github.com/twmb/franz-go` - default for Kafka

Use as the default Kafka client when Kafka is truly needed.

It is a strong fit for performance-sensitive and feature-complete Kafka work.

### `github.com/ThreeDotsLabs/watermill` - conditional

Use only when the team intentionally wants a higher-level eventing abstraction and has accepted its architectural style.

Avoid it for simple queue consumers where plain broker clients are easier to reason about.

## gRPC, protobuf, and multi-protocol APIs

### `google.golang.org/grpc` - default for pure gRPC

Use when the service is a normal gRPC service and you want the standard transport.

### `connectrpc.com/connect` - conditional but recommended for mixed clients

Use when one schema should serve Go backends, browsers, and gRPC-Web clients cleanly.

This is a very strong choice when you want one contract with fewer edge adapters.

### `buf` - default for protobuf hygiene

Use when raw `protoc` command lines are becoming brittle.

Use it for:

- linting
- breaking-change checks
- consistent code generation

### `github.com/grpc-ecosystem/go-grpc-middleware/v2` - conditional

Use when gRPC interceptors for logging, retries, recovery, selection, or validation are becoming non-trivial.

### `go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc` - default for gRPC observability

Use when tracing and metrics are required for gRPC servers or clients.

## GraphQL

### `github.com/99designs/gqlgen` - default for schema-first GraphQL

Use when GraphQL is truly needed and you want generated typed resolver contracts from a schema.

Pair it with `golang-graphql` ( `$golang-graphql` ) and `50-gap-coverage.md` because production GraphQL still needs
explicit auth, pagination, depth or complexity limits, batching, and error-shaping rules.

### `github.com/graph-gophers/graphql-go` - conditional

Use when the repo already standardizes on it or when its reflection-based model fits an existing codebase better than
schema-first generated resolver contracts.

Do not choose it just to avoid code generation if the service needs a durable public contract.

## Observability

### `go.opentelemetry.io/otel` and the Go OTel SDK - default

Use as the observability baseline for traces and cross-service context propagation.

### `go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp` - default for HTTP services

Use when a `net/http` or `chi` service needs tracing and standard instrumentation hooks.

### `github.com/prometheus/client_golang/prometheus` - default

Use for metrics collection.

### `github.com/prometheus/client_golang/prometheus/promhttp` - default

Use to expose Prometheus metrics endpoints.

## Identity and security

### `github.com/coreos/go-oidc/v3/oidc` - default for OIDC verification

Use when the service itself must verify OIDC ID tokens or work directly with an OIDC provider.

### `github.com/golang-jwt/jwt/v5` - conditional

Use when the service really owns JWT parsing or signing.

Do not make every service depend on it in a trusted-gateway architecture.

Run `govulncheck` after upgrades because JWT libraries do receive security advisories.

### `github.com/MicahParks/keyfunc/v3` - conditional

Use when direct JWT verification must pull keys from a JWKS endpoint and you need a `jwt.Keyfunc` helper for `github.com/golang-jwt/jwt/v5`.

## Testing

### standard `testing` package and `net/http/httptest` - default

Use first.

### `github.com/stretchr/testify` - conditional default

Use selectively for clearer assertions and targeted mocks.

Do not let it replace good test design.

### `github.com/testcontainers/testcontainers-go` - default for integration tests with real dependencies

Use when the test should run against a real Postgres, Redis, ClickHouse, Kafka, or RabbitMQ dependency in Docker.

### `github.com/DATA-DOG/go-sqlmock` - conditional

Use when you need narrow tests for query behavior without a real database.

Prefer real integration tests when behavior depends on actual PostgreSQL semantics.

## Core repo tools

### `gopls` - default

Use as the language server and analyzer surface for Go repos.

It is the default source for editor intelligence, refactors, and many modernizing analyzers.

### `golangci-lint` - default

Use as the main lint runner in CI and local checks.

Pin the version in CI. Do not let the tool drift implicitly.

### `govulncheck` - default

Use after dependency changes and before releases.

### `buf` - default for protobuf repos

Use for protobuf lint, breaking-change checks, and code generation orchestration.

## CLI and background execution

### `github.com/spf13/cobra` - conditional

Use for large or multi-command CLI tools.

Do not add it to every service just because it is popular.

### `github.com/robfig/cron/v3` - conditional

Use for in-process cron only when an external scheduler or queue is not the better fit.

Make ownership, overlap policy, and shutdown behavior explicit.

## Dependency injection

### manual DI - default

Use explicit constructors and wiring first.

### `github.com/samber/do/v2` - conditional

Use when the repo already uses it or when a real DI container helps enough to justify another abstraction layer.

If you adopt it, also route to `golang-samber-do` ( `$golang-samber-do` ).

### `google/wire` - avoid by default for new work

Do not start a new service on Wire. The repository was archived in 2025.

## Small utility packages

### `github.com/google/uuid` - default

Use when you need UUID generation and parsing with a small, familiar package.

## Packages to avoid by default in this stack

- ORM-heavy stacks for normal PostgreSQL services
- custom HTTP frameworks when `chi` already fits
- framework swaps without a measured reason
- runtime DI containers when constructors are still manageable
- low-level data clients before the higher-level official client is proven too slow
- broad helper libraries that hide context, timeouts, or error behavior

## Practical selection rules

1. Prefer the standard library first.
2. Prefer `chi` for new HTTP APIs in this pack.
3. Prefer `pgx` plus `sqlc` for PostgreSQL.
4. Prefer official or primary package docs over opinionated blog lists.
5. Ask whether the dependency removes real complexity or only moves it.
6. Run `govulncheck` after adding or upgrading important dependencies.
