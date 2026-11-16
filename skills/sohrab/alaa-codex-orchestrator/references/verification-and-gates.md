# Verification and Gate Policy

Stages A-F give the order of work. The verification decision and the floors below set which checks and reviews run inside them. They are distinct from workflow phases.

## The verification decision

The lead decides how much verification each change needs; no fixed pipeline applies. Decide once per task at plan time, in one or two lines in the plan or compact dispatch. Revisit the decision only when the task changes materially.

1. What can be wrong that the author's own focused check would not show: effects in other modules, concurrency, contract consumers, a trust boundary, data?
2. What does a miss cost, and can it be undone: blast radius, reversibility, exposure of production data, tenants, money or a public contract?
3. What evidence exists, and does it hold for this snapshot: who observed it, on which inputs, and did anything it covers change since?
4. What is the cheapest check that could prove the change wrong? Run that one. Stop adding checks when the next one could not change the decision.

Then choose per task: accept the author's observed focused evidence, read the diff yourself, have `alaa-verifier` run named checks, or dispatch an independent reviewer or specialist gate. An independent observer needs a reason drawn from questions 1 and 2: what it can see that the author cannot, or what the miss would cost. "The pipeline says so" is not a reason.

- A specialist trigger in `references/routing-matrix.md` that holds on a floor surface makes that specialist the required gate. Elsewhere it informs question 1, and it dispatches its specialist only with the reason the decision states.
- An owed affected or exhaustive check runs through `alaa-verifier`, or through the lead when its output is short enough to read in full.
- The declared review boundary sets when an independent review runs. A boundary where no task chose an independent observer and no floor applies earns no review dispatch.

## Floors

An independent gate is always required, whatever the decision says, for a change to:

- authentication, authorization or tenant isolation;
- secrets or cryptography;
- billing or money;
- a destructive or irreversible data operation, including a migration that drops or rewrites data;
- a breaking change to a public contract;
- a production deployment or release;
- any surface the user asks to have reviewed.

On a floor surface the author never approves its own work. The gate's blocking verdict binds the lead. Implementer evidence does not replace the gate. `alaa-reviewer` is the gate on a floor surface that no specialist trigger covers, including a review the user asks for.

## Evidence

Observed evidence counts by what it shows, not by who ran it. Outside the floors, the lead may accept an implementer's observed focused check on the same snapshot, and records that it did. Re-run a check independently only on a floor surface, or when its evidence is stale, unobserved or ambiguous. Check nothing unchanged again.

Where a floor or the decision requires independent acceptance, it requires an observer independent of the implementation with authority for that gate. An implementer's broad PASS cannot discharge it. Record the observer with the evidence; cite eligible independent evidence instead of repeating it.

## Findings

Triage every finding by its consequence under `alaa-workflow references/review-mode.md` `## Finding triage`.

## After a fix

Whoever fixes proves the fix with the check that failed, or with the check that would have caught the defect. A fix that touches a floor surface returns to that floor's gate, which judges the fix, not the whole change again. Any other further review needs a stated reason: the fix changed the design, or the first review could not see what it needed. There is no cycle count. A new round needs a new reason. When a second round finds blocking findings of the same kind, stop repairing and reconsider the approach or the decomposition: a returning defect class points at the plan, not the patch. Tell the user when you cannot resolve that yourself.

## Who fixes

Use the smallest capable hand. The lead may make a small, local, obvious correction itself when that is cheaper than a dispatch, inside the authorized scope, in files no active or pending lane owns. The implementer that holds the context continues for anything larger. Read-only roles stay read-only. A diagnosis may carry the proposed fix.

Keep one collected repair batch, because each separate repair pays its own context transfer and retest. Split it only where repair role authority differs, into the fewest compatible scoped assignments. For each assignment, continue the existing implementer whose valid assignment and context cover most failures through a host-supported continuation tool. Dispatch fresh only when continuation is unavailable, context is invalid, or `routing-matrix.md` selects another managed profile, external role or task pair. Execute the assignments serially and reconcile conflicting writers through `alaa-workflow references/workspace-and-integration.md` before continuing. Existing retry/stop budgets remain in force.

## Check collection

Load /alaa-testing-strategy before you build, run, repair or cite checks. Read its `references/100-test-execution.md` for the command list, collection, repair, retest and evidence, its `references/110-execution-resources.md` before a resource or timing decision, and its `references/120-result-classification.md` before you classify or repair a result.

