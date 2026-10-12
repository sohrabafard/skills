# Workflow Plan - Orchestrator model routing and instruction economy

- Task ID: `20261012-120000_orchestrator-routing`
- Mode: execution
- Profile: orchestrated
- Status: complete
- Created: `2026-10-12`
- Parent plan: none
- Prompt pack: `outputs/20261012-orchestrator-routing-plan/docs/_agent_plans/20261012-120000_orchestrator-routing__phase-prompts.md`
- Checkpoint: `outputs/20261012-orchestrator-routing-plan/docs/agents/20261012-120000_orchestrator-routing-state.md`
- Machine state: `outputs/20261012-orchestrator-routing-plan/.codex/state/20261012-120000_orchestrator-routing.json`
- Base branch and commit: `main` at `6f6c82facd91779bd3bec8e5c7028b499964091e`
- Work branch: existing `main` checkout; authorized local implementation, no commits
- Worktree: repository root `.`

## Summary and Outcome

Execution adopted on 2026-10-12 after the user supplied the kickoff and goal condition. The earlier planning-only authority statements below are dated history. Authorized local phases are complete at goal evaluation 1: source gates, independent reviews, available Codex allocation observations, documentation and curation are recorded. Blocked CLI/Claude proof remains explicit with exact next actions. The lead owned allocation, state, reconciliation and gates; implementation stayed in owning lanes. No external effects were authorized.

## Execution Preflight

