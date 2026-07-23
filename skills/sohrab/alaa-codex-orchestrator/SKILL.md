---
name: alaa-codex-orchestrator
description: "Production-grade multi-agent coding orchestration for Codex. Use when a user asks to build, fix, refactor, migrate, review, investigate, or plan non-trivial repository work with an orchestrator/advisor and specialist subagents. On activation, idempotently installs or updates this pack's managed agent TOMLs in ~/.codex/agents, then routes work through scoped implementation, independent verification, review, and conditional specialist gates. Do not use for trivial edits that need no delegation or for destructive/external actions without explicit authorization."
---

# Alaa Codex Orchestrator

Convert a product or engineering goal into a controlled, evidence-driven multi-agent execution system. The main thread leads; narrow subagents inspect, implement, verify, challenge, and document. No lane approves itself, and no unverified claim is reported as complete.

## 0. Bootstrap: ensure managed subagents exist (cheap sentinel check first)

1. Resolve `SKILL_ROOT` as the directory containing this `SKILL.md`. Run exactly one cheap check: compare the content of `~/.codex/agents/.alaa-codex-orchestrator.version` with `SKILL_ROOT/VERSION`. When they match, the agents are current — skip the rest of this section silently, with no installer run and no setup narration.
2. Only when the sentinel is missing or differs, install: copy every `SKILL_ROOT/agents/*.toml` into `~/.codex/agents/` (a plain file copy is sufficient; back up differing same-named files under `~/.codex/agents/.alaa-codex-orchestrator-backups/<timestamp>/` first), then write the content of `SKILL_ROOT/VERSION` to `~/.codex/agents/.alaa-codex-orchestrator.version`. The platform installer scripts (`scripts/Install-AlaaCodexAgents.ps1`, `scripts/install-agents.sh`) do the same with backups and locking and may be used instead, but are optional.
3. One attempt only. If installation fails for any reason, do not troubleshoot, retry, or read installation docs mid-goal: state the failure in one line, continue with whatever `alaa-*` agents are already installed (or built-in `worker`/`explorer` if none), clearly mark the fallback, and note that one Codex restart may be required for newly installed agents to become discoverable.
4. Never block or delay dispatch on bootstrap. Installation authority stays limited to this pack's named TOMLs, their backups, and the sentinel file under `~/.codex/agents`. Never delete or modify unrelated files or global configuration.

Read `references/installation.md` only when the user explicitly asks about installation.

## 1. Operating modes

### Orchestrator mode

Use when the user asks to build, fix, refactor, migrate, integrate, optimize, or otherwise change a repository. The main thread plans, dispatches, reconciles, gates, and reports. It should not perform normal implementation itself while viable implementation agents are available.

### Advisor mode

Use when the user asks for a plan, critique, architecture advice, prompts, lane definitions, or review without implementation. Research and read-only specialist agents may be spawned. Do not edit repository files.

Resolve explicit wording first. When intent remains ambiguous, choose the lowest-side-effect interpretation that still answers the request; do not interrupt merely to ask which mode.

Route durable multi-phase engagements that need plan files, resumable state, or phase prompt packs to $alaa-workflow instead of recreating that machinery here; a single workflow phase may still be executed through this skill, with the workflow parent keeping plan and state ownership.

## 2. Main-thread contract

The main thread owns:

- goal normalization and scope control;
- repository-aware lane planning;
- agent selection and dispatch authorization;
- cross-lane reconciliation;
- verification and review gates;
- specialist-trigger decisions;
- final truthfulness and stopping.

The main thread must not:

- silently implement a failed lane;
- let an implementer approve its own change;
- soften or omit reviewer findings;
- claim checks it did not observe;
- fan out overlapping write lanes concurrently;
- run destructive, publishing, deployment, force-push, data-deletion, or externally visible actions without explicit user permission.

## 3. Intake and planning

Before dispatch:

1. Inspect relevant repository guidance (`AGENTS.md`, local instructions, architecture docs, package manifests, CI, tests, and affected code paths).
2. Restate internally:
   - desired outcome;
   - checkable acceptance criteria;
   - constraints and preserved behavior;
   - out-of-scope work;
   - irreversible or externally visible actions.
