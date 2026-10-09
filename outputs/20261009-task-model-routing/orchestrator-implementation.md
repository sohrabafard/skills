# Paired orchestrator implementation

Status: implementation ready for independent acceptance. AGENT: alaa-implementer-high. CONFIGURED: gpt-6.1-sol/high from dispatch definition; REQUESTED: same; OBSERVED: unknown.
Effective authority: workspace-write restricted to owned trees and archive; shared/global installation, commit and external effects excluded. Runtime enforcement beyond supplied sandbox/tool grants unknown.

## Authoring draft
Every role including specialists and reviewers must have a task-specific choice of both model and reasoning effort. The orchestrator must decide it from actual remaining scope, task complexity, selected priority and evidence after ruling out missing context/specification/tool causes. A role must never imply its model or effort. Record and explicitly pass both controls on an observed runtime surface; conflicting static pins or effective overrides require an exact compatible available realization, otherwise stop the affected lane. Role responsibilities, grants, skills, verdicts and independent gates remain the same for every model. Preserve bounded implementer fit predicates and exceptional admission, and keep legacy IDs only as compatible authority identities. Prompting owns capability evidence and mechanics; workflow records decisions, the orchestrator owns actual allocation. Balanced is the default. A second independent lens does not require a stronger or different model.

## Compression record
The shipped allocation, capability-route, dispatch and lane clauses compress this draft. Cuts remove narration and duplicate ownership; preserve all-role scope, both controls, reason/evidence, actual control verification, exact compatibility or affected-lane block, unchanged authority/gates, bounded fit, exceptional admission and owner boundaries. Source edits never claim installed/session activation.

## Design
Extend the existing policy projection helper to neutralize all managed native definitions; retain metadata, bodies, role IDs and manifest engine. Reject per-role replacement pins and a role/model Cartesian product: both recreate identity-driven allocation. No installation or session reload is attempted. Compatibility IDs retain workload contracts while names confer no pair. No shared data/retry/concurrency behavior changes; file writes serialized against the policy lane and rendering waits canonical readiness.

## Verification
All commands use Python -B in the named skill cwd; sequential light process, no CPU-heavy suite. Full-serving model identity and installed activation remain unobserved.

| Scope | Exact command | Result |
|---|---|---|
| Both orchestrators | python -B scripts/render_agents.py --write | exit 0; 34 Codex / 30 Claude outputs including manifests |
| Codex | python -B scripts/render_agents.py --self-test --self-test-dir <repo>/outputs/20261009-task-model-routing/codex-render-fixtures | exit 0; all role parsed authority/body preservation plus drift fixtures |
| Claude | python -B scripts/render_agents.py --self-test --self-test-dir <repo>/outputs/20261009-task-model-routing/claude-render-fixtures | exit 0; all role authority/body preservation plus drift fixtures |
| Both orchestrators | python -B scripts/check_agent_contracts.py | exit 0; corrected CC stale assertion after original exit 1 |
| Both orchestrators | python -B scripts/check_agent_contracts.py --self-test | exit 0; 386 Codex / 337 Claude positive/negative fixtures |
| Both orchestrators | python -B scripts/check_agent_grants.py | exit 0; 33 Codex / 29 Claude authored role grants |
| Workflow | python -B -m unittest tests.test_workflow_files.TaskControlMetadataTest tests.test_workflow_files.WorkflowFilesTest.test_explicit_prompt_pack_records_roles_and_freshness tests.test_workflow_files.WorkflowFilesTest.test_documenter_metadata_is_optional_and_paired | 8 passed on exact approved escalation after two sandbox Temp mkdir failures; six pure tests passed before escalation |
| Workflow | python -B -m unittest tests.test_workflow_files.TaskControlMetadataTest | 6 passed after malformed model/component regression fix and truthful configured-intent metadata wording |
| Repo | git -c core.safecrlf=false diff --check -- <owned skill roots> | clean before final review fixes; final changed inputs reserved for independent gate |

Initial renderer self-tests had a wrong relative output parent and access denial; corrected resolved workspace directories passed. One CC repair command used the wrong cwd and made no edits; unchanged repeated failure was unnecessary. One real stale-checker repair passed. Known encoding corruption introduced by Windows default reads in five touched docs was restored from the original Unicode with explicit UTF-8; targeted scan is clean. No source workaround for Temp access.

