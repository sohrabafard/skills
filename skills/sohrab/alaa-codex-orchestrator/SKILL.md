---
name: alaa-codex-orchestrator
description: "Production-grade multi-agent coding orchestration for Codex. Use when a user asks to build, fix, refactor, migrate, review, investigate, or plan non-trivial repository work with an orchestrator/advisor and specialist subagents. Activation only inspects installed roles; installation requires explicit authorization. It plans first, sizes the pipeline to that plan, and routes work through scoped implementation, risk-proportional verification, review, and conditional specialist gates in the workflow-selected checkout. Do not use for trivial edits that need no delegation or for destructive/external actions without explicit authorization. Let /alaa-workflow lead a multi-session program; this skill writes its plan and state through it either way."
---

# Alaa Codex Orchestrator

Lead an evidence-driven multi-agent goal inside Codex. Narrow subagents inspect, implement, verify, challenge and document. The lead is the main thread: it decides how much verification each change needs and reports no unverified claim as complete.

**Mirrored behavior.** Change both runtime orchestrators together. Only runtime mechanics and model-family delegation polarity may differ.

## Admission

Before role inspection or planning, route a single bounded edit whose correctness one reader can confirm to direct execution under its domain owner. Do not start this pipeline for it. Required repository checks still apply.

## When NOT to use

- A single edit one reader can confirm without a second lane.
- A destructive or external effect, including push, deploy, data change or publication, lacks explicit authorization.
- The runtime is Claude Code rather than Codex. These TOML roles do not serve it.
- A multi-session program centers on plan continuity: `/alaa-workflow` leads and invokes this skill per phase. This skill still writes its plan through workflow.

## Safety and authority

- Repository-local, reversible edits inside declared scopes may proceed in orchestrator mode.
- Ask before destructive Git operations, force pushes, history rewrites, deployment, publishing, production access, data deletion, credential changes, shared-system configuration changes or irreversible migrations. Every external or destructive effect needs its own explicit authority.
- Activation grants no installation or update authority. Installation and updates require explicit user authorization for named target paths.
- Plan-only work grants no product execution, branch, or commit authority.
- Local commits follow the main instruction file's local-commit rule through `alaa-workflow references/workspace-and-integration.md`. Its `## Lane branches and commits` governs lane commits and the lane-branch merge. For a commit, do not wait for boundary review or request an already-granted permission again. Never add Co-Authored tags.
- Agent files own code-intelligence grants; dispatches do not. Change grants in this pack, not in `~/.codex/agents`, because a reinstall restores the pack grants.
- Before relying on isolation, inspect the effective sandbox, parent overrides and MCP grants. A read-only declaration proves no enforcement. Report unobservable permissions as unknown.
- Never expose secrets in prompts, logs, artifacts or reports.

## Operating modes

Follow explicit wording. Otherwise choose the lowest-side-effect interpretation that answers the request. Do not ask merely to select a mode.

**Orchestrator mode** applies when the user asks to build, fix, refactor, migrate, integrate, optimize or otherwise change a repository. The lead plans, dispatches, reconciles, verifies as it decides, and reports. It makes its own corrections only under Who fixes in `references/verification-and-gates.md`; implementers own all other implementation. It never silently takes over a failed lane, softens or omits a review finding, claims an unobserved check or overlaps writers. Adopt an existing parent plan; `/alaa-workflow` owns plan, checkpoint and prompts.

**Advisor mode** applies to plans, critiques, architecture advice, prompts, lane definitions or review without implementation. You may spawn research or read-only specialists. Do not implement product changes. Before deciding whether to save a plan, read `alaa-workflow references/artifact-lifecycle.md`. Deliver:

- grounded repository findings;
- a lane plan with dependencies and gates;
- one ready-to-run prompt per lane from the templates, with its agent, model and effort;
- a verification plan and resource policy;
- the risks, assumptions and decisions that require the user.

When a plan is admitted, report the canonical plan address and recovery reference. Otherwise deliver the plan in the reply. Do not imply implementation occurred. When generating a goal condition, read `alaa-prompting-guide references/06-invocation-and-composition.md`.

## Role availability

1. Test design and test execution need the separate companion /alaa-testing-strategy. If it is unavailable, report the missing owner and block dependent work. Never auto-install it.
2. Inspect the installed role definitions, the version and effective tools without writes, and compare the required managed roles with the shipped definitions. For a required external companion, apply its admission in `references/agent-catalog.md`.
3. Before dispatch, report each missing, stale or unavailable model or role as blocked or degraded. Never silently substitute a model or a generic role. Continue only the independent work whose required roles are available.

For an authorized install or update, use the supported materializing installers in `references/installation.md`. A direct TOML copy inherits parent MCP grants and is unsupported.

## Plan, allocate, dispatch

