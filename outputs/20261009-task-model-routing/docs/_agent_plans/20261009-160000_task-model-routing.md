# Workflow Plan - Task-specific model selection for every authority role

- Task ID: `20261009-160000_task-model-routing`
- Mode: execute
- Profile: `resumable`
- Status: completed
- Created: 2026-10-09
- Parent plan: not created
- Prompt pack: not created
- Machine state: not created
- Checkpoint: `outputs/20261009-task-model-routing/docs/agents/20261009-160000_task-model-routing-state.md`
- Base branch and commit: main, 85532a8dd1be46eb226537377899523ddc998039
- Work branch: existing main checkout; no commit or merge requested
- Worktree: repository root .

## Summary and Outcome

Fix task allocation across ALL managed authority roles in both runtimes. A role defines responsibility, permissions, required skills and verdict authority; it must not itself select a model or effort. The orchestrator owns the actual task decision; prompting-guide owns current capability evidence, supported pairs, runtime precedence and controlled model-neutral projections; workflow records the allocation and continuity. Preserve quality gates and source compatibility without a full role-by-model Cartesian product.

## Scope

Four skill trees (prompting-guide, both orchestrators, necessary workflow routing pointers and allocation-generation evidence), directly affected repository ownership instructions and tests, and this archive/index. Preserve installed definitions unless a separately applicable installation authorization is resolved; source edits alone never claim activation. Six adjacent skill ownership pointers (services-contract, golang, security-review, reliability-sla, testing-strategy and repo-docs) are included narrowly. No vendor, unrelated behavior, global runtime settings, paid calibration, commit or publication.

## Handoff Package

- Confirmed facts: initial tracked tree clean at the recorded HEAD. Prompting refs90 steps1/3 exempt nonimplementation roles from task selection. Both orchestrator model-effort-policy references limit orchestrator ownership to role triggers. Policies/checkers enforce static role pins, including frontier defaults. This is the causal defect, not just a poor default for two roles.
- Open assumptions: no calibrated model equivalence or savings. Installed overrides, account access and loaded-session activation are not proven by source checks.
- Ruled out: merely lowering Fable to Opus for each role; leaving support roles exempt; duplicating every role for every model; treating different model families as necessary independence; dispatch prose overriding a fixed Codex pin.
- Read first on resume: this plan/checkpoint, source-evidence.md, lane progress files and final verification/review records in this archive.
- Environment notes: Windows PowerShell/Python; use python -B and process-local PYTHONDONTWRITEBYTECODE=1. Current chat named-role pins cannot be changed by caller; do not pretend this session has reloaded revised definitions. Initial archive cwd did not exist; created it and initializer then passed.
- Traps: role identity versus task profile, parent permission overrides, inherited effort, historical reference claims, stale installed profiles, and automatic frontier selection justified only as a second lens.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-workflow | skills/sohrab/alaa-workflow/SKILL.md | artifact decisions | always | stop affected work |
| alaa-prompting-guide | skills/sohrab/alaa-prompting-guide/SKILL.md | capability and authoring decisions | always | stop affected work |
| alaa-codex-orchestrator | skills/sohrab/alaa-codex-orchestrator/SKILL.md | delegation | always | stop affected work |
| alaa-cc-orchestrator | skills/sohrab/alaa-cc-orchestrator/SKILL.md | paired contracts | paired changes | stop affected work |
| alaa-low-noise | skills/sohrab/alaa-low-noise/SKILL.md | output | always | stop affected work |
| alaa-code-intelligence-routing | skills/sohrab/alaa-code-intelligence-routing/SKILL.md | evidence selection | source inspection | stop affected work |
| alaa-testing-strategy | skills/sohrab/alaa-testing-strategy/SKILL.md | proof design | validation | stop affected work |
| alaa-repo-docs | skills/sohrab/alaa-repo-docs/SKILL.md | report | documentation | stop affected work |
| alaa-extract-agent-lessons | skills/sohrab/alaa-extract-agent-lessons/SKILL.md | curation | closure | stop affected work |

## Acceptance Contract

