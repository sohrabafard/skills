# Execution Pipeline and Gate Policy

`SKILL.md` carries the phase table, the execution profiles, and the authority boundaries. This file
owns what each phase actually does and what each gate requires. Read it before dispatching Stage A,
and again whenever a gate's requirement is in question.

Stages A-F define outcomes and authority. They are distinct from workflow phases. Combine compatible actions in the workflow plan. Keep each required outcome, observer and ordering constraint.

## Review boundary and execution cadence

This pair owns scheduling. /alaa-testing-strategy owns check necessity, breadth and proof. Before dispatch, read `alaa-workflow references/task-tracking.md` for task-store selection, plan resolution, registration, phase evidence and closure.

Resolve the canonical plan at its admitted address. Read a native `beads:<root-id>` plan through the bound issue store. Read a Markdown plan through its admitted file family. Verify live registration, hierarchy, prerequisite edges, resolved skills and readiness through the recorded store. A native plan requires its registered issue graph and evidence, with no Markdown prerequisite. Follow the workflow owner's outage and existing-family rules. Never initialize a replacement Beads database.

Read the plan's `Review boundary: phase|final`, `Final phase`, `Commit authority` and phase `Review status`/`Review evidence` in its canonical medium. For a native plan, use the final phase's exact issue ID. Pass that whole-engagement contract, plan reference and exact phase/task/subtask cursor into every nested invocation. Missing or inconsistent executing mappings block dependent dispatch; workflow owns their validation. Nested goals never reset the boundary or relabel intermediate output as final.

| Reached boundary | Required action |
|---|---|
| Subtask end | The implementer runs the smallest focused discriminating check and necessary touched-file lint/type/build; record its issue evidence. |
| Task end | The task owner runs bounded task-acceptance selectors across its subtasks, citing still-valid coverage; record its issue evidence. |
| Phase implementation end | Reconcile lane diffs and focused evidence. Collect missing phase checks through Stage C. Record phase test evidence without claiming independent acceptance. |
| Declared phase review end | Reconcile that phase's complete diff, required independent verification, correctness review and triggered specialists; triage findings under `alaa-workflow references/review-mode.md` `## Finding triage`, fixing blocking ones and retesting before acceptance. |
| Whole-engagement final end | Reconcile the complete candidate. Run review at the declared boundary and address its findings and all deferred findings in one planned repair batch. Collect required retests and final checks. |

Never dispatch independent subtask/task review. Under `Review boundary: final`, intermediate phases retain `REVIEW_PENDING`; tested issue closure advances readiness without claiming reviewed acceptance. Defer independent acceptance until that boundary; local checkpoints follow the commit protocol below. Under `phase`, only the declared phase end earns review. Preserve stricter genuine repository gates and necessary focused feedback; if a required earlier gate conflicts with the declared boundary, return the conflict to the plan owner rather than silently skipping either rule.

Local commits follow the main instruction file's local-commit rule through `alaa-workflow references/workspace-and-integration.md`. The integration parent commits each finished, validated topic or lane on the current work branch as it lands, at any phase, including before final review. A commit is a checkpoint, not acceptance; record review status separately. Reuse applicable standing authority without another approval. Preserve an identified snapshot when authority or validation is missing. The parent serializes commits and stages only owned changes; worker roles return evidence and do not write the shared index or commit. Pending worker review/commit handoffs never delay the parent's authorized checkpoint. Push, merge into another branch, tag and history rewrite still require explicit permission.

Nested invocations return tested evidence, pending review/commit and the next cursor. Stage C collects focused phase evidence. Stage D waits for the inherited review boundary. Plan one whole-engagement broad gate stage in Stage E, after final documentation, when required checks need that breadth. Phase transitions earn no broad pass. Earlier required repository gates follow the conflict rule above.

## Plan and allocation

Apply `routing-matrix.md` for planning controls and the single post-consolidation worker allocation pass. Persist choices in the workflow plan before dispatch; no second allocation artifact.

## Before any dispatch

