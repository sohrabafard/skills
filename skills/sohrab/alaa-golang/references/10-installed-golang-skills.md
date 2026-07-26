# The Vendor Go Skill Roster

The complete set of installed public `golang-*` skills and the condition that selects each one. When two of them look
equally right, `11-orchestration-and-overlap-guide.md` decides.

**Rule:** load a skill by naming it in the trigger form of the runtime you are in — Claude Code `/golang-testing`,
Codex `$golang-testing`. **Forbidden:** mentioning a vendor directory path in an answer to a user.

**Forbidden:** restating a vendor skill's content in this pack or in a repository. **Rule:** load it and follow it.
These skills are git subtrees; nothing in this pack edits them.

## Roster audit

One `###` entry below per `vendor/cc-skills-golang/skills/*/SKILL.md`. Last audited against vendor subtree
`112a945f0d7489b848705ab6f4fbf8c30c4ff053` (upstream `4881c01d`): `vendor=46 routed=46 missing=0 extra=0`.

This is the only place in this skill that states the roster size or the audit line. **Rule:** when the vendor pack
adds or removes a skill, update this file's entry list and this audit line, and nothing else.

## Orchestration

### golang-how-to (`/golang-how-to` · `$golang-how-to`)

Load it when the task is broad enough that you cannot name the primary Go skill yourself. It selects a primary plus
secondaries and carries the vendor catalogue. **Forbidden:** running its configure mode; see
`11-orchestration-and-overlap-guide.md`.

## Structure, architecture, and API shape

### golang-project-layout (`/golang-project-layout` · `$golang-project-layout`)

Module shape, folder layout, package boundaries, `cmd/` and `internal/`, workspaces, test layout.

### golang-design-patterns (`/golang-design-patterns` · `$golang-design-patterns`)

Boundary design, service layering, adapters and ports, constructors, resilience patterns, graceful-shutdown patterns.

### golang-structs-interfaces (`/golang-structs-interfaces` · `$golang-structs-interfaces`)

Interface size, receiver choice, type design, method sets, struct tags, embedding.

### golang-dependency-injection (`/golang-dependency-injection` · `$golang-dependency-injection`)

Choosing or changing a DI approach.

### golang-google-wire (`/golang-google-wire` · `$golang-google-wire`)

Load when `go.mod` requires `github.com/google/wire`, or the repository has `wire.Build`, `wire.NewSet`, or
`wire_gen.go`.

### golang-uber-dig (`/golang-uber-dig` · `$golang-uber-dig`)

Load when `go.mod` requires `go.uber.org/dig`.

### golang-uber-fx (`/golang-uber-fx` · `$golang-uber-fx`)

Load when `go.mod` requires `go.uber.org/fx`, or the code uses Fx modules or lifecycle hooks.

### golang-code-style (`/golang-code-style` · `$golang-code-style`)

Clarity, comment quality, line-level readability.

### golang-naming (`/golang-naming` · `$golang-naming`)

Package, exported identifier, error, method, receiver, and test names.

## Language, correctness, and debugging

### golang-modernize (`/golang-modernize` · `$golang-modernize`)

Version-aware rewrites, newer standard-library idioms, release upgrades, modernize analyzer output.

### golang-concurrency (`/golang-concurrency` · `$golang-concurrency`)

Goroutines, channels, `errgroup`, worker pools, backpressure, leaks, shared state.

### golang-context (`/golang-context` · `$golang-context`)

Cancellation, deadlines, propagation, request lifetime, `WithoutCancel`.

### golang-safety (`/golang-safety` · `$golang-safety`)

Nil safety, map and slice hazards, aliasing, numeric conversion, resource lifecycle, race-prone patterns.

### golang-error-handling (`/golang-error-handling` · `$golang-error-handling`)

Error creation, wrapping, sentinels, custom types, propagation, error-contract design.

### golang-troubleshooting (`/golang-troubleshooting` · `$golang-troubleshooting`)

Production debugging, compiler and test failures, deadlocks, panics, `pprof`, Delve.

## Data and dependencies

### golang-database (`/golang-database` · `$golang-database`)

Query patterns, pools, transactions, scanning, isolation, locking, application-side database access.

### golang-data-structures (`/golang-data-structures` · `$golang-data-structures`)

