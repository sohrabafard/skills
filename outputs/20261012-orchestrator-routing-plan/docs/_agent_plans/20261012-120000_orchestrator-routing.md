# Workflow Plan - Orchestrator model routing and instruction economy

- Task ID: `20261012-120000_orchestrator-routing`
- Mode: plan
- Profile: orchestrated
- Status: planning
- Created: `2026-10-12`
- Parent plan: none
- Prompt pack: `outputs/20261012-orchestrator-routing-plan/docs/_agent_plans/20261012-120000_orchestrator-routing__phase-prompts.md`
- Checkpoint: `outputs/20261012-orchestrator-routing-plan/docs/agents/20261012-120000_orchestrator-routing-state.md`
- Machine state: `outputs/20261012-orchestrator-routing-plan/.codex/state/20261012-120000_orchestrator-routing.json`
- Base branch and commit: `main` at `6f6c82facd91779bd3bec8e5c7028b499964091e`
- Work branch: existing `main` checkout; planning files only
- Worktree: repository root `.`

## Summary and Outcome

Deliverable now: a grounded execution plan, checkpoint, explicit JSON state and a reusable Codex kickoff plus goal condition. The user requested state; the JSON is a compact machine-readable handoff, not another plan. Implementation phases below remain pending.

Future outcome: both orchestrators select the least costly suitable available model/effort for each actual task, consistently honor current-generation selection, preserve independent authority, and carry fewer redundant instructions. Policy correctness, actual allocation behavior and worker quality are separate acceptance claims.

## Scope

- Planning writes: this output directory only. Preserve existing untracked `outputs/random-test/` and `outputs/sandbox-d-access/`.
- Future source owners: `skills/sohrab/alaa-prompting-guide/`, `skills/sohrab/alaa-codex-orchestrator/`, `skills/sohrab/alaa-cc-orchestrator/`. Workflow changes are conditional on a demonstrated recording/validation gap. Root checks and documentation change only for the affected contract.
- Excluded: vendor edits, unrelated skills, application code, role-grant expansion, broad model-name replacement in history, implicit main-session reconfiguration, installation, global settings, commits, publication and paid comparison runs.
- Keep model-neutral roles. Capability support is not selection eligibility; a role's name is not a model choice. Current-generation selection means the newest verified supported member of the selected family, not replacing suitable Luna with Sol.
- Allocation is by suitability, not model-use quotas. Preserve legitimate Sol, Sonnet, Opus, Astra and Fable cases. Missing facts go to retrieval; they do not justify a stronger model.

## Grounded Findings and Source Limits

| Finding | Evidence inspected on 2026-10-12 | Consequence |
|---|---|---|
| Old Sol remains explicitly selectable | `alaa-prompting-guide/assets/codex-model-policy.json`, models.gpt-6-sol.selection_enabled = true; 6.1 Sol also true | Confirmed source defect against the user's requested active-generation policy |
| Guidance already names 6.1 Sol | `alaa-prompting-guide/references/90-model-selection.md`, S definition and source table | Fix eligibility/enforcement, not only prose model labels |
| Luna fit is narrower than Haiku fit | Both `references/routing-matrix.md`: Codex mechanical/reproduced-bug routes versus CC bounded semantic Haiku branch | Investigate unintended exclusion of bounded non-bug work; do not assume model equivalence |
| All-role comparison is already required | Both routing matrices, All-role task allocation | The repair must make the cheap-fit decision observable and hard to bypass without duplicating policy |
| Current inspected Codex agent files are neutral | 34 user `alaa-*.toml` files; zero top-level model/effort assignments; planner/reviewer source and installed contracts inspected | No evidence of an installed pin causing these symptoms on this host |
| Installed Codex skill resolves to source | User skill symbolic link target matches this checkout | A source edit still does not prove an already-loaded chat reloaded its context |
| Bodies are substantial | `baseline.json`: Codex 2,779 words; CC 2,743 words, including frontmatter | Measure both body and route-loaded references; token savings remain unmeasured |
| Prior all-role transition was source-only | `outputs/20261009-task-model-routing/report.md` | Prior static PASS does not prove current live allocation behavior |
| Three active comparison rows still use old Sol | Planner inspected `alaa-prompting-guide/assets/evals/agent-comparisons.json` lines 74, 105, 162; `scripts/task_model_controls.py` lines 17-18 rejects inactive pairs | Preserve dated comparisons separately and deliberately revise active designs before disabling eligibility |
| Existing evaluation and contract gates leave a behavioral gap | Planner inspected eight-case comparison corpora and both `scripts/check_agent_contracts.py`; several assertions match literal wording | Add routing observations and red fixtures; review checker changes required by equivalent compression |

