# Workflow Plan - {{task}}

- Plan kind: execution
- Approved design: {{approved_design_display}}
- Task ID: `{{task_id}}`
- Mode: `{{mode}}`
- Profile: `{{profile}}`
- Task store: `{{task_store}}`
- Task binding: {{task_binding}}
{{hierarchy_header}}- Review boundary: {{review_boundary}}
- Final phase: {{final_phase}}
{{local_final_header}}- Commit authority: not granted
- Status: planning
- Created: `{{created_at}}`
- Parent plan: {{parent_plan_display}}
- Prompt pack: {{phase_prompts_display}}
- Checkpoint: {{continuation_state_display}}
- Machine state: {{state_display}}
- Base branch and commit: NEEDS_FILL
- Work branch: NEEDS_FILL
- Worktree: none

## Summary and Outcome

- Current repository truth: NEEDS_FILL
- Outcome: NEEDS_FILL
- Strategy: NEEDS_FILL

## Scope

- In scope: NEEDS_FILL
- Out of scope: NEEDS_FILL
- Constraints and assumptions: NEEDS_FILL

## Handoff Package

Knowledge held only in the current agent's head disappears on compaction. Fill a field when knowledge is learned, not on a schedule; leave unused fields empty. Field semantics are in the skill's `alaa-workflow references/context-continuity.md`, not in this repository.

- Confirmed facts (verified, each with how it was verified): none yet.
- Open assumptions (believed but unverified, each with what would verify it): none yet.
- Ruled out (approach, reason, evidence): none yet.
- Read first on resume (ordered exact paths): NEEDS_FILL
- Environment notes (command shapes that work here, and ones that look right but fail): none yet.
- Traps (looks correct, is not): none yet.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| NEEDS_FILL | NEEDS_FILL | NEEDS_FILL | NEEDS_FILL | NEEDS_FILL |

## Ordered Work

Keep only phases with a distinct decision, authority or integration barrier. Merge compatible work while retaining each acceptance outcome and evidence mapping.

{{ordered_work}}

## Task Allocation

After finalizing tasks, dependencies and consolidation, record the runtime orchestrator's all-role allocation.
In Codex, `/alaa-codex-orchestrator` owns `references/routing-matrix.md`.
In Claude Code, `/alaa-cc-orchestrator` owns `references/routing-matrix.md`.
Prompting-guide supplies capability/mechanics evidence; workflow stores decisions. Unresolved controls or availability block the affected dispatch. Material changes reassess only affected remaining tasks.

| Task/scope/complexity | Role authority | Priority/reason | Model | Effort | Selection/admission evidence and source date | Invocation/requested/effective controls | Availability/limits |
|---|---|---|---|---|---|---|---|
| NEEDS_FILL | NEEDS_FILL | NEEDS_FILL | NEEDS_FILL | NEEDS_FILL | NEEDS_FILL | NEEDS_FILL | NEEDS_FILL |

## Delegation

- Keep shared-context work in the main conversation.
- Independent lane ownership, if admitted: none.
{{task_delegation}}
- Disjoint writes and shared-resource conflicts: NEEDS_FILL
- Integration barriers and parallel/serialized rationale: NEEDS_FILL
- Consolidated tasks/checks and preserved outcome/evidence mappings: NEEDS_FILL
- Phase collection, repair/retest and review barriers, owners and resume evidence: NEEDS_FILL; apply the active runtime orchestrator's verification-and-gates.md.
- Reusable evidence and invalidation conditions: NEEDS_FILL
- Dispatches assume zero shared context: copy the relevant handoff-package facts into the dispatch text rather than referring to this conversation.
- Lanes report changed paths; this plan's owner records the validated snapshot and handles any explicitly authorized commit.
- Before execution, verify the adopted Beads workspace, project, nodes, parent-child relations and blocking edges through the binding owner; initialization proves only offline syntax. Nested invocations inherit this engagement's review boundary and final phase.

{{position_section}}
