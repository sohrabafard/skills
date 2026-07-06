# Go Skill Orchestration and Overlap Guide

Use this file after `full-guide.md` when a Go task is broad, ambiguous, or likely to need more than one public Go
skill.

This reference translates the vendor `golang-how-to` orchestration model into the Alaa Go rules. The public Go skills
provide detailed Go technique. `alaa-golang` adds platform boundaries: trusted gateway, repository pattern, Redis
cache-aside, TDD, observability, security, and production readiness.

## Core algorithm

1. Inspect repository evidence first: `go.mod`, imports, route setup, tests, docs, generated files, and existing
   conventions.
2. Choose one primary public Go skill for the main problem.
3. Add secondary public Go skills for adjacent risks at the start of the task, not after trouble appears.
4. Add local references from this skill when the task touches Alaa service architecture, cache policy, HTTP framework
   choice, trusted gateway context, tests, or production readiness.
5. Add Sohrab companion skills from `20-sohrab-companions.md` when the task crosses platform, security, data, delivery,
   or service-contract boundaries.
6. Keep the loaded set focused. Do not load every Go skill just because the task is written in Go.
7. Do not run `golang-how-to` configure mode or edit project `CLAUDE.md` / `AGENTS.md` files unless the user explicitly
   asks for always-loaded Go skills.

## Common task bundles

| Task shape | Primary skill | Also load | Local Alaa references |
| --- | --- | --- | --- |
| Design a new service or API | `golang-design-patterns` | `golang-project-layout`, `golang-structs-interfaces`, `golang-naming` | `60-service-architecture-patterns.md`, `62-clean-code-and-patterns.md` |
| Choose chi vs Fiber | `golang-how-to` | `golang-design-patterns`, `golang-testing` | `30-http-api-framework-choice.md`, `31-chi-api-guide.md`, or `$alaa-golang-fiber` |
| Implement DB-backed behavior | `golang-database` | `golang-error-handling`, `golang-security`, `golang-testing` | `60-service-architecture-patterns.md`, `63-tdd-and-testing-discipline.md` |
| Add Redis caching | `golang-performance` | `golang-concurrency`, `golang-safety`, `golang-testing` | `61-redis-cache-layer.md`, `60-service-architecture-patterns.md` |
| Build gRPC | `golang-grpc` | `golang-testing`, `golang-error-handling`, `golang-observability` | `60-service-architecture-patterns.md`, `20-sohrab-companions.md` if contracts matter |
| Build GraphQL | `golang-graphql` | `golang-testing`, `golang-error-handling`, `golang-security` | `40-production-ready-package-catalog.md`, `50-gap-coverage.md` |
| Build CLI | `golang-cli` | `golang-spf13-cobra` and `golang-spf13-viper` when imports or requirements fit | `63-tdd-and-testing-discipline.md` |
| Debug panic or bad output | `golang-troubleshooting` | `golang-safety`, `golang-testing`; add `golang-benchmark` only if performance-related | `62-clean-code-and-patterns.md` |
| Investigate slowness | `golang-observability` | `golang-benchmark`, then `golang-performance` after measurement | `40-production-ready-package-catalog.md` for tooling choices |
| Review security-sensitive code | `golang-security` | `golang-safety`, `golang-lint`, `golang-error-handling` | `20-sohrab-companions.md` for trust and service contracts |
| Change dependencies | `golang-dependency-management` | `golang-popular-libraries`, `golang-security`, `golang-continuous-integration` | `40-production-ready-package-catalog.md`, `SOURCES.md` |
| Configure CI | `golang-continuous-integration` | `golang-lint`, `golang-security`, `golang-testing` | Sohrab CI/CD companion if the repo is GitLab or platform-specific |
| Write tests | `golang-testing` | `golang-stretchr-testify` only when the repo uses Testify | `63-tdd-and-testing-discipline.md` |
| Use Samber helpers | matching `golang-samber-*` skill | adjacent correctness, performance, or error skill | Keep dependency use explicit and repo-conventional |
| Select DI approach | `golang-dependency-injection` | `golang-google-wire`, `golang-uber-dig`, `golang-uber-fx`, or `golang-samber-do` only when chosen or already present | `60-service-architecture-patterns.md` |
| Navigate or understand unfamiliar code | `golang-gopls` | `golang-project-layout` for module shape | read the file, then `go_search` / `go_file_context` / `go_package_api` — semantic, not grep |
| Refactor or restructure existing code | `golang-refactoring` | `golang-gopls` plus the target-shape skill (`golang-naming`, `golang-project-layout`, `golang-code-style`, `golang-design-patterns`, or `golang-modernize`) | `62-clean-code-and-patterns.md`, `63-tdd-and-testing-discipline.md`, and `$alaa-golang-clean-code-principles` for kit-era services |
| Look up a published package (versions, symbols, CVEs, importers, licenses) | `golang-pkg-go-dev` | `golang-dependency-management` to apply the change, `golang-security` for whole-tree scan | `40-production-ready-package-catalog.md`, `SOURCES.md` |
| Adopt latest Go language features | `golang-modernize` | `golang-lint`, `golang-gopls` for the mechanical rewrite | `70-go-1.26-and-modern-language.md` |