The user's recent-chat observations are accepted as reported symptoms, not a reproduced dispatch trace. Do not invent their originating sessions. If causal attribution needs actual decisions, use a bounded selection of relevant accessible chats or supplied traces and retain only allocation metadata, not raw transcripts.

Live official sources refreshed:
- [OpenAI model selection](https://developers.openai.com/api/docs/guides/model-selection): Luna for bounded work and 6.1 Sol for complex technical work; starting guidance, not local calibration.
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents): supported dispatch controls and role configuration; current host schema separately permits 6.1 Sol/high and Luna/medium with `fork_turns=none` for overrides.
- [Claude model selection](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model): efficiency-first Haiku and capability-first alternatives.
- [Claude subagents](https://code.claude.com/docs/en/sub-agents): refresh exact model/effort realization on the Claude target before dispatch.
- [Codex goals](https://learn.chatgpt.com/use-cases/follow-goals): evidence-based bounded continuation.

No full selector asset refresh, Claude-host inspection, comparative benchmark, post-change live routing, or serving-identity verification was performed. Older local capability dates retain their limits. No Hindsight tool was exposed; recall proceeded from repository truth. The Codex memory registry quick search yielded no relevant prior routing record.

## Skill Bindings

Paths resolve from repository root. Stop the dependent task when its required source is missing; never install or substitute silently.

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-workflow | skills/sohrab/alaa-workflow/SKILL.md | state, phase, handoff decisions | always | stop workflow writes |
| alaa-codex-orchestrator | skills/sohrab/alaa-codex-orchestrator/SKILL.md | Codex allocation and lanes | Codex execution | stop Codex dispatch |
| alaa-cc-orchestrator | skills/sohrab/alaa-cc-orchestrator/SKILL.md | mirrored-contract review and Claude allocation | affected CC contract or Claude execution | stop affected work |
| alaa-prompting-guide | skills/sohrab/alaa-prompting-guide/SKILL.md | model evidence, instruction edits, compression | always | stop instruction work |
| alaa-code-intelligence-routing | skills/sohrab/alaa-code-intelligence-routing/SKILL.md | evidence-surface choice | first discovery or changed question | stop dependent retrieval |
| alaa-low-noise | skills/sohrab/alaa-low-noise/SKILL.md | broad retrieval and dispatch | always | stop broad retrieval |
| alaa-testing-strategy | skills/sohrab/alaa-testing-strategy/SKILL.md | scenario or proof design | phases 1, 3, 4 | stop test decision |
| alaa-repo-docs | skills/sohrab/alaa-repo-docs/SKILL.md | published documentation alignment | phase 4 | stop documentation lane |
| alaa-extract-agent-lessons | skills/sohrab/alaa-extract-agent-lessons/SKILL.md | final curation | phase 4 and planning handoff | stop closure |
| alaa-memory-os | skills/sohrab/alaa-memory-os/SKILL.md | prior-context recall or drift handling | prior evidence or source disagreement | recall fail-open; preserve drift in repository |

## Ordered Work

### Phase 1 - Freeze eligibility and allocation acceptance

- Status: pending
- Depends on: explicit implementation kickoff
- Reasoning and selection reason: coupled judgment about eligibility, fit and proof; missing facts must be retrieved first.
- Settled/open decisions and invariants: user rejects old Sol as normal selection; no cheap-model quotas; determine exact safe eligibility schema and bounded semantic admission without inventing quality equivalence.
- Risk and required observers: instruction-contract risk; planner/test strategist advise, parent ratifies.
- Owned scope: source inspection and acceptance records under this output directory.
- Excluded from this phase: skill changes, installations, paid comparisons.
- Required skills: alaa-workflow, alaa-codex-orchestrator, alaa-cc-orchestrator, alaa-prompting-guide, alaa-code-intelligence-routing, alaa-low-noise, alaa-testing-strategy
- Work:
  - [ ] Read each skill that will change in full, including references and scripts, and the first-party pack contract and routing index. [skills: inherit]
  - [ ] Refresh capability sources and inspect actual runtime controls; distinguish source, installed, loaded and requested/observed states. [skills: inherit]
  - [ ] Finalize the scenario matrix below, scoring fields, minimal evidence consumer and ready lanes. Preserve historical capability/comparison records. [skills: inherit]
  - [ ] Record each planned policy delta separately from wording-only compression; ratify current eligibility and low-cost fit/rejection rules. [skills: inherit]
- Acceptance criteria: finite file ownership, expected decisions, invariants, red cases and proof limits are written before source edits.
- Validation commands: read-only policy parsing, relevant checker help/source inspection, current official source reads.
- Evidence observed: pending; baseline findings above are reusable on unchanged inputs.
- Snapshot: initial `baseline.json`; capture remaining affected inputs before execution.

### Phase 2 - Repair selection and compress the mirrored contract

- Status: pending
- Depends on: Phase 1 acceptance ratification
- Reasoning and selection reason: normal-to-coupled instruction engineering; keep eligibility and mirrored routing decisions coherent.
- Settled/open decisions and invariants: one capability owner; runtime orchestrators own task choice; unchanged authority/grants and independent gates.
- Risk and required observers: independent instruction reviewer; source/checker review after integrated candidate.
- Owned scope: prompting-guide eligibility owners; paired orchestrator SKILL/routing/model-effort/delegation contracts; generated definitions only through their owners.
- Excluded from this phase: workflow policy duplication, unrelated role renames, global configuration and installed copies.
- Required skills: alaa-workflow, alaa-codex-orchestrator, alaa-cc-orchestrator, alaa-prompting-guide, alaa-code-intelligence-routing, alaa-low-noise
- Work:
  - [ ] Make old Sol unavailable for normal task selection while retaining historical evidence; require an explicit, recorded user exception for any intentional legacy use. No unavailable-6.1 fallback to old Sol. [skills: inherit]
  - [ ] Preserve the three old-Sol comparison records as dated evidence and revise active comparison designs deliberately; distinguish historical read/validation from active task-control acceptance without weakening inactive-model rejection. [skills: inherit]
  - [ ] For every task authority, evaluate cheapest suitable available pairs explicitly. Select Luna/Haiku when their recorded fit holds; otherwise record the unmet fit criterion or stronger task-specific evidence. Keep model and effort separate. [skills: inherit]
  - [ ] Permit grounded bounded semantic work where justified, including suitable retrieval, verification and documentation; do not hardwire models to role names or treat every review as frontier work. [skills: inherit]
  - [ ] Preserve direct selection without a mandatory trial ladder; check fit again only for remaining work after a material change or failure classification. [skills: inherit]
  - [ ] Separate intended routing changes from a draft-then-compress pass. Preserve triggers, exceptions, scope, force, stop/failure rules, sources and dates; review relocation as a separate design change. [skills: inherit]
  - [ ] Regenerate affected model-neutral projections from their canonical sources and inspect mirrored semantic parity. [skills: inherit]
- Acceptance criteria: cases R1-R15 have one reachable owner and decision path; cheap-fit rejection is concrete; exact model/effort are supplied at dispatch; both skill bodies shrink without mandatory route-read inflation.
- Validation commands: focused policy/contract checks in Gate Matrix, then projection check if generated artifacts changed.
- Evidence observed: not run.
- Snapshot: freeze the combined source candidate before Phase 3.

### Phase 3 - Prove controls and allocation behavior

- Status: pending
- Depends on: Phase 2 candidate and Phase 1 test design
- Reasoning and selection reason: bounded checker edits with discriminating negative tests; behavioral observation needs a separately identified target harness.
- Settled/open decisions and invariants: a schema fixture cannot prove an LLM selected correctly; no fake worker-quality measurements.
- Risk and required observers: verifier executes, independent reviewer judges; test author does not approve the tests.
- Owned scope: existing policy/contract/evaluation checkers and corpora; evidence under this output directory.
- Excluded from this phase: automatic benchmark purchases, silent absent-runtime skips, changes by verifier.
- Required skills: alaa-workflow, alaa-codex-orchestrator, alaa-cc-orchestrator, alaa-prompting-guide, alaa-code-intelligence-routing, alaa-low-noise, alaa-testing-strategy
- Work:
  - [ ] Extend existing corpus/checkers with R1-R15, explicit task model/effort, admission reason, eligibility and capability fields. Inspect consumers before selecting a new schema or script. [skills: inherit]
  - [ ] Demonstrate red controls: old Sol enabled, cheap-fit skipped without reason, unsupported effort, caller controls overridden, missing gate and model-name-derived allocation must be rejected. Use scratch fixtures; do not mutate live configuration. [skills: inherit]
  - [ ] Run one consolidated source gate set on a frozen snapshot; record coverage instead of rerunning identical child checks. [skills: inherit]
  - [ ] Observe a bounded actual allocation-only case set in each available authorized host using the changed instructions, with neutral task descriptions and expected answers held by the reviewer. Capture selected model/effort and realized controls separately. [skills: inherit]
  - [ ] Mark unavailable Claude/Codex runtime evidence blocked or unrun. Prepare its exact handoff; do not claim both runtimes work from static validation. Worker-quality/cost comparisons require separately authorized experiments. [skills: inherit]
- Acceptance criteria: deterministic controls reject plausible wrong implementations; observed routing cases match the expected class or have an independently accepted factual exception; uncertainty remains explicit.
- Validation commands: Gate Matrix; approved allocation-only probe commands/tool arguments resolved against the actual host in Phase 1.
- Evidence observed: not run; no post-change live evidence exists.
- Snapshot: command, observer, input hashes, host surface and result attached to each proof layer.

### Phase 4 - Independent review, documentation and handoff

- Status: pending
- Depends on: Phase 3 integrated evidence
- Reasoning and selection reason: independent cross-owner review, then bounded documentation alignment.
- Settled/open decisions and invariants: no source edit is an installation; future activation remains a separate authority boundary.
- Risk and required observers: instruction reviewer mandatory; correctness reviewer for checker/generated behavior; release guardian only if packaging/version/install contracts changed.
- Owned scope: reviewed fixes through original writers, affected source documentation, output report and workflow state.
- Excluded from this phase: installation, commit, publication, source-only claims of runtime success.
- Required skills: alaa-workflow, alaa-codex-orchestrator, alaa-prompting-guide, alaa-low-noise, alaa-testing-strategy, alaa-repo-docs, alaa-extract-agent-lessons
- Work:
  - [ ] Obtain independent correctness and instruction-contract verdicts; resolve blocking findings with the existing retry budget and rerun only invalidated gates. [skills: inherit]
  - [ ] Report before/after bytes, words and route-loaded instruction totals plus rule-equivalence mapping; do not translate these into unmeasured token/cost savings. [skills: inherit]
  - [ ] Align affected documentation and produce an exact proposed install/reload verification handoff, without executing it. [skills: inherit]
  - [ ] Validate workflow artifacts and cold-start next action; record curation and the four independent lifecycle verdicts through the workflow owner. [skills: inherit]
- Acceptance criteria: no unresolved blocker/major finding, required source gates pass, live status accurately separated, no unexplained touched paths, handoff can resume without this conversation.
- Validation commands: affected Gate Matrix commands and workflow validator; no broad repeat solely for final narration.
- Evidence observed: not run.
- Snapshot: final scoped content manifest; uncommitted files retain recovery risk.

## Acceptance Scenarios

Balanced priority unless an explicit case changes it. These are task-fit expectations, not empirically established model-quality rankings. Test ordinary and adversarial paraphrases without leaking the expected answer into the allocation prompt.

| ID | Task or pressure | Required observable result |
|---|---|---|
| R1 | Both old and current Sol exposed; ordinary engineering task | 6.1 Sol is the workhorse candidate; old Sol is excluded from normal allocation |
| R2 | Current Sol unavailable; old Sol available | affected lane reports unavailable; no silent legacy fallback |
| R3 | Exact transformation over finite named existing files, discriminating check | Luna / Haiku selected; file count alone does not escalate |
| R4 | Reproduced local bug, traced cause, bounded repair and regression oracle | Luna / Haiku fit evaluated positively; effort justified separately |
| R5 | Small semantic non-bug edit, settled pattern and explicit invariants | evaluate low-cost route without requiring mechanical-only work; record any failed predicate |
| R6 | Bounded extraction, known-command verification or source-backed doc alignment | cheap pair considered regardless of authority-role title; output complete and bounded |
| R7 | Cross-boundary trust/consistency decision or conflicting evidence unresolved | retrieve missing facts; workhorse/frontier only with recorded reasoning/admission; no cheap-model quota |
| R8 | Independent reviewer with substantial cross-owner semantics | retain independent authority and choose from task complexity; diversity alone causes no escalation |
| R9 | Role name contains luna/haiku/astra/opus; or parent uses high effort | neither role label nor parent controls chooses child pair |
| R10 | Stale pin, force override, missing effort or unsupported effort | exact verified realization or affected-lane block; no prose-only configuration claim |
| R11 | Lane grows beyond fit, tool failure, interruption or completed work | classify cause, preserve valid edits and reallocate remaining scope only; no replay/trial ladder |
| R12 | Compression removes a gate, weakens must, drops exception or breaks router | instruction review/checker rejects it; permitted runtime/polarity differences remain |
| R13 | Read historical old-Sol comparison after active disablement | dated evidence remains readable/validatable; cannot authorize a new ordinary allocation |
| R14 | High-quality priority or many files but bounded fit unchanged | effort/priority do not waive fit, and volume alone does not force a stronger model |
| R15 | Astra/Fable selected for ordinary work without admission evidence | reject unexplained escalation; preserve justified exceptional selection |

An explicit legacy-model request is a separately recorded exception, not normal availability. A successful source fixture demonstrates checker discrimination, not end-to-end routing. Runtime routing demonstrates selection on the sampled cases, not universal worker suitability.

## Compression Acceptance

Use `baseline.json` and a rule inventory before changing instructions. Soft design target: reduce each orchestrator body by about 20%, if behavior-preserving compression permits it. Hard acceptance: both bodies measurably smaller, packaged description and reference gates pass, no lost contract, no hidden transfer of mandatory words into always-read references. If the target conflicts with a load-bearing rule, preserve the rule and report the achieved size and reason.

Measure bytes and whitespace words for body, routing matrix, control/delegation references, selected role contract, and representative mandatory read paths. Use the same measurement algorithm before and after. Model-specific token counts are optional only with an available compatible tokenizer. The independent reviewer compares the intended semantic delta first, then checks wording-only equivalence against that new contract.

## Task Allocation

Recommendations are dated 2026-10-12 and must be revalidated before future dispatch. Balanced priority applies to all rows. Models below are for the actual tasks, never role defaults. No paid comparison is required to allocate.

| Task/scope/complexity | Role authority | Priority/reason | Model | Effort | Selection/admission evidence and source date | Invocation/requested/effective controls | Availability/limits |
|---|---|---|---|---|---|---|---|
| Current advisory plan: coupled policy/proof/wording | alaa-planner-high | balanced; interacting contracts | gpt-6.1-sol | high | current host and OpenAI guidance, 2026-10-12; Luna lacks justified fit for this coupled design; Astra unnecessary | spawn_agent, fork none, explicit pair; neutral installed/source definition | dispatched; serving identity unknown |
| Current plan/prompt review: coupled instructions | alaa-instruction-reviewer | balanced; authority and cold-start correctness | gpt-6.1-sol | high | same capability evidence; cross-owner review exceeds bounded extraction | spawn_agent, fork none, explicit pair; neutral definition | dispatched and approved after focused repair; serving identity unknown |
| Phase 1 acceptance design | alaa-test-strategist | balanced; reject superficially green proof | gpt-6.1-sol | high | interacting source/live/compression oracles | explicit pair on revalidated host | future, unrun |
| Phase 2 eligibility + paired instruction contract | alaa-implementer-high | balanced; coupled ownership and exceptions | gpt-6.1-sol | high | coordinated technical artifact; cheap decomposition loses shared decisions | explicit pair on revalidated host | future, unrun |
| Phase 3 bounded checker edits after frozen schema | alaa-implementer-low | balanced; known local contracts and oracle | gpt-6.1-sol | low | provisional bounded semantic route; reassess Luna after scope/fit is settled | explicit pair; no role-derived setting | future; reclassification required if complexity differs |
| Phase 3 exact verification commands | alaa-verifier | balanced; bounded execution with exact result contract | gpt-6-luna | medium | finite commands and evidence extraction; diagnosis returned to owner | explicit pair; preserve verifier authority | host advertises pair; future controls rechecked |
| Phase 4 integrated correctness and instruction review | alaa-reviewer and alaa-instruction-reviewer, separate authority | balanced; cross-owner correctness | gpt-6.1-sol | high | meaningful semantic judgment, not second-lens model escalation | separate scopes and contexts, each explicit pair | future, unrun |
| Phase 4 verified doc alignment | alaa-documenter | balanced; finite source-backed edits | gpt-6-luna | medium | known claims/files and link checks; ambiguity returns to parent | explicit pair; no architecture decisions | future, unrun |

Claude scenario expectations target Haiku 5.5, Sonnet 5.5, Opus 5.5 and Fable 5.1 as named by the user and current sources. Exact Claude runtime IDs/efforts remain a Phase 1 host preflight, not a fabricated runnable configuration from Codex.

## Delegation

- Dependency edges: P1 -> P2 -> P3 -> P4. Scenario design and missing official evidence may run independently inside P1. Evidence documentation follows the verdict barrier.
- Ready now: plan/prompt review only; no implementation authorization in the current request.
- Future ready sets: after P1, one policy/paired-contract writer; after schema freeze, a checker writer may proceed on disjoint scripts/corpus while contract writer finishes prose. Serialize shared policy/schema, generators and integrated checks.
- Consolidation: mirrored contract and its compression stay in one lane because they share decisions; independent review and verification stay separate because authority differs.
- Parent owns artifacts/integration. No concurrent writers to policy, common fixtures or generated targets. Freeze all tested inputs during independent gates.
- Reuse unchanged evidence only for matching inputs and observer. Recheck actual host controls on each dispatch. Four available current slots are a host observation, not durable scheduling policy.

## Gate Matrix

All paths below are repository-relative; run each row from its stated directory. This is a future gate inventory, not a claim those commands ran. Inspect aggregate coverage first and cite identical covered children. Exit 1/2 fails the affected gate. CPU-heavy commands use the owning resource policy and explicit worker caps; ordinary Python static checks run bounded and sequentially.

| Working directory | Commands / trigger |
|---|---|
| skills/sohrab/alaa-prompting-guide | `python scripts/check_codex_model_policy.py --agent-root ../alaa-codex-orchestrator/agents --agent-root assets/rule-writer/codex` |
| skills/sohrab/alaa-prompting-guide | `python scripts/check_claude_model_policy.py`; `python scripts/check_agent_evals.py`; `python scripts/check_claude_agent_evals.py` |
| skills/sohrab/alaa-codex-orchestrator | `python scripts/check_agent_contracts.py`; `python scripts/render_agents.py --check`; `python scripts/validate_pack.py`; `python scripts/check_agent_grants.py` |
| skills/sohrab/alaa-cc-orchestrator | `python scripts/check_agent_contracts.py`; `python scripts/validate_pack.py`; `python scripts/check_agent_grants.py` |
| Changed checker's owning skill | same checker with `--self-test`; changed projection engine: `python scripts/profile_projection.py --self-test` from prompting-guide |
| Changed generated definitions | owning `python scripts/render_agents.py --write`, then `--check`; generation is implementation, never verifier mutation |
| Repository root | `python scripts/validate_sohrab_skill_pack.py`; `python scripts/check_skill_index.py`; `python scripts/check_fleet_references.py`; `python scripts/check_lifecycle_contract.py`; `git diff --check` |
| Repository root | `python skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan outputs/20261012-orchestrator-routing-plan/docs/_agent_plans/20261012-120000_orchestrator-routing.md` |

Runtime acceptance uses actual exposed tools/CLI only after verified capability and authority; no speculative command is committed here. If a new offline allocation-result validator is necessary, its command and red fixtures become an explicit Phase 1 decision and Phase 3 gate. Do not confuse a linter recognizing required phrases with an execution test of allocation.

## Handoff Package

- Confirmed facts (verified, each with how it was verified): findings and source limits above; baseline content/size identities in `baseline.json`. User explicitly wants latest Sol plus better low-cost fit, and asks for planning before implementation.
- Open assumptions (believed but unverified, each with what would verify it): specific historical dispatch causes need bounded trace evidence; changed routing needs actual host observation; comparative worker quality requires a separately authorized experiment.
- Ruled out (approach, reason, evidence): global find/replace of old model names erases legitimate history; pinning models to roles reverses current all-role task ownership; quotas manufacture cheap-model usage; static PASS cannot establish runtime behavior.
- Read first on resume (ordered exact paths): this plan and its prompt pack; its checkpoint; `skills/sohrab/alaa-prompting-guide/assets/codex-model-policy.json`; then the current phase's source owners and bindings.
- Environment notes (command shapes that work here, and ones that look right but fail): Python 3.14 executable available. `rg` on Windows uses directory plus `-g 'alaa-*.toml'`, not a wildcard in a literal path. Initializer ran from this output directory to cluster its standard family; companion references were expanded to repository-relative paths. Web reader rejected the Markdown content type for the subagents `.md` URL; HTML source worked. Existing native goal already existed; no second goal was created.
- Traps (looks correct, is not): `selection_enabled: true` admits old Sol despite newer prose; neutral role metadata still permits an arbitrary task choice; support in the schema is not serving identity; symlink freshness is not current-chat reload; word reduction is not measured savings. Do not mark the future implementation phases complete when this planning request completes.

## Planning Evidence and Handoff Status

- Planning artifact validator: repaired-then-pass (exit 0). Independent instruction review: APPROVED after one scoped R1-R15 coverage correction. See `outputs/20261012-orchestrator-routing-plan/validation.md` for final tested identity and limits.
- Compression pass: final plan and prompts consolidate scope, sources, six role fields and one scenario matrix; no duplicated implementation checklist in JSON/checkpoint. Intended future routing changes are explicitly distinct from wording-only compression.
- Curation: user correction retained in this plan as a scoped promotion candidate for the existing routing/policy owners; no memory write authorized or performed. Obvious repository facts need no new durable memory copy.
- Lifecycle for the requested skill repair: IMPLEMENTED not requested in this turn; MERGE_CANDIDATE not established; RELEASE_CANDIDATE and PUBLISHED not requested.

## Blockers and Next Action

- Planning blockers: none. Planning deliverables are ready; future implementation phases remain pending.
- Future proof limit: full two-runtime correctness cannot be claimed without the missing actual runtime evidence. Missing access/authority blocks that proof claim, not independent local source work.
- Next action: after the user submits the prepared implementation kickoff, read this plan, reconcile checkout and baseline, then execute Phase 1. Do not begin implementation from the current planning request.
