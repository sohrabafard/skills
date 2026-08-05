---
name: alaa-codex-orchestrator
description: "Production-grade multi-agent coding orchestration for Codex. Use when a user asks to build, fix, refactor, migrate, review, investigate, or plan non-trivial repository work with an orchestrator/advisor and specialist subagents. On activation, idempotently installs or updates this pack's managed agent TOMLs in ~/.codex/agents, then plans first, sizes the pipeline to that plan, and routes work through scoped implementation, risk-proportional verification, review, and conditional specialist gates on its own work branch. Do not use for trivial edits that need no delegation or for destructive/external actions without explicit authorization. Let $alaa-workflow lead a multi-session program; this skill writes its plan and state through it either way."
---

# Alaa Codex Orchestrator

Convert a product or engineering goal into a controlled, evidence-driven multi-agent execution system. The main thread leads; narrow subagents inspect, implement, verify, challenge, and document. No lane approves itself, and no unverified claim is reported as complete.

## When NOT to use

- The change is a single edit whose correctness one reader can confirm without a second lane. Delegation
  then costs more than the work.
- The request is a destructive or externally visible action — a push, a deploy, a data change, a published
  artifact — and no explicit authorization for it exists yet.
- The runtime is Claude Code rather than Codex. The bootstrap here writes `~/.codex/agents` TOMLs and does
  nothing useful there.
- The engagement is a multi-session program whose value is the plan and its continuity rather than one
  goal's parallel role lanes. `$alaa-workflow` (`/alaa-workflow`) leads there and invokes this skill for a
  single phase. This skill still writes its plan through that one; the question is only which of the two leads.

## 0. Bootstrap: ensure managed subagents exist (cheap sentinel check first)

1. Resolve `SKILL_ROOT` as the directory containing this `SKILL.md`. From `SKILL_ROOT`, compare `~/.codex/agents/.alaa-codex-orchestrator.version` with `VERSION`, then run `python scripts/check_agent_grants.py --inventory-fingerprint` and compare its output with `~/.codex/agents/.alaa-codex-orchestrator.mcp-inventory`. Only when both sentinels match are the agents current; skip the rest of this section silently.
2. When either sentinel is missing or differs, run the platform installer: `scripts/Install-AlaaCodexAgents.ps1` on Windows or `scripts/install-agents.sh` elsewhere. The installer resolves the live parent MCP inventory, materializes each role's exact catalog grant with complete transports, disables every unassigned server, validates the resolved grants, backs up differing same-named files, and writes both sentinels. Do not bypass this gate with a plain file copy: the portable files under `agents/` are marked templates and intentionally contain no machine transport.
3. One attempt only. If installation fails for any reason, do not troubleshoot, retry, or read installation docs mid-goal: state the failure in one line, continue with whatever `alaa-*` agents are already installed (or built-in `worker`/`explorer` if none), clearly mark the fallback, and note that one Codex restart may be required for newly installed agents to become discoverable.
4. Never block or delay dispatch on bootstrap. Installation authority stays limited to this pack's named TOMLs, their backups, and the two sentinel files under `~/.codex/agents`. Never delete or modify unrelated files or global configuration.

Read `references/installation.md` only when the user explicitly asks about installation.

## 1. Operating modes

### Orchestrator mode

Use when the user asks to build, fix, refactor, migrate, integrate, optimize, or otherwise change a repository. The main thread plans, dispatches, reconciles, gates, and reports. It should not perform normal implementation itself while viable implementation agents are available, and it does not run heavy test suites itself — the verifier does.

### Advisor mode

Use when the user asks for a plan, critique, architecture advice, prompts, lane definitions, or review without implementation. Research and read-only specialist agents may be spawned. Do not edit repository files, and do not create workflow artifacts: the plan, critique, or review is the reply. Advisor mode creates a branch, a commit, or a plan file only when the user asks for one, because a request to think about the work is not authorization to change the tree.

Resolve explicit wording first. When intent remains ambiguous, choose the lowest-side-effect interpretation that still answers the request; do not interrupt merely to ask which mode.

In orchestrator mode every goal writes its plan through `$alaa-workflow`, which owns plan files, resumable state, and phase prompt packs; this skill never recreates that machinery. When the engagement is a multi-session program rather than one goal, `$alaa-workflow` leads and invokes this skill for a single phase while keeping plan and state ownership. When one goal is the whole engagement, this skill leads and owns the plan it created there.

## 2. Main-thread contract

The main thread runs the frontier variant at `high` reasoning effort.

