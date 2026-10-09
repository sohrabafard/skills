# Workflow Plan - Go routing ownership and authoring alignment

- Task ID: `20261009-222708_go-routing-ownership`
- Mode: `execute`
- Profile: `resumable`
- Status: completed
- Created: `2026-10-09T22:27:08Z`
- Parent plan: none; the prior routing upgrade is completed history
- Prompt pack: not created
- Checkpoint: `docs/agents/20261009-222708_go-routing-ownership-state.md`
- Machine state: not created
- Base branch and commit: `main` / `52e576c31ca654e244a25657f8e8bca9bd3c32fe`
- Work branch: `main`
- Worktree: current checkout (`.`)

## Summary and Outcome

The user authorized planning followed by execution. Modernize the Go skill's controlling prose while making alaa-code-intelligence-routing the sole owner of provider selection, order, availability and fallback. Preserve Go doctrine and required native proof. Both runtimes consume the same Markdown contract; source checks do not establish live activation.

## Scope

- One coupled writer: `skills/sohrab/alaa-golang/` and narrowly necessary native-edit/diagnostic/dependency routing clarification in `skills/sohrab/alaa-code-intelligence-routing/`.
- Parent: this plan/checkpoint, `outputs/20261010-go-routing-ownership/`, and its entry in `outputs/README.md`.
- Exclude vendor, other skills, runtime/model policy, instructions, integration configuration, installation, reindexing, Go application changes, dependency/version modernization, commits and external effects.
- Execution profile: lean. One product lane; parent performs independent correctness review, instruction specialist reviews controlling text, verifier executes native gates. Product instructions are the deliverable; separate operational documentation is unnecessary.

## Handoff Package

- Confirmed facts (verified, each with how it was verified): current Git branch/HEAD above, tracked status clean and target scoped status clean before writes. Go has 23 files, SHA256 24f982663ae3f5f68577c856ad28dc78f840369df90a385e1033c6501b0c5874; routing has 13 files, SHA256 0c81cf9dd70fe68e2d2c60db7d61693d8386c79d573fdd1edd37817f050408be. Native reads and advisory inspection found duplicated provider rules in Go body, metadata and references 00/10/11/40/62. User wants future routing changes confined to their owner.
- Open assumptions (believed but unverified, each with what would verify it): effective serving model and narrower sandbox/MCP enforcement are not observable. No live cross-runtime conformance or performance gain will be claimed.
- Ruled out (approach, reason, evidence): copying replacement fallback rules into Go repeats the defect; requiring Serena or gopls for every edit contradicts the requested degraded path; removing mandatory native proof weakens acceptance; broad domain/version updates are outside this goal.
- Read first on resume (ordered exact paths): this plan, its checkpoint, `skills/sohrab/AGENTS.md`, the relevant target entrypoint, `skills/sohrab/alaa-prompting-guide/references/60-skill-authoring.md`, phase bindings below and task report receipts.
- Environment notes (command shapes that work here, and ones that look right but fail): installed Python is available; fleet checker accepts repeated `--skill`; workflow supports explicit plan/continuation/profile. Hindsight tools are absent from the current callable inventory; recall fails open to current repository truth. No memory write is authorized.
- Traps (looks correct, is not): a provider catalogue may retain factual entries without owning selection; a semantic mutation with unknown outcome must be reconciled before any alternative edit; a text search cannot prove complete references; a source scenario is not a live runtime test. Older Markdown has paired invocation forms; normalize affected files without inventing runtime-specific frontmatter.

## Decisions and Preserved Invariants

Use triggered pointers in Go, and keep executable provider policy in the routing owner. A future provider preference change must require no Go-side routing edit. Native Go commands remain domain proof recipes, not a second provider-selection table.

Ratified behavior change: provider diagnostics are supplemental unless the repository or acceptance criterion requires a specific semantic property beyond native proof. Missing optional provider diagnostics alone does not block authorized bounded edits or completion after required native gates pass. Any required uncovered property remains blocked; do not label native output equivalent without evidence.

