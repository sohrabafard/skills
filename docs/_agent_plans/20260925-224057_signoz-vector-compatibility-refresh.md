# Workflow Plan - SigNoz and Vector compatibility refresh

- Task ID: `20260925-224057_signoz-vector-compatibility-refresh`
- Mode: `execute`
- Profile: `resumable`
- Status: blocked
- Created: `2026-09-25T22:40:57Z`
- Parent plan: not created
- Prompt pack: `docs/_agent_plans/20260925-224057_signoz-vector-compatibility-refresh__phase-prompts.md`
- Checkpoint: `docs/agents/20260925-224057_signoz-vector-compatibility-refresh-state.md`
- Machine state: not created
- Base branch and commit: main / 3a62cbb615e0180458ebedd4bc9a0794c17c1e60
- Work branch: current main checkout; no integration requested
- Worktree: current repository

## Summary and Scope

Approved: SigNoz/ClickHouse skill compatibility refresh and Vector compatibility refresh, explicitly including relevant guidance for the latest stable Vector product release at execution time.
Source ownership: skills/sohrab/alaa-signoz-clickhouse-docs/** and skills/sohrab/vector-rust-observability-pipelines/**.
Lead owns this workflow family and artifacts/signoz-vector-compatibility-refresh/**.
Excluded: every other skill, consumers, dependencies, root scripts/indexes/manifests, vendor, installed/global surfaces, deployments and benchmarks. service-runtime-kit-governance and alaa-permission-generator remain deferred. No prior wave is presumed complete or reopened.
Execution authorized in the continuation chat on 2026-09-26. Execution profile: standard; workflow profile: resumable. Reuse the current checkout under the workspace owner: tracked clean, existing untracked workflow files belong to this selected family. No branch, commit, or integration effect is needed.

## Handoff Package

- Confirmed facts: git HEAD and tracked clean state observed; both skill entrypoints inspected. On 2026-09-26 vector.dev/releases listed 0.58.0; GitHub releases/latest redirected to vdev-v0.3.24, a different product surface.
- Open assumptions: installed consumer versions, real SigNoz schema/alert capability, executable Vector availability and effective agent identity are unknown.
- Ruled out: using GitHub latest without product filtering; upgrading consumers to satisfy documentation; live discovery without authorization.
- Read first on resume: repository instructions; this plan/checkpoint/prompt; canonical prompting/workflow/orchestrator owners; complete two-skill surfaces and applicable read-only observability/security/schema owners.
- Environment notes: PowerShell; use BelowNormal priority and python -B; Node checkers run from their owning skill directory.
- Traps: current upstream docs do not prove installed schema or alert support; fixtures do not prove deployment behavior; vdev is not Vector.

## Ordered Work

### Phase 1 - Evidence and compatibility contract
- Status: completed
- Depends on: none
- Owned scope: read-only research and subject evidence.
- Excluded from this phase: all surfaces and effects excluded by Scope and Authority; Phase 1 is read-only, reviewers are read-only.
- Snapshot: HEAD 3a62cbb615e0180458ebedd4bc9a0794c17c1e60; SHA-256 05f53eb6769adb2b50974d8593d36d13425033df0617db0635d781227ddcb314; paths skills/sohrab/alaa-signoz-clickhouse-docs/** and skills/sohrab/vector-rust-observability-pipelines/**; 77 baseline Git blobs, read-only research source identity.
- Work:
  - [x] Verify baseline, dirty state, prior execution and GPT/Claude migration evidence without repeating migrations.
  - [x] Read complete relevant instructions and script CLI contracts.
  - [x] Build dated documented/installed/latest-stable/proposed-range ledgers, with unknown consumer facts preserved.
  - [x] Review full latest Vector release plus intervening releases; classify relevant capabilities, breaking/default/security changes, deprecations and fixes.
- Acceptance criteria: source-tag provenance, compatibility impacts and material decisions explicit.
- Validation commands: git status --short; git rev-parse HEAD; installed version/help commands where available.
- Evidence observed: current baseline and prior migration verified; both complete skill reads and official release research observed; preflight artifact records limits.

### Phase 2 - Owned source lanes
- Status: completed
- Depends on: Phase 1
- Owned scope: Lane S owns only alaa-signoz-clickhouse-docs/**; Lane V owns only vector-rust-observability-pipelines/**.
- Excluded from this phase: all surfaces and effects excluded by Scope and Authority; Phase 1 is read-only, reviewers are read-only.
- Snapshot: HEAD 3a62cbb615e0180458ebedd4bc9a0794c17c1e60; SHA-256 1a890b9bd8f908041a0d63ee32a1fce2eb1c4d67ce56911c2aac13b4e964665f; paths skills/sohrab/alaa-signoz-clickhouse-docs/** and skills/sohrab/vector-rust-observability-pipelines/**; 109-file manifest artifacts/signoz-vector-compatibility-refresh/candidate-snapshot-2.json.
- Work:
  - [x] Lane S refreshes version/schema/query/API references and affected examples, preserving alert-surface uncertainty.
  - [x] Lane V updates canonical release ledger and related topic guidance/examples/tests, with an explicit release-delta coverage matrix.
  - [x] Each lane adds only meaningful regression fixtures for changed executable assertions; bounded checker repairs require observed defects.
- Acceptance criteria: no date-only update, invented capability, consumer support removal or security weakening; every relevant release delta mapped to source/test or justified omission.
- Validation commands: owner checker self-tests and relevant fixture/runtime checks from matrix below.
- Evidence observed: focused lane results are recorded in subject artifacts; independent review and combined native gates are tracked below.

### Phase 3 - Independent review and integration
- Status: blocked
- Depends on: Phase 2
- Owned scope: reviewers read only; writers repair their own lanes; lead serializes workflow/evidence writes.
- Excluded from this phase: all surfaces and effects excluded by Scope and Authority; Phase 1 is read-only, reviewers are read-only.
- Snapshot: HEAD 3a62cbb615e0180458ebedd4bc9a0794c17c1e60; SHA-256 1a890b9bd8f908041a0d63ee32a1fce2eb1c4d67ce56911c2aac13b4e964665f; paths skills/sohrab/alaa-signoz-clickhouse-docs/** and skills/sohrab/vector-rust-observability-pipelines/**; 109-file manifest artifacts/signoz-vector-compatibility-refresh/candidate-snapshot-2.json.
- Work:
  - [x] Fresh instruction/correctness review; security gate if secret/confinement rules change.
  - [x] Run combined source gates and record unavailable runtime/schema proof.
  - [x] Reconcile findings, final context-curation gate and checkpoint without external memory writes.
- Acceptance criteria: no unresolved in-scope blocking findings; evidence accurately separates source, fixtures, runtime, activation and evaluation.
- Validation commands: matrix below.
- Evidence observed: focused lane results are recorded in subject artifacts; independent review and combined native gates are tracked below.

## Preservation and Intentional Changes

Preserve Vector per-path delivery, acknowledgements, fanout/retry semantics, backpressure, disk-buffer capacity/failure behavior, VRL negative tests, confinement, secrets and strict warnings.
Preserve SigNoz vendor-owned read-only tables, actual-schema authority, query time bounds/shapes, signal routing, privacy, deployment-specific authorization and fail-closed alert fallback.
Intentional change: newly verified version-qualified guidance and relevant latest Vector capabilities. No model/effort policy change or support-floor removal is approved. A materially incompatible support decision requires user selection.

## Version Sources

Revalidate dated facts at execution:
- https://vector.dev/releases/
- https://github.com/vectordotdev/vector/releases (filter stable Vector product tags; exclude vdev)
- Vector release-linked upgrade guides and tag-matched component/VRL source
- https://signoz.io/changelog/
- https://github.com/SigNoz/signoz/releases
- https://clickhouse.com/docs/whats-new/changelog

Separate stable/preview, upstream support and actual consumer pins. Preserve older consumer guidance with explicit version conditions. Do not upgrade ClickHouse merely because a newer release exists.

## Validation Matrix

From Vector skill directory inspect --help, then run node scripts/check-vector-configs.mjs --self-test and node scripts/check-upstream-version.mjs --self-test; run their regular checks where dependencies exist. Use installed target Vector validate/test only on local fixtures; preserve strict validation and report unavailable binaries.
From SigNoz directory inspect checker --help, then self-tests for check-signoz-links.py, check-signoz-schema.py and check-signoz-sql.py; run local SQL and official link checks. Schema fixtures prove checker behavior only; use already available sanitized DESCRIBE evidence if version-matched, never silently query a deployment.
From repository root:
- python -B scripts/validate_sohrab_skill_pack.py
- python -B scripts/check_skill_index.py
- python -B scripts/check_fleet_references.py
- python -B scripts/check_lifecycle_contract.py
- python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20260925-224057_signoz-vector-compatibility-refresh.md
- git diff --check

Record commands, exit codes, worktree identity and scoped content hashes. Exit 2 or missing tool/network/schema is not PASS. Execution results are recorded in the focused, repair and final evidence artifacts; unavailable runtime proof remains blocked.

## Roles, Evaluation and Traceability

One lead delegates two disjoint writer lanes; no shared source file writes. Use canonical source mappings after runtime preflight; no new role or effort mappings. Independent reviewers never fix their reviewed changes.
Approved SigNoz refresh -> S lane; approved Vector refresh plus latest-release addition -> V lane; both -> independent integration phase.
Quality acceptance: dated provenance, relevant-delta coverage, explicit compatibility and meaningful negative checks. Speed/cost gains remain unmeasured hypotheses; no benchmark authorized.

## Stop, Recovery and Authority

No install, tool/dependency/service upgrade, production/cluster/provider access, live benchmark, commit/tag/merge/publish/deploy, deletion or global configuration changes.
Material drift stops only affected work. Preserve unrelated changes; resolve overlapping ownership before editing. One cause-specific repair and one materially different retry per failed operation, then report blocker/evidence/recovery. Never weaken a gate. Missing migration proof makes only affected conclusions provisional.

## Execution preflight - 2026-09-26

- Observed root: this repository; branch main; HEAD matches the planning baseline. Tracked status is clean. Scoped status found only this family's existing untracked workflow files. Full untracked enumeration warned about inaccessible retired scratch directories under _to_delete; no cleanup attempted.
- Native text/configuration/Git tools own this prose and metadata task; no structural code discovery is needed. Hindsight recall tools are unavailable; source inspection continues under fail-open recall. Local Codex memory supplied a migration lead only, delegated for repository verification.
- Active host exposes the required canonical roles. Installed implementer-sol, researcher and verifier definitions were read; installed-versus-source preflight is in progress. Native sandbox is workspace-write; effective per-agent MCP enforcement and serving identity remain unknown. No tool isolation is claimed.
- Lead request: GPT-6 Astra, observed identity unknown. Both writer roles use their canonical configured profile, with the escalation criterion: authoring judgment-bearing skill instructions and compatibility decisions. No pin/configuration change.
- Researcher owns prior migration/role evidence read-only. Lane S owns only the SigNoz skill; Lane V owns only the Vector skill. Both first read complete owned surfaces and research without edits, then wait for lead authorization. Lead alone owns workflow and subject artifacts.
- Chosen approach: additive version-qualified guidance with centralized release ledgers, preserved consumer paths and explicit unavailable deployment proof. Rejected: blindly trusting GitHub latest, bump-only refresh, live discovery, consumer upgrades, and re-running prior migrations.
- Required gates: focused lane checks, independent combined verification, fresh correctness and instruction review; security review when secret/confinement guidance changes. Additional specialist gates follow actual changed behavior, not product names.

## Phase 1 decision and Phase 2 authorization

Both writers confirmed complete recursive skill reads before edits (Vector: 28 files), including references, scripts, fixtures and metadata. No nested target instructions found. Prior migration and installation-metadata limits are recorded in `artifacts/signoz-vector-compatibility-refresh/preflight.md`.

Vector baseline 0.57.0; official index, stable product tag and full tagged release CUE identify 0.58.0 (2026-08-26) as the only intervening stable product release. `/releases/latest` selects vdev-v0.3.24 and is excluded. Released chart vector-0.58.0 reports appVersion 0.58.0-distroless-libc. Preserve older guidance with version conditions, including 0.57 historical runtime observations. Full release coverage will live in the skill ledger. New disk oversized-record acknowledgement, buffer metric removal, field-specific confinement and security fixes require topic-owner updates and security review.

SigNoz release list/tag evidence identifies v0.143.0 (2026-09-23), superseding the cached latest redirect to v0.142.1. Chart and collector versions are recorded against immutable tags; ClickHouse upstream stable/LTS are separate from SigNoz's bundled 25.12.5. Current installed consumer versions/schema remain unknown. Investigate alert route families independently: history API deprecation is not alert-definition API removal or proof of target ClickHouse alert support.

Bounded executable repairs are authorized only for reproduced defects. SigNoz observations: non-SELECT vendor DDL bypasses S8 in CLI classification; missing sorting-key evidence returns clean; production link scan includes intentional red fixture URLs; self-test depends on external DNS. Vector stable resolution must exclude drafts/prereleases/vdev and use released chart provenance; add discriminating offline regression cases before claiming repaired behavior. No broad checker redesign.

Chosen implementation remains additive and version-qualified. No consumer support is dropped. Static/fixture proof, public release evidence and target-runtime proof stay separate. Security reviewer is required. Writers own documentation within their disjoint lanes as explicitly selected by the user; no third documentation writer. Native source gates will run independently on a frozen scoped digest.

## Candidate freeze

Both owned lanes frozen on 2026-09-26. Combined source snapshot: `artifacts/signoz-vector-compatibility-refresh/candidate-snapshot.json`, 84 files, SHA-256 fb7f8e79623ec690d3a9efbbf41dfa44ba21dbeaa1487bb1adbfcdba8f479b95. Focused source/fixture checks pass; actual Vector configuration and VRL runtime proof is unavailable (spawnSync vector.exe EPERM; regular checker exit 2). Installed SigNoz schema and alert support were not probed. Complete Phase 2 source is ready for independent review; completion remains conditional on gates. Native combined verification and reviews are pending. Source writes remain frozen until findings are routed to their original writer.

Triggered read-only specialists: security for secret/confinement and session/authorization guidance; observability for new drop/ack/recovery states and removed metrics; release guardian for chart/appVersion and version-gated configuration/upgrade guidance. No actual deployment, API implementation, or data migration is changed; architecture/adversarial/API/migration implementation gates are not triggered by documenting upstream facts.


## Review cycle 1

- Correctness: CHANGES-REQUESTED. Major: quoted vendor SQL identifiers bypass S8 through actual run dispatch. Minor: a listable persisted SQL rule is not proof of current-version save acceptance. Both route to Lane S.
- Instruction: CHANGES-REQUESTED. Major: SigNoz logs/metrics/traces narrative guides (228/323/302 lines) cannot all be exempted as atomic; cluster coherent topics, preserving each complete query/schema example. Minor: stale phase snapshot/evidence sentences conflicted with actual progress; lead corrected them in this plan.
- Security review in progress; source remains frozen until findings are consolidated. Observability review assesses drop/ack/metric-change guidance. Runtime capacity rejected two simultaneous dispatch attempts; read-only specialist dispatches serialize after slots become available. No fallback role/model or gate omission.
- Reviewer snapshot validation: correctness and instruction reviewers independently checked all 84 files against the first candidate digest. This is source identity, not runtime proof.

## Fix cycle 1 authorized

Consolidated correctness, instruction, security, observability and release-guidance verdicts are in `artifacts/signoz-vector-compatibility-refresh/review-cycle-1.md`. All actionable source findings accepted. Original S and V lanes resumed with unchanged ownership; source freeze reopened only for those findings. Focused checks will run only for affected inputs, followed by independent finding closure and combined native gates. No third documentation writer: the user selected each skill's writer as its documentation owner. Runtime Vector evidence remains unavailable; no installation permitted.


## Candidate 2 and closure

Original writers completed accepted repair cycle 1. Snapshot: artifacts/signoz-vector-compatibility-refresh/candidate-snapshot-2.json, 109 files, SHA-256 1a890b9bd8f908041a0d63ee32a1fce2eb1c4d67ce56911c2aac13b4e964665f. Exact repair commands, expected negative results and narrative document grades are in artifacts/signoz-vector-compatibility-refresh/repair-evidence.md. Phase 2 source work is complete; Phase 3 remains in progress until independent closures, native gates and final checkpoint are reconciled. Security independently closed its source finding with PASS; runtime proof remains unavailable.

## Final source checkpoint

Authorized source work and all accepted source findings are complete. Correctness and instruction reviewers returned APPROVED, security source closure PASS, observability source gap closed with runtime gaps retained. Independent verification observed four root validators and diff whitespace check passing on unchanged candidate 2. Workflow validation initially failed two plan.phase-snapshot fields; the lead corrected those exact identity fields once. Its targeted recheck and final release-guidance status are recorded in artifacts/signoz-vector-compatibility-refresh/final-evidence.md. No source file changed after candidate 2 freeze.

Overall status remains blocked solely for unavailable actual Vector proof; this is not an outstanding source repair. IMPLEMENTED: not proven; required focused Vector runtime proof blocked. Source is complete and focused static/fixture proof passed. MERGE_CANDIDATE: not established while that proof is missing. RELEASE_CANDIDATE and PUBLISHED: not requested. Source review does not establish installed SigNoz schema/alert acceptance or runtime activation. Preserve the uncommitted checkout and source manifest. Recovery: in an authorized environment with an already available exact target Vector binary, run strict validate/test and version-gated fixtures; do not install or access consumers from this request. No further source edits or prior-wave reopening are indicated.

Final reusable-context curation scanned research, accepted review decisions, repairs and limitations. Version selection and diagnostic lessons already have canonical skill/test owners; no novel durable memory candidate remains. No external memory was written. Documentation grades and the full configured/unknown-observed agent roster are in final-evidence.md.