Record the check list and evidence at the workflow-selected owner before dispatch. Review waits until required pre-review collection, batch repair and retests pass. The canonical minimal early-repair exception returns to collection without review. Freeze the tested scope through `alaa-workflow references/workspace-and-integration.md` before verification; evidence needs no commit. Never weaken review to obtain a pass.

## Review boundary and execution cadence

Before dispatch, read `alaa-workflow references/task-tracking.md` for task-store selection, plan resolution, registration, phase evidence and closure.

Read a native `beads:<root-id>` plan through the bound issue store, with no Markdown prerequisite, and a Markdown plan through its admitted file family. Verify live registration, hierarchy, prerequisite edges, resolved skills and readiness through the recorded store.

Read these plan fields: `Review boundary: phase|final`, `Final phase`, `Commit authority`, and each phase's `Review status` and `Review evidence`. A native plan may have no phase milestone: `Final phase` then names the root, and the root is the one phase for the phase rules of this file. Pass that whole-engagement contract, plan reference and exact phase/task/subtask cursor into every nested invocation. Missing or inconsistent executing mappings block dependent dispatch. Nested goals never reset the boundary or relabel intermediate output as final.

| Reached boundary | Required action |
|---|---|
| Subtask end | The implementer runs the smallest focused discriminating check and necessary touched-file lint/type/build; record its issue evidence. |
| Task end | The task owner runs bounded task-acceptance selectors across its subtasks, citing still-valid coverage; record its issue evidence. |
| Phase implementation end | Reconcile lane diffs and focused evidence. Collect missing phase checks through Stage C. Record phase test evidence without claiming independent acceptance. |
| Declared phase review end | Reconcile that phase's complete diff. Run the verification that its tasks' decisions and the floors require, and triage findings before acceptance. |
| Whole-engagement final end | Reconcile the complete candidate. Run the verification that the decisions and the floors require, fix the findings triaged for fixing in one planned repair batch, and collect required retests and final checks. |

- Never dispatch independent subtask/task review.
- Under `Review boundary: final`, intermediate phases retain `REVIEW_PENDING`, and independent acceptance waits for that boundary.
- Under `phase`, only the declared phase end earns review.
- Preserve stricter genuine repository gates and necessary focused feedback. If a required earlier gate conflicts with the declared boundary, return the conflict to the plan owner rather than silently skipping either rule.

Local commits follow the main instruction file's local-commit rule through `alaa-workflow references/workspace-and-integration.md`. Its `## Lane branches and commits` owns the lane branch, lane commits, the merge and the lead's own commits. This file sets only the merge timing:

- Under `Review boundary: final`, later ready sets continue on the same lane branch, and the parent merges it once, after the final boundary accepts it.
- Under `Review boundary: phase`, the parent merges the lane branch at each phase's review, after that boundary accepts it.
- Create the documenter's lane branch after the last implementation merge. Merge it after the Stage E documentation gate accepts it and before the Stage E final validation.
- A boundary accepts a lane branch when the verification that its tasks' decisions and the floors require has passed. Without an independent review there, the lead records its own verdict and the accepted evidence with its reason in `Review status` and `Review evidence`.
- Push, tag, history rewrite and any merge other than the lane-branch merge still require explicit permission.

Nested invocations return tested evidence, their lane commits and branch, pending review and merge work, and the next cursor. Stage C collects focused phase evidence. Stage D waits for the inherited review boundary. Phase transitions earn no broad pass.

In Codex, the `workspace-write` sandbox keeps `.git` read-only, so a Git write from inside that sandbox is expected to fail; this is an inference from the read-only path, which `alaa-prompting-guide references/11-codex-runtime-features.md` owns, not documented behaviour. Record the lane branch in the plan, set the dispatch's `<commit>` field to none, and commit each lane's returned work as the lead under `## Lane branches and commits`. Grant commit authority to a lane only when the active sandbox lets it write `.git`. The lead creates the lane branch, merges and commits through the host's approval path for writes outside the sandbox. When that path is unavailable, the lead records the snapshot and reports the work uncommitted.

## Before any dispatch

1. Draw the fewest lanes that keep write scopes disjoint and buy real parallelism.
   - Give each lane one outcome, owned files or modules, exclusions, acceptance criteria in the envelope's criterion shape, focused commands, dependencies, resolved skill bindings under `alaa-workflow references/companion-routing.md` including its matching clean-code owner, and a bounded return shape.
   - Split a lane only for a disjoint write scope run in parallel, a different owning skill or authority, a different task model or effort, or work that exceeds one agent's context. Sequential work in one scope stays one lane, because each extra lane adds a dispatch, a context transfer and a reconciliation.
   - The lane, not the subtask, is the dispatch unit. One dispatch carries every subtask of a task that shares one registered profile and owning skill, and that agent runs the task-acceptance selectors at its end.
   - Before implementation or fix dispatch, classify actual command scope, never tier labels. Then send focused commands to subtask workers and explicitly bounded task-acceptance commands to the task owner, and reserve affected/exhaustive commands for boundary gates.
