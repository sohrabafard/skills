# WF evidence

Workflow/testing source, hierarchy generation, validation and compatibility fixtures are implemented; independent final acceptance remains with the parent.

- AGENT: alaa-implementer-high. CONFIGURED model/effort: unpinned in the installed definition. REQUESTED: gpt-6.1-sol/high. OBSERVED serving controls: unknown.
- Effective authority: workspace-write under supplied sandbox; only the two assigned skill trees and this evidence directory. Parent retains Beads, plan/checkpoint, staging and commit effects. MCP enforcement beyond exposed grants is unknown.
- Final source identity: HEAD 1a0799de71254427973f1253d80b846fea9acf10; 19 paths; SHA-256 6d94c29dda4946a608fe152098c69527acdd2126787cf17c3a89f803c52e5796; manifest WF-final-snapshot.json. Method: sorted repository-relative UTF-8 path + NUL + file bytes, including staged and untracked owned inputs.
- First-leaf source identity remains WF-source-snapshot.json. The task aggregate identity before the optional-root repair remains WF-task-snapshot.json; neither is misrepresented as current final-source proof.

## Design and invariants

- Explicit hierarchy marker separates new phased/delegated Beads families from existing local/flat/schema-2 history. Direct nondelegated plans emit one phase. New hierarchy snapshots use schema 3.
- Preserve one task authority, unique containment, genuine prerequisite edges, exact phase/task/subtask cursor, inherited review boundary, tested closure distinct from independent acceptance and explicit scoped user commit authority.
- Reject silent local migration, optional flat creation of new phased work and duplicate cadence ownership. Helpers stay offline; they cannot prove live binding, native nodes/edges/readiness, actual human authorization or runtime compliance.
- Partial failure preserves original outcomes. Fix and retest the defect within the existing finite budget; do not weaken assertions, findings, standards or fixtures. Concurrent writers remain disjoint; no lane commit or Beads mutation occurred.
- Compatibility/rollback: existing families validate under their old contract; new marked families require matching source/templates/helpers together. Freeze new families if consumers roll back.

## Changed paths and purpose

- `alaa-testing-strategy/SKILL.md`: Entry-point ownership and execution/proof contract.
- `alaa-testing-strategy/references/60-coverage.md`: Correct shared enumeration owner (B10 consumer).
- `alaa-testing-strategy/references/80-evidence-and-reporting.md`: Distinguish repaired input from unchanged flaky rerun; reconcile affected integration evidence.
- `alaa-testing-strategy/references/90-test-economy.md`: Use smallest focused case and bounded task-acceptance scope.
- `alaa-workflow/SKILL.md`: Entry-point ownership and execution/proof contract.
- `alaa-workflow/assets/continuation-state-template.md`: Exact task/subtask cursor and pending-boundary pointer.
- `alaa-workflow/assets/phase-prompts-template.md`: Inherit whole-engagement boundary and final candidate.
- `alaa-workflow/assets/phase-template.md`: One canonical rendered phase block for direct and phased generation.
- `alaa-workflow/assets/plan-template.md`: Hierarchy/review/authority headers and offline live-verification precondition.
- `alaa-workflow/assets/state-template.json`: Schema-selected exact task/subtask snapshot fields.
- `alaa-workflow/references/artifact-lifecycle.md`: New hierarchy admission and cursor-compatible artifact contents.
- `alaa-workflow/references/companion-routing.md`: Owner split and nearest-parent skill inheritance.
- `alaa-workflow/references/context-continuity.md`: Exact three-part cursor with schema compatibility.
- `alaa-workflow/references/phase-prompts.md`: Dispatch interface inherits engagement boundary.
- `alaa-workflow/references/task-tracking.md`: Canonical hierarchy, tested closure, REVIEW_PENDING and helper boundary.
- `alaa-workflow/references/workspace-and-integration.md`: Standing explicit commit authority after accepted boundary; current branch.
- `alaa-workflow/scripts/init_workflow_files.py`: Require explicit bound Beads for new phased/delegated plans; render direct one-phase, schema3 and LF.
- `alaa-workflow/scripts/validate_workflow_files.py`: Validate hierarchy/metadata/cursor/authority shape while preserving historical readers.
- `alaa-workflow/tests/test_workflow_files.py`: Failure-discriminating hierarchy/cursor/cadence cases and explicit historical compatibility fixtures.

## Proposal dispositions

