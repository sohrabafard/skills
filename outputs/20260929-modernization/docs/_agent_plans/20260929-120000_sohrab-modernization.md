# Workflow Plan - Sohrab current model and domain modernization

> Citation notation: `<repo>/` denotes this repository root; resolve it before invoking a command. Path lists use this display prefix only; strip it when reproducing a recorded hash manifest. [Original exact evidence](./20260929-120000_sohrab-modernization.raw.txt.gz) preserves the pre-normalization text.

- Task ID: `20260929-120000_sohrab-modernization`
- Mode: `execute`
- Profile: `resumable`
- Execution profile: `standard`
- Status: completed
- Created: `2026-09-29T09:00:18Z`
- Parent plan: none; the 20260926 plan is historical provenance.
- Prompt pack: not requested
- Checkpoint: `../agents/20260929-120000_sohrab-modernization-state.md`
- Machine state: none
- Base branch and commit: `main`, `0e9681c8253de0373a9bbbe4a9ff24a91b38c6db`
- Work branch: `codex/sohrab-sonnet55-modernization`
- Worktree: current repository checkout

## Summary and Outcome

Assess all 69 first-party skills against current official sources. Migrate active Sonnet 5 policy and guidance to verified Sonnet 5.5 behavior. Keep one coherent policy for GPT-6 Sol/Astra/Luna and Claude Fable 5.1/Opus 5.5/Sonnet 5.5. Update only evidenced findings while retaining production safety, security, testability, debugging, naming and maintainability.

This artifact family lives under `skills/sohrab/alaa-workflow/outputs/20260929-modernization/` to respect the user's write boundary. Other paths are repository-relative.

## Scope

- In scope: skills/sohrab skills and their references, policy, scripts, examples, assets, projections and manifests.
- Out of scope: root files, vendor/third-party trees, installed copies, consumer services, installation, deployment, commits, pushes and publication.
- Preserve existing work. User confirmed prior changes committed/pushed at the base SHA; rechecked tracked status was clean.
- No silent model fallback, fabricated version facts, unmeasured quality claims, indiscriminate version bumps or duplicate doctrine.
- Read each affected skill in full before editing. Draft instruction changes, then apply behavior-preserving compression.
- Keep compatibility guidance instead of raising consumer minimums without evidence and any required user decision.

## Acceptance Contract

1. Plan/checkpoint pass workflow validation and permit cold-start continuation.
2. Exactly one dated assessment per current skill records official sources, stable/preview distinction, consumer applicability, finding, disposition and proof or unknown.
3. Active Sonnet pins, routing, examples, metadata, evaluations and fixtures agree with Sonnet 5.5. Historical comparisons stay labeled historical.
4. Requested model families use one canonical policy. Configured selection never implies live serving identity or calibration.
5. Changes preserve triggers, ownership, authority, safety, exceptions, failure/stopping rules and meaningful examples; production advice specifies observable actions.
6. Applicable native gates and independent correctness/instruction reviews pass on a captured snapshot. Static, live, skipped, failed and blocked proof remain distinct.

## Handoff Package

- Confirmed facts: inventory is 69 immediate SKILL.md directories; official Sonnet 5.5 overview/migration/prompting docs verified on 2026-09-29. Canonical model policy is alaa-prompting-guide/assets; 12 Sonnet profiles project into alaa-cc-orchestrator agents. Native prose/config inspection owns evidence here. Base HEAD and clean tracked status rechecked.
- Open assumptions: every subject's applicable stable version, consumer versions, live Claude availability and calibration require evidence.
- Ruled out: blanket Sonnet replacement (historical facts and capabilities differ); domain copies of model policy; rewriting all skills without findings; modifying previous root-level plan; creating a second goal (host already created it).
- Read first on resume: this plan, its handoff package, checkpoint, assessment.json, then next lane's evidence and owned skill. Reconcile git status before acting; always reload after compaction.
- Environment notes: PowerShell and Python 3.13. Use python -B. Initializer succeeded from this artifact directory with ../../scripts/init_workflow_files.py; ../../../ was wrong. Branch creation needed sandbox escalation and succeeded. Do not use Bash brace expansion in PowerShell.
- Traps: full-skill reads found model delegation-template drift and frontend executable-example defects; fix their owning files and meaningful regressions before acceptance. Historical plan excluded model pins; this goal supersedes that exclusion. Role pins are configured evidence, actual identity/isolation unknown. Hindsight recall tools unavailable; continue with repository truth. No memory writes authorized. Legacy retired directories cause untracked status warnings; use scoped status.

