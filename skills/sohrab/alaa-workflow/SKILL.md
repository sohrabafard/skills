---
name: alaa-workflow
description: "Adaptive workflow control for long-running, multi-phase, resumable, delegated, handoff-sensitive, review, or prompt-pack repository work. Use when execution needs an ordered plan, durable continuation across compaction or a fresh agent, machine-readable orchestration state, independent review, or generated agent prompts. Multi-phase work gets a plan plus a checkpoint by default. Do not create workflow files for native Plan Mode, review-only requests, short read-only answers, or small single-phase edits unless the user explicitly asks for repository artifacts."
---

# Alaa Workflow

Coordinate long work so it survives losing the conversation, without making every task pay the full orchestration cost. The plan stays authoritative; secondary artifacts exist only where a real consumer needs them.

## Start

1. Read repository instructions and every user-named read-first artifact.
2. If a plan already exists, read it before execution, resume, delegation, review, or handoff, and follow the resume protocol in `references/context-continuity.md`.
3. Pair with `$alaa-low-noise` / `/alaa-low-noise` and the narrowest domain skill needed for technical decisions.
4. Select the artifact profile before writing workflow files.

## Select the profile

**`resumable` — a plan and a checkpoint — is the default for any work with more than one phase.** The asymmetry justifies it: the checkpoint is about ten lines and is written at four moments in the whole task, while losing position in the middle of long work costs an expensive rediscovery from `git status` and diffs, and sometimes gets it wrong. Drop to `direct`, a plan alone, only when the work is genuinely one phase and bounded. Choose `orchestrated` only when automation or another agent parses machine state, and `legacy` only when an old four-file consumer requires it.

Create the files with `scripts/init_workflow_files.py --task <title> [--profile <profile>] [--with-prompts]`, and add `--with-prompts` only when the user explicitly requests reusable implementation or review prompts. Exit `0` created them. Exit `1` means an output already exists and nothing was written, so continue that artifact family instead of forcing over it. Exit `2` means the invocation could not run and no files exist.

## Survive compaction and handoff

This is why the artifacts exist, and `references/context-continuity.md` owns the rules: how the three artifacts divide the work, what the handoff package holds, when to write, the cold-start test, and the resume protocol.

Three things are worth knowing without opening it.

Each artifact answers one question and no other — the plan where the work is going, the checkpoint where it stands right now, the plan's handoff package what the work has already learned. A fact written into two of them becomes a contradiction the first time one is updated.

Write when something happens — a phase ends, a decision lands, a validation runs, a handoff approaches, or something expensive is learned — never on a schedule. And do not wait for a compaction warning to record knowledge, because afterwards the same information survives only as a summary of a summary.

Compaction rarely announces itself, so detect it from your own state rather than from a signal. Treat any turn in which you cannot name the current phase, the last command you ran, and what it returned as a turn after compaction: re-read the plan and the checkpoint before taking any action, and where recollection and a file disagree, the file is right.

## Execute and resume

- Work from the plan in order; re-read it after interruption, compaction, or a branch or worktree change.
- Decompose each phase into subtasks that each carry one checkable outcome. A tick claims that outcome was observed, so tick a box once its evidence exists and never ahead of it. Several boxes at once is normal and correct: one change often satisfies several subtasks, and work that turns out to be already done is ticked as soon as you have verified it rather than assumed it.
- Bring the plan current before the next phase, before a handoff, and before any report. A plan left stale while the work moves on misreports position exactly as a premature tick does.
- Validate each behavior-changing phase before advancing.
- Fix failed gates, or record the exact blocker and the next safe action.
- On resume, follow the read order in `references/context-continuity.md` before taking any action.
- Complete only when implementation, validation evidence, documentation, artifact status, and the final reusable-context curation outcome agree.

## Work on a branch and commit each subtask

Every multi-phase or delegated run works on its own branch off a recorded base, commits at each completed subtask, and merges into the base only after the user confirms. A commit is the cheapest checkpoint that survives what the artifacts cannot: a crashed session, a wrong edit, and a lost conversation at the same time. `references/workspace-and-integration.md` owns the base capture, the dirty-tree refusal, the branch and worktree rules, the commit contract, and the final integration handshake.

## Curate reusable context