Previous source snapshot: 153 regular files in both orchestrators and workflow, excluding bytecode; SHA256 1e5831ab97548d13862347ca355694e146b8066c9d20d5e1ce78bf16bbc0f09d. Hash framing is ordered repository-relative UTF-8 path, NUL, raw file bytes, NUL. This report is outside that snapshot.

## Acceptance mapping

1. Every managed role: all 62 native role definitions omit both pins and require the explicit task pair; canonical lane covers both rule-writers.
2. Task selection: mirrored All-role task allocation owns scope/complexity/priority/evidence; legacy IDs and review depth imply no pair. Same-role routine/demanding workflow fixtures share identical authority text; canonical policy lane exercises supported real pairs and override rejection.
3. Authority: generators parse-check only control removal and preserve every body's/grant's other fields; exact source grant gates pass. Verdicts, skill requirements, independent gates remain intact.
4. Controls: common dispatch envelope requires both controls plus verified surface/effective settings; unsupported realization blocks only its lane. Current fixed chat roles are not claimed reloaded. Unknown serving identity is a reporting limit.
5. Ownership: orchestrators select actual tasks; prompting provides capability/mechanics/projected neutrality; workflow stores decisions and cannot validate live runtime from CLI arguments.
6. Proof: contracts have all-role missing-control red fixtures; renderers preserve all native authority/bodies; modern workflow prompts reject missing runtime/model/effort, unresolved values and absent dispatch verification. Legacy model-only input remains draft; history remains readable.

## Touched scope and reasons

Both orchestrators: SKILL.md; task routing, capability route, catalogs/common dispatch and necessary implementation/installation pointers; role contracts/metadata; all native roles/manifests; renderers/contracts/aggregate source validators. Codex installation negative fixtures now prepend a supported stale pair rather than replace a removed pin. Codex mirror ownership/installation pointers now use English source routing.
Workflow: allocation/prompt owners and plan/prompt templates; optional explicit effort CLI fields; selected-control validator; six focused pure fixtures and two existing prompt integration fixtures.

## Unrun and residual limits

Independent aggregate validators, full workflow suite, both shell installer-preflight gates, cross-pack links/structure and final instruction/correctness gates remain parent-owned. Changed aggregate/preflight inputs are recorded for that inventory. No installation, shared config, commit, live task/model calibration or paid calls. Ignored workflow test bytecode was discovered with unknown ownership and preserved. No unresolved implementation scope conflict.

## Portability review closure

Changed only the Codex control route sentence: fixed loaded role definitions are conditional on the actual host; source edits alone do not prove registry reload. Draft: make fixed current-chat controls a host condition and preserve reload evidence. Compression: conditional fixed-controls clause plus the unchanged source-versus-reload boundary. No behavioral gate or native definition changed. No broad tests repeated; independent final source checks remain parent-owned.

## Explicit owner and citation repair closure

Codex renderer imports no canonical dependency before CLI parsing. It loads projection helpers from the selected owner and binds that owner's task controls while loading its policy module, restoring any prior cached dependency afterward. Renderer and validator pass the explicit owner through generated-output checks. The default sibling path and public policy API return pair remain compatible. Claude has no supported alternate-owner CLI surface and is unchanged. Missing owner still fails closed with exit 2 and the canonical-policy-unavailable validator diagnostic. No installer or grant code changed.

The workflow phase prompt, artifact admission and plan template now name each runtime orchestrator beside its own routing-matrix reference; capability/mechanics ownership and allocation meaning are unchanged. Draft: separate runtime-specific allocation citations from capability evidence. Compression: one exact owner/reference sentence per runtime.

Focused proof: `PYTHONDONTWRITEBYTECODE=1 python -B outputs/20261009-task-model-routing/policy-root-proof/proof.py`, repository cwd, sequential lightweight process, exit 0. Copied renderer without sibling owner selects the explicit policy and task-control source despite a stale dependency cache; selected projection produces all 34 unchanged outputs. Copied validator with a missing explicit owner exits 2 with the canonical-policy-unavailable diagnostic. Evidence: `policy-root-proof/proof.py` and `policy-root-proof/missing-owner.log`. No aggregate, fleet, installer preflight or broad test repeated; those remain independent gates.

Final owned source freeze: 153 regular files across both orchestrators and workflow, excluding bytecode; SHA256 `db68bab1fbdf4effc7562c7132fcee97df6e4ff530cc30e6e5a2ac9bdc2bd3a0`. Framing remains ordered repository-relative UTF-8 path, NUL, raw bytes, NUL. Shared canonical owner remains separately frozen by its lane. No unresolved implementation blocker; independent acceptance remains pending.
