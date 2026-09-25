# Skill modernization audit — Stage A evidence

Audit date: 2026-09-25. Status: recommendations awaiting explicit selection. This is audit evidence, not an implementation plan or execution authorization.

## Baseline and coverage

Repository HEAD at intake: `4fdd8b709a745314a0575c25c06d0a390847bde6`; existing branch `codex/gpt6-agent-migration`. No branch was created. Existing staged and unstaged Claude migration changes were preserved. See `baseline-status.txt`, `baseline-head.txt`, and `source-manifest.json`.

Concurrent-state warning: the final hash comparison found six prompting-guide Claude policy/evaluation/checker files changed after audit intake, and tracked status also changed. This audit and its research lanes did not write those files. Their external writer is not established here. `source-integrity-final.json` names the six files; 1,495 inventory files retained their intake hashes. The Claude checkpoint still says in_progress/Phase3. Therefore affected policy/pack gate results below are observations of the versions read when commands ran, NOT certification of the final combined tree. No migration repair or repeated check was attempted while the source was moving. Freeze and finish W0 before dependent implementation planning is finalized.

The inventory contains 69 first-party skills and 1,501 files: 726 files under references, 265 under scripts (including fixtures), and 114 under agents. These are path counts, not counts of executable scripts or active roles. `inventory.json` enumerates each skill and its textual cross-skill dependencies; `source-manifest.json` enumerates every included file with hash and size. Textual edges are routing leads, not a proven runtime call graph.

All 69 bodies received substantive triage, with selected references, metadata and scripts inspected. This is NOT an exhaustive 1,501-file semantic audit, nor a test of every command or API. The per-skill matrix explicitly retains Not assessed for insufficient coverage. A clean structural check is not a domain correctness verdict. A dated historical snapshot is not inherently wrong; refresh is justified where current guidance or compatibility decisions depend on it.

Final matrix coverage: 1 None (inspected static algorithm guidance), 22 Minor recommendations, 1 Fundamental recommendation, and 45 Not assessed. Priorities independently total 2 P0, 16 P1, 8 P2 and 43 Defer. Some Not assessed rows are P1 because missing provider evidence matters; they are research dependencies, not approved implementation. `per-skill.csv` and `per-skill.json` contain all requested fields including independent A/B/C, dependencies, risk, benefit, validation, confidence and sources. `per-skill.md` is the compact reading view. `versions.md` separates verified stable releases, previews and unresolved exact versions.

Excluded from first-party modernization: 39 direct curated skill entries, five direct system skill entries, seven registered vendor subtrees, archived files, generated outputs as independent edit owners, installed user-home copies, and consumers outside this checkout. Counts for third-party entries use direct `*/SKILL.md` discovery only. Vendor registry: `vendor/subtrees.json`. Root generated README/install blocks belong to that registry; reviewer wrappers and manifests belong to their renderers; workflow artifacts belong to alaa-workflow. No vendor or generated file is proposed for manual editing.

Installed distinction: the inspected prompting-guide, workflow and both orchestrator skill paths are symlinks to repository sources. All 23 installed Codex role TOMLs equal transport-neutral source templates and contain no active `mcp_servers` sections. The installed version sentinel is 3.6.0 while source is 4.0.0. This is inconsistent installation evidence, not proof of effective isolation or a successful supported installation. Effective MCP enforcement and serving identity remain unknown. Read-only researchers stayed within their role restrictions; no MCP mutation was used.

Hindsight tools were unavailable; recall failed open to current repository evidence. The lightweight memory registry search found no relevant entry. No memory was written.

## Migration dependency

GPT: `docs/agents/20260925-120000_gpt6-agent-migration-state.md` records source migration complete. Its prior verification covers 201 frozen files, 16 source gates, 45 workflow tests, installer negative cases, and independent review. Forty-three files now differ from that historical snapshot, principally in shared/Claude migration surfaces; see `gpt-migration-snapshot-drift.json`. Historical all-green evidence cannot certify the changed combined tree. Current explicit Codex policy validation covers 24 pins, renderer check covers three generated files, and pack validation covers 23 roles, all exit 0. Calibration and installed activation remain unproven. Preserve the migration; do not redo it.

Claude: current checkpoint `docs/agents/20260925-110010_claude-model-migration-state.md` says in_progress, Phase 3. Independent integrated verification/review and final reconciliation remain pending in the recorded workflow. Current policy check passes 23 projections and pack check passes 22 roles, but this audit does not replace the migration's independent completion gates. Treat recommendations touching prompting-guide, shared policy or Claude agent surfaces as provisional until that workflow closes or supplies current final evidence. Do not overwrite its plan or changes.

Observed command-line versions: Codex CLI 0.147.0; Claude Code 2.1.282. The Codex version command returned exit 0 with temp cleanup/PATH alias permission warnings; no repair was attempted. These CLI observations do not establish the desktop app version, its backend, account eligibility, serving model or effective configuration.

