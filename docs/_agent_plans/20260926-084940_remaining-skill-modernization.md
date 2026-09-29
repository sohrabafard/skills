# Workflow Plan - Remaining first-party skill modernization program

- Task ID: `20260926-084940_remaining-skill-modernization`
- Mode: `plan`
- Profile: `resumable`
- Status: planning
- Created: `2026-09-26T08:49:40Z`
- Parent plan: not created; consolidates remaining audit work without superseding prior evidence
- Prompt pack: `docs/_agent_plans/20260926-084940_remaining-skill-modernization__phase-prompts.md`
- Checkpoint: `docs/agents/20260926-084940_remaining-skill-modernization-state.md`
- Machine state: not created
- Base branch and commit: main / 5d29c92c07bac8bcdc52f1c0c8bd107e5a5d8364
- Work branch: not created in planning
- Worktree: current repository

## Goal and Approval Record

The user selected consolidation of all remaining audit items into one final program after explicitly postponing Vector runtime validation. Earlier authority remains: first-party skills/sohrab only; planning here, implementation in a separate chat.
Approved local correction scope: unresolved F05/F06/F07; remaining F09 rows including ansible-validator and clickhouse-performance-schema-ops; bounded Kubernetes gate closure.
Approved research scope: F08 and all remaining Not assessed rows, with evidence-based classification, not speculative implementation. This retains the original W5 research-only boundary.
Explicitly deferred, not rejected: F02 service-runtime-kit-governance; F04 alaa-permission-generator; actual Vector validate/test recovery. No recommendation is permanently rejected in the available user record.
Excluded by authority: F10 installed/global reconciliation, F12 root install-skills.md correction, new roles, retirement, major consumer upgrades, model/effort policy changes, external effects and benchmarks.
Already handled: F01/F11 normalization/Arvan and F03 W2. Their checkpoints record local completion; no reopened implementation. F07 router changes in reliability/services must preserve completed F03 behavior.
SigNoz/Vector sources are recorded reviewed and complete, runtime proof still blocked/unverified. Preserve that distinction and leave those source scopes read-only.
One complete program includes completed, retained, research-only, deferred and blocked dispositions; it does not promise a clean bill of health for every skill.

## Handoff Package

- Confirmed facts: current HEAD observed with git; tracked status empty. Full untracked enumeration warned about inaccessible archived workflow-test directories, so full cleanliness is not claimed. Current migration checkpoints both completed; their recorded verification summaries exist. Historical hash manifests do not certify all current files.
- Open assumptions: current consumer versions, full untracked inventory, effective role activation, serving identity, provider contracts and required binary availability need scoped verification.
- Ruled out: treating Not assessed as None; generic fleet compression; replaying completed migrations; authorizing installs or deferred Vector retries through broad selection.
- Read first on resume: AGENTS.md; skills/sohrab/AGENTS.md; this family; artifacts/skill-modernization-audit-20260925/{audit.md,per-skill.json,inventory.json,versions.md}; canonical prompting/workflow/orchestrator owners; prior checkpoint/evidence paths below; README.fa.md routing map before skill edits.
- Environment notes: PowerShell and python -B, BelowNormal process priority. Native file evidence for instruction documents. Windows rg glob filters must use -g on the directory, not wildcard filenames passed as paths.
- Traps: a refreshed ledger is not a consumer upgrade; source pins are not activation; release docs are not installed proof; independent reviews may be capacity-blocked; stale historical audit rows may already be solved.

Prior state sources:
- docs/agents/20260925-110010_claude-model-migration-state.md; artifacts/claude-model-migration/final-workflow.log
- docs/agents/20260925-120000_gpt6-agent-migration-state.md; artifacts/gpt6-agent-migration/verification-summary.md
- docs/agents/20260925-143542_normalization-arvan-selected-fixes-state.md
- docs/agents/20260925-211735_w2-queue-deadline-semantics-state.md
- docs/agents/20260925-220655_k8s-helm-compatibility-refresh-state.md; artifacts/k8s-helm-compatibility-refresh/final-evidence.md
- docs/agents/20260925-224057_signoz-vector-compatibility-refresh-state.md; artifacts/signoz-vector-compatibility-refresh/final-evidence.md

## Ownership and Authorized Writes

