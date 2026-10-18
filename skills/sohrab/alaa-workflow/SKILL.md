---
name: alaa-workflow
description: "Adaptive workflow control with local or explicitly bound Beads task tracking for actionable plans and long-running, multi-phase, resumable, delegated, handoff-sensitive, review, or prompt-pack work. An execution-plan request saves a plan and checkpoint; authorized multi-phase work does so before implementation. Plans name exact phase/task skills. Plan-only authorizes planning artifacts only. Respect native Plan Mode and explicit no-file, read-only, or chat-only limits; short advice, ordinary review, and small single-phase edits create no files unless requested."
---

# Alaa Workflow

Coordinate long work so it survives losing the conversation without making every task pay the full orchestration cost. Plans own workflow gates; the selected task store owns task progress. Secondary artifacts exist only for a real consumer.

## Start

1. Read repository instructions and every user-named read-first artifact.
2. If a plan already exists, read it before execution, resume, delegation, review, or handoff, and follow the resume protocol in `references/context-continuity.md`.
3. When `/alaa-memory-os` says its trigger holds, invoke it before planning from prior context or publishing durable knowledge. Memory may contribute verified leads; it never owns this workflow's plan, checkpoint, evidence, or handoff.
4. Before the first non-trivial repository discovery or code-evidence choice, invoke `/alaa-code-intelligence-routing` once and reuse its routed result instead of retrieving the same fact through a second surface.
5. Pair with `/alaa-low-noise` and the narrowest domain skill needed for technical decisions.
6. Resolve task-store selection, and where task information, acceptance and evidence live, through `references/task-tracking.md`. Apply artifact admission/profile selection through `references/artifact-lifecycle.md` before writing, and populate phase/task skill bindings through `references/companion-routing.md` before execution or handoff.

## Select the profile

Select the smallest admitted profile through `references/artifact-lifecycle.md`; it also owns phase/lane complexity, consolidation and dependency planning. Record those decisions before execution.

Create phased files with `scripts/init_workflow_files.py --task <title> --task-store beads --beads-binding <portable-reference> [--profile <profile>] [--review-boundary phase|final] [--with-prompts]`. For genuinely single-phase work use `--profile direct`. The task-tracking reference owns store/binding arguments; use `--with-prompts` only for an explicit reusable-prompt request. Exit `0` means files were created. Exit `1` means a collision and no writes; continue that family instead of forcing over it. Exit `2` means the invocation could not run; do not assume an artifact set exists.

## Survive compaction and handoff

This is why the artifacts exist, and `references/context-continuity.md` owns the rules: how the three artifacts divide the work, what the handoff package holds, when to write, the cold-start test, and the resume protocol.

That reference owns artifact roles, event-driven updates and recovery when current position is uncertain. Follow its mode-aware resume protocol before acting after context loss.

## Execute and resume

- Work through the selected task authority and any admitted plan; apply the resume protocol after interruption, compaction, or a branch or worktree change.
- Register the phase/task/subtask hierarchy and bound task authority through `references/task-tracking.md` before dependent execution.
- Bring canonical workflow/task owners and derived snapshots current before the next phase, handoff, or report.
- Record the engagement's review boundary and final phase; pass them into nested orchestration. `alaa-codex-orchestrator` and `alaa-cc-orchestrator` `references/verification-and-gates.md` own cadence scheduling.
- Run the affected gates at the strength the change requires. Resolve cheap findings before an expensive gate, then cite an unchanged result instead of repeating it. A repository validation policy and `/alaa-testing-strategy` own stricter proof.
- Fix defects and retest the failing path within the active retry budget; never weaken assertions, conceal failures through fixtures, suppress findings or lower review standards. Record an unresolved blocker and next safe action; continue independent safe work.
- On resume, follow the read order in `references/context-continuity.md` before taking any action.
- Complete only when implementation, validation evidence, documentation, artifact status, and the final reusable-context curation outcome agree.
- Report completion as four independent states — `IMPLEMENTED`, `MERGE_CANDIDATE`, `RELEASE_CANDIDATE`, `PUBLISHED` — each with its own verdict, never collapsed into a single one. This skill owns that lifecycle for every run that consumes it, and `references/workspace-and-integration.md` owns what earns each state.

## Preserve workspace evidence

