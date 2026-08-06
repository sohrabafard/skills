# Workflow Plan - {{task}}

- Task ID: `{{task_id}}`
- Mode: `{{mode}}`
- Profile: `{{profile}}`
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

Knowledge that lives only in the current agent's head and disappears on compaction. Fill a field when something is learned, not on a schedule; leave a field empty rather than padding it. Field semantics are in `alaa-workflow references/context-continuity.md`, which is in the skill, not in this repository.

- Confirmed facts (verified, each with how it was verified): none yet.
- Open assumptions (believed but unverified, each with what would verify it): none yet.
- Ruled out (approach, reason, evidence): none yet.
- Read first on resume (ordered exact paths): NEEDS_FILL
- Environment notes (command shapes that work here, and ones that look right but fail): none yet.
- Traps (looks correct, is not): none yet.

## Ordered Work

### Phase 1 - Ground and implement

- Status: pending
- Depends on: none
- Owned scope: NEEDS_FILL
- Excluded from this phase: NEEDS_FILL
- Work:
  - [ ] Read the named sources and verify current behavior.
  - [ ] Make the smallest in-scope change.
- Acceptance criteria: NEEDS_FILL
- Validation commands: NEEDS_FILL
- Evidence observed: not run
- Commit: none yet

### Phase 2 - Validate and reconcile

- Status: pending
- Depends on: Phase 1
- Owned scope: NEEDS_FILL
- Excluded from this phase: NEEDS_FILL
- Work:
  - [ ] Run the affected validation surface and repair failures.
  - [ ] Reconcile documentation, status, blockers, and remaining work.
- Acceptance criteria: required behavior and evidence agree.
- Validation commands: NEEDS_FILL
- Evidence observed: not run
- Commit: none yet

## Delegation

- Keep shared-context work in the main conversation.
- Independent lane ownership, if admitted: none.
- Dispatches assume zero shared context: copy the relevant handoff-package facts into the dispatch text rather than referring to this conversation.
- Lanes report changed paths; this plan's owner stages and writes every commit.

## Blockers and Next Action

- Blockers: none known.
- Next action: replace `NEEDS_FILL` markers with repository-grounded content before execution.
