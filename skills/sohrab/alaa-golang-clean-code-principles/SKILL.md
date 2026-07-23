---
name: alaa-golang-clean-code-principles
description: Mandatory kit-era Go clean-code baseline for Ala services built on alaa-go-chi (news, notification v2, entitlement-platform after adoption, and every future Go service). Use BEFORE writing, reviewing, or refactoring any Go code in these repos — handlers, use cases, repositories, workers, consumers, relays, seeders, migrations, or tests — and whenever a task touches the canonical error envelope, TrustCtx or trusted headers, route families, outbox or transaction boundaries, idempotency, JSON wire tags, UUIDv7 public ids, goroutine lifecycles, config or env loading, metric and log vocabulary, or cross-service contracts. Enforces the thirteen P1–P13 principles with wrong/right Go examples and a pre-commit checklist. Do not use for non-Go work, or for generic Go questions with no Ala platform context — route those through alaa-golang.
---

# Alaa Golang Clean Code Principles

## Purpose

This is the kit-era discipline layer for Ala Go services: the thirteen named principles (P1–P13) an agent must
hold while writing Go on the `alaa-go-chi` base, each with a summary and a wrong/right example. It is the Go
counterpart of `alaa-vue-typescript-clean-code`.

It is deliberately **non-duplicative**: deep Go mechanics (naming, style, concurrency internals, error mechanics,
testing depth, patterns catalog) live in the `alaa-golang` skill tree and are referenced, never repeated here
(`references/50-skill-boundaries.md`). This skill owns only what that tree does not: how code must behave now
that the kit owns the platform's shared surfaces.

The one-sentence summary of everything here: **the kit writes shared things once; your service writes only its
domain; every boundary is a small interface; every identity, error, and side effect is explicit.**

## When to use

- Writing or modifying any Go code in a service built on `alaa-go-chi`.
- Reviewing or refactoring Go code for kit conformance, trust-boundary hygiene, or contract discipline.
- Designing a new handler, use case, repository, worker, consumer, or seeder in an Ala Go service.
- Deciding where logic belongs: kit vs service, domain vs infrastructure, port vs adapter.
- Pre-commit / pre-PR self-review (run the completion checklist below).

## When NOT to use

- Non-Go work (frontend, Laravel, infra-only tasks).
- Generic Go questions with no Ala platform context — use the `alaa-golang` router skill.
- Kit-internal development decisions (contract changes, new kit packages) — those are governed by
  `alaa-go-chi-framework.md` (`docs/idea/`) and its `CONTRACTS.md`; this skill is for kit *consumers*.

## Quick start

1. Read the repo-local `AGENTS.md` / `CLAUDE.md` first; repo truth wins over any example here.
2. Read `references/00-topic-map.md` and open only the principle group the task touches:
   - `references/10-kit-and-trust-boundary.md` — P1 kit-first, P2 route posture, P3 TrustCtx.
   - `references/20-domain-data-and-consistency.md` — P4 errors, P5 ports/adapters, P6 transactions+outbox,
     P7 idempotency, P8 explicit JSON/ids.
   - `references/30-runtime-and-observability.md` — P9 goroutine ownership, P10 config/constants,
     P11 observability discipline.
   - `references/40-testing-and-contracts.md` — P12 tests at boundaries, P13 cross-service contracts,
     plus the pre-commit checklist.
3. Read `references/full-guide.md` when the task is broad (new feature end to end, review of a whole package).
4. For any topic listed in `references/50-skill-boundaries.md`, load the referenced skill instead of improvising.

## The thirteen principles (index)

| # | Principle | One line |
|---|---|---|
| P1 | The Kit Writes It Once | never re-implement a kit-owned surface; wrap→kit PR, never fork |
| P2 | Route Posture Is Declared | every route names its family: Trusted / Anonymous / ProviderFacing / Operational |
| P3 | TrustCtx or Nothing | no raw trusted headers past the edge; UUIDv7 project, int64 user |
| P4 | Errors Are Domain Values | typed errkit errors; one boundary mapper; never string-match |
| P5 | Ports Inward, Adapters Outward | domain/application import no pgx/amqp/chi/Redis/SDKs |
| P6 | One Transaction, One Truth | state + outbox + audit in one tx; facts leave via the relay |
| P7 | Idempotency Is a Contract | everything re-runnable proven by a run-twice test |
| P8 | Explicit JSON, Explicit IDs | snake_case tags on every level; UUIDv7 via idkit only |
| P9 | No Naked Goroutines | every goroutine owned, cancellable, drained on shutdown |
| P10 | Config at Boot, Constants for Vocabulary | os.Getenv only in configkit; codes/events/metrics as constants |
| P11 | Observe What You Ship | kit metric names, bounded labels, unbroken correlation, DoD includes dashboards |
| P12 | Tests Prove the Boundary You Own | fakes at ports, testcontainers for infra, contracttest in CI |
| P13 | Contracts, Never Reach-Ins | APIs/events over tables; shared logic in the kit; unknowns marked, never invented |

