# Design Plan - Workflow plan kinds

- Plan kind: design
- Task ID: `20261018-194100_workflow-plan-kinds-design`
- Profile: resumable
- Task store: local
- Status: completed
- Created: `2026-10-18T19:42:38Z`
- Checkpoint: `docs/agents/20261018-194100_workflow-plan-kinds-design-state.md`
- Approval status: approved
- Approval by: user
- Approval on: 2026-10-18
- Approval evidence: Current thread goal explicitly directs implementation of the five requirements summarized below; this record captures that supplied design, not a newly inferred approval.

## Summary and Outcome

Separate design discussion and approval from tracked execution. The user-approved behavior authorizes local implementation and verification. No commit, push or installation.

## Scope

Workflow skill source, scripts, templates and tests. No other skill behavior, installed copies, vendor, or global configuration.

## Proposed Design

Use an explicit plan kind to select separate templates and validation. Keep design discussion local through approval; create the linked Beads execution family afterward. Route continuity and task rules to their existing single owners.

## Decisions

| Date | Owner | Decision | Reason |
|---|---|---|---|
| 2026-10-18 | user | Design plans are local and hierarchy-free, ending in approval. | Preserve context while discussing ideas and algorithms without creating execution issues. |
| 2026-10-18 | user | Execution follows an approved linked design and uses Beads milestone/task/subtask mapping. | Separate design authority from executable parallel work. |
| 2026-10-18 | user | Initializer and validator explicitly distinguish kinds and accept readable installed skill paths. | Remove execution-only validation friction from design. |
| 2026-10-18 | user | Lifecycle owns kinds/admission, tracking owns hierarchy, continuity owns handoff/checkpoint. | Keep one owner per rule. |

## Open Questions

None in the supplied behavioral design. Implementation may select schema details within these decisions.

## Acceptance Criteria

All five goal requirements implemented, workflow checks and repository gates exit 0, and separate temporary design/execution samples validate. Report changed files, observed checks and any unresolved ownership conflict.

## Handoff Package

- Confirmed facts (verified, each with how it was verified): Existing initializer emits one execution-shaped plan; validator applies phase checks; read-only planner inspected scripts and tests.
- Open assumptions (believed but unverified, each with what would verify it): none.
- Ruled out (approach, reason, evidence): One plan shape for both kinds conflicts with the user's explicit hierarchy-free design requirement.
- Read first on resume (ordered exact paths): this design; docs/_agent_plans/20261018-194100_workflow-plan-kinds-execution.md; skills/sohrab/alaa-workflow/references/artifact-lifecycle.md.
- Environment notes (command shapes that work here, and ones that look right but fail): Python 3.14 and native PowerShell; use python -B; no installed source edits.
- Traps (looks correct, is not): An approval record is evidence of the user's supplied design only; it grants no commit, push or installation authority.