| Item | Disposition | Evidence/reason |
|---|---|---|
| 01:A43 | Adapt via ORCH consumer | Current orchestrator preference/constraint conflict belongs to its exclusive writer; parent assigned ORCH. WF does not edit the mirrored trees. |
| 01:A44 | Adapt via CTRL Bash consumer | Redundant output re-checks differ from required artifact verification; parent assigned the narrow Bash exception to CTRL. |
| 01:A49 | Implement | Close reason now identifies the tested version and says closure implies no independent review; task/phase REVIEW_PENDING is explicit. |
| 01:A50 | Adapt | Final aggregate subsumption requires identical covered inputs/environment/flags/observer; documentation differences do not prove equivalence. |
| 01:A51 | Implement owner split | Workflow passes engagement/final-phase/review-boundary context; runtime scheduling stays in the mirrored gate owners. |
| 01:B27 | Implement | Workflow body now routes timing, curation and prompt-shape detail to existing owners; misleading sole-trigger claim removed. |
| 02:P1 | Implement | Bound phase-task-subtask hierarchy, short leaf scope, bounded task acceptance and review-pending milestone closure replace ambiguous task semantics. |
| 02:P2 | Implement | Testing owns discretionary-check necessity; phase template asks uncovered risk and why existing evidence is insufficient. |
| 02:P6 | Adapt | Smallest discriminating check; no new expensive setup/full suite at leaf end. Reuse reset-safe infrastructure without a blanket container ban or invented duration. |
| 02:O1 | Adapt; reject blanket cleanup | Size remains prioritization evidence. Workflow repeated body prose reduced; no warning-clearance sweep or deletion of testing obligations. |
| 03:N6 | Adapt; reject new skill/deploy edits | Existing workflow/testing and mirrored orchestrators cover the grounded cadence defect. Unverified transcript/performance claims and deploy gate mutation remain outside this lane. |
| 03:V8 | Preserve verified coverage | Existing test-economy owner remains; its shared setup/selector/build-once capabilities were not replaced. |
| 01:B10 consumer | Implement | Coverage obligation 2 points shared enumeration to observability-soc ref10; ref70 converts modes into tests; ownership/reachability and always-owed cases retained. |

## Observed validation

- Environment: repository root; installed Python 3.14.8. Ordinary bounded host processes; no CPU-heavy runner policy was supplied. CLI tests required exact-command escalation after Windows denied nested system-temp creation; no source/environment workaround weakened the gate.
- `python -B scripts/check_fleet_references.py --skill alaa-workflow --skill alaa-testing-strategy`: exit 0, 25 Markdown files/113 citations, no findings. First source pass had five ambiguous owner citations; explicit owner names repaired them before the passing source retest.
- `python -B skills/sohrab/alaa-workflow/tests/test_workflow_files.py TaskStoreCliTest LocalGraphTest BeadsMappingTest FamilyConsistencyTest`: exit 0, 22 historical compatibility cases.
- `python -B skills/sohrab/alaa-workflow/tests/test_workflow_files.py`: exit 0, 117 tests in 59.132s on WF-task-snapshot.json (f99fd769405416268aacee95418d65207cf78cdb75c9bb3a756d2b0f4b76f1d9). Output: WF-task-tests.log; temporary paths redacted and LF normalized.
- The later real-plan probe found an owned optional Root issue metadata bug and the parent checkpoint full-title cursor mismatch. Optional-root parsing was repaired; `python -B skills/sohrab/alaa-workflow/tests/test_workflow_files.py HierarchyUnitTest HierarchyCliTest` then exited 0, 12 tests in 2.119s on the repaired source. The 117-test aggregate was not repeated after that focused repair; final-source proof is the affected 12-test pass, not a claimed fresh full-suite pass.
- Earlier focused CLI execution exposed a skill-override variable-shadow defect after the temp-access retry; it was repaired and the exact failing override test passed. The original environment failure and actual defect are distinct from the successful repaired test.
- The in-memory hierarchy-control removal experiment is part of HierarchyUnitTest: removing hierarchy_nodes makes the negative oracle raise `AssertionError: Missing hierarchy rejection`; the unmodified guard refuses the orphan. No source mutation or surviving-mutation claim is hidden.
- `python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20261018-000000_skill-pack-optimization.md`: exit 1 before parent cursor normalization. After the root-header repair, only family.hierarchy-cursor errors remain because Current phase held the full phase title instead of exact Phase 1. Parent owns that correction and the next validator run.
- Scoped git diff whitespace check passed. All 19 owned source files were verified UTF-8 without BOM/LF. No pyc file was produced by the -B gates; an empty tests/__pycache__ directory of unknown provenance was preserved.

## Limits and integration

- Proof levels: source/reference checks are static; parser/CLI fixtures prove local offline logic. No live Beads, installed activation, runtime compliance, latency/cost improvement or independent acceptance is claimed.
- Not run: full-pack gates, final review, installed projections/installation, commit, publication or remote sync. The parent alone owns Beads closure/dispositions and final aggregate/review. A43/A44 consumer outcomes remain linked to ORCH/CTRL evidence at parent integration.
- No unowed consumer tests were added for Beads/framework internals. Native live issue/edge checks belong to the parent/upstream owner; the helper tests only its own offline mapping and no-side-effect choices.
- Parent next action: normalize/validate its cursor, reconcile this evidence with ORCH/CTRL consumer records, close tested implementation milestones without claiming review, and continue the declared final-only boundary.
