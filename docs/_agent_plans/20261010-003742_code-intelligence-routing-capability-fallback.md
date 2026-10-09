# Workflow Plan - Code intelligence routing capability and fallback upgrade

- Task ID: `20261010-003742_code-intelligence-routing-capability-fallback`
- Mode: `plan`
- Profile: `resumable`
- Status: planning
- Created: `2026-10-09T21:07:42Z`
- Parent plan: not created; the August routing-upgrade family is completed history
- Prompt pack: not created
- Checkpoint: `docs/agents/20261010-003742_code-intelligence-routing-capability-fallback-state.md`
- Machine state: not created
- Base branch and commit: `main` / `2f916326788eee35933b82ae4898a2dbfeace9af`
- Work branch: `main`; inspect again before approved implementation
- Worktree: current checkout (`.`)

## Summary and Outcome

The user authorized preparing this plan and checkpoint. Obtain separate approval of the validated plan before changing the target skill.

Upgrade `skills/sohrab/alaa-code-intelligence-routing/` for Codex and Claude: select each operation's best available evidence owner, reuse evidence, handle simultaneous outages without loops, and finish with native proof. Keep the contract compact and portable; capability decides routing, without assuming universal speed or completeness.

## Scope

- Authorized now: this plan and its checkpoint, read-only review, and their validation.
- Proposed after approval: the target skill body, metadata, and bundled references; review/evaluation evidence under `outputs/20261010-code-intelligence-routing/`.
- Preserve other skills, runtime/model policies, repository instruction files, indexes, completed historical plans, and other repositories. A newly discovered required cross-scope edit returns for a scope decision.
- No installation, provider upgrade, reindex, integration/hook configuration change, service startup, commit, or publication is part of this work.
- Deliver English repository artifacts and Persian user reports. Keep shipped guidance portable and self-contained. Use existing role definitions; no custom agent files are needed.

## Handoff Package

- Confirmed facts (verified, each with how it was verified): branch/HEAD above came from Git; tracked and scoped planning/target status were clean before this task. Reading the target found 11 files: body, metadata, nine references, and no scripts. The routing contract and default prompt currently limit a question to one secondary owner. Nine references require a topic map under the pack contract, but none exists. Local CLI output established CodeGraph `1.6.2`; the user subsequently reported successful reindexing of all projects. The latter is user evidence, not a new live verification.
- Open assumptions (believed but unverified, each with what would verify it): provider availability, semantic backend coverage, application/database identity, and access to both runtime families during implementation; inspect only the surface needed by a selected evaluation. Versioned upstream research establishes potential capability, not installation or health.
- Ruled out (approach, reason, evidence): copying an external workstation tool inventory or depending on its path, per user correction; repeated indexing, because the user completed it; unconditional parallel retrieval, because it duplicates facts; new custom agents, because existing writer/reviewer/verifier roles provide the required authority separation.
- Read first on resume (ordered exact paths): this plan; its checkpoint; `AGENTS.md`; `skills/sohrab/AGENTS.md`; `skills/sohrab/alaa-code-intelligence-routing/SKILL.md`; the reference selected by `skills/sohrab/alaa-prompting-guide/SKILL.md` for authoring; phase-bound skills below. Reuse prior research through the source ledger, refreshing only changed or unresolved claims.
- Environment notes (command shapes that work here, and ones that look right but fail): run the commands below from the repository root using PowerShell and installed Python. The workflow validator supports explicit `--plan`, `--continuation`, and `--profile resumable`. Fleet validation supports `--skill`; the skill-pack validator has no single-skill flag. The root `project-setup/` paths named in target reference 70 are absent; replace those dependencies inside the target with portable, sourced binding guidance rather than inventing an external owner.
- Traps (looks correct, is not): an index directory is not health proof; CLI transport fallback cannot fix the same bad index; a tool name is not backend support; installed metadata and lockfile intent are different evidence; source routes/migrations are not runtime registrations/schema; a timeout after mutation is not permission to replay it; static instruction checks are not observed runtime compliance.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-workflow | skills/sohrab/alaa-workflow/SKILL.md | Plan/checkpoint changes | All phases | Stop workflow mutation and report missing owner |
| alaa-codex-orchestrator | skills/sohrab/alaa-codex-orchestrator/SKILL.md | Role allocation or dispatch | All Codex phases | Stop affected dispatch |
| alaa-prompting-guide | skills/sohrab/alaa-prompting-guide/SKILL.md | Drafting/reviewing controlling text | All phases | Stop affected authoring/review |
| alaa-low-noise | skills/sohrab/alaa-low-noise/SKILL.md | Retrieval/output budgeting | All phases | Preserve bounded evidence; report missing owner |
| alaa-code-intelligence-routing | skills/sohrab/alaa-code-intelligence-routing/SKILL.md | Evaluating current routing | All phases | Stop target revision |
| alaa-testing-strategy | skills/sohrab/alaa-testing-strategy/SKILL.md | Acceptance/proof design | All phases | Stop proof-design decision |