1. Every managed role, including reviewer, architecture, adversarial, security, planner, researcher, verifier, documenter and rule-writer, has explicit task model/effort selection.
2. Balanced default and scope/reason/evidence determine selection. Same role supports different justified model/effort pairs. Role title, sensitivity, long task or model diversity alone does not force frontier use.
3. No model choice changes authority, grants, read-only limits, verdict format, independent gates or required skills.
4. Dispatch explicitly supplies BOTH controls on a verified runtime surface; pins/inheritance/forced overrides cannot silently defeat the selection. Unsupported or unavailable realization blocks the affected lane with evidence, not all independent work.
5. Prompting provides capabilities/presets/mechanics; orchestrators decide task allocation/admission; workflow records it. Remove contradictory ownership and fixed-role exceptions throughout active source.
6. Both runtimes' generated definitions, validators, contracts and scenarios cover the complete role inventory. Changed fixtures reject static frontier pins, missing control selections and authority drift. Source checks do not claim live model quality.

## Ratified design

Use model-neutral logical roles and explicit task-selected model AND effort. Omit both executable pins on dynamic roles. Preserve existing role identities/authority; legacy effort/model-named roles, if retained, are documented compatibility identities and cannot set selection merely through their names. Canonical policy registers dynamic roles and capabilities; any retained concrete preset is an explicitly chosen transport option, not a role default. Do not generate the Cartesian product. If a target surface cannot expose both controls, require an available exact verified realization or block that lane; no automatic config mutation or invented override.

The official current Codex docs allow spawn parameters for unpinned roles, but current named agents in this chat remain fixed. Claude Code since2.1.292 accepts non-fork invocation effort; environment/hook/provider overrides still require inspection. Use these exact differences without a second policy owner.

## Ordered Work

### Phase 1 - Establish contract and evidence

- Status: completed
- Depends on: none
- Owned scope: read-only sources and parent evidence
- Excluded from this phase: product edits
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-codex-orchestrator, alaa-low-noise
- Work:
  - [x] Inspect current checkout and causal paths. [skills: inherit]
  - [x] Obtain acceptance, runtime research and coupled design advice. [skills: inherit]
- Acceptance criteria: root cause and feasible runtime mechanism established.
- Validation commands: native source reads and official source retrieval.
- Evidence observed: explicit pin exception and validators identified; runtime researcher returned current invocation/precedence evidence.
- Snapshot: no files changed

### Phase 2 - Implement allocation and projection contracts

- Status: completed
- Depends on: Phase 1
- Owned scope: canonical policy/projection lane; paired orchestrator and workflow lane
- Excluded from this phase: installed copies and external effects
- Required skills: alaa-prompting-guide, alaa-workflow, alaa-codex-orchestrator, alaa-cc-orchestrator, alaa-low-noise
- Work:
  - [x] Replace role-fixed policy/projection contract and ownership descriptions. [skills: inherit]
  - [x] Implement all-role task allocation and executable role neutrality in both runtimes. [skills: inherit]
  - [x] Reconcile discriminating checks and generated artifacts. [skills: inherit]
- Acceptance criteria: all six criteria implemented; authoritative evidence preserved.
- Validation commands: changed policy/projection/contract/grant fixtures and scoped diff checks; independent aggregate inventory after freeze.
- Evidence observed: both frozen lane reports record focused policy, projection, contract, grants and workflow checks; review found and authors repaired partial-model validation, encoding and host-specific wording.
- Snapshot: HEAD 85532a8dd1be46eb226537377899523ddc998039 SHA256 1e5831ab97548d13862347ca355694e146b8066c9d20d5e1ce78bf16bbc0f09d paths both orchestrators and workflow; policy lane separately records c840013f171a9d3c037e8667e44ad06a9e04138f6903c3dd25c21b07275b3f7b

### Phase 3 - Independent proof and completion

- Status: completed
- Depends on: Phase 2
- Owned scope: independent review/verification, final artifacts and index
- Excluded from this phase: unrequested runtime or publication effects
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-codex-orchestrator, alaa-testing-strategy, alaa-repo-docs, alaa-extract-agent-lessons
- Work:
  - [x] Independently review complete semantics and executable controls. [skills: inherit]
  - [x] Run exact affected checks and all-role acceptance inventory. [skills: inherit]
  - [x] Reconcile curation, report, status and completion audit. [skills: inherit]
- Acceptance criteria: every explicit requirement has current direct evidence; no outstanding applicable gate.
- Validation commands: exact inventory after candidate freeze; workflow validator before handoff.
- Evidence observed: independent source review approved; all final aggregates, policy/grant/evaluation gates, 81 workflow tests, 18 installer negative paths, root structure/index/fleet/lifecycle and scoped diff checks passed. Failed earlier attempts remain recorded with their fixes and environment limits.
- Snapshot: HEAD 85532a8dd1be46eb226537377899523ddc998039 SHA256 3cfb58ae03e654fae65a158676b6df5f7f74245a928264e2f9dc12c0bba4d9c7 paths 138 changed source files listed in source-final.json