The 69-row table below defines item-level authority. CORRECT permits only the cited audit correction inside that skill's directory, after full reading and current evidence. CLOSE permits only scoped Kubernetes closure and necessary in-scope gate repairs. RESEARCH permits evidence artifacts, never source edits. RETAIN, COMPLETE and DEFER permit no source writes.
Lead owns this three-file workflow family and artifacts/remaining-skill-modernization/**. For Kubernetes closure only, lead may update the existing Kubernetes plan/prompt/checkpoint and evidence directory; preserve its history. Prior other families stay read-only.
Exclude vendor, third-party skills, newly added skills, root scripts/indexes/manifests/configuration, installed copies and external consumers. A root checker finding outside the selected source change is reported, not repaired.
Shared core lane is serialized: alaa-memory-os, both orchestrators, alaa-prompting-guide, alaa-code-intelligence-routing, alaa-reliability-sla and alaa-services-contract. Low-noise remains a read-only owner. No model pins, grants, generated wrappers or installer changes.
Compatibility lanes own disjoint directories: data/RabbitMQ/ClickHouse; Go; GitLab/HAProxy/Ansible; Quasar/Shaka. Assign at most one writer per file, respect available capacity, and prohibit a second lane editing a shared owner.

## Ordered Work

### Phase 1 - Reconcile evidence and freeze scope
- Status: pending
- Depends on: none
- Owned scope: read-only original inventory and prior evidence; lead workflow/evidence.
- Excluded from this phase: source writes, migration replay, external systems.
- Work:
  - [ ] Verify root, baseline, dirty state, current inventory and affected migration evidence.
  - [ ] Reconcile all 69 rows with current files; mark already-solved items without repeating edits.
  - [ ] Enumerate exact affected files and hashes within the named write directories before dispatch.
  - [ ] Verify roles/grants and build grouped official-source research queue.
- Acceptance criteria: no unclassified inventory row, no assumed completion, explicit file ownership.
- Validation commands: git rev-parse HEAD; git status --short --untracked-files=no; scoped untracked checks; owner source checks only when current drift justifies them.
- Evidence observed: planning baseline above; execution not started.
- Snapshot: no implementation changes in this phase yet.

### Phase 2 - Close Kubernetes gates
- Status: pending
- Depends on: Phase 1
- Owned scope: existing Kubernetes family/evidence; alaa-k8s-helm only for a demonstrated scoped closure defect.
- Excluded from this phase: new Kubernetes feature work, installs, clusters, Vector retry.
- Work:
  - [ ] Fix recorded workflow snapshot path syntax; validate the exact family.
  - [ ] Use one fresh bounded recovery cycle for freshness evidence and independent correctness review.
  - [ ] Reuse passing checks only if relevant hashes and environment assumptions still match.
- Acceptance criteria: actual outstanding gates pass or remain precisely blocked; never relabel blocked as complete.
- Validation commands: existing Kubernetes plan and recorded failure commands; no broad rerun.
- Evidence observed: historical source review/gates passed; freshness/workflow/reviewer closure blocked.
- Snapshot: existing 58-file evidence is historical; compare current content before reuse.

### Phase 3 - Shared owners and routing
- Status: pending
- Depends on: Phase 1; can proceed if Phase 2 is environment-blocked
- Owned scope: serialized core lane named above.
- Excluded from this phase: pins, grants, global/installed reconciliation, root installation docs.
- Work:
  - [ ] F05 refresh Hindsight source compatibility snapshots from official core/package evidence; keep global reconciliation separate.
  - [ ] F06 place runtime mechanics behind canonical owner and mirror orchestrator behavior; preserve recovery, observability and host-specific requirements.
  - [ ] F07 consolidate routers in code-intelligence-routing, reliability-sla and services-contract without lost triggers/exceptions or W2 drift.
- Acceptance criteria: one owner, mirrored orchestration, complete trigger reachability, authority and failure-case equivalence.
- Validation commands: applicable owner checks plus static positive/negative instruction scenarios; independent instruction/correctness gate.
- Evidence observed: universal watchdog/one-command text remains in both orchestrator bodies at planning time.
- Snapshot: capture scoped source hashes before/after.

### Phase 4 - Remaining compatibility groups
- Status: pending
- Depends on: Phase 3 for shared-owner edits; independent research may start after Phase 1
- Owned scope: nine CORRECT compatibility skill directories in the table.
- Excluded from this phase: installed upgrades, consumer changes, unapproved support-floor increases.
- Work:
  - [ ] Data lane: alaa-data-layer, alaa-laravel-job-rabbitmq, clickhouse-performance-schema-ops.
  - [ ] Go lane: alaa-golang; retain kit go.mod authority.
  - [ ] Operations lane: alaa-gitlab-ci-cd, alaa-haproxy, ansible-validator.
  - [ ] Frontend lane: alaa-quasar-app-vite-v3, alaa-shaka-player.
  - [ ] Produce dated compatibility tables and correct only evidence-backed version-sensitive instructions/examples.
- Acceptance criteria: exact released API/command provenance, explicit supported consumer ranges and unknowns; no latest-by-default migration.
- Validation commands: each skill's documented checker/help/self-tests and exact installed tool fixtures where available; no invented flags or install to obtain proof.
- Evidence observed: not run.
- Snapshot: lane manifests and combined candidate after integration.

### Phase 5 - Complete unassessed evidence
- Status: pending
- Depends on: Phase 1; read-only lanes may overlap non-conflicting work
- Owned scope: evidence only for RESEARCH rows, including F08 providers and unresolved Arvan platform facts.
- Excluded from this phase: source implementation for newly discovered findings.
- Work:
  - [ ] Read substantive instructions, references, scripts and metadata; classify A/B/C independently.
  - [ ] Use shared official dependency research; request no credentials or live access under this authority.
  - [ ] Record per-row category, issue/evidence, size, priority, proposed change, preserved behavior, dependencies, risk, expected benefit, validation, confidence and official source.
  - [ ] Present concrete newly justified changes for user selection; unavailable evidence stays blocked, never None.
- Acceptance criteria: every remaining row has explicit evidence coverage or named gap; new findings are reviewable and unimplemented.
- Validation commands: bounded non-destructive local self-tests where meaningful; no live benchmarks.
- Evidence observed: original audit only; not a full current semantic assessment.
- Snapshot: inspected source hashes and research dates.

### Phase 6 - Independent integration and final disposition
- Status: pending
- Depends on: Phases 2-5 completed or explicitly dispositioned blocked/deferred/research-only
- Owned scope: independent gates; lead workflow/evidence only.
- Excluded from this phase: unselected fixes, release or installation.
- Work:
  - [ ] Independent correctness and instruction review; security/API/release specialists only for triggered risks.
  - [ ] Integrate selected changes and validate frozen source; same writers repair owned findings.
  - [ ] Publish a 69-row final disposition and outstanding decision list without overwriting historical audit evidence.
  - [ ] Run workflow context-curation gate; record outcome without global memory writes.
- Acceptance criteria: selected edits independently accepted; every check truthful; all deferred/blocked/new-proposal work visible.
- Validation commands: combined matrix below and workflow validator.
- Evidence observed: not run.
- Snapshot: final scoped hashes and command evidence; no commit required.

## Versions, Sources and Preserved Capabilities

Initial audit versions.md and per-skill.json supply historical leads, not current release truth. Execution records each dependency once with five separate fields: documented version; observable consumer requirement/binary; latest officially supported stable; proposed compatibility range; migration implications. Record dates, URLs and release tags; separate previews and missing facts.
Official owners: OpenAI/Anthropic runtime docs; github.com/vectorize-io/hindsight/releases and package release sources; go.dev/doc/devel/release; laravel.com/docs and locked driver source; rabbitmq.com/docs; clickhouse.com/docs; docs.gitlab.com and instance/Runner evidence; haproxy.org version docs; docs.ansible.com; quasar.dev and official Quasar releases; shaka-player-demo.appspot.com/docs/api and official Shaka releases.
Current exact version targets are intentionally unresolved until Phase 1/4 research: select documentation corrections without changing consumer floors. Unsupported claims block only their dependent edit.
Preserve domain depth, triggers, exceptions, failure handling, authority/security, required evidence and completion. Specifically preserve durable-job receipt/W2 semantics, database transaction/tenant boundaries, Go kit authority, CI approvals, HAProxy parser/security behavior, Ansible safety, Quasar older supported consumers and Shaka attach/destroy/credentials behavior.

## Blockers

No planning blocker. Execution may be blocked by unavailable roles, source drift, upstream evidence, consumer versions or binaries. Kubernetes has recorded freshness/workflow/review blockers; Vector runtime recovery remains deferred. Resolve only within the approved scope.

## Validation, Evaluation and Recovery

Run owner gates proportionally, then combined root gates:
- python -B scripts/validate_sohrab_skill_pack.py
- python -B scripts/check_skill_index.py
- python -B scripts/check_fleet_references.py
- python -B scripts/check_lifecycle_contract.py
- python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20260926-084940_remaining-skill-modernization.md
- git diff --check

Inspect actual CLI contracts before calls. Use relevant code/script regression fixtures only for behavior changes; do not add tautological tests for prose. Independent reviewers inspect the actual candidate, not writer conclusions. No self-approval. Exit 2/unavailable is failed-to-run, never PASS. Record source/fixture/runtime/activation/evaluation separately and preserve canonical lifecycle definitions.
For instruction changes, use a fixed before/after scenario matrix covering positive/negative triggers, host differences, authority, interruption and recovery. Independent review checks identical preserved assertions; intentional improvements have explicit cases. Live model evaluation is not authorized. A future measured comparison would hold tasks/context/tools/gates constant, use repeated independent runs, and compare time/tokens/cost only for quality-passing runs. No measured benefit claimed now.
No before/after model-effort table: no mapping change selected. Revalidate canonical role availability and pins; unknown activation is not permission to substitute.
Retry budget: per failed operation, one cause-specific repair and one materially different retry. Kubernetes gets one newly scoped cycle; Vector runtime is explicitly excluded. Then stop the affected operation with evidence/recovery and continue independent work. No indefinite repair loop or weakened gates.
Authority exclusions: no install, upgrades, live model benchmarks, authenticated provider/production/cluster access, external messaging, commit/tag/merge/push/publish/deploy, deletion, retirement, global configuration or consumer mutation. Any required excluded change becomes a concrete separate decision.

## Traceability

F01/F11 -> COMPLETE prior family; F02/F04 -> DEFER; F03 -> COMPLETE and preservation constraint; F05/F06/F07 -> Phase 3; F08 -> Phase 5 research; F09 -> Phase 2/4, with SigNoz/Vector retained; F10 -> excluded installed proposal; F12 -> excluded root-doc proposal. All other Not assessed rows -> Phase 5. Algorithms -> RETAIN based on inspected static guidance.

## Per-skill Disposition and Write Allowlist

Original audit classifications remain historical; dispositions below define this program's authority. Every skill path is relative to skills/sohrab/.
| Skill | Audit size / priority | Disposition / phase | Approved action |
|---|---|---|---|
| alaa-algorithms-data-structures | None / Defer | RETAIN | Inspected static guidance unchanged |
| alaa-arvan-object-storage | Not assessed / P1 | RESEARCH / 5 | Evidence completion only; new source changes need selection. Obtain primary provider evidence before changing capability claims |
| alaa-async-messaging | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain body; assess durable-job implications only with F03 |
| alaa-bale-provider | Not assessed / P1 | RESEARCH / 5 | Evidence completion only; new source changes need selection. W5 obtain current Safir contract; no fundamental rewrite inferred |
| alaa-bash-shell | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Verify target shell and action before any edit |
| alaa-cc-orchestrator | Minor / P1 | CORRECT / 3 | F06 host-aware cadence behind canonical runtime owner; provisional until W0 |
| alaa-cicd-laravel-postgres | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. No change until target CI and database evidence |
| alaa-code-intelligence-routing | Minor / P2 | CORRECT / 3 | F07 move router; preserve all trigger conditions |
| alaa-codex-orchestrator | Minor / P1 | CORRECT / 3 | F06 canonical host-aware guidance; F10 installation remains separate |
| alaa-codex-runtime-ops | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain exact-gate recovery until concrete failing case |
| alaa-controlled-ops | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Inspect actual package and adopter before classification |
| alaa-crockford-base32-codecs | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. No rewrite inferred from age; inspect/run selected conformance separately |
| alaa-data-layer | Minor / P1 | CORRECT / 4 | W4 refresh selected version-specific guidance against consumers |
| alaa-docker-production | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Preserve guidance pending exact target compatibility |
| alaa-extract-agent-lessons | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain inspected behavior; no rewrite justified |
| alaa-frontend-developer | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Preserve body until consumer-specific audit |
| alaa-frontend-devops | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Check consumer build contract before changes |
| alaa-frontend-doc-annotations | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Verify target source before refreshing annotations |
| alaa-gitlab-ci-cd | Minor / P2 | CORRECT / 4 | W4 refresh feature ledger without raising minimum blindly |
| alaa-go-chi-development | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Keep kit authority; assess current kit before changes |
| alaa-golang | Minor / P1 | CORRECT / 4 | W4 version-aware baseline review; no automatic toolchain migration |
| alaa-golang-clean-code-principles | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain principles pending source-linked kit review |
| alaa-golang-fiber | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Reverify APIs before choosing an update |
| alaa-haproxy | Minor / P2 | CORRECT / 4 | W4 refresh supported-branch ledger |
| alaa-haproxy-lua | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain rules until exact binary/API audit |
| alaa-indexeddb-browser-storage | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Validate selected browser APIs and supported versions first |
| alaa-input-normalization | Minor / P1 | COMPLETE | Prior local result; no reopening |
| alaa-k8s-helm | Minor / P1 | CLOSE / 2 | Bounded pending gate closure only |
| alaa-keyset-pagination | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain contract until consumer-framework assessment |
| alaa-laravel-architecture | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. No change without current consumer architecture |
| alaa-laravel-job-rabbitmq | Minor / P1 | CORRECT / 4 | W4 verify driver/monitor-method deltas before refreshing facts |
| alaa-laravel-public-api-contract-pack | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Preserve refusal until executable routes/contracts inspected |
| alaa-laravel-upgrade-all-packages | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. No upgrade recommendation without consumer evidence |
| alaa-low-noise | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain behavior; resolve paired-orchestrator cadence in their scope |
| alaa-makefile | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Check supported target Make before edits |
| alaa-memory-os | Minor / P1 | CORRECT / 3 | F05 source ledger/compatibility refresh; global and installed changes separate |
| alaa-minio-object-storage | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Do not change compatibility without provider evidence |
| alaa-mongodb-patterns | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Keep server/driver matrix boundary |
| alaa-mono-package | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Inspect consumer workspace exports/locks first |
| alaa-observability-soc | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain canonical names versus requirement ownership |
| alaa-octane-performance | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Check installed server/Octane before API changes |
| alaa-partitioned-table-fk-audit | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Assess detector on target major before change |
| alaa-permission-generator | Minor / P1 | DEFER | Explicit user deferral; no edits |
| alaa-php-clean-code | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain target policy; full examples/consumer not assessed |
| alaa-postman-collections | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Verify current schema and importer before changes |
| alaa-project-constitution | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain ratification; inspect selected template before edit |
| alaa-prompting-guide | Minor / P1 | CORRECT / 3 | Provisional F06 canonical host-aware runtime facts; keep model pins unchanged |
| alaa-quasar-app-vite-v3 | Minor / P2 | CORRECT / 4 | W4 refresh version delta ledger |
| alaa-reliability-sla | Fundamental / P1 | CORRECT / 3 | F07 routing only; preserve completed F03 |
| alaa-repo-docs | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain body behavior; no rewrite justified |
| alaa-security-review | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain doctrine; no standards migration proposed |
| alaa-services-contract | Minor / P2 | CORRECT / 3 | F07 routing only; preserve completed F03 |
| alaa-shaka-player | Minor / P2 | CORRECT / 4 | W4 inspect API/default deltas; refresh ledger only |
| alaa-signoz-clickhouse-docs | Minor / P1 | DEFER | Source closure retained; runtime/activation proof deferred, no edits |
| alaa-sms-provider-mediana | Not assessed / P1 | RESEARCH / 5 | Evidence completion only; new source changes need selection. W5 obtain primary contract before expanded send guidance |
| alaa-system-design | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain design doctrine; no generic shortening |
| alaa-testing-strategy | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain proof tiers and gate strength |
| alaa-trust-gateway-auth | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. No change without gateway/service contract evidence |
| alaa-ui-ux-design-system | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain accessibility target; no whole-skill None claim |
| alaa-vue-typescript-clean-code | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain stable/preview distinction |
| alaa-workflow | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain current workflow; use it only after user selection |
| ansible-generator | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Keep generator role until target compatibility review |
| ansible-validator | Minor / P2 | CORRECT / 4 | Schedule compatibility/EOL review; no immediate floor bump |
| caas-arvan-kuber | Minor / P0 | RESEARCH / 5 | F01 completed; only remaining platform evidence research, no edits |
| clickhouse-performance-schema-ops | Minor / P2 | CORRECT / 4 | W4 selected SQL feature/version provenance review |
| jitsi-platform-architect | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Obtain target deployment and current docs before change |
| service-runtime-kit-governance | Minor / P0 | DEFER | Explicit user deferral; no edits |
| tusd-upload-platform | Not assessed / Defer | RESEARCH / 5 | Evidence completion only; new source changes need selection. Retain distinction; no version defect shown; consumer/client latest unknown |
| vector-rust-observability-pipelines | Minor / P1 | DEFER | Source closure retained; runtime/activation proof deferred, no edits |

Coverage: 69 original first-party skills. No new skill is automatically admitted.
