# Workflow Plan - Skill pack optimization

- Task ID: `20261018-000000_skill-pack-optimization`
- Mode: `execute`
- Profile: `resumable`
- Task store: `beads`
- Task binding: AGENTS.md#beads
- Task hierarchy: phase-task-subtask
- Review boundary: final
- Final phase: Phase 4
- Commit authority: explicit user grant: original task instruction to commit accepted phase work on the current branch; this engagement defers the scoped commit to final review acceptance.
- Status: complete
- Created: `2026-10-18T14:43:21Z`
- Parent plan: not created
- Completed provenance: `docs/_agent_plans/20261018-134259_skill-pack-review-verification.md`
- Prompt pack: not created
- Checkpoint: `docs/agents/20261018-000000_skill-pack-optimization-state.md`
- Machine state: not created; no automated JSON consumer exists
- Base branch and commit: `main` at `1a0799de71254427973f1253d80b846fea9acf10`
- Work branch: `main`; remain on the branch executing the plan
- Worktree: current repository checkout; no new worktree
- Root issue: `alaa-6dh`; discovered-from `alaa-kzj`

## Summary and Outcome

Completed source-grounded optimization of the skill pack. Every proposal receives one final parent-ratified outcome: implement/adapt with evidence, or reject with a reason. After handling each item, the parent removes it from its input report. Completion requires all three report files to exist at zero bytes, the mandatory cadence to be implemented, and the single final review/fix/test stage to pass.

All registered implementation and acceptance work passed through the single independent review boundary in Phase 4. This completion record is prepared for the authorized final commit; it becomes effective when that scoped commit succeeds and is verified. On commit failure, restore executing status and the delivery cursor. Live closure and the actual commit SHA are recorded in Beads alaa-6dh.5.2.2 and alaa-6dh.

## Scope and authority

- Inputs: `artifacts/skill-pack-review-20261018/01-contradictions-and-overlaps.md`, `02-optimization.md`, and `03-new-skill-proposals.md`. The current inputs contain 82, 34 and 8 numbered proposals respectively. These are file-item counts, not recounted Codex/Claude chats.
- Verify current cited skill references and read the initial recommendations; judge their reasoning. Do not audit transcript counts or scan private chat history.
- Product scope: the exclusive first-party skill trees in the ownership table, their source-owned helpers/fixtures/generated repository projections, and required repository indexes/instructions. Read every owned skill and its references/scripts before editing; load nested instructions first. New files are English, UTF-8 without BOM, LF and emoji-free.
- Preserve `vendor/`, third-party skill packs, installed/global definitions, sibling repositories and existing unrelated changes. Read-only inspection of a named sibling owner or official upstream source is permitted when needed to settle a reported fact; no sibling write follows from it.
- The user's phase-end commit instruction is standing authority for accepted execution commits on the current branch, not for planning-only commits. This engagement's explicit final-only review defers all intermediate commits. After Phase 4, the parent commits accepted scoped changes under this recorded authority.
- Push, tag, merge, deploy, install, global changes, memory publication and Dolt remote sync remain unauthorized. No persistent Goal or automation is created by this plan.
- Input reports already have user edits. Their item removal is authorized during execution. Existing verification artifacts and the older plan/checkpoint remain untouched. Record and preserve the unrelated staged index; do not use broad staging or an ordinary commit that would sweep it in.
- A retired file moves to `_to_delete/<YYYYMMDD>-<reason>/` with source/destination size evidence. Emptying the three named report files is explicitly requested; keep the files present.

## Mandatory policy to implement

This is an intentional behavior change, followed by a behavior-preserving compression pass.

| Decision | Canonical owner and required behavior |
|---|---|
| Hierarchy and task authority | Workflow task-tracking owns phase -> task -> subtask registration. New phased/delegated execution plans require an explicitly adopted, verified Beads binding. Register every node, parent-child relation, real blocking edge and acceptance criterion before dependent execution. Missing binding blocks dependent dispatch; do not create a substitute database or local tracker. |
| Compatibility | Preserve completed archives and existing local families until explicit migration. Small direct single-phase work and advice retain their admission boundaries; the new requirement does not silently rewrite all historical/local artifacts. |
| Subtask end | Only very short checks specific to its changed behavior. Select the smallest test/path/scenario that can distinguish success from the relevant error. No separate reviewer or independent verification pipeline is spawned. |
| Task end | Run bounded task acceptance tests, combining the affected subtasks' coverage. No separate task review. Reuse passing checks with identical covered inputs, environment, flags and observer requirements. |
| Review boundary | Mirrored orchestrator verification-and-gates owners schedule review at the declared phase end or whole-engagement end. Explicitly identify scope, current/final phase and review boundary. This engagement selects whole-engagement end. A nested orchestrator invocation cannot silently reset the final candidate to each task/phase. |
| Failures | Fix the defect and rerun the failing path. Never weaken assertions, suppress findings, lower review standards, change fixtures to conceal failure or add a review to each repair. Respect the existing finite repair/retry budget; preserve exact blockers and continue independent safe work. |
| Check necessity | Testing-strategy owns proof strength and the need for a check. For an added discretionary check, state the uncovered risk and why existing evidence is insufficient. Fixed time limits or blanket container prohibitions are not invented. New expensive setup/full suites do not belong to a subtask's tiny check. |
| Aggregate reuse | A required final aggregate can discharge covered narrower checks only with demonstrated identical inputs/environment/flags and required authority. Markdown can be a checker input; a documentation-only diff is not automatic equivalence. A phase transition, new agent or compaction alone does not invalidate evidence. |
| Commits | Workflow owns Git authority/evidence; orchestrators schedule the action. After successful boundary review, fixes and tests, commit with a Conventional Commit message on the current branch when explicit user authority is recorded. No task/subtask commit, failed-phase commit or repeated approval request. With final-only review, defer commits until final acceptance. |
| Evidence and closure | A tested leaf may close with its snapshot and test evidence while phase/engagement review remains pending. Leaf closure must never claim independent review occurred. Under final-only review, close an intermediate phase issue after its implementation/test criteria pass and record REVIEW_PENDING in the plan. This unblocks the next phase without claiming reviewed acceptance or permitting a commit; Phase 4 alone owns independent acceptance. |

Do not add a new cadence skill. Workflow owns hierarchy/continuity, testing-strategy proof necessity and strength, and the mirrored orchestrators runtime scheduling. Consumers point to these owners. Templates, helper schemas, fixtures, role contracts and repository projections must agree; prose-only repair is insufficient.

## Intake evidence and proposal protocol

- Immutable original inputs and prior dirty-tree evidence: `artifacts/skill-pack-optimization-20261018/intake-snapshot.json`.
- Exhaustive initial numbered-item ownership: `artifacts/skill-pack-optimization-20261018/proposal-routing.json`. Each of the 124 IDs occurs once. This is a static routing artifact, not an editable progress register.
- Initial Beads dependency import: `artifacts/skill-pack-optimization-20261018/initial-dependencies.jsonl`. It records the applied 66 edges for audit, never becomes a ready-set cache or competing task store.
- Final item decisions/results live in the owning Beads issue comments/acceptance, never in a second TODO ledger. Record report ID, current source/anchor, initial recommendation, final decision and reason, changed paths or rejection rationale, check/evidence address and snapshot.
- A proposal may be adapted or rejected after current-source verification; report labels and prior reviewer conclusions are leads. Do not mark uncertainty as a false fact or delete an item merely because its work is inconvenient.
- For an accepted item, remove it only after the required scoped implementation/checks exist and parent ratification is recorded. For a rejected item, record the source-based reason before removal. Parent is the sole writer of all three source reports, batches removals at completed task boundaries and preserves original numbering until removal.
- Cross-owner items have one primary decision issue; consumer patches stay with their exclusive writer. A domain task may close after its owned implementation and checks pass, recording unresolved consumer obligations in its evidence. Integration owns their completion and final proposal disposition; report removal waits for the full adopted outcome. This avoids a phase dependency cycle when an integration-owned consumer follows the domain phase.
- File 03's nine coverage rows route to SHARED (V1/V2), MEMDOC (V3/V4/V9), CTRL (V5/V6), PLATFORM (V7) and WF (V8); harness note H1 routes to CTRL. Legacy appendix N-8 and all summary/appendix/scaffolding sections route to INTEGRATE. Their raw text is preserved in the intake snapshot.
- No terminal deferred proposal is allowed: after bounded evidence retrieval, either implement a grounded alternative or reject the proposed action with an explicit reason. An unresolved required correction blocks completion and its item stays in the report. External-repository work may be rejected as outside this scope and recorded as a separately authorized follow-up, never silently implemented.

