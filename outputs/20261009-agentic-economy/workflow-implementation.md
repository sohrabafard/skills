# Workflow implementation evidence

Status: source edits complete; focused tests environmentally blocked; independent acceptance pending.

AGENT: alaa-implementer. CONFIGURED: gpt-6.1-sol / medium. REQUESTED: registered profile, no caller override. OBSERVED: unknown. Effective sandbox: workspace-write; repository and cache writes granted, network enabled. Tool grants visible; runtime enforcement of narrower role boundaries unknown. Operations stayed inside owned source/evidence scope; no commit, installation or memory publication.

## Completed work

- `skills/sohrab/alaa-workflow/SKILL.md`: routes profile/plan sizing to the existing owner and replaces mandatory parent reruns with combined-evidence reconciliation.
- `references/artifact-lifecycle.md`: separates remaining reasoning from risk, consolidates compatible tasks while preserving acceptance/observer boundaries, and requires dependencies, ready sets, resource conflicts and integration barriers. Runtime orchestrator owns observed capacity; no fixed writer ceiling.
- `references/context-continuity.md`: useful executable cold-start action and interrupted lane evidence reconciliation; no duplicate scheduler or resume artifact.
- `references/workspace-and-integration.md`: outcome/input/observer attribution, aggregate coverage inspection, affected invalidation and reuse across phases/agents/interruption.
- `assets/plan-template.md`: phase reasoning/decisions/risk and delegation schedule/evidence fields within existing plan.
- `assets/phase-prompts-template.md`: implementer and independent reviewer validation reconcile evidence before missing/invalidated checks.
- `scripts/init_workflow_files.py`: removes fixed checkpoint-count claim from help.
- `tests/test_workflow_files.py`: generated planning fields and unchanged two-artifact family; help regression check.

## Decisions and invariants

Preserved distinct acceptance outcomes, independent authority, disjoint ownership, memory/curation ownership, existing artifact family and legacy readability. Rejected a new schema/scheduler or hard migration of archived plans: qualitative reasoning and concurrency decisions belong in the plan, while the existing validator continues to check supported artifact/skill/evidence structure. Final templates expose those decisions without claiming that static shape validates model behavior or scheduling quality.

Intentional behavioral changes precede compression. Draft/final word counts: artifact-lifecycle 1012/970; context-continuity 1997/1978; workspace-and-integration 1115/1088. SKILL 1588, plan template 548 and prompt template 396 words after edits; no further safe compress substitution found in their changed text. Compression retained triggers, exceptions, authority, evidence attribution and failure behavior. Growth in references/templates introduces explicit reasoning/dependency planning capability; body profile duplication was removed as an intentional owner correction.

## Focused verification

Resource policy: bounded sequential lightweight Python commands; no CPU-heavy command or parallel runner; Python `-B`.

From `skills/sohrab/alaa-workflow/tests`:

```text
python -B -m unittest test_workflow_files.WorkflowFilesTest.test_generated_plan_exposes_reasoning_and_dependency_schedule_without_extra_artifacts test_workflow_files.WorkflowFilesTest.test_generated_phases_carry_dependencies_ownership_exclusions_and_evidence test_workflow_files.WorkflowFilesTest.test_help_states_the_default_profile_and_its_reason test_workflow_files.WorkflowFilesTest.test_direct_remains_available_as_one_small_plan test_workflow_files.WorkflowFilesTest.test_explicit_prompt_pack_records_roles_and_freshness test_workflow_files.WorkflowFilesTest.test_previous_version_plan_without_a_handoff_package_only_warns test_workflow_files.WorkflowFilesTest.test_representative_completed_legacy_artifacts_are_accepted
```

Initial result: exit 1, seven environmental errors before assertions. `workspace_tempdir()` line 163 `path.mkdir()` returned `PermissionError: [WinError 5] Access is denied` below the newly created user Temp directory.

First failure traceback, with portable source/runtime roots substituted for machine paths:

```text
ERROR: test_generated_plan_exposes_reasoning_and_dependency_schedule_without_extra_artifacts (test_workflow_files.WorkflowFilesTest.test_generated_plan_exposes_reasoning_and_dependency_schedule_without_extra_artifacts)
Traceback (most recent call last):
  File "skills/sohrab/alaa-workflow/tests/test_workflow_files.py", line 489, in test_generated_plan_exposes_reasoning_and_dependency_schedule_without_extra_artifacts
    with workspace_tempdir() as tmp:
         ~~~~~~~~~~~~~~~~~^^
  File "<python-runtime>/Lib/contextlib.py", line 141, in __enter__
    return next(self.gen)
  File "skills/sohrab/alaa-workflow/tests/test_workflow_files.py", line 163, in workspace_tempdir
    path.mkdir()
    ~~~~~~~~~~^^
  File "<python-runtime>/Lib/pathlib/_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: '<user-temp>/alaa-workflow-l3v553qz/.tmp-alaa-workflow-44d88ecc7f824b44bd1d1597c64b171c'
```

One cause-specific retry: same command with process-local `TEMP` and `TMP` set to writable cache root. Result: exit 1, seven errors at the same line below cache-root temporary directories. Retry budget exhausted; no code/test infrastructure repair attempted. Neither result proves source assertions pass.

From repository root: `git diff --check -- skills/sohrab/alaa-workflow` exit 0. Full scoped diff inspected. Full workflow suite and affected pack aggregates reserved for independent verifier, not run in this lane.

## Remaining work

Parent must reconcile the environmental blocker before focused/independent test proof, then inspect owner/cross-skill consistency and behavioral compression independently. The existing checkpoint template still demands the actual command/result while continuity now allows an evidence pointer; independent instruction review should assess whether that pointer needs explicit command/result wording. No publication or installed activation evidence is claimed.

Discriminating instruction-review cases: (1) a resumed unchanged lane cites attributable proof and executes only its remainder; (2) an edited shared fixture invalidates affected tests despite disjoint writes; (3) an aggregate omitting one child or using the wrong observer leaves that gate pending; (4) ready disjoint lanes sharing a port serialize, while independent resources expose concurrent work to runtime capacity; (5) merged tasks preserve two acceptance outcomes and required review authority; (6) high-risk mechanical work keeps risk gates without increasing its reasoning classification; (7) a completed legacy archive stays readable.

## Follow-up: batch task allocation

User steering adds one allocation stage after task/dependency/consolidation decisions. The lifecycle reference routes to `alaa-prompting-guide references/90-model-selection.md`, confirmed with the policy writer as canonical table/algorithm owner. The plan template stores task, official source row/date, priority, exact registered role/model/effort, selection reason, observed availability and evidence/calibration status. Dependency ready sets remain intact. Material changes reassess only affected remaining tasks; completed work is never replayed.

Draft then compressed both added instruction paragraphs without changing their conditions, recorded fields, ownership or reassessment scope. No source table, pins or selection algorithm copied. Follow-up touches only the lifecycle reference, plan template and this evidence file. No blocked tests repeated. Additional discriminating review case: finalize and consolidate three tasks, allocate all once, then change one pending task; retain the completed task and unaffected pending allocation, reclassify only the affected remainder, and block dispatch of an unavailable/unresolved profile.
