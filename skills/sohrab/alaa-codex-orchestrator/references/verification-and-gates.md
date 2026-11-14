# Verification and Gate Policy

Read this file before Stage A and whenever a gate's requirement is in question.

Stages A-F give the order of work. The verification decision below sets which checks and reviews run inside them. They are distinct from workflow phases. Combine compatible actions in the workflow plan. Keep each required outcome, observer and ordering constraint.

## The verification decision

The lead owns the outcome and decides how much verification each change needs, as a senior developer does. This file prescribes no pipeline, because a fixed one spends the same hand-offs on a typo as on an authentication change.

Decide once per task at plan time, record it in one or two lines in the plan or compact dispatch, and revisit it only when the task changes materially:

1. What can be wrong that the author's own focused check would not show: effects in other modules, concurrency, contract consumers, a trust boundary, data?
2. What does a miss cost, and can it be undone: blast radius, reversibility, exposure of production data, tenants, money or a public contract?
3. What evidence exists, and does it hold for this snapshot: who observed it, on which inputs, and did anything it covers change since?
4. What is the cheapest check that could prove the change wrong? Run that one. Stop adding checks when the next one could not change the decision.

Then choose per task: accept the author's observed focused evidence, read the diff yourself, have `alaa-verifier` run named checks, or dispatch an independent reviewer or a specialist gate. An independent observer needs a reason drawn from questions 1 and 2: what it can see that the author cannot, or what the miss would cost. "The pipeline says so" is not a reason.

`references/routing-matrix.md` owns every specialist trigger. On a floor surface the matching specialist is the required gate. Elsewhere a holding trigger informs question 1 and dispatches its specialist only with the reason the decision states.

An owed affected or exhaustive check runs through `alaa-verifier`, or through the lead when its output is short enough to read in full.

The decision sets whether and which verification a task gets; the declared review boundary sets when an independent review runs over the complete candidate. A boundary where no task chose an independent observer and no floor applies earns no review dispatch.

## Floors

An independent gate is always required, whatever the decision says, for a change to:

- authentication, authorization or tenant isolation: a miss lets a caller act as another user or tenant;
- secrets or cryptography: a miss exposes credentials or protected data;
- billing or money: a miss moves the wrong amount;
- a destructive or irreversible data operation, including a migration that drops or rewrites data: a miss cannot be undone;
- a breaking change to a public contract: a miss breaks consumers this repository cannot see;
- a production deployment or release: a miss reaches every user;
- any surface the user asks to have reviewed: the user wants a judgment other than the author's.

On a floor surface the author never approves its own work. The gate's blocking verdict binds the lead. Implementer evidence does not replace the gate. `alaa-reviewer` is the gate on a floor surface that no specialist trigger covers, including a review the user asks for.

## Evidence

Observed evidence counts by what it shows, not by who ran it. Outside the floors, the lead may accept an implementer's observed focused check on the same snapshot, and records that it did. An independent re-run is for a floor surface, or for stale, unobserved or ambiguous evidence. Nothing unchanged is checked again.

Before accepting or citing test evidence, apply /alaa-testing-strategy `references/100-test-execution.md` and `references/120-result-classification.md`. Where a floor or the decision requires independent acceptance, it requires an observer independent of the implementation with authority for that gate. An implementer's broad PASS cannot discharge it. Record the observer with the canonical evidence identity; cite eligible independent evidence instead of repeating it.

## Findings

Triage every finding by its consequence under `alaa-workflow references/review-mode.md` `## Finding triage`.

## After a fix

Whoever fixes proves the fix with the check that failed, or with the check that would have caught the defect. A fix that touches a floor surface returns to that floor's gate, because its author cannot approve it; the gate judges the fix, not the whole change again. Any other further review needs a stated reason: the fix changed the design, or the first review could not see what it needed. There is no cycle count. A new round needs a new reason. When a second round finds blocking findings of the same kind, stop repairing and reconsider the approach or the decomposition, because a returning defect class points at the plan, not the patch. Tell the user when you cannot resolve that yourself.

## Who fixes

Use the smallest capable hand. The lead may make a small, local, obvious correction itself when that is cheaper than a dispatch, inside the authorized scope, in files no active or pending lane owns. The implementer that holds the context continues for anything larger. Read-only roles stay read-only by their tool grants. A diagnosis may carry the proposed fix.