## Ratified decisions and evidence-sensitive remedies

User steering during execution: preserve the Bash external topic map and keep a short triggered pointer in the body. Router count alone does not justify moving an existing map into always-loaded SKILL.md. CTRL restores that map and reconciles the central and authoring placement rule; later lanes preserve external maps unless actual context/routing evidence justifies relocation. This is a design correction, not a measured runtime performance claim.

The user subsequently confirmed keeping the small direct single-phase nondelegated local-plan exception. The mandatory hierarchy governs new phased/delegated plans; no broader admission change is authorized or needed. The attached Beads skill is byte-identical to this checkout's upstream owner; CLI mechanics remain there, while the repository binding and workflow own hierarchy, acceptance and test/review cadence. Completion explicitly includes root `alaa-6dh` and phase epics `.3`, `.4` and `.5` after their criteria pass.

These decisions constrain implementation; a contrary live owner requires a recorded reassessment.

| Proposals | Decision / preserved behavior |
|---|---|
| 01:A49-A51, 02:P1-P6, 03:N6 | Implement the mandatory hierarchy/cadence above. Replace per-subtask reviewed-completion rules, define final scope, preserve independent final acceptance and support evidence subsumption. |
| 02:P7 | Add a generic changed-path-to-gate mapping contract only if needed in the constitution owner. Do not alter deploy's rules or bypass repository gates. Reject this task's proposed deploy mutation as out of scope. |
| 02:O1 | Body size is a prioritization signal, not a defect. Optimize consulted/duplicated material in already affected owners with preserved triggers and unique rules. Reject a blanket cleanup of system-design/algorithms or a warning-clearance target; record every affected portion's disposition. |
| 01:A36, B28; 02:O20-O21 | Mirror real behavioral changes in both orchestrators, preserve their allowed runtime/delegation differences, and keep scheduling, proof, return bounds and persistence with distinct owners. |
| 01:A6, A46, B10, C3; 02:O2 | Ratify the single call-form and marker conventions centrally. Preserve external topic maps and remove duplicate body routers; reference count alone never justifies relocation. A separately justified relocation preserves all triggers/destinations and follows retirement rules. Do not create a competing uncertainty taxonomy. |
| 01:A7-A9, B8-B9 | Use canonical contract/actual gateway evidence for limits, deny codes and timeouts. Do not invent a cursor-code registry or choose 503/504 from prose preference. |
| 01:A21, A33, A41-A42, B19, B21, C1-C2 | Preserve unique cache/fallback/histogram and request/connection requirements. Shared owner decides requirement versus value; security owns masking policy, Docker/Kubernetes express controls. No hypothetical signal names. |
| 01:A3-A5, B1-B5; 02:O10-O11 | Correct upgrade selection and require lock-diff rejection of unintended majors. Retain generic run-twice proof beyond queue redelivery. Express unsupported major-framework migration honestly; no invented new capability. |
| 01:A14-A18, B15-B20; 02:O8-O9,O19,O24,O26 | Preserve bounded shutdown, signal ownership, kit action-specific phase statuses, trace reinjection/warnings and error-text prohibition. Set one import/race/TDD owner without dropping stack-specific predicates. |
| 01:A19-A23,A39,B11-B13; 02:O6,O13 | Repair every duplicated sanitizer/SW occurrence, including frontend reference 30's network-only clause. Distinguish subset versus total-route budgets, preserve manual SW scenarios and retain required QA when SSR/PWA applies. |
| 01:A27-A31,B24; 02:O3,O5,O14 | Verify tusd StopUpload/upstream hook semantics and revocation-outage policy. Separate application versus tusd sizing/configuration, preserve the known missing tenant-prefix/migration warning, and label unsafe historical commands where copied. No invented replacement command or default. |
| 01:A1-A2,A40,A47-A48; 02:O12,O16,O17 | Preserve narrow Arvan activation and retry budget; one canonical Ansible gate list includes module currency. Do not replace a necessary cluster resource with a semantically different namespaced one. A pin printer does not refresh upstream facts or dates. |
| 01:A10-A13,A24-A26,A34-A35; 02:O7,O15,O25 | Remove unsourced volatile counts, conditionalize commit/apply authority, keep memory shape semantic and serialization adapter-specific, separate audit findings from installation, and fix actual documentation routing. |
| 01:A32,B22,B25; 02:O22,O23 | Retain provider-specific ambiguity/vendor mappings and raw/aggregate project_id requirements; route generic doctrine. Preserve dated ClickHouse provenance rather than inventing a replacement. |
| 01:B23; 02:O4,O27 | Preserve Shaka-specific behavior and cover every API family the checker recognizes (including ads, tracks and offline), not only configure/error paths. |
| 03:N1 | Reject a new runner-bootstrap skill now; existing GitLab/Docker owners exist. Add a portable owner extension only if current source evidence establishes a missing reusable procedure. No deploy implementation is inferred. |
| 03:N2 | Extend existing observability/shared-contract/Quasar owners. Repair the dangling Sentry pointer; separate canonical fleet names from ecosystem package selection; verify official SDK/browser/SSR behavior before normative changes. |
| 03:N3 | Separate tool-schema misuse/stale patch context from shell/harness recovery. Use current tool/official schema evidence and existing prompting/runtime owners; do not add a generic patch-failure skill. |
| 03:N4,N5,N7,N8,H1 | No new skill. Existing recovery/completion/loading/language owners cover most claims; reject unproven causal explanations. Any admitted extension needs a demonstrated gap. Global language/hooks and unobserved tool failures stay out of scope. |

## Skill Bindings

Load each binding before its owning decision/write when its mapped lane applies. A missing owner stops the dependent step; do not substitute or install it.

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-workflow | skills/sohrab/alaa-workflow/SKILL.md | Decision/write | always | Stop |
| alaa-codex-orchestrator | skills/sohrab/alaa-codex-orchestrator/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-prompting-guide | skills/sohrab/alaa-prompting-guide/SKILL.md | Decision/write | always | Stop |
| alaa-low-noise | skills/sohrab/alaa-low-noise/SKILL.md | Decision/write | always | Stop |
| alaa-code-intelligence-routing | skills/sohrab/alaa-code-intelligence-routing/SKILL.md | Decision/write | always | Stop |
| alaa-memory-os | skills/sohrab/alaa-memory-os/SKILL.md | Decision/write | mapped lane | Stop |
| beads | .agents/skills/beads/SKILL.md | Decision/write | always | Stop |
| alaa-testing-strategy | skills/sohrab/alaa-testing-strategy/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-cc-orchestrator | skills/sohrab/alaa-cc-orchestrator/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-extract-agent-lessons | skills/sohrab/alaa-extract-agent-lessons/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-project-constitution | skills/sohrab/alaa-project-constitution/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-bash-shell | skills/sohrab/alaa-bash-shell/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-codex-runtime-ops | skills/sohrab/alaa-codex-runtime-ops/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-repo-docs | skills/sohrab/alaa-repo-docs/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-services-contract | skills/sohrab/alaa-services-contract/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-keyset-pagination | skills/sohrab/alaa-keyset-pagination/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-trust-gateway-auth | skills/sohrab/alaa-trust-gateway-auth/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-security-review | skills/sohrab/alaa-security-review/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-observability-soc | skills/sohrab/alaa-observability-soc/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-reliability-sla | skills/sohrab/alaa-reliability-sla/SKILL.md | Decision/write | mapped lane | Stop |
| vector-rust-observability-pipelines | skills/sohrab/vector-rust-observability-pipelines/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-php-clean-code | skills/sohrab/alaa-php-clean-code/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-laravel-architecture | skills/sohrab/alaa-laravel-architecture/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-laravel-upgrade-all-packages | skills/sohrab/alaa-laravel-upgrade-all-packages/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-octane-performance | skills/sohrab/alaa-octane-performance/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-async-messaging | skills/sohrab/alaa-async-messaging/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-laravel-job-rabbitmq | skills/sohrab/alaa-laravel-job-rabbitmq/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-laravel-public-api-contract-pack | skills/sohrab/alaa-laravel-public-api-contract-pack/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-minio-object-storage | skills/sohrab/alaa-minio-object-storage/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-arvan-object-storage | skills/sohrab/alaa-arvan-object-storage/SKILL.md | Decision/write | mapped lane | Stop |
| tusd-upload-platform | skills/sohrab/tusd-upload-platform/SKILL.md | Decision/write | mapped lane | Stop |
| caas-arvan-kuber | skills/sohrab/caas-arvan-kuber/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-docker-production | skills/sohrab/alaa-docker-production/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-haproxy | skills/sohrab/alaa-haproxy/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-haproxy-lua | skills/sohrab/alaa-haproxy-lua/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-k8s-helm | skills/sohrab/alaa-k8s-helm/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-gitlab-ci-cd | skills/sohrab/alaa-gitlab-ci-cd/SKILL.md | Decision/write | mapped lane | Stop |
| ansible-generator | skills/sohrab/ansible-generator/SKILL.md | Decision/write | mapped lane | Stop |
| ansible-validator | skills/sohrab/ansible-validator/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-golang | skills/sohrab/alaa-golang/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-golang-clean-code-principles | skills/sohrab/alaa-golang-clean-code-principles/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-go-chi-development | skills/sohrab/alaa-go-chi-development/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-golang-fiber | skills/sohrab/alaa-golang-fiber/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-data-layer | skills/sohrab/alaa-data-layer/SKILL.md | Decision/write | mapped lane | Stop |
| service-runtime-kit-governance | skills/sohrab/service-runtime-kit-governance/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-frontend-developer | skills/sohrab/alaa-frontend-developer/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-frontend-devops | skills/sohrab/alaa-frontend-devops/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-vue-typescript-clean-code | skills/sohrab/alaa-vue-typescript-clean-code/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-quasar-app-vite-v3 | skills/sohrab/alaa-quasar-app-vite-v3/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-ui-ux-design-system | skills/sohrab/alaa-ui-ux-design-system/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-shaka-player | skills/sohrab/alaa-shaka-player/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-indexeddb-browser-storage | skills/sohrab/alaa-indexeddb-browser-storage/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-permission-generator | skills/sohrab/alaa-permission-generator/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-partitioned-table-fk-audit | skills/sohrab/alaa-partitioned-table-fk-audit/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-mongodb-patterns | skills/sohrab/alaa-mongodb-patterns/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-bale-provider | skills/sohrab/alaa-bale-provider/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-sms-provider-mediana | skills/sohrab/alaa-sms-provider-mediana/SKILL.md | Decision/write | mapped lane | Stop |
| alaa-signoz-clickhouse-docs | skills/sohrab/alaa-signoz-clickhouse-docs/SKILL.md | Decision/write | mapped lane | Stop |
| clickhouse-performance-schema-ops | skills/sohrab/clickhouse-performance-schema-ops/SKILL.md | Decision/write | mapped lane | Stop |