## Ordered Work

### Phase A - Intake and durable plan

- Status: completed
- Depends on: none
- Owned scope: workflow artifacts
- Excluded from this phase: all other phase ownership and global exclusions.
- Work:
  - [x] Inspect rules, baseline, role contracts and evidence owners.
  - [x] Obtain independent specification and official model research.
  - [x] Create branch and resumable artifact family inside scope.
  - [x] Write scope, acceptance, phases, ownership and resume protocol.
  - [x] Create 69-skill assessment inventory.
  - [x] Validate and present plan before implementation.
- Acceptance criteria: acceptance 1 with complete coverage inventory.
- Validation commands: workflow scripts/validate_workflow_files.py --plan <this-plan>.
- Evidence observed: initializer exit 0; base identity and clean tracked status; spec_contract six criteria; model_research official migration findings.
- Snapshot: HEAD 0e9681c8253de0373a9bbbe4a9ff24a91b38c6db; SHA256 0f0cd525c1bb6bfbc9e049979a6c37857b7bedcaa551ce01da08b303d151d342; paths intake-evidence.md installed-role-observations.json; sorted UTF-8 path/content SHA256 manifest phase-a.sha256; uncommitted.

### Phase B - Model policy and projections

- Status: completed
- Depends on: Phase A
- Owned scope: prompting-guide, paired orchestrators, low-noise model projections
- Excluded from this phase: all other phase ownership and global exclusions.
- Work:
  - [x] Persist dated official research and exact migration findings.
  - [x] Read full affected skills and update canonical policy, guides, fixtures and evaluations. The initial read-order lapse was reconciled and documented in model-evidence.md.
  - [x] Update controlled agent projections, active references and runtime availability guards.
  - [x] Run focused policy/evaluation/renderer/grants/pack gates as affected; independent integrated acceptance remains pending.
  - [x] Reconcile actual diffs, evidence, assessment and checkpoint; 32 source files including staged guide, aggregate SHA256 1f941b4d7824741502030c1c551f057ca3df5f5d2fbddde63f94e4883dc65df4.
- Acceptance criteria: acceptance 3-5; historical references preserved; calibration unrun unless measured.
- Validation commands: applicable focused owner validators, integrated commands listed in Phase D, and workflow validation after state updates.
- Evidence observed: model-evidence.md, 23 focused executions across 13 distinct commands; all final outcomes pass. Independent acceptance is Phase D.
- Snapshot: HEAD 0e9681c8253de0373a9bbbe4a9ff24a91b38c6db; SHA256 1f941b4d7824741502030c1c551f057ca3df5f5d2fbddde63f94e4883dc65df4; paths 32 source files listed in model-evidence.md; includes staged guide, uncommitted.

### Phase C - All-topic research and domain updates

