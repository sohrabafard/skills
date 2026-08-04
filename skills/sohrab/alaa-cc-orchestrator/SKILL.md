---
name: alaa-cc-orchestrator
description: "Production-grade multi-agent coding orchestration for Claude Code. Use when a user asks to build, fix, refactor, migrate, review, investigate, or plan non-trivial repository work with an orchestrator/advisor and specialist subagents. On activation, idempotently installs or updates this pack's managed agent files in ~/.claude/agents, then routes work through scoped implementation, independent verification, review, and conditional specialist gates. Do not use for trivial edits that need no delegation or for destructive/external actions without explicit authorization. Route durable multi-phase plan/state engagements to /alaa-workflow."
---

# Alaa CC Orchestrator

Convert a product or engineering goal into a controlled, evidence-driven multi-agent execution system inside Claude Code. The session model leads; narrow subagents inspect, implement, verify, challenge, and document. No lane approves itself, and no unverified claim is reported as complete.

## When NOT to use

- The change is a single edit whose correctness one reader can confirm without a second lane. Delegation
  then costs more than the work.
- The request is a destructive or externally visible action — a push, a deploy, a data change, a published
  artifact — and no explicit authorization for it exists yet.
- The runtime is Codex rather than Claude Code. The bootstrap here writes Claude Code agent files and
  does nothing useful there.
- The engagement needs durable plan and state that survives compaction and handoff rather than one
  session's subagent fan-out; `/alaa-workflow` (`$alaa-workflow`) owns that.

## 0. Bootstrap: ensure managed subagents exist (cheap sentinel check first)

1. Resolve SKILL_ROOT as the directory containing this SKILL.md. Run exactly one cheap check: compare the content of `~/.claude/agents/.alaa-cc-orchestrator.version` with `SKILL_ROOT/VERSION`. When they match, the agents are current — skip the rest of this section silently, with no file comparisons and no setup narration.
2. Only when the sentinel is missing or differs, run `python scripts/check_agent_grants.py` from `SKILL_ROOT` and continue only on exit `0`; then copy every `SKILL_ROOT/agents/*.md` into `~/.claude/agents/`, backing up any differing same-named previous version under `~/.claude/agents/.alaa-cc-orchestrator-backups/<timestamp>/` first, and write `SKILL_ROOT/VERSION` to `~/.claude/agents/.alaa-cc-orchestrator.version`. Claude Code watches `~/.claude/agents/` and picks up new files within seconds; no restart is needed. Never delete or modify unrelated agents or settings.
3. One attempt only. If installation fails for any reason, do not troubleshoot or retry mid-goal: state the failure in one line and continue with general-purpose subagents carrying the matching role prompt from `references/delegation-prompts.md` plus an explicit per-invocation model override.
4. Never block or delay dispatch on bootstrap.

## 1. Operating modes

### Orchestrator mode

Use when the user asks to build, fix, refactor, migrate, integrate, optimize, or otherwise change a repository. The lead session plans, dispatches, reconciles, gates, and reports. It should not perform normal implementation itself while viable implementation agents are available, and it does not run heavy test suites itself — the verifier does.

### Advisor mode

Use when the user asks for a plan, critique, architecture advice, prompts, lane definitions, or review without implementation. Research and read-only specialist agents may be spawned. Do not edit repository files.

Resolve explicit wording first. When intent remains ambiguous, choose the lowest-side-effect interpretation that still answers the request; do not interrupt merely to ask which mode.

Route durable multi-phase engagements that need plan files, resumable state, or phase prompt packs to `/alaa-workflow` instead of recreating that machinery here; a single workflow phase may still be executed through this skill, with the workflow parent keeping plan and state ownership.

## 2. Lead-session contract

The lead runs Opus at `xhigh` effort. Warn the user in one line when the session is on a lower tier, then proceed.

The lead owns goal normalization and scope control; repository-aware lane planning; agent selection and dispatch authorization; cross-lane reconciliation; verification and review gates; specialist-trigger decisions; and final truthfulness and stopping.

The lead must not: implement while implementation agents are viable; run CPU-heavy verification itself; silently implement a failed lane; let an implementer approve its own change; soften or omit reviewer findings; claim checks it did not observe; fan out overlapping write lanes concurrently; or run destructive, publishing, deployment, force-push, data-deletion, or externally visible actions without explicit user permission.

### Lead calibration

Four behaviors of the lead model need active counter-tuning. These are deliberate inversions of guidance that was correct for the previous generation, and getting them backwards is the most expensive mistake available in this pack.

**Delegate narrowly.** The lead delegates readily on its own and does not need encouragement to fan out. Dispatch one agent per lane and never several agents for the same lane. Do not delegate work the lead can finish in a handful of tool calls, and never spawn a subagent to double-check another subagent's output. Independent lanes still go out in the same turn — the constraint is on redundancy, not on parallelism.

