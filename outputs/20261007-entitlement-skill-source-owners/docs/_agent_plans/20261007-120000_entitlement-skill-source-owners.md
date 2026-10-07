# Workflow Plan - Entitlement skill source owners

- Task ID: `20261007-120000_entitlement-skill-source-owners`
- Mode: `execute`
- Profile: `resumable`
- Status: complete
- Created: `2026-10-07T14:34:07Z`
- Parent plan: not created
- Prompt pack: not created
- Checkpoint: `outputs/20261007-entitlement-skill-source-owners/docs/agents/20261007-120000_entitlement-skill-source-owners-state.md`
- Machine state: not created
- Base branch and commit: `main` at `2a2340d3677945578b505fce49de60e11561037d`
- Work branch: `codex/entitlement-skill-source-owners`
- Worktree: none

## Summary and Outcome

- Current repository truth: the extraction owner table in sibling `entitlement-api/docs/contracts/repository-extraction-v1.md` assigns model contracts to `authz-openfga`, API/events to `entitlement-api`, tuple projection to `entitlement-projector`, and the checker interface to `authz-sidecar`.
- Outcome: minimally repair current ownership, source paths and cross-repository route instructions in the two named skills without changing their wire or runtime contracts.
- Strategy: one implementation lane owns both skill folders; native prose/config evidence, independent verification, parent correctness review and independent instruction review. Orchestrator profile: `lean`.

## Scope

- In scope: extraction-related Markdown in `skills/sohrab/alaa-services-contract/` and `skills/sohrab/alaa-trust-gateway-auth/`; this artifact family.
- Out of scope: sibling edits, model upgrades, consumer pins, deployments, runtime code, checker changes, Postman relocation, installation, commits and remote effects; unrelated wording or router cleanup.
- Constraints and assumptions: preserve headers, envelopes, queue/event shapes, authorization rules, deadlines, stable runtime identity `projector`, and dated conformance provenance. Canonical ownership does not prove imported bundles or deployed model pins are current. No file deletion or new capability.

## Handoff Package

Knowledge that lives only in the current agent's head and disappears on compaction. Fill a field when something is learned, not on a schedule; leave a field empty rather than padding it. Field semantics are in `alaa-workflow references/context-continuity.md`, which is in the skill, not in this repository.