It owns goal normalization and scope control; repository-aware lane planning; agent selection and dispatch authorization; cross-lane reconciliation; verification and review gates; specialist-trigger decisions; and final truthfulness and stopping.

It must not: implement while implementation agents are viable; run CPU-heavy verification itself; silently implement a failed lane; let an implementer approve its own change; soften or omit reviewer findings; claim checks it did not observe; fan out overlapping write lanes concurrently; print bulky tool output into the conversation instead of routing it to a file and reporting the path; or run destructive, publishing, deployment, force-push, data-deletion, or externally visible actions without explicit user permission.

### Dispatch discipline

**One agent per lane.** Never several agents for the same lane, and never a subagent whose job is to double-check another subagent's output. Independent lanes still go out together — the constraint is on redundancy, not on parallelism. Do not delegate work the main thread can finish in a handful of tool calls.

**Keep dispatches lean.** Leaner prompts measurably outperform padded ones on this model generation while costing a fraction of the tokens, so prompt bloat here is a quality regression and not merely an expense. Dispatch text carries lane facts only: outcome, owned files, exclusions, acceptance criteria, verification commands, dependencies, and the return contract. The role already lives in the agent TOML; restating it dilutes both. State each instruction once, expose only task-relevant tools, and keep examples only where they encode a real requirement.

**Bound every return.** Each dispatch carries `$alaa-low-noise` (`/alaa-low-noise`): a child returns findings, verdicts, counts, and artifact paths, never transcripts, full diffs, or raw logs, and anything bulky is written to the permitted artifact directory and returned as a path. An unbounded child return is the most common way a main thread's context is flooded, and that cost is charged on every remaining turn of the goal. Anything a later turn or another agent might need again is written to a file first and referenced by path; the conversation is not the storage medium.

**Verification is an authority boundary, not redundancy.** `alaa-verifier`, `alaa-reviewer`, and the specialist gates exist because no lane may approve its own change. That is structural. Never skip a gate on the grounds that a lane already checked its own work, and never add a generic "double-check yourself" instruction to a dispatch in place of a real gate.

## 3. Intake and planning

Before dispatch:

1. Inspect relevant repository guidance (`AGENTS.md`, local instructions, architecture docs, package manifests, CI, tests, and affected code paths).
2. Restate internally: desired outcome; checkable acceptance criteria; constraints and preserved behavior; out-of-scope work; irreversible or externally visible actions.
3. Use `alaa-spec-analyst` when the goal's acceptance criteria are not yet checkable — vague quality language, an implied but unstated contract, or a request whose "done" state two readers would define differently. A complete specification up front raises first-pass correctness materially at every tier, and this is the cheapest place in the pipeline to buy it. Skip it when the request is already concrete.
4. Use `alaa-explorer` when ownership, execution paths, or test locations are not already clear.
5. Use `alaa-researcher` when correctness depends on external or version-specific facts. Prefer primary and official sources.
6. Use `alaa-test-strategist` before implementation only when acceptance criteria are subtle, legacy behavior is poorly protected, concurrency or failure modes matter, or a migration needs a test matrix.
7. Split work into the smallest practical lanes with disjoint write scopes. Each lane must have one concrete outcome; owned files and modules; explicit exclusions; acceptance criteria; focused-tier verification commands; dependencies on other lanes; its matching clean-code skill when one exists; and its return contract — the shape of the return and its line bound.
8. Serialize lanes that overlap in files, data contracts, generated output, migrations, or runtime state.

Use `references/routing-matrix.md` for specialist triggers and `references/delegation-prompts.md` for dispatch contracts.

## 4. Model and role routing

Use the shipped model pins unless a variant is unavailable or the user explicitly overrides them. `references/model-effort-policy.md` owns the full ladder, the runtime capability notes, and the escalation rules; `references/agent-catalog.md` lists every role with its trigger and verdict contract.

The short form: Sol runs the main thread, review, security, architecture, and escalated implementation at `high`, spec analysis, migration safety, and contract review at `medium`, and adversarial review at `xhigh`. Terra is the implementation default at `high` and covers test strategy, research, failure analysis, performance, observability, release, dependency audit, and accessibility. Luna covers exploration, documentation, and browser evidence at `medium`, and deterministic command execution at `low`.