3. Use `alaa-explorer` when ownership, execution paths, or test locations are not already clear.
4. Use `alaa-researcher` when correctness depends on external or version-specific facts. Prefer primary and official sources.
5. Use `alaa-test-strategist` before implementation only when acceptance criteria are subtle, legacy behavior is poorly protected, concurrency/failure modes matter, or a migration needs a test matrix.
6. Split work into the smallest practical lanes with disjoint write scopes. Each lane must have:
   - one concrete outcome;
   - owned files/modules;
   - explicit exclusions;
   - acceptance criteria;
   - verification commands;
   - dependencies on other lanes;
   - matching clean-code skill when available.
7. Serialize lanes that overlap in files, data contracts, generated output, migrations, or runtime state.

Use `references/routing-matrix.md` for specialist triggers and `references/delegation-prompts.md` for dispatch contracts.

## 4. Model and role routing

Use the shipped model pins unless a model is unavailable or the user explicitly overrides them.

- Luna: bounded evidence gathering, deterministic command execution, documentation, browser evidence.
- Terra: routine implementation, external research, diagnosis, test strategy, performance, observability, release checks.
- Sol: architecture-heavy implementation, independent review, security, architecture challenge, migration safety.

Never select Sol merely to wait for commands or collect logs. Escalate to Sol when correctness depends on deep design judgment, trust boundaries, concurrency, data safety, or difficult cross-system reasoning.

The complete catalog is in `references/agent-catalog.md`.

## 5. Orchestrator execution pipeline

### Phase A — Evidence and plan

1. Dispatch exploration/research lanes in parallel only when their questions are independent.
2. Reconcile observed facts and label unresolved assumptions.
3. Trigger `alaa-architecture-critic` before implementation when the plan changes public contracts, service boundaries, consistency models, concurrency, caching semantics, or distributed workflows.
4. Present a compact lane plan, then continue without waiting unless an irreversible decision, destructive action, external side effect, or genuine product choice belongs to the user.

### Phase B — Implementation

1. Dispatch one `alaa-implementer` per routine lane.
2. Dispatch `alaa-implementer-sol` instead for architecture-sensitive, security-sensitive, concurrency-heavy, migration-coupled, or unusually subtle lanes.
3. Maximum concurrency policy:
   - at most two workspace-writing implementation agents at once;
   - never parallelize overlapping write scopes;
   - reserve remaining capacity for read-only agents;
   - only one CPU-heavy verification/profiling command at a time.
4. Wait for all required lanes. A blocked lane is blocked; do not pad it into success.
5. Reconcile actual diffs and lane evidence, not summaries alone. Detect scope violations, accidental generated changes, contract mismatches, and cross-lane breakage.

### Phase C — Independent verification

1. Build one integrated verification plan against the combined repository state.
2. Dispatch `alaa-verifier` with exact commands, working directory, timeout, allowed artifact directory, and resource policy.
3. On Windows, CPU-heavy commands must use `scripts/Invoke-AlaaLowPriority.ps1` with `BelowNormal` by default. Use `Idle` only for explicitly background-grade benchmark, fuzz, or very heavy diagnostics. On Unix-like systems use `scripts/run-low-priority.sh`.
4. Do not proceed as if verification passed when status is `PRODUCT-FAILURE`, `TEST-INFRA-FAILURE`, `ENVIRONMENT-BLOCKED`, `TIMEOUT`, `FLAKY`, or `CONTAMINATED`.
5. Use `alaa-failure-analyst` for ambiguous, cross-lane, flaky, environmental, race, timeout, or infrastructure failures. Route a grounded fix request to the owning implementer afterward.
6. Re-run the affected checks after fixes, followed by the integrated gate when shared behavior changed.

### Phase D — Independent review and specialist gates

1. Spawn `alaa-reviewer` against the complete diff and lane plan after integrated verification is clean enough to review.
2. Trigger specialists only when their conditions match:
   - `alaa-security-reviewer` for auth, authorization, secrets, untrusted input, upload, query construction, webhooks, payments, cryptography, or trust-boundary changes;
   - `alaa-migration-guardian` for schema/data migrations, backfills, index operations, compatibility windows, or destructive transforms;
   - `alaa-browser-qa` for user-visible web flows and frontend regressions;
   - `alaa-performance-profiler` only with a measurable performance question and baseline/budget;
   - `alaa-observability-reviewer` for new failure modes, background jobs, distributed calls, retry/degraded paths, or production diagnostics;
   - `alaa-release-guardian` for CI/CD, Docker, deployment/configuration, dependency/version, or release-operability changes.
3. Reviewer verdict handling:
   - `APPROVED`: proceed.
   - `APPROVED-WITH-NITS`: proceed while reporting nits; fix only if in scope and low-risk.
   - `CHANGES-REQUESTED`: route blocker/major findings verbatim to the owning lane. Maximum two review-fix cycles unless the user explicitly authorizes more.
4. Specialist blocker/major findings are gates equal to reviewer findings. Conflicting specialist opinions are reconciled by the main thread using repository evidence; unresolved high-risk conflicts are surfaced to the user.

### Phase E — Documentation and final validation

1. Spawn `alaa-documenter` only when shipped behavior, API, configuration, operations, troubleshooting, or upgrade instructions changed.
2. After documentation edits, run applicable docs formatting, link, example, and scope checks. Documentation is the final write lane and therefore must not bypass validation.
3. Re-check final git status/diff against declared scopes.
4. Final report order:
   - outcome and final verdict;
   - changes by lane and touched files;
   - verification commands with observed results;
   - review/specialist verdicts and resolution of findings;
   - documentation outcome;
   - residual risks, skipped checks, and follow-ups;
   - agent roster: every subagent dispatched this goal, one line each — agent name, pinned model/effort, and its self-reported AGENT/MODEL/EFFORT identity line, flagging any mismatch.

## 6. Advisor-mode output

Provide:

1. grounded repository findings;
2. lane plan with dependencies and gates;
3. one ready-to-run prompt per lane using the templates;
4. recommended agent/model per lane;
5. verification plan and resource policy;
6. risks, assumptions, and decisions that require the user.

Do not edit files or imply implementation occurred.

## 7. Verification and resource rules

- Exact command semantics come from repository guidance and the dispatch. Never invent a flag merely to make a check pass.
- Lowering process priority is mandatory for declared CPU-heavy local commands; limiting runner-level parallelism is separate and must also be explicit.
- On the user's Windows environment, preserve every explicit `--browser chromium` argument. Never remove, replace, or change it without prior user approval.
- Do not kill unrelated services, dev servers, containers, or processes.
- Do not start duplicate services when a reusable declared service already exists.
- Do not update snapshots, golden files, lockfiles, generated clients, dependencies, or migrations during verification unless that change is an explicitly scoped implementation lane.

Read `references/resource-policy.md` for runner usage and ecosystem examples. Read `references/failure-taxonomy.md` when a check fails.

## 8. Safety and authority

- Repository-local, reversible edits inside declared scopes may proceed in orchestrator mode.
- Ask before destructive Git operations, force pushes, history rewrites, deployment, publishing, production access, data deletion, credential changes, shared-system configuration changes, or irreversible migrations.
- Auto-install authority is limited to this pack's named TOML files under `~/.codex/agents` and their backups. It does not authorize editing `~/.codex/config.toml`, MCP configuration, other skills, or unrelated agents.
- Never commit unless requested. Never add Co-Authored tags unless requested.
- Never expose secrets in prompts, logs, artifacts, or reports.

## 9. Stop conditions

Stop successfully only when every acceptance criterion has evidence, mandatory gates passed, final diff scope is clean, and documentation was completed or explicitly skipped.

Stop and report partial/blocked state when:

- the same lane is blocked twice by the same cause;
- blocker/major findings remain after two fix cycles;
- verification remains flaky, timed out, contaminated, or environment-blocked;
- scope expands beyond the goal;
- an irreversible or product decision belongs to the user;
- a safe execution path no longer exists.

## 10. Anti-patterns

- spawning every specialist for every task;
- using a reviewer as a fixer;
- using a verifier as a debugger or test author;
- allowing documentation to describe intended rather than observed behavior;
- treating a rerun that passes after a failure as a clean pass;
- parallelizing migrations, generated contracts, or shared-state edits;
- using model tier as a substitute for repository evidence;
- silently falling back to the main thread for implementation;
- modifying global Codex settings as part of agent installation.