1. Inspect relevant repository guidance (`AGENTS.md`, local instructions, architecture docs, package manifests, CI, tests, and affected code paths).
2. Restate internally: desired outcome; checkable acceptance criteria; constraints and preserved behavior; out-of-scope work; irreversible or externally visible actions.
3. Draw the fewest lanes that keep write scopes disjoint and buy real parallelism, each with one concrete outcome, owned files/modules, exclusions, acceptance criteria in the dispatch envelope's criterion shape, focused commands, dependencies, resolved skill bindings under `alaa-workflow references/companion-routing.md` including its matching clean-code owner, and return shape/line bound. Split a lane only for disjoint write scope run in parallel, a different owning skill or authority, a different task model or effort, or work exceeding one agent's context; absent another split reason, sequential work in one scope stays one lane, because each extra lane adds a dispatch, a context transfer and a reconciliation. The lane, not the subtask, is the dispatch unit: one dispatch carries every subtask of a task that shares one registered profile and owning skill, and that agent runs the task-acceptance selectors at its end. Before implementation or fix-cycle dispatch, classify actual command scope, never tier labels; send focused commands to subtask workers and explicitly bounded task-acceptance commands to the task owner; reserve affected/exhaustive commands for boundary gates; a focused command is the topic selector `/alaa-testing-strategy` names.
4. Apply `alaa-workflow references/workspace-and-integration.md` for one writer per file, generated output or shared resource and stopped-writer recovery. Disjoint-file lanes may share the current checkout; do not create a worktree automatically.

`references/routing-matrix.md` owns every specialist trigger; `references/delegation-prompts.md` owns
the dispatch contracts.

## Gate economics

Retain required retrieval, focused implementer checks and independent acceptance gates. Remove repetition only without new changes, failures or unresolved concerns. Model capability never waives an observer or mandatory gate. Never weaken review to obtain a pass.

Before designing implementation or verification, load /alaa-testing-strategy. Before building a command list, consolidating coverage or running collection/repair/retest, read its `references/100-test-execution.md`; before resource or timing decisions, read its `references/110-execution-resources.md`; before classifying or repairing a result, read its `references/120-result-classification.md`. Those owners define generic execution, evidence validity and failure handling; this section schedules their use under independent authority.

Record the check list and evidence at the workflow-selected owner before dispatch. `alaa-verifier` collects missing or invalidated evidence when the planned checks require its authority. Review waits until required pre-review collection, batch repair and retests pass. The canonical minimal early-repair exception returns to collection without review.

Assign the collected repair batch as one serialized implementation lane; reconcile conflicting writers through `alaa-workflow references/workspace-and-integration.md` before continuing. Continue the existing implementer whose valid assignment and context cover most failures through a host-supported continuation tool. Dispatch fresh only when continuation is unavailable, context is invalid, or `routing-matrix.md` selects another managed profile, external role or task pair. The analyst diagnoses and never fixes. Independent verification owns required retests after batch repair; implementer evidence never replaces independent acceptance. Existing retry/stop budgets remain in force.

Freeze the tested scope through `alaa-workflow references/workspace-and-integration.md` before verification. Evidence needs no commit; local checkpoints follow the commit protocol above and never discharge review.

## Reusable-context owner

Apply `alaa-workflow references/context-curation.md` at material boundaries and closure. Workflow owns scan timing, candidate location and gate reopening; lessons owns admission and memory owns authorized publication; consume its recorded outcome once, including when this run is a child phase.

## Stage A — Plan

Always first, never skipped, at any profile. Everything after it inherits its decisions, so a decomposition written before the solution is chosen decomposes the wrong solution and every lane then carries that mistake into its own diff.

1. Before the first write apply `alaa-workflow references/workspace-and-integration.md`: record base/checkout identity, inspect unrelated changes and resolve overlapping ownership. Use its current-checkout or isolation decision; disjoint existing changes alone require neither refusal nor a new branch.
2. Dispatch the specification, exploration, and research lanes whose conditions in `references/routing-matrix.md` hold, in parallel only when their questions are independent. Spending on `alaa-spec-analyst` here is the cheapest correctness lever in the pipeline and is wasted on a request that is already concrete.
3. Reconcile observed facts and label unresolved assumptions. Resolve missing facts through retrieval/clarification, then select the planning profile through `routing-matrix.md` before making the plan; the lead ratifies an advisory planner draft.
4. Before approving a new container image, toolchain, chart, CI include/template, generator, hook pack or
   script reused across repositories/pipelines (not an existing-artifact edit), apply /alaa-memory-os
   capability inquiry: this tree cannot establish what another owner already provides. Read any
   /alaa-services-contract infrastructure registry first and reuse sufficient current evidence.
   Record the verified owner/alternative and evidence, or the memory owner's scoped unavailable/unknown
   outcome, in the workflow plan and lane `<context>`. Empty recall never justifies `none` infrastructure.
   A verified alternative enters step 5 as reuse-or-extend; rejecting it for a parallel artifact requires
   its owner's or user's decision. Before local absence becomes a validation blocker or a permitted
   additional repair has an unresolved owner, use the same memory-owned inquiry and return to the runtime
   recovery owner; lookup adds no retry or native status authority.
