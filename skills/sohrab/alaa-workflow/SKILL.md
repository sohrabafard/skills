---
name: alaa-workflow
description: Adaptive workflow control for long-running, multi-phase, resumable, delegated, handoff-sensitive, review, or prompt-pack repository work. Use when execution needs an ordered plan, durable continuation, machine-readable orchestration state, independent review, or generated agent prompts. Default to the smallest useful profile. Do not create workflow files for native Plan Mode, review-only requests, short read-only answers, or small edits unless the user explicitly asks for repository artifacts.
---

# Alaa Workflow

Coordinate long work without making every task pay the full orchestration cost. Keep the main plan authoritative and admit secondary artifacts only when a real consumer needs them.

## Start

1. Read repository instructions and every user-named read-first artifact.
2. If a plan already exists, read it before execution, resume, delegation, review, or handoff.
3. Pair with `$alaa-low-noise` and the narrowest domain skill needed for technical decisions.
4. Select a mode and artifact profile before writing workflow files.

## Select the smallest profile

- Native Plan Mode or review-only: return the requested plan or findings in chat. Create files only when explicitly requested.
- `direct` (default): create one compact plan for bounded work.
- `resumable`: create the plan plus one human checkpoint when interruption, compaction, or handoff is plausible.
- `orchestrated`: add compact JSON state only when automation or multiple agents consume it.
- `legacy`: reproduce the transitional four-file set only for compatibility.
- Add `--with-prompts` only when the user explicitly requests reusable implementation/review prompts.

Use `scripts/init_workflow_files.py --task <title> --profile <profile> [--with-prompts]`. Read `references/artifact-lifecycle.md` for paths, compatibility flags, and update rules.

## Keep one source of truth

The plan alone owns outcome, scope, ordered work, phase dependencies, acceptance criteria, and validation commands. Do not duplicate those sections in checkpoint or JSON state.

Update secondary state only on:

1. a phase transition;
2. a material decision or scope change;
3. a validation result or blocker;
4. handoff or completion.

Record evidence, not raw logs. Preserve user changes and keep status honest when validation is blocked.

## Execute and resume

- Work from the plan in order; re-read it after interruption, compaction, or branch/worktree change.
- Validate each behavior-changing phase before advancing.
- Fix failed gates or record the exact blocker and next safe action.
- On resume, read the plan first, then the checkpoint, then JSON only if an automated consumer requires it.
- Complete only when implementation, validation evidence, documentation, and artifact status agree.

## Delegate selectively

Delegate only genuinely independent work with disjoint ownership, or high-volume exploration whose output should stay isolated. Keep shared-context phases in the main conversation when they require frequent coordination or latency matters.

The parent owns the plan, integration, conflict resolution, and final validation. Put lane ownership inside the parent plan or the delegated prompt; do not create a separate lane-plan artifact. See `references/artifact-lifecycle.md`.

A phase that is itself one bounded goal with parallel role lanes may be executed by invoking `$alaa-codex-orchestrator` (Codex) or `$alaa-cc-orchestrator` (Claude Code) for that phase. The workflow parent still owns the plan, integration, and evidence recording, and records the orchestrator's final report as the phase evidence. Keep simple phases direct; do not stack both orchestration layers on work one agent can finish.

## Generate prompts only on request

Use `implementer` and `independent reviewer`; add `documenter` only when the phase alters behavior, APIs, configuration, or operations. Start from `assets/phase-prompts-template.md`; keep each role to the six required fields and at most 250 words unless the user requests an exhaustive prompt. Before resolving runtime names, model names, feature syntax, or skill-trigger syntax, load `$alaa-prompting-guide` and verify current official documentation. Store the resolved values and verification date in the prompt pack, never in stable skill text. See `references/phase-prompts.md`.

## Review

Review the requested surface directly. Lead with actionable findings and exact evidence; create workflow artifacts only when explicitly requested or when a continuing fix loop needs them. See `references/review-mode.md`.

## Validate

Run `scripts/validate_workflow_files.py --plan <path>` for semantic validation. It correlates only explicit references or the selected plan stem, auto-detects adaptive versus legacy artifacts, and treats completed legacy records as readable history.

## Companion routing

Use `references/companion-routing.md` before domain-sensitive decisions. This skill owns coordination, not architecture, security, data, runtime, frontend, infrastructure, or documentation rules.

## When NOT to use

The frontmatter owns trigger boundaries. After this skill is selected, still avoid repository artifacts for ordinary Plan Mode, review-only work, and small tasks unless the user requests them.

## Direct references

- `references/artifact-lifecycle.md` - artifact admission, paths, lifecycle, resume, delegation, and compatibility.
- `references/phase-prompts.md` - optional role-based prompt generation and freshness checks.
- `references/review-mode.md` - review semantics and verdict shape.
- `references/companion-routing.md` - domain skill ownership.
