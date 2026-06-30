# Lane Plan - {{task}}

- Task ID: `{{task_id}}`
- Parent task ID: `{{parent_task_id}}`
- Lane: `{{lane}}`
- Created: `{{created_at}}`
- Mode: `delegated`
- Status: `planning`
- Plan path: `{{plan_path}}`
- State path: `{{state_path}}`
- Parent plan: `{{parent_plan_path}}`

## Summary

Write this section first. Explain the lane objective, the parent outcome it supports, and how this lane can run independently without drifting from the parent plan.

## Goal

### Lane objective

### Scope boundary

### Non-goals / intentionally deferred

### Definition of done for this lane

### Frozen decisions inherited from parent

### Current repository snapshot for this lane

### What is already good

### Gaps that remain

### Contracts touched by this lane

## Assumptions

- Assumption:
  - Status: `frozen | verify during execution | blocker if false`
  - Impact:
  - Verification path:

## Constraints

- Parent plan constraints:
- Lane write-scope constraints:
- Environment / approval constraints:
- Safety / destructive-action constraints:

## Closest existing patterns

- `path/to/file-or-module`
  - Why it is relevant:
  - What to reuse:
  - What must stay different:

## Phases (with dependencies)

### Phase L1 - Name

- Status: `pending`
- Objective:
- Depends on:
- Parallel-safe: `yes | no`
- Mandatory skills:
  - `$alaa-workflow`
  - `$alaa-low-noise`
  - `$skill-name`
- Exact files / modules to touch:
- Subtask checklist:
  - [ ] Read the parent plan, parent continuation state, lane plan, lane state, and relevant AGENTS.md files.
  - [ ] Confirm no shared parent-owned files are in this lane's write scope.
  - [ ] Write or update lane tests/fixtures first or alongside behavior changes.
  - [ ] Implement the lane change.
  - [ ] Record touched files, validation evidence, blockers, and parent handoff notes.
- Test-first checklist:
  - [ ] Add or extend targeted lane tests.
  - [ ] Add edge-case and failure-path coverage.
  - [ ] Reject hard-coded or test-special-cased behavior.
- Validation checklist:
  - [ ] Run lane-specific tests.
  - [ ] Run required type/lint/build checks for touched surfaces.
  - [ ] Record exact command results.
- Acceptance criteria:
- Risks / drift watchpoints:
- Completion signal:

## Parallel-safe work split

### Lane ownership

- Scope:
- Mandatory skills:
- Read scope:
- Write scope:
- Parent-owned files not to edit:
- Parent handoff trigger:

## Commands to run

### Discovery

### Implementation support

### Validation

## Files touched (append-only log)

- {{created_at}} - Created lane plan file.

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
  - [ ] The final lane plan is coherent, polished, and written in fluent English.
