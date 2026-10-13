# Python task-store lane

Status: implementation and three independent-review repairs saved; the initial 22 methods passed, followed by failing-first/green proof of the three repair methods. Independent closure acceptance remains parent-owned.

AGENT: alaa-implementer. CONFIGURED model/effort: omitted in the installed neutral definition. REQUESTED: gpt-6.1-sol/high. OBSERVED: unknown; no serving-identity evidence. Effective native sandbox: workspace-write; narrower dispatched scope is workflow scripts/tests and this record. No external MCP mutation used; MCP enforcement evidence is unknown.

## Changes and invariants

- `skills/sohrab/alaa-workflow/scripts/init_workflow_files.py`: explicit store/binding CLI, mode-dependent tasks and canonical position rendering; invalid options reject before writes and existing collision preflight remains.
- `skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py`: marked-family metadata, local graph/progress, Beads issue mappings/skills, exact companion identity and scalar cursor/status snapshot consistency. Unmarked families retain prior gates.
- `skills/sohrab/alaa-workflow/tests/test_workflow_files.py`: 22 new focused methods in TaskStoreCliTest, LocalGraphTest, BeadsMappingTest and FamilyConsistencyTest, using real templates/scripts and isolated fixtures.
- Protected invariants: one task owner, one cursor owner, schema 2 without new task keys, offline helpers, exact correlated family, immutable unmarked history, phase/skill/allocation/lifecycle gates.
- Design: dictionary-indexed task graph plus iterative Kahn traversal; reject repeated whole-graph searches and recursion because they add quadratic cost or depth failure. Graph traversal is reasoned O(V+E) time/space at arbitrary graph sizes, with completed chains of 10 and 2,000 tasks exercised; no timing-based complexity claim.
- Binding format is a portable project-relative owner reference with optional anchor; it proves neither owner existence nor live binding adoption.
- Rollback: marked families require compatible consumers; preserve unmarked history and freeze marked families if consumers roll back.

## Acceptance mapping

- A1/A2/A5: both stores across all profiles, explicit/default local, external owner reference, retained aliases and schema.
- A3/A4: mixed-store rejection, missing/duplicate local IDs/edges, cycles, incomplete prerequisites, opaque issue mapping uniqueness and skill overrides.
- A6/A8: status/cursor projection, independently stale snapshots, same-basename wrong-directory companions, direct fallback and duplicate cursor-owner rejection.
- A7: malformed CLI inventory/byte preservation and collision atomicity; live outage/mismatch/uncertain writes are independent scenario review, not helper proof.
- A9/A10/A11: draft/final controlling-text compression and independent combined gates remain parent-owned; lane files are strictly scoped.

## Focused evidence

All commands run from the repository root with Python -B, sequentially, bounded tool output, no declared CPU-heavy workload.

1. `python -B skills/sohrab/alaa-workflow/tests/test_workflow_files.py TaskStoreCliTest`: exit 1, 5 methods / 23 subtest errors, blocked at fixture nested directory creation with WinError 5 under the system temp root; no helper behavior exercised.
2. Same command with process-local TMP/TEMP pointing at a verified dedicated writable-cache root: exit 1, identical 5 methods / 23 errors at nested directory creation. Parent authorized this one materially different retry. No assertions or production code changed for the environment. Exact retry log: `task-store-cli.log`.
3. `python -B skills/sohrab/alaa-workflow/tests/test_workflow_files.py LocalGraphTest.test_completed_chain_and_large_chain_without_recursion`: exit 0, 1 method, 10/2,000 completed-chain cases, 0.022 seconds.
4. `git diff --check -- skills/sohrab/alaa-workflow/scripts skills/sohrab/alaa-workflow/tests`: exit 0; existing CRLF normalization notices only.
5. `python -B skills/sohrab/alaa-workflow/tests/test_workflow_files.py LocalGraphTest.test_draft_placeholder_preserves_ids_and_defers_only_unknown_edges`: exit 0, 1 method, 0.013 seconds. Draft placeholder outcomes retain stable IDs; unresolved draft edges are deferred, real missing edges fail, active phases reject markers. Parent authorized this source-grounded correction while host investigation proceeds.
6. Parent's exact outside-sandbox CLI run reached behavior: exit 1, only the profile-matrix method failed in 8 subcases because its assertion expected unquoted store metadata. The other 4 methods passed. The oracle and negative header mutation literals were corrected to require the exact code-wrapped store value emitted by the template; no value assertion was weakened.
7. With the same process-local TMP/TEMP remedy and parent-authorized `require_escalated`, the four focused groups ran sequentially:

| Command suffix after `python -B skills/sohrab/alaa-workflow/tests/test_workflow_files.py` | Result | Time | Log |
|---|---|---|---|
| `TaskStoreCliTest` | exit 0, 5 methods | 4.828 s | `task-store-cli-focused.log` |
| `LocalGraphTest` | exit 0, 5 methods | 9.019 s | `local-graph-focused.log` |
| `BeadsMappingTest` | exit 0, 5 methods | 6.782 s | `beads-mapping-focused.log` |
| `FamilyConsistencyTest` | exit 0, 7 methods | 15.850 s | `family-consistency-focused.log` |

No broad prefix approval, global environment/configuration edit, ACL change or altered temp fixture was used. These commands cover 22 distinct methods; the two earlier pure-method passes are included in LocalGraphTest and are not counted twice.

## Preserved snapshot and next step

HEAD: `1207d2e8c17d74ea77920ea9cb285b6c73554c7d`. Per-file SHA-256, raw file bytes, sorted relative paths, observed 2026-10-13:

```text
skills/sohrab/alaa-workflow/scripts/init_workflow_files.py c423dc20aafe4f5ec9c7fee47e87ee33b19ac69ef2452691afdb721b21372395
skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py 6fd12602b254882a21502acf966541fa7f70965706b4daf255b87eadae1f1b83
skills/sohrab/alaa-workflow/tests/test_workflow_files.py 6a0b38dec475a77f74da8ed7eff67d3d70ec0e651c4f1a62a35961fbf7e20679
```

Scripts/tests are frozen at this final source snapshot. Full workflow/pack gates, live Beads, installation, runtime compliance, cross-PC ownership and real agent activation are unrun/outside this lane. No blocking lane finding remains; these are focused implementer observations, not independent acceptance.

After the 22 methods passed, the parent identified an authored-contract issue in the generated local delegation sentence: asking to record ready sets could create a second mutable readiness cache. The parent-required replacement is `Local task prerequisites above own dependency edges; derive readiness before dispatch.` The rule-writer examined it, the parent checked draft/rewrite equivalence and retained this already minimal safe form. This is a source wording correction, not test weakening. The final initializer hash above includes this post-test sentence; validator/tests did not change. The prose lane was released to apply two accepted prose-only template reductions, with tokens/cursor strings unchanged. Parent independent final verification owns the integrated final snapshot.

No agent-facing docstrings were added or changed. New diagnostics were compressed in the authoring pass while retaining triggering condition, invariant and repair action. The exact structured diagnostic keys in focused tests stayed unchanged. Existing signatures/callers and the full scoped source diff were inspected; no extra framework, dependency or task scheduler was introduced.

## Independent-review repair cycle

The parent dispatched one scoped repair cycle for one major and two minor correctness findings, retaining the original model/effort and scripts/tests authority. No prose assets, other projects or runtime configuration changed. The runtime-evidence owner was consulted; no relevant Sentry/Spotlight operation was exposed, and these offline parser/initializer reproductions have no deployment or telemetry claim.

| Finding | Disposition and regression |
|---|---|
| Major: local families permit escaped issue mappings | Resolved by scanning the whole marked local document once for issue syntax, replacing the phase-only rejection. The new test rejects an escaped issue under Other work with both a known and an unknown skill, asserts `plan.local-issue-mapping`, and restores the valid control. |
| Minor: empty cursor fields absorb the following line | Resolved by restricting field whitespace/value capture to one line while retaining empty strings. The new test covers blockers followed by next action, and next action followed by touched surfaces; JSON empty arrays pass, genuinely nonempty scalars remain their whole value. |
| Minor: CLI accepts Beads binding `not applicable` | Resolved by rejecting the reserved sentinel before template rendering or writes. The new test covers exact and padded sentinel inputs, exit 2 and its specific misuse diagnostic, unchanged file bytes and unchanged path inventory. |

Exact command: `python -B skills/sohrab/alaa-workflow/tests/test_workflow_files.py ReviewRepairTest`. Cwd: repository root. Resource policy: sequential, 3 focused methods, bounded output, no CPU-heavy check. Native authority: exact-command `require_escalated`, no broad prefix; unchanged process-local TMP/TEMP dedicated writable-cache remedy.