- Status: completed
- Depends on: Phase A; model-owner decisions before model wording changes
- Owned scope: uniquely assigned skill directories in assessment.json
- Excluded from this phase: all other phase ownership and global exclusions.
- Work:
  - [x] Research backend/data/messaging/Go group. Evidence: backend-research.json, fourteen rows; private kit and consumer versions remain unknown.
  - [x] Research frontend/browser/media/design group. Evidence: frontend-research.json, nine coverage rows; one compatibility evidence gap remains explicit.
  - [x] Research infrastructure/operations/observability group. Evidence: operations-research.json, sixteen rows; consumer compatibility unknown.
  - [x] Research provider/security/contracts/specialized group. Evidence: specialized-research.json, fifteen rows.
  - [x] Research workflow/governance/testing/documentation group. Evidence: governance-research.json, eleven rows.
  - [x] Reconcile all 69 assessments against current content and consumer applicability. Six research JSON files cover the inventory; explicit unknowns remain consumer-specific.
  - [x] Dispatch exact disjoint edit scopes from findings; full skill reads precede edits.
  - [x] Apply justified changes and examples/assets; source edits and required focused proof complete. Independent verification-fix1.json closes ShellCheck and integration findings. Frontend scope includes verified Vue async-unmount promise, IndexedDB outbox ordering/blocked-helper, Shaka null-source unload and QoE in-flight queue-cap data-loss defects discovered during full reads. Preserve contracts; no new dependencies or installs. Operations scope also includes Arvan read-only verification (no implicit token mint or impersonation; an optional runner account must match the authenticated context) and fail-closed secret-output permissions/existing-file protection; use synthetic proof only. Full reads also justify bounded Docker corrections for cgroup-aware Go defaults, Compose file-backed secret permission limits, and Swarm host publishing versus loopback. Specialized wording corrects Mediana Unicode Nd documentation and Jitsi object-storage ownership without changing behavior. Source-confirmed GitLab corrections cover project-scoped resource groups, queue ordering versus discarding, unmatched workflow rules and supported changes-path variables; checker fixtures change only when current rejection contradicts official semantics. Full Ansible reads also require explicit operator bootstrap opt-in (never inferred agent installation authority), redacted secret findings with unchanged result shape, truthful Molecule stage/teardown failures and mocked regression proof; no real drivers or installations.
  - [x] Record changed/no-change/blocked disposition for every skill: 25 implemented pending independent gates; 44 assessed no-change, including one explicit private-phase unknown.
- Acceptance criteria: acceptance 2 and 5; no absent result treated as current proof.
- Validation commands: applicable focused owner validators, integrated commands listed in Phase D, and workflow validation after state updates.
- Evidence observed: backend-evidence.md, frontend-evidence.md, operations-evidence.md, specialized-evidence.md; focused passes and optional/environment failures recorded separately. Required independent shell checks and all review gates remain Phase D.
- Snapshot: HEAD 0e9681c8253de0373a9bbbe4a9ff24a91b38c6db; SHA256 2809135720497a6214f06123176c1c09ce422259b3953726e92317de1e85c614; paths 140 source files in candidate.sha256 across 25 skills; includes model lane, excludes mutable workflow artifacts; uncommitted.

### Phase D - Independent verification and review

- Status: completed
- Depends on: Phases B and C
- Owned scope: frozen candidate, read-only gates
- Excluded from this phase: all other phase ownership and global exclusions.
- Work:
  - [x] Capture HEAD, observed tool versions and scoped SHA-256 manifest. Candidate3 verifier observed native Python3.11.16; other exact version observations remain in lane evidence, no inferred version claims.
  - [x] Independent verifier runs applicable integrated gates and coverage checks. First-candidate evidence plus verification-fix1.json: required checks pass; optional environment failures and pending final document grading remain explicit.
  - [x] Deep correctness review of policy/projection/script interactions and changed scope. Candidate2 CHANGES-REQUESTED; six findings recorded in review-correctness.json.
  - [x] Instruction review of ownership, exceptions, scope, compression and authority. Independent instruction_review APPROVED candidate2; record review-instructions.json. Later instruction changes reopen affected review.
  - [x] Run triggered security/release/observability gates; BLOCK/conditional findings recorded. Migration preflight SAFE-WITH-CONDITIONS for indexed account-purge repair.
  - [x] Resolve cycle1 findings through owning writers; operations12file repair and frontend20file repair complete. Minimal frontend cycle2 COR7 repair independently APPROVED; security and observability repairs closed. Preserve all expected-red, failed and environment-blocked evidence.
  - [x] Recapture repaired candidate4 and obtain affected independent closure. Correctness/security approved; observability/migration/release approved with consumer-only conditions; instruction approved with one wording nit assigned to final documentation. Final documentation edits reopen affected gates.
