# Workflow Continuation State - {{task}}

- Task ID: `{{task_id}}`
- Created: `{{created_at}}`
- Updated: `{{created_at}}`
- Mode: `{{mode}}`
- Status: `planning`
- Main plan: `{{plan_path}}`
- Phase prompt pack: `{{phase_prompts_path}}`
- Machine state: `{{state_path}}`

## Resume protocol

A fresh agent must read these before continuing:

1. Relevant `AGENTS.md` files.
2. `{{plan_path}}` as the main source of truth.
3. This continuation file.
4. `{{state_path}}` if it exists and is readable.
5. `{{phase_prompts_path}}` before implementing or reviewing any phase.

## Current summary

- Current phase:
- Current checkpoint:
- Verified:
- Remaining:
- Blockers:
- Next action:

## Frozen decisions

- {{created_at}} - Created continuation state.

## Phase checklist status

### Phase P1 - Name

- Status: `pending`
- Checklist:
  - [ ] Not started.

## Lanes and subagents

### Parent / orchestrator

- Owns:
- Current responsibility:
- Last update:

### Lane - Name

- Agent / branch / worktree:
- Read scope:
- Write scope:
- Mandatory skills:
- Status:
- Last update:
- Handoff notes:

## Background jobs / long validations

- Job:
  - Started:
  - Command:
  - Owner:
  - Expected evidence:
  - Status:

## Validation evidence

- Command:
  - Ran at:
  - Result:
  - Evidence / notes:

## Touched files log

- {{created_at}} - Created continuation state file.

## Review evidence

- Phase:
  - Reviewer:
  - Verdict:
  - Blockers:
  - Follow-up:

## Docs alignment notes

- Affected docs:
- Final docs phase status:

## Done / Remaining / Deferred / Blocked

### Done

### Remaining now

### Deferred intentionally

### Blocked / waiting

## Handoff

- Last main plan read at:
- Last state update at: `{{created_at}}`
- What the next agent should do first:
- What the next agent must not do:
