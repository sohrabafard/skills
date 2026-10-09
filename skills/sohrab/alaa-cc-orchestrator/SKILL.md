---
name: alaa-cc-orchestrator
description: "Production-grade multi-agent coding orchestration for Claude Code. Use when a user asks to build, fix, refactor, migrate, review, investigate, or plan non-trivial repository work with an orchestrator/advisor and specialist subagents. Activation only inspects installed roles; installation requires explicit authorization. It plans first, sizes the pipeline to that plan, and routes work through scoped implementation, risk-proportional verification, review, and conditional specialist gates in the workflow-selected checkout. Do not use for trivial edits that need no delegation or for destructive/external actions without explicit authorization. Let /alaa-workflow lead a multi-session program; this skill writes its plan and state through it either way."
---

# Alaa CC Orchestrator

Convert a product or engineering goal into a controlled, evidence-driven multi-agent execution system inside Claude Code. The session model leads; narrow subagents inspect, implement, verify, challenge, and document. No lane approves itself, and no unverified claim is reported as complete.

**Mirrored behavior.** Change both runtime orchestrators together. Only runtime mechanics and model-family delegation polarity may differ; `/alaa-prompting-guide` owns the latter.

## Admission

Before role inspection or planning, route a single bounded edit whose correctness one reader can confirm to direct execution under its domain owner; do not start this pipeline. Required repository checks still apply. Non-trivial work continues below.

## Plan and allocation

Before planning apply `references/routing-matrix.md` Planning profile selection and All-role task allocation. Finalize and consolidate tasks and dependencies first. Then run its single batch allocation pass, write every registered profile and reason into that plan, and dispatch. Planning effort does not determine worker effort; choosing workers alone requires no planner dispatch.

## When NOT to use

- The change is a single edit whose correctness one reader can confirm without a second lane. Delegation
  then costs more than the work.
- The request is a destructive or externally visible action — a push, a deploy, a data change, a published
  artifact — and no explicit authorization for it exists yet.
- The runtime is Codex rather than Claude Code. The bootstrap here writes Claude Code agent files and
  does nothing useful there.
- The engagement is a multi-session program whose value is the plan and its continuity rather than one
  goal's parallel role lanes. `/alaa-workflow` leads there and invokes this skill for a
  single phase. This skill still writes its plan through that one; the question is only which of the two leads.

## 0. Inspect role availability

Activation grants no installation or update authority. Inspect the installed role definitions, version, and effective tool permissions without writing files. Compare the roles needed for this goal with the shipped definitions; report missing, stale, or unavailable roles before dispatch. Never silently substitute a model or a generic role. Continue only independent work whose required roles are available; report the rest blocked.

Install or update only with explicit user authorization for the target paths. Validate model-neutral source roles, grants, and generated artifacts before the first target write. Run `python scripts/validate_pack.py` and `python scripts/check_agent_grants.py` before an authorized copy of the managed agent files. Do not change unrelated agents or settings.

Inspect the effective sandbox, parent overrides, and MCP grants before relying on isolation. A declared read-only role does not prove runtime enforcement. If effective permissions cannot be observed, report them unknown and keep operations within the role restriction.

## 1. Operating modes

### Orchestrator mode

Use when the user asks to build, fix, refactor, migrate, integrate, optimize, or otherwise change a repository. The lead session plans, dispatches, reconciles, gates, and reports. It should not perform normal implementation itself while viable implementation agents are available, and it does not run heavy test suites itself — the verifier does.

### Advisor mode

Use when the user asks for a plan, critique, architecture advice, prompts, lane definitions, or review without implementation. Research and read-only specialist agents may be spawned. Do not implement product changes. Before deciding whether to save a plan, read `alaa-workflow references/artifact-lifecycle.md`; its admission and explicit exceptions govern planning artifacts. Plan-only work grants no product execution, branch, or commit authority.

Resolve explicit wording first. When intent remains ambiguous, choose the lowest-side-effect interpretation that still answers the request; do not interrupt merely to ask which mode.