Preserve kit-phase stops, P1-P13 handoff, owner precedence, gap reporting, freshness, framework/API/layer/cache rules, test-first behavior, package ladder, directive limits, build/vet/changed-package/full tests, conditional race/vulnerability checks and the four completion answers. Modernization may remove repetition and relocate lookup material only with a reviewed preservation map. Full drafts precede compressed delivery.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-workflow | skills/sohrab/alaa-workflow/SKILL.md | Plan/checkpoint decisions | All phases | Stop workflow edits |
| alaa-prompting-guide | skills/sohrab/alaa-prompting-guide/SKILL.md | Instruction authoring, review or controls | All phases | Stop affected action |
| alaa-codex-orchestrator | skills/sohrab/alaa-codex-orchestrator/SKILL.md | Allocation/delegation/gates | All phases | Stop dispatch |
| alaa-low-noise | skills/sohrab/alaa-low-noise/SKILL.md | Retrieval and returns | All phases | Preserve bounded evidence; report missing owner |
| alaa-golang | skills/sohrab/alaa-golang/SKILL.md | Go contract preservation | All phases | Stop source revision |
| alaa-code-intelligence-routing | skills/sohrab/alaa-code-intelligence-routing/SKILL.md | Evidence/tool selection | All phases | Stop routing revision |
| alaa-testing-strategy | skills/sohrab/alaa-testing-strategy/SKILL.md | Proof strength/scope | Validation decisions | Stop proof decision |
| alaa-extract-agent-lessons | skills/sohrab/alaa-extract-agent-lessons/SKILL.md | Final curation | Closure | Stop closure |

## Acceptance Contract

| ID | Outcome and evidence |
|---|---|
| A1 | All Go provider selection/order/fallback copies removed from body, references and metadata; triggered pointers reach the canonical owner. Inspect the entire 23-file package, not just keyword absence in SKILL.md. |
| A2 | Go domain obligations and native proof are preserved, with intentional optional-diagnostic change separately recorded. Baseline-to-final rule map and independent review required. |
| A3 | Canonical routing explicitly permits authorized bounded native edits without semantic providers and retains uncertainty limits, target identity, diff inspection, proof and unknown-mutation reconciliation. |
| A4 | Go dependency metadata/upgrade work starts with applicable native recipes; graph/semantic questions are conditional. No new fixed all-task provider sequence. |
| A5 | Complete lean instruction contract: role, triggers, procedure, authority, validation, output, stop/failure; one topic-map pointer; common frontmatter; affected Markdown uses /name and Codex metadata keeps $name. No environment-specific paths or new runtime assumptions. |
| A6 | Draft/compression/ownership evidence preserves rule force and distinguishes behavior changes from wording cuts. Current official authoring sources recorded; no improvement claim inferred from reduced words. |
| A7 | Independent review approves S1-S10 below; exact required native checks pass on the final snapshot. Live activation/compliance and performance remain unverified. |
| A8 | Scope preserved, no installations/configuration/commits, final plan/checkpoint/report agree and reusable-context gate recorded. |
| A9 | Latest explicit user preference: for supported source questions CodeGraph is preferred whenever adequate, including known files/symbols. Serena supplies a separately needed semantic operation or eligible fallback; configured gopls is the Go semantic fallback, then bounded native work. Reuse adequate evidence before any provider preference; never force an incapable provider, duplicate retrieval, or graph-based proof of resolved dependency/runtime state. |

## Static Conformance Scenarios