2. Apply `alaa-workflow references/workspace-and-integration.md` for one writer per file, generated output or shared resource, for checkout sharing and for stopped-writer recovery. Before the first implementation or documentation dispatch of a ready set, create or continue the lane branch under that file's `## Lane branches and commits`, and name it in each write-lane dispatch.

## Reusable-context owner

Apply `alaa-workflow references/context-curation.md` at material boundaries and at closure. Consume the recorded outcome once, also when this run is a child phase.

## Stage A — Plan

Stage A always runs first.

1. Before the first write, apply `alaa-workflow references/workspace-and-integration.md` `## Before the first write` and use its current-checkout or isolation decision.
2. Dispatch the specification, exploration and research lanes whose `references/routing-matrix.md` conditions hold, together when their questions are independent.
3. Reconcile observed facts and label unresolved assumptions. Then select the planning profile through `routing-matrix.md`.
4. Run a capability inquiry before you approve a new container image, toolchain, chart, CI include or template, generator, hook pack, or script reused across repositories or pipelines, because this tree cannot show what another owner already provides. An edit to an existing artifact is out of scope.
   1. Read any /alaa-services-contract infrastructure registry first, and reuse sufficient current evidence.
   2. Apply the /alaa-memory-os capability inquiry.
   3. Record the verified owner or alternative and its evidence in the workflow plan and the lane `<context>`, or the memory owner's scoped unavailable or unknown outcome. Empty recall never justifies `none` infrastructure.
   4. A verified alternative enters step 5 as reuse-or-extend. Rejecting it for a parallel artifact requires its owner's or the user's decision.

   Use the same inquiry before local absence becomes a validation blocker, and when a permitted additional repair has an unresolved owner. The lookup adds no retry and no native status authority.
5. Decide the solution before decomposing it. Name the chosen approach and each rejected alternative with its reason. Where the goal stores, indexes, caches or moves data, decide the representation and the access path with `/alaa-data-layer`. Where a path grows with tenants, rows, history or events, state its complexity bound with `/alaa-algorithms-data-structures`. Run the design pass under `/alaa-system-design` when that skill's conditions hold.
6. Record the architecture-critic trigger whenever `references/routing-matrix.md` or step 5 requires it. Complete the design record before implementation, also when the change meets the adversarial reviewer's blast-radius condition, because an irreversible change has no cheap second attempt.
7. Record known API-contract triggers and decide consumer impact, compatibility and deprecation before implementation.
8. Use `alaa-test-strategist` before implementation whenever its condition in `references/routing-matrix.md` holds.
9. Record the plan through /alaa-workflow, or adopt the existing parent plan, and keep task state there only. Apply `alaa-workflow references/companion-routing.md` for executable phase/task skill bindings before implementation or write-lane dispatch.
10. Run Batch allocation from `references/routing-matrix.md` and record all lane choices in the workflow plan; create no second allocation artifact. Present the plan and the verification decisions in one compact message and continue without waiting, unless an irreversible decision, destructive action, external side effect or genuine product choice belongs to the user.

## Stage B — Implementation

1. Dispatch one agent per ready lane, with the profile or admitted external role that `references/routing-matrix.md` selects and its selection evidence in the dispatch and the roster.
2. A lane is ready only after its required dependency contracts are reconciled and the workflow plan shows no write-ownership or shared-resource conflict. Dispatch ready independent lanes together when observed host slots and declared resource ceilings permit. When capacity is not observable, record that and use the smallest supported batch until capacity is established. Invent no ceiling and assume no unlimited capacity.
3. Reconcile at declared integration barriers before dependent work starts.
4. Lanes run the subtask-end and task-end checks of the cadence table and no boundary affected/exhaustive check; reconcile every excluded command and unrun check before accepting the lane.
5. Reconcile actual diffs and lane evidence, not summaries alone, to detect scope violations, accidental generated changes, contract mismatches and cross-lane breakage. Report a blocked lane as blocked, never as success. Record observed task progress and tested closure through `alaa-workflow references/task-tracking.md`.

