# Installed Public Go Skills

Use this file after `full-guide.md` establishes the baseline. Load only the public Go skills that match the real task.

## General rule

When loading a public Go skill, route to it explicitly in this form:

- Use `golang-modernize` ( `$golang-modernize` )

Do not mention vendor paths in normal user-facing answers.

## Structure, architecture, and API shape

### golang-project-layout ( `$golang-project-layout` )

Use it for module shape, folder layout, package boundaries, `cmd/`, `internal/`, config placement, workspaces, and test layout.

### golang-design-patterns ( `$golang-design-patterns` )

Use it for architecture, boundary design, service layering, adapters, ports, constructors, resilience patterns, and graceful shutdown patterns.

### golang-structs-interfaces ( `$golang-structs-interfaces` )

Use it for interface size, receiver choice, type design, method sets, struct tags, embedding, and boundary abstractions.

### golang-dependency-injection ( `$golang-dependency-injection` )

Use it when choosing or refactoring a DI approach. Prefer manual constructor injection unless repo complexity justifies a DI tool.

### golang-google-wire ( `$golang-google-wire` )

Use it when the repo imports `github.com/google/wire`, has `wire.Build`, `wire.NewSet`, `wire_gen.go`, or compile-time DI injector files. Do not choose Wire for fresh services by default.

### golang-uber-dig ( `$golang-uber-dig` )

Use it when the repo imports `go.uber.org/dig` or uses a runtime DI container without Fx lifecycle.

### golang-uber-fx ( `$golang-uber-fx` )

Use it when the repo imports `go.uber.org/fx`, uses Fx modules, lifecycle hooks, or `fx.New` for long-running services.

### golang-code-style ( `$golang-code-style` )

Use it for clarity, local style rules, comment quality, and line-level polish.

### golang-naming ( `$golang-naming` )

Use it for package names, exported identifiers, error names, method names, receiver names, and test names.

## Language, correctness, and debugging

### golang-modernize ( `$golang-modernize` )

Use it for version-aware rewrites, newer standard-library idioms, Go release upgrades, and modernize analyzer output.

### golang-concurrency ( `$golang-concurrency` )

Use it for goroutines, channels, errgroup, worker pools, backpressure, leaks, and shared-state design.

### golang-context ( `$golang-context` )

Use it for cancellation, deadlines, context propagation, tracing context, and request lifetime.

### golang-safety ( `$golang-safety` )

Use it for nil safety, map/slice hazards, aliasing, numeric conversion, resource lifecycle, and race-prone patterns.

### golang-error-handling ( `$golang-error-handling` )

Use it for error creation, wrapping, sentinels, custom error types, logging, propagation, and error-contract design.

### golang-troubleshooting ( `$golang-troubleshooting` )

Use it for production debugging, compiler/test failures, deadlocks, panics, `pprof`, Delve, and systematic diagnosis.

## Data and dependencies

### golang-database ( `$golang-database` )

Use it for query patterns, pools, transactions, scanning, isolation, locking, migrations, and application-side database access.

### golang-data-structures ( `$golang-data-structures` )

Use it when performance or mutation behavior depends on slices, maps, builders, heaps, generic containers, unsafe, or weak pointers.

### golang-dependency-management ( `$golang-dependency-management` )

Use it for adding, auditing, upgrading, pinning, tidying, visualizing, or securing dependencies.

### golang-popular-libraries ( `$golang-popular-libraries` )

Use it for broad library discovery. Pair it with this pack's package catalog for final production choices.

## Transport, protocols, CLIs, and docs

### golang-grpc ( `$golang-grpc` )

Use it for gRPC services, protobuf code generation, interceptors, streaming, TLS/mTLS, bufconn tests, and status errors.

### golang-graphql ( `$golang-graphql` )

Use it for GraphQL servers, schemas, resolvers, subscriptions, `gqlgen`, `graphql-go`, N+1 prevention, and complexity limits.

### golang-cli ( `$golang-cli` )

Use it for CLIs, command lifecycle, flags, config layering, exit codes, I/O, signals, and CLI tests.

### golang-spf13-cobra ( `$golang-spf13-cobra` )

Use it when the repo imports `github.com/spf13/cobra`, defines command trees, flags, completions, docs generation, or Cobra command tests.

### golang-spf13-viper ( `$golang-spf13-viper` )

Use it when the repo imports `github.com/spf13/viper`, uses layered config, env binding, config files, hot reload, or Cobra/Viper integration.

### golang-swagger ( `$golang-swagger` )

Use it for Swagger/OpenAPI docs with `swaggo/swag`, annotations, generated docs, Swagger UI routes, and framework integrations including chi and Fiber.

## Quality, operations, and delivery

### golang-testing ( `$golang-testing` )

Use it for unit, integration, HTTP, fuzz, race, fixture, mock, and coverage patterns.

### golang-stretchr-testify ( `$golang-stretchr-testify` )

Use it when the repo already uses Testify or when assertions, mocks, and suites are appropriate.

### golang-lint ( `$golang-lint` )

Use it for `golangci-lint`, `go vet`, analyzer policy, `nolint` hygiene, staticcheck, revive, and lint configuration.

### golang-benchmark ( `$golang-benchmark` )

Use it for `testing.B`, `benchstat`, profiles, regression detection, and measurement methodology.

### golang-performance ( `$golang-performance` )

Use it for CPU, memory, I/O, GC, pooling, caching, and hot-path optimization after a bottleneck is proven.

### golang-observability ( `$golang-observability` )

Use it for logs, metrics, traces, profiling, dashboards, alerting, and production telemetry.

### golang-security ( `$golang-security` )

Use it for code-level hardening, injection defenses, secrets, crypto, filesystem safety, auth-sensitive code, and threat review.

### golang-documentation ( `$golang-documentation` )

Use it for package docs, exported comments, examples, README, changelog, and developer-facing Go docs.

### golang-continuous-integration ( `$golang-continuous-integration` )

Use it for CI, GitHub Actions, release gates, dependency automation, security scans, coverage, GoReleaser, and AI review workflows.

## Samber-specific skills

Use a Samber skill when the repo imports that package or the user explicitly asks for it.

### golang-samber-do ( `$golang-samber-do` )

Use it for `github.com/samber/do` or `github.com/samber/do/v2` dependency injection and service lifecycle.

### golang-samber-lo ( `$golang-samber-lo` )

Use it for `github.com/samber/lo` functional helpers.

### golang-samber-mo ( `$golang-samber-mo` )

Use it for `github.com/samber/mo` option, result, either, future, and functional composition types.

### golang-samber-ro ( `$golang-samber-ro` )

Use it for `github.com/samber/ro` reactive streams and event-driven pipelines.

### golang-samber-slog ( `$golang-samber-slog` )

Use it for Samber `slog-*` helpers, adapters, routing, sampling, or backend handlers.

### golang-samber-hot ( `$golang-samber-hot` )

Use it for `github.com/samber/hot` in-memory caching.

### golang-samber-oops ( `$golang-samber-oops` )

Use it for `github.com/samber/oops` structured errors.

## Learning-only or ecosystem-radar work

### golang-stay-updated ( `$golang-stay-updated` )

Use it for Go ecosystem awareness, recent changes, learning resources, communities, or discovery-oriented exploration.
