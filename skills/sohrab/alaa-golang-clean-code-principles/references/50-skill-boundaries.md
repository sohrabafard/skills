# Skill Boundaries — What This Skill Does Not Own

This skill adds nothing on the topics below. When a task needs one, load the owner and let it answer. Every
vendor Go skill in the first table is reached through the `/alaa-golang` router, which selects
among all 46 of them; the direct trigger is given so you can jump when the router has already chosen.

## Go depth — owned by the `alaa-golang` tree

| Topic | Owner |
|---|---|
| Naming conventions | `/golang-naming` |
| Line-level style and clarity | `/golang-code-style` |
| Project layout and monorepos | `/golang-project-layout` |
| Struct and interface design, embedding, receivers | `/golang-structs-interfaces` |
| Design-pattern mechanics — functional options, constructor idioms, resilience wrappers, iterator internals | `/golang-design-patterns` |
| DI stance — manual first; wire, dig, fx, or do when the repo imports them | `/golang-dependency-injection` plus the matching package skill |
| Concurrency, channels, `errgroup` | `/golang-concurrency` |
| `context` propagation | `/golang-context` |
| Nil-safety, aliasing, defensive copies | `/golang-safety` |
| Error mechanics — wrapping, `Is`/`As`, sentinels | `/golang-error-handling` |
| Database access patterns | `/golang-database` |
| Test and benchmark mechanics | `/golang-testing`, `/golang-stretchr-testify`, `/golang-benchmark` |
| Performance, profiling, troubleshooting | `/golang-performance`, `/golang-troubleshooting` |
| Language-level security | `/golang-security` |
| Lint configuration | `/golang-lint` |
| Modern idioms, upgrades, latest-Go features | `/golang-modernize` plus `/alaa-golang` reference 70 |
| Structural discovery and semantic code navigation | `/alaa-code-intelligence-routing`: CodeGraph for unknown structure, Serena for known Go symbols and diagnostics, direct `/golang-gopls` only for one recorded fallback |
| Safe, staged, at-scale refactoring process | `/golang-refactoring` |
| Published-package lookup — versions, CVEs, symbols | `/golang-pkg-go-dev` |
| Go map and slice behavior | `/golang-data-structures` |
| chi-vs-Fiber policy, Ala Go baseline, repository pattern, Redis cache rules, TDD discipline | `/alaa-golang` references 30, 31, 60, 61, 62, 63 |

**The pattern boundary, stated precisely so it can be checked.**
`references/60-design-patterns-kit-era.md` names *decisions*: which pattern a symptom indicates, which kit
surface or principle already owns that pattern's job, and which look-alike it is not. It ships no implementation
mechanic — no idiom, no code shape, no internal. Every "how do I write it" question goes to
`/golang-design-patterns` through the router. If you find a Go mechanic in that
file, it is a defect in this skill: delete it and route the reader.

## Doctrine this skill applies but does not legislate

| Question | Owner |
|---|---|
| Retry counts, backoff curves, timeout budgets, degradation, the ambiguous-timeout rule | `/alaa-reliability-sla` |
| Which layer to test a behavior at, doubles, flake control, coverage policy | `/alaa-testing-strategy` |
| Required signals, severity rubric, the definition-of-done gate for a shipped feature, SOC evidence | `/alaa-observability-soc` |
| The *names* of metrics, events, error codes, queues, headers; exact envelope and readiness shapes | `/alaa-services-contract` |
| Capacity, topology, and consistency decisions above a single service | `/alaa-system-design` |
| How good is good enough — the platform quality bar | `/alaa-project-constitution` `references/quality-bar.md` |
| The active kit scope phase, kit contract changes, releases, consumer registration and audits | `/alaa-go-chi-development` |
| Trusted-header semantics, permission bitmap, gateway boundary | `/alaa-trust-gateway-auth` |
| Broker architecture beyond `mqkit`'s surface | `/alaa-async-messaging` |
| Authn, authz, tenant isolation, trust-boundary changes | `/alaa-security-review` |
| The complexity budget of a growing path, the real bound on an input dimension, structure choice from the access pattern, and the N+1 family across database, HTTP, cache, and permission calls | `/alaa-algorithms-data-structures` |
| Model choice, reasoning effort, runtime capability | `/alaa-prompting-guide` `references/50-effort-and-thinking.md` |
| Container, Kubernetes, and CI delivery | `/alaa-docker-production`, `/alaa-k8s-helm`, `/alaa-gitlab-ci-cd` |

Division of labor in one sentence: **`/alaa-golang` teaches you to write good Go; this skill
teaches you to write Go that belongs on this platform; `/alaa-go-chi-development` decides when the platform lets you write it at all.**

When guidance appears to conflict, platform contracts win — `/alaa-services-contract` for exact shapes, this skill for kit-era discipline. A real conflict is a drift to
record in a change request through `/alaa-go-chi-development`, never a
disagreement to resolve silently in code.

## Companion routing

- `/alaa-golang` — the mandatory router for every Go depth topic; the tables above give the exact division.
- `/alaa-go-chi-development` — the active scope phase, the kit capability and
  surface inventory that P1 is checked against, and the change-request channel P1 sends a misfitting shape to.
- `/alaa-services-contract` — exact platform contracts, and the *names* of metrics,
  events, error codes, queues, and headers.
- `/alaa-trust-gateway-auth` — trusted-header semantics, permission bitmap, gateway
  boundary.
- `/alaa-observability-soc` — the signal model, requirement levels, the
  definition-of-done gate for a shipped feature, SOC evidence, alert and runbook quality.
- `/alaa-reliability-sla` — retry shape, backoff policy, timeout budgets, degradation,
  and the ambiguous-timeout rule.
- `/alaa-testing-strategy` — test layer choice, test doubles, flake control, coverage
  policy.
- `/alaa-system-design` — capacity, topology, and consistency decisions above one service.
- `/alaa-project-constitution` — `references/quality-bar.md` is the platform
  quality bar. This skill restates no bar of its own; read that file when asked how good is good enough.
- `/alaa-async-messaging` — broker architecture beyond `mqkit`'s surface.
- `/alaa-security-review` — mandatory when authn, authz, tenant isolation, or a trust
  boundary changes.
- Model choice, reasoning effort, and runtime capability (whether subagents, plan mode, or background jobs
  exist) are owned by `/alaa-prompting-guide` `references/50-effort-and-thinking.md`.
  This skill names no model and assumes no runtime feature.
