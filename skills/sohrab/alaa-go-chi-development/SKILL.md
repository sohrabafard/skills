---
name: alaa-go-chi-development
description: "Governance contract for the shared alaa-go-chi Go kit (git.alaatv.com/vk/alaa-go-chi) and the services built on it: how an agent works inside the kit repository, and how an agent works in a consumer service. Use for kit-owner intake, change, release and propagation; consumer bootstrap, diagnosis, upgrade and migration; kit capability lookup; change requests and baseline proposals; registry rows; and audits. Phase-aware by mechanism, not by pinned state: it reads the kit repository's owner-ratified execution-scope decision at session start and enforces whatever that decision says, granting nothing and stopping when the phase is unrecognised. Do not use it when go.mod does not require alaa-go-chi; route Go craft and the P1-P13 bar to /alaa-golang ($alaa-golang) and /alaa-golang-clean-code-principles ($alaa-golang-clean-code-principles), and model or effort questions to /alaa-prompting-guide ($alaa-prompting-guide)."
---

# alaa-go-chi Development — Kit and Consumer Governance

The kit writes shared things once; a service repository contains only its domain. This skill is the operating
contract for both sides of that line: working **inside the kit repository**, and working **in a consumer service
built on the kit**. Repository truth outranks this skill: where they disagree, follow the repository, name the
file you followed, and log the disagreement as drift.

Cross-skill names appear as `/name` (`$name`): `/name` triggers in Claude Code, `$name` in Codex.

**Do not use this skill** when the target `go.mod` does not require `git.alaatv.com/vk/alaa-go-chi`, or when the
task changes no kit surface, generated artifact, contract document, or registry row: write the domain code and
route craft questions through "What this skill does not own".

## Start here — every session, before planning or editing

1. **Read the active phase from the kit repository.** Run `scripts/phase-check.sh <kit-repo-root>` and act on the
   exit code it documents; if you cannot run it, do the same three-location read by hand per
   [05-phase-and-source-truth](references/05-phase-and-source-truth.md). The phase decides which consumer-facing
   capabilities you hold. This skill never sets it and never infers it.
2. For any Go planning, code, review, or validation — kit and consumer alike — load `/alaa-golang`
   (`$alaa-golang`) and `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`), and cite
   P-numbers in every finding.
3. Open the one reference whose condition below is true of your task.

## Router — match the condition you can observe

| If this is true right now | Open |
|---|---|
| You are about to name a kit package, CLI flag, env key, default, metric, or Make target | [12](references/12-kit-capability-map.md) capability map |
| The repo you will write to requires the kit and lacks the behaviour asked for | [10](references/10-consumer-development.md) consumer development |
| That repo has the behaviour and it fails, drifts from its generated output, or must move to a newer pin | [15](references/15-debug-upgrade-migrate.md) debug/upgrade/migrate |
| You concluded a kit surface must change, or that code you were about to write belongs in the kit | [20](references/20-change-request-workflow.md) change requests |
| The repo you will write to **is** `alaa-go-chi` | [30](references/30-kit-owner-workflow.md) kit-owner workflow |
| You were asked to find defects and no fix is authorized yet | [40](references/40-platform-audit.md) platform audit |
| A service has no row in the kit's `docs/CONSUMERS.md`, or its row contradicts that service's `go.mod` | [50](references/50-consumer-registry.md) consumer registry |

**When two rows are true at once**, open the one for the repository you will actually write to and act on it; open
a second only if its condition still holds afterwards. Consumer work that uncovers a kit defect hops to `20-` and
stops there: filing the request is the whole hop, never a continuation into `30-`.

## Governing laws

1. **A consumer never changes the kit** — no edits, forks, or quiet re-implementation. Its own
   `docs/CONSUMERS.md` row is the only kit-repo file it may edit (`50-`); every kit need becomes one timestamped
   file (`20-`); the only sanctioned interim code form is a marked `KIT-WRAP` (`10-`).
2. **Baseline-first for shared logic.** Transport, contracts, trust, lifecycle, operational mechanics,
   generators, and cross-service invariants are kit-owned; domain policy stays in the service; the test that
   decides a specific case is in `10-`.
3. **Every consumer keeps a true row** in `docs/CONSUMERS.md` (`50-`); an unregistered service gets no impact
   analysis and is broken silently.
4. **Contract surfaces move as one change** — the artifacts that must land together are listed in `30-`. Error
   codes are append-only; metric names and env keys are kit-owned.
5. **Generated files change only through their generators**, run at the version the consumer pins; goldens are
   regenerated, never hand-edited. Two generated seams have owners outside the kit (`12-`).
6. **Read the decision records named in `12-` before designing kit-owned behaviour**, newest first. Ratified is not
   implemented: confirm against source before stating that a key, flag, or capability exists.
7. **Evidence honesty.** One outcome vocabulary and one proof ladder, defined once in `05-`. Never report a proof
   above the level that actually ran.

## When NOT to use

- `go.mod` does not require `git.alaatv.com/vk/alaa-go-chi` and no task proposes adopting it. There is no
  kit relationship to govern.
- The question is Go craft — naming, error shape, package layout, the P1-P13 bar — rather than who owns a
  change and how it reaches consumers.
- The question is which model or effort level to run at.
- The routing table below names the owner for each of these.

## What this skill does not own

Route these; adopt the owner skill vocabulary.

- Go code, layering, the P1–P13 bar — `/alaa-golang` (`$alaa-golang`), `/alaa-golang-clean-code-principles`
  (`$alaa-golang-clean-code-principles`).
- What a service of this kind must guarantee, and the repository quality bar — `/alaa-project-constitution`
  (`$alaa-project-constitution`).
- Fleet envelopes, readiness bodies, header names, deadlines, code and metric registries —
  `/alaa-services-contract` (`$alaa-services-contract`).
- Retries, timeouts, breakers, shedding, degradation, error budgets, SLOs — `/alaa-reliability-sla`
  (`$alaa-reliability-sla`). Test design, honest doubles, the six proof levels — `/alaa-testing-strategy`
  (`$alaa-testing-strategy`).
- Boundary design before code — `/alaa-system-design` (`$alaa-system-design`). Complexity bounds and structure
  choice — `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`).
- Security verdicts — `/alaa-security-review` (`$alaa-security-review`). The ControlledOps Composer package —
  `/alaa-controlled-ops` (`$alaa-controlled-ops`). A prompt for another agent — `/alaa-prompting-guide`
  (`$alaa-prompting-guide`).

Every other domain is routed beside the kit package it belongs to, in `12-`.

## Before reporting any task done

State in the reply: the phase and the record you read it from; which laws above your work touched and how each
was satisfied; every gate you ran with an outcome word from `05-`, and every gate you did not run as `not run`
with its blocker. No claim is stated above the proof level that actually ran.
