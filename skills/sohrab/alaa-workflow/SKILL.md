---
name: alaa-workflow
description: "Durable design and execution planning for long-running, multi-phase, resumable, delegated, handoff-sensitive, review, or prompt-pack work. Design plans discuss ideas and algorithms locally through explicit approval; execution plans follow an approved linked design with bound Beads tracking and exact phase/task skills. A plan request saves its admitted plan and checkpoint; plan-only authorizes no implementation. Respect native Plan Mode and explicit no-file, read-only, or chat-only limits; short advice, ordinary review, and small single-phase edits create no files unless requested."
---

# Alaa Workflow

Keep long work resumable without imposing orchestration on every task. Plans own design decisions and workflow gates; the selected task store owns execution task progress. Secondary artifacts exist only for a real consumer.

## Start

1. Read repository instructions and every user-named read-first artifact.
2. If a plan already exists, read it before execution, resume, delegation, review, or handoff, and follow the resume protocol in `references/context-continuity.md`.
3. When `/alaa-memory-os` says its trigger holds, invoke it before planning from prior context or publishing durable knowledge. Memory may contribute verified leads; it never owns this workflow's plan, checkpoint, evidence, or handoff.
4. Before the first non-trivial repository discovery or code-evidence choice, invoke `/alaa-code-routing-gortex` once and reuse its routed result instead of retrieving the same fact through a second surface.
5. Pair with `/alaa-low-noise` and the narrowest domain skill needed for technical decisions.
6. Before writing, resolve plan kind, approval and artifact/profile admission through `references/artifact-lifecycle.md`. Resolve execution task authority and evidence through `references/task-tracking.md`, and exact skill bindings through `references/companion-routing.md`.

## Select the profile

Select kind, approval admission, profile and execution phase/lane planning through `references/artifact-lifecycle.md`.

Initialize design with `scripts/init_workflow_files.py --task <title> --plan-kind design`. Initialize execution with `scripts/init_workflow_files.py --task <title> --plan-kind execution --approved-design <path> --task-store beads --beads-binding <portable-reference> [--profile <profile>] [--review-boundary phase|final] [--with-prompts]`. The kind owner decides allowed flags; `references/task-tracking.md` owns execution binding arguments. Exit `0` means files were created. Exit `1` means a collision and no writes; continue that family instead of forcing over it. Exit `2` means the invocation could not run; do not assume an artifact set exists.

## Survive compaction and handoff

This is why the artifacts exist, and `references/context-continuity.md` owns the rules: how the three artifacts divide the work, what the handoff package holds, when to write, the cold-start test, and the resume protocol.

That reference owns artifact roles, event-driven updates and recovery when current position is uncertain. Follow its mode-aware resume protocol before acting after context loss.

## Execute and resume

This section applies to execution engagements and issue-only implementation.

- Work through the selected task authority and any admitted plan; apply the resume protocol after interruption, compaction, or a branch or worktree change.
- Apply the execution hierarchy and task authority in `references/task-tracking.md` before dependent work.
- Bring canonical workflow/task owners and derived snapshots current before the next phase, handoff, or report.
- Record the engagement's review boundary and final phase; pass them into nested orchestration. `alaa-codex-orchestrator` and `alaa-cc-orchestrator` `references/verification-and-gates.md` own cadence scheduling.
- Record phase test-collection, repair/retest and inherited review barriers in the plan through `references/artifact-lifecycle.md`. Route their execution order to the runtime orchestrator pair's `references/verification-and-gates.md`; cite eligible unchanged evidence. Repository validation policy and `/alaa-testing-strategy` own stricter proof.
- Fix defects and retest the failing path within the active retry budget; never weaken assertions, conceal failures through fixtures, suppress findings or lower review standards. Record an unresolved blocker and next safe action; continue independent safe work.
- On resume, follow the read order in `references/context-continuity.md` before taking any action.
- Complete only when implementation, validation evidence, documentation, artifact status, and the final reusable-context curation outcome agree.
- Report completion as four independent states — `IMPLEMENTED`, `MERGE_CANDIDATE`, `RELEASE_CANDIDATE`, `PUBLISHED` — each with its own verdict, never collapsed into a single one. This skill owns that lifecycle for execution runs, and `references/workspace-and-integration.md` owns what earns each state.

## Preserve workspace evidence

Before writing, identify the base, checkout and unrelated changes through `references/workspace-and-integration.md`. It owns write isolation, execution evidence snapshots and authorized Git integration.

