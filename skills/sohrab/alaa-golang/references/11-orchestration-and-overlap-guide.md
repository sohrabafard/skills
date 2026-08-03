# Skill Overlap Boundaries

Read this when two skills both look like they own your question, or when a task needs more than one at once. The
single-situation router is `00-topic-map.md`; this file resolves the cases where several skills touch the same ground.

Trigger forms: Claude Code `/name`, Codex `$name`.

## Loading more than one skill

**Rule:** choose one primary skill for the problem you are solving, and load the secondary skills for the adjacent
risks at the start of the task, not after something breaks.

| The task is… | Primary | Also load |
|---|---|---|
| designing a new service or API | `/golang-design-patterns` (`$golang-design-patterns`) | `/golang-project-layout` (`$golang-project-layout`), `/golang-structs-interfaces` (`$golang-structs-interfaces`), `/golang-naming` (`$golang-naming`) |
| implementing database-backed behaviour | `/golang-database` (`$golang-database`) | `/golang-error-handling` (`$golang-error-handling`), `/golang-security` (`$golang-security`), `/golang-testing` (`$golang-testing`) |
| adding a cache | `/golang-performance` (`$golang-performance`) | `/golang-concurrency` (`$golang-concurrency`), `/golang-safety` (`$golang-safety`), `/golang-testing` (`$golang-testing`) |
| building gRPC | `/golang-grpc` (`$golang-grpc`) | `/golang-testing` (`$golang-testing`), `/golang-error-handling` (`$golang-error-handling`), `/golang-observability` (`$golang-observability`) |
| building GraphQL | `/golang-graphql` (`$golang-graphql`) | `/golang-testing` (`$golang-testing`), `/golang-error-handling` (`$golang-error-handling`), `/golang-security` (`$golang-security`) |
| building a CLI | `/golang-cli` (`$golang-cli`) | `/golang-spf13-cobra` (`$golang-spf13-cobra`), `/golang-spf13-viper` (`$golang-spf13-viper`) when `go.mod` requires them |
| debugging a panic or wrong output | `/golang-troubleshooting` (`$golang-troubleshooting`) | `/golang-safety` (`$golang-safety`), `/golang-testing` (`$golang-testing`) |
| investigating slowness | `/golang-observability` (`$golang-observability`) | `/golang-benchmark` (`$golang-benchmark`), then `/golang-performance` (`$golang-performance`) |
| reviewing security-sensitive code | `/golang-security` (`$golang-security`) | `/golang-safety` (`$golang-safety`), `/golang-lint` (`$golang-lint`), `/golang-error-handling` (`$golang-error-handling`) |
| changing dependencies | `/golang-dependency-management` (`$golang-dependency-management`) | `/golang-pkg-go-dev` (`$golang-pkg-go-dev`), `/golang-security` (`$golang-security`) |
| configuring CI | `/golang-continuous-integration` (`$golang-continuous-integration`) | `/golang-lint` (`$golang-lint`), `/golang-security` (`$golang-security`), `/golang-testing` (`$golang-testing`) |
| navigating unfamiliar code | `/alaa-code-intelligence-routing` (`$alaa-code-intelligence-routing`) | `/golang-project-layout` (`$golang-project-layout`); CodeGraph maps unknown structure and Serena answers the exact known symbol |
| restructuring existing code | `/golang-refactoring` (`$golang-refactoring`) | `/alaa-code-intelligence-routing` (`$alaa-code-intelligence-routing`) and the skill that defines the target shape |
| adopting a newer Go feature | `/golang-modernize` (`$golang-modernize`) | `/golang-lint` (`$golang-lint`) and the semantic diagnostics selected by `/alaa-code-intelligence-routing` (`$alaa-code-intelligence-routing`) |

**Forbidden:** loading a Go skill because the task is written in Go. **Rule:** load a skill when the task hits the
condition that skill's row names, and no others.