## Model and runtime notes

This skill is written to run identically under **Claude Fable 5, Claude Opus 4.8, Claude Sonnet 5 (Claude Code)**
and **GPT-5.5 (Codex)**:

- All instructions are imperative, self-contained markdown; nothing depends on a runtime-specific tool.
- Skill triggers differ by runtime: in Codex prompts reference companions as `$alaa-golang`,
  `$alaa-services-contract`; in Claude Code as `/alaa-golang` (or the pack-qualified `/alaa-golang`).
  When this skill's references name a companion skill, use the trigger character of the runtime you are in —
  see the `alaa-prompting-guide` skill's trigger-syntax reference when writing prompts for another model.
- Do not assume subagents, background jobs, or plan modes exist; when they do, this skill needs none of them.

## Hard rules (the non-negotiables agents most often break)

- Never hand-roll an error response, middleware chain, readiness envelope, outbox table, or seeder mechanism —
  the kit owns them (P1).
- Never read `r.Header` or `os.Getenv` outside their single sanctioned locations (P3, P10).
- Never publish to the broker from a use case — outbox only (P6).
- Never ship a wire struct with an untagged nested field (P8) or a `gen_random_uuid()` default (P8).
- Never fire `go func()` without an owner, cancellation, and drain (P9).
- Never guess an external fact — mark it `NEEDS_<PROVIDER>_CONFIRMATION` / `[gap]` (P13).

## Companion routing

- `alaa-golang` — mandatory router for all Go depth topics (see `references/50-skill-boundaries.md`).
- `alaa-services-contract` — exact platform contracts (envelopes, headers, readiness, notification ingress).
- `alaa-trust-gateway-auth` — trusted-header semantics, permission bitmap, gateway boundary.
- `alaa-observability-soc` — signal model, SOC evidence, alert/runbook quality.
- `alaa-async-messaging` — broker architecture reasoning beyond the kit's mqkit surface.
- `alaa-security-review` — mandatory when authn/authz, tenant isolation, or trust boundaries change.

## Reference navigation

- `references/00-topic-map.md` — shortest reading path per task type.
- `references/10-kit-and-trust-boundary.md` — P1–P3 with examples.
- `references/20-domain-data-and-consistency.md` — P4–P8 with examples.
- `references/30-runtime-and-observability.md` — P9–P11 with examples.
- `references/40-testing-and-contracts.md` — P12–P13 + the pre-commit checklist.
- `references/50-skill-boundaries.md` — exactly what lives in `alaa-golang` and is not repeated here.
- `references/60-design-patterns-kit-era.md` — decision map: what each classic (GoF) design pattern becomes
  on this platform (Singleton→composition root, Observer→outbox, Template Method→kit skeletons, …). Opens
  with a symptom → pattern recognition table and look-alike disambiguation — run it before choosing any
  pattern; mechanics stay in `golang-design-patterns` via the router.
- `references/full-guide.md` — all thirteen principles in one file.
- `references/90-source-map.md` — canonical sources and freshness triggers.

## Completion checks (the pre-commit checklist)

- Nothing kit-owned re-implemented locally (P1); route postures declared (P2).
- No raw trusted headers past the edge; identity types UUIDv7-project / int64-user (P3).
- Errors are typed values mapped once at the boundary (P4).
- Imports flow inward only; side effects behind ports (P5).
- Atomic truths share one transaction; facts leave via the outbox (P6).
- Everything re-runnable proven idempotent by a run-twice test (P7).
- Every wire field tagged snake_case; every public id UUIDv7 via idkit (P8).
- Every goroutine owned, cancellable, drained (P9).
- Config injected at boot; vocabulary as constants (P10).
- Metrics bounded and kit-named; correlation unbroken; dashboards/alerts/runbook exist (P11).
- Failing test first; fakes at ports; contracttest green (P12).
- No reach-ins; shared logic in the kit; unknowns marked, never invented (P13).

## Maintenance rules

- Keep this file routing-first; principle detail lives in `references/`.
- When the kit (`alaa-go-chi-framework.md`) changes a contract this skill cites (envelope, env keys, metric
  names, pooling lanes), update the affected reference file and `full-guide.md` in the same effort.
- Keep P-numbering stable; new principles append, never renumber.
- Keep examples aligned with the current identity contract (UUIDv7 project / int64 user) and the two-lane
  pooling contract; these are the two facts most likely to rot.
