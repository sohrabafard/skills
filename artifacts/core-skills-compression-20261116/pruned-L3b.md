# Pruned rules, lane L3b — `alaa-workflow`

Paths are relative to `skills/sohrab/alaa-workflow/`. Baseline: `37ce87a4`. To restore a rule, take
its sentence from that commit. No checker clause was deleted or reworded in this lane, so the last
column is empty in every row.

## Pruned

| File | Rule, in one line | Code | Checker clause deleted |
|---|---|---|---|
| `SKILL.md` | Start: read repository instructions | P4 | |
| `SKILL.md` | Direct references preamble: this skill owns coordination, not architecture, security, data, runtime, frontend, infrastructure or documentation rules | P5 | |
| `SKILL.md` | "This file owns ..." tails on the pointers to the continuity, workspace, curation, review and prompt references | P5 | |
| `references/task-tracking.md` | Opening statement of what this file and two sibling files own | P5 | |
| `references/task-tracking.md` | Do not copy a CLI manual or implement another Beads client | P1 | |
| `references/task-tracking.md` | `## Division of labor`: the store owns registration, status and evidence; workflow owns planning and completion rules. Kept: only `Task store: local` tracks mutable task state in Markdown | P5 | |
| `references/task-tracking.md` | `## Where task information lives`: status, priority, assignee and dependencies live in the Beads issue. Kept in `## Issue fields`: notes, comments, the plan's share and the memory pointer | P5 | |
| `references/task-tracking.md` | Select: verify the active workspace and project through the binding owner before every issue read or change. Kept: availability condition 3 | P3 | |
| `references/task-tracking.md` | Native plan: read back every node's parent, label, criteria, skill bindings and edges with `bd show` and `bd children`. Kept: the graph check and the `bd ready` query | P3 | |
| `references/task-tracking.md` | Native plan: read the root back after the guarded update that marks it `registered` | P3 | |
| `references/task-tracking.md` | Native plan: repeat the registration checks on every resume. Kept: the resume protocol verifies registration and ancestry; a material change returns the root to `draft` | P3 | |
| `references/task-tracking.md` | Hierarchy: verify distinct subtask scope and acceptance in the bound issues before execution. Kept: the distinct-acceptance rule | P3 | |
| `references/task-tracking.md` | Prerequisites: inspect existing issues and edges first; read back the affected dependencies. Kept: the native readiness query that confirms direction | P3 | |
| `references/task-tracking.md` | Prerequisites: use the upstream skill and the installed CLI help for edge changes | P1 | |
| `references/task-tracking.md` | Outage: record the user's "this task is unclaimed" statement as unverified | P3 | |
| `references/task-tracking.md` | Outage recovery: read back each reconciled entry before clearing the pending list | P3 | |
| `references/task-tracking.md` | Migration: read the newly registered issue back before marking the local task migrated | P3 | |
| `references/task-tracking.md` | Outage: bounded session work "reports its result"; after a non-atomic close, "do not claim race safety" | P1 | |
| `references/task-tracking.md` | Pointer-only sentences: plan contents follow context-continuity; `## Beads capabilities in use` owns the `--sandbox` rule; `## Agent identity and ownership` owns the failed-heartbeat case; resume and evidence reconciliation follow two other files | P5 | |
| `references/task-tracking.md` | Repeats of "offline syntax or validation proves no authority, live issue, workspace or readiness". Kept once in `## Phase-task-subtask hierarchy` and once at the validator in `artifact-lifecycle.md` | P6 | |
| `references/context-continuity.md` | `## The four ways context is lost`: what a new session and a different agent start with | P4 | |
| `references/context-continuity.md` | Inventory of what an execution plan contains (the plan template is the format) | P5 | |
| `references/context-continuity.md` | Resume: record what was stale after reconciling snapshots; after compaction, record each discrepancy in the cursor or issue notes | P3 | |
| `references/context-continuity.md` | Cold-start test: also run it periodically during long work. Kept: before a handoff and before a long unattended stretch | P3 | |
| `references/context-continuity.md` | Pointer-only sentences: outage reconciliation follows task-tracking; workspace owns evidence reuse; "this does not migrate task-store authority"; "the rules here hold regardless" | P5 | |
| `references/workspace-and-integration.md` | Stopped-writer recovery: preserve the process identity and the observed liveness evidence | P3 | |
| `references/workspace-and-integration.md` | Tested state: record the observation time. Kept: command, result, identity and manifest method | P3 | |
| `references/workspace-and-integration.md` | `## What this file does not own` | P5 | |
| `references/workspace-and-integration.md` | Pointer-only sentences: context-continuity owns artifact contents; the orchestrator allocates lanes and capacity; the orchestrator owns independent acceptance | P5 | |
| `references/artifact-lifecycle.md` | `## Contents, updates, resume and delegation`: three bullets that list what context-continuity, task-tracking and `SKILL.md` own. Kept as `## Artifact contents`: update only the admitted set; no duplicate state | P5 | |
| `references/artifact-lifecycle.md` | Pointer-only sentences: task-tracking owns availability and hierarchy; companion-routing owns skill bindings; workspace owns shared-check coverage; the orchestrator owns capacity and dispatch mechanics; the prompting guide supplies capabilities | P5 | |
| `references/companion-routing.md` | Opening statement of what workflow and the orchestrators own | P5 | |
| `references/companion-routing.md` | Ownership tails in Core companions: prompting-guide "owns capability and trigger-syntax evidence"; low-noise and workflow "neither substitutes for the other"; lessons skill "owns the decision-interface, judgment-rubric and knowledge-card shapes" | P5 | |
| `references/phase-prompts.md` | Ownership tails: the prompting guide owns capabilities and projections; the orchestrator owns role triggers and the runtime profile; `SKILL.md`, context-continuity and companion-routing own delegation, field semantics and mapping | P5 | |
| `references/phase-prompts.md` | Do not repeat the plan, repository instructions, generic engineering advice or the other role's prompt. Kept: add only task-specific constraints that affect correctness | P1 | |
| `references/review-mode.md` | Evidence order steps 1 and 2: read the named artifact first; inspect current behaviour and nearby tests | P2 | |
| `references/context-curation.md` | Link the curation outcome from admitted position records when needed | P3 | |
| `references/context-curation.md` | Memory owns storage authority and search-before-create, "not this timing reference" | P5 | |
| `assets/plan-template.md` | "Prompting-guide supplies capability/mechanics evidence; workflow stores decisions" | P5 | |
| `assets/plan-template.md` | "Knowledge held only in the current agent's head disappears on compaction" | P1 | |