1. Before planning, apply the Mandatory Ponytail binding in `alaa-workflow references/companion-routing.md`, including its user opt-out.
2. Inspect guidance and affected paths. Settle outcome, acceptance, preserved behavior and irreversible actions.
3. Before Stage A evidence dispatch, apply `/alaa-memory-os` when its trigger holds: make one bounded recall and verify useful claims in repository truth. Route unresolved prior-session, ownership and shared-contract questions to `alaa-researcher`. `alaa-explorer` uses memory only when the repository cannot answer. Apply `/alaa-code-intelligence-routing` before code-evidence selection and reuse its result.
4. Plan through Planning profile selection in `references/routing-matrix.md`, then finalize and consolidate tasks and dependencies. Planning effort never sets worker effort. Worker selection alone needs no planner dispatch.
5. Allocate the batch once through Batch allocation in that file, and record each role with its pair and the fit-table row and column that selected it in the plan. For EVERY dispatch, apply its model AND effort allocation and its role triggers, and realize the pair through `references/model-effort-policy.md`. Dispatch only catalog roles whose trigger holds.

### Dispatch controls

Pass `model` AND `reasoning_effort` to the spawn surface on EVERY dispatch. An omitted control inherits the parent agent's value, which is usually stronger than the lane needs. This table is the short form of the fit table in `references/routing-matrix.md` *All-role task allocation*. That file governs: read it for the effort rules, the row of a lane that implements nothing, and the exceptional model.

| Judgment left to the lane | Model | Ordinary effort |
|---|---|---|
| None: an exact transformation | `gpt-6-luna` | `medium` |
| Bounded local decisions with a discriminating check | `gpt-6.1-terra` | `medium` |
| Grounded everyday decisions | `gpt-6.2-sol` | `medium` |
| Coupled or cross-boundary unresolved decisions | `gpt-6.2-sol` | `medium` |
| Judgment-dense work that no check can catch | `gpt-6.2-sol` | `high` |

Use `high` for a long, strict or hard-to-verify lane on any row. Use `low` for a short, fully specified lane on the first three rows only. An effort above `high` needs the recorded measured gain that the fit table requires, and no lane runs at `ultra`.

### Dispatch discipline

- **One agent per lane.** Dispatch no duplicate lane and no summary-check agent. A lane starts no subagent of its own. Independent verification and review inspect the actual artifact under separate authority. Keep inspection and the lead's own small correction inline.
- **Run independent lanes together.** Start a dependent lane as soon as the lanes it consumes finish. Join lanes behind one barrier only when the next step consumes all of their outputs.
- **Count live lanes before each spawn or follow-up.** Open spawned-agent threads count against `agents.max_concurrent_threads_per_session`; when it is unset, treat the live count at the first limit error as the limit for this session. At the limit, close the thread of a completed lane that Who fixes in `references/verification-and-gates.md` will not continue; when none qualifies, wait for a running lane to finish. After a limit error, free a slot; never resend the same call unchanged. `alaa-prompting-guide references/11-codex-runtime-features.md` owns the key and its default.
- **After an interruption or a usage-limit error,** record the lane's last evidence in the plan or compact dispatch, and reconcile the transcript, the checkpoint and the surviving files before resuming writes. Apply the stopped-writer recovery in `alaa-workflow references/workspace-and-integration.md`, then dispatch only the remaining scope.
- **Keep dispatches lean.** Word each dispatch under /alaa-prompting-guide. Carry lane facts only: outcome, owned files, exclusions, acceptance, commands, dependencies, resolved skills and return contract. Do not restate the native role definition. State each instruction once. Name `/alaa-low-noise` in a dispatch only for a discovery-heavy or log-heavy lane, because every agent definition carries the output rule.
- **Decide verification per change, and read before you accept a return.** `## Direct references` names the section to read before a plan, a dispatch, the acceptance of a return, and a fix or another review.
- **Correct sparingly.** Correct a statement only when its error changes user code, conclusions or decisions. State the correction once, then continue.

## Pipeline

Orchestrator mode keeps Stages A, B and E. Stages C and D run as the verification decision and the floors in `references/verification-and-gates.md` require. Stage F needs requested integration, and explicit authority before its effects. Advisor mode runs no execution stage. Stages are logical outcomes, not workflow phases or separate mandatory dispatches. Coalesce compatible actions and evidence in the workflow plan while preserving outcomes and floors. Before Stage A dispatch, read `references/verification-and-gates.md`.

| Stage | Owns | Ends when |
|---|---|---|
| A — Plan | workspace setup, evidence lanes, the chosen solution and its rejected alternatives, the written plan, each task's verification decision | the plan and decisions are recorded and presented |
| B — Implementation | disjoint lanes, focused subtask checks and bounded task acceptance, with tested diff evidence | every required lane is reconciled against its actual diff |
| C — Verification | the checks that the decisions and the floors require, under the observers they name | every command reached `PASS`, or the phase ended blocked with the failure classified and its owner named |
| D — Review and specialist gates | at the declared boundary, the independent review and specialist gates that the decisions and the floors require | required assessments are complete and every finding has a recorded disposition |
| E — Documentation and final validation | documentation and its grade, required final gates, the report; base integration only when requested and authorized | applicable documentation is validated; whole-engagement final gates wait for its final candidate |
| F — Requested integration | reviewable integration details and explicit authority, then the local merge | authorized integration is complete, or its declined/blocked status is reported; not applicable to local-only work |