- Current checkout: `main`, HEAD `9086158d204e8015f7fd0c1e66f83f710bc0dfac`, repository root `.`; initially clean. Compared with the planning HEAD, only this planning family and unrelated `outputs/random-test/` and `outputs/sandbox-d-access/` changed. Every file hash in `baseline.json` still matches. Preserve that historical baseline.
- Execution profile: standard. Coupled policy/instruction work requires separate verification, correctness review and instruction review; no irreversible/high-blast-radius trigger is present. Reassess packaging/release and other specialist triggers from actual changes.
- Evidence routing: native reads/parsers for named Markdown/JSON/TOML, Git diff for scope, native checkers for proof. Structural Python questions route through the code-intelligence owner before discovery. No integration configuration changes.
- Capability refresh: official [Codex custom-agent controls](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents) and [model-selection guidance](https://learn.chatgpt.com/docs/model-selection#how-to-think-about-models-and-reasoning-effort) fetched on 2026-10-12. Explicit spawn model/effort precede global/parent defaults unless a custom role pins them. Current tool schema supports `gpt-6.1-sol/high`, `gpt-6.1-sol/low`, and `gpt-6-luna/medium` with `fork_turns=none`.
- Installed preflight: test strategist, implementer-high/low, verifier, reviewer, instruction reviewer, documenter and researcher are present, have no model/effort pins, and their instruction bodies match source. Installed/source version is 5.3.0. No project-role override was found. User config has Astra/high as main settings; these are not child task allocation and do not prove this session's serving identity.
- Permission evidence: parent managed policy is workspace-write with auto-review. Role read-only declarations restrict behavior but do not prove enforcement. Installed definitions carry template markers and no materialized MCP tables; inherited grants/isolation are not verified. No installation is authorized or performed. Lanes must use only their scoped operations; no claim of enforced MCP isolation is made.
- Phase 1 task controls: retain `alaa-test-strategist`, `gpt-6.1-sol/high`, balanced. Coupled source/runtime/compression oracle design has unresolved consumer/schema decisions, so the bounded extraction/Luna fit is not established; decomposition would split shared acceptance decisions. No exceptional model is needed. Supply both controls explicitly with fresh context; report serving identity unknown unless observed.
- Memory: registry lookup found no relevant prior routing record; no Hindsight tool is exposed. Resume uses repository plan/history without memory recall evidence or writes.
- Python 3.14, Git and ripgrep are available. No source validation has run yet. A mistyped PowerShell numeric read argument was corrected once; it changed no files.
- Detailed observed preflight and source links: `outputs/20261012-orchestrator-routing-plan/execution-preflight.md`. Phase 1 strategist spawn accepted with the selected pair; observed serving identity is unknown. Workflow artifact validator reported no blocking errors after execution adoption.

Planning delivered this plan, checkpoint, JSON state and kickoff. Execution now follows the phase evidence below; the JSON remains a compact handoff rather than another plan.

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

### Acceptance ratification - 2026-10-12

Acceptance strategist `/root/acceptance_design` returned `pass-with-actions` after scoped native inspection. No test or runtime experiment ran in that lane. Parent ratifies these decisions:

- Keep capability policy schema 2. Set `gpt-6-sol.selection_enabled` false, retaining its supported-effort history. Ordinary task-control validation remains fail-closed; an intentional user legacy exception is recorded separately and never restores ordinary eligibility.
- Preserve the original comparison corpus and corresponding original policy as dated historical-only files under `alaa-prompting-guide/assets/evals/history/20261009/`, with a manifest of provenance and hashes. Historical validation is an explicit separate path, never accepted by ordinary task selection. Revise the three active unrun old-Sol designs deliberately; do not create identical candidate/comparator pairs by renaming.
- R5 cheap semantic admission: explicit outcome, finite named scope, grounded local contracts, known pattern or causal path, settled cross-boundary decisions, bounded local discretion, and a discriminating check. A reproduced bug is not required for non-bug work. Apply fit to every authority role. Select the cheapest supported available suitable pair, with model and effort justified separately; record the actual failed fit predicate or stronger task-specific evidence when rejecting it. No quotas, automatic trial ladder, frontier-by-title or old-Sol fallback.
- Separate intended policy deltas from wording-only compression. Keep the baseline rule inventory and per-rule equivalence mapping; measure both bodies and representative complete mandatory read paths using raw bytes and whitespace words. Any relocation needs its own reason/review. Preserve every gate, exception, authority limit and force.
- New allocation-only evidence has separate neutral inputs and reviewer oracle, distinct from worker-quality comparisons. Use a finite R1-R15 corpus including role/priority/volume paraphrases. Results identify case/runtime/run, input/loaded-contract hashes, selected pair, fit/admission/rejection evidence, alternatives, status/blocker, requested/effective/observed controls, independent verdict and forbidden effects; unobservable counters stay unknown. Synthetic host/control records prove only the validator/scenario response, not actual availability or resolution. Two fresh runs per available authorized allocator configuration; no worker-quality or paid model comparison.
- Extend existing consumers before introducing a new one. A single new `scripts/check_allocation_evals.py` plus `assets/evals/allocation-cases.json` and `allocation-oracle.json` is admitted for the distinct allocation evidence consumer. Define/document its precise flags and red fixtures before independent execution. Static fixture PASS never establishes allocator compliance.
- Phase 2 policy/prose lane owns prompting-guide `assets/codex-model-policy.json`, `references/90-model-selection.md`, `references/92-agent-evaluation.md`; both orchestrators' `SKILL.md`, `references/routing-matrix.md`, `references/model-effort-policy.md`; evidence only under this task's `policy-lane/`. No other source changes without parent reconciliation.
- Phase 3 checker lane owns prompting-guide `scripts/check_codex_model_policy.py`, `scripts/check_agent_evals.py`, `assets/evals/agent-comparisons.json`, the three historical archive files, the new allocation checker/case/oracle files; both orchestrators' `scripts/check_agent_contracts.py`; evidence only under this task's `checker-lane/`. It may propose a narrowly necessary shared consumer edit; do not silently expand ownership. Archive originals from HEAD, never a concurrently edited policy.
- Both writers complete their affected-skill full-read requirement before edits and report it. They share the frozen schema/acceptance above but no writable files. Checker work may proceed while prose is written; final prose-sensitive fixture alignment waits for the policy writer. Generators, versions, installers, grants, workflow source and unrelated files are excluded.
- Checker allocation reassessed to `alaa-implementer-high`, `gpt-6.1-sol/high`, balanced: archival versus active validation, a new allocation evidence consumer, and semantic compression controls interact; this is not the provisional bounded local checker edit from planning. Luna and Sol-low fit are not established for those remaining coupled decisions. No frontier admission. Policy/prose remains `alaa-implementer-high`, `gpt-6.1-sol/high`; independent verifier and bounded verified-documentation tasks retain planned Luna/medium after controls refresh.
- Independent gate coverage: each `validate_pack.py` covers generated drift/grants and only part of contract checking. Retain the full `check_agent_contracts.py` for each runtime. CC aggregate checks its agent-root policy, not rule-writer; Codex aggregate does not cover rule-writer either. Run canonical full-root policy checks separately. Changed checker self-tests and the new allocation/archive checks are additional gates.
- Phase 1 remaining obligation: writer full-source reads and precise allocation CLI/schema documentation. Source edits proceed only after those read requirements in their own scopes. Live post-change observation, actual child realization, worker quality and cost savings remain distinct pending/unrun claims.

Both writers subsequently reported complete affected-skill body/reference/executable-script reads before source edits, with lane inventories. Identical mirrored contents were reused where recorded. The checker identified two additional owning consumers: `alaa-prompting-guide/scripts/codex_model_policy.py` and `scripts/task_model_controls.py`. Parent ratifies those two files solely for ordinary/archive boundary enforcement and discriminating self-tests: an original historical policy must not re-enable old Sol through an ordinary public API. Explicit historical validation has no active-dispatch authority. The documented user legacy exception stays separate; any new executable exception interface requires an explicit decision, never an implicit bypass. This shared-consumer scope retains the coupled Sol 6.1/high allocation. Precise allocation CLI/schema documentation remains the checker lane's next prerequisite for independent execution.

Dispatch roster: `acceptance_design` completed, requested Sol 6.1/high, configured neutral, observed unknown; `policy_contract` and `routing_checks` next, each requested Sol 6.1/high with fresh context and explicit controls. All use bounded role authority; unmaterialized MCP isolation remains unverified.

### Phase 1 - Freeze eligibility and allocation acceptance

- Status: complete
- Depends on: explicit implementation kickoff
- Reasoning and selection reason: coupled judgment about eligibility, fit and proof; missing facts must be retrieved first.
- Settled/open decisions and invariants: user rejects old Sol as normal selection; no cheap-model quotas; determine exact safe eligibility schema and bounded semantic admission without inventing quality equivalence.
- Risk and required observers: instruction-contract risk; planner/test strategist advise, parent ratifies.
- Owned scope: source inspection and acceptance records under this output directory.
- Excluded from this phase: skill changes, installations, paid comparisons.
- Required skills: alaa-workflow, alaa-codex-orchestrator, alaa-cc-orchestrator, alaa-prompting-guide, alaa-code-intelligence-routing, alaa-low-noise, alaa-testing-strategy
- Work:
  - [x] Read each skill that will change in full, including references and scripts, and the first-party pack contract and routing index. [skills: inherit]
  - [x] Refresh capability sources and inspect actual runtime controls; distinguish source, installed, loaded and requested/observed states. [skills: inherit]
  - [x] Finalize the scenario matrix below, scoring fields, minimal evidence consumer and ready lanes. Preserve historical capability/comparison records. [skills: inherit]
  - [x] Record each planned policy delta separately from wording-only compression; ratify current eligibility and low-cost fit/rejection rules. [skills: inherit]
- Acceptance criteria: finite file ownership, expected decisions, invariants, red cases and proof limits are written before source edits.
- Validation commands: read-only policy parsing, relevant checker help/source inspection, current official source reads.
- Evidence observed: acceptance strategist ratified, official capability/control refresh and installed neutral definitions inspected, separate allocation interface/corpus/oracle frozen before consumer implementation. See execution-preflight.md and checker-lane/allocation-interface.md.
- Snapshot: HEAD 9086158d204e8015f7fd0c1e66f83f710bc0dfac; SHA256 b8f6a94284bca455e02f1268397975db6919f6657f1c3bdfb642914752f6de3f; paths execution-baseline.json, the original pre-edit source manifest. Historical baseline.json remains preserved.

### Phase 2 - Repair selection and compress the mirrored contract

- Status: complete
- Depends on: Phase 1 acceptance ratification
- Reasoning and selection reason: normal-to-coupled instruction engineering; keep eligibility and mirrored routing decisions coherent.
- Settled/open decisions and invariants: one capability owner; runtime orchestrators own task choice; unchanged authority/grants and independent gates.
- Risk and required observers: independent instruction reviewer; source/checker review after integrated candidate.
- Owned scope: prompting-guide eligibility owners; paired orchestrator SKILL/routing/model-effort/delegation contracts; generated definitions only through their owners.
- Excluded from this phase: workflow policy duplication, unrelated role renames, global configuration and installed copies.
- Required skills: alaa-workflow, alaa-codex-orchestrator, alaa-cc-orchestrator, alaa-prompting-guide, alaa-code-intelligence-routing, alaa-low-noise
- Work:
  - [x] Make old Sol unavailable for normal task selection while retaining historical evidence; require an explicit, recorded user exception for any intentional legacy use. No unavailable-6.1 fallback to old Sol. [skills: inherit]
  - [x] Preserve the three old-Sol comparison records as dated evidence and revise active comparison designs deliberately; distinguish historical read/validation from active task-control acceptance without weakening inactive-model rejection. [skills: inherit]
  - [x] For every task authority, evaluate cheapest suitable available pairs explicitly. Select Luna/Haiku when their recorded fit holds; otherwise record the unmet fit criterion or stronger task-specific evidence. Keep model and effort separate. [skills: inherit]
  - [x] Permit grounded bounded semantic work where justified, including suitable retrieval, verification and documentation; do not hardwire models to role names or treat every review as frontier work. [skills: inherit]
  - [x] Preserve direct selection without a mandatory trial ladder; check fit again only for remaining work after a material change or failure classification. [skills: inherit]
  - [x] Separate intended routing changes from a draft-then-compress pass. Preserve triggers, exceptions, scope, force, stop/failure rules, sources and dates; review relocation as a separate design change. [skills: inherit]
  - [x] Inspect mirrored semantic parity and projection drift. No role/projection source changed, so regeneration was not triggered; independent pack gates checked generated drift. [skills: inherit]
- Acceptance criteria: cases R1-R15 have one reachable owner and decision path; cheap-fit rejection is concrete; exact model/effort are supplied at dispatch; both skill bodies shrink without mandatory route-read inflation.
- Validation commands: focused policy/contract checks in Gate Matrix, then projection check if generated artifacts changed.
- Evidence observed: instruction-review.md APPROVED, correctness-review.md APPROVED after one fix cycle; both bodies and all ten representative mandatory routes shrink. Conditional evaluation-interface growth is measured separately.
- Snapshot: HEAD 9086158d204e8015f7fd0c1e66f83f710bc0dfac; SHA256 d1546d4ea18a917471c7925319e2f89f81d3b3026a5ed2881018c05da9c663ec; paths policy-lane/source-snapshot.json, the eleven-file policy manifest. Compression measurements remain in size-and-read-paths.json.

### Phase 3 - Prove controls and allocation behavior

- Status: complete
- Depends on: Phase 2 candidate and Phase 1 test design
- Reasoning and selection reason: bounded checker edits with discriminating negative tests; behavioral observation needs a separately identified target harness.
- Settled/open decisions and invariants: a schema fixture cannot prove an LLM selected correctly; no fake worker-quality measurements.
- Risk and required observers: verifier executes, independent reviewer judges; test author does not approve the tests.
- Owned scope: existing policy/contract/evaluation checkers and corpora; evidence under this output directory.
- Excluded from this phase: automatic benchmark purchases, silent absent-runtime skips, changes by verifier.
- Required skills: alaa-workflow, alaa-codex-orchestrator, alaa-cc-orchestrator, alaa-prompting-guide, alaa-code-intelligence-routing, alaa-low-noise, alaa-testing-strategy
- Work:
  - [x] Extend existing corpus/checkers with R1-R15, explicit task model/effort, admission reason, eligibility and capability fields. Inspect consumers before selecting a new schema or script. [skills: inherit]
  - [x] Demonstrate red controls: old Sol enabled, cheap-fit skipped without reason, unsupported effort, caller controls overridden, missing gate and model-name-derived allocation must be rejected. Use scratch fixtures; do not mutate live configuration. [skills: inherit]
  - [x] Run one consolidated source gate set on a frozen snapshot; record coverage instead of rerunning identical child checks. [skills: inherit]
  - [x] Observe a bounded actual allocation-only case set in each available authorized host using the changed instructions, with neutral task descriptions and expected answers held by the reviewer. Capture selected model/effort and realized controls separately. [skills: inherit]
  - [x] Mark unavailable Claude/Codex runtime evidence blocked or unrun. Prepare its exact handoff; do not claim both runtimes work from static validation. Worker-quality/cost comparisons require separately authorized experiments. [skills: inherit]
- Acceptance criteria: deterministic controls reject plausible wrong implementations; observed routing cases match the expected class or have an independently accepted factual exception; uncertainty remains explicit.
- Validation commands: Gate Matrix; approved allocation-only probe commands/tool arguments resolved against the actual host in Phase 1.
- Evidence observed: source gates and both source review repairs passed; final source pin and original capture preservation verified. Two fresh v2 collaboration repetitions yield sixty reviewed records, 240 passing semantic criteria and strict oracle 53 passed/seven failed with independently accepted factual exceptions. The assembled evidence passed --require-live after one preserved configuration-ID metadata correction. CLI matrix remains blocked/unrun with exact next actions; no worker-quality inference is made. See final reconciliation and runtime-review.md.
- Snapshot: HEAD 9086158d204e8015f7fd0c1e66f83f710bc0dfac; SHA256 562dd5ff9e92c9d5cde385614f602f7804b7aad6f2ab54d2d0ae8ad1d6753aab; paths verification/probe-v2/source-pin-refreshed.json, the final 541-file source manifest. Capture hashes are in runtime/reviewer-v2-verdict.json.

### Phase 4 - Independent review, documentation and handoff

- Status: complete
- Depends on: Phase 3 integrated evidence
- Reasoning and selection reason: independent cross-owner review, then bounded documentation alignment.
- Settled/open decisions and invariants: no source edit is an installation; future activation remains a separate authority boundary.
- Risk and required observers: instruction reviewer mandatory; correctness reviewer for checker/generated behavior; release guardian only if packaging/version/install contracts changed.
- Owned scope: reviewed fixes through original writers, affected source documentation, output report and workflow state.
- Excluded from this phase: installation, commit, publication, source-only claims of runtime success.
- Required skills: alaa-workflow, alaa-codex-orchestrator, alaa-prompting-guide, alaa-low-noise, alaa-testing-strategy, alaa-repo-docs, alaa-extract-agent-lessons
- Work:
  - [x] Obtain independent correctness and instruction-contract verdicts; resolve blocking findings with the existing retry budget and rerun only invalidated gates. [skills: inherit]
  - [x] Report before/after bytes, words and route-loaded instruction totals plus rule-equivalence mapping; do not translate these into unmeasured token/cost savings. [skills: inherit]
  - [x] Align affected documentation and produce an exact proposed install/reload verification handoff, without executing it. [skills: inherit]
  - [x] Validate workflow artifacts and cold-start next action; record curation and the four independent lifecycle verdicts through the workflow owner. [skills: inherit]
- Acceptance criteria: no unresolved blocker/major finding, required source gates pass, live status accurately separated, no unexplained touched paths, handoff can resume without this conversation.
- Validation commands: affected Gate Matrix commands and workflow validator; no broad repeat solely for final narration.
- Evidence observed: source correctness and instruction review APPROVED; runtime review APPROVED-WITH-NITS with seven accepted exceptions retaining failed strict statuses. Both bodies and ten representative mandatory routes are smaller. Independent documentation links/grades, workflow/diff retries, closure-manifest hashes and scope audit passed; curation has no novel candidate. Final completion metadata receives its own bounded workflow/diff check. See final reconciliation.
- Snapshot: HEAD 9086158d204e8015f7fd0c1e66f83f710bc0dfac; SHA256 8063abf29c29dc8c858083e26d56c45c2364c44de8de3544222ad4028075e823; paths closure-manifest.json, the document/review/matrix/source-pin manifest. Active workflow metadata is validated separately; uncommitted recovery risk remains.

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

The following table preserves the planning recommendations. Actual execution uses the ratifications above and this roster: acceptance_design/test-strategist, policy_contract/implementer-high, routing_checks/implementer-high, instruction_gate/instruction-reviewer and correctness_gate/reviewer each requested `gpt-6.1-sol/high`; source_verifier/verifier and documentation/documenter each requested `gpt-6-luna/medium`. All seven installed role definitions were neutral and explicit spawn controls were accepted; observed serving identity and enforced MCP isolation remain unknown. Followups reuse the same lane rather than count as new dispatches. Documentation is finite verified-source alignment with exact file/link/size checks, so bounded Luna fit holds; uncertainty returns to the parent. No frontier or main-session identity is inferred.

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
- Ready now: Phase 1 acceptance design and capability refresh under the implementation kickoff; source writers wait for parent ratification.
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

## Historical Planning Evidence and Handoff Status

- Planning artifact validator: repaired-then-pass (exit 0). Independent instruction review: APPROVED after one scoped R1-R15 coverage correction. See `outputs/20261012-orchestrator-routing-plan/validation.md` for final tested identity and limits.
- Compression pass: final plan and prompts consolidate scope, sources, six role fields and one scenario matrix; no duplicated implementation checklist in JSON/checkpoint. Intended future routing changes are explicitly distinct from wording-only compression.
- Curation: user correction retained in this plan as a scoped promotion candidate for the existing routing/policy owners; no memory write authorized or performed. Obvious repository facts need no new durable memory copy.
- Lifecycle for the requested skill repair: IMPLEMENTED not requested in this turn; MERGE_CANDIDATE not established; RELEASE_CANDIDATE and PUBLISHED not requested.

## Historical Planning Blockers and Next Action

- Planning blockers: none. Planning deliverables are ready; future implementation phases remain pending.
- Future proof limit: full two-runtime correctness cannot be claimed without the missing actual runtime evidence. Missing access/authority blocks that proof claim, not independent local source work.
- Next action: execute Phase 1 acceptance design, ratify schema/ownership and live-probe evidence boundaries, then dispatch the coupled Phase 2 writer. Refresh exact controls before every dispatch.

## Execution scope addendum

Parent authorizes prompting-guide SKILL.md and references/00-topic-map.md solely to expose the new allocation checker exact command, exit behavior and reference router. This is an intended discoverability addition, measured separately from orchestrator compression. The policy lane owns these two paths and coordinates flags with the checker lane. No second reference router or relocated obligation is authorized.

## Earlier Execution Observations (Chronological Evidence)

- Instruction gate dispatched as `/root/instruction_gate`, `alaa-instruction-reviewer`, requested `gpt-6.1-sol/high`, balanced. Cross-owner exception/authority/compression judgment does not establish bounded Luna fit; no frontier admission. Refreshed installed definition is neutral, explicit request accepted, serving identity and enforced MCP isolation unknown. Authority is bounded native read-only inspection.
- Writer corrected UTF-8 decoding damage confined to two routing matrices, before source gate execution. The checker interface's required role field was aligned in reference 92; reviewer invalidated the stale read and refreshed it.
- Writer then identified six compression fidelity issues in paired bodies. Parent authorized one coherent repair preserving the original advisor-decision timing, exclusive role verbs, blocked reporting, identical aggregate invocation, explicit goal/scope ownership and specialist-only trigger language. Instruction gate holds its final verdict until the new identity is frozen. No source acceptance pass is claimed yet.
- Codex CLI 0.160.0 help/version returned successfully with access-denied warnings for user-home temporary aliases. This is a preflight warning, not a proven inference blocker. No recovery, settings change or inference has been attempted. Claude allocation-only safe-mode proposal remains separate from unproven child-effort realization on 2.1.286.
- Independent instruction verdict is APPROVED on the eleven-file candidate; exact inspected scope and limits are in `instruction-review.md`. A subsequent matrix newline-preservation repair changes bytes only and requires refreshed identity reconciliation, not an invented semantic pass.
- Checker source/data are frozen. Its focused checks passed after two preserved repairs: an allocation self-test guard accessed missing synthetic evidence before rejecting live mode (exit 2), and a Codex contract red fixture matched metadata too broadly (exit 1). Each cause received one scoped repair and a passing retry. `checker-lane/focused-results.jsonl` retains both failures; independent acceptance is still pending.
- Integrated verifier allocation: `alaa-verifier`, `gpt-6-luna/medium`, balanced. Explicit finite commands, settled inputs, bounded artifact writes and discriminating exit/results meet cheap fit; no diagnosis, semantic discretion, repair or broader task. Exact commands/limits live in `verification-dispatch.md`. Refreshed installed verifier and reviewer definitions match source and omit both executable controls; actual serving identity and MCP isolation remain unknown.

## Final Execution Reconciliation

The earlier planning and chronological sections are dated evidence. Current source identity is `verification/probe-v2/source-pin-refreshed.json` (541 files); the final checker SHA-256 is `f64494abc128bdc7e2cb25dbd9cbfc3dbb16c28340cd4a513145314f4112b268`. Policy and checker snapshots identify the original eleven/thirteen source paths; later pin deltas identify the two coordinated review repairs. Source remains uncommitted on execution HEAD `9086158d204e8015f7fd0c1e66f83f710bc0dfac`.

Source evidence: sixteen independent initial commands, three archive followups, four correctness-fix followups, the ordinary active-corpus check, and three probe-parity followups passed on their identified inputs. The original blocked CLI matrix passed ordinary structural validation separately. Source correctness and instruction review are APPROVED; runtime observation review is APPROVED-WITH-NITS. Earlier failures and cause-specific repairs remain recorded, not recast as clean initial passes.

Two fresh v2 Codex collaboration captures cover sixty records. All response contracts and 240 semantic criteria pass independent review. Strict oracle results remain 53 passed and seven failed. The reviewer independently accepted all seven factual exceptions; the parent ratifies them under this plan's explicit exception clause. `runtime-review.md` and `runtime/reviewer-v2-verdict.json` own the precise cases, source facts and limits. No raw record or oracle was normalized. The original two captures exposed a probe/consumer mismatch and remain diagnostic only; a new pinned neutral schema fixed that defect without changing consumer semantics, scenario facts or the oracle.

CLI evidence stays separate: initial Codex startup access denied, one environment retry timed out at 600 seconds with no final answer, Claude returned expired-OAuth 401 before inference. Second CLI repetitions were unrun. Exact immediate Claude action is user-run `claude auth login`; after authentication use the v2 request/current manifests, not the old helper's hardcoded v1 paths. Codex CLI readiness needs host diagnosis of the preserved startup/timeout records before any new authorized retry. Windows denied process-ownership inspection; descendant state remains unknown and no broad cleanup occurred. Serving identity, installed activation, full tool-trace audit, child controls, worker quality, cost and savings remain unproven.

Final dispatch roster: eleven agents, six distinct authority roles. The original seven are recorded above; `allocation_capture_1`, `allocation_capture_2`, `allocation_v2_1`, and `allocation_v2_2` each used `alaa-implementer-high`, explicit `gpt-6.1-sol/high`, balanced, fresh context. Each pair of captures was sequential and oracle-blind. Coupled routing/authority judgment did not meet bounded extraction fit; no frontier model was admitted. Installed role controls were refreshed, neutral and source-identical. All observed serving identities remain unknown; followups are not new dispatches. Main identity and input/output token counts are not observable. No authorized commit exists for a completion-span measurement.

Documentation: `outputs/README.md`, `execution-report.md` and `runtime-proof-handoff.md` are independently GREEN at 24, 23 and 27 physical lines. Independent links, scope, evidence hashes and workflow/diff retries passed; the initial narrative-heading/snapshot/EOF findings remain recorded. Final completion metadata is checked separately. The scope audit found 24 authorized source paths, 274 task-output paths including the navigation index, 31 owned retired read batches and zero outside-scope changes. API/data/events/Postman/localized docs are inapplicable to this skill-only change. No installation, global setting, commit, publication or paid model comparison occurred.

Curation final gate scanned user judgments, two source review cycles, compression findings, CLI failures and captured allocation exceptions. The user decisions now live in their canonical policy/routing owners; no competing memory copy is needed. Probe parity and control/evidence separation are already represented by source contracts and tests. Authentication, permission and capture-helper incidents are volatile task evidence, not durable doctrine. No novel candidate passes admission; no memory note or deferred promotion was created, and no pipeline reopening remains.

Lifecycle: IMPLEMENTED proven by focused and independent source evidence on the identified uncommitted snapshot, with uncommitted recovery risk. MERGE_CANDIDATE not proven because full two-runtime/CLI evidence remains unavailable. RELEASE_CANDIDATE and PUBLISHED were not requested. Local requested completion does not imply either blocked proof or external authority.

Cold-start handoff: read this reconciliation, the checkpoint, `runtime-proof-handoff.md`, `runtime-review.md` and the final verification records. Preserve all source/capture identities. Resume only the named blocked proof after the relevant host state/authority changes; do not rerun completed source work or reinterpret accepted exceptions as universal model-quality evidence.