- Confirmed facts (verified, each with how it was verified): read-only review confirmed stale active monorepo references and retained responsibilities; extraction owner table inspected at lines 9-16. Required installed spec/implementer/verifier/instruction-reviewer role contract fields match shipped source; installed pack version sentinel is older, so it is not activation proof. Effective permission enforcement remains unknown; lane restrictions still apply.
- Open assumptions (believed but unverified, each with what would verify it): Postman destination and deployed consumer/model pins remain unknown; inspect their owners only if separately requested.
- Ruled out (approach, reason, evidence): global monorepo-name replacement would erase dated evidence; automatic `projector` telemetry rename conflicts with current `.env.example`; consumer-contract edits would violate canonical bundle ownership.
- Read first on resume (ordered exact paths): this plan; its checkpoint; `skills/sohrab/AGENTS.md`; sibling `entitlement-api/docs/contracts/repository-extraction-v1.md`.
- Environment notes (command shapes that work here, and ones that look right but fail): run repository gates from the Git root with `python -B`. Artifact initializer ran inside this subject directory to cluster plan/checkpoint products; all sources and checkpoint pointers below resolve from the Git root. The requested installed `skill-creator` was read; its packaged source below supports portable resume. Hindsight tools are unavailable; prior memory was only a lead verified against repository truth.
- Traps (looks correct, is not): accessible monorepo files and imported snapshots are not current authoring owners; historical evidence keeps its original paths and date; future executor/SPOA plans are not deployed behavior. Telemetry drift resolved in the candidate: sibling `authz-openfga/docker-compose.yml:35-36` enables JSON logs/native metrics but not trace export. The reality row now requires checking owner config; observability obligations remain unchanged.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-workflow | skills/sohrab/alaa-workflow/SKILL.md | Plan, continuity and closure | always | stop |
| alaa-codex-orchestrator | skills/sohrab/alaa-codex-orchestrator/SKILL.md | Lane admission and gates | always | stop |
| skill-creator | skills/.system/skill-creator/SKILL.md | Narrow skill update and validation | always | stop |
| alaa-services-contract | skills/sohrab/alaa-services-contract/SKILL.md | Shared contract ownership | always | stop |
| alaa-trust-gateway-auth | skills/sohrab/alaa-trust-gateway-auth/SKILL.md | Gateway trust/source ownership | always | stop |
| alaa-prompting-guide | skills/sohrab/alaa-prompting-guide/SKILL.md | Instruction draft/compression and role policy | always | stop |
| alaa-code-intelligence-routing | skills/sohrab/alaa-code-intelligence-routing/SKILL.md | Evidence selection; native prose/config owner | always | stop |
| alaa-low-noise | skills/sohrab/alaa-low-noise/SKILL.md | Bounded retrieval and lane returns | always | stop |
| alaa-memory-os | skills/sohrab/alaa-memory-os/SKILL.md | Prior ownership recall | shared-owner questions | fail-open recall; no publication |
| alaa-testing-strategy | skills/sohrab/alaa-testing-strategy/SKILL.md | Proof and check scope | validation | stop |
| alaa-repo-docs | skills/sohrab/alaa-repo-docs/SKILL.md | Artifact language, links and exemptions | Markdown writes | stop |
| alaa-codex-runtime-ops | skills/sohrab/alaa-codex-runtime-ops/SKILL.md | Independent gate transport recovery | runtime failure | preserve evidence and report blocked |
| alaa-extract-agent-lessons | skills/sohrab/alaa-extract-agent-lessons/SKILL.md | Final reusable-context gate | closure | stop |

## Ordered Work

### Phase A - Acceptance and plan

- Status: complete
- Depends on: none
- Owned scope: read-only acceptance and this plan/checkpoint.
- Excluded from this phase: product edits and external effects.
- Required skills: alaa-workflow, alaa-codex-orchestrator, alaa-prompting-guide, alaa-code-intelligence-routing, alaa-low-noise, alaa-memory-os, alaa-repo-docs
- Work:
  - [x] Revalidate checkout, required role contracts and extraction ownership. [skills: inherit]
  - [x] Obtain the spec analyst's observable acceptance and select one settled implementation lane. [skills: inherit]
- Acceptance criteria: active owners and preserved behavior are explicit; no unresolved decision needed for source-routing repairs.
- Validation commands: native file inspection; role TOML field comparison; `git status`, `git rev-parse HEAD`.
- Evidence observed: scoped checkout clean; required role contract fields match; spec acceptance received. Existing-infrastructure check not triggered: no shared image, generator or reusable script created.
- Snapshot: no files changed

### Phase B - Minimal implementation

- Status: complete
- Depends on: Phase A
- Owned scope: both named skill folders, Markdown only.
- Excluded from this phase: scripts, metadata, sibling files and external effects.
- Required skills: skill-creator, alaa-services-contract, alaa-trust-gateway-auth, alaa-prompting-guide, alaa-code-intelligence-routing, alaa-low-noise, alaa-repo-docs
- Work:
  - [x] Read each skill's complete contract/resources and fix active extracted-owner references. [skills: inherit]
  - [x] Preserve wire/runtime rules and historical evidence; compress authored instructions without losing behavior. [skills: inherit]