Keep one collected repair batch, because each separate repair pays its own context transfer and retest. Split it only where repair role authority differs, into the fewest compatible scoped assignments. For each assignment, continue the existing implementer whose valid assignment and context cover most failures through a host-supported continuation tool. Dispatch fresh only when continuation is unavailable, context is invalid, or `routing-matrix.md` selects another managed profile, external role or task pair. Execute the assignments serially and reconcile conflicting writers through `alaa-workflow references/workspace-and-integration.md` before continuing. Existing retry/stop budgets remain in force.

## Check collection

Before designing implementation or verification, load /alaa-testing-strategy. Read its `references/100-test-execution.md` before you build a command list, consolidate coverage, or run collection, repair or retest; its `references/110-execution-resources.md` before a resource or timing decision; and its `references/120-result-classification.md` before you classify or repair a result.

Record the check list and evidence at the workflow-selected owner before dispatch. `alaa-verifier` collects missing or invalidated evidence when the planned checks require its authority. Review waits until required pre-review collection, batch repair and retests pass. The canonical minimal early-repair exception returns to collection without review. Freeze the tested scope through `alaa-workflow references/workspace-and-integration.md` before verification; evidence needs no commit. Never weaken review to obtain a pass.

## Review boundary and execution cadence

This orchestrator pair owns scheduling. /alaa-testing-strategy owns check necessity, breadth and proof. Before dispatch, read `alaa-workflow references/task-tracking.md` for task-store selection, plan resolution, registration, phase evidence and closure.

Resolve the canonical plan at its admitted address. Read a native `beads:<root-id>` plan through the bound issue store. Read a Markdown plan through its admitted file family. Verify live registration, hierarchy, prerequisite edges, resolved skills and readiness through the recorded store. A native plan requires its registered issue graph and evidence, with no Markdown prerequisite. Follow the workflow owner's outage and existing-family rules. Never initialize a replacement Beads database.

Read these plan fields in the plan's canonical medium: `Review boundary: phase|final`, `Final phase`, `Commit authority`, and each phase's `Review status` and `Review evidence`. For a native plan, use the final phase's exact issue ID. Pass that whole-engagement contract, plan reference and exact phase/task/subtask cursor into every nested invocation. Missing or inconsistent executing mappings block dependent dispatch; workflow owns their validation. Nested goals never reset the boundary or relabel intermediate output as final.

| Reached boundary | Required action |
|---|---|
| Subtask end | The implementer runs the smallest focused discriminating check and necessary touched-file lint/type/build; record its issue evidence. |
| Task end | The task owner runs bounded task-acceptance selectors across its subtasks, citing still-valid coverage; record its issue evidence. |
| Phase implementation end | Reconcile lane diffs and focused evidence. Collect missing phase checks through Stage C. Record phase test evidence without claiming independent acceptance. |
| Declared phase review end | Reconcile that phase's complete diff. Run the verification that its tasks' decisions and the floors require, and triage findings under Findings above before acceptance. |
| Whole-engagement final end | Reconcile the complete candidate. Run the verification that the decisions and the floors require, fix the findings triaged for fixing in one planned repair batch, and collect required retests and final checks. |

- Never dispatch independent subtask/task review.
- Under `Review boundary: final`, intermediate phases retain `REVIEW_PENDING`; tested issue closure advances readiness without claiming reviewed acceptance. Defer independent acceptance until that boundary.
- Under `phase`, only the declared phase end earns review.
- Preserve stricter genuine repository gates and necessary focused feedback. If a required earlier gate conflicts with the declared boundary, return the conflict to the plan owner rather than silently skipping either rule.

Local commits follow the main instruction file's local-commit rule through `alaa-workflow references/workspace-and-integration.md`. Its `## Lane branches and commits` owns the lane branch, lane commits, the merge and the lead's own commits:

- Implementation and documentation lanes commit their owned paths on the lane branch their dispatch names, when their focused checks pass, at any phase, including before final review.
- The integration parent commits work that no lane owns, and work a lane returned uncommitted after its focused checks passed, as it lands.
- A commit is a checkpoint, not acceptance; record review status separately.
- Reuse applicable standing authority without another approval.
- Preserve an identified snapshot when authority or validation is missing.
- Pending review never delays a lane's or the parent's authorized checkpoint.
- Under `Review boundary: final`, later ready sets continue on the same lane branch. The parent merges it once, after the final boundary accepts it under the rule below. A fix after that merge follows `## Lane branches and commits` step 7.
- Under `Review boundary: phase`, the parent merges the lane branch at each phase's review, after that boundary accepts it.
- The documenter's lane branch is created after the last implementation merge. It merges after the Stage E documentation gate accepts it and before the Stage E final validation.
- A boundary accepts a lane branch when the verification its tasks' decisions and the floors require has passed. Without an independent review there, the lead records its own verdict and the accepted evidence with its reason in `Review status` and `Review evidence`.
- Push, tag, history rewrite and any merge other than the lane-branch merge still require explicit permission.

In Codex, the `workspace-write` sandbox keeps `.git` read-only, so a Git write from inside that sandbox is expected to fail; this is an inference from the read-only path, not documented behaviour. `alaa-prompting-guide references/11-codex-runtime-features.md` owns the read-only path fact. Record the lane branch in the plan, set the dispatch's `<commit>` field to none, and commit each lane's returned work under step 9 of `## Lane branches and commits`. Grant commit authority to a Codex lane only when the active sandbox lets it write `.git`. The lead creates the lane branch, merges and commits through the host's approval path for writes outside the sandbox. When that path is unavailable, the lead records the snapshot and reports the work uncommitted.

Nested invocations return tested evidence, their lane commits and branch, pending review and merge work, and the next cursor. Stage C collects focused phase evidence. Stage D waits for the inherited review boundary. When required checks need whole-engagement breadth, plan one whole-engagement broad gate stage in Stage E, after final documentation. Phase transitions earn no broad pass. Earlier required repository gates follow the conflict rule above.

## Before any dispatch

1. Inspect relevant repository guidance (`AGENTS.md`, local instructions, architecture docs, package manifests, CI, tests, and affected code paths).
2. Restate internally: desired outcome; checkable acceptance criteria; constraints and preserved behavior; out-of-scope work; irreversible or externally visible actions.
3. Draw the fewest lanes that keep write scopes disjoint and buy real parallelism.
   - Give each lane one concrete outcome, owned files or modules, exclusions, acceptance criteria in the dispatch envelope's criterion shape, focused commands, dependencies, resolved skill bindings under `alaa-workflow references/companion-routing.md` including its matching clean-code owner, and a return shape with a line bound.
   - Split a lane only for one of these reasons: a disjoint write scope run in parallel, a different owning skill or authority, a different task model or effort, or work that exceeds one agent's context. Sequential work in one scope stays one lane, because each extra lane adds a dispatch, a context transfer and a reconciliation.
   - The lane, not the subtask, is the dispatch unit. One dispatch carries every subtask of a task that shares one registered profile and owning skill, and that agent runs the task-acceptance selectors at its end.
   - Before implementation or fix dispatch, classify actual command scope, never tier labels. Then send focused commands to subtask workers and explicitly bounded task-acceptance commands to the task owner, and reserve affected/exhaustive commands for boundary gates. A focused command is the topic selector that `/alaa-testing-strategy` names.
4. Apply `alaa-workflow references/workspace-and-integration.md` for its rule of one writer per file, generated output or shared resource, and for stopped-writer recovery. Lanes with disjoint files may share the current checkout. Do not create a worktree automatically. Before the first implementation or documentation dispatch of a ready set, create or continue the lane branch that file's `## Lane branches and commits` prescribes, and name it in each write-lane dispatch.

## Reusable-context owner

Apply `alaa-workflow references/context-curation.md` at material boundaries and at closure. Workflow owns scan timing, candidate location and gate reopening. The lessons skill owns admission, and the memory skill owns authorized publication. Consume the recorded outcome once, including when this run is a child phase.

## Stage A — Plan

Always first, never skipped, because every lane inherits its decisions.