## Ownership and integration barriers

Paths below are under `skills/sohrab/`. A row owns each named entire skill tree, including source helpers and its generated repository files; it does not own installed copies. No two active writers may own the same tree.

| Lane / task issue | Exclusive skill trees | Additional semantic prerequisites |
|---|---|---|
| WF / alaa-6dh.2.1 | `alaa-workflow/`, `alaa-testing-strategy/` | alaa-6dh.1.1 |
| ORCH / alaa-6dh.2.2 | `alaa-codex-orchestrator/`, `alaa-cc-orchestrator/` | alaa-6dh.2.1.1 (frozen decisions) |
| CTRL / alaa-6dh.2.3 | `alaa-prompting-guide/`, `alaa-low-noise/`, `alaa-extract-agent-lessons/`, `alaa-project-constitution/`, `alaa-bash-shell/` | alaa-6dh.2.1.1 (frozen decisions) |
| MEMDOC / alaa-6dh.2.4 | `alaa-memory-os/`, `alaa-codex-runtime-ops/`, `alaa-repo-docs/`, `alaa-code-intelligence-routing/` | alaa-6dh.1.1 |
| SHARED / alaa-6dh.3.1 | `alaa-services-contract/`, `alaa-keyset-pagination/`, `alaa-trust-gateway-auth/`, `alaa-security-review/`, `alaa-observability-soc/`, `alaa-reliability-sla/`, `vector-rust-observability-pipelines/` | alaa-6dh.2.1, alaa-6dh.2.3, alaa-6dh.2.4 |
| PHP / alaa-6dh.3.2 | `alaa-php-clean-code/`, `alaa-laravel-architecture/`, `alaa-laravel-upgrade-all-packages/`, `alaa-octane-performance/`, `alaa-async-messaging/`, `alaa-laravel-job-rabbitmq/`, `alaa-laravel-public-api-contract-pack/` | alaa-6dh.2.1, alaa-6dh.2.3, alaa-6dh.2.4 |
| STORAGE / alaa-6dh.3.3 | `alaa-minio-object-storage/`, `alaa-arvan-object-storage/`, `tusd-upload-platform/` | alaa-6dh.2.1, alaa-6dh.2.3, alaa-6dh.2.4 |
| PLATFORM / alaa-6dh.3.4 | `caas-arvan-kuber/`, `alaa-docker-production/`, `alaa-haproxy/`, `alaa-haproxy-lua/`, `alaa-k8s-helm/`, `alaa-gitlab-ci-cd/`, `ansible-generator/`, `ansible-validator/` | alaa-6dh.2.2, alaa-6dh.2.3, alaa-6dh.2.4 |
| GO / alaa-6dh.3.5 | `alaa-golang/`, `alaa-golang-clean-code-principles/`, `alaa-go-chi-development/`, `alaa-golang-fiber/`, `alaa-data-layer/`, `service-runtime-kit-governance/` | alaa-6dh.3.1.1 (frozen decisions), alaa-6dh.3.2.1 (frozen decisions), alaa-6dh.2.1, alaa-6dh.2.2 |
| UI / alaa-6dh.3.6 | `alaa-frontend-developer/`, `alaa-frontend-devops/`, `alaa-vue-typescript-clean-code/`, `alaa-quasar-app-vite-v3/`, `alaa-ui-ux-design-system/` | alaa-6dh.3.1.1 (frozen decisions), alaa-6dh.2.1, alaa-6dh.2.3 |
| PLAYER / alaa-6dh.3.7 | `alaa-shaka-player/`, `alaa-indexeddb-browser-storage/` | alaa-6dh.3.3.1 (frozen decisions), alaa-6dh.3.6.1 (frozen decisions), alaa-6dh.2.1 |
| AUDIT / alaa-6dh.3.8 | `alaa-permission-generator/`, `alaa-partitioned-table-fk-audit/`, `alaa-mongodb-patterns/` | alaa-6dh.2.1, alaa-6dh.2.3, alaa-6dh.2.4 |
| SIGNALS / alaa-6dh.3.9 | `alaa-bale-provider/`, `alaa-sms-provider-mediana/`, `alaa-signoz-clickhouse-docs/`, `clickhouse-performance-schema-ops/` | alaa-6dh.3.1.1 (frozen decisions), alaa-6dh.2.1 |

The parent owns the three report files, plan/checkpoint, static intake evidence, task mutations and final Git integration. INTEGRATE owns root/index/doc updates only after all writers stop. Root checker edits require a named acceptance regression and parent assignment; do not widen a prose fix into generic tooling refactoring.

Known adjacent issue `alaa-ce4` is open/unassigned and concerns frontend delivery names in services-contract. It is not adopted here. Before SHARED writes, recheck ownership; preserve that issue's unrelated scope. Coordinate any true overlap rather than claiming its whole outcome.

## Ordered Work

### Phase 0 - Prepare the plan and registered hierarchy

- Status: complete
- Phase issue: alaa-6dh.1
- Review status: REVIEW_PENDING
- Review evidence: No independent review at this intermediate phase. Whole-engagement acceptance belongs to Phase 4 and artifacts/skill-pack-optimization-20261018/review-clearance.md; this historical phase retains REVIEW_PENDING.
- Depends on: none
- Reasoning and selection reason: A planning/authority boundary precedes implementation.
- Settled/open decisions and invariants: Mandatory policy and ratified decisions apply; decision subtasks resolve source gaps before dependent writes.
- Risk and required observers: Owner checks only; review is pending until Phase 4.
- Owned scope: Only this plan, checkpoint, immutable intake/routing/import artifacts and repo:skills Beads family.
- Excluded from this phase: Skill implementation, report removal, review, commits.
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-low-noise, alaa-code-intelligence-routing
- Work:
  - Task issue: alaa-6dh.1.1 [skills: inherit]
    - Subtask issue: alaa-6dh.1.1.1 [skills: alaa-workflow]
    - Subtask issue: alaa-6dh.1.1.2 [skills: alaa-workflow]