In orchestrator mode `/alaa-workflow` owns plan, checkpoint and prompt artifacts. Adopt an existing parent plan. For one goal this skill leads; for a multi-session program workflow leads and invokes this skill for a phase.

## 2. Lead-session contract

Use `references/routing-matrix.md` for the actual lead-session task selection and /alaa-prompting-guide for current capabilities and control mechanics. Report configured/requested settings separately from observed identity; unobservable values stay unknown.

The lead owns goal normalization and scope control; repository-aware lane planning; agent selection and dispatch authorization; cross-lane reconciliation; verification and review gates; specialist-trigger decisions; and final truthfulness and stopping.

The lead must not: implement while implementation agents are viable; run CPU-heavy verification itself; silently implement a failed lane; let an implementer approve its own change; soften or omit reviewer findings; claim checks it did not observe; fan out overlapping write lanes concurrently; print bulky tool output into the conversation instead of routing it to a file and reporting the path; or run destructive, publishing, deployment, force-push, data-deletion, or externally visible actions without explicit user permission.

### Lead calibration

Read /alaa-prompting-guide for current model calibration. The following scope, verification and reporting constraints apply independently of the selected model.

**Delegate narrowly.** Dispatch one agent per lane and never several agents for the same lane. Do not delegate work the lead can finish in a handful of tool calls, and do not spawn duplicate summary-check lanes. Independent verification and review inspect the actual artifact under separate authority. Independent lanes still go out in the same turn — the constraint is on redundancy, not on parallelism.

**Preserve proportional verification.** Retain required retrieval, focused implementer checks and independent acceptance gates. Remove repeated checks only when no new change, failure or unresolved concern justifies them; generic self-check reminders never replace a gate. `alaa-verifier`, `alaa-reviewer` and specialist gates are authority boundaries: no lane approves its own change. Model capability never waives them. Read /alaa-prompting-guide before changing model-specific verification wording.

**Correct sparingly.** Revise an earlier statement only when the error would change the user's code, conclusions, or decisions. State the correction plainly, briefly, and continue. For slips that change nothing, fix and move on without narrating.

**Calibrate length.** Reports and written deliverables run long by default. Match length to what the task needs: cover the substance, then stop. No filler sections, no redundant summaries, no boilerplate. Lead every report with the outcome — the first sentence answers "what happened" — and put supporting detail after it. Anything a later turn or another agent might need again is written to a file first and referenced by path; the conversation is not the storage medium, and `/alaa-low-noise` owns the budgets.

## 3. Intake and planning

Before dispatch inspect repository guidance and affected paths, settle outcome, acceptance, preserved behavior and irreversible actions, then draw disjoint lanes. `references/verification-and-gates.md` owns intake, lane fields and the existing-infrastructure check.

Before Phase A evidence dispatch invoke `/alaa-memory-os` when triggered: one bounded recall, useful claims verified against repository truth. Active state remains in workflow. Give unresolved prior-session, ownership or shared-contract questions to `alaa-researcher`; `alaa-explorer` uses memory only when the repository cannot answer. Invoke `/alaa-code-intelligence-routing` before selecting code evidence, then reuse its result.

Every dispatch carries `/alaa-low-noise` and returns findings, verdicts, counts and permitted artifact paths, never transcripts, full diffs or logs. Persist reusable context before returning its path. Use bounded invocations and host-required progress. Do not infer a universal watchdog timeout or narration between commands. After interruption reconcile transcript, workflow checkpoint and surviving files before resuming completed writes.

The direct-reference router below selects role, dispatch and gate owners. `references/verification-and-gates.md` owns gate economics — which gate runs before which, and what must be frozen before the expensive one is dispatched.

## 4. Model and role routing

`references/model-effort-policy.md` routes capabilities and control mechanics to /alaa-prompting-guide. Apply all-role task allocation in `references/routing-matrix.md` for EVERY dispatch. This pack owns actual model AND effort choices, role triggers in `references/routing-matrix.md` and authority/output contracts in `references/agent-catalog.md`.

Choose one correctness review profile for a scope. Both standard and deep review routes use the existing `alaa-reviewer`; record the deep-review trigger without creating a duplicate review lane.

