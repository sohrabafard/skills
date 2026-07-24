# Artifact Admission and Lifecycle

Use the smallest artifact set with a real consumer.

## Profiles

| Profile | Plan | Checkpoint | JSON state | Prompt pack | Use for |
|---|---:|---:|---:|---:|---|
| `direct` | required | no | no | opt-in | Genuinely single-phase, bounded work |
| `resumable` | required | required | no | opt-in | **Default.** Anything multi-phase |
| `orchestrated` | required | required | required | opt-in | An automated consumer parses the state |
| `legacy` | required | required | required | required | An old four-file consumer requires it |

`resumable` is the documented default: work with more than one phase gets a plan and a checkpoint. `direct` is not the fallback for anything that does not obviously need state — it is a deliberate downgrade, chosen when the work is genuinely one phase and bounded, and it accepts that an interruption is paid for with a rediscovery from `git status` and diffs.

Native Plan Mode and review-only work create no repository artifacts unless the user asks for files.

## Paths and correlation

- Plan: `docs/_agent_plans/<stem>.md`, or `docs/plan/<stem>.md` when that family already exists.
- Prompt pack: same plan directory, `<stem>__phase-prompts.md`.
- Checkpoint: `docs/agents/<stem>-state.md`.
- JSON state: `.codex/state/<stem>.json`.

Continue an active task's existing family and stem. Resolve companions only from explicit references or this selected stem; never attach an unrelated newest file.

## Ownership

Three owners, three questions, no overlap: the plan owns the destination and route, the checkpoint owns position, and the plan's handoff package owns knowledge. Nothing belongs to two of them.

The plan owns:

- outcome and scope;
- ordered work and dependencies;
- acceptance criteria;
- validation commands and required evidence.

The handoff package is a section inside the plan, not a separate file — knowledge is only useful next to the route it belongs to, and a fourth file is a fourth thing to keep honest. It owns:

- confirmed facts, each with how it was verified;
- open assumptions, each with what would verify it;
- ruled-out approaches, each with the reason and the evidence;
- the ordered, minimal list of exact paths to read first on resume;
- environment notes — command shapes that work here, and ones that look right but fail;
- traps — anything that looks correct and is not.

The checkpoint contains only status, current phase, last verified result, blockers, next action, touched surfaces, and update time.

JSON contains only schema version, task identity, status, plan path, current phase, next actions, blockers, last validation, and update time.

`references/context-continuity.md` owns the semantics of these fields and when they earn a line. This file owns only where each artifact lives and what it is permitted to contain.

## Update events

The write triggers are owned by `references/context-continuity.md`. On disk they resolve to two different cadences: the checkpoint and any JSON state are updated after a phase completes or fails, after a material decision or scope change, after a validation runs, and before a handoff or completion; the handoff package is appended to whenever something is learned that would be expensive to rediscover, which is learning-driven rather than phase-driven.

Do not maintain duplicate phase checklists, review history, lane definitions, documentation status, or touched-file histories in secondary state.

## Resume and handoff

`references/context-continuity.md` owns the read order, the cold-start test, the post-compaction rules, and what a handoff must contain. Do not restate them here.

## Delegation

Delegate independent lanes with disjoint write scopes or high-volume isolated context. Keep shared-context phases in the parent conversation. The parent owns integration and reruns the combined validation surface.

Record lane ownership in the parent plan or delegated prompt. Do not create a lane-plan file.

## Compatibility

`--with-state`, `--state-only`, `--no-continuation`, `--lane`, `--parent-plan`, and `--mode` remain available for one transition period and emit deprecation warnings when they alter profile behavior. Use `--profile legacy` when an old consumer requires four files.

Completed legacy artifacts remain historical evidence. Validate them with warnings; do not rewrite them unless they become actively executable.
