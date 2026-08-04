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
4. Select a mode and artifact profile before writing workflow files.

## Select the profile

| Profile | Plan | Checkpoint | JSON state | Use for |
|---|---|---|---|---|
| `direct` | yes | no | no | Genuinely single-phase, bounded work |
| `resumable` | yes | yes | no | **Default.** Anything multi-phase |
| `orchestrated` | yes | yes | yes | Automation or another agent parses the state |
| `legacy` | yes | yes | yes | Compatibility with an old four-file consumer |

**`resumable` is the default for any work with more than one phase.** The asymmetry justifies it: the checkpoint is about ten lines and is written at four moments in the whole task, while losing position in the middle of long work costs an expensive rediscovery from `git status` and diffs, and sometimes gets it wrong. Drop to `direct` only when the work is genuinely one phase and bounded.

Native Plan Mode and review-only requests still create no repository artifacts unless the user asks for files. Add `--with-prompts` only when the user explicitly requests reusable implementation or review prompts.

Use `scripts/init_workflow_files.py --task <title> [--profile <profile>] [--with-prompts]`. Read `references/artifact-lifecycle.md` for paths, compatibility flags, and update rules.

## Keep one source of truth

Three artifacts, three jobs, no overlap. The **plan** owns the destination and route. The **checkpoint** owns position. The plan's **handoff package** owns knowledge — what the work has already learned, which is the part compaction destroys first.

Never duplicate plan sections into the checkpoint or JSON. Record evidence, not raw logs. Keep status honest when validation is blocked.

## Survive compaction and handoff

This is why the artifacts exist, and `references/context-continuity.md` owns the rules: when to write, what the handoff package holds, the cold-start test, and the resume protocol. Read it before any long run, handoff, or resume.

Two things are worth knowing without opening it. Write when something happens — a phase ends, a decision lands, a validation runs, a handoff approaches, or something expensive is learned — never on a schedule. And do not wait for a compaction warning to record knowledge, because afterwards the same information survives only as a summary of a summary.

## Execute and resume

- Work from the plan in order; re-read it after interruption, compaction, or a branch or worktree change.
- Validate each behavior-changing phase before advancing.
- Fix failed gates, or record the exact blocker and the next safe action.
- On resume, follow the read order in `references/context-continuity.md`: plan, then handoff package, then checkpoint, then the named read-first files, and JSON only when an automated consumer requires it.
- Complete only when implementation, validation evidence, documentation, artifact status, and the final reusable-context curation outcome agree.

## Curate reusable context

At each completed or failed phase and each material decision boundary, invoke
`$alaa-extract-agent-lessons` / `/alaa-extract-agent-lessons` for an intermediate scan only when the phase
produced an explicit user or team judgment, an accepted tradeoff, a verified surprise, a costly detour, a
validation-driven method change, a coordination bottleneck, or non-obvious reusable knowledge. Put each
admitted candidate in the matching handoff-package field. Record judgment as a confirmed fact about who chose
what and why, not as a universal fact. Do not publish active plan, checkpoint, or validation state to memory.

Before completion, after implementation, validation, review, and documentation evidence are stable, run the
skill's final full-engagement gate even when the expected result is empty. Reconcile intermediate candidates,
route authorized durable publication through `$alaa-memory-os` / `/alaa-memory-os`, and record persisted,
deferred, rejected, or no admitted candidates in the final phase evidence and checkpoint. This workflow owns
when and where curation occurs; `alaa-extract-agent-lessons` owns admission and reusable shapes. If the final
gate returns `pipeline reopen required`, reopen the owning phase, perform the authorized repository promotion,
rerun every affected validation, review, documentation, and documentation-check gate, then rerun final curation.
Never close the plan against evidence the curation gate changed.

## Delegate selectively

Delegate only genuinely independent work with disjoint ownership, or high-volume exploration whose output should stay isolated. Keep shared-context phases in the main conversation when they need frequent coordination or latency matters.

A dispatch is a one-way context wall; `references/context-continuity.md` covers what that requires of the dispatch text and the return.

The parent owns the plan, integration, conflict resolution, and final validation. Put lane ownership inside the parent plan or the delegated prompt; do not create a separate lane-plan artifact.

A phase that is itself one bounded goal with parallel role lanes may be executed by invoking `$alaa-codex-orchestrator` in Codex or `/alaa-cc-orchestrator` in Claude Code for that phase. The workflow parent still owns the plan, integration, and evidence recording, and records the orchestrator's final report as the phase evidence. Keep simple phases direct; do not stack both orchestration layers on work one agent can finish.

## Generate prompts only on request

Use `implementer` and `independent reviewer`; add `documenter` only when the phase alters behavior, APIs, configuration, or operations. Start from `assets/phase-prompts-template.md`; keep each role to the six required fields and at most 250 words unless the user requests an exhaustive prompt.

Before resolving runtime names, model names, effort levels, feature syntax, or skill-trigger syntax, load `$alaa-prompting-guide` / `/alaa-prompting-guide` and verify current official documentation. Model and effort choices come from its `references/50-effort-and-thinking.md`, never from memory or from a value copied out of an older prompt pack. Store the resolved values and the verification date in the prompt pack, never in stable skill text. See `references/phase-prompts.md`.

## Review

Review the requested surface directly. Lead with actionable findings and exact evidence; create workflow artifacts only when explicitly requested or when a continuing fix loop needs them. See `references/review-mode.md`.

## Validate

Run `scripts/validate_workflow_files.py --plan <path>` for semantic validation. It correlates only explicit references or the selected plan stem, auto-detects adaptive versus legacy artifacts, and treats completed legacy records as readable history.

## Companion routing

Use `references/companion-routing.md` before domain-sensitive decisions. This skill owns coordination and continuity, not architecture, security, data, runtime, frontend, infrastructure, or documentation rules.

## When NOT to use

The frontmatter owns trigger boundaries. After this skill is selected, still avoid repository artifacts for ordinary Plan Mode, review-only work, and small single-phase tasks unless the user requests them.

## Direct references

- `references/context-continuity.md` — surviving compaction, handoff, and a fresh agent; the handoff package, write triggers, cold-start test, and resume protocol.
- `references/artifact-lifecycle.md` — artifact admission, paths, lifecycle, and compatibility.
- `references/phase-prompts.md` — optional role-based prompt generation and freshness checks.
- `references/review-mode.md` — review semantics and verdict shape.
- `references/companion-routing.md` — domain skill ownership.