At a completed or failed phase, or a material decision boundary, run an intermediate scan through `$alaa-extract-agent-lessons` / `/alaa-extract-agent-lessons` only when that boundary carries one of the seven signals `references/context-curation.md` lists, and park each admitted candidate in the matching handoff-package field. Before completion, run the same skill's final full-engagement gate even when the expected result is empty, and record its outcome in the final phase evidence and the checkpoint.

This workflow owns when and where curation happens. `references/context-curation.md` owns the seven signals, what a candidate is recorded as, where publication is authorized, and what a `pipeline reopen required` verdict obliges.

## Delegate selectively

Delegate only genuinely independent work with disjoint write scopes, or high-volume exploration whose output should stay isolated. Keep shared-context phases in the main conversation when they need frequent coordination or latency matters.

A dispatch is a one-way context wall; `references/context-continuity.md` covers what that requires of the dispatch text and the return.

The parent owns the plan, integration, conflict resolution, and final validation, and reruns the combined validation surface. Put lane ownership inside the parent plan or the delegated prompt; do not create a separate lane-plan artifact.

A phase that is itself one bounded goal with parallel role lanes may be executed by invoking `$alaa-codex-orchestrator` in Codex or `/alaa-cc-orchestrator` in Claude Code for that phase. The workflow parent still owns the plan, integration, and evidence recording, and records the orchestrator's final report as the phase evidence. Keep simple phases direct; do not stack both orchestration layers on work one agent can finish.

## Generate prompts only on request

Use `implementer` and `independent reviewer`; add `documenter` only when the phase alters behavior, APIs, configuration, or operations. Start from `assets/phase-prompts-template.md`; keep each role to the six required fields and at most 250 words; the target yields when the user requests an exhaustive prompt, and whenever required behavior-affecting content does not fit.

Before resolving any runtime name, model name, effort level, feature syntax, or skill-trigger syntax, load `$alaa-prompting-guide` / `/alaa-prompting-guide` and verify current official documentation. `references/phase-prompts.md` owns the freshness gate, the role definitions, and where a resolved value is allowed to live.

## Review

Review the requested surface directly. Lead with actionable findings and exact evidence; create workflow artifacts only when explicitly requested or when a continuing fix loop needs them. `references/review-mode.md` owns the evidence order, the must-check areas, and the verdict vocabulary a phase can hand across a lane boundary.

## Validate the workflow artifacts

Run `scripts/validate_workflow_files.py --plan <path>` before a handoff and before reporting the work complete. It correlates only explicit references or the selected plan stem, auto-detects adaptive versus legacy artifacts, and treats completed legacy records as readable history.

Exit `0` is clean, and warnings alone do not fail it. Exit `1` is a blocking error in the artifacts, repaired before the plan advances rather than reported as a pass. Exit `2` is the validation failing to run at all — nothing selected, a plan that does not exist, an uncorrelatable companion, or a file that cannot be read — and a `2` is a failed gate, never evidence that the artifacts are clean.

## When NOT to use

The frontmatter owns trigger boundaries. After this skill is selected, still create no repository artifacts for native Plan Mode, review-only requests, or small single-phase edits unless the user asks for files.

## Direct references

This skill owns coordination and continuity, not architecture, security, data, runtime, frontend, infrastructure, or documentation rules. Each section above names what a reference owns; the table is the only place a triggering condition is written, so the two cannot drift apart.

| You are about to | Read |
|---|---|
| Begin a long run, hand off, resume, or find you cannot name your own current position | `references/context-continuity.md` |
| Write the first workflow file, weigh one profile against another, or attach to an artifact family that already exists | `references/artifact-lifecycle.md` |
| Make the first write of a multi-phase or delegated run, commit a subtask, or ask the user to accept the result | `references/workspace-and-integration.md` |
| Reach the first phase boundary of a long run, or close a plan | `references/context-curation.md` |
| Generate a prompt pack, or resolve a runtime, model, or effort value for one | `references/phase-prompts.md` |
| Review a diff, plan, or artifact instead of executing one | `references/review-mode.md` |
| Take a technical decision this skill does not own — architecture, security, data, testing depth, frontend, infrastructure, or documentation | `references/companion-routing.md` |
