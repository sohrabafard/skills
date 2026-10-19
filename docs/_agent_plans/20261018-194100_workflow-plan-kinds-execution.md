# Workflow Plan - Separate design and execution plans

- Plan kind: execution
- Approved design: `docs/_agent_plans/20261018-194100_workflow-plan-kinds-design.md`
- Task ID: `20261018-194100_workflow-plan-kinds-execution`
- Mode: execute
- Profile: resumable
- Task store: beads
- Task binding: AGENTS.md#beads
- Task hierarchy: phase-task-subtask
- Review boundary: final
- Final phase: Phase 1
- Commit authority: not granted
- Status: completed
- Created: `2026-10-18T19:42:38Z`
- Parent plan: not created
- Prompt pack: not created
- Checkpoint: `docs/agents/20261018-194100_workflow-plan-kinds-execution-state.md`
- Machine state: not created
- Base branch and commit: main, 3f044c6479972c63ab47e1651cb7999238bc19af
- Work branch: main
- Worktree: current repository checkout

## Summary and Outcome

- Current repository truth: Clean base, execution-shaped templates/validation, unittest suite and inspected neutral role definitions.
- Outcome: Implement the linked user-approved design with kind-specific scripts, templates, rules and regressions.
- Strategy: Two disjoint writers and one final integrated validation/review boundary.
- Blockers: none known

## Scope

- In scope: skills/sohrab/alaa-workflow and task evidence.
- Out of scope: other skill behavior, vendor, installation, commit, push and remote sync.
- Constraints and assumptions: Preserve existing unmarked families and old evidence; new explicit execution plans always use Beads. Small work that needs no plan stays outside artifact admission.

## Handoff Package

- Confirmed facts (verified, each with how it was verified): bd where resolves the bound shared hub; project issue search found no matching open work; alaa-sj9 with two task/leaf pairs registered. Source base is clean.
- Open assumptions (believed but unverified, each with what would verify it): Actual serving identity is not observable; host exposes requested models/efforts and role authority.
- Ruled out (approach, reason, evidence): Reusing execution validation for design fails the explicit no-hierarchy requirement; silently migrating old plans would change their authority.
- Read first on resume (ordered exact paths): this plan; linked checkpoint; linked design; artifacts/workflow-plan-kinds-20261018.
- Environment notes (command shapes that work here, and ones that look right but fail): Run bd commands separately with explicit --actor; parent actor codex:01a14f6e:lead. No auto commit/push/install.
- Traps (looks correct, is not): Offline schema validates recorded metadata, not live Beads readiness or authentic human approval. New explicit execution rejects state-only initialization because it cannot emit the required plan; historical state-only validation remains supported.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-workflow | skills/sohrab/alaa-workflow/SKILL.md | Plan and continuity | always | Stop dependent work |
| alaa-prompting-guide | skills/sohrab/alaa-prompting-guide/SKILL.md | Instruction edits | always | Stop instruction edits |
| alaa-low-noise | skills/sohrab/alaa-low-noise/SKILL.md | Bounded retrieval and returns | always | Bound output manually |
| alaa-codex-orchestrator | skills/sohrab/alaa-codex-orchestrator/SKILL.md | Dispatch and final gates | always | Stop dispatch |

## Ordered Work

### Phase 1 - Plan kinds and final acceptance

- Status: completed
- Phase issue: alaa-sj9
- Depends on: none
- Reasoning and selection reason: Coupled schema decisions settled once; scripts/templates/tests and instruction owners admit independent write scopes.
- Settled/open decisions and invariants: Explicit --plan-kind; approved-design link; new execution Beads hierarchy; design checkpoint has position, never execution cursor. Existing unmarked validation stays compatible. No weakening of execution gates.
- Risk and required observers: False approval, template/validator mismatch and owner drift; final verifier plus correctness and instruction reviewers.
- Owned scope: workflow skill and task artifacts.
- Excluded from this phase: installed sources, other skills, commits and pushes.
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-low-noise, alaa-codex-orchestrator
- Work:
  - Task issue: alaa-sj9.1 [skills: inherit]
    - Subtask issue: alaa-sj9.1.1 [skills: inherit]
  - Task issue: alaa-sj9.2 [skills: inherit]
    - Subtask issue: alaa-sj9.2.1 [skills: inherit]