**Forbidden:** running `/golang-how-to` (`$golang-how-to`) configure mode, or editing a repository's `CLAUDE.md` or `AGENTS.md` to
force-load Go skills. **Rule:** if always-loaded Go skills would help, say so and let the user decide. This is the only
place in this skill that states this rule.

## Observability, benchmark, performance, troubleshooting

- `/golang-observability` (`$golang-observability`) — production signals, dashboards, traces, structured logs.
- `/golang-benchmark` (`$golang-benchmark`) — measurement: `testing.B`, pprof, traces, `benchstat`.
- `/golang-performance` (`$golang-performance`) — optimisation of a bottleneck that has been measured.
- `/golang-troubleshooting` (`$golang-troubleshooting`) — root cause of a crash, deadlock, or behaviour nobody can explain.

**Rule:** observe, then measure, then optimise, in that order.
**Forbidden:** adding pooling, caching, preallocation, or a low-level rewrite before a profile or a benchmark names
the bottleneck. **Rule:** when asked to make something faster with no measurement in hand, produce the measurement
first and report it.

## Dependency injection

- `/golang-dependency-injection` (`$golang-dependency-injection`) — the approach.
- `/golang-google-wire` (`$golang-google-wire`), `/golang-uber-dig` (`$golang-uber-dig`), `/golang-uber-fx` (`$golang-uber-fx`), `/golang-samber-do` (`$golang-samber-do`) — one per framework.

**Rule:** load a framework skill when `go.mod` already requires that framework.
**Forbidden:** introducing a DI framework into a service that does not require one, and using a container to supply a
dependency a constructor could take as an argument.

## Samber packages

- `/golang-samber-lo` (`$golang-samber-lo`) — slice, map, channel, and tuple helpers.
- `/golang-samber-ro` (`$golang-samber-ro`) — reactive streams.
- `/golang-samber-mo` (`$golang-samber-mo`) — Option, Result, Either, Future.
- `/golang-samber-oops` (`$golang-samber-oops`) — structured errors.
- `/golang-samber-hot` (`$golang-samber-hot`) — in-process caching.
- `/golang-samber-slog` (`$golang-samber-slog`) — slog adapters and handlers.
- `/golang-samber-do` (`$golang-samber-do`) — dependency container.

**Rule:** load one when `go.mod` requires that package, or when the user names it.
**Forbidden:** adding a functional-helper package to replace a loop that fits in five lines.

## Errors, safety, security

- `/golang-error-handling` (`$golang-error-handling`) — creating, wrapping, matching, and handling an error exactly once.
- `/golang-safety` (`$golang-safety`) — nil, slice aliasing, numeric conversion, concurrent maps, zero values.
- `/golang-security` (`$golang-security`) — injection, crypto, secrets, filesystem and network exposure, untrusted input.

**Rule:** load `/golang-safety` (`$golang-safety`) together with `/golang-security` (`$golang-security`) whenever the change parses untrusted input or sits on
an authentication or authorization path.
**Forbidden:** reporting a nil dereference as a security finding unless a caller from outside the trust boundary can
reach it. **Rule:** say who can reach it, or report it as a correctness defect.

## Style, naming, lint, documentation

- `/golang-code-style` (`$golang-code-style`) — clarity and readability for a human.
- `/golang-naming` (`$golang-naming`) — package, type, function, error, receiver, and test names.
- `/golang-lint` (`$golang-lint`) — analyzer configuration and suppression policy.
- `/golang-documentation` (`$golang-documentation`) — package docs, examples, README, changelog.

**Rule:** `/golang-lint` (`$golang-lint`) decides what the tool enforces; `/golang-code-style` (`$golang-code-style`) decides what a reviewer asks for.
**Forbidden:** a `//nolint` without the specific linter named and a comment giving the reason. **Rule:** if the reason
cannot be written in one line, fix the code instead.

## CLI

- `/golang-cli` (`$golang-cli`) — command lifecycle, exit codes, signals, stdout and stderr.
- `/golang-spf13-cobra` (`$golang-spf13-cobra`) — command trees, flags, completion.
- `/golang-spf13-viper` (`$golang-spf13-viper`) — layered config, environment binding, hot reload.