1. Before the first write, apply `alaa-workflow references/workspace-and-integration.md` `## Before the first write` and use its current-checkout or isolation decision.
2. Dispatch the specification, exploration, and research lanes whose conditions in `references/routing-matrix.md` hold, in parallel only when their questions are independent.
3. Reconcile observed facts and label unresolved assumptions. Then select the planning profile through `routing-matrix.md` before you make the plan.
4. Run a capability inquiry before you approve a new container image, toolchain, chart, CI include or template, generator, hook pack, or script reused across repositories or pipelines. An edit to an existing artifact is out of scope. The inquiry is required because this tree cannot establish what another owner already provides.
   1. Read any /alaa-services-contract infrastructure registry first, and reuse sufficient current evidence.
   2. Apply the /alaa-memory-os capability inquiry.
   3. Record the verified owner or alternative and its evidence in the workflow plan and the lane `<context>`. When the memory owner returns a scoped unavailable or unknown outcome, record that outcome instead. Empty recall never justifies `none` infrastructure.
   4. A verified alternative enters step 5 as reuse-or-extend. Rejecting it for a parallel artifact requires its owner's or the user's decision.

   Use the same memory-owned inquiry before local absence becomes a validation blocker, and when a permitted additional repair has an unresolved owner; then return to the runtime recovery owner. The lookup adds no retry and no native status authority.
5. Decide the solution before decomposing it. Name the chosen approach and each rejected alternative with the reason it was rejected. Where the goal stores, indexes, caches, or moves data, decide the representation and the access path with `/alaa-data-layer`. Where a path grows with tenants, rows, history, or events, state its complexity bound with `/alaa-algorithms-data-structures`. Run the design pass under `/alaa-system-design` when that skill's conditions hold; `references/routing-matrix.md` names the three conditions it adds beyond the architecture critic's own triggers.
6. Record the architecture-critic trigger whenever `references/routing-matrix.md` or step 5 requires it. Complete the design record before implementation, also when the change meets the adversarial reviewer's blast-radius condition, because an irreversible change has no cheap second attempt.
7. Record known API-contract triggers and decide consumer impact, compatibility and deprecation before implementation.
8. Use `alaa-test-strategist` before implementation, not after, whenever its condition in `references/routing-matrix.md` holds: a test matrix designed after the code exists is written against what was built rather than against what the change had to prove.
9. Record the plan through /alaa-workflow or adopt the existing parent plan. Record ordered phases, acceptance, focused phase checks, the final gate and handoff knowledge. Use `alaa-workflow references/context-continuity.md` for canonical position and resume. Apply `alaa-workflow references/companion-routing.md` for executable phase/task skill bindings before implementation or write-lane dispatch. Workflow owns this machinery; the orchestrator consumes it without duplicating task state.
10. Run Batch allocation from `references/routing-matrix.md`, record all lane choices in the workflow plan, and create no second allocation artifact. Present the plan and the decisions in one compact message, then continue without waiting. Wait only when an irreversible decision, destructive action, external side effect, or genuine product choice belongs to the user.

## Stage B — Implementation

1. Select the managed implementation profile or admitted external role through `references/routing-matrix.md` before assignment or reassignment, then dispatch one agent per ready lane. Carry the selection evidence in the dispatch and the roster.
2. Take dependencies and readiness from the selected task authority and the phase barriers. Take write ownership and shared-resource conflicts from the workflow plan. A lane is ready only after its required dependency contracts are reconciled. Dispatch ready independent lanes together when observed host slots and declared resource ceilings permit. Increase parallel writers when capacity and ready work justify it. When capacity is not observable, record that and use the smallest supported batch until capacity is established. Do not invent a ceiling or assume unlimited capacity.
3. Reconcile at declared integration barriers before dependent work starts. Reserve capacity for the next required gate only when it is ready.
4. Lanes run the subtask-end and task-end checks of the cadence table above and no boundary affected/exhaustive check. Choose the smallest discriminating checks for the claimed behavior and for changed exported-surface, contract, type or lint properties. Return the observed output, or mark the property not checked. Role definitions own dispatch-conflict handling; reconcile every excluded command and unrun check before accepting the lane.
5. Wait for all required lanes. A blocked lane is blocked; do not pad it into success.
6. Reconcile actual diffs and lane evidence, not summaries alone. Detect scope violations, accidental generated changes, contract mismatches, and cross-lane breakage. Record observed task progress and tested closure through `alaa-workflow references/task-tracking.md`.

## Stage C — Verification

