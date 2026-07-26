# What This Skill Does Not Own

This skill routes Go work. It does not set doctrine, and it does not publish values. Every row below names an owner,
the observable condition that hands the topic to that owner, and both trigger forms — Claude Code `/name`, Codex
`$name`.

Two consequences follow, and they are absolute:

- **This skill originates no name and no number.** It writes no metric name, no error code, no event name, no retry
  count, no backoff curve, no timeout budget, no SLO window, and no coverage threshold. Where such a value is needed,
  load the owner and take the value from there. Where this skill shows a value the kit has already implemented — an
  environment key `httpkit` reads, its default, the range it clamps to — it cites the kit file the value was read from
  and the date it was read, and that is a report of implemented behaviour, not a decision. **Rule:** when a cited kit
  value and kit source disagree, the source wins and the citation is stale; re-read it and say so.
- **When this skill and an owner disagree, the owner wins.** Follow the owner, and report the disagreement as drift in
  your final message, naming both files. Do not edit either skill to make the conflict disappear.

## Doctrine owners

| Owner | Load it when you are about to… |
|---|---|
| `/alaa-project-constitution` (`$alaa-project-constitution`) | decide whether a change is finished, whether a service is production ready, or what quality bar applies to a repository |
| `/alaa-reliability-sla` (`$alaa-reliability-sla`) | choose a retry count, a backoff curve, a jitter policy, a timeout budget, a circuit-breaker threshold, a degradation mode, a load-shedding policy, or an SLO/error-budget window |
| `/alaa-testing-strategy` (`$alaa-testing-strategy`) | decide which kinds of test a change requires, where the boundary between unit, integration, contract and load testing sits, or what a test suite must cover before release |
| `/alaa-system-design` (`$alaa-system-design`) | split a system into services, choose a synchronous or asynchronous boundary, or place a responsibility in one service rather than another |
| `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) | state the complexity budget for a path whose input grows with tenants, rows, retained history, or fan-out per event; find the enforced upper bound on a growing dimension; choose a data structure from an access pattern; or resolve a database, HTTP, cache, or permission call that sits inside a loop. A path on which every dimension already has a small maximum enforced in code needs none of it. How a Go map or slice itself behaves is `/golang-data-structures` (`$golang-data-structures`) |
| `/alaa-services-contract` (`$alaa-services-contract`) | write or change any name or value on a service's external surface: metric names, environment keys, error codes, event names, response envelope fields, header names, status-code mappings, deadline and window values |
| `/alaa-observability-soc` (`$alaa-observability-soc`) | decide which signals a change must emit, what level of instrumentation is required, which dashboard or alert must exist before merge, or what evidence an incident needs |
| `/alaa-security-review` (`$alaa-security-review`) | change authentication, authorization, tenant isolation, secret handling, cryptography, or any code reachable by an untrusted caller |
| `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) | read a trusted-gateway header, construct or consume identity context, evaluate a permission bitmap, or decide what a service may believe about its caller |
| `/alaa-data-layer` (`$alaa-data-layer`) | change a schema, write a migration, choose a pooling lane, design a lock, or scope data access to a tenant |
| `/alaa-async-messaging` (`$alaa-async-messaging`) | design broker topology, an outbox relay, a consumer's acknowledgement point, a dead-letter path, or a replay procedure |
| `/alaa-keyset-pagination` (`$alaa-keyset-pagination`) | paginate a list endpoint or a query over a table that grows without a fixed maximum |
| `/alaa-permission-generator` (`$alaa-permission-generator`) | add, rename, or renumber a permission name or bitmap id, or regenerate the permission map |

## Platform owners