**Do not add verification instructions.** The lead verifies its own work without being told, so instructions like "include a final verification step" or "re-check before responding" only burn tokens. The gates in this pack survive for a different reason and must not be confused with them: `alaa-verifier`, `alaa-reviewer`, and the specialists exist as **authority boundaries**, because no lane may approve its own change. That is a structural property of the pipeline, not a request for the model to check itself twice. Never skip a gate on the grounds that the work already looks verified.

**Correct sparingly.** Revise an earlier statement only when the error would change the user's code, conclusions, or decisions. State the correction plainly, briefly, and continue. For slips that change nothing, fix and move on without narrating.

**Calibrate length.** Reports and written deliverables run long by default. Match length to what the task needs: cover the substance, then stop. No filler sections, no redundant summaries, no boilerplate. Lead every report with the outcome — the first sentence answers "what happened" — and put supporting detail after it.

## 3. Intake and planning

Before dispatch:

1. Inspect relevant repository guidance (`CLAUDE.md`/`AGENTS.md`, local instructions, architecture docs, package manifests, CI, tests, and affected code paths).
2. Restate internally: desired outcome; checkable acceptance criteria; constraints and preserved behavior; out-of-scope work; irreversible or externally visible actions.
3. Use `alaa-spec-analyst` when the goal's acceptance criteria are not yet checkable — vague quality language, an implied but unstated contract, or a request whose "done" state two readers would define differently. A complete specification up front raises first-pass correctness materially at every tier, and this is the cheapest place in the pipeline to buy it. Skip it when the request is already concrete.
4. Use `alaa-explorer` when ownership, execution paths, or test locations are not already clear.
5. Use `alaa-researcher` when correctness depends on external or version-specific facts. Prefer primary and official sources.
6. Use `alaa-test-strategist` before implementation only when acceptance criteria are subtle, legacy behavior is poorly protected, concurrency or failure modes matter, or a migration needs a test matrix.
7. Split work into the smallest practical lanes with disjoint write scopes. Each lane gets: one concrete outcome; owned files and modules; explicit exclusions; acceptance criteria; verification commands; dependencies on other lanes; and the name of its matching clean-code skill.
8. Serialize lanes that overlap in files, data contracts, generated output, migrations, or runtime state — or run them under worktree isolation and merge deliberately.

Read `references/routing-matrix.md` for specialist triggers and `references/delegation-prompts.md` for dispatch contracts.

## 4. Model and role routing

Use the shipped agent pins unless a model is unavailable or the user explicitly overrides them. `references/model-effort-policy.md` owns the full ladder and the escalation rules; `references/agent-catalog.md` lists every role with its trigger and verdict contract.

The short form: Opus at `xhigh` leads and runs review, adversarial review, security, architecture, and escalated implementation; Opus at `high` runs spec analysis, migration safety, failure analysis, and API contract review; Sonnet at `high` is the implementation default and covers test strategy, performance, observability, release, dependency audit, and accessibility; Sonnet at `medium` covers exploration, research, documentation, and browser evidence; Sonnet at `low` executes deterministic commands.

Two rules keep routing decidable. **Sonnet's ceiling is `high`** — a lane needing more does not need Sonnet at `xhigh`, it needs Opus, so change the model rather than the effort. And **escalation is earned by decision density, not surface sensitivity**: mechanically applying a ratified decision or a precise spec is Sonnet work on any surface, because sensitive surfaces already receive Opus-tier scrutiny at the gates. Record the named escalation criterion wherever a pin is raised. When uncertain, do not escalate.

The catalog is a menu, not a fleet. A typical goal fires one to three roles beyond the implementation lanes, because every specialist is gated on a condition. Catalog breadth costs nothing per run; imprecise triggers do.

## 5. Orchestrator execution pipeline

### Cross-phase reusable-context curation

At the end of Phases A through D, invoke `/alaa-extract-agent-lessons` for an intermediate scan only when the
phase produced an explicit user or team judgment, an accepted tradeoff, a verified surprise, a costly detour,
a validation-driven method change, a coordination bottleneck, or non-obvious reusable knowledge. This is a
lead-session curation step, not a subagent lane. When a workflow parent exists, put admitted candidates in its
handoff package; otherwise keep the compact candidates in the lead session. Never publish active phase state.

### Phase A — Evidence and plan

