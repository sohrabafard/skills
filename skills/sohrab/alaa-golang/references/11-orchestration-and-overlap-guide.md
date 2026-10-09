# Skill Overlap Boundaries

Read this when two skills both look like they own your question, or when a task needs more than one at once. The
single-situation router is `00-topic-map.md`; this file resolves the cases where several skills touch the same ground.

## Loading more than one skill

**Rule:** choose one primary skill for the problem you are solving, and load the secondary skills for the adjacent
risks at the start of the task, not after something breaks.

| The task is… | Primary | Also load |
|---|---|---|
| designing a new service or API | `/golang-design-patterns` | `/golang-project-layout`, `/golang-structs-interfaces`, `/golang-naming` |
| implementing database-backed behaviour | `/golang-database` | `/golang-error-handling`, `/golang-security`, `/golang-testing` |
| adding a cache | `/golang-performance` | `/golang-concurrency`, `/golang-safety`, `/golang-testing` |
| building gRPC | `/golang-grpc` | `/golang-testing`, `/golang-error-handling`, `/golang-observability` |
| building GraphQL | `/golang-graphql` | `/golang-testing`, `/golang-error-handling`, `/golang-security` |
| building a CLI | `/golang-cli` | `/golang-spf13-cobra`, `/golang-spf13-viper` when `go.mod` requires them |
| debugging a panic or wrong output | `/golang-troubleshooting` | `/golang-safety`, `/golang-testing` |
| investigating slowness | `/golang-observability` | `/golang-benchmark`, then `/golang-performance` |
| reviewing security-sensitive code | `/golang-security` | `/golang-safety`, `/golang-lint`, `/golang-error-handling` |
| changing dependencies | `/golang-dependency-management` | `/golang-pkg-go-dev`, `/golang-security` |
| configuring CI | `/golang-continuous-integration` | `/golang-lint`, `/golang-security`, `/golang-testing` |
| navigating unfamiliar code | `/alaa-code-intelligence-routing` | `/golang-project-layout` for package-layout decisions |
| restructuring existing code | `/golang-refactoring` | `/alaa-code-intelligence-routing` and the skill that defines the target shape |
| adopting a newer Go feature | `/golang-modernize` | `/golang-lint` and `/alaa-code-intelligence-routing` when a local code-intelligence question needs answering |

**Forbidden:** loading a Go skill because the task is written in Go. **Rule:** load a skill when the task hits the
condition that skill's row names, and no others.

**Forbidden:** running `/golang-how-to` configure mode, or editing a repository's `CLAUDE.md` or `AGENTS.md` to
force-load Go skills. **Rule:** if always-loaded Go skills would help, say so and let the user decide. This is the only
place in this skill that states this rule.

## Observability, benchmark, performance, troubleshooting

- `/golang-observability` — production signals, dashboards, traces, structured logs.
- `/golang-benchmark` — measurement: `testing.B`, pprof, traces, `benchstat`.
- `/golang-performance` — optimisation of a bottleneck that has been measured.
- `/golang-troubleshooting` — root cause of a crash, deadlock, or behaviour nobody can explain.

**Rule:** observe, then measure, then optimise, in that order.
**Forbidden:** adding pooling, caching, preallocation, or a low-level rewrite before a profile or a benchmark names
the bottleneck. **Rule:** when asked to make something faster with no measurement in hand, produce the measurement
first and report it.

## Dependency injection

- `/golang-dependency-injection` — the approach.
- `/golang-google-wire`, `/golang-uber-dig`, `/golang-uber-fx`, `/golang-samber-do` — one per framework.

**Rule:** load a framework skill when `go.mod` already requires that framework.
**Forbidden:** introducing a DI framework into a service that does not require one, and using a container to supply a
dependency a constructor could take as an argument.

## Samber packages

- `/golang-samber-lo` — slice, map, channel, and tuple helpers.
- `/golang-samber-ro` — reactive streams.
- `/golang-samber-mo` — Option, Result, Either, Future.
- `/golang-samber-oops` — structured errors.
- `/golang-samber-hot` — in-process caching.
- `/golang-samber-slog` — slog adapters and handlers.
- `/golang-samber-do` — dependency container.

**Rule:** load one when `go.mod` requires that package, or when the user names it.
**Forbidden:** adding a functional-helper package to replace a loop that fits in five lines.

## Errors, safety, security

- `/golang-error-handling` — creating, wrapping, matching, and handling an error exactly once.
- `/golang-safety` — nil, slice aliasing, numeric conversion, concurrent maps, zero values.
- `/golang-security` — injection, crypto, secrets, filesystem and network exposure, untrusted input.