## Acceptance Contract

| ID | Required outcome | Evidence |
|---|---|---|
| A01 | A question selects one primary owner by operation and worktree; reuse adequate returned source, graph paths, metadata, and prior results. Fresh literal/known-file questions retain bounded native shortcuts. | Routing/source diff; S01-S03 |
| A02 | Fallback is finite and operation-specific across multiple outages; every transition identifies the missing fact, failed capability, and lost guarantee. | State-machine review; S04-S07 |
| A03 | Wrong-worktree evidence is rejected. Empty, truncated, stale, heuristic, and unsupported results cannot establish absence or completeness. | S03, S05, S08 |
| A04 | Semantic mutations require supported operations and authorization; an uncertain result is reconciled before continuation, never replayed or automatically replaced with text editing. | S09; instruction review |
| A05 | Boost documentation, application boot, and database failures are independent. Native alternatives must observe the same intended application/environment/database for runtime claims. | S10-S12 |
| A06 | Relevant native tools and fallback procedures ship inside the skill, without workstation paths or an external inventory dependency; presence and project recipes are checked when needed. | New native reference; portability/source review |
| A07 | Cover every verified relevant capability group with a trigger, supported operation/transport/backend, authority class, source/version, fallback, rule owner, and acceptance mapping. Record a reason for excluding speculative or unrelated groups. Installed inventory bounds usability; optional/beta tools and unsafe operations are never assumed universally available or read-only. | Complete capability ledger; S06, S09, S13 and a mapped scenario for each included group |
| A08 | One owner per rule, conditional reference loading, a single body pointer to the topic map, preserved authority/stop conditions, and a documented draft-to-compressed rewrite. Metadata agrees with the routing contract. | Instruction review; pack/fleet/link checks |
| A09 | Native repository gates determine completion. Missing or unrun gates remain explicit; static validity, observed behavior, and measured performance are separate conclusions. | Command receipts; scenario/evaluation record |
| A10 | The approved scope is preserved; no changes to the skill before plan approval, and no integration changes or repeated indexing during implementation. | Git path review; target manifest comparison |
| A11 | Final evidence covers all scenarios below. Live checks in each runtime family are attempted only when an existing authorized surface is available; unavailable cells remain unverified, with no cross-runtime performance claim. | Runtime/scenario matrix with observed, unrun, failed, and blocked cells |

## Proposed Routing and Fallback Contract

The target references will own these approved routing decisions.

| Operation | Primary selection | Eligible fallback and evidence limit |
|---|---|---|
| Unknown code location, cross-file flow, callers/impact | CodeGraph explore with a bounded question | MCP transport failure may use installed CLI against the same valid worktree/index. For an unresolved structural fact, use Serena if its backend supports that fact, then bounded native search/source. Shared index failure skips the CLI detour. No inferred graph completeness from text. |
| Source already returned by exploration | Reuse adequate, fresh returned source | Read only a missing/stale region from the current file. Semantic verification or runtime validation is a new, named question rather than a reread of the same fact. |
| Symbol identity, references, implementations, diagnostics, or semantic edits | Serena when the active backend exposes the required operation | Use an existing stack-declared native semantic interface for an equivalent operation, such as gopls, if available. Targeted source can support a partial read claim, not complete reference coverage or semantic mutation. |
| Literal/config/Markdown evidence, known-path text, structured data | Bounded native file/search/parser operations | Use an available equivalent native operation, preserve scope and format, and state missing parser guarantees. Do not start a graph or language server merely to read known text. |
| Laravel/package guidance | Boost documentation with verified installed package versions | Version-correct official documentation through an available documentation/web surface. Installed package source answers implementation questions; it does not silently replace documentation of conventions. |
| Laravel runtime/application/schema facts | The applicable Boost operation | Equivalent authorized project-native commands only if they observe the same environment. On boot failure, boot-dependent CLI commands are not independent fallbacks. On database failure, source migrations describe intent only. |
| Tests, lint, type/build checks, formatting, and diff inspection | Inspected repository-native recipes | An alternative must prove the same acceptance property; otherwise report the gate blocked. Tool discovery and static graph output cannot mark execution passed. |