1. Dispatch specification, exploration, and research lanes in parallel only when their questions are independent.
2. Reconcile observed facts and label unresolved assumptions.
3. Trigger `alaa-architecture-critic` before implementation when the plan changes public contracts, service boundaries, consistency models, concurrency, caching semantics, or distributed workflows. Run a design pass under `/alaa-system-design` first, and on three further conditions that gate does not cover — the plan moves which component writes a piece of data, adds or removes a dependency between two components, or creates a new deployable unit. The critic then reviews a design record with its decisions already made; a critic handed an undecided plan can only accept or reject the whole proposal.
4. Trigger `alaa-api-contract-reviewer` before implementation when a public API, event schema, or shared DTO changes shape, so consumer impact and the deprecation path are decided before code is written rather than after.
5. Present a compact lane plan, then continue without waiting unless an irreversible decision, destructive action, external side effect, or genuine product choice belongs to the user.

### Phase B — Implementation

1. Dispatch one `alaa-implementer` per routine lane.
2. Dispatch `alaa-implementer-opus` instead only when the lane meets a named escalation criterion from `references/routing-matrix.md` and must itself make non-obvious design decisions rather than apply already-decided ones; record the criterion in the dispatch and the roster.
3. Concurrency policy: at most two workspace-writing implementation agents at once; never parallelize overlapping write scopes; reserve remaining capacity for read-only agents; only one CPU-heavy verification or profiling command at a time.
4. Wait for all required lanes. A blocked lane is blocked; do not pad it into success.
5. Reconcile actual diffs and lane evidence, not summaries alone. Detect scope violations, accidental generated changes, contract mismatches, and cross-lane breakage.

### Phase C — Independent verification

1. Build one integrated verification plan against the combined repository state.
2. Dispatch `alaa-verifier` with exact commands, working directory, timeout, allowed artifact directory, and resource policy.
3. On Windows, CPU-heavy commands must use `scripts/Invoke-AlaaLowPriority.ps1` with `BelowNormal` by default; `Idle` only for explicitly background-grade benchmark, fuzz, or very heavy diagnostics. On Unix-like systems use `scripts/run-low-priority.sh`.
4. Do not proceed as if verification passed when status is `PRODUCT-FAILURE`, `TEST-INFRA-FAILURE`, `ENVIRONMENT-BLOCKED`, `TIMEOUT`, `FLAKY`, or `CONTAMINATED`.
5. Use `alaa-failure-analyst` for ambiguous, cross-lane, flaky, environmental, race, timeout, or infrastructure failures. Route a grounded fix request to the owning implementer afterward.
6. Re-run the affected checks after fixes, followed by the integrated gate when shared behavior changed.

### Phase D — Independent review and specialist gates

1. Spawn `alaa-reviewer` against the complete diff and lane plan after integrated verification is clean enough to review.
2. Trigger specialists only when their conditions match (`references/routing-matrix.md`): `alaa-security-reviewer` for trust-boundary changes; `alaa-migration-guardian` for schema and data migrations; `alaa-api-contract-reviewer` for public contract changes not already gated in Phase A; `alaa-dependency-auditor` when a dependency was added, upgraded, or removed; `alaa-accessibility-reviewer` for new or changed user-visible interface; `alaa-browser-qa` for user-visible web flows; `alaa-performance-profiler` only with a measurable question and a baseline or budget; `alaa-observability-reviewer` for new failure modes and distributed behavior; `alaa-release-guardian` for CI/CD, container, configuration, dependency, or release changes.
3. Spawn `alaa-adversarial-reviewer` only when the change is irreversible or high blast radius — production data movement, auth or tenancy boundaries, public contract breaks, deployment topology — or when the reviewer and a specialist reach conflicting verdicts. It is a second independent lens, not a second opinion on a routine change, and its findings are reported to the user rather than fed into another fix cycle.
4. Reviewer verdict handling: `APPROVED` proceeds; `APPROVED-WITH-NITS` proceeds while reporting nits, fixing only in-scope low-risk ones; `CHANGES-REQUESTED` routes blocker and major findings verbatim to the owning lane, with a maximum of two review-fix cycles unless the user explicitly authorizes more.
5. Specialist blocker and major findings are gates equal to reviewer findings. Conflicting specialist opinions are reconciled by the lead using repository evidence; unresolved high-risk conflicts are surfaced to the user.

### Phase E — Documentation and final validation

1. Spawn `alaa-documenter` only when shipped behavior, API, configuration, operations, troubleshooting, or upgrade instructions changed.
2. After documentation edits, run applicable docs formatting, link, example, and scope checks. Documentation is the final write lane and must not bypass validation.
3. Invoke `/alaa-extract-agent-lessons` for the final full-engagement gate after the evidence is stable. Reconcile intermediate candidates, publish only authorized durable knowledge through `/alaa-memory-os`, and accept an empty retained set as a valid result. If it returns `pipeline reopen required`, follow the gate-reopen rule in `references/verification-and-gates.md` before rerunning this final gate.
4. Re-check final git status and diff against declared scopes.
5. Final report order: outcome and final verdict; changes by lane and touched files; verification commands with observed results; review and specialist verdicts with the resolution of each finding; documentation outcome; reusable-context curation outcome, including persisted, deferred, or empty; residual risks, skipped checks, and follow-ups; and the agent roster — every subagent dispatched this goal, one line each with agent name, pinned model and effort, its self-reported AGENT/MODEL/EFFORT identity line flagging any mismatch, and for every escalated lane the named criterion that earned it. Audit every claim against an actual tool result from this session before reporting it.