- Acceptance criteria: All linked design requirements implemented; no single-owner conflict; complete regression suite, sample design/execution validation and applicable root gates pass; final independent findings resolved.
- Validation commands: python -B skills/sohrab/alaa-workflow/tests/test_workflow_files.py; both scripts --self-test if supported; temporary sample initialization and validation; root structure, index, fleet and lifecycle gates; git diff --check.
- Evidence observed: artifacts/workflow-plan-kinds-20261018/verification.md records the initial 144-test suite, four repository gates, final six affected tests and isolated design/execution samples; all passed. Final artifact validation is recorded there after completion metadata is saved.
- Review status: APPROVED
- Review evidence: artifacts/workflow-plan-kinds-20261018/review.md; independent correctness and instruction reviews APPROVED, including affected correctness re-review after the relative-link repair.
- Snapshot: HEAD 3f044c6479972c63ab47e1651cb7999238bc19af; SHA256 130f88682e51226f966706b21d85030b5ca7929898eab36a792b78c98604f6a5; paths artifacts/workflow-plan-kinds-20261018/source-sha256.json

## Task Allocation

| Task/scope/complexity | Role authority | Priority/reason | Model | Effort | Selection/admission evidence and source date | Invocation/requested/effective controls | Availability/limits |
|---|---|---|---|---|---|---|---|
| Schema planning | alaa-planner | balanced; parser/template compatibility | gpt-6.1-sol | medium | Cross-boundary decisions exceed mechanical fit; 2026-10-18 current source and host | explicit model/effort, fork_turns=none | Available; serving identity unknown |
| Scripts/templates/tests | alaa-implementer | balanced; interacting validation and compatibility | gpt-6.1-sol | medium | Coupled parsers and legacy fixtures exceed bounded local mechanical change | explicit model/effort, fork_turns=none | Available; neutral role inspected |
| Skill/reference contract | alaa-implementer | balanced; authority and continuity reconciliation | gpt-6.1-sol | medium | Several normative owners need semantic reconciliation | explicit model/effort, fork_turns=none | Available; neutral role inspected |
| Final verification | alaa-verifier | balanced; exact commands | gpt-6-luna | medium | Finite execution and results, settled contracts | explicit model/effort, fork_turns=none | Available; role restriction applies |
| Final correctness and instruction gates | alaa-reviewer; alaa-instruction-reviewer | balanced; combined compatibility and authority judgment | gpt-6.1-sol | medium | Interaction review needs workhorse judgment; no frontier need | explicit model/effort, fork_turns=none | Available; role restrictions apply |
| Final documentation parity | alaa-documenter | balanced; exact source/document comparison | gpt-6-luna | medium | Settled 14-file source and command contract; no design discretion | explicit model/effort, fork_turns=none | Available; neutral role inspected, serving unknown |

## Delegation

- Scripts writer owns scripts/, tests/ and assets/ inside workflow; prose writer owns SKILL.md and references/ only. Parent owns this artifact family and integrated evidence.
- Disjoint write scopes: the two lanes above; no shared generators, ports or runtime writes. Code writer owns template/script alignment.
- Dependency edges and ready sets: both leaves have no blocking prerequisites, only parent-child containment; query Beads readiness before dispatch. Final gate waits for both leaves and integrated source freeze.
- Integration barriers and parallel/serialized rationale: parallel independent writes; serialize combined tests and final fixes.
- Reusable evidence and invalidation conditions: focused lane checks retained; independent final observer runs the combined suite once, affected reruns after fixes only.
- Draft then compress instruction edits; preserve out-of-scope architecture and history.

## Execution Position

- Position owner: `docs/agents/20261018-194100_workflow-plan-kinds-execution-state.md`.

## Final outcome

All five design requirements are implemented. The three named references retain sole ownership of plan-kind admission, Beads hierarchy and continuity. No rule remains unplaced. Documentation parity and the changed-file inventory are recorded in artifacts/workflow-plan-kinds-20261018/documentation.md. No separate memory candidate was admitted: the reusable decisions are now authoritative skill rules.

The source snapshot establishes IMPLEMENTED and MERGE_CANDIDATE after the final gates; RELEASE_CANDIDATE and PUBLISHED were not requested. The user prohibited commit, push and installation for this goal. The uncommitted source and task artifacts remain the recovery surface. Beads owns final node closure; this plan does not mirror issue status.
