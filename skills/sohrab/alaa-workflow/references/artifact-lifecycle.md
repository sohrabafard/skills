# Artifact Admission and Lifecycle

Use the smallest artifact set with a real consumer.

## Profiles

| Profile | Plan | Checkpoint | JSON state | Prompt pack |
|---|---:|---:|---:|---:|
| `direct` | required | no | no | opt-in |
| `resumable` | required | required | no | opt-in |
| `orchestrated` | required | required | required | opt-in |
| `legacy` | required | required | required | required |

Native Plan Mode and review-only work create no repository artifacts unless the user asks for files.

## Paths and correlation

- Plan: `docs/_agent_plans/<stem>.md`, or `docs/plan/<stem>.md` when that family already exists.
- Prompt pack: same plan directory, `<stem>__phase-prompts.md`.
- Checkpoint: `docs/agents/<stem>-state.md`.
- JSON state: `.codex/state/<stem>.json`.

Continue an active task's existing family and stem. Resolve companions only from explicit references or this selected stem; never attach an unrelated newest file.

## Ownership

The plan owns:

- outcome and scope;
- ordered work and dependencies;
- acceptance criteria;
- validation commands and required evidence.

The checkpoint contains only status, current phase, last verified result, blockers, next action, touched surfaces, and update time.

JSON contains only schema version, task identity, status, plan path, current phase, next actions, blockers, last validation, and update time.

## Update events

Update checkpoint or JSON only after a phase transition, material decision/scope change, validation result/blocker, or handoff/completion. Do not maintain duplicate phase checklists, review history, lane definitions, documentation status, or touched-file histories in secondary state.

## Resume and handoff

Read the plan first. Then read the checkpoint. Read JSON only when automation or orchestration consumes it. A handoff must identify the current phase, last verified result, blocker if any, and next executable action.

## Delegation

Delegate independent lanes with disjoint write scopes or high-volume isolated context. Keep shared-context phases in the parent conversation. The parent owns integration and reruns the combined validation surface.

Record lane ownership in the parent plan or delegated prompt. Do not create a lane-plan file.

## Compatibility

`--with-state`, `--state-only`, `--no-continuation`, `--lane`, `--parent-plan`, and `--mode` remain available for one transition period and emit deprecation warnings when they alter profile behavior. Use `--profile legacy` when an old consumer requires four files.

Completed legacy artifacts remain historical evidence. Validate them with warnings; do not rewrite them unless they become actively executable.