For one unchanged question, keep the attempted owner/operation set. Select lazily, skip known unavailable candidates, and never cycle. Permit at most one cause-specific, non-mutating capability/health repair and one materially different retry for a failed operation when the cause supports it; otherwise advance immediately. An authorized fallback is a different eligible operation, not a reset of that retry budget. Scope or environment changes invalidate only affected evidence and capability state. Exhaustion leaves a partial answer or blocks the dependent claim; unrelated work can continue.

Inventory/activation is not automatically harmless: inspect side effects before project activation, onboarding, arbitrary execution, or generated-file operations. A semantic mutation with unknown outcome requires actual diff/state reconciliation; if safe continuation cannot be established, stop that operation. No provider fallback expands authority.

## Native Guidance to Bundle

Create `references/45-native-tools.md` with triggers, presence checks, bounded examples, and output/evidence limits for the surfaces below; do not copy a workstation inventory.

| Need | Relevant candidates, subject to observed availability and project configuration |
|---|---|
| Files/literals/structure | `rg`, `fd`, native file reads; `ast-grep` only for supported syntactic queries, never a substitute for binding/type resolution |
| Structured content | `jq`, `yq`, or an available language parser matched to the actual format and tool dialect |
| Working changes/history | Scoped Git status/diff/show and an explicit worktree identity |
| PHP/Laravel | Installed PHP/Composer, inspected Composer scripts, project test runner, PHPStan/Pint when configured; Artisan only for an authorized operation in the intended environment |
| Go | Go toolchain/project recipes, gopls for a missing supported semantic operation, configured formatter/linter/test wrappers such as gofmt, goimports, gofumpt, golangci-lint, or gotestsum |
| Other project gates | Existing package-manager scripts and lockfile-selected tooling; stack owners retain test/build policy |

## Evaluation Matrix

Both runtime families use the same bounded questions and capability assumptions. Define expected evidence boundaries before execution and record actual traces separately. Simulate outages through declared unavailability or disposable fixtures; do not change working MCP registrations/services.

| Scenario | Required decision |
|---|---|
| S01: healthy discovery returns source and paths | Reuse both; zero duplicate retrieval of the already answered fact |
| S02: known literal/config question | Use the bounded native path without unnecessary provider startup |
| S03: missing/stale source region or heuristic call edge | Retrieve only the gap; retain uncertainty |
| S04: CodeGraph MCP transport unavailable | Same-index CLI only when independently usable; no retry loop |
| S05: index stale/wrong root | No CLI-as-repair claim; reject wrong-root evidence and use eligible scoped alternatives |
| S06: Serena/backend operation unavailable | Skip unsupported operations; use an equivalent available semantic operation or label partial evidence |
| S07: two providers unavailable; then all relevant candidates unavailable | Continue through the finite eligible chain, then stop the dependent claim truthfully |
| S08: empty, paginated, or truncated result | Complete the bounded page/gap if needed; do not infer absence from missing evidence |
| S09: semantic rename/edit times out after possible mutation | Reconcile actual state; no replay, broad replacement, or authority expansion |
| S10: Boost docs unavailable, application metadata healthy | Retain metadata; select version-correct documentation fallback |
| S11: application boot unavailable, documentation healthy | Retain documentation; do not claim boot-dependent CLI is independent proof |
| S12: database unavailable or wrong environment | Retain unrelated evidence; block live-schema claims without equivalent observation |
| S13: optional/beta capability advertised but absent in inventory | Do not call it or assume it is read-only |
| S14: native proof tool unavailable | Block the required gate; report other observed results without a PASS substitution |
| S15: resume/worktree/branch/service identity changes | Reuse only evidence whose identity and freshness remain valid |

Mandatory static acceptance: every scenario has an expected owner/fallback, forbidden inference/action, and mapped final rule, reviewed independently. For available runtime evaluations record requested/observed model controls, runtime/version, worktree, capability assumptions, operation trace, result, duplicate retrieval count, and termination. Record time/tokens only if observable. Missing runtime cells do not fail a static source check, but they prevent claims that both families were behaviorally validated. Do not claim a speedup without a comparable baseline on the same environment/questions.

