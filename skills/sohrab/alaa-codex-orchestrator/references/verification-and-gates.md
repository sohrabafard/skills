# Execution Pipeline and Gate Policy

`SKILL.md` carries the phase table, the execution profiles, and the authority boundaries. This file
owns what each phase actually does and what each gate requires. Read it before dispatching Stage A,
and again whenever a gate's requirement is in question.

Stages A-F name required orchestration outcomes and authority, not workflow phases, separate meetings, dispatches, artifacts or repeated checks. Coalesce compatible actions and evidence in the workflow plan; retain each outcome, observer and ordering constraint. Gate economics below orders collection, batch repair and retest before review.

## Review boundary and execution cadence

This pair owns scheduling; /alaa-workflow owns hierarchy, cursor and review evidence; /alaa-testing-strategy owns test necessity, breadth and proof strength. Consume `alaa-workflow references/task-tracking.md` sections `Phase-task-subtask hierarchy`, `Acceptance and evidence by level` and `Close reason` before dispatch.

New phased/delegated work uses the bound Beads phase-task-subtask hierarchy; never create a fresh flat phased plan. Verify its live registration, parent-child relations, prerequisites and readiness through the bound owner. Existing unmarked/local families retain their original contract until explicit migration.

Read the plan's `Review boundary: phase|final`, `Final phase`, `Commit authority` and phase `Review status`/`Review evidence`. Pass that whole-engagement contract, plan reference and exact phase/task/subtask cursor into every nested invocation. Missing or inconsistent executing mappings block dependent dispatch; workflow owns their validation. Nested goals never reset the boundary or relabel intermediate output as final.

| Reached boundary | Required action |
|---|---|
| Subtask end | The implementer runs the smallest focused discriminating check and necessary touched-file lint/type/build; record its issue evidence. |
| Task end | The task owner runs bounded task-acceptance selectors across its subtasks, citing still-valid coverage; record its issue evidence. |
| Phase implementation end | Reconcile all lane diffs and evidence, then run Stage C's centralized collection and repair barrier, even under final-only review; record phase test evidence without claiming independent acceptance. |
| Declared phase review end | Reconcile that phase's complete diff, required independent verification, correctness review and triggered specialists; triage findings under `alaa-workflow references/review-mode.md` `## Finding triage`, fixing blocking ones and retesting before acceptance. |
| Whole-engagement final review end | Reconcile all remaining phases as one complete candidate; run the required independent review, one fix pass covering its findings and every deferred finding, then retests and final gates. |

Never dispatch independent subtask/task review or make a subtask/task commit. Under `Review boundary: final`, intermediate phases retain `REVIEW_PENDING`; tested issue closure advances readiness without claiming reviewed acceptance. Defer independent acceptance and commits until that boundary. Under `phase`, only the declared phase end earns review. Preserve stricter genuine repository gates and necessary focused feedback; if a required earlier gate conflicts with the declared boundary, return the conflict to the plan owner rather than silently skipping either rule.

At an authorized review boundary, successful required review, accepted fixes and retests trigger the integration parent's Conventional Commit on the current branch, limited to its owned candidate. Reuse a recorded standing user grant; do not invent another approval. Without that grant, or after failed review/tests, preserve an identified uncommitted snapshot and report pending authority or failure. `alaa-workflow references/workspace-and-integration.md` owns the commit protocol. Worker roles never gain commit authority.

Nested invocations complete applicable stage outcomes and return tested evidence, pending review/commit and the next cursor. Stage C runs at each phase implementation end; Stage D and final E gates wait for the inherited boundary. The exhaustive tier belongs only to the whole engagement's final candidate after final documentation when required; an intermediate phase may complete its local documentation without claiming final proof.

## Plan and allocation

Apply `routing-matrix.md` for planning controls and the single post-consolidation worker allocation pass. Persist choices in the workflow plan before dispatch; no second allocation artifact.

## Before any dispatch