5. Decide the solution before decomposing it. Name the chosen approach and each rejected alternative with the reason it was rejected. Where the goal stores, indexes, caches, or moves data, decide the representation and the access path with `/alaa-data-layer`. Where a path grows with tenants, rows, history, or events, state its complexity bound with `/alaa-algorithms-data-structures`. Run the design pass under `/alaa-system-design` when that skill's conditions hold; `references/routing-matrix.md` names the three conditions it adds beyond the architecture critic's own triggers.
6. Record the architecture-critic trigger whenever `references/routing-matrix.md` or step 5 requires it. Complete the design record before implementation; schedule its independent judgment at the declared review boundary, subject to stricter repository gates above.
7. Record known API-contract triggers and decide consumer impact, compatibility and deprecation before implementation. Schedule independent contract judgment at the declared review boundary; a newly discovered trigger reopens the affected plan and gate.
8. Use `alaa-test-strategist` before implementation, not after, whenever its condition in `references/routing-matrix.md` holds: a test matrix designed after the code exists is written against what was built rather than against what the change had to prove.
9. Record the plan through /alaa-workflow or adopt the existing parent plan. Record ordered phases, acceptance, focused phase checks, the final gate and handoff knowledge. Follow `alaa-workflow references/task-tracking.md` for selected-store task records and evidence-based progress; use `alaa-workflow references/context-continuity.md` for canonical position and resume. Apply `alaa-workflow references/companion-routing.md` for executable phase/task skill bindings before implementation or write-lane dispatch. Workflow owns this machinery; the orchestrator consumes it without duplicating task state.
10. After tasks/dependencies are consolidated, run Batch allocation from `references/routing-matrix.md` once and record all lane choices. Choose the execution profile from the finished plan, then present the plan and the profile in one compact message and continue without waiting, unless an irreversible decision, destructive action, external side effect, or genuine product choice belongs to the user.

## Stage B — Implementation

1. Select the managed implementation profile or admitted external role through `references/routing-matrix.md` before assignment or reassignment, then dispatch one agent per ready lane. Carry selection evidence in the dispatch and roster.
2. Consume dependencies/readiness from the selected task authority and phase barriers, write ownership and shared-resource conflicts from the workflow plan. A lane is ready only after required dependency contracts are reconciled. Dispatch ready independent lanes together when observed host slots and declared resource ceilings permit; increase parallel writers when capacity and ready work justify it. Record an unavailable capacity observation and use the smallest supported batch until capacity is established; do not invent a ceiling or assume unlimited capacity.
3. Never overlap writes to files, generated outputs, contracts, migrations or shared runtime state. Reconcile at declared integration barriers before dependent work starts. Reserve capacity for the next required gate only when it is ready; apply /alaa-testing-strategy `references/110-execution-resources.md` before scheduling CPU-heavy work.
4. Each subtask lane runs its focused failure-mode topic selectors and necessary touched-file lint/type/build on the shared build cache. The explicitly assigned task owner runs bounded task-acceptance selectors at task end; neither may run boundary affected/exhaustive checks. It writes no test `/alaa-testing-strategy` finds unowed; that skill owns the tiers and the test-need decision. Choose the smallest discriminating checks for claimed behavior and changed exported-surface, contract, type or lint properties; return observed output, or mark the property not checked. Role definitions own dispatch-conflict handling; reconcile every excluded command and unrun check before accepting the lane.
5. Wait for all required lanes. A blocked lane is blocked; do not pad it into success.
6. Reconcile actual diffs and lane evidence, not summaries alone. Detect scope violations, accidental generated changes, contract mismatches, and cross-lane breakage. Record observed task progress and tested closure through `alaa-workflow references/task-tracking.md`; closure implies neither reviewed acceptance nor commit authority.

## Stage C — Independent verification