## Restatements replaced by a pointer to the owner

These rules still bind; the owner states them. Listed so that the owner can restore the local copy.

| File | Local copy removed | Owner now cited |
|---|---|---|
| `SKILL.md` | Fix defects and retest the failing path within the retry budget; never weaken assertions, hard-code expected results, suppress findings or lower review standards | /alaa-testing-strategy and its `references/100-test-execution.md` |
| `references/artifact-lifecycle.md` | Classify each phase and lane into five reasoning classes and record the reason for the class | The runtime orchestrator's `references/routing-matrix.md` (task grounding and workload class) |
| `references/artifact-lifecycle.md` | Field list of the allocation record | The runtime orchestrator's `references/routing-matrix.md` (record the allocation) |
| `references/companion-routing.md` | The five conditions that route a phase to subsystem design | `alaa-system-design`, "when its trigger applies" |
| `references/companion-routing.md` | When to read testing references 100, 110 and 120 | `/alaa-testing-strategy`, which routes its own references |
| `references/phase-prompts.md` | `$name` in Codex, `/name` in Claude Code | `/alaa-prompting-guide` `references/06-invocation-and-composition.md` |
| `references/context-continuity.md` | Require a compact structured return, not a narrative; children return findings and paths, the parent synthesizes | /alaa-low-noise `references/workflow-integration.md` *Delegated lanes* |
| `references/context-continuity.md` | Wording that reassures a model about remaining context | /alaa-prompting-guide. Kept here: never show raw context-budget numbers |