Before writing, identify the base, working branch or checkout, and unrelated changes. Preserve disjoint work; resolve overlapping ownership before editing. Commit and merge only with explicit user authority. A run without commit authority records the observed worktree identity and scoped content hash beside each validation result. `references/workspace-and-integration.md` owns those records, branch and worktree choices, and integration when requested.

## Curate reusable context

Apply `/alaa-extract-agent-lessons` through `references/context-curation.md`; it owns intermediate signal triggers, the mandatory final full-engagement gate, recording locations and pipeline reopening. Curation grants no additional artifact or publication authority.

## Delegate selectively

Delegate only genuinely independent work with disjoint write scopes, or high-volume exploration whose output should stay isolated. Keep shared-context phases in the main conversation when they need frequent coordination or latency matters.

A dispatch is a one-way context wall; `references/context-continuity.md` covers what that requires of the dispatch text and the return.

The parent owns the plan, integration, conflict resolution and final validation. Reconcile combined evidence through `references/workspace-and-integration.md` before deciding what still needs a run. Put lane ownership inside the parent plan or dispatch; do not create a separate lane-plan artifact.

A phase that is itself one bounded goal with parallel role lanes may be executed by invoking `/alaa-codex-orchestrator` in Codex or `/alaa-cc-orchestrator` in Claude Code for that phase. The workflow parent still owns the plan, integration, and evidence recording, and records the orchestrator's final report as the phase evidence. Keep simple phases direct; do not stack both orchestration layers on work one agent can finish.

## Generate prompts only on request

Start from `assets/phase-prompts-template.md`; `references/phase-prompts.md` owns roles, six-field shape, word target and its exceptions. Review prompts inherit the declared engagement boundary.

Before resolving any runtime name, model name, effort level, feature syntax, or skill-trigger syntax, load `/alaa-prompting-guide` and verify current official documentation. `references/phase-prompts.md` owns the freshness gate, the role definitions, and where a resolved value is allowed to live.

## Review

Review the requested surface directly. Lead with actionable findings and exact evidence; create workflow artifacts only when explicitly requested or when a continuing fix loop needs them. `references/review-mode.md` owns the evidence order, the must-check areas, and the verdict vocabulary a phase can hand across a lane boundary.

## Validate the workflow artifacts

When a workflow artifact family is admitted, run `scripts/validate_workflow_files.py --plan <path>` before handoff and completion. It correlates explicit references or the selected stem, validates marked task-store families and snapshots offline, and preserves unmarked completed history. Its structural result proves neither live Beads binding nor readiness. Issue-only work creates no plan just to run this artifact validator; required behavior validation still runs, with results recorded in its issue through `references/task-tracking.md`.

For admitted families, exit `0` is clean; warnings alone do not fail it. Exit `1` is a blocking artifact error to repair before advancement, never report as a pass. Exit `2` means validation failed to run; a missing selected plan, uncorrelatable companion, or unreadable file is a failed gate, never evidence that artifacts are clean. No artifact validation runs for issue-only work; report that distinction without implying its required behavior validation passed.

## When NOT to use

`references/artifact-lifecycle.md` owns artifact admission and its exceptions; activation alone never authorizes product execution.

## Direct references

This skill owns coordination and continuity, not architecture, security, data, runtime, frontend, infrastructure, or documentation rules. This table selects references; their named sections own the detailed procedures.

| You are about to | Read |
|---|---|
| Begin a long run, hand off (including to another PC), resume, or find you cannot name your own current position | `references/context-continuity.md` |
| Write the first workflow file, weigh one profile against another, or attach to an artifact family that already exists | `references/artifact-lifecycle.md` |
| Select or migrate a task store, decide where task information, acceptance or evidence lives, write issue fields or a close reason, link a follow-up or cross-project dependency, resolve task readiness/ownership, or encounter a Beads outage or uncertain update | `references/task-tracking.md` |
| Make the first write of a multi-phase or delegated run, record an evidence snapshot, exercise authorized Git integration, or state which completion states a finished run reached | `references/workspace-and-integration.md` |
| Reach a completed/failed phase or material decision boundary with a curation signal, or prepare completion | `references/context-curation.md` |
| Generate a prompt pack, or resolve a runtime, model, or effort value for one | `references/phase-prompts.md` |
| Review a diff, plan, or artifact instead of executing one | `references/review-mode.md` |
| Take a technical decision this skill does not own — architecture, security, data, testing depth, frontend, infrastructure, or documentation | `references/companion-routing.md` |
