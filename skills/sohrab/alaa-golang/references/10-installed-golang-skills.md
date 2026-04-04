# Installed Public Go Skills

Use this file when `alaa-golang` triggers and you need to select the already-installed public Go skills that should
handle the detailed work. Each entry explains the main decision surface and the usual companions.

## golang-benchmark

Use `golang-benchmark` when the question is about measuring performance rather than guessing about it. This is the first
stop for `pprof`, `benchstat`, trace interpretation, regression measurement, and proof that a claimed hot path is
actually hot before `golang-performance` changes code.

## golang-cli

Use `golang-cli` when the project is a command-line tool or when the task touches Cobra, Viper, flags, exit codes, shell
completion, config layering, or version embedding. Pair it with `golang-project-layout` for structure and
`golang-testing` for command behavior.

## golang-code-style

Use `golang-code-style` when code clarity, local conventions, comment quality, or line-by-line style rules are the main
question. It is the detailed style companion behind `alaa-golang`'s Uber-influenced baseline.

## golang-concurrency

Use `golang-concurrency` when goroutines, channels, locks, worker pools, errgroup flows, backpressure, or goroutine
leaks are involved. Pair it with `golang-context` whenever cancellation or request lifetimes matter.

## golang-context

Use `golang-context` when cancellation, deadlines, propagation, tracing context, or `context.Context` API boundaries are
the main issue. This skill keeps request and worker lifecycles explicit instead of hand-wavy.

## golang-continuous-integration

Use `golang-continuous-integration` when the task is about GitHub Actions, release gates, lint and test automation,
coverage, SAST, Dependabot, Renovate, or release packaging for Go projects. This is the CI owner, not the code-style
owner.

## golang-data-structures

Use `golang-data-structures` when slices, maps, arrays, heaps, builders, copy semantics, or generic containers are the
real decision surface. It is especially helpful when performance or mutation behavior depends on data-structure
internals.

## golang-database

Use `golang-database` when Go code is touching SQL, pools, transactions, isolation, query patterns, scanning,
nullability, or database tests. It owns application-side database access patterns, not schema design policy.

## golang-dependency-injection

Use `golang-dependency-injection` when you need to choose or refactor a wiring model, compare manual constructors
against DI libraries, or reason about service lifetime and composition. Pair it with `golang-project-layout` and
`golang-design-patterns` for larger service design work.

## golang-dependency-management

Use `golang-dependency-management` when the task is about `go.mod`, `go.work`, version selection, upgrades,
vulnerability review, dependency size, or update automation. It is the right companion before adding or replacing
non-trivial libraries.

## golang-design-patterns

Use `golang-design-patterns` when the question is architectural: constructors, options, lifecycle, resilience, modular
service design, or API-shaping patterns. It is the main design companion for services and reusable packages.

## golang-documentation

Use `golang-documentation` when the work is about package docs, godoc, examples, README, CONTRIBUTING, or published
developer guidance. Pair it with `alaa-docs-farsi` only when repository-level documentation strategy or Ala-style docs
are also in scope.

## golang-error-handling

Use `golang-error-handling` when error semantics, wrapping, inspection, classification, recovery, or structured logging
are under discussion. This is the detailed error owner behind `alaa-golang`'s "handle errors once" baseline.

## golang-grpc

Use `golang-grpc` when protobufs, gRPC service design, interceptors, bufconn tests, status codes, streaming RPCs, or
transport-level gRPC concerns are involved. It is the gRPC-specific transport owner.

## golang-lint

Use `golang-lint` when the task is about `golangci-lint`, `go vet`, linter selection, `.golangci.yml`, suppressions, or
interpreting lint output. This skill turns style policy into enforced tooling.

## golang-modernize

Use `golang-modernize` when code should adopt newer Go idioms, newer standard-library features, or newer tooling
practices. Start here when the repo feels stale or the request mentions upgrading to the latest Go patterns.

## golang-naming