1. Inspect relevant repository guidance (`AGENTS.md`, local instructions, architecture docs, package manifests, CI, tests, and affected code paths).
2. Restate internally: desired outcome; checkable acceptance criteria; constraints and preserved behavior; out-of-scope work; irreversible or externally visible actions.
3. Split into the smallest practical disjoint lanes, each with one concrete outcome, owned files/modules, exclusions, acceptance criteria, focused commands, dependencies, resolved skill bindings under `alaa-workflow references/companion-routing.md` including its matching clean-code owner, and return shape/line bound. Before implementation or fix-cycle dispatch, classify actual command scope, never tier labels; send focused commands to subtask workers and explicitly bounded task-acceptance commands to the task owner; reserve affected/exhaustive commands for boundary gates; a focused command is the topic selector `/alaa-testing-strategy` names.
4. Serialize lanes that overlap in files, data contracts, generated output, migrations, or runtime state — or run them under worktree isolation and merge deliberately.

`references/routing-matrix.md` owns every specialist trigger; `references/delegation-prompts.md` owns
the dispatch contracts.

## Gate economics

Retain required retrieval, focused implementer checks and independent acceptance gates. Remove repetition only without new changes, failures or unresolved concerns. Model capability never waives an observer or mandatory gate.

Schedule gates by the collection barrier below, regardless of cost. Repository validation policy overrides this section within its repository; `/alaa-testing-strategy` owns that precedence.

Before validation dispatch, record one check list in the existing plan: required gates, exact scoped inputs and commands, aggregate-to-child coverage, observer, and eligible evidence citations. Inspect aggregate execution; a wrapper's name proves no coverage. Run an aggregate instead of its identical covered children only when inputs, environment, flags and required independent authority match. Run uncovered gates separately; report partial coverage. Count underlying checks once, not wrapper and child as separate passes. Phase transitions and new agents alone earn no rerun. A required final exhaustive aggregate discharges covered narrower checks only when covered inputs, environment, flags and required observer match demonstrably; preserve focused feedback and run uncovered checks. Markdown and templates can be checker inputs: documentation-only change proves no equivalence. Evidence quality below owns reuse; /alaa-testing-strategy owns stricter proof and fresh exhaustive gates. Preserve mandatory checks and changed-input reruns; run checker self-tests only when checker logic changes. The gates of one pass consume one build, compile, render or image per tree state; a dispatch that rebuilds what an earlier gate of the pass produced is corrected before it runs.

1. **Collect before repair.** After merging or reconciling phase diffs, run every required runnable phase check centrally once through `alaa-verifier`, reusing eligible covered evidence. A failure does not cancel independent remaining checks. Record each command's exit/result and each unrun check's blocker. A fail-fast aggregate proves only executed coverage: dispatch its supported keep-going mode or exact uncovered child commands; preserve failure exits.
2. **Repair as one batch, then retest, then Review.** Combine the full collection's failures verbatim into one serialized fix lane with explicit scope/ownership; retire conflicting writers. Classify first, use the failure analyst for ambiguous ownership and preserve environment/security authority limits. Only a failure blocking all or most remaining checks permits a minimal early repair: record blocked checks and cause, repair only that obstruction, then run or resume all required checks, including previously blocked checks, before any Review. Invalidate affected evidence. After batch repair, independent verification reruns failed and invalidated checks before Stage D. Unresolved required checks block Review and acceptance. Keep existing retry/stop budgets; never weaken tests or review to obtain a pass.
3. **Freeze before verifying.** Pin a content snapshot of tracked diff, relevant untracked files and tool inputs, and prevent concurrent writes; commit only after the authorized boundary has passed. Evidence needs no commit. `alaa-workflow references/workspace-and-integration.md` owns the commit protocol and forbidden writes during a pass.

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
9. Write the plan through `/alaa-workflow` at the `resumable` profile or adopt the existing parent plan. It records ordered phases, acceptance, per-phase validation, and handoff knowledge. Follow `alaa-workflow references/task-tracking.md` for selected-store task records and evidence-based progress; use `alaa-workflow references/context-continuity.md` for canonical position and resume. Apply `alaa-workflow references/companion-routing.md` for executable phase/task skill bindings before implementation or write-lane dispatch. Workflow owns this machinery; the orchestrator consumes it without duplicating task state.
10. After tasks/dependencies are consolidated, run Batch allocation from `references/routing-matrix.md` once and record all lane choices. Choose the execution profile from the finished plan, then present the plan and the profile in one compact message and continue without waiting, unless an irreversible decision, destructive action, external side effect, or genuine product choice belongs to the user.

