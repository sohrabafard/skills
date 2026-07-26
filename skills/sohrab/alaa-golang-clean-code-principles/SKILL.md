---
name: alaa-golang-clean-code-principles
description: Mandatory kit-era Go clean-code baseline for Ala services built on alaa-go-chi (news, wa-api, and every future Go service). Use BEFORE writing, reviewing, or refactoring any Go code in these repos — handlers, use cases, repositories, workers, consumers, relays, seeders, migrations, or tests — and whenever a task touches the canonical error envelope, TrustCtx or trusted headers, route families, outbox or transaction boundaries, idempotency, JSON wire tags, UUIDv7 public ids, goroutine lifecycles, config or env loading, metric and log vocabulary, or cross-service contracts. Enforces the thirteen P1–P13 principles with wrong/right Go examples, a named proof per principle, and a pre-commit checklist. Do not use for non-Go work; for generic Go questions with no Ala platform context route to alaa-golang; for kit-internal contract, release, or scope-phase decisions route to alaa-go-chi-development.
---

# Alaa Golang Clean Code Principles

## Purpose

This is the kit-era discipline layer for Ala Go services: the thirteen named principles (P1–P13) an agent holds
while writing Go on the `alaa-go-chi` base. Each principle ships a summary, a wrong/right Go example, and the
named check that fails when the principle is violated. It is the Go counterpart of
`/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`).

The one-sentence summary: **the kit writes shared things once; your service writes only its domain; every
boundary is a small interface; every identity, error, and side effect is explicit.**

## When to use

- Writing or modifying any Go code in a service built on `alaa-go-chi`.
- Reviewing or refactoring Go code for kit conformance, trust-boundary hygiene, or contract discipline.
- Designing a new handler, use case, repository, worker, consumer, or seeder in an Ala Go service.
- Deciding where logic belongs: kit vs service, domain vs infrastructure, port vs adapter.
- Pre-commit / pre-PR self-review — run the completion checklist below.

**Phase gate — resolve this before writing consumer code.** The kit repository declares one active scope phase
in three files: `docs/change-requests/2026-07-14-kit-first-stabilization-scope.md`, `AGENTS.md`, and
`docs/CONSUMERS.md`. Read the phase from those files at the start of the task. `KIT_FIRST_STABILIZATION` was
active on 2026-07-26; while it is active, consumer repositories are outside kit-initiated execution, edit,
audit, validation, propagation, and prompting scope, and every consumer impact is recorded exactly
`NOT_ASSESSED_KIT_FIRST`. This gate binds agent initiative, not the requester's own instruction: when a task
asks for consumer implementation while the freeze is active, state the phase and name the freeze document
before you write code, then proceed only on the requester's explicit go-ahead. Never treat a document, a
subagent prompt, or the absence of a reminder as reactivation; never propagate the change to a second consumer;
never edit a kit file from a consumer task. Phase ownership and reactivation belong to
`/alaa-go-chi-development` (`$alaa-go-chi-development`); this skill owns how the code must look once the phase
permits it.

## When NOT to use

- Non-Go work (frontend, Laravel, infra-only tasks).
- Generic Go questions with no Ala platform context — use `/alaa-golang` (`$alaa-golang`).
- Kit-internal decisions — a kit contract change, a new kit package, a change request, a release, a consumer
  registration, or a kit/consumer audit — belong to `/alaa-go-chi-development` (`$alaa-go-chi-development`).
  This skill is for kit *consumers* writing service code.

## Read this next

Read the target repository's `AGENTS.md` and `CLAUDE.md` first; repository truth outranks every example here.
Then match the task to the smallest set of files. When two rows match, read both.