## Overlap boundaries

### Performance cluster

- `golang-observability`: production signals, dashboards, alerts, traces, structured logs.
- `golang-benchmark`: measurement, pprof, trace capture, benchstat, regression comparison.
- `golang-performance`: optimization patterns after a bottleneck is proven.
- `golang-troubleshooting`: root-cause workflow for crashes, deadlocks, unexpected behavior, and hard-to-reproduce bugs.

Recommended: observe first, measure second, optimize third.

Not recommended: applying pooling, caching, or low-level rewrites without a measured bottleneck.

### Dependency injection cluster

- `golang-dependency-injection`: concepts, manual constructors, and library selection.
- `golang-google-wire`: compile-time DI for repos already using Wire.
- `golang-uber-dig`: runtime reflection container without Fx lifecycle.
- `golang-uber-fx`: app framework with lifecycle hooks and modules.
- `golang-samber-do`: type-safe container with scopes and lifecycle.

Recommended: prefer manual constructor injection until the graph complexity justifies a tool.

Not recommended: introducing a DI framework to hide required dependencies or compensate for unclear package boundaries.

### Samber functional cluster

- `golang-samber-lo`: finite slice, map, channel, tuple, and iterator helpers.
- `golang-samber-ro`: reactive or event-driven streams.
- `golang-samber-mo`: Option, Result, Either, Future, IO, Task, and functional composition types.

Recommended: use a Samber skill when the repo already imports that package or the user explicitly asks for it.

Not recommended: adding functional helper packages when a short standard-library loop is clearer.

### Error, safety, and security cluster

- `golang-error-handling`: error creation, wrapping, matching, recovery, and single-handling rule.
- `golang-samber-oops`: structured errors when that package is already chosen.
- `golang-safety`: internal correctness hazards such as nil, slice aliasing, numeric overflow, concurrent maps, and zero values.
- `golang-security`: external threat model, injection, crypto, secrets, auth-sensitive code, filesystem and network safety.

Recommended: load `golang-safety` with `golang-security` for auth, parser, and untrusted-input changes.

Not recommended: treating a nil panic as a security issue unless an attacker can trigger or exploit it.

### Style, naming, lint, and docs cluster

- `golang-code-style`: clarity, formatting choices, comments, and local readability.
- `golang-naming`: package, type, function, interface, error, receiver, and test names.
- `golang-lint`: analyzer config, golangci-lint, suppressions, CI lint failures.
- `golang-documentation`: godoc, package comments, examples, README, changelog, and developer docs.

Recommended: use `golang-lint` for tool policy and `golang-code-style` for human readability.

Not recommended: using `//nolint` without a narrow reason and owner.

### CLI cluster

- `golang-cli`: command lifecycle, exit codes, signals, stdout/stderr, terminal behavior.
- `golang-spf13-cobra`: command trees, flags, completion, command tests.
- `golang-spf13-viper`: layered config, env binding, config files, hot reload, test isolation.

Recommended: load Cobra and Viper skills only when the imports exist or the CLI requirements justify them.

Not recommended: adding Cobra or Viper for a one-command internal tool with simple flags.

### Type design vs architecture

- `golang-structs-interfaces`: type-level decisions, method sets, embedding, interface size, struct tags.
- `golang-design-patterns`: architectural use of types, middleware chains, adapters, resilience, lifecycle, API shape.

Recommended: load both when a type decision changes service boundaries.

Not recommended: adding broad interfaces before there is a consumer that needs them.

### Concurrency vs context

- `golang-concurrency`: goroutine ownership, channels, locks, worker pools, backpressure, races.
- `golang-context`: cancellation, deadlines, request-scoped values, propagation, `WithoutCancel`.

Recommended: load both when goroutines are cancelled through context.

Not recommended: starting goroutines from handlers without explicit ownership, cancellation, and error reporting.

### Modernize vs lint

- `golang-modernize`: language and standard-library adoption.
- `golang-lint`: analyzer configuration, rule interpretation, suppression policy.

Recommended: use lint output to find candidates, then use modernize rules to choose safe rewrites.

Not recommended: adopting newer language features if the repo's `go.mod` or CI matrix does not support them.

### Package lookup and discovery cluster

Four skills touch third-party packages; each owns a different stage.

- `golang-pkg-go-dev`: read-only facts about a *published* import path via `godig` — versions, symbols, examples,
  `imported-by`, licenses, and CVEs, even for a package not yet in `go.mod`. It queries pkg.go.dev, never your checkout.
- `golang-popular-libraries`: which library to adopt for a use case; stdlib-vs-third-party judgment.
- `golang-dependency-management`: editing `go.mod` — `go get`, upgrade, pin, `replace`/`exclude`, tidy, workspaces.
- `golang-security`: whole-tree reachable-CVE scanning with `govulncheck` and remediation.

