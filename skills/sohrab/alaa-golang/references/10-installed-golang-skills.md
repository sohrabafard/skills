# Installed Public Go Skills

Use this file after `full-guide.md` establishes the baseline. Load only the public Go skills that match the real task.

## General rule

When loading a public Go skill, route to it explicitly in this form:

- Use `golang-modernize` ( `$golang-modernize` )

Do not mention vendor paths in normal user-facing answers.

This file should have one `###` heading per `vendor/cc-skills-golang/skills/*/SKILL.md`. Last audited against
vendor subtree `112a945f0d7489b848705ab6f4fbf8c30c4ff053` (upstream `4881c01d`): `vendor=46 routed=46 missing=0 extra=0`.

The three additions since the previous audit are the code-intelligence and refactoring tier: `golang-gopls`,
`golang-refactoring`, and `golang-pkg-go-dev`. They change how a strong Go agent reads and reshapes a codebase, so
route to them deliberately, not only when a user names them.

For broad, ambiguous, or cross-cutting Go work, load `golang-how-to` first and then load the primary plus secondary
skills it selects. Keep Alaa platform, trusted-gateway, repository, cache, and TDD rules from this skill in force.

## Orchestration

### golang-how-to ( `$golang-how-to` )

Use it as the vendor Go skill orchestrator for broad coding, review, debug, setup, and overlapping-domain tasks. It
selects primary plus secondary public Go skills, disambiguates competing clusters, and carries the vendor by-category
catalog.

In Alaa repos, use `golang-how-to` for skill selection only. Do not run its configure mode or edit project
`CLAUDE.md` / `AGENTS.md` files unless the user explicitly asks to force-load Go skills.

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

Use it for adding, auditing, upgrading, pinning, tidying, visualizing, or securing dependencies (editing `go.mod`).

### golang-pkg-go-dev ( `$golang-pkg-go-dev` )

Use it to query pkg.go.dev for a known import path with the `godig` CLI/MCP: available versions, exported symbols and
signatures, runnable examples, `imported-by`, licenses, and known CVEs — including packages not yet in `go.mod`. It is
the read-only ecosystem-lookup layer. It does not edit `go.mod` (use `golang-dependency-management`) and cannot see your
local, resolved build or call sites (use `golang-gopls`).

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

## Code intelligence, navigation, and safe refactoring

Prefer these over grep-and-hand-edit whenever a question is about the *resolved build* (types, call graphs, interface
satisfaction) or when reshaping existing code. `grep` finds text; these find meaning.

### golang-gopls ( `$golang-gopls` )

Use it for semantic code intelligence via `gopls` (the official Go language server): go-to-definition, find references,
call/implementation hierarchy, workspace symbol search, package API discovery, post-edit diagnostics, safe rename, and
`extract`/`inline`/`fill`/`rewrite` code actions. Reach it through gopls's own MCP server (`go_*` tools, preferred), the
native `LSP` tool, or the `gopls` CLI. Load it before any navigation-heavy read or any rename/extract/inline. It reasons
only about your locally resolved build (`go.sum`, including `replace` forks); for the published ecosystem use
`golang-pkg-go-dev`.

### golang-refactoring ( `$golang-refactoring` )

Use it for the safe, at-scale *process* of restructuring existing Go: a coverage-adaptive safety net, behavior-preserving
tool-driven transforms (gopls Rename/Inline/Extract, `gofmt -r`, `eg`, `gopatch`, `go/analysis` fixers), the Fowler
catalog mapped to Go, breaking import cycles, moving types across packages with type aliases, and a human-in-the-loop
flow of small stacked PRs. It owns *how* to change code safely; the *target shape* stays owned by `golang-naming`,
`golang-project-layout`, `golang-code-style`, `golang-design-patterns`, and `golang-modernize` — load it alongside
whichever of those defines the destination. Never mix a structural change and a behavioral change in one commit.

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