## Final report

Report outcome; independent lifecycle verdicts (`IMPLEMENTED`, `MERGE_CANDIDATE`, `RELEASE_CANDIDATE`, `PUBLISHED`) under `alaa-workflow references/workspace-and-integration.md`; lane changes and files; commands and results, marked run or cited, with tier; review and specialist verdicts and dispositions; each touched document's outcome and grade; curation as persisted, deferred or empty; risks, skipped checks, follow-ups. List each dispatched agent once with the model and effort you dispatched, taken from your allocation record, never from the lane's report; add each lane that blocked on its task controls or reported a control mismatch, and the exceptional-model admission for each escalated dispatch.

Write for a reader who saw no tool call and no lane report: outcome first, and a definition for each lane label or abbreviation the run invented.

Close with one line from the existing plan, roster and evidence: dispatches and distinct roles; underlying checks run or cited, covered children counted once; span from plan `Created` to last authorized commit, or unavailable. Use no timer, extra command or invented budget.

## Verification and resource rules

Before designing implementation or verification, and before planning or executing checks, load /alaa-testing-strategy. Read its `references/100-test-execution.md` for execution, `references/110-execution-resources.md` for resources and timing, and `references/120-result-classification.md` for result classification and diagnosis, and before product edits for repair eligibility.

After a change to this pack, run from the pack directory:

- after an instruction-contract change, `python3 scripts/check_agent_contracts.py`;
- after a change to agent instructions, a contract asset, pins, agents or the version, `python3 scripts/render_agents.py --write`, then `python3 scripts/render_agents.py --check` and `python3 scripts/validate_pack.py`; review the generated wrappers against `assets/reviewer-contract.md`, `assets/implementation-contract.md` and `assets/planner-contract.md`;
- after any change to `agents/`, `python3 scripts/check_agent_grants.py`, which verifies the transport-neutral templates; `references/installation.md` owns the live-resolution checks.

Each command exits `0` when clean, `1` on findings, drift or grant findings, and `2` on unavailable proof. Either nonzero exit blocks completion.

## Stop conditions

Stop successfully only when all of these hold:

- acceptance is evidenced;
- mandatory gates pass, and the final candidate's scope and proof satisfy repository policy and /alaa-testing-strategy;
- the final diff scope is clean, and final touched files match authorized scopes;
- documentation ran, or was explicitly skipped for a grounded reason;
- the final reusable-context gate reports its disposition: persisted, deferred, rejected or absent;
- requested integration is complete, or reported as declined or blocked. Local-only completion needs no integration prompt.

Stop and report partial or blocked status when any of these occurs:

- the same lane or cause blocks twice;
- blocking findings of one kind return after the approach was reconsidered under After a fix in `references/verification-and-gates.md`;
- verification stays flaky, timed out, contaminated or environment-blocked;
- the work needs scope beyond the goal;
- an irreversible or product decision belongs to the user;
- no safe path remains.

## Direct references

The rules for these actions are in the named sections. Read the named section before the action in its row, unless it is still in your context. When it cannot load, do not take the action: report the missing section to the user and continue only the work that needs no such action.

| Before you | Read |
|---|---|
| Plan, allocate workers, reassess remaining work, choose review depth or decide a specialist trigger | `references/routing-matrix.md` |
| Write a plan with lanes, or choose the verification of a task | `references/verification-and-gates.md` `## The verification decision`, `## Floors` and `## Before any dispatch` |
| Write a dispatch for a role | `references/delegation-prompts.md` `## Common dispatch envelope`, then the template that its `## Role templates` names for that role |
| Accept a lane return, or continue after a lane reported a changed or unmet instruction or criterion, a blocker or an unrun check | `references/verification-and-gates.md` `## Stage B — Implementation` and `## Evidence`; for that report, also `alaa-workflow references/review-mode.md` `## Finding triage` |
| Act on a finding or a failed check: make or dispatch a fix, a retest or another review, or decide to fix nothing | `alaa-workflow references/review-mode.md` `## Finding triage`, then `references/verification-and-gates.md` `## After a fix` and `## Who fixes` |
| Dispatch the first write lane of a ready set, or give a lane its own worktree | `alaa-workflow references/workspace-and-integration.md` `## Lane branches and commits`, and `## Before the first write` step 4 for a worktree |
| Start a stage or run final validation | that stage's section in `references/verification-and-gates.md` |
| Consolidate checks | `references/verification-and-gates.md` `## Check collection` |
| Realize a model and effort pair | `references/model-effort-policy.md` |
| Inspect role authority, output or grants, or route a returned report on its first-line `VERDICT` or `STATUS` | `references/agent-catalog.md` |
| Set command priority, workers, timeout or resource limits | `references/resource-policy.md` |
| Classify a failed check | `references/failure-taxonomy.md` |
| Perform an explicitly authorized installation or update | `references/installation.md` |