- Validation commands: root <repo>/scripts/validate_sohrab_skill_pack.py, check_skill_index.py, check_fleet_references.py, check_lifecycle_contract.py via python -B; git diff --check; affected skill validators. Run checker self-tests only for changed checkers. Model commands come from prompting-guide SKILL.md. Docs links/grades use alaa-repo-docs checker.
- Acceptance criteria: acceptance 6; one cause-specific repair/retry per failed operation; at most two review fix cycles.
- Validation commands: applicable focused owner validators, integrated commands listed in Phase D, and workflow validation after state updates.
- Evidence observed: initial review reports plus recorded fix-closure reports close all executable findings. Final candidate8 instruction review closes documentation D1-D8/R1-R3; no source findings remain. Optional environment failures and consumer-only adoption conditions remain explicit.
- Snapshot: HEAD 0e9681c8253de0373a9bbbe4a9ff24a91b38c6db; SHA256 f502125cdda2acdadc4115ce289c95abc92cd9953d1b33a20c67ecd5bf76dc2d; paths 154 source files in candidate-4.sha256 across 25 skills; executable review closed, final documentation reopens affected gates; uncommitted.

### Phase E - Documentation and final handoff

- Status: completed
- Depends on: Phase D
- Owned scope: isolated final docs lane and lead-owned workflow files
- Excluded from this phase: all other phase ownership and global exclusions.
- Work:
  - [x] Document final verified behavior and source provenance; independent candidate8 instruction approval accepts 232 GREEN, 73 YELLOW, 18 ORANGE and 11 atomic exemptions, with no eligible RED.
  - [x] Refresh affected hash manifests through owner scripts and inspect landed files. Candidate8 contains 378 source paths across 25 skills; final EOF-only delta verified.
  - [x] Re-run gates affected by final edits; cite valid unchanged proof. Candidate7/8 parent receipts, final independent verification and diagnostic closure identify all inputs and exits.
  - [x] Final reusable-context curation;zero admitted; existing canonical owners retain all reusable rules; no memory publication authorized.
  - [x] Validate workflow/coverage, cold-start review, final scope and checkbox reconciliation; final status artifact gate recorded in final-status-gates.json.
  - [x] Report four completion states, proof limits, agent roster and accounting in completion-report.json and agent-roster.json; user handoff follows.
- Acceptance criteria: implementation, evidence, docs and status agree; no unexplained changes or invented live claims.
- Validation commands: applicable focused owner validators, integrated commands listed in Phase D, and workflow validation after state updates.
- Evidence observed: candidate8 instruction review APPROVED; independentverification plus diagnosticclosure PASS; parentnativeaffectedgates PASS; optional historical/environment failures remain explicit.
- Snapshot: HEAD 0e9681c8253de0373a9bbbe4a9ff24a91b38c6db; SHA256 78de558ae3d3ef8b60e26f0860636952652ed198ad6595a7a7527838c6d1672f; paths 378 source files in candidate-8.sha256 across 25 skills; uncommitted, staging preserved.

## Delegation

Lead owns plan/checkpoint, assessment ledger, integration and authority. Research lanes are read-only with bounded evidence returns. Spec/research roles are configured Sol/medium; observed identity unknown. Judgment-dense instruction writing uses alaa-implementer-sol (Astra/high). At most two writers concurrently, each owning whole disjoint skill directories; reuse agents for their lanes. Independent gates never fix. Every dispatch includes outcome, ownership, exclusions, criteria, commands, dependencies and alaa-low-noise return bounds. Exact per-skill statuses live in assessment.json; dispatched identities and current lanes are in agent-roster.json. All source is frozen at candidate8. Executable repairs and both isolated documentation lanes completed; independent final instruction review APPROVED. Final verifier is active after host capacity release. Authorization clarification is limited by authorization-guidance-review.md; design status not-required because behavior and contracts remain unchanged.

## Blockers and Next Action

- Blockers: none for requested local scope. Consumer adoption, installation, livecalibration, release andpublication were not requested or run.
- Next action: deliver the completed local handoff. Final status gates passed; no source work remains. Any later commit/install/push/release needs explicit user authority.