1. At phase implementation end, reconcile focused lane and task evidence against the phase's acceptance criteria. Collect only missing or invalidated focused checks and explicit earlier repository obligations. Before Stage D, require independent focused evidence for the complete declared review scope on the reconciled candidate. Cite eligible independent evidence. Collect missing, invalidated or required-fresh coverage through `alaa-verifier`. Schedule broad final coverage in Stage E.
2. Apply /alaa-testing-strategy `references/100-test-execution.md` for scope, reuse, aggregate coverage, freshness and command validity. Require the correct observer before citing evidence.
3. When independent checks remain to run, dispatch `alaa-verifier` with the exact consolidated commands, cwd, timeout, artifact directory and resource policy derived through /alaa-testing-strategy `references/110-execution-resources.md`. Use only host-exposed dispatch/continuation mechanisms. Under Codex, route Docker socket permission failures through /alaa-codex-runtime-ops before the canonical host fallback.
4. Classify and route results through /alaa-testing-strategy `references/120-result-classification.md` for classification.
   Apply this orchestrator's Failure routing in `references/routing-matrix.md`. The verifier executes, the analyst diagnoses, and the owning lane repairs; neither a clear owner nor a cheap fix bypasses the canonical collection barrier.
5. After batch repair, apply the canonical retest procedure before Stage D. Unresolved required pre-review results block review. Unresolved required results block acceptance.

## Stage D — Independent review and specialist gates

1. Only at the inherited review boundary, select `alaa-reviewer` or `alaa-reviewer-deep` by the routing matrix, then spawn that one profile against the complete diff and lane plan after Stage C's collection, batch repair and required retests pass. Under the `lean` profile the main thread performs this review itself against a diff it did not write; the authority boundary holds because the reviewer is not the author, and `SKILL.md` Execution profile decides when `lean` becomes `standard` and `alaa-reviewer` is dispatched.
2. Trigger a specialist only when its own condition in `references/routing-matrix.md` holds. That file owns every trigger; this one names no condition and narrows none, because a shorter local copy of a trigger list does not read as a summary at dispatch time — it reads as the list, and the conditions it dropped become gates nobody ran. The triggers are identical at every profile.
3. At that same boundary, spawn `alaa-adversarial-reviewer` only when its condition in `references/routing-matrix.md` holds. That condition has two arms and they are not interchangeable: the blast-radius arm is recorded in Stage A and selects the `hardened` profile, while the conflicting-verdict arm is discovered here and fires the reviewer inside whatever profile is already running. A new conflict triggers that lens without retroactively changing completed design work or resetting the inherited boundary. It is a second independent lens, not a second opinion on a routine change, and its findings are reported to the user rather than fed into another fix cycle.
4. Reviewer verdict handling: `APPROVED` proceeds; `APPROVED-WITH-NITS` proceeds; `CHANGES-REQUESTED` routes blocker and major findings verbatim to the owning lane; minor findings and nits follow `alaa-workflow references/review-mode.md` `## Finding triage`.
5. Specialist blocker and major findings are gates equal to reviewer findings. Conflicting specialist opinions are reconciled by the main thread using repository evidence; unresolved high-risk conflicts are surfaced to the user.
6. Present every finding this phase leaves open — reported to the user rather than routed to a lane — as one decision set: each item with its severity per lens, the smallest fix that closes it, and what closing it costs. Ask once. Answered one at a time, each answer can move the tree again and invalidate affected final evidence, including any required exhaustive run.

For required Ent review, interpret the native report under `alaa-ent-go-orm-db references/85-specialist-delegation.md`. `STATUS: COMPLETE` means the assessment finished. It grants no approval. A missing report, `STATUS: BLOCKED`, `STATUS: INCOMPLETE` or missing required evidence blocks acceptance even without findings. Triage findings at their reported severity and apply the specialist conflict route above.

## Stage E — Documentation and final validation

1. Spawn `alaa-documenter` when its condition in `references/routing-matrix.md` holds. It is the final write lane, which is why every check below runs after it and not before.
2. Documentation is graded, not merely written. `alaa-repo-docs references/15-document-size-and-clustering.md` owns the size ladder, its thresholds, the measuring command, and the one condition under which the largest grade may stand; `/alaa-repo-docs` applies it. This skill decides only that the grade is measured and reported, never what the ladder says — a local copy of it goes stale the moment that skill retunes a threshold.
3. After documentation edits, run the documentation gate below. Documentation is the final write lane and must not bypass validation.
4. If integration is requested and explicitly authorized, bring the base branch into the work branch before final verification; otherwise verify the current candidate and mark integration not requested or awaiting authority as applicable. Freeze the final candidate and record its content snapshot and any integrated base commit. Select required checks and proof from repository policy and /alaa-testing-strategy. Collect required affected and exhaustive checks in one whole-engagement gate stage. Run any required exhaustive tier once, fresh on the final candidate after documentation. Cite matching coverage and run only uncovered checks. No candidate writes may overlap the final pass. If a result blocks acceptance, apply Gate economics and the existing retry budget. Reopen affected review and repeat only failed, invalidated or required-fresh checks.