## Curate reusable context

For execution completion and signal-bearing boundaries, apply `/alaa-extract-agent-lessons` through `references/context-curation.md`; it owns intermediate signal triggers, the mandatory final full-engagement gate, recording locations and pipeline reopening. Curation grants no additional artifact or publication authority.

## Delegate selectively

Delegate only genuinely independent work with disjoint write scopes, or high-volume exploration whose output should stay isolated. Keep shared-context phases in the main conversation when they need frequent coordination or latency matters.

A dispatch is a one-way context wall; `references/context-continuity.md` covers what that requires of the dispatch text and the return.

The parent owns the plan, integration, conflict resolution and final validation. Reconcile combined evidence through `references/workspace-and-integration.md` before deciding what still needs a run. Put lane ownership inside the parent plan or dispatch; do not create a separate lane-plan artifact.

A phase that is itself one bounded goal with parallel role lanes may be executed by invoking `/alaa-codex-orchestrator` in Codex or `/alaa-cc-orchestrator` in Claude Code for that phase. The workflow parent still owns the plan, integration, and evidence recording, and records the orchestrator's final report as the phase evidence. Keep simple phases direct; do not stack both orchestration layers on work one agent can finish.

## Generate prompts only on request

Start from `assets/phase-prompts-template.md`; `references/phase-prompts.md` owns roles, six-field shape, word target and its exceptions. Review prompts inherit the declared engagement boundary.

Before resolving any runtime name, model name, effort level, feature syntax, or skill-trigger syntax, load `/alaa-prompting-guide` and verify current official documentation. `references/phase-prompts.md` owns the freshness gate, the role definitions, and where a resolved value is allowed to live.

## Review

Review the requested surface directly. Lead with actionable findings and exact evidence; create workflow artifacts only when explicitly requested or when a continuing fix loop needs them. `references/review-mode.md` owns the evidence order, the must-check areas, the verdict vocabulary a phase can hand across a lane boundary, and finding triage before any fix.

## Validate the workflow artifacts

When a workflow artifact family is admitted, run `scripts/validate_workflow_files.py --plan <path>` before handoff and completion. It applies kind-specific offline checks and correlates explicit references or the selected stem while preserving unmarked history. `references/artifact-lifecycle.md` owns approval-proof limits; `references/task-tracking.md` owns live Beads-proof limits. Issue-only work creates no plan just to run this artifact validator; required behavior validation still runs, with results recorded in its issue through `references/task-tracking.md`.

For admitted families, exit `0` is clean; warnings alone do not fail it. Exit `1` is a blocking artifact error to repair before advancement, never report as a pass. Exit `2` means validation failed to run; a missing selected plan, uncorrelatable companion, or unreadable file is a failed gate, never evidence that artifacts are clean. No artifact validation runs for issue-only work; report that distinction without implying its required behavior validation passed.

## When NOT to use

`references/artifact-lifecycle.md` owns artifact admission and its exceptions; activation alone never authorizes product execution.

## Direct references

This skill owns coordination and continuity, not architecture, security, data, runtime, frontend, infrastructure, or documentation rules. This table selects references; their named sections own the detailed procedures.

| You are about to | Read |
|---|---|
| Begin a long run, hand off (including to another PC), resume, or find you cannot name your own current position | `references/context-continuity.md` |
| Write the first workflow file, choose design versus execution or verify approval, weigh profiles, or attach to an existing family | `references/artifact-lifecycle.md` |
| Resolve execution hierarchy, select or migrate a task store, decide where task information, acceptance or evidence lives, write issue fields or a close reason, link a follow-up or cross-project dependency, assign/resume/transfer an agent's Beads identity or issue ownership, resolve readiness, or encounter a Beads outage or uncertain update | `references/task-tracking.md` |
| Make the first write of a multi-phase or delegated run, record an evidence snapshot, exercise authorized Git integration, or state which completion states a finished run reached | `references/workspace-and-integration.md` |
| Reach an execution phase or decision boundary with a curation signal, or prepare execution completion | `references/context-curation.md` |
| Generate a prompt pack, or resolve a runtime, model, or effort value for one | `references/phase-prompts.md` |
| Review a diff, plan, or artifact instead of executing one | `references/review-mode.md` |
| Take a technical decision this skill does not own — architecture, security, data, testing depth, frontend, infrastructure, or documentation | `references/companion-routing.md` |