**Rule:** load `/golang-safety` together with `/golang-security` whenever the change parses untrusted input or sits on
an authentication or authorization path.
**Forbidden:** reporting a nil dereference as a security finding unless a caller from outside the trust boundary can
reach it. **Rule:** say who can reach it, or report it as a correctness defect.

## Style, naming, lint, documentation

- `/golang-code-style` — clarity and readability for a human.
- `/golang-naming` — package, type, function, error, receiver, and test names.
- `/golang-lint` — analyzer configuration and suppression policy.
- `/golang-documentation` — package docs, examples, README, changelog.

**Rule:** `/golang-lint` decides what the tool enforces; `/golang-code-style` decides what a reviewer asks for.
**Forbidden:** a `//nolint` without the specific linter named and a comment giving the reason. **Rule:** if the reason
cannot be written in one line, fix the code instead.

## CLI

- `/golang-cli` — command lifecycle, exit codes, signals, stdout and stderr.
- `/golang-spf13-cobra` — command trees, flags, completion.
- `/golang-spf13-viper` — layered config, environment binding, hot reload.

**Rule:** load Cobra or Viper when `go.mod` requires them.
**Forbidden:** adding either to a tool with one command and three flags.

## Type design against architecture

- `/golang-structs-interfaces` — method sets, receivers, embedding, interface size, struct tags.
- `/golang-design-patterns` — middleware chains, adapters, lifecycle, API shape.

**Rule:** load both when a type decision moves a boundary between packages.
**Forbidden:** declaring an interface before a consumer exists that calls every method on it.

## Concurrency against context

- `/golang-concurrency` — goroutine ownership, channels, locks, worker pools, backpressure, races.
- `/golang-context` — cancellation, deadlines, request-scoped values, propagation.

**Rule:** load both whenever a goroutine is cancelled through a context.

**Forbidden — absolutely, with no exception:** starting a goroutine that has no owner, no cancellation path, and no
place its error is reported. This is P9 in `/alaa-golang-clean-code-principles`, it is a rule and not a preference,
and this file does not soften it. **Rule:** every goroutine is started by a component that also stops it, takes a
context that shutdown cancels, and either returns its error to that owner or is a documented fire-and-forget whose
failure is recorded as a metric.

## Modernize against lint

- `/golang-modernize` — language and standard-library adoption.
- `/golang-lint` — analyzer configuration and rule interpretation.

**Rule:** use lint output to find candidates and modernize rules to choose the rewrite.
**Forbidden:** adopting a language feature the repository's `go` directive does not allow — see
`70-modern-go-baseline.md`.

## Local semantics against godig against govulncheck

The dividing question is whether you are asking about *this repository's build* or *the published ecosystem*.

- /alaa-code-intelligence-routing — evidence and editing surfaces for this repository;
  it owns provider selection and degraded operation.
- `/golang-pkg-go-dev` — the published ecosystem: versions, symbols, examples, importers, licences, and CVEs of a
  package, including one not yet in `go.mod`. It queries pkg.go.dev, never your checkout.
- `/golang-security` — the whole-tree reachable-CVE audit with `govulncheck ./...`, which is the gate of record.

**Rule:** route local evidence and editing-surface choices through /alaa-code-intelligence-routing,
learn ecosystem facts with godig, and gate releases with `govulncheck`.
**Forbidden:** stating a package's version, licence, CVE status, or importer set from memory. **Rule:** query
`godig` and cite what it returned.

## Refactoring against the target shape

- `/golang-refactoring` — the process: blast radius, PR ordering, the branch model, tool-driven transforms, the
  coverage safety net. It never decides what the result should look like.
- `/golang-naming`, `/golang-project-layout`, `/golang-code-style`, `/golang-design-patterns`, `/golang-modernize` —
  the destination: the new name, the new package, the target shape, the modern idiom.
- `/alaa-golang-clean-code-principles` — the destination for any service on the kit.

**Rule:** load the process skill and the destination skill together; use /alaa-code-intelligence-routing
for the editing surface and any missing semantic guarantee before the dependent operation.
**Forbidden:** a commit that both moves code and changes behaviour. **Rule:** land the move, verify the tests are
unchanged and green, then land the behaviour change separately.
**Forbidden:** refactoring code that has no test covering the behaviour being preserved. **Rule:** add that test
first — `63-tdd-and-testing-discipline.md` — or report that you cannot and stop.