## Stage C — Verification

1. At phase implementation end, reconcile focused lane and task evidence against the phase's acceptance criteria. Collect only missing or invalidated focused checks and explicit earlier repository obligations. Apply each task's verification decision and the floors to the reconciled candidate.
2. When the decision or a floor names an independent verifier, collect missing, invalidated or required-fresh coverage through `alaa-verifier`. Dispatch it with the exact consolidated commands, cwd, timeout, artifact directory and resource policy derived through /alaa-testing-strategy `references/110-execution-resources.md`.
3. Route classified results through Failure routing in `references/routing-matrix.md`.
4. After batch repair, apply After a fix and the canonical retest procedure.

## Stage D — Review and specialist gates

1. At the inherited review boundary, once Check collection lets review start, dispatch the independent review and specialist gates that the tasks' decisions and the floors require, against the complete diff and lane plan. Spawn the one correctness reviewer that the routing matrix selects: `alaa-reviewer` or `alaa-reviewer-deep`. A diff reading by the lead that a decision chose happens at the same point.
2. Spawn `alaa-adversarial-reviewer` only when its condition in `references/routing-matrix.md` holds. Its conflicting-judgment arm, discovered here, fires without resetting the inherited boundary.
3. `APPROVED` and `APPROVED-WITH-NITS` proceed. Under `CHANGES-REQUESTED`, route each finding triaged for fixing verbatim to the hand Who fixes selects.
4. Present every finding this phase leaves open for the user as one decision set: each item with its severity per lens, the smallest fix that closes it, and its cost. Ask once, because each separate answer can move the tree and invalidate final evidence.

For required Ent review, interpret the native report under `alaa-ent-go-orm-db references/85-specialist-delegation.md`. Its `STATUS: COMPLETE` means the assessment finished and grants no approval. A missing report, `STATUS: BLOCKED`, `STATUS: INCOMPLETE` or missing required evidence blocks acceptance even without findings.

## Stage E — Documentation and final validation

1. Spawn `alaa-documenter` when its `references/routing-matrix.md` condition holds. It is the final write lane; every check below runs after it.
2. After documentation edits, run the documentation gate below and report the size grade it measures.
3. Run the final validation in this order:
   1. If integration is requested and explicitly authorized, bring the base branch into the work branch before final verification. Otherwise verify the current candidate, and mark integration as not requested or awaiting authority.
   2. Freeze the final candidate. Record its content snapshot and any integrated base commit.
   3. Collect required affected and exhaustive checks in one whole-engagement gate stage. Run any required exhaustive tier once, fresh on the final candidate after documentation.
   4. If a result blocks acceptance, apply After a fix and the existing retry budget.
4. Consume the workflow owner's final reusable-context gate after evidence is stable; an empty retained set is valid. Follow its `pipeline reopen required` outcome before closure.
5. Check the final Git status and diff against the declared scopes, and that task progress and workflow status match what landed.

## Stage F — Requested integration

A local-only request completes after Stage E without a merge prompt. Run requested integration through `alaa-workflow references/workspace-and-integration.md` `## The integration handshake`, and reuse existing explicit authorization for the exact operation. If the base advanced after final verification, rerun the required final gates on the changed candidate.

## Documentation gate

Documentation changes, written after code review, require at least:

- final diff scope check;
- repository docs formatter/linter when available;
- touched-link validation when available;
- example/config snippet validation when safely supported;
- spot-check against verified behavior;
- the size grade that `alaa-repo-docs references/15-document-size-and-clustering.md` requires, measured with `alaa-repo-docs scripts/check_markdown_links.py` in its line-budget mode. Consume that result; do not judge the grade here. Its exit `1` on an unapproved document at the largest grade is a failed gate, and its exit `2` proves nothing.

## Final success criteria

Report completion only when the stop conditions in `SKILL.md` hold and also:

- every acceptance criterion maps to evidence marked run, cited, or review-only with its review evidence; run or cited evidence carries its tier;
- required final checks and proof levels passed on the final candidate, with no unverified candidate change afterward, and no mandatory command is failed, flaky, timed out, blocked or contaminated;
- the verification that each task's decision and the floors require is complete, with attributable evidence at the declared boundary;
- every finding has a recorded disposition, each finding triaged for fixing is fixed and proven, and each blocking floor-gate finding is confirmed fixed by that gate or explicitly accepted by the user;
- no `pipeline reopen required` result remains unresolved;
- every changed subtask has tested diff evidence;
- no destructive or external action was performed without authorization.
