# Purpose

Provide a durable workflow for long, multi-step repository work so that planning, implementation, validation, resume, handoff, and delegated execution stay coherent even when the task spans many turns or many files.

# Trigger boundaries and ownership

Use this skill when the task needs one or more of these:

- a detailed execution-ready plan grounded in the current repository
- a multi-phase implementation loop with explicit status tracking
- durable repo-local memory that survives long sessions, compaction, or agent handoff
- user-authorized subagents or parallel lanes
- cross-skill orchestration across Alaa's ecosystem

Do not use this skill as a substitute for domain expertise. Pair it with the correct stack skill when the work touches contracts, frameworks, infrastructure, databases, or runtime behavior.

# Instruction precedence

If instructions conflict, follow this order:

1. explicit user constraints for the current task
2. repo-local `AGENTS.md` and closer agent instructions
3. this skill
4. general best practices

If a higher-precedence rule blocks a lower-precedence workflow step, follow the higher-precedence rule and record the deviation in the plan.

# Workflow modes

Choose exactly one primary mode at the start. A task can move from one mode to another, but record the transition.

## `plan`

Use when the user wants a plan first or the surface is in native plan mode.

Outputs:

- a deep plan file, unless file creation is forbidden
- optional state file when resumability or delegation is likely

## `execute`

Use when the task already has enough direction and needs implementation.

Outputs:

- plan updates as the run advances
- state updates when continuity matters
- code, docs, tests, and validation results

## `resume`

Use when continuing a prior task from existing workflow artifacts.

Outputs:

- updated plan/state
- refreshed next actions
- explicit reconciliation of old assumptions vs current repo state

## `delegated`

Use when the user explicitly authorizes subagents and the work has truly independent lanes.

Outputs:

- parent plan and parent state remain the source of truth
- optional child lane plan and state files
- integrated, validated final result from the parent agent

# Artifact path and naming rules

## Path family selection

Choose the plan directory in this order:

1. the existing task-specific path already in use
2. existing `docs/_agent_plans/`
3. existing `docs/plan/`
4. default `docs/_agent_plans/`

Use `.codex/state/` for state JSON whenever state files are needed.

## Naming rules

Parent task stem:

- `<YYYYMMDD-HHMMSS>_<slug>`

Parent artifacts:

- plan: `docs/_agent_plans/<stem>.md` or `docs/plan/<stem>.md`
- state: `.codex/state/<stem>.json`

Child lane artifacts:

- plan: `<parent-stem>__<lane>.md`
- state: `<parent-stem>__<lane>.json`

Keep parent and child stems stable for the life of the task.

## When to create artifacts

Create a plan file when:

- the user asks for a plan
- the task is long, risky, or multi-phase
- the task may continue later or transfer to another agent
- the task includes subagents or parallel lanes

Create a state file when:

- the run is likely to span many turns or many hours
- delegated or parallel execution is involved
- the task has meaningful blockers, validation status, or handoff notes that should not live only in chat
- the task is risky enough that another agent should be able to resume from artifacts alone

Skip plan/state files only for truly small tasks with no continuity value.

## Constrained mode

If the current task forbids new files or allows only one output file:

- do not create the normal plan/state files
- embed the same structure in chat or the single permitted file
- keep the exact plan headings if possible

# Plan mode

The plan must be implementation-ready. It must be rooted in the current repository and current task state.

## Deep-plan quality bar

A good plan is not a list of vague bullets. It must tell the executing agent exactly what to do next and what to avoid. Prefer deterministic recommendations over open-ended option lists unless a decision truly cannot be frozen yet.

Every plan should explicitly separate:

1. what is already good
2. what gaps remain
3. what must change now
4. what is intentionally deferred

Do not reopen settled architecture unless the current repository state directly contradicts it.

## Repository grounding checklist

Before finalizing the plan:

1. find the closest relevant implementation patterns in the repo
2. map the exact surfaces likely to change: code, config, tests, migrations, docs, CI, runtime, infra
3. identify contract boundaries: HTTP, events, jobs, DB schema, CLI, env vars, config files, build pipelines
4. identify rollout or migration risk
5. identify the real validation commands for this repository