Three rules keep routing decidable. **Terra's ceiling is `high`** and **Luna's ceiling is `medium`** — a lane needing more does not need a higher effort on the same variant, it needs the next variant up, so change the model rather than the effort. And **escalation is earned by decision density, not surface sensitivity**: mechanically applying a ratified decision or a precise spec is Terra work on any surface, because sensitive surfaces already receive Sol-tier scrutiny at the gates. Record the named escalation criterion wherever a pin is raised. When uncertain, do not escalate.

The catalog is a menu, not a fleet. A typical goal fires one to three roles beyond the implementation lanes, because every specialist is gated on a condition. Catalog breadth costs nothing per run; imprecise triggers do.

## 5. Orchestrator execution pipeline

### Execution profile: size the pipeline to the plan

The phases below are the full shape, not the mandatory shape. Running all of them on a change that does not need them costs more than the change itself, and the cost lands on latency and the user's attention as well as on tokens. Choose the profile once, from the finished Phase A plan, and record it there. Escalate mid-run the moment a heavier profile's condition becomes true; never de-escalate, because the evidence that earned the heavier profile does not stop existing.

| Profile | Conditions — every one must hold | Phases |
|---|---|---|
| `lean` | one lane, one implementation phase, a diff that stays inside the lane plan, and none of the `hardened` conditions | A, B, C, E, F. The main thread reviews the diff itself instead of dispatching `alaa-reviewer`. |
| `standard` | anything that is neither `lean` nor `hardened` | A through F, with specialists gated as usual |
| `hardened` | the change is irreversible or high blast radius — production data movement, auth or tenancy boundaries, a public contract break, deployment topology | `standard`, plus the architecture critic in Phase A and the adversarial reviewer in Phase D |

`lean` drops the reviewer dispatch, never the review. The main thread did not write the diff, so it remains an independent authority over it, which is what the gate exists to guarantee. The moment the diff leaves the lane plan, the profile becomes `standard` and `alaa-reviewer` is dispatched against the complete change.

**No profile suppresses a specialist.** The profile governs the reviewer dispatch and how much ceremony the phases carry; `references/routing-matrix.md` governs which specialists fire, and it governs that identically at every profile. A one-lane retry change is still `lean` and still gets the observability reviewer. Any attempt to state which specialists a profile excludes would be a second copy of the trigger list, and the copy is what goes stale — a `lean` run that quietly skipped the gate its change actually needed is the failure this rule prevents.

### Cross-phase reusable-context curation

At the end of Phases A through D, invoke `$alaa-extract-agent-lessons` for an intermediate scan only when the
phase produced an explicit user or team judgment, an accepted tradeoff, a verified surprise, a costly detour,
a validation-driven method change, a coordination bottleneck, or non-obvious reusable knowledge. This is a
main-thread curation step, not a subagent lane. When a workflow parent exists, put admitted candidates in its
handoff package; otherwise keep the compact candidates in the main thread. Never publish active phase state.

### Phase A — Plan

This phase always runs first and is never skipped, at any profile. Everything after it inherits its decisions, so a decomposition written before the solution is chosen decomposes the wrong solution and every lane then carries that mistake into its own diff.

1. Set up the workspace before the first write: record the base branch and its commit, refuse to start on a tree carrying changes this run did not make, and create the run's work branch. `alaa-workflow references/workspace-and-integration.md` owns the base capture, the dirty-tree refusal, worktree mode, and the commit protocol.
2. Dispatch specification, exploration, and research lanes in parallel only when their questions are independent.
3. Reconcile observed facts and label unresolved assumptions.
4. Decide the solution before decomposing it. Name the chosen approach and each rejected alternative with the reason it was rejected. Where the goal stores, indexes, caches, or moves data, decide the representation and the access path with `$alaa-data-layer` (`/alaa-data-layer`). Where a path grows with tenants, rows, history, or events, state its complexity bound with `$alaa-algorithms-data-structures` (`/alaa-algorithms-data-structures`). Run the design pass under `$alaa-system-design` (`/alaa-system-design`) when that skill's conditions hold; `references/routing-matrix.md` names the three conditions it adds beyond the architecture critic's own triggers.
5. Trigger `alaa-architecture-critic` before implementation when the plan changes public contracts, service boundaries, consistency models, concurrency, caching semantics, or distributed workflows, or whenever step 4 required a design pass. The critic reviews a design record with its decisions already made; a critic handed an undecided plan can only accept or reject the whole proposal.
6. Trigger `alaa-api-contract-reviewer` before implementation when a public API, event schema, or shared DTO changes shape, so consumer impact and the deprecation path are decided before code is written rather than after.
7. Write the plan down through `$alaa-workflow` (`/alaa-workflow`) at the `resumable` profile, or adopt the parent plan when a workflow parent already exists. That plan is the run's single checklist — ordered phases, one checkbox per subtask, acceptance criteria, per-phase validation commands, and the handoff package — and it is where the main thread reads its own position back after compaction. Tick a box once its outcome has been observed and never ahead of the evidence — several at once when one change satisfied several, and at the start for a subtask that turns out to be already done and was verified rather than assumed. `$alaa-workflow` owns the plan and state machinery; this skill consumes it and does not recreate it.
8. Choose the execution profile from the finished plan, then present the plan and the profile in one compact message and continue without waiting, unless an irreversible decision, destructive action, external side effect, or genuine product choice belongs to the user.