## Ordered Work

### Phase 1 - Prepare and approve the execution contract

- Status: planning
- Depends on: none
- Reasoning and selection reason: the user explicitly requested a reviewable plan/checkpoint before product edits.
- Settled/open decisions and invariants: user scope and completed reindex are settled; implementation approval is outstanding.
- Risk and required observers: incomplete fallback/acceptance rules; read-only planner advice and independent instruction review.
- Owned scope: this plan and checkpoint only.
- Excluded from this phase: target skill edits and execution evaluations.
- Required skills: alaa-workflow, alaa-codex-orchestrator, alaa-prompting-guide, alaa-low-noise, alaa-code-intelligence-routing, alaa-testing-strategy
- Work:
  - [x] Inspect current target, repository rules, prior completed plan, and available validation interfaces; reuse completed parallel research. [skills: inherit]
  - [x] Draft the acceptance, fallback, scope, and evidence contract with a resumable checkpoint. [skills: inherit]
  - [x] Compress the draft without changing decisions; obtain independent review and pass planning checks. [skills: inherit]
  - [ ] Receive explicit user approval of this plan before advancing. [skills: inherit]
- Acceptance criteria: A10; all remaining acceptance outcomes and next actions are checkable without conversation history.
- Validation commands: V01-V03 below; compare the target manifest to the baseline.
- Evidence observed: initializer exit 0; planner advisory complete; V01/V02 exit 0 after review corrections. V03 found only the two new planning files in scoped status, no target changes, and the unchanged 11-file target manifest. Independent instruction review approved the revised plan with no remaining actionable findings; complete capability coverage and checkpoint receipts closed its two initial findings. User approval is the only outstanding Phase 1 task.
- Snapshot: target baseline at HEAD `2f916326788eee35933b82ae4898a2dbfeace9af`; SHA256 `b86d0ae583fb0dcbc079984e1018140b472c90b5a70947efd62db152de07e89b`; paths `skills/sohrab/alaa-code-intelligence-routing/` (11 files).

### Phase 2 - Implement the approved routing contract

- Status: pending
- Depends on: Phase 1 and explicit plan approval
- Reasoning and selection reason: one writer keeps interdependent routing, fallback, capability and metadata rules consistent.
- Settled/open decisions and invariants: A01-A11 and the matrices above govern; verify installed interfaces before concrete examples.
- Risk and required observers: weakened authority, duplicated owners, accidental capability promises; independent Phase 3 observers review the integrated result.
- Owned scope: target skill directory and grouped task evidence only.
- Excluded from this phase: unrelated skill/policy/configuration files and deployment effects.
- Required skills: alaa-workflow, alaa-codex-orchestrator, alaa-prompting-guide, alaa-low-noise, alaa-code-intelligence-routing, alaa-testing-strategy
- Work:
  - [ ] Recheck working-tree changes and source-sensitive gaps; create an old-rule to new-owner map and scenario expectations. [skills: inherit]
  - [ ] Update body, metadata, references 10/20/40/60/70/80/90 as needed; inspect 30/50 and change only rules directly affected by the approved contract. Add 00-topic-map and 45-native-tools. [skills: inherit]
  - [ ] Replace stale external binding dependencies with self-contained, sourced guidance; preserve setup authority limits. Draft, then compress; review content relocation as a separate behavioral change. [skills: inherit]
  - [ ] Prepare the complete capability/source ledger, map every included group to a scenario, and prepare the final scoped diff for independent acceptance. [skills: inherit]
- Acceptance criteria: A01-A08 and A10 are implemented; A09/A11 have evidence slots with no fabricated results.
- Validation commands: focused V05 and diff review during authoring; V04-V09 once after integration in Phase 3.
- Evidence observed: not run; not authorized yet.
- Snapshot: not captured yet.

### Phase 3 - Review, validate, and report