**Rule:** load Cobra or Viper when `go.mod` requires them.
**Forbidden:** adding either to a tool with one command and three flags.

## Type design against architecture

- `/golang-structs-interfaces` (`$golang-structs-interfaces`) — method sets, receivers, embedding, interface size, struct tags.
- `/golang-design-patterns` (`$golang-design-patterns`) — middleware chains, adapters, lifecycle, API shape.

**Rule:** load both when a type decision moves a boundary between packages.
**Forbidden:** declaring an interface before a consumer exists that calls every method on it.

## Concurrency against context

- `/golang-concurrency` (`$golang-concurrency`) — goroutine ownership, channels, locks, worker pools, backpressure, races.
- `/golang-context` (`$golang-context`) — cancellation, deadlines, request-scoped values, propagation.

**Rule:** load both whenever a goroutine is cancelled through a context.

**Forbidden — absolutely, with no exception:** starting a goroutine that has no owner, no cancellation path, and no
place its error is reported. This is P9 in `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`), it is a rule and not a preference,
and this file does not soften it. **Rule:** every goroutine is started by a component that also stops it, takes a
context that shutdown cancels, and either returns its error to that owner or is a documented fire-and-forget whose
failure is recorded as a metric.

## Modernize against lint

- `/golang-modernize` (`$golang-modernize`) — language and standard-library adoption.
- `/golang-lint` (`$golang-lint`) — analyzer configuration and rule interpretation.

**Rule:** use lint output to find candidates and modernize rules to choose the rewrite.
**Forbidden:** adopting a language feature the repository's `go` directive does not allow — see
`70-modern-go-baseline.md`.

## Local semantics against godig against govulncheck

The dividing question is whether you are asking about *this repository's build* or *the published ecosystem*.

- `/alaa-code-intelligence-routing` (`$alaa-code-intelligence-routing`) — this repository: CodeGraph for unknown
  structure, Serena for known Go symbols and semantic edits, and direct `/golang-gopls` (`$golang-gopls`) only for one
  recorded unavailable, unhealthy, or missing build-aware operation. Serena's Go backend itself uses `gopls`.
- `/golang-pkg-go-dev` (`$golang-pkg-go-dev`) — the published ecosystem: versions, symbols, examples, importers, licences, and CVEs of a
  package, including one not yet in `go.mod`. It queries pkg.go.dev, never your checkout.
- `/golang-security` (`$golang-security`) — the whole-tree reachable-CVE audit with `govulncheck ./...`, which is the gate of record.

**Rule:** read and reshape through the selected semantic owner, learn ecosystem facts with godig, and gate releases with `govulncheck`.
**Forbidden:** stating a package's version, licence, CVE status, or importer set from memory. **Rule:** query
`godig` and cite what it returned.

## Refactoring against the target shape

- `/golang-refactoring` (`$golang-refactoring`) — the process: blast radius, PR ordering, the branch model, tool-driven transforms, the
  coverage safety net. It never decides what the result should look like.
- `/golang-naming` (`$golang-naming`), `/golang-project-layout` (`$golang-project-layout`), `/golang-code-style` (`$golang-code-style`), `/golang-design-patterns` (`$golang-design-patterns`), `/golang-modernize` (`$golang-modernize`) —
  the destination: the new name, the new package, the target shape, the modern idiom.
- `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) — the destination for any service on the kit.

**Rule:** load the process skill and the destination skill together, with the semantic actuator selected by
`/alaa-code-intelligence-routing` (`$alaa-code-intelligence-routing`); Serena is the default Go surface and direct
`/golang-gopls` (`$golang-gopls`) is one recorded fallback.
**Forbidden:** a commit that both moves code and changes behaviour. **Rule:** land the move, verify the tests are
unchanged and green, then land the behaviour change separately.
**Forbidden:** refactoring code that has no test covering the behaviour being preserved. **Rule:** add that test
first — `63-tdd-and-testing-discipline.md` — or report that you cannot and stop.