## Stage B — Implementation

1. Select the registered implementation profile through `references/routing-matrix.md` before assignment or reassignment, then dispatch one agent per ready lane. Carry selection evidence in the dispatch and roster.
2. Consume dependencies/readiness from the selected task authority and phase barriers, write ownership and shared-resource conflicts from the workflow plan. A lane is ready only after required dependency contracts are reconciled. Dispatch ready independent lanes together when observed host slots and declared resource ceilings permit; increase parallel writers when capacity and ready work justify it. Record an unavailable capacity observation and use the smallest supported batch until capacity is established; do not invent a ceiling or assume unlimited capacity.
3. Never overlap writes to files, generated outputs, contracts, migrations or shared runtime state. Reconcile at declared integration barriers before dependent work starts. Reserve capacity for the next required gate only when it is ready; run only one CPU-heavy verification or profiling command at a time.
4. Each subtask lane runs its focused failure-mode topic selectors and necessary touched-file lint/type/build on the shared build cache. The explicitly assigned task owner runs bounded task-acceptance selectors at task end; neither may run boundary affected/exhaustive checks. It writes no test `/alaa-testing-strategy` finds unowed; that skill owns the tiers and the test-need decision. Choose the smallest discriminating checks for claimed behavior and changed exported-surface, contract, type or lint properties; return observed output, or mark the property not checked. Role definitions own dispatch-conflict handling; reconcile every excluded command and unrun check before accepting the lane.
5. Wait for all required lanes. A blocked lane is blocked; do not pad it into success.
6. Reconcile actual diffs and lane evidence, not summaries alone. Detect scope violations, accidental generated changes, contract mismatches, and cross-lane breakage. Record observed task progress and tested closure through `alaa-workflow references/task-tracking.md`; closure implies neither reviewed acceptance nor commit authority.

## Stage C — Independent verification

1. At each phase implementation end, build one integrated verification plan for the affected tier as `/alaa-testing-strategy` defines it, plus the acceptance criteria this phase claims. Apply Gate economics' collection barrier; final-only review defers acceptance, not phase test collection. At the inherited review boundary, reconcile the complete candidate's evidence and run missing or invalidated checks. When required by repository policy or /alaa-testing-strategy, the exhaustive tier runs in Stage E on the final candidate, not here.
2. Dispatch only gates reached by changed paths. Apply Evidence quality below before citing an unchanged result; reuse requires the correct observer as well as unchanged tree, tool/dependency versions, environment/service state, and flags/seed/cwd. Cite eligible results instead of re-running; when re-running, name the changed condition or missing independent authority.
3. Dispatch `alaa-verifier` with exact commands, working directory, timeout, allowed artifact directory, and resource policy. When the environment matches, the dispatch reuses the lanes' build cache or built artifact rather than a clean build. Use only batching or orchestration tools the current host actually exposes; API capability is not host capability.
4. On Windows, CPU-heavy commands must use `scripts/Invoke-AlaaLowPriority.ps1` with `BelowNormal` by default; `Idle` only for explicitly background-grade benchmark, fuzz, or very heavy diagnostics. On Unix-like systems use `scripts/run-low-priority.sh`. When `/alaa-testing-strategy` sends a gate into a container of the CI job image, the dispatch names the image reference, the read-only mount, the copy into the container filesystem, a `--cpus` limit below the host's logical CPU count, and the gate's parallel flag sized to that limit. That `--cpus` limit replaces the low-priority wrapper for the container run. The gate's own parallel mode inside it counts as the one CPU-heavy command Stage B step 3 allows. A container dispatch that returns `ENVIRONMENT-BLOCKED` for Docker, the image, a mount, the copy, a setup step, or a service is re-dispatched once on the host under the wrapper above, and the report names why. Under Codex, a Docker named-pipe permission failure goes to `/alaa-codex-runtime-ops` before that host re-dispatch.
5. Do not proceed as if verification passed when status is `PRODUCT-FAILURE`, `TEST-INFRA-FAILURE`, `ENVIRONMENT-BLOCKED`, `TIMEOUT`, `FLAKY`, or `CONTAMINATED`. Continue safe independent checks; stop unsafe or contaminated execution and name affected unrun checks, without calling collection complete. Classify before any repair through `references/failure-taxonomy.md`; a host/environment or stale-cache failure justifies no product edit.
6. Route the collected batch through `references/routing-matrix.md` Failure routing and Gate economics; the analyst diagnoses and never fixes. Neither a clear owner nor a cheap fix bypasses collection.
7. After the batch fix, independently rerun failed topic selectors and checks whose inputs changed, followed by the integrated gate when shared behavior changed. Resume all outstanding required checks; retain only eligible unchanged evidence. Any new failures follow the same collection barrier within existing retry/stop budgets.