- Status: pending
- Depends on: Phase 2 integrated snapshot
- Reasoning and selection reason: separate instruction correctness, executable checks, and live behavior evidence without duplicate broad reviews.
- Settled/open decisions and invariants: passing structure does not establish runtime behavior or performance; unavailable cells remain visible.
- Risk and required observers: instruction reviewer, independent general reviewer, and verifier on the same immutable snapshot.
- Owned scope: read-only reviews/checks; the Phase 2 writer owns any necessary in-scope repairs; parent owns plan/checkpoint/evidence integration.
- Excluded from this phase: unapproved setup or cross-scope repairs to make a gate pass.
- Required skills: alaa-workflow, alaa-codex-orchestrator, alaa-prompting-guide, alaa-low-noise, alaa-code-intelligence-routing, alaa-testing-strategy
- Work:
  - [ ] Run V04-V09 and independent instruction/general reviews against the integrated snapshot; map A01-A11 and S01-S15 to results. [skills: inherit]
  - [ ] Execute safe read-only evaluations through each already available runtime family; record inaccessible cells and observed controls, without installing or reconfiguring providers. [skills: inherit]
  - [ ] Route actionable findings to the writer within the failure budget; recheck changed/invalidated evidence only. [skills: inherit]
  - [ ] Reconcile source/docs/metadata, record final snapshot and unresolved limits, update checkpoint, and present the truthful Persian handoff. [skills: inherit]
- Acceptance criteria: A01-A11 reconciled; mandatory source checks and independent reviews pass, or the phase remains blocked. Unavailable optional live cells restrict claims explicitly.
- Validation commands: V01-V09, consolidated rather than rerun per reviewer.
- Evidence observed: not run.
- Snapshot: not captured yet.

## Validation Commands and Receipts

Run from the repository root. Capture command, exit code, relevant output, and input snapshot. Exit 2 is failed/unavailable, never PASS. Separate pre-existing findings outside scope from introduced defects without waiving a required gate.

| ID | Command / observation |
|---|---|
| V01 | `python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20261010-003742_code-intelligence-routing-capability-fallback.md --continuation docs/agents/20261010-003742_code-intelligence-routing-capability-fallback-state.md --profile resumable` |
| V02 | `python -B skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py . --files docs/_agent_plans/20261010-003742_code-intelligence-routing-capability-fallback.md docs/agents/20261010-003742_code-intelligence-routing-capability-fallback-state.md` |
| V03 | `git diff --check`; scoped status/diff plus target manifest comparison to prove the planning boundary |
| V04 | `python -B scripts/validate_sohrab_skill_pack.py` |
| V05 | `python -B scripts/check_fleet_references.py --skill alaa-code-intelligence-routing` |
| V06 | `python -B scripts/check_skill_index.py` |
| V07 | `python -B scripts/check_lifecycle_contract.py` |
| V08 | `python -B skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py` |
| V09 | `python -B skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py . --files` followed by the exact changed Markdown paths; independent A01-A11/S01-S15 review and scoped Git diff |

Manifest procedure: sort all files under the target by repository-relative POSIX path; concatenate each path, one space, its SHA256, and a newline; SHA256 the UTF-8 result. Save the implementation receipts in `outputs/20261010-code-intelligence-routing/`. Checker self-tests are unnecessary unless checker code changes, which is outside this plan.

Planning receipts observed on 2026-10-10: V01 returned exit 0, `Validation completed without blocking errors (profile: resumable).`; V02 returned exit 0, `Validated links in 2 Markdown file(s)`. Both passed again after review corrections at 2026-10-09T21:19:49Z. V03 `git diff --check` returned exit 0; scoped `git status --short --untracked-files=all --` with the two planning paths and target directory showed only the two new planning files. The Python manifest comparison returned exit 0, `target_files=11`, `target_unchanged=True`, and the baseline digest recorded in Phase 1. Because Git diff does not inspect untracked content, a separate Python read checked both new files: UTF-8, no machine-specific absolute paths, no template markers, and no trailing whitespace; exit 0. Independent review returned APPROVED, with no remaining actionable findings. V04-V09 and live provider evaluations have not run; they belong to the approved implementation phases.

## Task Allocation

The active runtime orchestrator owns these task selections; roles remain model-neutral. Recheck availability/control support before dispatch. Main-session serving identity/effort are unobservable. No writing lane self-accepts its output.