## Task Allocation

Current host role profiles are fixed; configured values below are consciously selected for these actual tasks and do not claim new dynamic behavior is already active. Observed identity unknown; no comparative calibration.

| Task | Role | Configured model/effort | Priority and reason | Dependency |
|---|---|---|---|---|
| Acceptance | alaa-spec-analyst | Sol medium | Balanced, bounded specification audit | none |
| Runtime research | alaa-researcher | Sol medium | Balanced, narrow current-document lookup | none |
| Coupled design advice | alaa-planner-high | Sol high | Balanced, coupled schema/projection/dispatch reasoning | causal findings |
| Canonical contract implementation | alaa-implementer-high | Sol high | Balanced, interdependent schema/projection/checker change | ratified design |
| Paired execution implementation | alaa-implementer-high | Sol high | Balanced, multiple coupled runtime controls and authority invariants | agreed canonical schema; rendering waits policy |
| Independent correctness | alaa-reviewer | Sol high | Balanced, transition regression/authority review | frozen candidate |
| Instruction semantics | same independent alaa-reviewer | Sol high | same reviewer covers authority/loading/ownership/compression; no unresolved specialist question | frozen candidate |
| Release compatibility | alaa-release-guardian | Sol medium | bounded schema and installer transition | frozen candidate |
| Verification | alaa-verifier | Luna low | exact observed commands | frozen inputs |

## Delegation

Two disjoint write lanes may run together. Canonical lane owns prompting tree and root/pack ownership clauses; paired lane owns both orchestrators and necessary workflow pointers/generation metadata. Rendering depends on schema-ready signal. Parent alone owns plan and integration. Observed capacity four agents including parent; queue ready work accordingly. Reuse prior inspected source and unchanged checks; changed schema invalidates affected policy/projection tests, not unrelated application suites.

## Blockers and Next Action

- Blockers: none for source implementation; current session static registrations cannot demonstrate dynamic activation.
- Next action: none for the source goal; installation, reload and publication remain separate authorized actions.

## Bounded implementation decisions

- Shared schema handshake: schema v2, all logical roles task-selected with no executable pins; canonical helper exposes validate_task_selection(role, selection, policy, resolved=None). Prompting owns control validity, not task suitability.
- Workflow initializer currently accepts runtime/model without effort and can overstate live verification. Paired owner may repair the affected generator/validator/tests narrowly: preserve historical readability, distinguish draft metadata from executable task allocation, require both controls before dispatch. This source change invalidates only affected workflow evidence.
- Focused author proof: changed renderer fixtures, contract normal/self-tests, grants normal, selection checker fixtures and affected workflow tests; one light sequential runner. Native aggregate acceptance remains independent, with covered commands consolidated.

## Final repair record

- Independent release review found the new unconditional projection-parser import incompatible with older supported hosts. Parent added optional stdlib/backport loading and a strict source-wrapper fallback; focused self-test passed. Independent release review masked both parsers and verified both renderers against current wrappers, closing the finding.
- Independent installation preflight found that explicit PolicyRoot could not resolve projection helpers before CLI parsing. Paired owner repaired the loader without weakening source rejection or destination invariants; independent PowerShell and Bash preflight passed.
- Fleet validation identified three ambiguous or misowned workflow citations; the same lane corrected the citations and the independent fleet retry passed. Unaffected passing root/workflow checks remain valid.
- Final curation: user ownership correction is promoted into canonical skills; no separate memory publication or transient-environment rule is warranted.

## Completion audit

- User requirements 1 and 2: actual task allocation belongs to each runtime orchestrator; all-role executable pins removed and explicit supported controls required. No role-title frontier exception remains.
- Acceptance A1-A16: source review approved, final affected checks passed. No live calibration or activation claim.
- Lifecycle: IMPLEMENTED and MERGE_CANDIDATE proven for the recorded uncommitted snapshot; RELEASE_CANDIDATE and PUBLISHED not requested. Uncommitted files remain locally recoverable but are not an immutable publication.
- Curation resolved through existing canonical owners; no memory write. Final docs and links checked in parent closure evidence.