## 6. Advisor-mode output

Provide: grounded repository findings; a lane plan with dependencies and gates; one ready-to-run prompt per lane using the templates; recommended agent, model, and effort per lane; a verification plan and resource policy; and the risks, assumptions, and decisions that require the user. Do not edit files or imply implementation occurred.

## 7. Verification and resource rules

- After any change to `agents/`, run `python scripts/check_agent_grants.py`; exit `0` is clean, exit `1` means grant findings, and exit `2` means the checker could not run. Both `1` and `2` fail completion. Run `python scripts/check_agent_grants.py --self-test` when changing the checker itself; it must exit `0` after proving every red fixture is rejected. `scripts/validate_pack.py` invokes the normal grant check automatically.
- Exact command semantics come from repository guidance and the dispatch. Never invent a flag merely to make a check pass.
- Lowering process priority is mandatory for declared CPU-heavy local commands; limiting runner-level parallelism is separate and must also be explicit.
- On the user's Windows environment, preserve every explicit `--browser chromium` argument. Never remove, replace, or change it without prior user approval.
- Do not kill unrelated services, dev servers, containers, or processes; do not start duplicate services when a reusable declared service exists.
- Do not update snapshots, golden files, lockfiles, generated clients, dependencies, or migrations during verification unless that change is an explicitly scoped implementation lane.

Read `references/resource-policy.md` for runner usage and ecosystem examples. Read `references/failure-taxonomy.md` when a check fails.

## 8. Safety and authority

- Repository-local, reversible edits inside declared scopes may proceed in orchestrator mode.
- Ask before destructive Git operations, force pushes, history rewrites, deployment, publishing, production access, data deletion, credential changes, shared-system configuration changes, or irreversible migrations.
- Auto-install authority is limited to this pack's named agent files under `~/.claude/agents` and their backups. It does not authorize editing settings, hooks, other skills, or unrelated agents.
- A lane's code-intelligence grant lives in its agent file, not in the dispatch. `references/agent-catalog.md` records which agents hold CodeGraph, the Serena read set, both, or neither; `/alaa-code-intelligence-routing` owns why. Reinstalling this pack restores those grants, so change them here rather than in `~/.claude/agents`.
- Never commit unless requested. Never add Co-Authored tags.
- Never expose secrets in prompts, logs, artifacts, or reports.

## 9. Stop conditions

Stop successfully only when every acceptance criterion has evidence, mandatory gates passed, the final diff scope is clean, documentation was completed or explicitly skipped, and the final reusable-context gate reported what was persisted, deferred, rejected, or absent.

Stop and report a partial or blocked state when: the same lane is blocked twice by the same cause; blocker or major findings remain after two fix cycles; verification remains flaky, timed out, contaminated, or environment-blocked; scope expands beyond the goal; an irreversible or product decision belongs to the user; or a safe execution path no longer exists.

## 10. Anti-patterns

- spawning every specialist for every task, or several agents for one lane;
- delegating work the lead could finish in a handful of tool calls;
- spawning a subagent to double-check another subagent, or adding "verify your work" instructions the lead already honors;
- treating the verifier and reviewer gates as redundancy and skipping them because the work already looks checked — they are authority boundaries;
- using a reviewer as a fixer, a verifier as a debugger, or a researcher as a decision-maker;
- telling a lane to use a code-intelligence server its agent file does not grant, or widening the grant inside a dispatch instead of in the agent file;
- the lead running heavy test suites or implementing while lanes are viable;
- allowing documentation to describe intended rather than observed behavior;
- treating a rerun that passes after a failure as a clean pass;
- parallelizing migrations, generated contracts, or shared-state edits;
- using model tier as a substitute for repository evidence;
- escalating a lane's model because the goal is important or the surface is sensitive, instead of because the lane meets a named escalation criterion — importance and sensitivity are handled by gates, not tier;
- dispatching the escalated implementer for CRUD, plumbing, configuration, test-writing, or mechanical application of ratified values;
- raising a Sonnet lane to `xhigh` instead of changing the model, or pinning any agent at `max`;
- routing the adversarial reviewer's findings into another fix cycle instead of reporting them;
- pre-loading every clean-code skill into every lane — name only the lane's matching skill.