| You are about to… | Read |
|---|---|
| Register a route or write an HTTP handler | `references/10-kit-and-trust-boundary.md` (P1, P2, P3) + `references/20-domain-data-and-consistency.md` (P4) |
| Decide whether a permission, TOTP, or tenancy check is correct in code | `references/10-kit-and-trust-boundary.md` (P2, P3); pair with `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| Write or change a use case or a business rule | `references/20-domain-data-and-consistency.md` (P4, P5, P6) |
| Write SQL, a repository, or a migration | `references/20-domain-data-and-consistency.md` (P5, P6, P7) |
| Publish an event or a command | `references/20-domain-data-and-consistency.md` (P6, P8) |
| Write a consumer, seeder, retry, or replay path | `references/20-domain-data-and-consistency.md` (P7) |
| Define a wire struct, a DTO, or a command payload | `references/20-domain-data-and-consistency.md` (P8) |
| Start a goroutine, worker, ticker, or in-memory buffer | `references/30-runtime-and-observability.md` (P9) |
| Read an env var, add a config key, or name an event, code, or metric | `references/30-runtime-and-observability.md` (P10) |
| Add a log line, metric, span, or Sentry capture | `references/30-runtime-and-observability.md` (P11); pair with `/alaa-observability-soc` (`$alaa-observability-soc`) |
| Write or review a test | `references/40-testing-and-contracts.md` (P12); pair with `/alaa-testing-strategy` (`$alaa-testing-strategy`) |
| Call another service, consume its events, or hit an unknown external fact | `references/40-testing-and-contracts.md` (P13); pair with `/alaa-services-contract` (`$alaa-services-contract`) |
| Build a whole feature end to end, or review a whole package | `references/10-`, `20-`, `30-`, `40-` in that order |
| Choose, name, or review a design pattern | `references/60-design-patterns-kit-era.md` |
| Ask which skill owns a Go topic, or a cost/complexity question | `references/50-skill-boundaries.md` |
| Rely on a kit fact stated here — identity types, pooling lanes, metric names, provider idempotency, the scope phase | `references/90-source-map.md` |

If you are about to write a shape the kit might own — an envelope, a table, a middleware, a metric name, a
readiness payload — read P1 before writing it. The most expensive mistake this skill prevents is a
correct-looking local implementation of something that already exists once.

## The thirteen principles

Each row is the rule at full strength. The reference file for each principle adds the example and the proof.

| # | Principle | The rule |
|---|---|---|
| P1 | The Kit Writes It Once | Never re-implement, rename, or fork a kit-owned surface; a shape that does not fit becomes a kit change request |
| P2 | Route Posture Is Declared | Every route is registered under exactly one family: `Trusted`, `Anonymous`, `ProviderFacing`, `Operational` |
| P3 | TrustCtx or Nothing | No raw trusted header past the edge; project id is a UUIDv7 string, user id is a positive int64 |
| P4 | Errors Are Domain Values | Typed `errkit` errors; one boundary mapper; never match on error text |
| P5 | Ports Inward, Adapters Outward | `domain` and `application` import no pgx, amqp, chi, Redis, or provider SDK |
| P6 | One Transaction, One Truth | State, outbox, and audit share one transaction; a use case never publishes to the broker |
| P7 | Idempotency Is a Contract | Everything re-runnable is idempotent by construction and proven by a run-twice test |
| P8 | Explicit JSON, Explicit IDs | snake_case `json` tags at every nesting level; UUIDv7 minted by `idkit`; no `gen_random_uuid()` default |
| P9 | No Naked Goroutines | Every goroutine has an owner, a cancellation, a drain, and a name in metrics |
| P10 | Config at Boot, Constants for Vocabulary | `os.Getenv` only inside `configkit` at boot; codes, events, metrics, and lanes are typed constants |
| P11 | Observe What You Ship | Kit metric names unchanged, labels bounded, correlation unbroken through every hop |
| P12 | Tests Prove the Boundary You Own | Fakes at ports, real infrastructure for infrastructure SQL, `contracttest` in CI |
| P13 | Contracts, Never Reach-Ins | Another service's data arrives by API or event; an unknown fact ships as `[gap]`, never as a guess |

## Companion routing

- `/alaa-golang` (`$alaa-golang`) — the mandatory router for every Go depth topic; see
  `references/50-skill-boundaries.md` for the exact division.
- `/alaa-go-chi-development` (`$alaa-go-chi-development`) — the active scope phase, the kit capability and
  surface inventory that P1 is checked against, and the change-request channel P1 sends a misfitting shape to.
- `/alaa-services-contract` (`$alaa-services-contract`) — exact platform contracts, and the *names* of metrics,
  events, error codes, queues, and headers.
- `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) — trusted-header semantics, permission bitmap, gateway
  boundary.