- Acceptance criteria: canonical model/mapping owner is `authz-openfga`; events and audiences use `entitlement-api`; projection uses repository `entitlement-projector`; checker interface uses `authz-sidecar`. Route procedure separates owners, consumes pinned generated bundles and preserves pin agreement. Active orientation/telemetry separates repositories while preserving runtime names. Trust source map retains gateway executable precedence. Postman references are historical or explicitly unresolved, never assigned to an invented destination. Dated conformance remains dated.
- Validation commands: focused scoped diff review and new source-pointer existence checks; no exhaustive pack gates in the implementation lane.
- Evidence observed: 12 reference files changed; SKILL/script/metadata and dated conformance/deadline/queue files unchanged. Implementer reports 18/18 source-pointer checks and focused `git diff --check` exit 0. Parent independently measured normalized sizes: services 430883 to 430800 bytes; trust 135534 to 135513 bytes. Diff saved as `outputs/20261007-entitlement-skill-source-owners/skill-diff.patch`.
- Snapshot: HEAD 2a2340d3677945578b505fce49de60e11561037d; SHA256 978b8b181a5381fe502232d3baa487a50b9ef55df97b4b54da1283068059048a; paths skills/sohrab/alaa-services-contract/ and skills/sohrab/alaa-trust-gateway-auth/; manifest `outputs/20261007-entitlement-skill-source-owners/candidate-manifest.json`.

### Phase C - Independent verification

- Status: complete
- Depends on: Phase B
- Owned scope: read-only integrated candidate; evidence files inside this subject directory.
- Excluded from this phase: product edits, installations, runtime/deployment checks and external effects.
- Required skills: alaa-testing-strategy, alaa-services-contract, alaa-trust-gateway-auth, alaa-low-noise
- Work:
  - [x] Freeze the two skill folders and capture HEAD plus deterministic SHA-256 content manifest. [skills: inherit]
  - [x] Execute applicable skill, fleet, index, lifecycle, instruction and trust checks. [skills: inherit]
- Acceptance criteria: all required static gates and checker self-tests pass; every new source pointer is verified; evidence names commands, snapshots and limits. This proves instructions/configuration statically, not deployed authorization.
- Validation commands: `python -B scripts/validate_sohrab_skill_pack.py`; `python -B scripts/check_skill_index.py`; `python -B scripts/check_fleet_references.py`; `python -B scripts/check_lifecycle_contract.py`; `python -B skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py`; `python -B skills/sohrab/alaa-trust-gateway-auth/scripts/trust_boundary_check.py --self-test`; requested skill-creator `quick_validate.py` for both skills; touched-link check with `alaa-repo-docs/scripts/check_markdown_links.py`; `git diff --check`. Run sequentially, no downloads or product mutations.
- Evidence observed: ten static commands exited 0; 43 hashes, encoding, source pointers, protected unchanged files and whole-skill sizes verified. See verification.md. Its incorrect alternate aggregate method was reconciled by an independent focused follow-up, preserving original evidence; see verifier-snapshot-final.md. Runtime/deployed proof excluded.
- Snapshot: HEAD 2a2340d3677945578b505fce49de60e11561037d; SHA256 978b8b181a5381fe502232d3baa487a50b9ef55df97b4b54da1283068059048a; paths skills/sohrab/alaa-services-contract/ and skills/sohrab/alaa-trust-gateway-auth/.

### Phase D - Correctness and instruction review

- Status: complete
- Depends on: Phase C
- Owned scope: read-only complete skill diff and acceptance.
- Excluded from this phase: fixes, artifact mutations and external effects.
- Required skills: alaa-codex-orchestrator, alaa-prompting-guide, skill-creator, alaa-services-contract, alaa-trust-gateway-auth, alaa-low-noise
- Work:
  - [x] Parent reviews correctness; instruction reviewer independently checks ownership, source selection and compression. [skills: inherit]
  - [x] Route any findings to the implementer and revalidate only affected evidence. [skills: inherit]
- Acceptance criteria: approved; no unresolved blocker/major. Check scenarios: add a protected route, diagnose a deny, resolve a notification audience and refresh a conformance snapshot. No new authorization, security-control, API-shape, migration, observability-level or deployment change is admitted; corresponding product specialist gates are not triggered.
- Validation commands: native read-only diff/source inspection.
- Evidence observed: original major API bundle-consumer omission resolved in one bounded fix to the protected-route reference. Independent instruction-closure-final.md is APPROVED with no findings. Independent verifier-closure-final.md reports three affected checks PASS and 43 unchanged final hashes. Parent reviewed the two-hunk delta; runtime-model SHA, migration/admission and compatible version differences are explicit. Final structure and affected fleet checks also exit 0 in final-static-results.json. No sibling source was edited.
- Snapshot: HEAD 2a2340d3677945578b505fce49de60e11561037d; SHA256 e6fa953819342848986a77ba0ce1e37f63969d0d639e395c478213842fa533cf; paths skills/sohrab/alaa-services-contract/ and skills/sohrab/alaa-trust-gateway-auth/; candidate-manifest-v2.json. Initial review evidence retains its v1 identity.

