---
name: alaa-go-chi-development
description: Governance and workflow contract for the alaa-go-chi Go kit and every service built on it (news, notification v2, entitlement-api and tusd after migration, and all future Ala Go services). Use this skill whenever a task involves building or migrating a consumer service on alaa-go-chi, requesting a change or reporting a bug in a kit-owned surface, proposing a new shared/baseline feature, registering a consumer in the kit's CONSUMERS.md, processing an incoming kit-change-request as the kit owner, propagating a kit change to consumers, or auditing the kit and its consumers for bugs, drift, and duplicated logic that should be abstracted into the kit. Also use it when writing handoff prompts for consumer-service agents. It does not replace alaa-golang or alaa-golang-clean-code-principles for actual Go coding — it routes to them and adds the kit↔consumer governance layer on top.
---

# alaa-go-chi Development — Kit ↔ Consumer Governance

## Purpose

`alaa-go-chi` (repo: `alaa-go-chi`, module `git.alaatv.com/vk/alaa-go-chi`) is the shared base for every Ala Go
macro-service. Its whole reason to exist is captured in one sentence from the framework document: **the kit writes
shared things once; a service repository contains only its domain.** The moment a consumer re-implements a kit
surface, patches the kit privately, or grows a second copy of logic another consumer also has, the platform is
back to the drift the kit was built to kill.

This skill is the operating contract that keeps that from happening. It governs three roles that different agents
(or the same agent at different times) will play:

- **Consumer developer** — building `news`, `notif`, or any new service on the kit; migrating `entitlement-api`
  and `tusd` onto it.
- **Kit owner** — receiving change-request documents, evolving the kit safely, and propagating changes.
- **Platform auditor** — periodically inspecting the kit plus all registered consumers for bugs, contract drift,
  and duplicated logic that deserves promotion into the kit.

Identify your role first (§ "Which mode am I in?"), then read only the reference file for that mode.

## The three laws (apply in every mode)

These come directly from the platform owner and from `GOVERNANCE.md` in the kit repo. They are not style
preferences; violating any of them recreates the fork problem.

1. **Consumers never change the kit.** If a consumer needs an upgrade, finds a bug, or hits a limitation in any
   kit-hosted surface (any package or contract listed in framework §3/§7 — envelopes, middleware, trustkit,
   pgkit, mqkit, outboxkit, jobkit, seedkit, readykit, obskit, configkit, errkit, httpkit, audiencekit, idkit,
   runkit, contracttest, the scaffold, CI templates, deploy templates), it does **not** edit kit code, does not
   fork, and does not quietly re-implement. It writes one **timestamped change-request document per feature or
   bug** (`YYYY-MM-DD-<slug>.md`) that fully explains the need, the evidence, and the impact. The human owner
   carries that document to the kit-owner agent, who verifies it against all consumers before changing anything.
   Format and workflow: `references/20-change-request-workflow.md`.

2. **Baseline-first for shareable logic.** Any feature or logic that could plausibly serve more than one
   consumer (a new middleware, a cache shape, a retry policy, a provider-agnostic helper, a lint, a deploy
   pattern) is not implemented service-locally first. The consumer writes a timestamped **baseline proposal**
   document, the kit adopts it (possibly amended), and only then does the consumer use it — from the kit.
   The only sanctioned interim form is a thin local **wrap** (never a fork), which per `GOVERNANCE.md` may live
   at most two releases before it must become a kit feature request or recorded drift.

3. **Every consumer registers itself.** An agent that starts building or migrating a service on the kit adds
   that service to `docs/CONSUMERS.md` **in the alaa-go-chi repository** as part of its first work session, and
   keeps its row current (kit version pinned, status, repo path, contracttest status). This registry is the
   input the kit owner and the auditor iterate over — an unregistered consumer is invisible to impact analysis
   and will be broken silently by kit changes. Registry format: `references/50-consumer-registry.md`.

## Which mode am I in?

| You are asked to… | Mode | Read |
|---|---|---|
| Implement, extend, or migrate a service that uses the kit (news, notif, entitlement-api, tusd, new service) | **Consumer development** | `references/10-consumer-development.md` |
| Report a kit bug, request a kit upgrade, or propose a new shared feature | **Change request / baseline proposal** | `references/20-change-request-workflow.md` |
| Act as the kit's responsible agent: review an incoming request doc, change the kit, release, propagate | **Kit ownership** | `references/30-kit-owner-workflow.md` |
| Inspect/monitor/audit the kit and consumers; find bugs, drift, duplication; decide what gets abstracted | **Platform audit** | `references/40-platform-audit.md` |
| Register a service or read/update the consumer roster | **Registry** | `references/50-consumer-registry.md` |

A single task often crosses modes — e.g., consumer work discovers a kit bug (mode C → file a change request),
or an audit finds duplication (mode A → write a baseline proposal → kit ownership implements → propagate).
Follow each mode's reference at the point you enter it.

## Source-of-truth order

For any factual question, trust in this order — and verify before acting:

1. **Kit repo executable truth** — kit code, `contracttest`, generated scaffold output, CI templates.
2. **`CONTRACTS.md`** (kit repo) — every enforced shape, metric name, env key, and its change history.
3. **`GOVERNANCE.md`** (kit repo) — change rules, semver classification, merge gates, deprecation shape.
4. **`alaa-go-chi-framework.md`** (kit repo root) — the ratified design; all §12 decisions are closed.
5. Consumer architecture docs — `docs/news-service-go-architecture.md`, `docs/notif-service-go-architecture.md`,
   `docs/2026-07-05-entitlement-platform-kit-adoption.md` (all in the kit repo's `docs/`).
6. This skill and its references.

If two of these disagree, that is **drift**: do not silently pick a side — record it (drift note per
`alaa-basic-memory-os` rules when Basic Memory is available, otherwise a timestamped doc) and continue on the
safest verified behavior.

## Known consumers and repo map (as of 2026-07-08 — verify against `docs/CONSUMERS.md`)

| Service | Status | Where |
|---|---|---|
| `news` | designed (Rev 4), to be built on the kit scaffold | repo created from `alaa-go-chi new service news` |
| `notif` (notification v2) | designed (Rev 6), to be built on the kit scaffold | repo created from `alaa-go-chi new service notif` |
| `entitlement-api` | existing service; migrate after news+notif complete | `entitlement-platform/services/entitlement-api` |
| `tusd` | existing service; migrate after news+notif complete | `tusd` repo |

The live registry in the kit repo (`docs/CONSUMERS.md`) always outranks this table.

## Mandatory skill routing

This skill owns governance only. Route the actual engineering to the domain skills — in Claude Code with `/name`
(pack-qualified `/sohrab-skills:<name>` if needed), in Codex with `$name`.

| When the task involves | Load |
|---|---|
| **Any Go code at all** (writing, reviewing, planning, refactoring) | `/alaa-golang` (router) **and** `/alaa-golang-clean-code-principles` (P1–P13 baseline) — both are mandatory, not optional, for kit and consumer code alike |
| Envelopes, health/readiness, gateway prefixes, cross-service runtime conventions | `/alaa-services-contract` |
| Trusted headers, TrustCtx, permission bitmaps, TOTP, tenant isolation | `/alaa-trust-gateway-auth`, `/alaa-security-review` |
| Postgres, migrations, pooling lanes, Redis | `/alaa-data-layer` |
| RabbitMQ, outbox, consumers, DLQ, idempotency | `/alaa-async-messaging` |
| Logs/metrics/traces/Sentry/SigNoz | `/alaa-observability-soc` |
| Docker/Compose/Swarm images and runtime | `/alaa-docker-production`; Kubernetes/Helm/Arvan → `/alaa-k8s-helm`, `/caas-arvan-kuber` |
| GitLab CI pipelines | `/alaa-gitlab-ci-cd` |
| Writing prompts for another agent (consumer-update prompts, handoffs) | `/alaa-prompting-guide` — mandatory before authoring any cross-agent prompt |
| Long multi-phase or resumable work; noisy investigation | `/alaa-workflow`, `/alaa-low-noise` |
| Docs packs (README, BIG_PICTURE, RUNBOOK, api-summary) | `/alaa-docs-farsi` |

Division of labor with the two Go skills, stated once so nobody duplicates content:
`/alaa-golang` owns *how to write Go*; `/alaa-golang-clean-code-principles` owns *how consumer code must behave
on the kit* (P1–P13); **this skill owns *how the kit and its consumers change over time*** — who may change
what, through which documents, and how changes propagate.

## Non-negotiables checklist (self-check before finishing any task in any mode)

- [ ] I did not edit kit code from a consumer context (only `docs/CONSUMERS.md` registration is allowed).
- [ ] Every kit need I hit became one timestamped change-request or baseline-proposal file, one file per topic.
- [ ] Any shareable logic I wrote is either already kit-hosted, or a documented ≤2-release wrap with a filed proposal.
- [ ] The consumer registry row for my service exists and is current.
- [ ] `/alaa-golang` + `/alaa-golang-clean-code-principles` were loaded for all Go work; findings report P-numbers.
- [ ] `contracttest` runs (or its blocked-reason is reported) for any consumer surface I touched.
- [ ] Kit changes followed `GOVERNANCE.md`: classification, `CONTRACTS.md` + docs + contracttest in the same change.
- [ ] Cross-agent prompts I produced were written with `/alaa-prompting-guide` and saved as timestamped files.

## Model and runtime notes

Written to run identically under Claude Fable 5 / Opus 4.8 / Sonnet 5 (Claude Code) and GPT-5.5 (Codex):
imperative, self-contained markdown; no runtime-specific tooling required. Skill triggers differ by runtime
(`/name` vs `$name`) — when generating prompts for another runtime, use `alaa-prompting-guide`'s trigger-syntax
reference. Subagents/plan modes are optional accelerators, never prerequisites: in Claude Code, broad multi-repo
audit sweeps may fan out to Explore/general-purpose subagents; in Codex, run the same sweep sequentially.

## Reference index

| File | Read when |
|---|---|
| `references/10-consumer-development.md` | building or migrating any service on the kit |
| `references/20-change-request-workflow.md` | filing kit bugs/upgrades or baseline proposals |
| `references/30-kit-owner-workflow.md` | acting as the kit's responsible agent |
| `references/40-platform-audit.md` | monitoring/auditing kit + consumers |
| `references/50-consumer-registry.md` | registering a consumer / maintaining the roster |
| `assets/templates/kit-change-request.md` | template for law 1 documents |
| `assets/templates/baseline-proposal.md` | template for law 2 documents |
| `assets/templates/consumers-registry.md` | template for `docs/CONSUMERS.md` (first registration creates it) |
| `assets/templates/consumer-update-prompt.md` | template for propagation prompts to consumer agents |
| `assets/templates/audit-report.md` | template for platform audit outputs |