Missing target models or roles are explicit blocked/degraded execution, never silent fallback. Diagnose missing context, tool failure, and specification ambiguity before attributing failure to model capacity. The catalog is a menu; dispatch only roles whose triggers hold.

## 5. Orchestrator execution pipeline

Phases A through E run in orchestrator mode; Phase F applies only to user-requested integration and requires explicit authorization before effects. Advisor mode runs no execution phases; section 1 routes its planning artifacts separately. These are logical outcomes, not mandatory separate dispatches or repeated ceremonies. Coalesce compatible actions and evidence under the workflow plan; preserve outcomes, independent authority and gate economics. `references/verification-and-gates.md` owns what each phase does, its triggers, and what each gate requires — read it before dispatching Phase A.

| Phase | Owns | Ends when |
|---|---|---|
| A — Plan | workspace setup, evidence lanes, the chosen solution and its rejected alternatives, the written plan, the profile | the plan and profile are recorded and presented |
| B — Implementation | one lane per disjoint write scope, focused-tier checks, a reviewable diff per completed subtask | every required lane is reconciled against its actual diff |
| C — Verification | one integrated affected-tier plan, executed by an authority that owns no lane | every command reached `PASS`, or the phase ended blocked with the failure classified and its owner named |
| D — Review and specialist gates | the independent review, plus every specialist whose trigger holds | findings are resolved or explicitly accepted by the user |
| E — Documentation and final validation | documentation and its grade, required final gates, the report; base integration only when requested and authorized | the candidate has the proof required for the requested outcome |
| F — Requested integration | reviewable integration details and explicit authority, then the local merge | authorized integration is complete, or its declined/blocked status is reported; not applicable to local-only work |

### Execution profile: size the pipeline to the plan

**Every profile preserves Phases A through E and their required gates.** Phase F is conditional; local-only completion requires no merge prompt. Select and record the profile from the finished plan. Escalate when a heavier condition becomes true; do not de-escalate because its qualifying evidence persists. Implementation-role reassessment follows `references/routing-matrix.md`.

| Profile | Conditions — every one must hold | Shape |
|---|---|---|
| `lean` | one lane, one implementation phase, a diff that stays inside the lane plan, and none of the `hardened` conditions or deep-review triggers | Phases A–E, and F only when requested; the lead performs Phase D's review itself instead of dispatching `alaa-reviewer`, and specialists still fire on their own triggers |
| `standard` | anything that is neither `lean` nor `hardened` | Phases A–E with every required gate; F only when requested |
| `hardened` | the change meets the adversarial reviewer's blast-radius condition in `references/routing-matrix.md` | `standard`, plus the architecture critic in Phase A and the adversarial reviewer in Phase D |

`lean` review is independent because the lead did not author the diff. If the diff leaves the lane plan, select `standard` and dispatch `alaa-reviewer` against the complete change.

**No profile suppresses a specialist.** Apply only the triggers owned by `references/routing-matrix.md`, identically at every profile.

### Final report

Report: outcome; separate verdicts for `IMPLEMENTED`, `MERGE_CANDIDATE`, `RELEASE_CANDIDATE`, `PUBLISHED` under `alaa-workflow references/workspace-and-integration.md`; lane changes/touched files; commands/results marked run or cited and tier; review/specialist verdicts and finding dispositions; documentation outcome/grade per touched document; curation persisted/deferred/empty; risks, skipped checks and follow-ups. List every dispatched agent once with configured/requested model/effort, separately observed identity or unknown, observable mismatches only, and the named admission criterion for each escalated lane.

Close with one accounting line from existing plan, roster and evidence: dispatches/distinct roles; underlying checks run/cited (covered children counted once); branch span from plan `Created` to last authorized commit, or unavailable. No timer, extra command or invented budget.

## 6. Advisor-mode output

Provide: grounded repository findings; a lane plan with dependencies and gates; one ready-to-run prompt per lane using the templates; recommended agent, model, and effort per lane; a verification plan and resource policy; and the risks, assumptions, and decisions that require the user. Apply section 1's artifact admission: report saved plan/checkpoint paths when admitted; otherwise deliver the plan in the reply. Do not imply implementation occurred.