### Phase E - Final audit and closure

- Status: complete
- Depends on: Phase D
- Owned scope: artifact family; candidate held unchanged.
- Excluded from this phase: new skill edits, sibling changes, commits and external effects.
- Required skills: alaa-workflow, alaa-codex-orchestrator, alaa-extract-agent-lessons, alaa-repo-docs, alaa-testing-strategy
- Work:
  - [x] Reconcile every acceptance criterion with the final diff and observed evidence. [skills: inherit]
  - [x] Finish curation, workflow validation and exact final scope inspection. [skills: inherit]
- Acceptance criteria: all scoped fixes present and independently approved; artifacts current; no unexplained changes. Skill instructions are semantically atomic; plan/state are named exempt artifacts under repo-docs sizing. Separate product documentation lane skipped: runtime/product behavior is unchanged. No additional exhaustive runtime tier is applicable to a Markdown-only owner/path repair; full pack static checks ran once on the initial candidate; a later bounded paragraph correction requires only affected revalidation and instruction closure review.
- Validation commands: `python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan outputs/20261007-entitlement-skill-source-owners/docs/_agent_plans/20261007-120000_entitlement-skill-source-owners.md`; final Git status/diff and artifact link validation.
- Evidence observed: acceptance reconciled with final diff, independent approval and observed static proof. Curation retained no new durable candidate; owner facts already have canonical sources, and transport/digest detours stay in task evidence. No memory publication or pipeline reopen is needed. Workflow and artifact-link results are recorded in final-audit.md and final-artifact-validation.json; final skill snapshot held unchanged.
- Snapshot: HEAD 2a2340d3677945578b505fce49de60e11561037d; SHA256 e6fa953819342848986a77ba0ce1e37f63969d0d639e395c478213842fa533cf; paths skills/sohrab/alaa-services-contract/ and skills/sohrab/alaa-trust-gateway-auth/. Task evidence is clustered under outputs/20261007-entitlement-skill-source-owners/.
- Lifecycle: IMPLEMENTED proven on final uncommitted snapshot; MERGE_CANDIDATE proven by applicable gates and independent approval; RELEASE_CANDIDATE not requested; PUBLISHED not requested. Local recovery risk: candidate is uncommitted. Integration not requested; last authorized commit and branch span unavailable.

## Delegation

- Keep shared-context work in the main conversation.
- Spec: `minimal_fix_spec`, read-only; configured `gpt-6.1-sol` / `medium`, observed identity unknown.
- Implementation: one `alaa-implementer` owns both skill folders; ratified owner mapping needs no difficult-design escalation. Parent owns artifacts/integration.
- Verification: `alaa-verifier` via independent ephemeral CLI after collaboration spawn exhausted its thread limit; instruction gate: `alaa-instruction-reviewer` via independent ephemeral CLI; lean correctness gate: parent. Installed role contract fields verified; runtime effective grants remain unknown and restrictions are enforced procedurally.
- Dispatches assume zero shared context: copy the relevant handoff-package facts into the dispatch text rather than referring to this conversation.
- Lanes report changed paths; this plan's owner records the validated snapshot and handles any explicitly authorized commit.

## Blockers and Next Action

- Blockers: none unresolved. Collaboration thread-limit and startup-permission failures were recovered; original instruction finding is closed. See runtime-recovery.md and instruction-closure-final.md.
- Next action: none; local requested outcome complete. Commit, integration and publication remain unauthorized and unrequested.
