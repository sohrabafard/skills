---
name: alaa-workflow
description: Use this skill for long-running, multi-phase, or behavior-changing repository work that needs durable plan/state artifacts, phased execution, resume or handoff safety, or user-authorized subagents and parallel lanes. It should support both plan mode and execution mode, keep repo-local memory in `docs/plan/*` or `docs/_agent_plans/*` plus `.codex/state/*.json`, document progress and validation continuously, and pair with narrower Alaa skills by domain. Do not use it for tiny single-file edits, short read-only answers, or narrow domain work that does not need long-horizon coordination.
---

# Alaa Workflow

This skill is the workflow operating system for long tasks. It owns orchestration, continuity, and execution discipline. It does not replace domain-specific skills.

## What this skill must produce

- A repository-grounded, implementation-ready plan when the task is in plan mode.
- Durable repo-local memory for long execution, resume, handoff, or delegated work.
- Tight phase discipline: plan -> implement -> validate -> repair -> update state.
- Clear routing to narrower Alaa skills when the work touches a specific stack or subsystem.

## Use this skill when

- The user asks for a detailed plan, turns on plan mode, or wants implementation from a plan.
- The task is large enough that context drift, resumability, or phased execution matters.
- The work spans multiple files, contracts, tests, migrations, infrastructure, or rollout risk.
- The user says the run may continue later, may need another agent, or explicitly allows subagents.

## Do not use this skill when

- The task is a tiny edit with no coordination cost.
- The task is read-only and does not need durable artifacts.
- A narrower domain skill can handle the task directly without long-horizon workflow overhead.

## Start sequence

1. Read repo-local `AGENTS.md` and any closer agent instructions first.
2. Pair with `$alaa-low-noise` for any non-trivial run.
3. Read `references/00-topic-map.md` and then only the smallest relevant reference sections.
4. Decide the workflow mode: `plan`, `execute`, `resume`, or `delegated`.
5. Route to the correct companion skill before making domain-sensitive decisions.
6. Create or continue workflow artifacts only when they add real continuity value.

## Artifact and naming rules

- Never rename these path families:
  - `.codex/state/*.json`
  - `docs/plan/*`
  - `docs/_agent_plans/*`
- If the current task already has a plan or state file, continue that exact file family and stem.
- Otherwise choose the plan directory in this order:
  1. existing task-specific path already referenced in chat or repo docs
  2. existing `docs/_agent_plans/`
  3. existing `docs/plan/`
  4. default `docs/_agent_plans/`
- Parent plan file naming must be `<YYYYMMDD-HHMMSS>_<slug>.md`.
- Parent state file naming should reuse the same stem: `.codex/state/<YYYYMMDD-HHMMSS>_<slug>.json`.
- Child lane artifacts should stay adjacent to the parent by reusing the same stem:
  - plan: `<parent-stem>__<lane>.md`
  - state: `<parent-stem>__<lane>.json`
- Never migrate an in-flight task from `docs/plan/` to `docs/_agent_plans/` or the reverse.

## Plan mode contract

When planning, produce an implementation-ready plan, not a conceptual outline.

The plan must be specific to the current repository and current state. It must explicitly capture:

- what is already good
- what gaps remain
- what must change now
- what is intentionally deferred
- frozen decisions, scope boundaries, and non-goals
- exact files, modules, or surfaces likely to change
- validation commands, acceptance criteria, and risk or drift watchpoints
- execution order and any safe parallel lanes

Keep the mandatory exact headers required by this skill. The template is in `assets/plan-template.md`.

Read `references/full-guide.md`, especially:

- `# Workflow modes`
- `# Plan mode`
- `## Mandatory exact plan headers`
- `## Deep-plan quality bar`

## Execution mode contract

Treat the current plan file as the primary source of truth for sequencing. During execution:

- work one phase at a time unless delegated mode is justified
- re-open exact files before editing if time has passed or another lane may have changed them
- run phase validation before moving on
- update plan/state files after each meaningful milestone, before long validation runs, before handoff, and at task completion
- keep terminal output low-noise and move durable knowledge into repo-local artifacts instead of chat

Read `references/full-guide.md`, especially:

- `# Execution mode`
- `## Update cadence`
- `## Resume and handoff protocol`
- `# State files`

## Subagent Strategy

Treat `allow to use subagents` as explicit authorization.

Also accept close equivalents such as:

- `use subagents`
- `you can delegate this`
- `split this into subagents`
- `parallelize this`

Use subagents only when the task has real independent lanes. The parent agent remains the manager and owns:

- the parent plan and parent state file
- lane design and write-scope allocation
- integration, validation, and final synthesis
- conflict handling and rollback decisions

If subagents are unavailable, disabled, or not worth the overhead, keep the same lane design in the plan and execute it serially.

Read `references/full-guide.md`, especially:

- `# Delegated execution and subagents`
- `## Spawn criteria`
- `## Parent-agent duties`
- `## Fallback when subagents are unavailable`

## Companion routing

This skill handles workflow, not domain ownership. Read `references/companion-routing.md` and actively pair with the right stack skill before making architecture or runtime decisions.

## Windows and Codex surface notes

This skill should work well in Codex app, CLI, and IDE environments, but optimize examples for Windows 11 + native PowerShell first. Use `references/windows-powershell.md` when shell examples or JSON validation commands are needed.

## Useful bundled files

- `assets/plan-template.md` - parent plan skeleton with the required exact headers
- `assets/lane-plan-template.md` - child-lane plan skeleton
- `assets/state-template.json` - recommended state schema starter
- `scripts/init_workflow_files.py` - deterministic artifact bootstrapper
- `scripts/validate_workflow_files.py` - quick plan/state validator

## Completion standard

A run is not done when code has changed. It is done when the plan, validations, remaining work, and handoff state all agree.

Before finishing:

- reconcile plan vs. actual work
- mark done, remaining, deferred, and blocked items clearly
- make the next agent able to continue from the artifacts alone
- produce the final report in the order defined in `references/full-guide.md`

## Reference navigation

- `references/00-topic-map.md` - smallest useful reading path
- `references/full-guide.md` - detailed operating rules
- `references/companion-routing.md` - ecosystem pairing map
- `references/windows-powershell.md` - native Windows and PowerShell patterns