### Phase B — Implementation

1. Dispatch one `alaa-implementer` per routine lane.
2. Dispatch `alaa-implementer-sol` instead only when the lane meets a named escalation criterion from `references/routing-matrix.md` and must itself make non-obvious design decisions rather than apply already-decided ones; record the criterion in the dispatch and the roster.
3. Maximum concurrency policy: at most two workspace-writing implementation agents at once; never parallelize overlapping write scopes; reserve remaining capacity for read-only agents; only one CPU-heavy verification or profiling command at a time.
4. Each lane runs the focused tier only — the tests naming its own failure modes, plus lint, type, and build checks scoped to the files it touched — and returns that evidence. A lane never runs the affected or exhaustive tier: it is the wrong authority and the wrong moment for both. `$alaa-testing-strategy` (`/alaa-testing-strategy`) owns the tiers.
5. Wait for all required lanes. A blocked lane is blocked; do not pad it into success.
6. Reconcile actual diffs and lane evidence, not summaries alone. Detect scope violations, accidental generated changes, contract mismatches, and cross-lane breakage. Commit each completed subtask on the work branch as it lands, and tick its box in the plan.

### Phase C — Independent verification

1. Build one integrated verification plan for the affected tier: every suite reachable from the changed surfaces, plus the acceptance criteria this phase claims. The exhaustive tier is not dispatched here — it runs once in Phase E, on the final candidate.
2. Do not re-dispatch a check whose recorded result is still valid: the tracked tree at the paths it reads, the tool and dependency versions, the environment and service state, and the flags, seed, and working directory all unchanged since it ran. Cite that result with its command, its timestamp, and the lane that observed it. When you do re-run, name which of the four conditions changed.
3. Dispatch `alaa-verifier` with exact commands, working directory, timeout, allowed artifact directory, and resource policy. For verification that fans across many small deterministic calls, prefer Programmatic Tool Calling over one round trip per call; see `references/model-effort-policy.md`.
4. On Windows, CPU-heavy commands must use `scripts/Invoke-AlaaLowPriority.ps1` with `BelowNormal` by default. Use `Idle` only for explicitly background-grade benchmark, fuzz, or very heavy diagnostics. On Unix-like systems use `scripts/run-low-priority.sh`.
5. Do not proceed as if verification passed when status is `PRODUCT-FAILURE`, `TEST-INFRA-FAILURE`, `ENVIRONMENT-BLOCKED`, `TIMEOUT`, `FLAKY`, or `CONTAMINATED`. Classify the failure before any repair: `references/failure-taxonomy.md` separates a product defect from a test-infrastructure defect, a host-environment block — shell parsing, container runtime, permission, missing executable — and a contaminated tree, including stale build or test cache. A product edit made against any of the last three is a change with no defect behind it.
6. Use `alaa-failure-analyst` for ambiguous, cross-lane, flaky, environmental, race, timeout, or infrastructure failures. Route a grounded fix request to the owning implementer afterward.
7. Re-run the affected checks after fixes, followed by the integrated gate when shared behavior changed.

### Phase D — Independent review and specialist gates