## Prioritized findings

| ID | Size / priority | Evidence and decision |
|---|---|---|
| F01 | Minor / P0 | `caas-arvan-kuber/SKILL.md:76` invokes `python3 alaa-k8s-helm scripts/check_manifests.py ...`; Python interprets the directory-like first token as its script. Resolve the owning skill root and name its actual checker file. Preserve `--profile arvan`, exit-code semantics and live-cluster proof. P0 is broken execution, not a demonstrated production outage. |
| F02 | Minor / P0 | `service-runtime-kit-governance/SKILL.md:55` says to commit regenerated outputs unconditionally. Add the explicit authorization boundary. Higher-level instructions still prohibit unauthorized commits; none was observed. P0 denotes the blocking instruction contradiction. Preserve generator ownership and secret checks. |
| F03 | Fundamental / P1 | `alaa-reliability-sla/SKILL.md` blanket queue expiry language and `references/40-admission-and-shedding.md:9-14` durable receipt semantics conflict in scope. Separate synchronous waiting deadlines from durable job validity/retention. Potential lost-work impact is an inference; no consumer failure was observed. Shared public behavior changes require architecture, async-contract and test review. |
| F04 | Minor / P1 | `alaa-permission-generator/SKILL.md:30-34` describes a machine-specific source_root as universal. Preserve catalog authority and missing-checkout hard stops, but derive the configured root from the actual catalog instead of committing a machine path. Do not change the external catalog or invent permission maps. |
| F05 | Minor / P1 | `alaa-memory-os/references/store-hindsight.md:7` has older core/agent-package snapshots; global memory routing says local while source selects hindsight. Refresh source compatibility guidance only if selected. Global reconciliation and installed upgrade are separate, excluded effects. |
| F06 | Minor / P1, provisional | Both orchestrators prescribe universal one-command/watchdog narration (`SKILL.md:62` Codex, `:74` Claude), while low-noise routes cadence to the active host. Move runtime facts to prompting-guide and retain task-appropriate bounded calls, observability and recovery. Preserve independent gates and mirrored behavior. Do not claim fewer calls or tokens until evaluated. |
| F07 | Minor / P2 | Routing layout conflicts with the one-router contract in code-intelligence-routing (nine refs, missing map), reliability-sla and services-contract (map plus body routers). Consolidate only after preserving every trigger and exception. |
| F08 | Not assessed / P1 evidence dependency | Bale wire facts, Mediana provenance and Arvan object-storage capabilities contain explicit unknowns. Obtain provider evidence before proposing normative API changes. Missing evidence is not proof that the current contract is false, and does not alone justify a fundamental rewrite. |
| F09 | Minor / P1 or P2 by row | Version-aware ledger refresh for Go/data/RabbitMQ, Kubernetes/Helm, SigNoz, Vector, GitLab, HAProxy, Quasar and Shaka. Retain supported consumer ranges and current lockfile authority. Latest upstream is not an approved upgrade target. |
| F10 | Separate installed-surface proposal / P1 | Reconcile source/installed role sentinel and materialized grants. Installation requires separate named-target permission; this audit grants none. Current role pins matching source do not prove grants were materialized or that running agents activated them. |
| F11 | Minor / P1 | `alaa-input-normalization/references/10-normalization-contract.md:70-73,112-114` promises code-point length preservation despite NFC; the corpus includes two-code-point to one-code-point composition. Express the invariant relative to NFC(input). `references/30-backend-middleware-binding.md:44-65` also calls undefined `fieldName`; the official Laravel13 parent class supplies none. Complete the example. Preserve NFC, Nd folding, mode split, corpus and four-runtime proof. |
| F12 | Minor / P2, root documentation companion | `install-skills.md:234` says Codex has no plugin, while current official Codex documentation includes plugins. Remove that obsolete rationale without changing the supported local role installation path or granting installation authority. This root companion is separate from the 69 skill rows. |

## Recommended selectable waves

These are recommendation groups, not a saved execution plan. Dependencies and exact ownership would be planned only after selection.

