# Code intelligence routing upgrade - completion report

The approved local source upgrade is complete. Independent instruction and general reviews approved the change; required native checks passed. Runtime and performance claims remain bounded by the evidence below.

## Scope and snapshot

- Source: `skills/sohrab/alaa-code-intelligence-routing/`, 13 final files; 9 existing files modified and 2 references added. References 30/50 are unchanged.
- Observed branch: `main`; HEAD: `74735f6d6b1a79cead1255406df9070255d93309`.
- Final target SHA256: `0c81cf9dd70fe68e2d2c60db7d61693d8386c79d573fdd1edd37817f050408be`.
- Manifest: [13 file hashes](authoring-drafts/08-metadata-corrected-target-manifest.sha256). Hash construction is defined in the [plan](../../docs/_agent_plans/20261010-003742_code-intelligence-routing-capability-fallback.md).
- Task artifacts: this output directory plus the plan and [checkpoint](../../docs/agents/20261010-003742_code-intelligence-routing-capability-fallback-state.md).
- The intervening external commit changed planning files only. The agent did not commit, stage, install, reindex, change integration configuration or edit another skill. Existing staging was preserved.

The body now loads one topic map and routes by the requested operation. The references cover all applicable provider subsets, including none, normal absence versus degraded capability, finite fallback, evidence reuse and identity, uncertain mutation reconciliation, and independent Laravel documentation/application/database failure domains. Native guidance is bundled and portable. Forty capability groups are qualified by inventory, backend, authority and source. No universally faster provider or measured speedup is asserted.

## Acceptance audit

| Requirement | Closure evidence |
|---|---|
| A01: operation owner and evidence reuse | Routing contract, S01-S03 source review and independently graded synthetic decisions |
| A02: every applicable subset and finite fallback | [Availability matrix](availability-matrix.md), S04-S07, instruction review of Laravel's eight subsets and four applicable CodeGraph/Serena subsets for other stacks; native availability qualified |
| A03: identity, freshness and completeness | Routing contract and S03/S05/S08 static and synthetic coverage |
| A04: supported mutation and uncertain outcomes | S09 denies replay/text substitution; source and proposed decisions reviewed; no live mutation trial |
| A05: independent Boost failure domains | Stack binding, S10-S12; same application/environment/database required for runtime alternatives |
| A06: self-contained native guidance | Bundled reference 45, portability inspection and source/link checks; no workstation inventory dependency |
| A07: full relevant capability mapping | [40-group ledger](capability-ledger.md), source-qualified operations, authority and scenario mappings, independent general review |
| A08: ownership, loading and compression | [Rule migration](rule-migration.md), preserved authoring drafts, one body topic-map pointer, metadata and instruction closure |
| A09: native proof and truthful limits | Native receipts below distinguish static gates, synthetic decisions, one live smoke and unavailable cells |
| A10: authorization and scope | Phase 1 target unchanged before approval; final scoped diff and manifest; no integration or indexing work |
| A11: scenarios and runtime limits | [S01-S15 expectations](scenario-expectations.md), independent 15/15 Codex proposed-decision grades; Claude authentication failure and unrun provider cells explicitly retained |

## Reviews and checks

| Evidence | Observed result / reuse boundary |
|---|---|
| [Instruction review](instruction-review.md) | APPROVED on final 13-file manifest; duplicate ownership and lost metric safeguards corrected and independently closed |
| [General review](general-review.md) | APPROVED on preceding Markdown-identical snapshot; parent reused after YAML-only UI-summary repair, independently closed by instruction reviewer |
| V04 skill-pack validation | Initial exit 1 for 66-character UI summary; exact repair to 62 characters; independent corrective run exit 0 |
| V05 scoped fleet references | Writer's complete correction receipt: exit 0, 1 of 69 skills, 12 Markdown files, 15 citations, no findings; cited rather than independently rerun; later YAML-only change does not invalidate it |
| V06 skill index | Independent verifier exit 0 |
| V07 lifecycle contract | Independent verifier exit 0 |
| V08 agent contracts | Independent verifier exit 0 |
| V01 workflow and V09 links | Independent verifier exit 0; links checked across 20 Markdown files. Final report/checkpoint edits receive separate closure checks |
| V03 diff hygiene | Independent verifier exit 0; final target staged/unstaged checks both exit 0 |

Reproducible commands, outputs, time/resource limits and snapshots are preserved in [initial verification](verification/verification-receipt.json), [corrective verification](verification/corrective-receipt.json), and [authoring receipts](authoring-report.md). The verifier used BelowNormal priority, two logical CPUs and a 120-second command timeout. Initial failures remain recorded. A mistaken manifest basename blocked one corrective preflight; correcting the dispatch path resolved it without source changes or a waived gate. The later [closure receipt](verification/final-artifact-receipt.json) records only changed-artifact checks and final scope/hash observations; unchanged product gates were not repeated.

## Behavioral evidence and limits

- **Observed live:** CodeGraph 1.6.2 status matched this worktree, and one bounded MCP exploration succeeded with source and relationships. See [environment evidence](environment-evidence.md) and [smoke receipt](codegraph-smoke.json). This establishes one observed call, not a benchmark or fleet health.
- **Observed synthetic:** one Codex source-prompt replay returned 15 proposed decisions; the independent general reviewer graded all PASS. No case tools executed. [Receipt](runtime-evaluation/codex-receipt.json) retains the original input snapshot and the reviewed reuse decision after later non-invalidating edits.
- **Blocked optional cell:** Claude CLI 2.1.294 was invoked with explicit model/effort and tools disabled, but exited 1 with expired OAuth HTTP 401 before completing a replay. [Receipt](runtime-evaluation/claude-receipt.json). No authentication or settings change was attempted.
- **Unverified:** live Serena/Boost, real outage recovery, uncertain-write reconciliation, installed-skill activation in either runtime, effective narrower sandbox enforcement and serving model identities. Source-level cross-runtime compatibility is not observed compliance in both runtimes.
- **Not measured:** comparative latency, total-session token savings or accuracy gains. No performance baseline was run.

## Completion and recovery

`IMPLEMENTED`: proven by focused/native gates on the identified local content snapshot. `MERGE_CANDIDATE`: all applicable local integration gates and independent reviews passed. `RELEASE_CANDIDATE`: not requested. `PUBLISHED`: not requested. These labels use the workflow owner's definitions, without adding a release step.

The product changes remain local and uncommitted by the agent. This is the remaining recovery risk; manifests, preserved drafts and review/check receipts identify accepted content but do not replace a commit. No mandatory source-upgrade blocker or requested implementation action remains. Later edits to relevant inputs invalidate the corresponding evidence.

## Separate research boundary

The user's additive-tool research request produced a [separate report](../20261010-code-intelligence-adjunct-research/report.md). It did not change this skill, its approved plan, acceptance contract or configuration. Candidate tools were not installed or benchmarked. No adoption work is implied by completing that investigation.

## Dispatch accounting

Serving identities/efforts and complete input/output token counters are not observable. The following are requested controls, not serving-model proof. Eleven distinct collaboration agents were dispatched across the task; reuse/follow-up turns are not additional agents.

| Agent | Requested model / effort | Responsibility |
|---|---|---|
| codegraph_research | gpt-6-luna / high | Primary-source research |
| serena_research | gpt-6-luna / high | Primary-source research |
| boost_research | gpt-6-luna / high | Primary-source research |
| routing_plan_advisor | gpt-6.1-sol / medium | Read-only planning advice |
| routing_plan_review | gpt-6.1-sol / high | Independent plan review |
| routing_implementation | gpt-6.1-sol / high | Sole product writer and corrections |
| routing_instruction_gate | gpt-6.1-sol / high | Independent instruction review |
| routing_codex_replay | gpt-6.1-sol / medium | Synthetic source-prompt replay |
| adjunct_tools_research | gpt-6.1-sol / medium | Separately authorized live research |
| routing_verification | gpt-6-luna / medium | Independent command execution |
| routing_acceptance_review | gpt-6.1-sol / medium | Independent general review and replay grading |

The separate failed Claude CLI attempt requested claude-sonnet-5-5/medium; it is not included in the collaboration-agent count. Aggregate branch span and full session token breakdown are unavailable. Command receipts distinguish checks run independently, a cited focused writer check, and deliberately unrun live cells.
