# Skill Boundaries — What Lives in `alaa-golang` (Referenced, Not Repeated)

This skill deliberately adds **nothing** on the topics below. When a task needs them, load the `alaa-golang`
router (Codex: `$alaa-golang` · Claude Code: `/alaa-golang` or `/alaa-golang`) and let it route to
the specific public Go skill. Duplicating that material here would create exactly the drift this pack forbids.

| Topic | Owned by (via the alaa-golang router) |
|---|---|
| Naming conventions | `golang-naming` |
| Line-level style and clarity | `golang-code-style` |
| Project layout / monorepos | `golang-project-layout` |
| Struct/interface design, embedding, receivers | `golang-structs-interfaces` |
| Design-pattern catalog (functional options, constructors, graceful shutdown, resilience) | `golang-design-patterns` — this pack's `60-design-patterns-kit-era.md` only maps pattern intent to kit surfaces; mechanics stay there |
| DI stance — manual first; wire/dig/fx/do when present | `golang-dependency-injection` + specific skills |
| Concurrency, channels, errgroup | `golang-concurrency` |
| `context` propagation | `golang-context` |
| Nil-safety, aliasing, defensive copies | `golang-safety` |
| Error mechanics (wrapping, Is/As, sentinels) | `golang-error-handling` |
| Database access patterns | `golang-database` |
| Testing, testify, benchmarks | `golang-testing`, `golang-stretchr-testify`, `golang-benchmark` |
| Performance, profiling, troubleshooting | `golang-performance`, `golang-troubleshooting` |
| Security | `golang-security` |
| Lint configuration | `golang-lint` |
| Modern idioms / upgrades / latest-Go (1.26) features | `golang-modernize` + `alaa-golang` reference 70 |
| Semantic code navigation and diagnostics | `golang-gopls` (via the alaa-golang router) |
| Safe, staged, at-scale refactoring process | `golang-refactoring` (via the alaa-golang router) |
| Published-package lookup (versions, CVEs, symbols) | `golang-pkg-go-dev` (via the alaa-golang router) |
| chi-vs-Fiber policy, Ala Go baseline, repository pattern, Redis cache rules, TDD discipline | `alaa-golang` references 30/31/60/61/62/63 |

Division of labor in one sentence: **`alaa-golang` teaches you to write good Go; this skill teaches you to
write Go that belongs on this platform.** When guidance appears to conflict, platform contracts win —
`alaa-services-contract` for exact shapes, this skill for kit-era discipline — and a real conflict is a drift
to record, not to resolve silently.

One boundary that is not a Go one: the complexity budget a growing path is held to, the real bound on an input
dimension, structure choice from the access pattern, and the N+1 family across database, HTTP, cache, and permission
calls belong to `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`). Read it when deciding what a
path is allowed to cost as its input grows; read `golang-data-structures` through the router when the question is how
a Go map or slice behaves.

Related non-Go companions this skill assumes exist (never re-derive their content): `alaa-services-contract`,
`alaa-trust-gateway-auth`, `alaa-observability-soc`, `alaa-async-messaging`, `alaa-security-review`,
`alaa-docker-production`, `alaa-gitlab-ci-cd`.