## Mandatory exact plan headers

The plan must contain these exact top-level headings:

- `## Goal`
- `## Assumptions`
- `## Constraints`
- `## Closest existing patterns`
- `## Phases (with dependencies)`
- `## Parallel-safe work split`
- `## Commands to run`
- `## Files touched (append-only log)`
- `## Done / Remaining`

Use `assets/plan-template.md` unless a stronger task-specific structure is already in flight.

## Required content under each heading

### `## Goal`

Capture all of these:

- problem statement in repository terms
- in-scope work now
- non-goals and deferrals
- definition of done
- frozen decisions already made
- current repository snapshot relevant to the task
- what is already good
- what gaps remain
- architecture boundaries and contract surfaces

### `## Assumptions`

List only assumptions that materially affect implementation or validation. Mark each assumption as either:

- `frozen`
- `verify during execution`
- `blocker if false`

### `## Constraints`

Include user constraints, repo rules, approval or sandbox limits, environment limits, version constraints, rollout limits, and any stack-specific guardrails.

### `## Closest existing patterns`

List concrete paths or modules in the repository and explain:

- why each one is the closest pattern
- what to copy
- what must stay different

### `## Phases (with dependencies)`

For every phase include:

- objective
- inputs and dependencies
- exact files or modules to touch
- `Parallel-safe` or `Not parallel-safe`
- validation commands
- acceptance criteria
- risk or drift watchpoints
- completion signal

### `## Parallel-safe work split`

Define lane ownership even if the task stays single-agent. Include:

- parent-agent responsibilities
- per-lane scope
- read scope
- write scope
- dependencies on other lanes
- merge notes and integration order

### `## Commands to run`

Group commands by purpose:

- discovery
- implementation support
- validation
- rollback or recovery when relevant

Only include commands that make sense in the current repository.

### `## Files touched (append-only log)`

Use a timestamped append-only log. Do not rewrite history.

### `## Done / Remaining`

Maintain these subsections:

- Done
- Remaining now
- Deferred intentionally
- Blocked or waiting

## Optional extra headings

You may add headings such as `## Risks and drift watchpoints` or `## Contract notes` when useful, but do not remove the mandatory exact headings.

# Execution mode

The parent plan is the runbook. Execute against it, not against vague memory.

## Standard execution loop

1. read the next active phase and its dependencies
2. re-open the exact files you are about to change
3. make the smallest coherent diff that advances the phase
4. run validation for that phase
5. repair failures before moving on
6. update plan and state artifacts
7. move to the next phase only when acceptance criteria are met or a blocker is recorded

## Update cadence

Update plan/state artifacts at these moments:

- immediately after artifact creation
- when a phase starts
- when a phase finishes
- after any meaningful decision freeze or scope change
- before and after long validation runs
- before handing off to another agent or another thread
- before closing the task

## Low-noise execution rules

- Do not waste context by dumping whole files or long command output into chat.
- Prefer targeted search, targeted reads, and summarized results.
- Redirect large logs to files when needed and reference the file path.
- Put durable reasoning in plan/state artifacts, not ephemeral terminal chatter.
- Re-read the smallest necessary artifact slices when resuming.

## Resume and handoff protocol

A new agent should be able to resume with these steps:

1. read the closest `AGENTS.md`
2. read the current plan file
3. read the current state file if it exists
4. inspect the append-only touched-file log and current remaining work
5. re-open only the files relevant to the active phase
6. continue execution without needing hidden chat context

Before leaving a task mid-stream, update:

- active phase
- completed work
- remaining next actions
- blockers
- validation status
- touched files
- any frozen decisions that changed

# State files

State files are durable machine-readable memory, not a second copy of the full plan.

## Recommended schema

Use `assets/state-template.json` as the starter shape. Keep keys stable when possible.

The state should usually include:

- task identity and mode
- status and timestamps
- plan path
- current phase
- completed and pending phases
- frozen decisions and constraints
- lane ownership blocks
- validation status
- touched files
- risk list
- handoff summary and next actions

## Safe-write protocol

This is mandatory when more than one agent or lane may touch the same coordination files.

1. Re-open the file immediately before writing.
2. For JSON state files, validate parse before patching.
3. Edit only the smallest owned block or append-only log entry.
4. Do not reformat or reorder unrelated sections.
5. Re-parse JSON after writing.
6. If the file is truncated, invalid, unexpectedly changed by another lane, or otherwise suspicious, stop and record a conflict block in the plan.

## Conflict block format

When coordination artifacts become unsafe, add this block to the plan and stop dependent work:

- `file:` exact path
- `issue:` what failed
- `evidence:` command output, timestamp, or parse error
- `impact:` what can no longer be trusted
- `required_unblock:` what must happen before continuing

# Delegated execution and subagents

Codex subagent workflows require explicit authorization from the user. Treat phrases like `allow to use subagents` as sufficient authorization.

## Spawn criteria

Use subagents only when all of these are true:

- the task has at least two meaningful low-coupling lanes
- each lane has a crisp scope and validation target
- shared write surfaces are limited or parent-owned
- the parent can integrate the results safely

Avoid subagents when:

- the task is tiny
- most work is one dependency chain
- multiple lanes would fight over the same files
- the main value is a single debug loop with shared state everywhere

## Parent-agent duties

The parent agent must:

- keep the parent plan and parent state authoritative
- define each lane before spawning: scope, inputs, read scope, write scope, validation target, merge notes
- decide whether a lane is read-only research, implementation, review, or verification
- integrate changes, resolve conflicts, and run the final acceptance pass
- close or redirect broken lanes instead of letting them drift

## Lane design rules

- One concern per lane.
- Prefer read-heavy explorer or researcher lanes for discovery.
- Prefer disjoint-file implementer lanes for code changes.
- Add a reviewer or verifier lane only when independent validation materially helps.
- Child lanes must update only their owned blocks in shared artifacts.
- Parent-owned files are never broad-write targets for children.
- Keep fan-out small by default, usually two to four lanes unless the repository and tooling clearly justify more.
- Avoid deeper delegation trees unless the environment already supports and expects them.

## Role selection guidance

When the environment exposes built-in or custom agent roles, prefer this order:

1. explorer or researcher for read-only discovery
2. worker or implementer for scoped code changes
3. reviewer or verifier for independent checking

Do not assume custom roles exist. Use them only if the current environment already exposes them.

## Worktree guidance

If the surface supports worktrees and the parallel lanes have substantial code changes, prefer separate worktrees to reduce shared-write conflicts. If worktrees are unavailable, tighten write ownership and rely on the safe-write protocol.

## Fallback when subagents are unavailable

If the feature is unavailable, disabled, or inappropriate, do not discard the lane design. Keep the same structure in the plan and execute the lanes serially under the parent agent.

# Surface notes

- Codex app uses `/plan-mode` for native plan mode.
- Codex CLI uses `/plan`.
- `/status`, `/resume`, and `/fork` are useful session controls in long CLI runs.
- For difficult long tasks, medium or high reasoning is usually a better baseline than low. For especially hard, long-horizon work, extra-high reasoning can be justified.
- On Windows 11 in the Codex app, prefer native PowerShell-safe commands first.

# Final report

Finish with this order:

1. `Touched files:`
2. `Persian summary:`
3. `Next step:` or concrete verification commands
4. `Suggested commit message:`

If your team already has a legacy report label convention, keep that convention only when the repository or user explicitly requires it.

# Anti-patterns

- Writing a vague plan that could fit any repository.
- Reopening settled architecture without a concrete contradiction.
- Dumping long logs or full file contents into chat.
- Letting progress live only in chat instead of plan/state artifacts.
- Rewriting shared state files end-to-end during delegated work.
- Spawning subagents just because the user allowed it, without a real lane split.
- Advancing to the next phase before current validation passes or a blocker is recorded.
