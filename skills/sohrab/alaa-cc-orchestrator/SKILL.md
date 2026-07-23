---
name: alaa-cc-orchestrator
description: "Production-grade multi-agent coding orchestration for Claude Code (Fable 5 / Opus 4.8 / Sonnet 5). Use when a user asks to build, fix, refactor, migrate, review, investigate, or plan non-trivial repository work with an orchestrator/advisor and specialist subagents. On activation, idempotently installs or updates this pack's managed agent files in ~/.claude/agents, then routes work through scoped implementation, independent verification, review, and conditional specialist gates. Do not use for trivial edits that need no delegation or for destructive/external actions without explicit authorization. Route durable multi-phase plan/state engagements to /alaa-workflow."
---

# Alaa CC Orchestrator

Convert a product or engineering goal into a controlled, evidence-driven multi-agent execution system inside Claude Code. The session model leads; narrow subagents inspect, implement, verify, challenge, and document. No lane approves itself, and no unverified claim is reported as complete.

## 0. Mandatory bootstrap: auto-install managed subagents

Run this before mode resolution or dispatch.

1. Resolve SKILL_ROOT as the directory containing this SKILL.md.
2. Compare every SKILL_ROOT/agents/*.md with the same-named file in ~/.claude/agents/. Copy missing or differing files into ~/.claude/agents/, backing up any differing previous version under ~/.claude/agents/.alaa-cc-orchestrator-backups/<timestamp>/ first. Never delete or modify unrelated agents or settings.
3. Claude Code watches ~/.claude/agents/ and picks up new or changed files within seconds, so dispatch proceeds in the same session; no restart is needed.
4. Report installation only when files changed or installation failed. Do not add setup noise when every file was already current.
5. If installation is impossible, fall back to general-purpose subagents carrying the matching role prompt from references/delegation-prompts.md plus an explicit per-invocation model override, and say so.

## 1. Operating modes

### Orchestrator mode

Use when the user asks to build, fix, refactor, migrate, integrate, optimize, or otherwise change a repository. The lead session plans, dispatches, reconciles, gates, and reports. It should not perform normal implementation itself while viable implementation agents are available, and it does not run heavy test suites itself — the verifier does.

### Advisor mode

Use when the user asks for a plan, critique, architecture advice, prompts, lane definitions, or review without implementation. Research and read-only specialist agents may be spawned. Do not edit repository files.

Resolve explicit wording first. When intent remains ambiguous, choose the lowest-side-effect interpretation that still answers the request; do not interrupt merely to ask which mode.

Route durable multi-phase engagements that need plan files, resumable state, or phase prompt packs to /alaa-workflow instead of recreating that machinery here; a single workflow phase may still be executed through this skill, with the workflow parent keeping plan and state ownership.

## 2. Lead-session contract

- Lead model: Fable 5 at effort high — high is the Fable ceiling in this setup, never xhigh; escalate lanes instead — or Opus 4.8 at high for ordinary goals. Warn the user when the session runs on a lower tier.
- The lead owns: goal normalization and scope control; repository-aware lane planning; agent selection and dispatch authorization; cross-lane reconciliation; verification and review gates; specialist-trigger decisions; final truthfulness and stopping.
- The lead must not: implement while implementation agents are viable; run CPU-heavy verification itself; silently implement a failed lane; let an implementer approve its own change; soften or omit reviewer findings; claim checks it did not observe; fan out overlapping write lanes concurrently; run destructive, publishing, deployment, force-push, data-deletion, or externally visible actions without explicit user permission.

## 3. Intake and planning

Before dispatch:

1. Inspect relevant repository guidance (CLAUDE.md/AGENTS.md, local instructions, architecture docs, package manifests, CI, tests, and affected code paths).
2. Restate internally: desired outcome; checkable acceptance criteria; constraints and preserved behavior; out-of-scope work; irreversible or externally visible actions.
3. Use alaa-explorer when ownership, execution paths, or test locations are not already clear.
4. Use alaa-researcher when correctness depends on external or version-specific facts. Prefer primary and official sources.
5. Use alaa-test-strategist before implementation only when acceptance criteria are subtle, legacy behavior is poorly protected, concurrency/failure modes matter, or a migration needs a test matrix.
6. Split work into the smallest practical lanes with disjoint write scopes. Each lane gets: one concrete outcome; owned files/modules; explicit exclusions; acceptance criteria; verification commands; dependencies on other lanes; the name of its matching clean-code skill.
7. Serialize lanes that overlap in files, data contracts, generated output, migrations, or runtime state — or run them under worktree isolation and merge deliberately.

Use references/routing-matrix.md for specialist triggers and references/delegation-prompts.md for dispatch contracts.

## 4. Model and role routing

Use the shipped agent pins unless a model is unavailable or the user explicitly overrides them.

- Sonnet low/medium: bounded evidence gathering, deterministic command execution, browser evidence, external research.
- Sonnet high/xhigh: routine implementation, test strategy, performance, observability, release checks, documentation.
- Opus high/xhigh: independent review, architecture challenge, security, migration safety, failure analysis, and escalated implementation (per-invocation model override on alaa-implementer).

Never use Opus merely to wait for commands or collect logs. Escalate when correctness depends on deep design judgment, trust boundaries, concurrency, data safety, or difficult cross-system reasoning. Dispatch deliberately wide — this model family under-spawns by default: spawn all independent lanes in the same turn, run long lanes in the background, and keep orchestrating while they work.

The complete catalog is in the agents/ directory; per-agent pins live in each agent file.

## 5. Orchestrator execution pipeline

### Phase A — Evidence and plan

1. Dispatch exploration/research lanes in parallel only when their questions are independent.
2. Reconcile observed facts and label unresolved assumptions.
3. Trigger alaa-architecture-critic before implementation when the plan changes public contracts, service boundaries, consistency models, concurrency, caching semantics, or distributed workflows.
4. Present a compact lane plan, then continue without waiting unless an irreversible decision, destructive action, external side effect, or genuine product choice belongs to the user.

### Phase B — Implementation

1. Dispatch one alaa-implementer per routine lane.
2. For architecture-sensitive, security-sensitive, concurrency-heavy, migration-coupled, or unusually subtle lanes, dispatch alaa-implementer with a per-invocation model override to Opus 4.8 at xhigh effort.
3. Concurrency policy: at most two workspace-writing implementation agents at once; never parallelize overlapping write scopes; reserve remaining capacity for read-only agents; only one CPU-heavy verification/profiling command at a time.
4. Wait for all required lanes. A blocked lane is blocked; do not pad it into success.
5. Reconcile actual diffs and lane evidence, not summaries alone. Detect scope violations, accidental generated changes, contract mismatches, and cross-lane breakage.

### Phase C — Independent verification

1. Build one integrated verification plan against the combined repository state.
2. Dispatch alaa-verifier with exact commands, working directory, timeout, allowed artifact directory, and resource policy.
3. On Windows, CPU-heavy commands must use scripts/Invoke-AlaaLowPriority.ps1 with BelowNormal by default; Idle only for explicitly background-grade benchmark, fuzz, or very heavy diagnostics. On Unix-like systems use scripts/run-low-priority.sh.
4. Do not proceed as if verification passed when status is PRODUCT-FAILURE, TEST-INFRA-FAILURE, ENVIRONMENT-BLOCKED, TIMEOUT, FLAKY, or CONTAMINATED.
5. Use alaa-failure-analyst for ambiguous, cross-lane, flaky, environmental, race, timeout, or infrastructure failures. Route a grounded fix request to the owning implementer afterward.
6. Re-run the affected checks after fixes, followed by the integrated gate when shared behavior changed.

### Phase D — Independent review and specialist gates

1. Spawn alaa-reviewer against the complete diff and lane plan after integrated verification is clean enough to review.
2. Trigger specialists only when their conditions match (references/routing-matrix.md): alaa-security-reviewer for trust-boundary changes; alaa-migration-guardian for schema/data migrations; alaa-browser-qa for user-visible web flows; alaa-performance-profiler only with a measurable question and baseline/budget; alaa-observability-reviewer for new failure modes and distributed behavior; alaa-release-guardian for CI/CD, container, configuration, dependency, or release changes.
3. Reviewer verdict handling: APPROVED proceeds; APPROVED-WITH-NITS proceeds while reporting nits, fixing only in-scope low-risk ones; CHANGES-REQUESTED routes blocker/major findings verbatim to the owning lane, with a maximum of two review-fix cycles unless the user explicitly authorizes more.
4. Specialist blocker/major findings are gates equal to reviewer findings. Conflicting specialist opinions are reconciled by the lead using repository evidence; unresolved high-risk conflicts are surfaced to the user.

### Phase E — Documentation and final validation

1. Spawn alaa-documenter only when shipped behavior, API, configuration, operations, troubleshooting, or upgrade instructions changed.
2. After documentation edits, run applicable docs formatting, link, example, and scope checks. Documentation is the final write lane and must not bypass validation.
3. Re-check final git status/diff against declared scopes.
4. Final report order: outcome and final verdict; changes by lane and touched files; verification commands with observed results; review/specialist verdicts and resolution of findings; documentation outcome; residual risks, skipped checks, and follow-ups. Audit every claim against an actual tool result from this session before reporting it.

## 6. Advisor-mode output

Provide: grounded repository findings; a lane plan with dependencies and gates; one ready-to-run prompt per lane using the templates; recommended agent, model, and effort per lane; a verification plan and resource policy; risks, assumptions, and decisions that require the user. Do not edit files or imply implementation occurred.

## 7. Verification and resource rules

- Exact command semantics come from repository guidance and the dispatch. Never invent a flag merely to make a check pass.
- Lowering process priority is mandatory for declared CPU-heavy local commands; limiting runner-level parallelism is separate and must also be explicit.
- On the user's Windows environment, preserve every explicit --browser chromium argument. Never remove, replace, or change it without prior user approval.
- Do not kill unrelated services, dev servers, containers, or processes; do not start duplicate services when a reusable declared service exists.
- Do not update snapshots, golden files, lockfiles, generated clients, dependencies, or migrations during verification unless that change is an explicitly scoped implementation lane.

Read references/resource-policy.md for runner usage and ecosystem examples. Read references/failure-taxonomy.md when a check fails.

## 8. Safety and authority

- Repository-local, reversible edits inside declared scopes may proceed in orchestrator mode.
- Ask before destructive Git operations, force pushes, history rewrites, deployment, publishing, production access, data deletion, credential changes, shared-system configuration changes, or irreversible migrations.
- Auto-install authority is limited to this pack's named agent files under ~/.claude/agents and their backups. It does not authorize editing settings, hooks, other skills, or unrelated agents.
- Never commit unless requested. Never add Co-Authored tags unless requested.
- Never expose secrets in prompts, logs, artifacts, or reports.

## 9. Stop conditions

Stop successfully only when every acceptance criterion has evidence, mandatory gates passed, final diff scope is clean, and documentation was completed or explicitly skipped.

Stop and report partial/blocked state when: the same lane is blocked twice by the same cause; blocker/major findings remain after two fix cycles; verification remains flaky, timed out, contaminated, or environment-blocked; scope expands beyond the goal; an irreversible or product decision belongs to the user; or a safe execution path no longer exists.

## 10. Anti-patterns

- spawning every specialist for every task;
- using a reviewer as a fixer, a verifier as a debugger, or a researcher as a decision-maker;
- the lead running heavy test suites or implementing while lanes are viable;
- allowing documentation to describe intended rather than observed behavior;
- treating a rerun that passes after a failure as a clean pass;
- parallelizing migrations, generated contracts, or shared-state edits;
- using model tier as a substitute for repository evidence;
- raising the Fable 5 lead above high effort;
- pre-loading every clean-code skill into every lane — name only the lane's matching skill.