5. Consume the workflow owner's final reusable-context gate after evidence is stable; an empty retained set is valid. Follow its `pipeline reopen required` outcome before closure.
6. Re-check final Git status and diff against declared scopes; confirm canonical task progress and workflow status match what landed; record the last authorized commit timestamp when available, otherwise record it as unavailable.
7. Report in the order `SKILL.md` states, and audit every claim against an actual tool result from this session before reporting it.

## Stage F — Requested integration

This phase applies only when the user requests integration. A local-only request completes after Stage E without a merge prompt. For requested integration, present the candidate, diff, gate evidence, and residual risks. Reuse existing explicit authorization for the exact operation; when it is absent, ask only after the result is reviewable and do not merge before it arrives.

Integrate under `alaa-workflow references/workspace-and-integration.md`. If the base advanced after final verification, incorporate it on the work branch and rerun the required final gates against the changed candidate; a clean merge also changes the tested tree. When the base did not move and the evidence remains applicable, no repeated gate is owed. Push, tag, branch deletion, worktree removal, and remote effects each require explicit authority. A declined or unanswered integration request leaves the candidate intact and is reported accurately, without invalidating completed local work.

## Evidence quality

Before accepting or citing test evidence, apply /alaa-testing-strategy `references/100-test-execution.md` and `references/120-result-classification.md`. Independent acceptance additionally requires an observer independent of the implementation with authority for that gate. An implementer's broad PASS cannot discharge it. Record the observer with the canonical evidence identity; cite eligible independent evidence instead of repeating it.

## Gate reopen owner

When curation changes repository instructions, apply `alaa-workflow references/context-curation.md` for reopening affected gates; this run consumes that decision rather than defining a second protocol.

## Finding ownership

- Findings are routed verbatim to the lane that owns the behavior.
- Cross-cutting findings become a new serialized lane with an explicit scope.
- Select the fix owner through Failure routing in `references/routing-matrix.md`.
- The reviewer/specialist never fixes its own finding.

## Maximum cycles

Plan one repair batch. A second fix-review cycle needs a new or unresolved blocking finding and remaining authority. Stop after two cycles unless the user authorizes more. Apply any stricter per-cause budget first. A new agent or stage never resets it. Required retests count against the applicable retry budget.

## Documentation gate

Because the documenter writes after code review, documentation changes require at least:

- final diff scope check;
- repository docs formatter/linter when available;
- touched-link validation when available;
- example/config snippet validation when safely supported;
- spot-check against verified behavior;
- the size grade `alaa-repo-docs references/15-document-size-and-clustering.md` requires, measured with `alaa-repo-docs scripts/check_markdown_links.py` in its line-budget mode. Consume that result rather than judging the grade here: its exit `1` on an unapproved document at the largest grade is a failed gate, and its exit `2` proves nothing.

## Final success criteria

The orchestrator may report completion only when:

- every acceptance criterion maps to evidence, each marked run, cited, or review-only with its review evidence; run or cited items carry their tier;
- required final checks and proof levels passed on the final candidate, including a fresh exhaustive tier when required, with no unverified candidate changes afterward;
- no mandatory command is failed, flaky, timed out, blocked, or contaminated;
- required reviewer and specialist assessments are complete, and blockers/majors are resolved or explicitly accepted by the user;
- final touched files match authorized scopes;
- documentation ran or was explicitly skipped for a grounded reason;
- the final reusable-context pass reported persisted, deferred, rejected, or no admitted candidates;
- no `pipeline reopen required` result remains unresolved;
- canonical task progress and workflow status match what landed; every changed subtask has tested diff evidence and the declared boundary has attributable review; local checkpoints follow the main instruction rule independently of review status;
- requested integration is complete or explicitly reported declined/blocked; local-only work needs no integration prompt;
- no destructive/external action was performed without authorization.