When generating a goal condition, read `alaa-prompting-guide references/06-invocation-and-composition.md`; it owns condition syntax and the skill-led kickoff.

## 7. Verification and resource rules

Schedule the commands below through `references/verification-and-gates.md` Gate economics; proven aggregate coverage may discharge an identical child invocation, never a different scope or observer.

Run `python scripts/check_agent_contracts.py` after instruction-contract changes and `python scripts/check_agent_contracts.py --self-test` after checker changes. Exit `0` is clean, `1` is findings, and `2` is unavailable proof; either nonzero blocks completion. These fixtures check source requirements, not live model behavior.


- Exact command semantics come from repository guidance and the dispatch. Never invent a flag merely to make a check pass.
- After any change to `agents/`, the grant checker must pass before completion; `references/agent-catalog.md` states its exact invocation and exit-code contract.
- Lowering process priority is mandatory for declared CPU-heavy local commands; limiting runner-level parallelism is separate and must also be explicit.
- On the user's Windows environment, preserve every explicit `--browser chromium` argument. Never remove, replace, or change it without prior user approval.
- Do not kill unrelated services, dev servers, containers, or processes; do not start duplicate services when a reusable declared service exists.
- Do not update snapshots, golden files, lockfiles, generated clients, dependencies, or migrations during verification unless that change is an explicitly scoped implementation lane.

The direct-reference router selects resource and failure handling before those decisions.

## 8. Safety and authority

- Repository-local, reversible edits inside declared scopes may proceed in orchestrator mode.
- Ask before destructive Git operations, force pushes, history rewrites, deployment, publishing, production access, data deletion, credential changes, shared-system configuration changes, or irreversible migrations.
- Installation and updates require explicit user authorization for named target paths; activation grants none.
- A lane's code-intelligence grant lives in its agent file, not in the dispatch. `references/agent-catalog.md` records which agents hold CodeGraph, the Serena read set, both, or neither; `/alaa-code-intelligence-routing` owns why. Reinstalling this pack restores those grants, so change them here rather than in `~/.claude/agents`.
- Commit only with explicit user authorization, in the workflow-selected checkout. Without it, preserve the reviewed diff and pin validation to a content snapshot under the workflow protocol. Every external or destructive effect requires its own explicit authority. Never add Co-Authored tags.
- Never expose secrets in prompts, logs, artifacts, or reports.

## 9. Stop conditions

Stop successfully only when every acceptance criterion has evidence, mandatory gates passed, the final candidate passed the scope and proof levels required by repository policy and /alaa-testing-strategy, the final diff scope is clean, documentation was completed or explicitly skipped, the final reusable-context gate reported what was persisted, deferred, rejected, or absent, and any requested integration has an accurately reported authorized, declined, or blocked outcome. Local-only requests complete without an integration prompt.

Stop and report a partial or blocked state when: the same lane is blocked twice by the same cause; blocker or major findings remain after two fix cycles; verification remains flaky, timed out, contaminated, or environment-blocked; scope expands beyond the goal; an irreversible or product decision belongs to the user; or a safe execution path no longer exists.

## 10. Failure discipline

Use a reviewer only to judge, a verifier only to execute evidence commands, and a researcher only to retrieve. Classify shell, runtime, permission and stale-cache failures before any product edit; `references/failure-taxonomy.md` owns the categories. Never report fail-then-pass as clean PASS. Report adversarial findings without another fix loop. Name only the lane's matching clean-code skill, not the whole family.

## Direct references

| Before you | Read |
|---|---|
| Plan, allocate workers, reassess remaining work or decide a specialist trigger | `references/routing-matrix.md` |
| Dispatch a role | `references/delegation-prompts.md` |
| Start Phase A, consolidate checks or decide gate requirements | `references/verification-and-gates.md` |
| Select or deviate from a model/effort profile | `references/model-effort-policy.md` |
| Inspect role authority, output or grants | `references/agent-catalog.md` |
| Set command priority, workers, timeout or resource limits | `references/resource-policy.md` |
| Classify a failed check | `references/failure-taxonomy.md` |