- Acceptance criteria: All 124 numbered proposals and auxiliary claims are routed exactly once; source-backed choices, ownership, tests, authority, dependencies and resume protocol are concrete. Planning validation and live Beads graph checks pass.
- Validation commands: python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20261018-000000_skill-pack-optimization.md; proposal-routing coverage and UTF-8/LF preservation check; scoped git diff --check; bd lint and live dependency/readiness readback.
- Evidence observed: Four read-only intake lanes completed; 124 numbered items mapped; live graph readback verified 57 issues, 56 hierarchy relations and 66 blocking edges. Workflow validator exit 0 (offline-Beads warning only); live graph readback, 124/124 coverage, 57-issue lint, UTF-8/LF and 13-file/index preservation checks passed. Planning only.
- Snapshot: HEAD 1a0799de71254427973f1253d80b846fea9acf10; SHA-256 34d5b14eca583fe997931e57e175d67dc97dfb5a98f38a6ac8182646f7375411; paths artifacts/skill-pack-optimization-20261018/*; deterministic sorted relative-path + NUL + raw bytes. Final full planning snapshot is recorded in the planning issue close reason.

### Phase 1 - Establish hierarchy, cadence and control owners

- Status: complete
- Phase issue: alaa-6dh.2
- Review status: REVIEW_PENDING
- Review evidence: No independent review at this intermediate phase. Whole-engagement acceptance belongs to Phase 4 and artifacts/skill-pack-optimization-20261018/review-clearance.md; this historical phase retains REVIEW_PENDING.
- Depends on: Phase 0; native leaf prerequisites remain in Beads
- Reasoning and selection reason: Consumers need stable hierarchy, cadence and ownership anchors before domain edits.
- Settled/open decisions and invariants: Mandatory policy and ratified decisions apply; decision subtasks resolve source gaps before dependent writes.
- Risk and required observers: Owner checks only; review is pending until Phase 4.
- Owned scope: WF, ORCH, CTRL and MEMDOC exclusive skill trees and their own templates/scripts/fixtures.
- Excluded from this phase: Domain changes, global/installed files, transcript recounts, independent review, commits.
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-low-noise, alaa-code-intelligence-routing
- Work:
  - Task issue: alaa-6dh.2.1 [skills: inherit]
    - Subtask issue: alaa-6dh.2.1.1 [skills: alaa-workflow, alaa-testing-strategy]
    - Subtask issue: alaa-6dh.2.1.2 [skills: alaa-workflow, alaa-testing-strategy]
  - Task issue: alaa-6dh.2.2 [skills: inherit]
    - Subtask issue: alaa-6dh.2.2.1 [skills: alaa-codex-orchestrator, alaa-cc-orchestrator]
    - Subtask issue: alaa-6dh.2.2.2 [skills: alaa-codex-orchestrator, alaa-cc-orchestrator]
  - Task issue: alaa-6dh.2.3 [skills: inherit]
    - Subtask issue: alaa-6dh.2.3.1 [skills: alaa-prompting-guide, alaa-low-noise, alaa-extract-agent-lessons, alaa-project-constitution, alaa-bash-shell]
    - Subtask issue: alaa-6dh.2.3.2 [skills: alaa-prompting-guide, alaa-low-noise, alaa-extract-agent-lessons, alaa-project-constitution, alaa-bash-shell]
  - Task issue: alaa-6dh.2.4 [skills: inherit]
    - Subtask issue: alaa-6dh.2.4.1 [skills: alaa-memory-os, alaa-codex-runtime-ops, alaa-repo-docs, alaa-code-intelligence-routing]
    - Subtask issue: alaa-6dh.2.4.2 [skills: alaa-memory-os, alaa-codex-runtime-ops, alaa-repo-docs, alaa-code-intelligence-routing]
- Acceptance criteria: The mandatory policy is executable through source contracts, templates, role projections and discriminating tests. Both runtimes agree. Existing local/completed families remain compatible. No review is introduced below the declared boundary.
- Validation commands: Bounded workflow unittest selections; python -B skills/sohrab/alaa-workflow/tests/test_workflow_files.py at task completion when applicable; affected orchestrator check_agent_contracts.py and changed-checker self-tests; check_fleet_references.py --skill for changed skills only. Defer combined acceptance to Phase 4.
- Evidence observed: All four task checks passed; WF task suite plus affected parser retest, ORCH contracts/selftests/render parity/pack checks, and scoped MEMDOC/CTRL checks are recorded by their task owners. User-directed Bash map restoration and routing-policy correction passed focused retests. New helper accepted this migrated plan. Current source manifests were read back. Canonical task results and proposal decisions are in their Beads issues, linked to artifacts/skill-pack-optimization-20261018/lanes/. Independent review remains pending.
- Snapshot: HEAD 1a0799de71254427973f1253d80b846fea9acf10; SHA-256 9eb44a507e0ae7edd428650252b08e568f657301b69eb0ee9fb4d5cfb09f13c8; paths enumerated in artifacts/skill-pack-optimization-20261018/phase1-snapshot.json. Implementation/test milestone only; REVIEW_PENDING.

### Phase 2 - Resolve domain proposals with rolling parallel writers

- Status: complete
- Phase issue: alaa-6dh.3
- Review status: REVIEW_PENDING
- Review evidence: No independent review at this intermediate phase. Whole-engagement acceptance belongs to Phase 4 and artifacts/skill-pack-optimization-20261018/review-clearance.md; this historical phase retains REVIEW_PENDING.
- Depends on: Phase 1; native leaf prerequisites remain in Beads
- Reasoning and selection reason: Domain decisions depend on Phase 1; owner decisions additionally unblock their actual consumers within this phase.
- Settled/open decisions and invariants: Mandatory policy and ratified decisions apply; decision subtasks resolve source gaps before dependent writes.
- Risk and required observers: Owner checks only; review is pending until Phase 4.
- Owned scope: SHARED, PHP, STORAGE, PLATFORM, GO, UI, PLAYER, AUDIT and SIGNALS exclusive trees.
- Excluded from this phase: Sibling-repository writes, invented platform values, vendor edits, blanket body-size cleanup, independent review and commits.
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-low-noise, alaa-code-intelligence-routing
- Work:
  - Task issue: alaa-6dh.3.1 [skills: inherit]
    - Subtask issue: alaa-6dh.3.1.1 [skills: alaa-services-contract, alaa-keyset-pagination, alaa-trust-gateway-auth, alaa-security-review, alaa-observability-soc, alaa-reliability-sla, vector-rust-observability-pipelines]
    - Subtask issue: alaa-6dh.3.1.2 [skills: alaa-services-contract, alaa-keyset-pagination, alaa-trust-gateway-auth, alaa-security-review, alaa-observability-soc, alaa-reliability-sla, vector-rust-observability-pipelines]
  - Task issue: alaa-6dh.3.2 [skills: inherit]
    - Subtask issue: alaa-6dh.3.2.1 [skills: alaa-php-clean-code, alaa-laravel-architecture, alaa-laravel-upgrade-all-packages, alaa-octane-performance, alaa-async-messaging, alaa-laravel-job-rabbitmq, alaa-laravel-public-api-contract-pack]
    - Subtask issue: alaa-6dh.3.2.2 [skills: alaa-php-clean-code, alaa-laravel-architecture, alaa-laravel-upgrade-all-packages, alaa-octane-performance, alaa-async-messaging, alaa-laravel-job-rabbitmq, alaa-laravel-public-api-contract-pack]
  - Task issue: alaa-6dh.3.3 [skills: inherit]
    - Subtask issue: alaa-6dh.3.3.1 [skills: alaa-minio-object-storage, alaa-arvan-object-storage, tusd-upload-platform]
    - Subtask issue: alaa-6dh.3.3.2 [skills: alaa-minio-object-storage, alaa-arvan-object-storage, tusd-upload-platform]
  - Task issue: alaa-6dh.3.4 [skills: inherit]
    - Subtask issue: alaa-6dh.3.4.1 [skills: caas-arvan-kuber, alaa-docker-production, alaa-haproxy, alaa-haproxy-lua, alaa-k8s-helm, alaa-gitlab-ci-cd, ansible-generator, ansible-validator]
    - Subtask issue: alaa-6dh.3.4.2 [skills: caas-arvan-kuber, alaa-docker-production, alaa-haproxy, alaa-haproxy-lua, alaa-k8s-helm, alaa-gitlab-ci-cd, ansible-generator, ansible-validator]
  - Task issue: alaa-6dh.3.5 [skills: inherit]
    - Subtask issue: alaa-6dh.3.5.1 [skills: alaa-golang, alaa-golang-clean-code-principles, alaa-go-chi-development, alaa-golang-fiber, alaa-data-layer, service-runtime-kit-governance]
    - Subtask issue: alaa-6dh.3.5.2 [skills: alaa-golang, alaa-golang-clean-code-principles, alaa-go-chi-development, alaa-golang-fiber, alaa-data-layer, service-runtime-kit-governance]
  - Task issue: alaa-6dh.3.6 [skills: inherit]
    - Subtask issue: alaa-6dh.3.6.1 [skills: alaa-frontend-developer, alaa-frontend-devops, alaa-vue-typescript-clean-code, alaa-quasar-app-vite-v3, alaa-ui-ux-design-system]
    - Subtask issue: alaa-6dh.3.6.2 [skills: alaa-frontend-developer, alaa-frontend-devops, alaa-vue-typescript-clean-code, alaa-quasar-app-vite-v3, alaa-ui-ux-design-system]
  - Task issue: alaa-6dh.3.7 [skills: inherit]
    - Subtask issue: alaa-6dh.3.7.1 [skills: alaa-shaka-player, alaa-indexeddb-browser-storage]
    - Subtask issue: alaa-6dh.3.7.2 [skills: alaa-shaka-player, alaa-indexeddb-browser-storage]
  - Task issue: alaa-6dh.3.8 [skills: inherit]
    - Subtask issue: alaa-6dh.3.8.1 [skills: alaa-permission-generator, alaa-partitioned-table-fk-audit, alaa-mongodb-patterns]
    - Subtask issue: alaa-6dh.3.8.2 [skills: alaa-permission-generator, alaa-partitioned-table-fk-audit, alaa-mongodb-patterns]
  - Task issue: alaa-6dh.3.9 [skills: inherit]
    - Subtask issue: alaa-6dh.3.9.1 [skills: alaa-bale-provider, alaa-sms-provider-mediana, alaa-signoz-clickhouse-docs, clickhouse-performance-schema-ops]
    - Subtask issue: alaa-6dh.3.9.2 [skills: alaa-bale-provider, alaa-sms-provider-mediana, alaa-signoz-clickhouse-docs, clickhouse-performance-schema-ops]
- Acceptance criteria: Every assigned report item has a grounded parent-ratified implemented/adapted or rejected disposition; unique requirements survive relocation; source, references and affected owner checks agree. No new skill is created merely from anecdotal frequency.
- Validation commands: Tiny selector/path/scenario checks per subtask; bounded task tests and check_fleet_references.py --skill per affected skill. Existing domain scripts run only for their changed covered surface. No full-pack command in each lane.
- Evidence observed: All nine domain tasks and their 18 subtasks closed after bounded checks and parent input-hash reconciliation. Phase epic alaa-6dh.3 is a tested milestone with REVIEW_PENDING, not reviewed acceptance. A1/A6 consumer obligations pass to Phase 3. STORAGE's local PyYAML absence was resolved by its supported cached immutable CI container without installation. Independent acceptance is unrun.
- Snapshot: HEAD 1a0799de71254427973f1253d80b846fea9acf10; SHA-256 eccc89f98bc127908c2d70071efa511b22b83014303f2f53eaae5d45b6b5cce6; paths enumerated in artifacts/skill-pack-optimization-20261018/phase2-snapshot.json (768 inputs).

### Phase 3 - Integrate coverage and finish documentation

- Status: complete
- Phase issue: alaa-6dh.4
- Review status: REVIEW_PENDING
- Review evidence: No independent review at this intermediate phase. Whole-engagement acceptance belongs to Phase 4 and artifacts/skill-pack-optimization-20261018/review-clearance.md; this historical phase retains REVIEW_PENDING.
- Depends on: Phase 2; native leaf prerequisites remain in Beads
- Reasoning and selection reason: All writers must stop before report exhaustion, cross-owner reconciliation and final candidate freeze.
- Settled/open decisions and invariants: Mandatory policy and ratified decisions apply; decision subtasks resolve source gaps before dependent writes.
- Risk and required observers: Owner checks only; review is pending until Phase 4.
- Owned scope: Parent-owned report removals, touched indexes, outputs/README.md when a new upgrade record is actually emitted, task artifacts, scoped consumer integration. A6 remaining convention-only consumers include alaa-postman-collections, alaa-algorithms-data-structures, alaa-system-design, the two cited runtime-ops call sites, frontend-developer reference 95 and Vue clean-code eval expectations that still require both forms. Domain writers completed PHP/Go/shared consumers. Do not perform a blanket call-site sweep.
- Excluded from this phase: Fresh unrelated refactors, independent review, commits and generated installed files.
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-low-noise, alaa-code-intelligence-routing
- Work:
  - Task issue: alaa-6dh.4.1 [skills: inherit]
    - Subtask issue: alaa-6dh.4.1.1 [skills: alaa-workflow, alaa-prompting-guide, alaa-repo-docs]
    - Subtask issue: alaa-6dh.4.1.2 [skills: alaa-workflow, alaa-prompting-guide, alaa-repo-docs]
- Acceptance criteria: Every proposal and auxiliary claim has one terminal disposition in its Beads owner; all accepted changes exist; three input files are present and exactly zero bytes. Task evidence is linked, metadata/indexes are current, all files are UTF-8 without BOM with LF, and the final candidate is frozen.
- Validation commands: Coverage/zero-byte/owner-scope assertions, changed reference/index checks where needed, scoped git diff --check; reuse unchanged evidence. Measure body footprint per changed skill without claiming runtime speed gains.
- Evidence observed: All 124 numbered outcomes and auxiliary/scaffold dispositions are resolved; three reports are zero bytes. Index and artifact checks passed after disclosed metadata repairs. All ten original unrelated file hashes and index entries are preserved. Exact results: artifacts/skill-pack-optimization-20261018/phase3-acceptance.md. No independent review occurred.
- Snapshot: HEAD 1a0799de71254427973f1253d80b846fea9acf10; SHA-256 ec745fd082cf3050b25b89dca7b2693cb3a3eb78c73804997c08448324309f90; paths enumerated in artifacts/skill-pack-optimization-20261018/phase3-candidate.json (2238 product/gate inputs).

### Phase 4 - Final review, fix, test and authorized commit

- Status: complete
- Phase issue: alaa-6dh.5
- Review status: APPROVED
- Review evidence: Single final boundary completed; artifacts/skill-pack-optimization-20261018/review-clearance.md and linked security/schema records. Earlier phase snapshots retain their historical tested-but-unreviewed meaning.
- Depends on: Phase 3; native leaf prerequisites remain in Beads
- Reasoning and selection reason: This is the only independent review and acceptance boundary for this engagement.
- Settled/open decisions and invariants: Mandatory policy and ratified decisions apply; decision subtasks resolve source gaps before dependent writes.
- Risk and required observers: Independent instruction and correctness review, triggered security review, persisted-schema compatibility review and independent verification. Schema version 3, hierarchy fields and helper CLI defaults are observable by saved-family consumers; the compatibility specialist checks version 2 and existing local families. No application UI, dependency, deployment topology or production data migration changed, so those specialist gates are not triggered merely by guidance mentioning them.
- Owned scope: Complete frozen scoped candidate, independent review evidence, focused repairs, consolidated verification, final curation and current-branch commit.
- Excluded from this phase: Push, merge, tag, release, installation, global settings, external memory publication and Dolt remote sync.
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-low-noise, alaa-code-intelligence-routing
- Work:
  - Task issue: alaa-6dh.5.1 [skills: inherit]
    - Subtask issue: alaa-6dh.5.1.1 [skills: alaa-workflow, alaa-codex-orchestrator, alaa-prompting-guide, alaa-testing-strategy]
    - Subtask issue: alaa-6dh.5.1.2 [skills: alaa-workflow, alaa-codex-orchestrator, alaa-prompting-guide, alaa-testing-strategy]
  - Task issue: alaa-6dh.5.2 [skills: inherit]
    - Subtask issue: alaa-6dh.5.2.1 [skills: alaa-workflow, alaa-extract-agent-lessons]
    - Subtask issue: alaa-6dh.5.2.2 [skills: alaa-workflow, alaa-extract-agent-lessons]
- Acceptance criteria: Final instruction/correctness and triggered specialist reviews accept the same candidate; all required checks pass after fixes; no tests/review weakened; evidence identifies exact inputs. Final curation resolved; three reports stay empty; accepted owned scope committed on current branch under the user's recorded authority while unrelated staged work is preserved.
- Validation commands: Cheap final review first; fix and affected retest; independent verifier runs the four root pack gates and uncovered owner gates once. Changed checker --self-test only where applicable. Validate workflow artifacts, bd lint, git diff --check, scoped digest/index preservation and actual commit readback.
- Evidence observed: Independent review approved the final candidate; final-verification-recheck.json records native PASS, repaired failures and exact unchanged-input reuse. The full workflow suite passed 130 tests; both orchestrators, container gates and constitution checks passed on unchanged inputs. Three source reports remain empty and all 124 outcomes are terminal. Ten original unrelated file hashes/index entries are preserved. The accepted scope is delivered by the authorized containing commit; actual hash and scope readback are recorded in Beads alaa-6dh.5.2.2.
- Snapshot: HEAD 1a0799de71254427973f1253d80b846fea9acf10; product SHA-256 24aa88d79f4e483bac8946d045b5e4486f1d2c5847027350d620abd70bc8b878; paths enumerated in artifacts/skill-pack-optimization-20261018/final-candidate.json (2238 inputs). Native result and current ownership verification: final-verification-recheck.json and final-verification-recheck-logs/owned-text-paths.txt.
- Final curation: Full engagement scanned after stable implementation, review, verification and documentation. No new admitted candidates. User choices on external topic maps and the bounded local-plan exception are already promoted to their canonical skill/workflow owners; do not duplicate them in memory. Runtime-pin checks, full-read sequencing, encoding and proof/reuse duties already have canonical owners; their observed violations stay in task evidence. Evidence-capture failures are one-off harness history, not new rules. No external memory note is written, no promotion remains, and no pipeline reopen is required. Two separately registered unclaimed investigation spikes (alaa-147 and alaa-x05) remain outside this acceptance.


## Task Allocation

The runtime orchestrator owns allocation; workflow records it. The root session's actual controls are not observable. Its advisory plan was supplied by a separately allocated planner; the parent ratifies this plan. All dispatch rows below use explicit model and reasoning_effort with fork_turns=none. Verify BOTH effective model and effort against neutral installed definitions before dispatch; role availability is currently exposed, future availability is rechecked, serving identity remains unknown. Future allocations below are provisional until the ready leaf's remaining decisions are checked; material changes reassess only affected remaining work. Role title and risk alone select no model.

Official evidence was refreshed on 2026-10-18: [model-selection guidance](https://developers.openai.com/api/docs/guides/model-selection) and [subagent control precedence](https://learn.chatgpt.com/docs/agent-configuration/subagents). The former supports economical scoped work and revisable technical work; local per-task effort decisions are not calibration claims. The active host exposes the pairs below. No runtime performance, worker-quality or serving-identity claim follows.

| Task/scope/complexity | Role authority | Priority/reason | Model | Effort | Selection/admission evidence and source date | Invocation/requested/effective controls | Availability/limits |
|---|---|---|---|---|---|---|---|
| PLAN: Ground proposals and publish the execution plan | alaa-planner-high | balanced; user priority for cadence | gpt-6.1-sol | high | Coupled hierarchy, cross-owner scope and deferred acceptance; medium leaves interacting planning decisions. 2026-10-18 source; role-neutral | Explicit pair; verify at dispatch | Exposed; recheck at dispatch |
| WF: Implement workflow hierarchy and test doctrine | alaa-implementer-high | balanced; user priority for cadence | gpt-6.1-sol | high | Schema, compatibility, closure and proof interact; decomposition cannot settle cross-boundary decisions in advance. 2026-10-18 source; role-neutral | Explicit pair; verify at dispatch | Exposed; recheck at dispatch |
| ORCH: Mirror cadence and phase-end commit scheduling | alaa-implementer-high | balanced; user priority for cadence | gpt-6.1-sol | high | Mirrored scheduling, role authority and generated contracts need coupled reasoning. 2026-10-18 source; role-neutral | Explicit pair; verify at dispatch | Exposed; recheck at dispatch |
| CTRL: Unify prompt, noise, lesson and constitution control owners | alaa-implementer | balanced; user priority for cadence | gpt-6.1-sol | medium | Several existing instruction owners; cross-owner decisions exceed bounded Luna admission. 2026-10-18 source; role-neutral | Explicit pair; verify at dispatch | Exposed; recheck at dispatch |
| MEMDOC: Repair memory, runtime recovery and documentation boundaries | alaa-implementer | balanced; user priority for cadence | gpt-6.1-sol | medium | Adapter/authority/documentation boundaries require semantic reconciliation. 2026-10-18 source; role-neutral | Explicit pair; verify at dispatch | Exposed; recheck at dispatch |
| SHARED: Resolve shared contract, trust, security and telemetry owners | alaa-implementer-high | balanced; user priority for cadence | gpt-6.1-sol | high | Auth, registry and requirement ownership interact; no stronger frontier pair is justified. 2026-10-18 source; role-neutral | Explicit pair; verify at dispatch | Exposed; recheck at dispatch |
| PHP: Repair PHP, Laravel, messaging and contract-pack ownership | alaa-implementer | balanced; user priority for cadence | gpt-6.1-sol | medium | Upgrade transactions and runtime/queue boundaries are not mechanical. 2026-10-18 source; role-neutral | Explicit pair; verify at dispatch | Exposed; recheck at dispatch |
| STORAGE: Resolve storage and tusd contract differences | alaa-implementer-high | balanced; user priority for cadence | gpt-6.1-sol | high | Hook revocation semantics, failure behavior and separate storage control planes remain coupled. 2026-10-18 source; role-neutral | Explicit pair; verify at dispatch | Exposed; recheck at dispatch |
| PLATFORM: Align platform, container, proxy, CI and Ansible policies | alaa-implementer | balanced; user priority for cadence | gpt-6.1-sol | medium | Platform/resource constraints and validator ownership require ordinary semantic judgment. 2026-10-18 source; role-neutral | Explicit pair; verify at dispatch | Exposed; recheck at dispatch |
| GO: Unify Go testing, lifecycle and data/runtime-kit boundaries | alaa-implementer | balanced; user priority for cadence | gpt-6.1-sol | medium | Runtime lifecycle, imports, phase gates and unique propagation requirements need reconciliation. 2026-10-18 source; role-neutral | Explicit pair; verify at dispatch | Exposed; recheck at dispatch |
| UI: Consolidate frontend security, QA and observability | alaa-implementer | balanced; user priority for cadence | gpt-6.1-sol | medium | SW/security/SSR and measurement-scope changes cross existing owners. 2026-10-18 source; role-neutral | Explicit pair; verify at dispatch | Exposed; recheck at dispatch |
| PLAYER: Align player and browser-storage boundaries | alaa-implementer-low | balanced; user priority for cadence | gpt-6-luna | medium | After storage/UI decisions freeze: finite known boundary/API-check edits, preserved checked API set, scoped checker oracle. 2026-10-18 source; role-neutral | Explicit pair; verify at dispatch | Exposed; recheck at dispatch |
| AUDIT: Clarify permission, FK-audit and MongoDB scope | alaa-implementer-low | balanced; user priority for cadence | gpt-6-luna | medium | Bounded authority/count/date edits with named files and explicit before/after scenarios; no new audit algorithm. 2026-10-18 source; role-neutral | Explicit pair; verify at dispatch | Exposed; recheck at dispatch |
| SIGNALS: Consolidate provider and ClickHouse signal rules | alaa-implementer-low | balanced; user priority for cadence | gpt-6-luna | medium | After shared decisions freeze: local pointer/wording edits retain vendor ambiguity and project_id behavior; exact reference oracle. 2026-10-18 source; role-neutral | Explicit pair; verify at dispatch | Exposed; recheck at dispatch |
| INTEGRATE: A1/A6 remaining consumer clauses and pack routing indexes | alaa-implementer-low | balanced; user priority for cadence | gpt-6-luna | medium | Reallocated from documenter because these clauses control agents. Seven named files, settled central call-form and narrow Arvan trigger, bounded wording discretion, exact links/JSON/scope checks. Two independent UI consumers use their existing owner and full-read provenance. Parent alone resolves report coverage. 2026-10-18 source; role-neutral | Explicit pair; neutral installed definition verified | Exposed; serving identity unknown |
| ACCEPT: Run the single final review and verification cycle | alaa-reviewer | balanced; user priority for cadence | gpt-6.1-sol | high | Whole changed executable surface and hierarchy interactions; separate instruction reviewer for controlling prose. 2026-10-18 source; role-neutral | Explicit pair; verify at dispatch | Exposed; recheck at dispatch |
| DELIVER: Curate and commit the accepted scoped candidate | alaa-documenter | balanced; user priority for cadence | gpt-6-luna | medium | Bounded final evidence/curation report; parent alone executes authorized Git effect. 2026-10-18 source; role-neutral | Explicit pair; verify at dispatch | Exposed; recheck at dispatch |
| Three completed input-mapping lanes | alaa-explorer | balanced; independent sources | gpt-6.1-sol | medium | Cross-owner fact verification; unsettled contracts reject bounded Luna route | Explicit controls with fork_turns=none; installed roles unpinned | All returned; observed serving identity unknown |
| Completed cadence advisory lane | alaa-planner-high | mandatory policy first | gpt-6.1-sol | high | Coupled hierarchy, compatibility, closure and generator planning | Explicit controls with fork_turns=none; installed role unpinned | Returned; observed serving identity unknown |
| Final instruction review | alaa-instruction-reviewer | independent authority | gpt-6.1-sol | high | Complete cross-owner behavioral contract; defer until Phase 4 | Explicit controls; fresh context; verify BOTH effective model and effort | Dispatched; findings/verdicts in review evidence |
| Final security review, only if authority/trust rules changed | alaa-security-reviewer | actual changed trust/approval boundary | gpt-6.1-sol | medium | Bounded changed-boundary audit with settled policy | Explicit controls; fresh context | Dispatched; findings/verdicts in review evidence |
| Final workflow persisted-format compatibility | alaa-api-contract-reviewer | actual schema 2/3 and helper CLI transition | gpt-6.1-sol | medium | Existing-family compatibility spans initializer, validator, templates and generators; open transition questions fail bounded Luna suitability. No broader public API audit | Explicit controls; fresh context; neutral role required | Dispatched; findings/verdicts in review evidence |
| Final integrated verification | alaa-verifier | bounded command execution | gpt-6-luna | medium | Exact selectors and outcome classification; no design decision | Explicit controls; low resource priority; no fixes | Ready after final documenter freeze |
| Evidence gap in upstream/another repository | alaa-researcher | unblock named source fact | gpt-6.1-sol | medium | Conflicting current sources require fact judgment; no implementation | Explicit controls; bounded query/return | Conditional, not dispatched |

For PLAYER/AUDIT/SIGNALS, Luna admission requires settled upstream decisions, finite named files, bounded semantic discretion and the listed cheap discriminating checks. Reject that allocation if any predicate fails; retrieve the missing fact or reallocate the remaining leaf. Medium is the local balanced choice for these repetitive instruction edits and verdict bookkeeping, not a claim of better calibration than other supported efforts.

## Delegation and resource scheduling

- Observed capacity on 2026-10-18 is five agents including the parent: use all four child slots whenever four genuinely independent ready lanes exist. Re-read live capacity on resume; this is not a universal runtime limit.
- Schedule from native Beads readiness plus phase, authority, file and shared-resource barriers. Do not reserve an idle reviewer during implementation or create agents just to fill slots. Release/reuse completed slots; no nested fan-out that bypasses capacity.
- Phase 1 initially admits WF and MEMDOC. ORCH and CTRL join once WF's decision subtask freezes anchors; WF's executable work can continue in its own tree. Serialize projection generation after its source contracts stop changing.
- SHARED decision intake depends on closed WF/CTRL/MEMDOC decision leaves; its implementation also depends on their completed tasks. The native ancestor Phase 1 barrier still gates Phase 2 readiness. Do not dispatch a leaf that native readiness keeps blocked, even when its direct prerequisites are closed.
- Phase 2 initially favors SHARED, PHP, STORAGE and PLATFORM. As their decision subtasks finish, admit the actually unblocked GO/UI/PLAYER/SIGNALS lanes; AUDIT fills an independent slot. Keep shared contract decisions together and consumer writes disjoint.
- The parent's integration edits never overlap an active owner's files. Separate generator processes and full suites from writers on their inputs. Run at most one expensive combined gate at a time; no duplicated broad suite per lane.
- Before every dispatch, claim the ready leaf and verify actual source/installed role availability, pins, sandbox/MCP limits, and BOTH effective model and effort. Unobservable serving identity remains unknown; a read-only role is not proof of sandbox enforcement.
- Dispatch carries goal, owned files, exclusions, exact acceptance issue, source references, resolved skill bindings, decision dependencies, validation tier and compact return shape. Tell every writer it is not alone and must preserve others' changes.
- Each return carries item IDs/decisions, changed paths, command/result/snapshot, unresolved source facts and next action. The leaf's notes/comments are its interruption/progress record; no separate lane plan or checkpoint.
- Independent review is dispatched only in Phase 4. Reviewers never fix. Findings return verbatim to the owning implementation lane; accepted fixes get affected retests and final clearance within that same review stage.

## Cross-owner integration contracts

- A6: PHP, GO and SHARED own their cited convention sentences. Phase 3 owns remaining Postman, algorithms, system-design and two runtime-ops consumers. Parent additionally ratifies the exact contradictory both-form instructions in frontend-developer references/95-sources-and-maintenance.md and Vue clean-code evals/evals.json; the existing UI writer owns only those two consumers under alaa-6dh.4.1.1. Keep the original A6 report item until all named consumers reconcile; never sweep untouched legacy call sites.
- A1: PLATFORM owns Docker/HAProxy routing; Phase 3 owns `skills/sohrab/README.md` and its existing `README.fa.md` routing mirror. These are pack indexes, not repository-root READMEs. A41/C2: SHARED security owns the discriminator/container posture; PLATFORM owns Docker/HAProxy/Kubernetes consumers.
- A21/N2: SHARED observability reference 20 Browser client signals and reference 60 Sentry authority split feed UI/Quasar wiring; services reference 21 owns only verified shared config facts. No invented browser names or universal SDK privacy option.
- B19: SHARED observability reference 20 Cache signals feeds GO/Fiber. B21/A42/C1: observability reference 80 Permitted phone derivative feeds SIGNALS providers; default omission/reference and approved country-code-only redaction preserve subscriber secrecy.
- User-directed router policy applies to later lanes. STORAGE owns its legacy numeric router-validator alignment with focused accepted/rejected fixtures, preserving path and single-router checks. Other legacy policy checkers are reconciled in Phase 3 only if current evidence identifies them.

## Validation design and evidence economy

Preserve behavior while reducing instruction cost. Each changed rule needs the relevant trigger, exception, authority, source date, stop/failure path and unique capability preserved unless the mandatory user change explicitly replaces it. Owner relocation is a separate semantic change; draft first, compress second, and use counterexamples rather than word count as correctness proof.

Required hierarchy/cadence fixtures in WF/ORCH: valid three-level family; missing/duplicate/orphan nodes; parent versus prerequisite; incompatible/legacy family handling; unresolved executing mappings; exact checkpoint cursor; no task/subtask review or commit; permitted final-only override; unauthorized/premature commit rejected; failed test cannot be weakened; covered aggregate reuse; Markdown-input change invalidation; correctly identified whole-engagement final candidate.

Task command owners:
- WF: scoped cases from `skills/sohrab/alaa-workflow/tests/test_workflow_files.py`; helper/validator cases and existing compatibility fixtures. Use the task-end suite once when all changes warrant it.
- ORCH: each affected `scripts/check_agent_contracts.py`; regenerate through each `scripts/render_agents.py --write` only after source freeze, then validate parity. Run self-tests after checker/renderer logic changes.
- CTRL: prompting-guide policy/projection/allocation checks only when their covered inputs change. A neutral source registration edit is not proof of installed activation.
- Every changed skill: `python -B scripts/check_fleet_references.py --skill <exact-name>` with repeated `--skill` as needed. Other owner-native checks are selected after inspecting their supported invocation; absence is not a pass.
- Final verifier: `python -B scripts/validate_sohrab_skill_pack.py`; `python -B scripts/check_skill_index.py`; `python -B scripts/check_fleet_references.py`; `python -B scripts/check_lifecycle_contract.py`. Run these once on the complete candidate; aggregate coverage discharges identical already-covered commands.
- Final planning/artifact check: `python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20261018-000000_skill-pack-optimization.md`; `git diff --check` scoped to agent-owned paths; zero-byte, proposal-disposition, encoding, scope and untouched-baseline assertions.

Do not run product suites merely to validate this planning turn. Source/static checks do not prove live agent compliance, installed skill activation, development-time savings or cost reduction. Record footprint and actual observed commands separately from unrun runtime claims.

Final verification allocation (after the single review/fix stage and final documentation):
- Parent confirmed final-documenter admission at gpt-6-luna/medium: isolated evidence note and grounded documentation eligibility; no product decisions. Configured role is neutral; serving identity unknown.
- Workflow CLI tests hit Windows sandbox temp-directory denial before product execution; exact escalated focused retry passed without product/environment changes. Run the final low-priority workflow command with exact scoped escalation from the start; Docker likewise uses scoped escalation based on recorded named-pipe denial. No ACL/global setup change or installation.
- Independent verifier runs the four root gates above, the workflow's full suite on the final source (117 cases before final repairs; report the observed final count), and the active plan validator. The later optional-root repair means the earlier full suite is historical; its 12 affected cases passed, but final independent source acceptance is still owed.
- For each orchestrator, run `scripts/check_agent_contracts.py` and its `--self-test`, then `scripts/validate_pack.py` from that skill's directory. The aggregate already checks generated drift and grants; do not also repeat renderer/grant normal commands. Normal contract checks remain separate because the aggregate does not call every planning/verification/economy assertion. Run the CC pack's supported `--self-test` for changed aggregate logic; Codex pack exposes no such flag.
- Run the changed tusd pack validator and its `--self-test` in the previously verified cached immutable CI image identified in STORAGE-checks.json. Use no pull/network, read-only repository/rootfs, one CPU, 128 MiB, and a bounded writable temporary filesystem for fixtures. Do not install PyYAML or substitute a parser. This supplies independent observer and full changed-checker proof; retain the earlier six router-fixture result as focused feedback.
- Run the exact constitution template validator and AUDIT-cli-assertion.py replay. Other unchanged domain runtime/configuration checks have no changed covered implementation inputs; their scope exclusions remain in the lane evidence.
- Run the existing Markdown checker on exact changed product Markdown and final narrative documentation; measure eligible documentation through its line-budget mode. Plans, checkpoints and decision/evidence records are named exemptions, not narrative splits. Run scoped `git diff --check`, encoding, zero-byte, coverage, candidate-hash and original-index assertions.
- One CPU-heavy invocation at a time; Windows uses the existing BelowNormal runner with two CPUs and a 300-second timeout for the workflow suite. Lightweight static commands remain bounded and sequential per gate. Freeze product writes throughout verification. Every failure retains its exact command and reason; corrections go to an implementer, never the verifier.

Before a gate, freeze its scope and record HEAD, command, flags/environment, required observer and SHA-256 of a deterministic sorted manifest `relative-path + NUL + file-bytes`. Include untracked inputs. Reuse evidence only while its covered inputs and authority remain valid. Snapshot records are evidence, not task status.

Final review repair allocation: `wf_final_fix` and `orch_final_fix` use neutral `alaa-implementer-high`, requested gpt-6.1-sol/high, fresh context. WF owns C1-C3/I2; ORCH owns I1; parent owns C4. Accepted findings, allocation reasoning, limits and frozen source are recorded in `artifacts/skill-pack-optimization-20261018/review-findings.md` and Beads `alaa-6dh.5.1.1`. Serving identity is unknown; no observed mismatch. These are repairs within the single final review stage.

Second final repair allocation: `design_final_fix`, neutral `alaa-implementer`, requested gpt-6.1-sol/medium, owns only the remaining I1 system-design seam. Exact finding and bounded semantic admission are recorded in `review-findings.md`; no other source scope is reopened.

Final verification repair allocation: original `citation_final_fix` stopped before edits because its installed compatibility role has an incompatible Astra/xhigh pin. Reallocated remaining identical mechanical work to `citation_repair`, verified neutral `alaa-implementer-low`, requested gpt-6-luna/medium; role identity changes no authority/admission. No installed/global definition is modified. Gate 1 reproduced a missing local reference in Bale; the existing target is alaa-observability-soc references/70-soc-evidence.md. Exact source qualification in Bale and the matching Mediana paragraph is mechanical, finite and behavior-preserving. Full owning skill reads precede edits. Only two SKILL.md files and lane evidence are writable; no gate or policy change. Final verifier retains passing unaffected inputs; rerun affected native gates and previously uncaptured gates 17/20 after this repair and refreshed documentation.

## Context, checkpoint and resume

Use the workflow resume protocol: bound issue, plan, handoff package, checkpoint, then the exact remaining sources. Verify branch, dirty tree, source availability, active claims and surviving lane writes before acting. Read `bd where` first; use current prime context or refresh it when stale.

Checkpoint after a meaningful decision, completed task, observed validation, blocker, phase boundary, or impending handoff. Keep current phase/task/subtask, last command/result, pending final review/commit, next safe action and touched surfaces in the checkpoint. Put expensive findings and ruled-out approaches in this plan's handoff package; task evidence remains in its issue. No timed checkpoint churn.

A cold-start reader must be able to identify the next ready leaf, satisfied prerequisites, allowed paths, evidence to reuse, unresolved facts and exact next command without rereading every completed report. After compaction, reconcile actual owners rather than trusting a summary. Unknown or interrupted mutations are read back before retry.

## Handoff Package

- Confirmed facts (verified, each with how it was verified): The three live reports contain 124 numbered proposals, archived with raw content and hashes in intake-snapshot.json. Four read-only lanes read the reports and checked cited owner passages; they performed no product edits or tests. Beads `bd where` matched AGENTS.md; 57 created issues have repo:skills, 56 parent-child relations and 66 blocking edges were read back. The predecessor alaa-kzj is closed. Existing dirty/staged files and index identities were captured before writes. Current branch/HEAD are in the header.
- Open assumptions (believed but unverified, each with what would verify it): No unresolved source assumption blocks the accepted scope; proposal-dispositions.json records the final source decisions. External application behavior, installed activation, serving identity and runtime speed/cost gains remain unproven. The two out-of-scope investigation spikes preserve their uncertainty without claiming a defect or fix.
- Ruled out (approach, reason, evidence): Recounting chats is explicitly excluded. No new skill is justified by file 03 alone; extend existing owners where a verified gap remains. No blanket body-size cleanup, global language/hook fix, deploy gate mutation, replacement database, local fallback task store, per-subtask/task review, interim commit or unsupported safety-gate weakening. The completed predecessor family is evidence, not an active family to rewrite.
- Read first on resume (ordered exact paths): This plan after the active issue; `docs/agents/20261018-000000_skill-pack-optimization-state.md`; `artifacts/skill-pack-optimization-20261018/proposal-routing.json`; the active proposal text in intake-snapshot.json or its still-present report; the exact owning skill and references for that leaf.
- Environment notes (command shapes that work here, and ones that look right but fail): PowerShell/native Python reads and planning writes work. A sandboxed Beads search warned that the hub gate lock was access-denied; the same scoped command outside sandbox succeeded. Subsequent hub reads/writes used exact-command escalation. No ACL/global configuration changed. Use one bd invocation per command and native bulk dependency import; never per-command BEADS_DIR overrides. A large raw bd show was truncated; compact field projection returned verifiable IDs/labels/edges. A long shell write failed before execution with WinError 206; the bounded apply_patch path succeeded, followed by explicit LF normalization. Hindsight recall is not exposed; canonical-source planning proceeded without it.
- Traps (looks correct, is not): The prior checkpoint's next action is stale although its parent issues are closed; do not reopen or repeat that work. `bd where` proves routing only. Static artifact validation proves neither live readiness nor hierarchical runtime compliance. Documentation can invalidate tests. Task closure is not phase review. A lower warning count is not performance proof. Existing staged verification/old-plan files must not be swept into the final commit.

## Historical planning evidence

- Intake analysis and allocation: four completed agents, three `alaa-explorer` at requested gpt-6.1-sol/medium and one `alaa-planner-high` at requested gpt-6.1-sol/high. Configured roles were unpinned; serving controls unobservable. No independent reviewer was dispatched.
- Planning validation: workflow validator exited 0 with the expected offline-Beads warning; live issue/edge checks separately passed. Coverage is 124/124, all mapped sources exist, Beads lint passed for 57 issues, and all 13 pre-existing files plus the staged index are unchanged. The first encoding assertion found CRLF; only the five owned planning artifacts were normalized and the same assertion then passed. No product test or independent review ran at the planning boundary.
- Curation at planning boundary: the user's hierarchy/cadence decision is retained here as the authorized target contract; no separate durable memory note is needed or authorized. Source-owned facts stay with their owners.
- Product lifecycle at this handoff: IMPLEMENTED in progress (Phase 1 source contract frozen; remaining execution incomplete); MERGE_CANDIDATE not proven (final review/gates unrun); RELEASE_CANDIDATE not requested; PUBLISHED not requested.
- Commit/push/sync: no planning commit; execution commit remains conditional on final acceptance; push and remote sync not authorized.

## Final lifecycle and delivery

- IMPLEMENTED: proven by focused and native evidence on the identified final candidate.
- MERGE_CANDIDATE: proven by independent final review, resolved repairs and required native checks; see final-verification-recheck.json.
- RELEASE_CANDIDATE: not requested.
- PUBLISHED: not requested.
- Commit: authorized scoped containing commit on main; actual SHA, scope and preservation readback belong to Beads alaa-6dh.5.2.2. No push, tag, merge, installation or Dolt remote sync.
- Process limits: documented read-order violations and failed harness/capture attempts were not treated as passing proof. Independent native checks establish the final source result. Installed activation, application runtime behavior, serving identity and performance remain unproven.

## Execution Position

- Position owner: `docs/agents/20261018-000000_skill-pack-optimization-state.md`.