| Owner | Load it when you are about to… |
|---|---|
| `/alaa-go-chi-development` (`$alaa-go-chi-development`) | check the active scope phase; change anything inside the kit; file a kit change request or baseline proposal; register a consumer; or discover that the capability your service needs is a kit-owned surface the kit does not yet have |
| `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) | write, review, or refactor Go in a repository whose `go.mod` requires `git.alaatv.com/vk/alaa-go-chi` — its P1–P13 are the conformance bar |
| `/alaa-golang-fiber` (`$alaa-golang-fiber`) | edit a repository whose `go.mod` requires `github.com/gofiber/fiber/v2` or `/v3`, or build a Fiber prototype the user has explicitly scoped |
| `/alaa-prompting-guide` (`$alaa-prompting-guide`) | choose a model, a reasoning effort, or a thinking budget; decide whether a subagent, plan mode, or background execution is available; or write a prompt for another agent. Its `references/50-effort-and-thinking.md` owns effort and thinking. This skill names no model and no effort level anywhere |

## Go mechanics owners

The vendor `golang-*` skills own Go technique. This skill selects among them and never restates them. The roster, its
audited size, and the condition that selects each skill live in `10-installed-golang-skills.md`; the boundaries
between skills that look alike live in `11-orchestration-and-overlap-guide.md`.

## What belongs here: the gap test

This skill's other half. Everything above says a topic belongs to someone else; this says a topic belongs here
precisely because it belongs to no one else. Filling that gap is one of this skill's three jobs, equal in weight to
routing — see `SKILL.md`.

A rule belongs in `alaa-golang` when **all three** of the following hold. Check them in this order and stop at the
first one that fails.

1. **No vendor `golang-*` skill states it.** `10-installed-golang-skills.md` is the inventory to check against; check
   it before deciding, rather than assuming from the skill's name.
2. **No doctrine owner, platform owner, or companion listed in this file owns it.**
3. **It is a Go-language, Go-toolchain, or Ala-Go-platform decision** — not a language-neutral one.

The outcome is determined, not discretionary:

| Result | What you do |
|---|---|
| All three hold | The rule lives here. State it once, in exactly one reference file. |
| Check 1 fails | Route to that vendor skill and state nothing yourself. |
| Check 2 fails | Route to that owner and state nothing yourself. |
| Check 3 fails | It is not this skill's ground at all. Route it if it has an owner; otherwise leave it and say so. |

**Rule:** when a Go task needs a decision that all three checks show is covered by nothing, make the decision, and
name it in your final report — which decision you had to make, why no source covered it, and where you recorded it.
The report is the minimum; a durable record belongs in the reference file that now states the rule, or in a note
through `/alaa-basic-memory-os` (`$alaa-basic-memory-os`) when the decision outlives the task.

**Forbidden:** deciding a gap silently. An undeclared gap decision is invisible to the maintainer, so the next agent
meets the same gap and decides it differently — which is how one platform grows two answers to one question.

## Maintaining this skill's own files

**Rule:** every reference in this skill exists for exactly one of two reasons — it routes, or it fills a gap the test
above proved. Both are first-class. A file is not removable for "not routing".

**Rule:** remove a gap file only when a vendor `golang-*` skill or an owner named in this file has since taken that
ground, and name in the removal which skill took it and which file now states the rule.

**Forbidden:** removing a reference because it reads as policy rather than as routing. Being policy no one else holds
is the reason a gap file exists.

## What this skill does own

The current result of the gap test above. Everything below is stated here and nowhere else in the pack, which is why
this skill is the front door:

- Which Go skill to load for an observed situation (`00-topic-map.md`, `10-`, `11-`, `20-`).
- The HTTP framework decision for an Ala Go service, and the record of why it is settled (`30-`).
- The Go mechanics of writing a chi service on the kit: routing, decoding, validation, error mapping, testing (`31-`).
- The Go mechanics of failure at the call site: deadline propagation, per-attempt clamping, server bounds, decode
  limits, cancellation cause, drain (`45-`).
- What the kit gives a chi service under load, what it does not, and where each absence must be taken (`46-`).
- The service layout and the repository boundary (`60-`).
- Redis cache mechanics against the kit's Redis client behaviour (`61-`).
- Import direction between packages (`62-`).
- The test-first sequence for a behaviour change (`63-`).
- Which language and standard-library features a repository may use, given its `go` directive (`70-`).
- Which package to reach for in this stack (`40-`).
