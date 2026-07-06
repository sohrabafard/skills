# Live Sources

Use these sources when a task depends on current package state, current Go releases, official framework behavior, or current Codex guidance.

## Freshness triggers

Re-check official or primary sources when the user asks for latest/current behavior, a Go release or security fix, a package major version, a framework comparison, a vulnerability, or current Codex/subagent/model guidance.

## Official Go sources

### https://go.dev/doc/devel/release

Use for current stable Go version, supported releases, release dates, and security notes.

### https://tip.golang.org/doc/go1.26

Use for the Go 1.26 release notes: language, toolchain, runtime, compiler, standard-library, and security changes. This
is the canonical source behind `70-go-1.26-and-modern-language.md`; re-read it when a task depends on a specific 1.26
feature or a `1.26.x` patch. The stable mirror is <https://go.dev/doc/go1.26> once the release ships.

### https://go.dev/ref/spec

Use for the current Go language specification when a syntax, generics, or type-system detail must be exact.

### https://go.dev/doc/modules/layout

Use for official module and package layout guidance.

### https://pkg.go.dev/golang.org/x/tools/gopls

Use for `gopls` capabilities, MCP tools, code actions, and settings behind the `golang-gopls` skill. Prefer semantic
navigation over grep for questions about the resolved build.

### https://pkg.go.dev

Use as the package index queried by `godig` (the `golang-pkg-go-dev` skill): versions, symbols, examples, importers,
licenses, and known CVEs for a published import path.

### https://pkg.go.dev/testing

Use for Go tests, benchmarks, examples, fuzz tests, `testing.T`, `testing.F`, helpers, cleanup, and subtests.

### https://go.dev/blog/subtests

Use for table-driven subtests, sub-benchmarks, focused `go test -run`, and parallel subtest behavior.

### https://go.dev/doc/security/fuzz/

Use for fuzzing rules, seed corpus behavior, fast deterministic fuzz targets, and security-sensitive input testing.

## HTTP framework sources

### https://github.com/go-chi/chi

Use for chi README, route examples, middleware examples, and current project guidance.

### https://pkg.go.dev/github.com/go-chi/chi/v5

Use for chi package API docs and current major version details.

### https://pkg.go.dev/github.com/go-chi/chi/v5/middleware

Use for request ID, recovery, timeout, throttle, and related middleware behavior.

### https://pkg.go.dev/github.com/go-chi/cors

Use for CORS middleware behavior and mounting constraints.

### https://docs.gofiber.io/

Use for Fiber v3 behavior. Load `$alaa-golang-fiber` for Fiber tasks.

## Package sources for this stack

### https://pkg.go.dev/github.com/jackc/pgx/v5

Use for PostgreSQL driver and toolkit details.

### https://docs.sqlc.dev/

Use for `sqlc` code generation, config, and query annotations.

### https://github.com/pressly/goose

Use for Goose migration behavior and current release state.

### https://atlasgo.io/docs

Use for Atlas migration, schema planning, CI, and drift-control guidance.

### https://pkg.go.dev/github.com/redis/go-redis/v9

Use for Redis client API and version state.

### https://clickhouse.com/docs/integrations/go

Use for official ClickHouse Go client guidance.

### https://pkg.go.dev/github.com/rabbitmq/amqp091-go

Use for the RabbitMQ-maintained AMQP client.

### https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo

Use for Kafka client capabilities and current package surface.

### https://pkg.go.dev/github.com/testcontainers/testcontainers-go

Use for integration-test container orchestration.

### https://golang.testcontainers.org/

Use for the full Testcontainers Go documentation site.

## Observability and security sources

### https://opentelemetry.io/docs/languages/go/

Use for OpenTelemetry Go setup and signal maturity.

### https://pkg.go.dev/go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp

Use for HTTP instrumentation details.

### https://pkg.go.dev/github.com/prometheus/client_golang/prometheus

Use for Prometheus metrics primitives.

### https://pkg.go.dev/github.com/coreos/go-oidc/v3/oidc

Use for OIDC verification guidance.

### https://pkg.go.dev/github.com/golang-jwt/jwt/v5

Use when a service really owns JWT parsing or signing.

## Official OpenAI and Codex sources

### https://developers.openai.com/codex/skills

Use for current skills behavior, `openai.yaml`, and implicit invocation rules.

### https://developers.openai.com/codex/concepts/subagents

Use for current subagent behavior and configuration.

### https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide

Use for current Codex prompting recommendations.

## Conflict resolution order

1. official Go docs
2. official Fiber or chi docs
3. official package docs or primary project docs
4. official OpenAI and Codex docs
5. installed public Go skills
6. Sohrab companion skills
7. discovery lists and community posts