| ID | Required decision |
|---|---|
| S1 | Graph only, ordinary source fix: reuse graph evidence, make bounded native edit, inspect diff, run native proof. |
| S2 | Neither provider configured: no setup demand; adequate bounded source and native proof permit an authorized local edit. |
| S3 | Serena only: use eligible operation for the named need; do not require CodeGraph setup. |
| S4 | Missing semantic operation: use an available equivalent; if a required semantic guarantee is still missing, block only the dependent operation/claim. |
| S5 | Dependency-only upgrade: native manifests/version tooling first; no mandatory symbol survey. |
| S6 | Wrong root, stale or truncated evidence: reject or qualify only affected facts, never claim completeness. |
| S7 | Adequate evidence already returned: do not retrieve the same fact again. |
| S8 | Edit may have run before timeout: reconcile actual state before continuation; no blind replay or automatic text replacement. |
| S9 | Optional provider diagnostics absent: native gates still execute; explicitly required unproven gate remains blocked. |
| S10 | Change the provider priority in the canonical owner: Go pointers and domain obligations remain valid without a second policy edit. |
| S11 | Known source file or symbol, healthy matching CodeGraph and adequate source/structural operation: use CodeGraph; known identity alone does not select Serena. |
| S12 | Adequate evidence already returned: no extra Serena/native read or retroactive CodeGraph query; ask only a newly missing semantic fact. |
| S13 | A semantic edit/diagnostic needs an operation CodeGraph does not expose: select Serena directly when eligible, or configured gopls for a supported Go gap; no pointless graph-first probe or setup. |

## Ordered Work

### Phase 1 - Ground and plan

- Status: completed
- Depends on: none
- Reasoning and selection reason: explicit user request; bounded ownership/authoring repair with known target and preservation contract.
- Settled/open decisions and invariants: scope and policy decisions above ratified; no product decision remains open.
- Risk and required observers: authoring may accidentally remove Go obligations; independent advisory inspected all Go files.
- Owned scope: plan/checkpoint and task evidence only.
- Excluded from this phase: product edits.
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-codex-orchestrator, alaa-low-noise, alaa-golang, alaa-code-intelligence-routing
- Work:
  - [x] Inspect current sources, prior routing outcome, affected owners and official authoring guidance. [skills: inherit]
  - [x] Ratify advisory scope, preserved rules, scenarios and consolidated allocation. [skills: inherit]
  - [x] Save and validate executable plan/checkpoint before writer dispatch. [skills: inherit]
- Acceptance criteria: A1-A8 have checkable evidence and owners.
- Validation commands: V1, baseline manifest and scoped Git status.
- Evidence observed: initializer and V1 exit 0; advisory ratified. Exact command and tested planning inputs are in `outputs/20261010-go-routing-ownership/planning-receipt.json`.
- Snapshot: HEAD 52e576c31ca654e244a25657f8e8bca9bd3c32fe; SHA256 439fdefc76f42996ab588c4ce2c733fc51afa1e0afa896ce4930a115e4ded36c; paths docs/_agent_plans/20261009-222708_go-routing-ownership.md, docs/agents/20261009-222708_go-routing-ownership-state.md. Captured before receipt insertion.

### Phase 2 - Implement the coupled contract

- Status: completed
- Depends on: Phase 1 validated plan
- Reasoning and selection reason: ordinary coordinated authoring with semantic preservation; one writer avoids conflicting provider and Go rules.
- Settled/open decisions and invariants: A1-A6 and decisions above; no broad domain changes.
- Risk and required observers: lost domain obligations, unreachable owner, hidden provider requirements; Phase 3 independent gates.
- Owned scope: two target skill directories and task authoring evidence only.
- Excluded from this phase: parent plan/checkpoint/history index and all other files.
- Required skills: alaa-prompting-guide, alaa-low-noise, alaa-golang, alaa-code-intelligence-routing
- Work:
  - [x] Read both complete target packages, preserve full drafts and create a rule-preservation map. [skills: inherit]
  - [x] Modernize Go body/affected references/metadata and canonical native-continuation routing. [skills: inherit]
  - [x] Run focused V3 plus scoped diff checks; freeze a complete product manifest and return evidence. [skills: inherit]
  - [x] Apply A9 in canonical routing references 10/40 only, preserving Go unchanged and all prior guarantees; record a separate draft/diff/manifest and focused checks. [skills: inherit]