| Task/scope/complexity | Role authority | Priority/reason | Model | Effort | Selection/admission evidence and source date | Invocation/requested/effective controls | Availability/limits |
|---|---|---|---|---|---|---|---|
| Completed independent CodeGraph, Serena, Boost research | alaa-researcher | User requested parallel Luna research | gpt-6-luna | high | Scoped primary-source research; results reused, 2026-10-10 | Three dispatched lanes; serving identity unobservable | Complete; no repeat sweep |
| Advisory planning | alaa-planner | Balanced; settled scope, bounded semantic choices | gpt-6.1-sol | medium | Routing matrix and current neutral role, checked 2026-10-10 | Fresh-context explicit override dispatched; observed serving model/effort unknown | Read-only actions; narrower sandbox enforcement unknown |
| Plan and final instruction review | alaa-instruction-reviewer | Balanced; interacting authority/fallback/compression decisions | gpt-6.1-sol | high | Instruction gate plus substantive semantic judgment, 2026-10-10 | Fresh-context explicit override; record observations at dispatch | Read-only; no implementation ownership |
| Approved product authoring and fixes | alaa-implementer | Balanced; coupled rules across body/metadata/references | gpt-6.1-sol | high | Named scope, acceptance and interacting semantic decisions, 2026-10-10 | Future fresh-context explicit override | Plan approval and current controls required |
| Final general acceptance review | alaa-reviewer | Balanced; focused complete-change correctness review | gpt-6.1-sol | medium | Distinct from instruction/compression specialist, 2026-10-10 | Future fresh-context explicit override | Independent of writer; avoid replaying specialist work |
| Exact command verification | alaa-verifier | Balanced; fixed commands and bounded evidence capture | gpt-6-luna | medium | Mechanical verification, no fix or design authority, 2026-10-10 | Future fresh-context explicit override | Serialize resource-heavy checks; no broad test additions |

## Delegation

- Parent ratifies the plan, controls scope/approval, integrates evidence, and writes checkpoint updates. Each dispatch receives relevant facts explicitly.
- Ready sets: planning advisor/reviewer now; one writer after approval; instruction reviewer, general reviewer, and verifier after integration. With three worker slots available, these final read-only lanes may run concurrently against the same unchanged snapshot.
- No parallel product writers. The target's operational documentation is authored with its instructions in Phase 2; a separate documenter is unnecessary unless a new documentation deliverable is approved.
- Runtime evaluations are bounded verifier work after explicit capability admission; they do not authorize scenario-induced mutations in a user's project.
- Reuse research and command receipts. Invalidate only on relevant source, input, worktree, environment, capability, or artifact changes. Do not repeat broad checks merely for a new reviewer.

## Source Ledger

Phase 2 reconciles verified documentation with relevant installed inventories through bounded reads, without checking every provider at startup. Each capability-group ledger entry records: inclusion/exclusion and reason; trigger; operation and transport/backend requirements; read/write/execute authority; source/version; evidence limit; fallback; owning file; and acceptance/scenario IDs. Reference 90 owns shipped provenance; existing reference owners retain routing and authority. Missing installation evidence means unknown. Cover every verified relevant group, including specialized operations beyond default entry points when supported by evidence.

Prior research was completed on 2026-10-10 through three parallel Luna lanes. The links below are entry points for refreshing version-sensitive claims, not proof that any capability is installed.

- CodeGraph: [release history](https://github.com/colbymchenry/codegraph/releases), [MCP surface](https://colbymchenry.github.io/codegraph/reference/mcp-server/), [CLI](https://colbymchenry.github.io/codegraph/reference/cli/), [resolution](https://colbymchenry.github.io/codegraph/core-concepts/resolution/), [framework routes](https://colbymchenry.github.io/codegraph/guides/framework-routes/). Local baseline is 1.6.2; do not apply newer documentation blindly.
- Serena: [releases](https://github.com/oraios/serena/releases), [tools](https://oraios.github.io/serena/01-about/035_tools.html), [language support](https://oraios.github.io/serena/01-about/020_programming-languages.html). Research identified stable 1.7.0 and beta documentation; effective inventory/backend determines usable operations.
- Boost: [releases](https://github.com/laravel/boost/releases), [changelog](https://github.com/laravel/boost/blob/main/CHANGELOG.md), [official guide](https://laravel.com/framework/docs/boost). Research identified 2.10.3; inspect project package evidence and active inventory before concrete claims.
- Prompt authoring: `skills/sohrab/alaa-prompting-guide/references/60-skill-authoring.md`, its routed mechanics/evaluation references, [OpenAI skill guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), and [Claude skills](https://code.claude.com/docs/en/skills).
- Prior completed work: `docs/_agent_plans/20260801-172256_code-intelligence-routing-skill-upgrade.md` and its checkpoint are historical evidence only.

## Blockers and Next Action

- Blockers: no planning blocker identified. Product implementation is awaiting explicit user approval of this plan.
- Next action: present the validated plan/checkpoint and wait for explicit plan approval. Approval of preparing this plan must not be treated as approval of Phase 2.
