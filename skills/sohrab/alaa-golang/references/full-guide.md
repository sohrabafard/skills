# Alaa Golang Full Guide

## Table of contents

- Service profile
- Language version stance
- Framework stance
- Architecture stance
- Code intelligence stance
- Data and cache stance
- Testing stance
- Observability and security stance
- Orchestration stance
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

## Language version stance

Target the current Go release and write modern Go by default.

- Assume Go 1.26 unless the repo's `go.mod` `go` directive or CI matrix says otherwise; match the repo, never regress it.
- Prefer current standard-library idioms over hand-rolled equivalents (`slices`, `maps`, `iter` iterators,
  range-over-func, `min`/`max`, `log/slog`, `errors.Join`, `t.Context` in tests).
- When touching older code, run a `golang-modernize` pass and adopt safe rewrites rather than leaving legacy idioms in
  place — but only up to the version the repo's `go` directive and CI actually support.
- Read `70-go-1.26-and-modern-language.md` for the Go 1.26 baseline and the adoption rules, and verify any
  version-sensitive claim against `SOURCES.md` before relying on it.

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

Read `60-service-architecture-patterns.md` for the default service shape. For any service on the `alaa-go-chi` base,
load `$alaa-golang-clean-code-principles` first — its P1–P13 principles are the mandatory kit-era discipline (kit-first
reuse, declared route posture, TrustCtx, typed errkit errors, ports/adapters, one-transaction-plus-outbox, idempotency,
explicit JSON/ids, owned goroutines, config-at-boot, bounded observability, contracts-never-reach-ins).

## Code intelligence stance

Read and reshape code semantically, not by grep-and-guess.

- Use `$golang-gopls` for navigation and diagnostics: `go_search` to locate a symbol, `go_file_context` on each file
  you open, `go_package_api` to read a dependency's surface, `go_symbol_references` before changing any definition, and
  `go_diagnostics` after every edit. It reasons about the resolved build, including `replace`d forks.
- Prefer gopls Rename/Inline/Extract and generated rewrites (`gofmt -r`, `eg`, `gopatch`) over hand-edits across many
  call sites — they are behavior-preserving by construction.
- Use `$golang-refactoring` for any staged, at-scale restructuring; keep each commit purely structural or purely
  behavioral, and never mix a code move with an optimization.
- Use `$golang-pkg-go-dev` (`godig`) for published-ecosystem facts (versions, symbols, importers, licenses, CVEs), and
  `govulncheck ./...` for the whole-tree reachable-CVE gate.

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

## Orchestration stance

For broad Go tasks, use `golang-how-to` as the vendor skill selector and then apply the Alaa rules in this skill.

- Load the primary and secondary public Go skills together when the task spans multiple concerns.
- Keep local Alaa references in force for framework choice, repository pattern, Redis cache behavior, trusted gateway
  context, TDD, observability, and production readiness.
- Do not run `golang-how-to` configure mode or edit project agent config files unless the user explicitly asks for
  always-loaded Go skills.

Read `11-orchestration-and-overlap-guide.md` for common bundles, overlap boundaries, recommended patterns, and
anti-patterns.

## Validation baseline

Use the narrowest checks that match the task:

- `go build ./...` and gopls `go_diagnostics` on changed files for a fast type/compile check
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

- Any Go code on `alaa-go-chi`: load `alaa-golang-clean-code-principles` ( `$alaa-golang-clean-code-principles` ) first for the P1–P13 discipline, then the vendor Go skills below.
- Broad Go task or unclear skill boundary: use `golang-how-to` ( `$golang-how-to` ) and `11-orchestration-and-overlap-guide.md`.
- Navigate, understand, or diagnose existing code: use `golang-gopls` ( `$golang-gopls` ) for semantic navigation and post-edit diagnostics.
- Restructure existing code at scale: use `golang-refactoring` ( `$golang-refactoring` ) with `golang-gopls` and the target-shape skill.
- Look up a published package: use `golang-pkg-go-dev` ( `$golang-pkg-go-dev` ), then `golang-dependency-management` to apply changes.
- Adopt latest Go (1.26) idioms: read `70-go-1.26-and-modern-language.md`, then use `golang-modernize` ( `$golang-modernize` ) and often `golang-lint` ( `$golang-lint` ).
- Design or review a service: use `golang-project-layout` ( `$golang-project-layout` ), `golang-design-patterns` ( `$golang-design-patterns` ), `golang-error-handling` ( `$golang-error-handling` ), `golang-observability` ( `$golang-observability` ), and local architecture references.
- Build or review Fiber: load `alaa-golang-fiber` ( `$alaa-golang-fiber` ).
- Build or review chi: read `31-chi-api-guide.md`.
- Debug concurrency or leaks: use `golang-concurrency` ( `$golang-concurrency` ), `golang-context` ( `$golang-context` ), `golang-safety` ( `$golang-safety` ), and `golang-troubleshooting` ( `$golang-troubleshooting` ).
- Build or audit GraphQL: use `golang-graphql` ( `$golang-graphql` ).
- Choose packages: read `40-production-ready-package-catalog.md`, then route to the narrow vendor skill if one exists.
- Change platform behavior, CI, contracts, trust boundaries, or deployment: add the relevant companion skill from `20-sohrab-companions.md`.
