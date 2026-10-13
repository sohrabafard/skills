# Dual task-store workflow

The workflow pack now supports local task tracking and explicitly bound Beads tracking with one task authority per family. This source-only delivery passed 106 workflow tests, source validators and consistency checks. The verification record below owns final artifact-gate results. No installation or live-hub operation was performed.

## Behavior

- New work defaults to local tracking. Beads requires explicit project adoption and a portable binding reference; the binding may identify an external hub without a repository-local database.
- Resolve the binding owner and confirm workspace/project scope before using issues. The helper is offline: it validates and records the reference but does not discover or contact Beads. Unavailable or mismatched Beads stops tracking-dependent work; it never silently falls back.
- Beads owns issue identity, status, priority, assignee and issue edges. Workflow plans continue to own goals, phases, phase barriers, acceptance and evidence. Continuity state owns current position, blockers and next action. There are no editable mirrors.
- Beads-only issue work can remain issue-only where artifact admission allows it. Existing unmarked families keep their prior contract. Marked families require compatible consumers; freeze them during rollback until those consumers return.
- Both orchestrator gate references now consume selected-store task progress and workflow-owned position instead of requiring universal plan checkboxes.

See [task tracking](../../skills/sohrab/alaa-workflow/references/task-tracking.md) for the canonical selection, authority, readiness, compatibility and migration rules.

## Helper examples

```powershell
python skills/sohrab/alaa-workflow/scripts/init_workflow_files.py --task "Example work"
python skills/sohrab/alaa-workflow/scripts/init_workflow_files.py --task "Example work" --task-store beads --beads-binding "AGENTS.md#beads"
```

Choose one example for a new family. The caller must resolve `AGENTS.md#beads` to the configured project binding before tracking-dependent work. These examples document argument syntax only; initialization was not run in the repository.

## Evidence and limits

- Source identity: [snapshot](source-snapshot.md), manifest SHA-256 `b67537a006084689f21addcf517fbe6df90aab74a90162c11f625be291f52bc9`.
- Review: [independent review](review-round-1.md) records approved correctness and instruction closure, including approval of the four fixture corrections.
- Plan: [saved execution plan](docs/_agent_plans/20261013-000000_dual-task-store-workflow.md) records acceptance, scope, allocation and curation.
- Verification: [independent evidence](verification.md) records the 106-test pass, static checks and final saved-plan validation. Earlier failures remain recorded alongside their corrections.
- Documentation checks: [scoped link and line-budget results](doc-checks.md).

The changes remain uncommitted source. Installation, publication, live-hub integration, PC2 behavior, runtime compliance and performance impact were not verified.
