---
name: alaa-go-chi-development
description: "Governance, capability map, and evidence-first workflow for the shared alaa-go-chi Go kit and every service built on it (news, notif, entitlement-api, tusd, wa-api, and all future Ala Go services). Use for new-service bootstrap, existing-service diagnosis/upgrade/migration, kit capability selection, config/readiness/API-contract/scaffold/Tier-2 generation work, kit bug or baseline requests, kit-owner intake/changes/releases, consumer registration/propagation prompts, and kit/consumer audits. Phase-aware: it enforces the kit repo's owner-ratified scope decision — currently the KIT_FIRST_STABILIZATION freeze (kit-only evidence; no consumer inspection, edits, compatibility claims, prompts, propagation, or release gates until explicit owner reactivation). Routes actual Go engineering to alaa-golang and alaa-golang-clean-code-principles."
---

# alaa-go-chi Development — Kit ↔ Consumer Governance

`alaa-go-chi` (module `git.alaatv.com/vk/alaa-go-chi`) is the shared base for every Ala Go service: **the kit
writes shared things once; a service repository contains only its domain.** The moment a consumer re-implements a
kit surface, patches the kit privately, or grows a second copy of logic another service also has, the platform is
back to the drift the kit was built to kill. This skill is the operating contract that prevents that — it owns
*how the kit and its consumers change over time*: who may change what, through which documents, and how changes
propagate. Repository truth always outranks this skill.

## Start here (every session)

1. Identify your role: kit owner, service developer/debugger/upgrader, change-request author, or auditor.
2. In the kit repo, read `CONSTITUTION.md` in full before planning or edits; then the task-relevant parts of
   `GOVERNANCE.md`, `CONTRACTS.md`, `docs/RUNBOOK.md`, `docs/CONSUMERS.md`, `docs/INDEX.md`, and current source.
3. Read [phase and source truth](references/05-phase-and-source-truth.md) — mandatory in every mode. It defines
   the authority order and the active scope phase. **`KIT_FIRST_STABILIZATION` is currently active**: kit-only
   scope, no consumer inspection/edits/prompts/propagation, every consumer impact exactly
   `NOT_ASSESSED_KIT_FIRST`, until the owner explicitly reactivates consumer work. Verify the phase against repo
   truth; never infer reactivation.
4. For any Go planning, code, review, or validation, load `alaa-golang-clean-code-principles` (P1–P13) and
   normally `alaa-golang` — mandatory, not optional, for kit and consumer code alike.
5. Read only the mode/capability references your task needs (table below).

## Which mode am I in?

| You are asked to… | Read |
|---|---|
| Create or extend a service on the kit | [10-consumer-development](references/10-consumer-development.md) + [12-kit-capability-map](references/12-kit-capability-map.md) |
| Debug, upgrade, migrate, or review a service | [15-debug-upgrade-migrate](references/15-debug-upgrade-migrate.md) + capability map |
| Report a kit bug / request an upgrade / propose a shared baseline | [20-change-request-workflow](references/20-change-request-workflow.md) |
| Act as the kit's responsible agent: intake, change, release, propagate | [30-kit-owner-workflow](references/30-kit-owner-workflow.md) + capability map |
| Audit the kit (and, after reactivation, consumers) | [40-platform-audit](references/40-platform-audit.md) |
| Register a service / maintain the roster | [50-consumer-registry](references/50-consumer-registry.md) |

A single task often crosses modes — consumer work discovers a kit bug (file a change request), an audit finds
duplication (baseline proposal → kit ownership → propagation). Follow each mode's reference at the point you
enter it.

## Governing laws (apply in every mode)

1. **Consumers never change the kit.** No edits, no forks, no quiet re-implementation. A kit need becomes one
   timestamped `YYYY-MM-DD-<slug>.md` change-request or baseline-proposal file — the only channel. The only
   sanctioned interim form is a thin marked `KIT-WRAP` with a same-day request on file and a maximum two-release
   lifetime. The only kit-repo file a consumer agent may edit is its own `docs/CONSUMERS.md` row.
2. **Baseline-first for shared logic.** Platform-shaped behavior (transport, contracts, trust, lifecycle,
   operational mechanics, generators, cross-service invariants) belongs in the kit; domain policy stays in the
   service. If code would look materially identical in a second service, it is kit material — propose, don't
   duplicate.
3. **Every consumer registers itself** in the kit's `docs/CONSUMERS.md` and keeps its row current. An
   unregistered consumer is invisible to impact analysis and will be broken silently.
4. **Contract surfaces move atomically:** implementation, tests, `CONTRACTS.md`, decision record, generated
   artifacts, docs/index/runbook, and release classification land together. Error codes are append-only; metric
   names and env keys are kit-owned.
5. **Generated files change only through their generators.** Tier-2 outputs come only from `alaa-go-chi gen` with
   the matching kit version; goldens regenerate, never hand-edit.
   Two generated seams have platform-external owners: **permissions** come from `alaa-permission-catalog` via the
   `alaa-permission-generator` skill (`internal/authz/permissions_gen.go` + the `auth` seed — never hand-written),
   and **local runtime/shared-infra generation** mirrors the canonical `service-runtime-kit` identity so every Go
   and Laravel service reuses the one `alaa-shared-infra` instance — services never declare sibling infra.
   Runtime-kit behavior evolves centrally in the kit with a multi-consumer abstraction mindset (the Go counterpart
   of `service-runtime-kit-governance`), never per-service.