## Stage D — Independent review and specialist gates

1. Only at the inherited review boundary, select `alaa-reviewer` or `alaa-reviewer-deep` by the routing matrix, then spawn that one profile against the complete diff and lane plan after Stage C's collection, batch repair and required retests pass. Under the `lean` profile the main thread performs this review itself against a diff it did not write; the authority boundary holds because the reviewer is not the author, and the moment the diff leaves the lane plan the profile becomes `standard` and `alaa-reviewer` is dispatched.
2. Trigger a specialist only when its own condition in `references/routing-matrix.md` holds. That file owns every trigger; this one names no condition and narrows none, because a shorter local copy of a trigger list does not read as a summary at dispatch time — it reads as the list, and the conditions it dropped become gates nobody ran. The triggers are identical at every profile.
3. At that same boundary, spawn `alaa-adversarial-reviewer` only when its condition in `references/routing-matrix.md` holds. That condition has two arms and they are not interchangeable: the blast-radius arm is recorded in Stage A and selects the `hardened` profile, while the conflicting-verdict arm is discovered here and fires the reviewer inside whatever profile is already running. A new conflict triggers that lens without retroactively changing completed design work or resetting the inherited boundary. It is a second independent lens, not a second opinion on a routine change, and its findings are reported to the user rather than fed into another fix cycle.
4. Reviewer verdict handling: `APPROVED` proceeds; `APPROVED-WITH-NITS` proceeds; `CHANGES-REQUESTED` routes blocker and major findings verbatim to the owning lane; minor findings and nits follow `alaa-workflow references/review-mode.md` `## Finding triage`.
5. Specialist blocker and major findings are gates equal to reviewer findings. Conflicting specialist opinions are reconciled by the main thread using repository evidence; unresolved high-risk conflicts are surfaced to the user.
6. Present every finding this phase leaves open — reported to the user rather than routed to a lane — as one decision set: each item with its severity per lens, the smallest fix that closes it, and what closing it costs. Ask once. Answered one at a time, each answer can move the tree again and invalidate affected final evidence, including any required exhaustive run.

## Stage E — Documentation and final validation