| Wave | Scope | Dependency / risk | Acceptance direction |
|---|---|---|---|
| W0 | Close or obtain current Claude migration evidence; preserve GPT migration and separate activation/calibration evidence | External to this modernization implementation scope; blocks only affected shared-model/Claude changes | Existing workflow's independent gates and frozen source identity; no rerun or overwrite of migration |
| W1 | F01, F02, F04, F11: Arvan command, runtime-kit commit boundary, permission-catalog portability, input-normalization prose/example | Small source edits; no external catalog, cluster or Git effects | Negative command-path fixture, approval/no-approval instruction scenarios, configured-root/missing-root cases, Unicode composition and complete Laravel middleware examples; required native gates |
| W2 | F03: reliability queue semantics, with services-contract and async-messaging consistency | Fundamental; dependent contracts serialize; consumer impact must be investigated before normative change | Waiting/recoverable, accepted durable, expired-validity and redelivery scenarios; preserved receipt guarantee; independent contract/security/reliability judgment |
| W3 | F05, F06, F07, F12: shared ownership/routing, host-aware runtime guidance, installation-document rationale | F06 waits for W0; paired orchestrators change together; installed/global repair excluded | Trigger reachability, authority and exception equivalence; source validators; installed proof and quality evaluation explicitly separate |
| W4 | F09: compatibility ledger refresh, selected dependency groups only | Consumer versions frequently unknown; no implicit major upgrade | Dated official stable/preview ledger, target lock/runtime evidence before changing supported ranges, exact-binary/schema checks where required |
| W5 | F08 and remaining Not assessed rows: evidence completion | Research-only until gaps close; unavailable providers block their own claims only | Primary provider contract, complete selected references/scripts review, consumer proof, then classify change size |

Recommended first selection: W1 and W2; select W3 after W0 evidence closes; select only named W4 dependency groups. Keep W5 as separately selected research. This recommendation does not approve any wave.

## Capability preservation and evaluation

Every selected change must preserve domain depth, trigger reachability, exceptions, failure and recovery handling, authority/installation boundaries, security invariants, source priority, required evidence and completion conditions. Compression is behavior-preserving only when all those remain equivalent. F03 deliberately changes an ambiguous public behavioral contract and must not be presented as compression. F01/F02/F04 repair bounded execution/authority/portability defects.

Do not spread model names or effort tables into domain skills. Keep shared invariants model-neutral; prompting-guide owns adaptation and controlled role projections. No model/effort remapping is recommended by this audit.

Quality evidence: representative positive/negative task cases, trigger selection, correct source choice, preserved authority and failure handling, and independent review of the actual artifact. Speed/cost evidence: compare task/context/tools and acceptance criteria held constant, change one factor, use independent repetitions, and compare only quality-passing runs. Measure elapsed time, tokens/cost, redundant reads/checks, and completion fidelity only in an explicitly authorized evaluation. All improvement claims here are hypotheses. No live benchmark or model comparison ran.

Unchanged recommendation: `alaa-algorithms-data-structures` static guidance was read together with all eight references and merits None/Defer; it contains no executable asset. Consumer performance remains unmeasured. Also retain the core proof-tier doctrine, fail-closed security, workflow lifecycle, source-first documentation, low-noise evidence preservation, and UI accessibility/preview-release distinctions. Limited inspection supports retaining these behaviors; it does not certify every reference or script in their skills as None. The matrix uses Not assessed for those whole-skill gaps.

## Separate decisions outside the source program

- New roles: none proposed; existing researchers, implementers, verifiers and independent specialists cover the identified work.
- Installation/tool upgrades: F10, Codex CLI refresh, Hindsight package refresh and any global-memory correction require separate permission and target paths. No install is bundled with W3/W4.
- Major-version migration: none approved or silently proposed as a default. Go toolchain, Kubernetes API, Helm major, Vue preview, PHP/Laravel and provider compatibility changes need explicit consumer-specific decisions.
- Retirement: none proposed; lack of recent evidence is insufficient for retirement. Any later selected retirement must archive under repository policy, never delete.
- Scope expansion: application consumers, cluster access, external catalogs, global policy, vendor refresh and runtime calibration remain separate.

## Observed validation and limitations

See `checks.json` and named logs: four root native gates; policy-only Codex check (zero pins, insufficient by itself); explicit Codex 24-pin check; Claude 23-projection check; Codex renderer; both orchestrator pack checks. Ten lead-run commands returned exit 0. The backend researcher additionally observed the Python normalization reference self-test pass (145 cases, two modes); this is single-runtime proof, not the four-runtime harness or middleware integration. No full workload suite, live provider probe, browser flow, installed activation test, model benchmark, or consumer integration test ran. Prior GPT verification is cited historical evidence, not counted as newly run.

Untracked enumeration emitted access warnings in old archived temporary directories; archived contents were excluded and not modified. The bounded tracked baseline was captured separately. Checks used Python without bytecode and BelowNormal shell priority. No auto-review escalation or permission rejection occurred.

Three independent alaa-researcher lanes were dispatched, all configured gpt-6-sol/medium; runtime identity unknown. The lead was requested as GPT-6 Astra, but observed model/effort and token counters are unavailable. Agent declaration did not establish enforced isolation. Branch span is unavailable because this task created no plan/branch/commit.

Stage B boundary: no selection has been recorded. No implementation plan, checkpoint, execution prompt, implementation, installation, commit or publication was created. After explicit item/wave selection, only the approved plan, required workflow companions and self-contained execution prompt may be written.