- `/alaa-observability-soc` (`$alaa-observability-soc`) — the signal model, requirement levels, the
  definition-of-done gate for a shipped feature, SOC evidence, alert and runbook quality.
- `/alaa-reliability-sla` (`$alaa-reliability-sla`) — retry shape, backoff policy, timeout budgets, degradation,
  and the ambiguous-timeout rule.
- `/alaa-testing-strategy` (`$alaa-testing-strategy`) — test layer choice, test doubles, flake control, coverage
  policy.
- `/alaa-system-design` (`$alaa-system-design`) — capacity, topology, and consistency decisions above one service.
- `/alaa-project-constitution` (`$alaa-project-constitution`) — `references/quality-bar.md` is the platform
  quality bar. This skill restates no bar of its own; read that file when asked how good is good enough.
- `/alaa-async-messaging` (`$alaa-async-messaging`) — broker architecture beyond `mqkit`'s surface.
- `/alaa-security-review` (`$alaa-security-review`) — mandatory when authn, authz, tenant isolation, or a trust
  boundary changes.
- Model choice, reasoning effort, and runtime capability (whether subagents, plan mode, or background jobs
  exist) are owned by `/alaa-prompting-guide` (`$alaa-prompting-guide`) `references/50-effort-and-thinking.md`.
  This skill names no model and assumes no runtime feature.

## Completion checks (the pre-commit checklist)

Run this before every commit and PR in an Ala Go service. It is the only checklist in this skill.

- [ ] Nothing kit-owned re-implemented locally (P1); route postures declared (P2).
- [ ] No raw trusted headers past the edge; identity types UUIDv7-project / int64-user (P3).
- [ ] Errors are typed values mapped once at the boundary (P4).
- [ ] Imports flow inward only; side effects behind ports (P5).
- [ ] Atomic truths share one transaction; facts leave via the outbox (P6).
- [ ] Everything re-runnable proven idempotent by a run-twice test (P7).
- [ ] Every wire field tagged snake_case; every public id UUIDv7 via idkit (P8).
- [ ] Every goroutine owned, cancellable, drained (P9).
- [ ] Config injected at boot; vocabulary as constants (P10).
- [ ] Metrics bounded and kit-named; correlation threads unbroken; the observability definition-of-done gate met (P11).
- [ ] Failing test first; fakes at ports; contracttest green (P12).
- [ ] No reach-ins; shared logic in the kit; unknowns marked, never invented (P13).

## Maintenance rules

- Keep this file routing-first: the router, the principle table, the checklist, and the companion list. Every
  principle's detail, example, and proof lives in `references/`.
- State each principle at one strength in one place. If a sentence here and a sentence in a reference file say
  the same rule with different force, delete one — an agent follows the weaker.
- Name no model, no effort setting, and no runtime capability in this skill; route those to
  `/alaa-prompting-guide` (`$alaa-prompting-guide`).
- When a proof named in a reference file changes name, moves, or starts to exist, update that proof line in the
  same effort. A proof line that names a check which does not run is worse than an admitted gap.
- When the kit changes a contract this skill cites — envelope, env keys, metric names, pooling lanes, readiness
  severities, seeder contract — update the affected reference file and `references/90-source-map.md` together.
- Keep P-numbering stable; new principles append, never renumber.