How a Go slice, map, builder, heap, generic container, or weak pointer behaves. **Rule:** for what a path is allowed
to *cost* as its input grows, load `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) instead.

### golang-dependency-management (`/golang-dependency-management` · `$golang-dependency-management`)

Editing `go.mod`: adding, upgrading, pinning, replacing, tidying, workspaces.

### golang-pkg-go-dev (`/golang-pkg-go-dev` · `$golang-pkg-go-dev`)

Querying pkg.go.dev with `godig` for a known import path: versions, exported symbols, examples, importers, licences,
CVEs — including a package not yet in `go.mod`.

### golang-popular-libraries (`/golang-popular-libraries` · `$golang-popular-libraries`)

Broad library discovery. Pair with `40-production-ready-package-catalog.md` for the final choice in this stack.

## Transport, protocols, CLIs, and docs

### golang-grpc (`/golang-grpc` · `$golang-grpc`)

gRPC services, protobuf generation, interceptors, streaming, TLS and mTLS, `bufconn` tests, status errors.

### golang-graphql (`/golang-graphql` · `$golang-graphql`)

GraphQL servers, schemas, resolvers, subscriptions, `gqlgen`, N+1 prevention, complexity limits.

### golang-cli (`/golang-cli` · `$golang-cli`)

Command lifecycle, flags, config layering, exit codes, I/O, signals, CLI tests.

### golang-spf13-cobra (`/golang-spf13-cobra` · `$golang-spf13-cobra`)

Load when `go.mod` requires `github.com/spf13/cobra`.

### golang-spf13-viper (`/golang-spf13-viper` · `$golang-spf13-viper`)

Load when `go.mod` requires `github.com/spf13/viper`.

### golang-swagger (`/golang-swagger` · `$golang-swagger`)

Swagger and OpenAPI with `swaggo/swag`: annotations, generated docs, UI routes, framework integration.

## Code intelligence, navigation, and refactoring

### golang-gopls (`/golang-gopls` · `$golang-gopls`)

Semantic code intelligence through `gopls`: definitions, references, call and implementation hierarchies, workspace
symbol search, package API discovery, post-edit diagnostics, safe rename, and extract/inline/fill/rewrite actions.
Reach it through the gopls MCP server (`go_*` tools), the native LSP tool, or the CLI. It reasons about the locally
resolved build, including `replace`d forks.

### golang-refactoring (`/golang-refactoring` · `$golang-refactoring`)

The safe, staged process of restructuring existing Go: coverage safety net, behaviour-preserving transforms (gopls
Rename, Inline, Extract; `gofmt -r`; `eg`; `gopatch`; `go/analysis` fixers), breaking import cycles, moving types with
aliases, and small stacked PRs. It owns *how*; the target shape is owned elsewhere.

## Quality, operations, and delivery

### golang-testing (`/golang-testing` · `$golang-testing`)

Unit, integration, HTTP, fuzz, race, fixture, mock, and coverage mechanics.

### golang-stretchr-testify (`/golang-stretchr-testify` · `$golang-stretchr-testify`)

Load when `go.mod` requires Testify.

### golang-lint (`/golang-lint` · `$golang-lint`)

`golangci-lint`, `go vet`, analyzer policy, `nolint` hygiene, staticcheck, revive, configuration.

### golang-benchmark (`/golang-benchmark` · `$golang-benchmark`)

`testing.B`, `benchstat`, profiles, regression detection, measurement methodology.

### golang-performance (`/golang-performance` · `$golang-performance`)

CPU, memory, I/O, GC, pooling, and hot-path optimisation — after a bottleneck is measured.

### golang-observability (`/golang-observability` · `$golang-observability`)

Logs, metrics, traces, profiling, dashboards, alerting, production telemetry mechanics.

### golang-security (`/golang-security` · `$golang-security`)

Code-level hardening, injection defences, secrets, crypto, filesystem safety, `govulncheck ./...` as the whole-tree
gate.

### golang-documentation (`/golang-documentation` · `$golang-documentation`)

Package docs, exported comments, examples, README, changelog.

### golang-continuous-integration (`/golang-continuous-integration` · `$golang-continuous-integration`)

CI, release gates, dependency automation, security scans, coverage, GoReleaser.

## Samber packages

**Rule:** load one of these when `go.mod` requires that package, or when the user names it.

### golang-samber-do (`/golang-samber-do` · `$golang-samber-do`)
`github.com/samber/do` and `/v2` dependency injection and service lifecycle.

### golang-samber-lo (`/golang-samber-lo` · `$golang-samber-lo`)
`github.com/samber/lo` functional helpers.

### golang-samber-mo (`/golang-samber-mo` · `$golang-samber-mo`)
`github.com/samber/mo` Option, Result, Either, Future, IO, Task.

### golang-samber-ro (`/golang-samber-ro` · `$golang-samber-ro`)
`github.com/samber/ro` reactive streams and event pipelines.

### golang-samber-slog (`/golang-samber-slog` · `$golang-samber-slog`)
Samber `slog-*` adapters, routing, sampling, and backend handlers.

### golang-samber-hot (`/golang-samber-hot` · `$golang-samber-hot`)
`github.com/samber/hot` in-memory caching.

### golang-samber-oops (`/golang-samber-oops` · `$golang-samber-oops`)
`github.com/samber/oops` structured errors.

## Ecosystem awareness

### golang-stay-updated (`/golang-stay-updated` · `$golang-stay-updated`)

Load when the task is learning or discovery about the Go ecosystem rather than changing code.