Use `golang-naming` when the main problem is choosing better package, type, interface, error, enum, receiver, or test
names. It prevents a generic style review from turning into naming guesswork.

## golang-observability

Use `golang-observability` when the work is about structured logs, Prometheus, OpenTelemetry, continuous profiling,
trace correlation, or production signal design. Pair it with `alaa-observability-soc` when operational evidence
requirements matter.

## golang-performance

Use `golang-performance` after measurement has identified a real bottleneck and you need concrete optimization patterns.
It is not the first stop for "maybe this is slow"; that role belongs to `golang-benchmark`.

## golang-popular-libraries

Use `golang-popular-libraries` when the task asks for library recommendations or when a new dependency is about to be
introduced. It helps avoid random package choices and pushes the agent toward well-supported ecosystem options.

## golang-project-layout

Use `golang-project-layout` when the task is about repository shape, package placement, `cmd/`, `internal/`, monorepos,
workspaces, or server layout. It is especially relevant for Fiber services and mixed repos with commands plus packages.

## golang-safety

Use `golang-safety` when the code risks panics, aliasing bugs, nil misuse, numeric conversion problems, or unsafe
lifecycle behavior. It is the defensive-coding companion to style and concurrency work.

## golang-samber-do

Use `golang-samber-do` when the project already uses `github.com/samber/do/v2` or has decided to adopt it for dependency
injection and lifecycle management. Load it instead of treating Samber Do as generic DI.

## golang-samber-hot

Use `golang-samber-hot` when in-memory caching with `github.com/samber/hot` is in play or under evaluation. It owns
eviction strategy, stale handling, and cache-specific operational patterns for that library.

## golang-samber-lo

Use `golang-samber-lo` when the codebase already uses `github.com/samber/lo` or when functional helpers are the
deliberate approach for slice, map, or tuple transforms. It helps keep that style disciplined instead of ad hoc.

## golang-samber-mo

Use `golang-samber-mo` when the project uses or is evaluating `github.com/samber/mo` for monadic result or option flows.
This is the right companion when nullable or functional control-flow design is the real question.

## golang-samber-oops

Use `golang-samber-oops` when the codebase already depends on `github.com/samber/oops` or when the task is specifically
about adopting its structured error model. It should own Oops-specific behavior instead of generic error advice.

## golang-samber-ro

Use `golang-samber-ro` when the task is about reactive streams, observables, backpressure, or event-driven flows
implemented with `github.com/samber/ro`. Load it when the repo is genuinely using that model, not for ordinary
goroutines.

## golang-samber-slog

Use `golang-samber-slog` when the project uses Samber's `slog-*` extensions for routing, sampling, formatting, or
backend integration. It is the specialized companion for those packages on top of generic observability guidance.

## golang-security

Use `golang-security` when the task is a security review or touches injection, secrets, crypto, file safety, cookies,
network hardening, or risky user-input handling in Go. Pair it with `alaa-security-review` when the trust boundary
extends beyond generic code safety.

## golang-stay-updated

Use `golang-stay-updated` when the user wants learning resources, release news, community channels, or guidance on how
to keep up with the Go ecosystem. It is a knowledge-radar skill, not an implementation skill.

## golang-stretchr-testify

Use `golang-stretchr-testify` when the repo imports `testify` or the task is about assertions, mocks, suites, or
testify-specific testing behavior. Load it alongside `golang-testing` when the test strategy itself also matters.

## golang-structs-interfaces

Use `golang-structs-interfaces` when the design issue is about composition, embedding, interface size, type switches,
field tags, or receiver tradeoffs. It is the detailed type-system companion behind many design reviews.

## golang-testing

Use `golang-testing` for table-driven tests, unit and integration tests, race checks, fuzzing, fixtures, snapshot tests,
leak detection, or test architecture. This is the default test owner for Go tasks.

## golang-troubleshooting

Use `golang-troubleshooting` when something is wrong and the main need is root-cause debugging rather than design or
style guidance. It covers deadlocks, crashes, race detection, Delve, GODEBUG, and systematic debugging flow.
