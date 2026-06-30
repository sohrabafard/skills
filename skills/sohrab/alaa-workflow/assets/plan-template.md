# Agent Plan - {{task}}

- Task ID: `{{task_id}}`
- Created: `{{created_at}}`
- Mode: `{{mode}}`
- Status: `planning`
- Plan path: `{{plan_path}}`
- Phase prompt pack: `{{phase_prompts_path}}`
- Continuation state: `{{continuation_state_path}}`
- Machine state: `{{state_path}}`

## Summary

Write this section first. In complete, fluent English, explain:

- Topic: what this task is about in repository terms.
- Target outcome: what must be true after executing this plan.
- Main strategy: the core idea for reaching the outcome, including how the phases, parallel lanes, tests, and integration fit together.

## Goal

### Problem statement

### In scope now

### Non-goals / intentionally deferred

### Definition of done

### Frozen decisions

### Current repository snapshot

### What is already good

### Gaps that remain

### Architecture boundaries and contract surfaces

## Assumptions

- Assumption:
  - Status: `frozen | verify during execution | blocker if false`
  - Impact:
  - Verification path:

## Constraints

- User constraints:
- Repo / AGENTS constraints:
- Environment / approval constraints:
- Version / rollout constraints:
- Safety / privacy / destructive-action constraints:

## Closest existing patterns

- `path/to/file-or-module`
  - Why it is relevant:
  - What to reuse:
  - What must stay different:

## Phases (with dependencies)

### Phase P1 - Name

- Status: `pending`
- Objective:
- Depends on:
- Parallel-safe: `yes | no | lane-only`
- Mandatory skills:
  - `$alaa-workflow`
  - `$alaa-low-noise`
  - `$skill-name`
- Optional / situational skills:
- Branch / worktree guidance:
  - Suggested branch: `feat/<fixed-branch-name>`
  - Worktree path: user-chosen; do not hardcode
  - Suggested commit message: `type(scope): message`
  - Suggested user-run Git commands:
    ```bash
    git switch -c feat/<fixed-branch-name>
    git status --short
    # after review and user approval:
    git add <paths>
    git commit -m "type(scope): message"
    ```
- Exact files / modules likely to touch:
- Subtask checklist:
  - [ ] Read the main plan, continuation state, machine state if available, and relevant AGENTS.md files.
  - [ ] Re-open the closest existing implementation patterns before editing.
  - [ ] Write or update the phase's tests/fixtures first or alongside the behavior change.
  - [ ] Implement the smallest coherent change that satisfies the phase objective.
  - [ ] Update docs or state notes affected by this phase.
- Test-first checklist:
  - [ ] Identify existing tests that should fail or be extended.
  - [ ] Add targeted tests for new behavior, edge cases, failure paths, and regressions.
  - [ ] Confirm tests are general-purpose and not hard-coded to the implementation.
- Validation checklist:
  - [ ] Run targeted tests for changed behavior.
  - [ ] Run type/lint/build checks relevant to touched surfaces.
  - [ ] Run smoke or integration checks when the phase changes user-visible behavior.
  - [ ] Record exact command results in the state files.
- Acceptance criteria:
- Risks / drift watchpoints:
- Completion signal:

### Phase P2 - Integration / convergence

- Status: `pending`
- Objective:
- Depends on:
- Parallel-safe: `no`
- Mandatory skills:
  - `$alaa-workflow`
  - `$alaa-low-noise`
- Branch / worktree guidance:
- Exact files / modules likely to touch:
- Subtask checklist:
  - [ ] Read the main plan and every lane handoff before integrating.
  - [ ] Merge or apply lane outputs in the planned order.
  - [ ] Resolve conflicts centrally; do not let child lanes own shared integration files.
  - [ ] Run combined validation after all lanes are integrated.
  - [ ] Update state files with integrated results, blockers, and next actions.
- Test-first checklist:
  - [ ] Add integration tests that fail if lane contracts do not compose.
  - [ ] Add regression tests for boundary behavior and conflict-prone surfaces.
- Validation checklist:
  - [ ] Run all phase-level validation commands.
  - [ ] Run full affected-suite validation.
  - [ ] Record evidence in state files.
- Acceptance criteria:
- Risks / drift watchpoints:
- Completion signal:

### Final Phase - Documentation alignment and handoff

- Status: `pending`
- Objective: Align all affected project documentation, guides, runbooks, contracts, API docs, architecture notes, and handoff artifacts with the final implementation and validation evidence.
- Depends on: all implementation and integration phases
- Parallel-safe: `limited; read-only doc audit lanes may run in parallel, final doc edits are integrated by the parent`
- Mandatory skills:
  - `$alaa-workflow`
  - `$alaa-low-noise`
  - `$alaa-docs-farsi` when Persian or repository documentation conventions are involved
- Exact files / modules likely to touch:
- Subtask checklist:
  - [ ] Audit every touched surface for required docs updates.
  - [ ] Update package or module guides in the same change as behavior/export changes.
  - [ ] Update project overview, feature docs, API/contracts, runbooks, and migration notes when affected.
  - [ ] Reconcile plan, phase prompt pack, continuation state, machine state, and final report.
  - [ ] Mark remaining/deferred/blocked items explicitly.
- Test-first checklist:
  - [ ] Validate examples, commands, links, generated docs, or schema snippets where applicable.
- Validation checklist:
  - [ ] Run documentation validation, link checks, generated-doc checks, or at minimum a targeted static review.
  - [ ] Re-run affected implementation gates if docs generation changes code or artifacts.
- Acceptance criteria:
- Risks / drift watchpoints:
- Completion signal:

## Parallel-safe work split

### Parent agent / orchestrator

- Owns:
- Integrates:
- Validates:
- Updates these parent-owned artifacts:
  - `{{plan_path}}`
  - `{{phase_prompts_path}}`
  - `{{continuation_state_path}}`
  - `{{state_path}}`

### Lane - Name

- Scope:
- Mandatory skills:
- Read scope:
- Write scope:
- Depends on:
- Validation target:
- Branch / worktree notes:
- Parent handoff trigger:
- Merge notes:
- Lane checklist:
  - [ ] Read the main plan and lane instructions.
  - [ ] Confirm write scope is disjoint before editing.
  - [ ] Write/update tests for this lane.
  - [ ] Run lane validation.
  - [ ] Return handoff summary, files changed, validation evidence, blockers, and suggested commit message.

## Commands to run

### Discovery

### Implementation support

### Validation

### Documentation alignment

### Recovery / rollback (if relevant)

## Phase prompt pack

- Required path: `{{phase_prompts_path}}`
- Status: `must be created with this plan`
- Checklist:
  - [ ] Include global standing rules for all phase prompts.
  - [ ] Include one Codex/GPT-5.5 `/goal` implementation prompt per phase.
  - [ ] Include one Opus 4.8 review prompt per phase.
  - [ ] Include a fix-loop prompt for CHANGES-REQUESTED reviews.
  - [ ] Include branch/worktree and parallel-lane run instructions when relevant.

## Files touched (append-only log)

- {{created_at}} - Created plan file.

## Done / Remaining

### Done

### Remaining now

### Deferred intentionally

### Blocked / waiting

## Draft-to-final rewrite record

- Draft prepared: `no`
- Final rewrite completed: `no`
- Rewrite check:
  - [ ] No material detail from the draft was lost.
  - [ ] The final plan is coherent, polished, and written in fluent English.
  - [ ] The final plan has a clear beginning, middle, and completion path.