- Red, before production edits: exit 1; 3 methods / 6 failing subcases in 2.237 s. Sentinel cases incorrectly returned 0 and wrote a family; empty fields produced `state.snapshot-blockers` / `state.snapshot-next_actions`; both escaped issue cases incorrectly returned 0. Log: `review-repair-red.log`.
- Green, after the three cause-specific repairs, without modifying the red assertions: exit 0; all 3 methods / 6 subcases passed in 2.513 s. Log: `review-repair-green.log`.
- Scoped `git diff --check -- skills/sohrab/alaa-workflow/scripts skills/sohrab/alaa-workflow/tests`: exit 0. Relevant source diff/callers were inspected. The existing diagnostic keys remained stable; new concise messages preserve the exact store/sentinel condition and remedial action after the draft/compression check.

The latest frozen repair snapshot supersedes the earlier snapshot above. HEAD remains `1207d2e8c17d74ea77920ea9cb285b6c73554c7d`; raw-byte per-file SHA-256, sorted relative paths, observed 2026-10-13:

```text
skills/sohrab/alaa-workflow/scripts/init_workflow_files.py 1aa955dd8178e078fdfd1708ccfd660043ed940e4733c415b1d0b474af93abe4
skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py ed9b9fb3120636d03a1839e7ebdafe426392450773ce863f1d5655edb84e0aeb
skills/sohrab/alaa-workflow/tests/test_workflow_files.py 0e1c210ab8d9513afb24c7d67112bd906874ff3f574d90fe471762174562be29
```

This repair run executed only ReviewRepairTest, not the earlier four groups or full suite. The field parser is shared, so independent final verification must reconcile its callers on this new snapshot. Scripts/tests are frozen for closure review. All three dispatched findings are resolved at focused proof level; no lane blocker remains.

## Frozen-suite fixture reconciliation

The independent verifier's `01-workflow-tests.log` records 106 methods, exit 1, four failures. Read-only assessment confirmed fixture drift: three existing positive workspace/snapshot tests changed the marked plan status to executing without reconciling its checkpoint, while the fourth expected a dependency-schedule placeholder deliberately replaced by the ratified canonical readiness sentence. Production validation matches the contract and was preserved.

After the parent released the freeze, only `test_workflow_files.py` changed: reconcile the checkpoint status before validation in the three affected fixtures, including before the negative snapshot test; replace the obsolete placeholder assertion with the exact canonical local-readiness assertion. Expected exits, workspace/snapshot diagnostic assertions, other placeholder assertions and artifact-count assertions remain intact. No production-source change occurred in this cycle.

Exact focused command:

```text
python -B skills/sohrab/alaa-workflow/tests/test_workflow_files.py WorkflowFilesTest.test_a_phase_that_changed_nothing_records_none_and_passes WorkflowFilesTest.test_completed_uncommitted_phase_requires_observed_snapshot WorkflowFilesTest.test_recorded_work_branch_and_base_satisfy_the_workspace_gate WorkflowFilesTest.test_generated_plan_exposes_reasoning_and_dependency_schedule_without_extra_artifacts
```

Cwd: repository root. Authority/resource policy: one sequential focused command, exact-command escalation, established process-local TMP/TEMP dedicated writable-cache remedy, bounded output. Observed green: exit 0, 4 methods in 1.348 s. Log: `fixture-reconciliation-green.log`. The existing independent red evidence was reused without a duplicate suite run. Scoped `git diff --check -- skills/sohrab/alaa-workflow/tests/test_workflow_files.py` exited 0; the four changed fixture diff regions were inspected.

Latest frozen snapshot, superseding earlier snapshots; HEAD unchanged, raw-byte per-file SHA-256, sorted relative paths, observed 2026-10-13:

```text
skills/sohrab/alaa-workflow/scripts/init_workflow_files.py 1aa955dd8178e078fdfd1708ccfd660043ed940e4733c415b1d0b474af93abe4
skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py ed9b9fb3120636d03a1839e7ebdafe426392450773ce863f1d5655edb84e0aeb
skills/sohrab/alaa-workflow/tests/test_workflow_files.py 1c3b04f93ff39d711d9216c77c8188fb162a2a81659ba4b836e40c30be8e0ac5
```

No broad rerun or production-source edit was performed. All four fixture findings are resolved at focused proof level; no lane blocker remains. Scripts/tests are frozen again for parent-owned independent closure review and full-suite verification.
