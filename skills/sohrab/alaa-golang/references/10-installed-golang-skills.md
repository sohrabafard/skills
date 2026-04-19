# Installed Public Go Skills

Use this file after `full-guide.md` establishes the baseline. Load only the public Go skills that match the real task.

## General rule

When you decide to load a public Go skill, route to it explicitly in this form:

- Use `golang-modernize` ( `$golang-modernize` )

That is enough. Do not mention vendor paths.

## Structure, architecture, and API shape

### golang-project-layout ( `$golang-project-layout` )

Use it when the task is about module shape, folder layout, package boundaries, `cmd/`, `internal/`, config placement, or test layout.

### golang-design-patterns ( `$golang-design-patterns` )

Use it when the task is about architecture, boundary design, service layering, adapters, ports, or application structure.

### golang-structs-interfaces ( `$golang-structs-interfaces` )

Use it when interface size, receiver choice, type design, method sets, or boundary abstractions are the real issue.

### golang-dependency-injection ( `$golang-dependency-injection` )

Use it when you need to choose or refactor a DI approach. Pair it with the local package catalog because `google/wire` is now archived and should not be a fresh default.

### golang-code-style ( `$golang-code-style` )

Use it when clarity, local style rules, comment quality, or line-by-line polish are the main issue.

### golang-naming ( `$golang-naming` )

Use it when package names, exported identifiers, error names, method names, or test naming need cleanup.

## Language, correctness, and debugging

### golang-modernize ( `$golang-modernize` )

Use it for version-aware rewrites, newer standard-library idioms, and Go release upgrades.

### golang-concurrency ( `$golang-concurrency` )

Use it for goroutines, channels, errgroup, worker pools, backpressure, leaks, and shared-state design.

### golang-context ( `$golang-context` )

Use it when cancellation, deadlines, context propagation, tracing context, or request lifetime is the key problem.

### golang-safety ( `$golang-safety` )

Use it for nil-safety, map and slice hazards, race-prone patterns, and correctness guardrails.

### golang-error-handling ( `$golang-error-handling` )

Use it for error creation, wrapping, surfacing, propagation, and error-contract design.

### golang-troubleshooting ( `$golang-troubleshooting` )

Use it for production debugging, runtime investigation, `pprof`, compiler or test failures, and systematic diagnosis.

## Data and dependencies

### golang-database ( `$golang-database` )

Use it for query patterns, pools, transactions, scanning, isolation, and application-side database access.

### golang-data-structures ( `$golang-data-structures` )

Use it when performance or mutation behavior depends on slices, maps, builders, heaps, or generic containers.

### golang-dependency-management ( `$golang-dependency-management` )

Use it when adding, auditing, upgrading, pinning, or visualizing dependencies.

### golang-popular-libraries ( `$golang-popular-libraries` )

Use it for broad library discovery. Pair it with the local package catalog when the recommendation must fit this exact stack.

## Transport, protocols, and CLIs

### golang-grpc ( `$golang-grpc` )

Use it for gRPC services, protobuf code generation, interceptors, streaming, and transport behavior.

### golang-cli ( `$golang-cli` )

Use it for CLIs, Cobra, flags, shell completion, config layering for tools, and command lifecycle.

## Quality, operations, and delivery

### golang-testing ( `$golang-testing` )

Use it for unit, integration, HTTP, and mocking patterns.

### golang-stretchr-testify ( `$golang-stretchr-testify` )

Use it when the repo already uses `testify` or when selective assertions and mocks are appropriate.

### golang-linter ( `$golang-linter` )

Use it for `golangci-lint`, analyzer policy, `nolint` hygiene, and modernization analyzers.

### golang-benchmark ( `$golang-benchmark` )

Use it when you need measurement instead of guesswork: `testing.B`, `benchstat`, profiles, and regressions.

### golang-performance ( `$golang-performance` )

Use it for CPU, memory, I/O, and runtime tuning after a hot path is proven.

### golang-observability ( `$golang-observability` )

Use it for logs, metrics, traces, profiling, dashboards, and alerting inside Go services.

### golang-security ( `$golang-security` )

Use it for code-level hardening, secrets, injection defenses, crypto usage, logging hygiene, and threat-model review.

### golang-documentation ( `$golang-documentation` )

Use it for package docs, code comments, developer docs, and project-facing Go documentation.

### golang-continuous-integration ( `$golang-continuous-integration` )

Use it for CI pipelines, release gates, dependency automation, security scans, coverage, and Go release flows.

## Samber-specific skills

If the repo already uses one of these packages, route to the matching skill instead of treating it as generic Go:

- `golang-samber-do` ( `$golang-samber-do` )
- `golang-samber-lo` ( `$golang-samber-lo` )
- `golang-samber-mo` ( `$golang-samber-mo` )
- `golang-samber-ro` ( `$golang-samber-ro` )
- `golang-samber-slog` ( `$golang-samber-slog` )
- `golang-samber-hot` ( `$golang-samber-hot` )
- `golang-samber-oops` ( `$golang-samber-oops` )

## Learning-only or ecosystem-radar work

### golang-stay-updated ( `$golang-stay-updated` )

Use it when the task is about Go ecosystem awareness, recent changes, or learning-oriented exploration rather than direct implementation.