- Acceptance criteria: A1-A6 and A9 implemented; S1-S13 mapped without fabricated live results.
- Validation commands: V3 and scoped V7.
- Evidence observed: writer completed 10 changed files, full drafts/compression and rule/scenario maps. V3 and scoped V7 exit 0; 30 content checks passed after a newline-classification checker repair, with no product repair for that failure. Exact receipts are in `outputs/20261010-go-routing-ownership/authoring-report.md`. Independent acceptance remains Phase 3.
- Snapshot: HEAD 52e576c31ca654e244a25657f8e8bca9bd3c32fe; SHA256 43df187cbd34026e120dfee1b4c39a43502a54db6ee0806af6a72d7876d467ac; paths skills/sohrab/alaa-golang/, skills/sohrab/alaa-code-intelligence-routing/ (36 files); manifest `outputs/20261010-go-routing-ownership/authoring-final-manifest.txt`.

### Phase 3 - Independently accept and close

- Status: completed
- Depends on: Phase 2 frozen diff
- Reasoning and selection reason: separate author, judgment and command authority; all checks are cheap static work.
- Settled/open decisions and invariants: source validity is not live runtime or speed proof.
- Risk and required observers: instruction specialist, parent correctness review, independent verifier.
- Owned scope: read-only source gates; author owns fixes, parent owns plan/checkpoint/report/history entry.
- Excluded from this phase: setup, broad application tests, runtime credential repair and unrelated fixes.
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-codex-orchestrator, alaa-low-noise, alaa-golang, alaa-code-intelligence-routing, alaa-testing-strategy, alaa-extract-agent-lessons
- Work:
  - [x] Complete independent instruction and parent correctness reviews of the whole change and S1-S10. [skills: inherit]
  - [x] Run V2/V4-V7 independently; cite valid V3, repair only owned findings and rerun invalidated gates. [skills: inherit]
  - [x] Review A9 and S11-S13 incrementally, verify affected routing inputs, and retain valid earlier Go proof. [skills: inherit]
  - [x] Record sources, current snapshot, all acceptance outcomes, limits and final curation; update history and workflow artifacts. [skills: inherit]
  - [x] Run final changed-artifact V1/V6/V7 and report lifecycle states. [skills: inherit]
- Acceptance criteria: A1-A9 proven, mandatory gates pass and no unresolved required work.
- Validation commands: V1-V7 as consolidated below.
- Evidence observed: both reviews approved S1-S10; independent V2 initially failed on two cross-skill citations, then passed after one citation-only author fix. Incremental specialist review approved the exact delta. Affected V6/V7 passed, refreshed V3 cited; V4/V5 and unchanged V6 retained with explicit impact rationale. Verification receipts preserve both runs. Final artifact commands and tested hashes are in outputs/20261010-go-routing-ownership/final-artifact-receipt.json. Curation found no additional admitted memory candidate; no memory publication. The user's scope concern is assessed against baseline in review.md and report.md.
- A9 closure evidence: steering-report.md records the two-reference revision and byte-identical Go package. Parent and independent specialist approved S11-S13 while preserving S1-S10; steering verification V2/V6/V7 passed, refreshed V3 cited, unaffected evidence retained with impact rationale. Official MCP/resolution sources and user authority are recorded separately from earlier edits. History index link/line-budget exit 0, GREEN 23 lines. Final artifact receipt covers exact closed workflow/report inputs.
- Snapshot: HEAD 52e576c31ca654e244a25657f8e8bca9bd3c32fe; SHA256 ee706eae796c874bc68c91740fa2203b4c1316b2cc41a8d54fa65aaa68994024; paths both target packages (36 files), steering-final-manifest.txt. Uncommitted recovery depends on preserving this working tree and task evidence.

## Validation Commands

All commands run from repository root with installed Python; scripts are unchanged, so no checker self-tests. Exit 1/2 is not PASS. Static proof only. No Go application code or live provider surface is changed, so application suites and paid runtime replay are outside this verification.

| ID | Command / observer |
|---|---|
| V1 | `python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20261009-222708_go-routing-ownership.md --continuation docs/agents/20261009-222708_go-routing-ownership-state.md --profile resumable` / parent |
| V2 | `python -B scripts/validate_sohrab_skill_pack.py` / verifier |
| V3 | `python -B scripts/check_fleet_references.py --skill alaa-golang --skill alaa-code-intelligence-routing` / writer focused; cite only with exact successful receipt and unchanged inputs |
| V4 | `python -B scripts/check_skill_index.py` and `python -B scripts/check_lifecycle_contract.py` / verifier |
| V5 | `python -B skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py` / verifier |
| V6 | `python -B skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py . --files` plus exact changed Markdown paths / verifier; parent for later report/workflow-only edits |
| V7 | `git diff --check` and `git diff --cached --check`, scoped path/status and deterministic manifest inspection / writer focused, verifier combined, parent final artifacts |