1. Spawn `alaa-documenter` when its condition in `references/routing-matrix.md` holds. It is the final write lane, which is why every check below runs after it and not before.
2. Documentation is graded, not merely written. `alaa-repo-docs references/15-document-size-and-clustering.md` owns the size ladder, its thresholds, the measuring command, and the one condition under which the largest grade may stand; `/alaa-repo-docs` applies it. This skill decides only that the grade is measured and reported, never what the ladder says — a local copy of it goes stale the moment that skill retunes a threshold.
3. After documentation edits, run the documentation gate below. Documentation is the final write lane and must not bypass validation.
4. If integration is requested and explicitly authorized, bring the base branch into the work branch before final verification; otherwise verify the current candidate and mark integration not requested or awaiting authority as applicable. Select final checks and proof levels from repository validation policy and /alaa-testing-strategy. Preserve the independent verification/review gates and every required check. Run any required exhaustive tier once, fresh on the final candidate after documentation; this means the whole engagement's final candidate, never a nested intermediate phase; do not require unrelated suites merely because this is Stage E. Record the content snapshot and, when integration is in scope, the base commit. No candidate writes may overlap the final pass.

5. Consume the workflow owner's final reusable-context gate after evidence is stable; an empty retained set is valid. Follow its `pipeline reopen required` outcome before closure.
6. Re-check final Git status and diff against declared scopes; confirm canonical task progress and workflow status match what landed; record the last authorized commit timestamp when available, otherwise record it as unavailable.
7. Report in the order `SKILL.md` states, and audit every claim against an actual tool result from this session before reporting it.

## Stage F — Requested integration

This phase applies only when the user requests integration. A local-only request completes after Stage E without a merge prompt. For requested integration, present the candidate, diff, gate evidence, and residual risks. Reuse existing explicit authorization for the exact operation; when it is absent, ask only after the result is reviewable and do not merge before it arrives.

Integrate under `alaa-workflow references/workspace-and-integration.md`. If the base advanced after final verification, incorporate it on the work branch and rerun the required final gates against the changed candidate; a clean merge also changes the tested tree. When the base did not move and the evidence remains applicable, no repeated gate is owed. Push, tag, branch deletion, worktree removal, and remote effects each require explicit authority. A declined or unanswered integration request leaves the candidate intact and is reported accurately, without invalidating completed local work.

## Evidence quality

Accept evidence with exact command, cwd, environment/resource limits, exit/result and observed output; a summary saying "tests pass" is insufficient.

Independent acceptance requires an observer independent of the implementation with authority for that gate. An implementer's broad PASS cannot discharge it, even with unchanged inputs. A cited result names command, timestamp, tested tree and observer; cite valid unchanged independent evidence instead of repeating it. `/alaa-testing-strategy` owns the four unchanged-input conditions and excludes exhaustive results from reuse.

## Gate reopen owner

When curation changes repository instructions, apply `alaa-workflow references/context-curation.md` for reopening affected gates; this run consumes that decision rather than defining a second protocol.

## Finding ownership

- Findings are routed verbatim to the lane that owns the behavior.
- Cross-cutting findings become a new serialized lane with an explicit scope.
- Select the fix owner through Implementation routing in `references/routing-matrix.md`.
- The reviewer/specialist never fixes its own finding.

## Maximum cycles

Two fix-review cycles are the default, unless the user explicitly authorizes more. Verification reruns necessary to evaluate those fixes do not count as extra review cycles. After two unresolved cycles, stop and report options rather than oscillating.

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

- every acceptance criterion maps to evidence, each marked run or cited and carrying its tier;
- required final checks and proof levels passed on the final candidate, including a fresh exhaustive tier when required, with no unverified candidate changes afterward;
- no mandatory command is failed, flaky, timed out, blocked, or contaminated;
- reviewer and triggered specialist blockers/majors are resolved or explicitly accepted by the user;
- final touched files match authorized scopes;
- documentation ran or was explicitly skipped for a grounded reason;
- the final reusable-context pass reported persisted, deferred, rejected, or no admitted candidates;
- no `pipeline reopen required` result remains unresolved;
- canonical task progress and workflow status match what landed; every changed subtask has tested diff evidence and the declared boundary has attributable review; commit only when authorized at that boundary;
- requested integration is complete or explicitly reported declined/blocked; local-only work needs no integration prompt;
- no destructive/external action was performed without authorization.