1. At phase implementation end, reconcile focused lane and task evidence against the phase's acceptance criteria. Collect only missing or invalidated focused checks and explicit earlier repository obligations. Apply each task's verification decision and the floors to the reconciled candidate. When the decision or a floor names an independent verifier, collect missing, invalidated or required-fresh coverage through `alaa-verifier`.
2. When independent checks remain to run, dispatch `alaa-verifier` with the exact consolidated commands, cwd, timeout, artifact directory and resource policy derived through /alaa-testing-strategy `references/110-execution-resources.md`. Use only host-exposed dispatch and continuation mechanisms. Under Codex, route Docker socket permission failures through /alaa-codex-runtime-ops before the canonical host fallback.
3. Route classified results through Failure routing in `references/routing-matrix.md`.
4. After batch repair, apply After a fix and the canonical retest procedure.

## Stage D — Review and specialist gates

1. At the inherited review boundary, once Check collection above lets review start, dispatch the independent review and specialist gates that the tasks' decisions and the floors require, against the complete diff and lane plan. Spawn the one correctness reviewer the routing matrix selects: `alaa-reviewer` or `alaa-reviewer-deep`. When a decision chose the lead's own diff reading, it happens at the same point.
2. Spawn `alaa-adversarial-reviewer` only when its condition in `references/routing-matrix.md` holds. Its conflicting-judgment arm, discovered here, fires without resetting the inherited boundary.
3. `APPROVED` and `APPROVED-WITH-NITS` proceed. Under `CHANGES-REQUESTED`, route each finding triaged for fixing verbatim to the hand Who fixes selects.
4. Present every finding this phase leaves open for the user as one decision set: each item with its severity per lens, the smallest fix that closes it, and what closing it costs. Ask once, because each separate answer can move the tree and invalidate final evidence, including a required exhaustive run.

For required Ent review, interpret the native report under `alaa-ent-go-orm-db references/85-specialist-delegation.md`. `STATUS: COMPLETE` means the assessment finished. It grants no approval. A missing report, `STATUS: BLOCKED`, `STATUS: INCOMPLETE` or missing required evidence blocks acceptance even without findings.

## Stage E — Documentation and final validation

1. Spawn `alaa-documenter` when its condition in `references/routing-matrix.md` holds. It is the final write lane, so every check below runs after it.
2. After documentation edits, run the documentation gate below and report the size grade it measures.
3. Run the final validation in this order:
   1. If integration is requested and explicitly authorized, bring the base branch into the work branch before final verification. Otherwise keep the current candidate as the verification target, and mark integration as not requested or as awaiting authority.
   2. Freeze the final candidate. Record its content snapshot and any integrated base commit.
   3. Select required checks and proof from repository policy and /alaa-testing-strategy.
   4. Collect required affected and exhaustive checks in one whole-engagement gate stage. Run any required exhaustive tier once, fresh on the final candidate after documentation.
   5. If a result blocks acceptance, apply After a fix and the existing retry budget.
4. Consume the workflow owner's final reusable-context gate after evidence is stable; an empty retained set is valid. Follow its `pipeline reopen required` outcome before closure.
5. Re-check the final Git status and diff against the declared scopes. Confirm that canonical task progress and workflow status match what landed. Record the last authorized commit timestamp when available; otherwise record it as unavailable.
6. Report in the order `SKILL.md` states, and audit every claim against an actual tool result from this session before reporting it.

## Stage F — Requested integration

This phase applies only when the user requests integration. A local-only request completes after Stage E without a merge prompt. Run requested integration through `alaa-workflow references/workspace-and-integration.md` `## The integration handshake`, and reuse existing explicit authorization for the exact operation. If the base advanced after final verification, rerun the required final gates on the changed candidate.

## Documentation gate

Documentation changes, written after code review, require at least:

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
- the verification that each task's decision and the floors require is complete; every finding has a recorded disposition, each finding triaged for fixing is fixed and proven, and each blocking floor-gate finding is confirmed fixed by that gate or explicitly accepted by the user;
- final touched files match authorized scopes;
- documentation ran or was explicitly skipped for a grounded reason;
- the final reusable-context pass reported persisted, deferred, rejected, or no admitted candidates;
- no `pipeline reopen required` result remains unresolved;
- canonical task progress and workflow status match what landed; every changed subtask has tested diff evidence and the declared boundary has attributable verification evidence; local checkpoints follow the main instruction rule independently of review status;
- requested integration is complete or explicitly reported declined/blocked; local-only work needs no integration prompt;
- no destructive/external action was performed without authorization.