Manifest: sorted repository-relative POSIX path, one space, each file SHA256 and newline; SHA256 of UTF-8 concatenation. Include all files under both product packages, including untracked additions. Freeze covered inputs during gates. Reuse only with matching inputs, observer, environment and commands; the earlier routing-upgrade gates do not cover new edits.

## Task Allocation

Source guidance: current OpenAI model selection read 2026-10-10, Sol medium for revisable coordinated technical work; Luna for bounded tasks. Installed definitions are neutral and present; explicit fresh-fork model/effort arguments are supported by this host. Serving identity and narrower enforcement remain unknown. No model comparison is being run.

| Task/scope/complexity | Role authority | Priority/reason | Model | Effort | Selection/admission evidence and source date | Invocation/requested/effective controls | Availability/limits |
|---|---|---|---|---|---|---|---|
| Bounded grounded advisory | alaa-planner | Balanced; known owners and concrete user outcome | gpt-6.1-sol | medium | Coordinated technical synthesis; 2026-10-10 | Fresh explicit pair; neutral definition | Completed read-only; observed unknown |
| Coupled instruction authoring | alaa-implementer | Balanced; preservation and ownership judgment, not mechanical replacement | gpt-6.1-sol | medium | Complete scope/acceptance and advisory; lower mechanical lane would leave semantic decisions unresolved | Fresh explicit pair; neutral definition | Available; no self-acceptance |
| Instruction contract gate | alaa-instruction-reviewer | Balanced; check complete preservation and policy boundaries | gpt-6.1-sol | medium | Bounded two-skill contract with specified intended deltas | Fresh explicit pair; neutral definition | Available; read-only, no fixes |
| Exact independent commands | alaa-verifier | Balanced; fixed commands and deterministic receipts | gpt-6-luna | medium | Mechanical scope with no design/fix authority | Fresh explicit pair; neutral definition | Available; serialized commands |

## Delegation and Sources

One writer owns the coupled rule changes. After its freeze, instruction review and cheap native verification may run concurrently; neither writes product files. Parent reviews the diff independently under lean profile. Four host slots are exposed; no overlapping writer or unrelated lane. No separate documenter: these executable instruction documents are the product and are reviewed together.

Current official authoring evidence: [OpenAI skills](https://learn.chatgpt.com/docs/build-skills), [Claude skills](https://code.claude.com/docs/en/skills), [OpenAI model guidance](https://developers.openai.com/api/docs/guides/model-selection). Common frontmatter, clear activation boundaries and conditional supporting files agree with the local authoring owner. Record detailed provenance in the task report, not copied runtime/version policy in Go.

Full planning draft: `outputs/20261010-go-routing-ownership/planning-draft.md`. The final plan is its compressed, explicitly ratified contract. Parent owns continuation; child returns facts/paths rather than a second plan.

## Blockers and Next Action

- Blockers: none. Live activation/performance remain unverified; installation/publication were not requested.
- Next action: no remaining local implementation. Deliver final management report and preserve the verified uncommitted snapshot. A9 reused the same Sol/medium writer/reviewer and Luna/medium verifier; no new agents or Go policy copies.

## Latest user steering

After the citation fix passed, the user explicitly prioritized CodeGraph where it can answer,
then Serena for its strengths, then native tools, to avoid duplicate searches and context use;
configured gopls remains a valid Go semantic fallback. This authorizes the incremental central
policy refinement A9. It is separate from the earlier native-continuation clarification, and
does not retroactively explain that earlier edit. Official CodeGraph MCP/resolution documentation
was refreshed: explore accepts known file/symbol names and returns source/paths, while heuristic
edges retain limits. No local speed or token benchmark is inferred.