Recommended: `godig` to learn facts, `golang-dependency-management` to change `go.mod`, `golang-security` to prove a CVE
is reachable in your tree.

Not recommended: guessing a package version, CVE status, or importer set from memory when `godig` can answer it.

### Code intelligence: gopls vs godig vs govulncheck

These are not interchangeable; pick by whether the question is about your build or the ecosystem.

- `golang-gopls` (`gopls`): your *locally resolved* build — where a symbol is defined, every call site in your repo,
  interface satisfaction, post-edit diagnostics, safe rename/extract/inline, and a lightweight `go_vulncheck`
  reachability check mid-edit. Sees `replace`d forks; grep and `godig` cannot.
- `golang-pkg-go-dev` (`godig`): the *published ecosystem* — anything not tied to your build (versions, licenses,
  ecosystem-wide importers, CVEs of a package you have not added).
- `golang-security` (`govulncheck ./...`): the *whole-tree* audit of record for CI gates and periodic sweeps.

Recommended: use `gopls` to read and reshape code before editing (`go_search` → `go_file_context` →
`go_symbol_references` → edit → `go_diagnostics`); use `godig` for ecosystem facts; use `govulncheck` for the CI gate.

Not recommended: hand-editing across dozens of call sites when a gopls Rename or a generated `gofmt -r`/`eg`/`gopatch`
rewrite is behavior-preserving by construction.

### Refactoring vs target-shape skills

- `golang-refactoring`: the safe, staged *process* of changing existing code — blast-radius mapping, PR ordering
  (structural before behavioral), the refactoring-branch git model, tool-driven mechanics, and the coverage-adaptive
  safety net. It never owns what the result should look like.
- `golang-naming` / `golang-project-layout` / `golang-code-style` / `golang-design-patterns` / `golang-modernize`: the
  *target shape* — the new name, the new package, the target control flow, the target pattern, the modern idiom.

Recommended: load `golang-refactoring` together with whichever target-shape skill defines the destination, plus
`golang-gopls` as the actuator; keep every commit purely structural or purely behavioral, never both. For kit-era Ala
services, hold `$alaa-golang-clean-code-principles` (P1–P13) as the definition of the shape the refactor moves toward.

Not recommended: mixing a code move and an optimization in one PR, or refactoring critical code that has no test
safety net.

## Sample routing traces

### "Review this handler that queries Postgres and writes Redis"

Load `golang-how-to`, `golang-database`, `golang-error-handling`, `golang-security`, `golang-testing`, then read
`60-service-architecture-patterns.md`, `61-redis-cache-layer.md`, and `63-tdd-and-testing-discipline.md`.

Check for SQL or Redis in handlers, missing context propagation, unsafe auth assumptions, cache invalidation gaps, and
missing behavior tests.

### "The API is slow under load"

Load `golang-observability` first. If signals identify a hot path, load `golang-benchmark` for measurement and
`golang-performance` for fixes. Add `golang-concurrency` when goroutines, locks, channels, or worker pools are involved.

Avoid cache or pooling changes until the bottleneck is visible from traces, metrics, pprof, or benchmarks.

### "Create a GraphQL endpoint"

Load `golang-graphql`, `golang-testing`, `golang-error-handling`, and `golang-security`. Read
`40-production-ready-package-catalog.md` and `50-gap-coverage.md`.

Design schema, resolvers, batching, pagination, auth checks, query depth or complexity limits, error shaping, and tests
before implementation.

### "Add GitHub Actions for this Go repo"

Load `golang-continuous-integration`, `golang-lint`, `golang-security`, and `golang-testing`. If the repo uses GitLab,
add the Sohrab GitLab companion instead of forcing GitHub Actions.

Use current action major versions, least-privilege permissions, dependency scanning, `go test -race`, `go vet`,
`golangci-lint`, and release gates that match the repo.

### "Rename this exported method across the whole service and move it to a new package"

Load `golang-refactoring` as primary, `golang-gopls` as the actuator, and `golang-naming` plus `golang-project-layout`
for the target name and location. For a kit-era Ala service, also load `$alaa-golang-clean-code-principles`.

Map blast radius with `go_symbol_references` first, prefer gopls Rename over hand-edits, use a type alias for the moved
type so callers migrate gradually, grep for struct-tag and `text/template` references the rename cannot see, and land
the move and any behavioral change as separate atomic PRs.

### "Explain how this unfamiliar Postgres-backed service is wired"

Load `golang-gopls` first: `go_workspace` for layout, `go_search` to locate the entrypoint and route setup,
`go_file_context` on each file you open, and `go_package_api` to read a dependency's surface without reading every file.
Then read `60-service-architecture-patterns.md` to name the layers you find, and `$alaa-golang-clean-code-principles`
if the service is on `alaa-go-chi`.

Do not grep-and-guess call graphs when `go_symbol_references` gives the exact, build-accurate answer.