6. **Preserve the platform invariants** (P1–P13): route posture, trusted identity, typed error envelopes,
   transaction truth, idempotency, bounded owned concurrency, boot-time config, low-cardinality telemetry,
   real-boundary proof.
7. **Evidence honesty.** Never claim production/SLA readiness from unit tests alone; name which load, HA/failover,
   chaos, capacity, truth-tier, remote-CI, and live SLO evidence exists or is missing. Remote CI is
   `runner_contract_pending` until a real runner job passes.
8. **Consult the ratified decision register before designing kit-owned behavior.** The kit's contract decisions —
   HTTP read/write/idle/body bounds and the per-route body override, trust / `X-Access` / location semantics,
   error / readiness / log / trace / Sentry vocabularies, MQ message-id / fingerprint / per-role channels /
   prefetch, outbox lease-fence-quarantine, job execution budget + PG classifier, shutdown budget/grace, and
   release / CI / image-digest policy — plus the **consumer-tunable env surface** (every knob, default, and clamp)
   live in the kit repo's `docs/change-requests/2026-07-21-kit-bug-remediation-decision-register.md` (its ratified
   `Owner outcome` blocks, the `Consumer-tunable env surface` table, and the two 2026-07-23 amendment rounds). Read
   the relevant decision before proposing or coding in that area — silently re-deciding or diverging from a ratified
   value is exactly the drift this skill exists to kill. **Ratified is not implemented:** confirm the implementation
   status from the plan phases and current source, and never claim an env key or capability exists until code proves
   it. A consumer-binding value reaches consumer repos only through the generated
   `docs/consumer-templates/{AGENTS.md,CLAUDE.md}` (laws 1 and 4) — so it must land there, not only in the kit.

## Mandatory skill routing

This skill owns governance; route the engineering (Claude Code `/name`, Codex `$name`):

| Task involves | Load |
|---|---|
| Any Go code at all | `alaa-golang` + `alaa-golang-clean-code-principles` (both mandatory) |
| Envelopes, readiness, gateway prefixes, cross-service conventions | `alaa-services-contract` |
| Trusted headers, TrustCtx, permissions, TOTP, tenancy | `alaa-trust-gateway-auth`, `alaa-security-review` |
| Adding/changing permission names or bitmap ids; onboarding the permission map | `alaa-permission-generator` (catalog: `alaa-permission-catalog`) |
| Local runtime / shared-infra generation parity with Laravel services | `service-runtime-kit-governance` |
| Postgres, migrations, pooling lanes, Redis | `alaa-data-layer` |
| RabbitMQ, outbox, consumers, DLQ, idempotency | `alaa-async-messaging` |
| Logs/metrics/traces/Sentry/SigNoz | `alaa-observability-soc` |
| Docker/Compose/Swarm; Kubernetes/Helm/Arvan | `alaa-docker-production`; `alaa-k8s-helm`, `caas-arvan-kuber` |
| GitLab CI pipelines | `alaa-gitlab-ci-cd` |
| OpenAPI/Postman artifacts | `alaa-postman-collections`, `golang-swagger` |
| Writing prompts for another agent (propagation, handoffs) | `alaa-prompting-guide` — mandatory first |
| Long multi-phase work; noisy investigation | `alaa-workflow`, `alaa-low-noise` |
| Docs packs | `alaa-docs-farsi` |

## Completion check (before finishing any task in any mode)

- [ ] Current code and applicable contracts were inspected; assumptions and drift are explicit.
- [ ] The active phase was verified from repo truth and respected; during kit-first, no consumer work occurred and
      all consumer impacts remain `NOT_ASSESSED_KIT_FIRST`.
- [ ] No kit surface was edited from a consumer context; every kit need became one timestamped request file; any
      shareable logic is kit-hosted or a documented ≤2-release `KIT-WRAP` with a filed proposal.
- [ ] `alaa-golang` + `alaa-golang-clean-code-principles` were loaded for all Go work; findings cite P-numbers.
- [ ] Public/env/error/metric/migration/generated contracts and docs agree; generated files were regenerated, not
      hand-edited; the registry row (where phase-allowed) is current.
- [ ] Targeted tests, relevant contract/generator/governance gates, race/static checks, and truth-tier tests ran —
      or their exact blockers are reported. Security, privacy, concurrency, failure, observability, rollback, and
      operations were assessed proportionally.
- [ ] Cross-agent prompts were authored with `alaa-prompting-guide` and saved as timestamped files (reactivated
      phase only).

## Reference index

| File | Purpose |
|---|---|
| `references/05-phase-and-source-truth.md` | mandatory authority order, phase gate, evidence vocabulary |
| `references/10-consumer-development.md` | building/extending a service on the kit (phase-gated) |
| `references/12-kit-capability-map.md` | current kit packages, CLI commands, generated surfaces, validation targets |
| `references/15-debug-upgrade-migrate.md` | diagnose, upgrade, migrate, review without forking the kit |
| `references/20-change-request-workflow.md` | the durable consumer→kit request channel |
| `references/30-kit-owner-workflow.md` | intake, implementation, release, phase-gated propagation |
| `references/40-platform-audit.md` | kit-only audit now; kit+consumer audit after reactivation |
| `references/50-consumer-registry.md` | registry row contract and phase-aware semantics |
| `assets/templates/` | request, proposal, registry, propagation-prompt, and audit templates |
| `evals/evals.json` | phase, governance, capability, and diagnostic behavior evaluations |
