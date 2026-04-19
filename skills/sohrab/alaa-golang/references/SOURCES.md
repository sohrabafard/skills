# Live Sources

Use these sources when a task depends on current package state, current Go releases, official framework behavior, or current OpenAI/Codex guidance.

## Official Go sources

### https://go.dev/doc/devel/release

Use for:

- current stable Go version
- supported major releases
- minor release dates and security fix notes

### https://go.dev/doc/go1.26

Use for:

- Go 1.26 language and toolchain changes
- current release-note wording
- standard library or runtime changes that affect migration work

### https://go.dev/blog/gofix

Use for:

- current `go fix` guidance
- `new(expr)` modernization
- safe upgrade patterns for Go 1.26+

### https://go.dev/doc/modules/layout

Use for:

- official module and package layout guidance

### https://go.dev/gopls/analyzers

Use for:

- current analyzer names
- modernization analyzers such as `errorsastype`
- editor and analysis guidance

## HTTP framework sources

### https://github.com/go-chi/chi

Use for:

- `chi` README
- route and middleware examples
- current feature set and changelog

### https://pkg.go.dev/github.com/go-chi/chi/v5

Use for:

- package API docs
- middleware list
- current major-version details

### https://pkg.go.dev/github.com/go-chi/chi/v5/middleware

Use for:

- request ID, recovery, timeout, throttle, and related middleware behavior

### https://pkg.go.dev/github.com/go-chi/cors

Use for:

- CORS middleware behavior and mounting constraints

### https://docs.gofiber.io/

Use for:

- current Fiber docs and current major version
- confirm Fiber-specific behavior before recommending it

## Package sources for this stack

### https://pkg.go.dev/github.com/jackc/pgx/v5

Use for PostgreSQL driver and toolkit details.

### https://docs.sqlc.dev/

Use for `sqlc` code generation, config, and query annotation behavior.

### https://github.com/pressly/goose

Use for Goose migration behavior and current release state.

### https://atlasgo.io/docs

Use for Atlas migration, schema planning, CI, and drift-control guidance.

### https://pkg.go.dev/github.com/redis/go-redis/v9

Use for Redis client API and version state.

### https://clickhouse.com/docs/integrations/go

Use for official ClickHouse Go client guidance and the split between `clickhouse-go` and `ch-go`.

### https://pkg.go.dev/github.com/ClickHouse/clickhouse-go/v2

Use for high-level ClickHouse client API details.

### https://pkg.go.dev/github.com/ClickHouse/ch-go

Use for low-level ClickHouse client details when you are considering hot-path optimization.

### https://pkg.go.dev/github.com/rabbitmq/amqp091-go

Use for the RabbitMQ-maintained AMQP client.

### https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo

Use for Kafka client capabilities and current package surface.

### https://connectrpc.com/docs/go/getting-started/

Use for Connect basics and generated-code expectations.

### https://connectrpc.com/docs/go/deployment/

Use for h2c, timeouts, CORS, and production deployment behavior for Connect.

### https://buf.build/docs/

Use for Buf config, lint, and code generation guidance.

### https://buf.build/docs/breaking/

Use for breaking-change detection and baseline choices.

### https://pkg.go.dev/github.com/grpc-ecosystem/go-grpc-middleware/v2

Use for current interceptor modules and deprecations.

### https://pkg.go.dev/github.com/coreos/go-oidc/v3/oidc

Use for OIDC verification guidance.

### https://pkg.go.dev/github.com/golang-jwt/jwt/v5

Use for direct JWT parsing or signing when a service really owns that responsibility.

### https://pkg.go.dev/github.com/MicahParks/keyfunc/v3

Use for JWKS-backed `jwt.Keyfunc` helpers that fit `github.com/golang-jwt/jwt/v5`.

### https://pkg.go.dev/github.com/testcontainers/testcontainers-go

Use for integration-test container orchestration.

### https://golang.testcontainers.org/

Use for the full Testcontainers Go documentation site.

### https://pkg.go.dev/resty.dev/v3

Use for current Resty major version and API docs.

## Observability sources

### https://opentelemetry.io/docs/languages/go/

Use for OpenTelemetry Go setup and signal maturity.

### https://opentelemetry.io/docs/languages/go/instrumentation/

Use for manual instrumentation guidance.

### https://pkg.go.dev/go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp

Use for HTTP instrumentation details.

### https://pkg.go.dev/go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc

Use for gRPC instrumentation details.

### https://pkg.go.dev/github.com/prometheus/client_golang/prometheus

Use for Prometheus metrics primitives and concurrency guarantees.

## Discovery source

### https://github.com/avelino/awesome-go

Use only for discovery and breadth.

Do not treat it as the final authority for package choice. Confirm shortlisted packages from official docs or package docs before recommending them.

## Official OpenAI and Codex sources

### https://developers.openai.com/codex/skills

Use for current skills behavior, `openai.yaml`, and implicit invocation rules.

### https://developers.openai.com/codex/subagents

Use for current subagent behavior and configuration.

### https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide

Use for current Codex prompting recommendations.

### https://developers.openai.com/api/docs/guides/latest-model

Use for current GPT-5.4 guidance when model behavior matters.

### https://developers.openai.com/codex/changelog

Use for recent Codex changes that may affect skill-writing assumptions.

## Conflict resolution order

1. official Go docs
2. official package docs or primary project docs
3. official OpenAI and Codex docs
4. installed public Go skills
5. Sohrab companion skills
6. discovery lists such as `awesome-go`