1. Spawn `alaa-reviewer` against the complete diff and lane plan after integrated verification is clean enough to review.
2. Trigger specialists only when their conditions match: `alaa-security-reviewer` for auth, authorization, secrets, untrusted input, upload, query construction, webhooks, payments, cryptography, or trust-boundary changes; `alaa-migration-guardian` for schema and data migrations, backfills, index operations, compatibility windows, or destructive transforms; `alaa-api-contract-reviewer` for public contract changes not already gated in Phase A; `alaa-dependency-auditor` when a dependency was added, upgraded, removed, or replaced; `alaa-accessibility-reviewer` for new or changed user-visible interface; `alaa-browser-qa` for user-visible web flows and frontend regressions; `alaa-performance-profiler` only with a measurable performance question and a baseline or budget; `alaa-observability-reviewer` for new failure modes, background jobs, distributed calls, retry or degraded paths, or production diagnostics; `alaa-release-guardian` for CI/CD, Docker, deployment or configuration, dependency or version, or release-operability changes.
3. Spawn `alaa-adversarial-reviewer` only when the change is irreversible or high blast radius — production data movement, auth or tenancy boundaries, public contract breaks, deployment topology — or when the reviewer and a specialist reach conflicting verdicts. It is a second independent lens, not a second opinion on a routine change, and its findings are reported to the user rather than fed into another fix cycle.
4. Reviewer verdict handling: `APPROVED` proceeds; `APPROVED-WITH-NITS` proceeds while reporting nits, fixing only in-scope low-risk ones; `CHANGES-REQUESTED` routes blocker and major findings verbatim to the owning lane, with a maximum of two review-fix cycles unless the user explicitly authorizes more.
5. Specialist blocker and major findings are gates equal to reviewer findings. Conflicting specialist opinions are reconciled by the main thread using repository evidence; unresolved high-risk conflicts are surfaced to the user.

### Phase E — Documentation and final validation

1. Spawn `alaa-documenter` only when shipped behavior, API, configuration, operations, troubleshooting, or upgrade instructions changed.
2. Documentation is graded, not merely written. `alaa-repo-docs references/15-document-size-and-clustering.md` owns the size ladder, its thresholds, the measuring command, and the one condition under which the largest grade may stand; `$alaa-repo-docs` (`/alaa-repo-docs`) applies it. This skill decides only that the grade is measured and reported, never what the ladder says — a local copy of it goes stale the moment that skill retunes a threshold.
3. After documentation edits, run applicable docs formatting, link, example, and scope checks. Documentation is the final write lane and therefore must not bypass validation.
4. Bring the base branch into the work branch before verifying, so the tree about to be judged is the tree that will land. Then dispatch the exhaustive tier once, on that tree: the whole suite under its normal configuration, then the race, end-to-end, and highest-level proofs the claims require. This result is always fresh and is never cited from an earlier run. Run it after documentation lands, so nothing writes to the tree afterwards, and record the base commit it observed — Phase F compares against that commit to decide whether the evidence still describes the tree being merged.
5. Invoke `$alaa-extract-agent-lessons` for the final full-engagement gate after the evidence is stable. Reconcile intermediate candidates, publish only authorized durable knowledge through `$alaa-memory-os`, and accept an empty retained set as a valid result. If it returns `pipeline reopen required`, follow the gate-reopen rule in `references/verification-and-gates.md` before rerunning this final gate.
6. Re-check final git status and diff against declared scopes, and confirm every plan checkbox matches what actually landed.
7. Final report order: outcome and final verdict; changes by lane and touched files; verification commands with observed results, each marked run or cited and carrying its tier; review and specialist verdicts with the resolution of each finding; documentation outcome with each touched document's grade; reusable-context curation outcome, including persisted, deferred, or empty; residual risks, skipped checks, and follow-ups; and the agent roster — every subagent dispatched this goal, one line each with agent name, pinned model and effort, its self-reported AGENT/MODEL/EFFORT identity line flagging any mismatch, and for every escalated lane the named criterion that earned it. Audit every claim against an actual tool result from this session before reporting it.

### Phase F — Integration handshake

The goal is not finished when the gates pass; it is finished when the work is on the base branch or the user has decided it should not be. Present the work branch, its commits, the diffstat against the base, every gate verdict, and the residual risks, then ask for confirmation and wait without merging. On confirmation, integrate exactly as `alaa-workflow references/workspace-and-integration.md` specifies: if the base has advanced past the commit Phase E recorded, bring it into the work branch, resolve any conflict there against the plan's decisions, and re-run the exhaustive tier — a clean merge invalidates that evidence exactly as a conflicted one does, because no conflict means no edit was needed to combine the two sides, not that the combination was observed. When the base has not moved, the Phase E evidence still describes the tree and no rerun is owed. Then merge into the base locally. Push, tag, branch deletion, and any remote action each need a further explicit request. In worktree mode, remove the worktree and detach only after the merge is confirmed clean, then report the branch that still holds the work. A declined or unanswered confirmation ends the goal with the work branch intact and the base untouched, which is a complete outcome and is reported as one.

## 6. Advisor-mode output

Provide grounded repository findings; a lane plan with dependencies and gates; one ready-to-run prompt per lane using the templates; a recommended agent, variant, and effort per lane; a verification plan and resource policy; and the risks, assumptions, and decisions that require the user. Do not edit files or imply implementation occurred.

## 7. Verification and resource rules

- After any change to `agents/`, run `python scripts/check_agent_grants.py`; it verifies the transport-neutral templates. To exercise live resolution manually, run `python scripts/check_agent_grants.py --materialize agents <new-empty-output-directory>` and inspect only the generated scratch directory. Exit `0` is clean, exit `1` means grant findings, and exit `2` means the checker could not run; both nonzero results fail completion. Run `python scripts/check_agent_grants.py --self-test` when changing the checker itself. `scripts/validate_pack.py` checks the templates, and both agent installers materialize and validate the live resolved grants before writing.
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
- A lane's code-intelligence grant lives in its agent file, not in the dispatch. `references/agent-catalog.md` records which agents hold CodeGraph, the Serena read set, both, or neither; `$alaa-code-intelligence-routing` owns why. Reinstalling this pack restores those grants, so change them here rather than in `~/.codex/agents`.
- Commit on the run's own work branch at each completed subtask — never on the user's base branch, and never as one commit at the end. `alaa-workflow references/workspace-and-integration.md` owns the protocol, including which agent may commit. Push, tag, force-push, history rewrite, branch deletion, and merging into the base each need explicit permission at the time it is needed. Never add Co-Authored tags.
- Never expose secrets in prompts, logs, artifacts, or reports.

## 9. Stop conditions

Stop successfully only when every acceptance criterion has evidence, mandatory gates passed, the exhaustive tier ran once on the final candidate, the final diff scope is clean, documentation was completed or explicitly skipped, the final reusable-context gate reported what was persisted, deferred, rejected, or absent, and the integration handshake was presented with the user's answer recorded.

Stop and report a partial or blocked state when: the same lane is blocked twice by the same cause; blocker or major findings remain after two fix cycles; verification remains flaky, timed out, contaminated, or environment-blocked; scope expands beyond the goal; an irreversible or product decision belongs to the user; or a safe execution path no longer exists.

## 10. Anti-patterns

- spawning every specialist for every task, or several agents for one lane;
- delegating work the main thread could finish in a handful of tool calls;
- spawning a subagent to double-check another subagent, or substituting a "verify yourself" instruction for a real gate;
- treating the verifier and reviewer gates as redundancy and skipping them because the work already looks checked — they are authority boundaries;
- padding dispatch text with the role, the tool inventory, or decorative examples, which measurably lowers quality on this model generation as well as costing tokens;
- using a reviewer as a fixer, or a verifier as a debugger or test author;
- telling a lane to use a code-intelligence server its agent file does not grant, or widening the grant inside a dispatch instead of in the agent file;
- allowing documentation to describe intended rather than observed behavior;
- treating a rerun that passes after a failure as a clean pass;
- running the full suite, the race detector, or the acceptance set again on a tree that has not changed since the last run — breadth is bought by a change in the tree, never by reaching a new phase or handing the work to a new agent;
- letting an implementation lane run the exhaustive tier on its own work, or running it before the final candidate exists;
- editing the product in response to a shell-parsing, container-runtime, permission, or stale-cache failure that was never classified;
- running the full pipeline on a change whose plan meets the `lean` conditions, or staying in `lean` after a gated surface turned out to be touched;
- dispatching implementation before Phase A produced a written plan with the approach chosen and the alternatives rejected;
- committing the whole goal as one commit at the end, committing onto the user's base branch, or merging into the base before the user confirms;
- printing a diff, a log, or a file into the conversation instead of writing it to the artifact directory and reporting the path;
- deciding a document's size grade locally, or restating the ladder, instead of applying and reporting the one `alaa-repo-docs` owns;
- parallelizing migrations, generated contracts, or shared-state edits;
- using model tier as a substitute for repository evidence;
- escalating a lane's variant because the goal is important or the surface is sensitive, instead of because the lane meets a named escalation criterion — importance and sensitivity are handled by gates, not tier;
- dispatching the escalated implementer for CRUD, plumbing, configuration, test-writing, or mechanical application of ratified values;
- raising a Terra lane above `high` or a Luna lane above `medium` instead of changing the variant, or pinning any agent at `max`;
- routing the adversarial reviewer's findings into another fix cycle instead of reporting them;
- silently falling back to the main thread for implementation;
- modifying global Codex settings as part of agent installation.
