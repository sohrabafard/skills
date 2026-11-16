# Lane returns

Final reports of the Phase 1 lanes, as returned. Model output, dated 2026-11-16.

## L4 — alaa-code-intelligence-routing and alaa-low-noise

STATUS: COMPLETE. Lane L4 compressed `alaa-code-intelligence-routing` and `alaa-low-noise`. Each rule now has one owner, provenance is separate from run-time rules, and all six gates exit 0. The reduction is modest, because most of this text already carries a rule (see item 3).

1. Metadata: AGENT alaa-implementer-sonnet-high. CONFIGURED: unknown (no definition file read). REQUESTED: claude-opus-5-5 at medium effort. OBSERVED: the runtime reports model claude-opus-5-5; effort is unknown. Skills loaded before the first edit: /alaa-prompting-guide (and its 60-skill-authoring sections), /alaa-ponytail full, plus the preloaded /alaa-code-intelligence-routing, /alaa-testing-strategy, /alaa-services-contract and /alaa-trust-gateway-auth.
2. Branch `worktree-agent-ae19ba799f515098e`, worktree `agent-ae19ba799f515098e`. Commits:
   - 54156b40 refactor(alaa-code-intelligence-routing): give each operation-card rule one owner
   - ce641c74 refactor(alaa-low-noise): give search, slice and capture rules one owner
   - 435f9ce7 docs(alaa-code-intelligence-routing): compress references without rule changes
   - 35482b34 docs(alaa-low-noise): compress body and references without rule changes
3. Words (from measure.py; frontmatter / body / references / total):
   - Code-intelligence routing: before 105/753/9273/10178, after 105/753/8963/9868 (-3%).
   - Low-noise: before 77/965/1604/2675, after 77/960/1371/2437 (-9%).
   - Neither `SKILL.md` frontmatter nor the operation card rows changed, so criterion 4 holds by identity. The code-intelligence body is preloaded into 31 agents and cited by its card; I changed it not at all. The mapping report shows little history or duplication in these two skills. The rest is rule-bearing text.
4. Relocations (no file retired; nothing moved to `_to_delete`):
   - Read with a line range, `sed` only through the shell, reuse graph source: removed from 45. The card owns them.
   - Lane-local `init`/`sync` grant: 40 keeps a one-clause pointer to the card, so it does not contradict the card.
   - `LSP` tool choice, position from the query result, Codex uses the CLI: removed from 40. The card owns them. 40 keeps the limits the card does not state: reads only, session-root workspace, check that returned paths are in your worktree, the tools-list reachability rule.
   - Heuristic edges and provider order: removed from 40. 10 owns them (40 "Other source" now points there).
   - "Pointer, not a copied table" (stated three times in 70): one statement now, in the preamble of 70.
   - Low-noise discovery order, the "avoid by default" list, the report shape and the capture steps: removed from noise-control-patterns, which keeps the commands and a pointer to `SKILL.md` *Part 1*. "Stop at the first step that answers" and "summarize the result, not the material" moved into the body.
   - The ownership sentences in model-output-profiles and workflow-integration now point at the body. "Universal behavioral guarantees" moved into the body's *Model calibration*.
   - The two bulky-output statements in the low-noise body are now one rule that keeps both reasons.
5. Checker literals changed: 0. No clause checker binds these files.
6. Left for Phase 2, rules also stated in another skill: the reasons in mapping section 7 still hold. Low-noise `SKILL.md` lines 23, 47, 51 and 33 overlap the orchestrators' delegation-prompts, PG 43 and testing 110. Its workflow-integration return contract overlaps both orchestrator `SKILL.md` files, and its polarity rule overlaps PG 06. Code-intelligence 80 (read-only MCP) overlaps PG 80 and PG 11.
7. Rules that make an agent recheck or retry: code-intelligence 10:44 (one repair, one retry), 10:74, 45:13 (rerun only on change), 50:13 (recheck the reminder conflict per version), 80:30, 90:3 and 90:14. Low-noise SKILL:30 (re-read only for a new reason), SKILL:48 and 90-source-map:17.
8. Rules that look wrong or stale:
   - Code-intelligence `50-hooks.md:48` says to change "the checker together", but no such checker exists in the repo. Left verbatim.
   - Low-noise `90-source-map.md:12` uses the Codex skills URL `developers.openai.com/codex/skills/`, which PG 00-source-map calls stale. Left as is.
   - Low-noise 90-source-map carries no verification dates; I added none.
9. Gates, run from the worktree root with PYTHONDONTWRITEBYTECODE=1: `validate_sohrab_skill_pack`, `check_skill_index`, `check_fleet_references` and `check_lifecycle_contract` each exited 0, and so did `check_agent_grants.py` in both orchestrators. Criterion 3: grep finds `## Operation card` once (SKILL.md:18) and `## Delegated lanes` once (workflow-integration.md:20).
   - Dispatch conflict: committing per change class needs a gated tree, so the gates ran three times (after the relocate pass, after the compress pass, and after a final edit to 75) instead of once. Every run exited 0.

Not run: any other suite; this lane needs no tests. Independent review is pending at the final boundary. Not committed: nothing; the tree is clean.

## L3 — alaa-workflow

STATUS: COMPLETE — `alaa-workflow` was compressed with its behaviour, every cited heading, every checker-bound clause, every template token and every dated provenance line preserved; all seven gates exit 0, but the measured reduction is small (3.3%) because most of the text is rule-dense or bound by a checker.

AGENT: lane L3 implementer; CONFIGURED: unknown (no definition file observed); REQUESTED: `claude-opus-5-5` / medium; OBSERVED: model `claude-opus-5-5` (from the runtime environment); effort unknown.

1. **Commits.** Branch `worktree-agent-af12345c75b181eca`, worktree `agent-af12345c75b181eca`.
   - `7b63e9b8` docs(alaa-workflow): compress skill text without behaviour change
   - `8ba6bb11` docs(alaa-workflow): restore narrowed triggers and tighten remaining prose. This repairs three trigger regressions from the first commit: the resume pointer in Start step 2, the plain-resume router trigger, and the "after all checks pass" gate on root registration. It also reverts asset edits that saved no words.

2. **Words (measure.py).**
   - Before: 19449 total (body 1116, references 16389, assets 1800).
   - After: 18814 total (body 1104, references 15766, assets 1800).
   - Why so little:
     - `workspace-and-integration.md` is mostly sentences bound by the `workspace` checker.
     - The `task-tracking.md` capability table and its sections are rule-dense; each row is a separate decision.
     - Assets are rendered by the scripts, so only a few words were free to cut.

3. **Moves.** All are within one file, so all are class 1. Class 2 moves: none.
   - Failed heartbeat, then ping, then outage: merged the old Outage-section paragraph into `task-tracking.md` `## Agent identity and ownership`; the Outage section now points there.
   - Exit-13 re-read and "never retry blindly": the identity guard paragraph now owns it, and the capability row keeps only the mechanics.
   - Resume protocol: three pointers in `SKILL.md` became one rule under `## Survive compaction and handoff` plus the Start step 2 pointer.
   - Cadence owner: two pointers became one, which now also names independent observers.
   - `artifact-lifecycle.md`: *Permitted contents*, *Update events*, *Resume and handoff* and *Delegation* merged into `## Contents, updates, resume and delegation`. Every trigger survives, and nothing outside the file cited those headings.
   - Dispatch wall: stated once in `context-continuity.md` `## Delegation is a context boundary`; the four-ways bullet now points there.
   - Retired files: none.

4. **Checker literals changed:** 0. No tuple lost a clause. `context-continuity.md` line 121 and every `workspace` and `COLLECTION_SEAMS` sentence are verbatim. Asset `{{token}}` lines were not touched (the diff contains 0 token lines).

5. **Left for Phase 2.**
   - Checker-bound sentences: all Appendix B sentences, unchanged.
   - Not deduplicated:
     - "A design plan is always local" (`task-tracking.md:19` and `artifact-lifecycle.md:19`): not identical, because task-tracking adds the no-reason and outside-the-test clauses.
     - `companion-routing.md` core-companion bullets versus `SKILL.md` Start steps 3–5: the reference adds detail, and the body rule must stay loaded.
   - Rules also stated in other skills: as in mapping section 4.
     - Never weaken assertions (`SKILL.md` Execute).
     - Lane commit and checkpoint rules (w&i versus both `verification-and-gates.md`).
     - Command, result and the one line that mattered (`context-continuity.md`, `alaa-low-noise`).
     - Ample context (`context-continuity.md` *After compaction*, `alaa-prompting-guide` 40-fable-5).

6. **Re-review, re-test or re-confirm rules (listed, not changed).**
   - `task-tracking.md:84`: repeat registration checks on resume and after a material change.
   - `task-tracking.md:53, 172, 177`: recheck bd help after an upgrade.
   - `context-continuity.md:123`: recheck mapped skill availability.
   - `context-continuity.md:131`: repeat the resume protocol after compaction.
   - `workspace-and-integration.md:83`: rerun the affected gates after a base integration.
   - `context-curation.md:36`: rerun every affected gate after a pipeline reopen.
   - `artifact-lifecycle.md:58`: run the validator before handoff and before completion.
   - `assets/phase-prompts-template.md:15`: re-check source evidence before use.

7. **Rules that look wrong or stale (listed only).**
   - The `task-tracking.md:53` provenance cites bd 1.3.1, while `:33` cites bd 1.3.2 observed 2026-11-14. The two version stamps sit side by side and were not reconciled.
   - `bd formula list` "no formula on 2026-11-02" and `external_projects` "unset on 2026-11-02" are dated observations that may be stale.

8. **Gates** (worktree root, `PYTHONDONTWRITEBYTECODE=1 python3 -B`): `validate_sohrab_skill_pack` 0, `check_skill_index` 0, `check_fleet_references` 0, `check_lifecycle_contract` 0. `alaa-testing-strategy check_execution_contracts` 0. cc `check_agent_contracts` 0. codex `check_agent_contracts` 0.

Skills loaded before the first edit: `/alaa-prompting-guide` (with `references/60-skill-authoring.md`), `/alaa-ponytail` at level full, `/alaa-low-noise`; the routing and testing skills were preloaded.

Not run, as excluded: `init_workflow_files.py` and `validate_workflow_files.py`. Asset safety therefore rests on reading their regexes. The only asset edits were reverted, so no asset changed in net.

Acceptance criteria 4 and 5: all 14 Appendix A headings return one hit each, and no heading was renamed.

Boundary conflicts: none.

## L2 — alaa-testing-strategy

STATUS: COMPLETE. Lane L2 compressed `alaa-testing-strategy` and gave each repeated rule one owner. All gates exit 0. The reduction is moderate (about 15%), not large, because no checker literal was reworded.

AGENT: alaa-implementer-sonnet-high. CONFIGURED model/effort: unknown (not observable). REQUESTED: claude-opus-5-5 (opus) at medium effort. OBSERVED: model claude-opus-5-5 from the runtime environment; effort unknown.

1. Outcome. Every always-apply rule has one compressed statement in `SKILL.md`. The body routes through `references/00-topic-map.md`. References 10 to 90 no longer restate body rules. The design step list keeps one pointer per step and no restated rule.

2. Branch `worktree-agent-a0d1f951f3f2d3946`, worktree `agent-a0d1f951f3f2d3946`.
- fda42de9 refactor(alaa-testing-strategy): give each repeated testing rule one owner
- c9dc5100 docs(alaa-testing-strategy): compress body, references and metadata
- 051b32b8 fix(alaa-testing-strategy): restore rules lost in compression

The fix commit restores four items the compression had dropped:
- the always-loaded ban on suppressing findings and altering fixtures;
- the no-reset exception in `90` *Setup once*;
- the `30` cleanup pointer to `90`;
- the clear timeout message in `50`.

Every commit was made by path. `git status` is clean. Only owned paths changed. `check_execution_contracts.py` has no diff.

3. Words (`measure.py`, before → after):
- frontmatter 112 → 104;
- body 3986 → 3412;
- references 14635 → 12406;
- other 240 → 211;
- total 18973 → 16133 (-15%).

Most of the remaining body is checker-bound or required content: the tier table and validity text, the output contract and the 15 non-negotiables. References 100, 110 and 120 are almost entirely checker literals, so they were only trimmed.

4. Relocations (rule: old site → owner, pointer site):
- Effect-absence list: `10` assertion rules → `SKILL.md` core rule. The body line now also names files, credentials and messages.
- Happy-path job: `10` section → `70` *Ordering*. Design step 9 now points to `70`.
- Step-2 break examples: `SKILL.md` → `10` catalogue, behind a pointer.
- Consumer-tests-instead text and unreachable examples: `SKILL.md` → `90` *Candidates that are not owed a test*, behind a triggered pointer.
- Triplication discriminator: one copy, kept in the body because it applies on every run and a pointer cost as many words. `20` keeps only which test survives. The pointers in `10`, `20` and `90` go to `SKILL.md` *The core rule*.
- Substitution reasons: `30` → non-negotiable 3. `30` keeps only the examples.
- Unreachable-level procedure: `40` → `80` *When a test cannot be run at all*.
- Flake-by-construction list in `50`: replaced by pointers to non-negotiable 11 and `90` *Setup once*. Seeded randomness and the clear timeout message stay in `50`.
- `10` *Anti-patterns*: every item kept, with its reason replaced by a pointer to the owning file.
- Preambles that restated the router or a body rule were removed from 10 to 120.
- `00-topic-map.md`: the `90` row gains "write or review a test over shared infrastructure" and the `70` row gains "write its happy path".
- No file was retired.

5. Checker literals changed: 0 in every tuple. Clause counts match baseline: REQUIREMENTS 213, NORMATIVE_DUPLICATES 105, CONTRADICTIONS 19. The hash is unchanged. Appendix A headings, the `90` heading and the `100` section names are verbatim.

6. Left for Phase 2:
- `100` and `120` still restate the concealment and unrun-check rules beside the body's lines. The checker binds them to those files, so they stay.
- Most of `110` and `120`, and the 27 doctrine clauses in `SKILL.md`, can shrink only together with their literals.
- Restated in other skills: the tier definitions in both `verification-and-gates.md`, and the "never weaken assertions" line in workflow `SKILL.md`.

7. Rules that cause re-review, re-test or re-confirmation (listed only):
- `80-evidence-and-reporting.md:33`: a reviewer may demand one re-run.
- `100-test-execution.md:13`: confirm selection before citing a result.
- `100-test-execution.md:23`: rerun failed or invalidated checks.
- `SKILL.md:114`: re-run every result downstream of a changed condition.

8. Looks contradictory (listed, not changed): `50-flake.md:32` treats an unclassifiable flake as a product defect, while the `SKILL.md:179` stop condition says to report blocked.

9. Gates, each exit 0 (`PYTHONDONTWRITEBYTECODE=1`, `-B`):
- `validate_sohrab_skill_pack`: 0 (warning: body is 192 lines);
- `check_skill_index`: 0;
- `check_fleet_references`: 0;
- `check_lifecycle_contract`: 0;
- `check_execution_contracts`: 0;
- `check_agent_contracts` for cc and codex: 0 each.

Skills loaded before the first edit: /alaa-prompting-guide (with `60-skill-authoring.md`), /alaa-ponytail full, /alaa-low-noise, and the preloaded /alaa-code-intelligence-routing, /alaa-services-contract and /alaa-trust-gateway-auth. /alaa-workflow *Lane branches and commits* was read late, after the first two commits. All three commits comply with it. /alaa-testing-strategy was the text under edit, not doctrine applied to this lane.

Residual risk: no independent review has run yet; it is pending at the final boundary. The review-only acceptance criterion 5 was checked by hand: every non-negotiable, stop condition and output field is still in `SKILL.md`.

## L5a — orchestrator pair, SKILL.md and references

STATUS: COMPLETE. Lane L5a is done: `SKILL.md` and `references/**` of both orchestrator packs are compressed in identical terms, with each repeated rule given one owner, and every gate exits 0. The reduction is small, about 4.5% of reference words in cc and 3.7% in codex.

Metadata: AGENT alaa-implementer-sonnet-high (lane L5a). CONFIGURED model and effort: unknown. REQUESTED: `claude-opus-5-5` (`opus`) at `medium`. OBSERVED: the model is claude-opus-5-5 according to the runtime system context; effort was not observable.

1. **Branch:** `worktree-agent-aa0d3616432fb65d3`, worktree `agent-aa0d3616432fb65d3`.
   - `06ed7919` docs(orchestrators): compress SKILL.md and references of the mirrored pair (compress class)
   - `9ee00ad5` docs(orchestrators): give each repeated pair rule one owner file (relocate class; the body gives the reason for each move)
2. **Words, from `measure.py`** (before → after):

   | Pack | `SKILL.md` body | references |
   |---|---|---|
   | cc | 2564 → 2521 | 14370 → 13693 |
   | codex | 2554 → 2512 | 14757 → 14218 |

   - The cap is the checker-pinned prose. About 250 literals bind whole sentences, mostly in gates, routing and `SKILL.md`. I changed no literal, so those sentences stay verbatim. Going much further needs Phase 2 rewording of literals together with the checkers.
   - The XML templates under `delegation-prompts/` were already terse and carry literals and regexes. I left them unchanged except `30-implementation.md`.
3. **Relocations** (owner ← old site; the old site keeps a pointer, or the always-loaded body carries the rule):
   - `SKILL.md` §9 ← gates *Final success criteria* bullets: diff scope, documentation, reusable context, integration. §9 took the stronger wording; the gates list now points at §9.
   - `SKILL.md` *Dispatch discipline* ← routing intro "one agent per lane".
   - `SKILL.md` *Plan and allocation* ← routing's "planning effort is not worker effort" line and its "worker selection needs no planner dispatch" line.
   - `model-effort-policy.md` ← routing step 6 default and omission sentences.
   - routing *All-role task allocation* ← model-effort-policy rules: legacy IDs, second lens, review-depth pair, "model choice changes no tools", capacity diagnosis, reassessment. The policy intro now names each of these.
   - `SKILL.md` §8 and routing ← catalog intro install and legacy-ID sentences.
   - `delegation-prompts.md` read-back rule ← cc `30-implementation.md` pair-passing sentence. The codex template gained the same pointer.
   - Inside each file I also merged repeats: install authority, testing-strategy pointers, never-fall-back and diagnose-capacity in `SKILL.md`; the scattered role-ID statements in routing.
   - No file was retired.
4. **Checker literals:** none changed in either `check_agent_contracts.py`. Every tuple count equals the baseline (cc IMPLEMENTER 17, codex 16, and so on).
   - Clauses also required in L5b files that stay verbatim in mine: "model choice changes no authority"; the Task controls, Effective authority and metadata substrings; "Commit only on the lane branch your dispatch names".
5. **Left for Phase 2:**
   - Bound by a checker outside my scope, kept verbatim: `COLLECTION_SEAMS` and `COLLECTION_CONTRADICTIONS` text, and the testing-strategy pointers in `SKILL.md`, gates, `resource-policy.md` and `failure-taxonomy.md`.
   - Restating another skill, compressed in place only:
     - alaa-workflow: gates lane-commit bullets, gates `task-tracking.md` restatements (no replacement Beads database, `REVIEW_PENDING`), the `--sandbox`/`--readonly` sentence in `delegation-prompts.md`.
     - alaa-prompting-guide: `SKILL.md` concurrency-limit paragraph; model-effort-policy alias-only, 2.1.292 precedence and Fable advisor paragraphs.
     - alaa-low-noise: `SKILL.md` §2 and §3 return rules.
     - alaa-code-intelligence-routing: catalog LSP/Serena paragraph.
     - alaa-testing-strategy: the `<doctrine>` in `20-design.md`.
6. **Rules that make an agent re-review, re-test or re-confirm** (cc lines; codex mirrors them):
   - `verification-and-gates.md`:
     - :50 — a fix on a floor surface returns to that floor's gate.
     - :171 — re-apply After a fix on a blocking result.
     - :173 — re-check the final Git status and diff.
     - :174 — audit every claim against a tool result.
     - :178 — rerun the final gates if the base advanced.
   - `delegation-prompts.md`:28 — read back each invocation.
   - `routing-matrix.md`:99 — the lane rechecks the admission predicates.
   - `40-verification.md`:20 — one identical rerun for flake detection.
7. **Rules that look stale or wrong** (left unchanged):
   - codex `installation.md` keeps the "Version 5" and "Version 4" migration notes. They are history-dated, and the rules in them are restated in routing.
   - `README-fa.md` says 4.0.0; that file belongs to L5b.
8. **Gate exits:** each command in criteria 1–3 exited 0 on the committed state. That is 4 root gates, 4 per pack, and `check_execution_contracts.py`.
   - Criterion 5: identical files stay identical. 10, 30 and 50 keep only 2–4 differing lines. Gates differs only by the codex `.git` paragraph, the `AGENTS.md` guidance line, the Docker routing line and the reviewer-deep line.
   - Criterion 6: Appendix A headings are intact.
   - Not run: `render_agents.py --write`, which belongs to L5b.

Boundary conflicts: none. The scratchpad is shared with another session, which overwrote my first `gates.sh`. My scripts there now use the `l5a_` prefix.

## L5b — orchestrator pair, contract assets and agents

STATUS: COMPLETE. Both packs' contract assets, hand-written agents, stack bindings and wrapper description tails are compressed and the generated wrappers are re-rendered. Every assigned gate exits 0. The reduction is modest (about 5–7%), not the "far fewer words" the goal asked for.
AGENT: alaa-implementer-sonnet-high. CONFIGURED: none (the role is model-neutral). REQUESTED: claude-opus-5-5, medium. OBSERVED: claude-opus-5-5 (system prompt); effort unknown.

1. **Outcome:** same as the STATUS line, and behaviour is unchanged by the walk-through. Most bodies are lists in which each item is a rule, and the contract's Verification section is almost all checker literal, so little can be cut without dropping a rule.

2. **Branch and commits:** branch `worktree-agent-a2f9b95f003d9d1f8`, worktree `agent-a2f9b95f003d9d1f8`.
   - `83b5e655` refactor(orchestrators): compress contract assets and agent definitions
   - `4c72f765` fix(orchestrators): restore control and read-only clauses lost in compression

   Both commits cover both packs and are class 1 only.

3. **Words (`measure.py`), baseline to now:**

| Pack | Assets | Hand-written agents | Generated agents | Source total |
|---|---|---|---|---|
| cc | 4270 → 4096 | 13324 → 12430 | 19091 → 18096 | 34657 → 33589 |
| codex | 4977 → 4770 | 12270 → 11556 | 23862 → 22673 | 35267 → 34346 |

   The implementation contract went from 1438 to about 1350 words.

4. **Relocations and retirements:** no files were retired and no rule moved between files. Two in-file pointers:
   - In 9 VERDICT agents per pack, the output item "NOT ASSESSED: each part of the declared scope you did not inspect, and why" now reads "NOT ASSESSED, as the Return protocol defines it". The Return protocol in the same file states that content.
   - An attempt to merge the contract's testing-strategy lines widened a design-only rule to every lane. It was reverted in `4c72f765`.

5. **Checker literals:** one literal changed one-to-one in both `check_agent_contracts.py` files, inside the inline 16-item `agent_failures` tuple, which stays at 16. "including defaults normalized under" became "resolve an omitted field through". Every module-level tuple count equals `baseline.md` in both checkers. No other literal changed.

6. **Left for Phase 2 (verbatim in my files):**
   - The seven `specialist_cadence_failures` shared clauses in `agents/alaa-architecture-critic` (L5a's templates require them too).
   - The `RUN_ECONOMY` `verifier_agent` and `implementation_contract` clauses (checked across both packs).
   - The `## Lane branches and commits` citation.
   - The operation-card line.

7. **Rules that make an agent re-review, re-test or re-confirm (listed only, none changed):**
   - architecture-critic Evaluate bullet: re-check the plan's existing-infrastructure answers through /alaa-memory-os.
   - explorer and researcher: verify every memory hit or material claim against current sources.
   - reviewer: "Report every issue… including uncertain and low-severity ones".
   - implementation contract: "After editing, inspect the full diff and callers."

8. **Rules that look wrong, stale or contradictory (listed only):**
   - Pre-existing divergences between the packs:
     - the verifier's "never diagnose" bullets;
     - the reviewer's filtering and adversarial-lens bullets;
     - the instruction-reviewer's authority sentence;
     - the architecture-critic's "preloaded" versus "when installed";
     - the test-strategist's codex-only "Doctrine:" line;
     - descriptions of adversarial-reviewer, api-contract-reviewer, dependency-auditor, documenter and spec-analyst (only escaping differs for spec-analyst).
   - Codex-only lines in hand-written agents and the planner contract, which I treat as runtime mechanics: "Start no subagent" and the shell-access line.
   - The critic cites "verification-and-gates.md Phase A step 4", but the mapping report lists that file's sections as Stage A to F, so the citation is possibly stale.
   - Move 4: I trimmed only the repeated wrapper tails. The hand-written descriptions held no repeated or decorative words worth cutting. The code-graph line is unchanged.
   - Dispatch conflict: the required changelog sentence says "checker literals updated one-to-one". It is true, but only one literal changed, and each entry says so.

9. **Gates (final run, `PYTHONDONTWRITEBYTECODE=1`, `python3 -B`), all exit 0:**
   - Repository root: `validate_sohrab_skill_pack.py`, `check_skill_index.py`, `check_fleet_references.py`, `check_lifecycle_contract.py`.
   - Each pack: `render_agents.py --write`, `render_agents.py --check`, `validate_pack.py`, `check_agent_contracts.py`, `check_agent_grants.py`.
   - `alaa-prompting-guide`: `check_claude_model_policy.py`, `check_codex_model_policy.py --agent-root assets/rule-writer/codex`.
   - No `__pycache__` was created and the tree is clean.
   - Review-only checks: every output-contract item count is unchanged, and only the `description` frontmatter of the generated wrappers changed.
   - Not run: install scripts. The pair-parity diff shows only the existing hunks. Independent review is pending at the final boundary.

Skills loaded before the first edit: /alaa-prompting-guide (60 and 80 read), /alaa-ponytail full, /alaa-low-noise. /alaa-code-intelligence-routing, /alaa-testing-strategy, /alaa-services-contract and /alaa-trust-gateway-auth were preloaded. Scratch tooling is in `/tmp/claude-1000/-home-sohrab-project-skills/75ecedca-09c9-4d1a-998e-2f75020937a5/scratchpad/l5b/`, with sources in `src/`, and `build.py`, `tool.py` and `wrappers.py`.

## L1 — alaa-prompting-guide

STATUS: COMPLETE. Lane L1 is done. `alaa-prompting-guide` retired its six superseded model files and its dated refresh log, gave each repeated rule one owner, and was compressed. Every gate in criteria 1 to 3 exits 0.
AGENT alaa-implementer-sonnet-high; CONFIGURED unknown (none observable in a definition); REQUESTED claude-opus-5-5 / medium; OBSERVED model claude-opus-5-5 (from the system prompt), effort unknown.

1. **Outcome.** The six retired files hold 7,801 words. The surviving text was compressed too, but unevenly (see item 3).
2. **Branch, worktree and commits.** Branch `worktree-agent-a43dd3681f6f3868e`, worktree `agent-a43dd3681f6f3868e`.
   - 0c22acae refactor: retire superseded model references (class 2)
   - 8701b080 refactor: give each repeated rule one owner (class 2)
   - 6bddb6ac docs: cut vendor restatement in the runtime references (41 and 11, owner-approved; this also compresses them)
   - dd87d3ab docs: compress the skill text (class 1). It also holds two moves inside a file: the Opus unattended-completion rule (21) and the Haiku admission paragraph (36).
   - bee4a45a docs: tighten model references and put the SKILL.md body back as it was (class 1)
   - 05bdc23c docs: restore clauses lost in the compress passes (class 1 repair)
   - Correction to the 6bddb6ac message: its key-term grep ran before the cuts, on about 15 terms. A wider grep after the cuts found no citation outside the skill (05bdc23c records it).
   - Correction to the dd87d3ab message: its "nothing removed" claim was true only after the 05bdc23c repairs. My final sentence-level check found no further loss, but it is a self-check, not a review.
3. **Word counts (measure.py).**
   - Before: frontmatter 89, body 797, references 36,913, assets 4,507, total 42,355.
   - After: frontmatter 89, body 790, references 25,947, assets 4,452, total 31,327 (−26%).
   - Most of the cut is the retired files. The surviving references fell about 11%.
   - 06, 12, 43 and 90 changed by less than 5%. 43 is left almost as it was because it is the reference the carry-over review judges against.
   - 60, 61 and 50 grew slightly because they became owners of relocated rules. 31 and 36 also grew slightly, because their pointers are longer than the copies they replaced.
4. **Relocations (rule: old sites → owner; pointers left at the old sites).**
   - Artifact test, now with the script option: 80 and 70 → 60.
   - Wording failure modes: 70 → 60. The owner gained two exceptions: a bare prohibition for a genuine boundary, and no reason needed when the rationale is obvious.
   - Allocation ownership: 12, 31, 36 and 43 → 90.
   - Focused checks: 12, 21 and 31 → 80.
   - Observed identity: 11 and 41 → 80.
   - Codex TOML directories and keys: 11 → 80.
   - Codex skill discovery, install default, listing load and `allow_implicit_invocation`: 11 → 61.
   - Codex AGENTS.md chain: 11 → 70.
   - Per-surface default effort, minimum Code version and alias: 41 and 90 → each current model file.
   - When to raise effort: 21 and 31 → 50.
   - Haiku 4.5 effort rule: 35 → 50.
   - Legacy-model request: 12 and the topic map now point to 90.
   - Retired with sizes unchanged: 10-gpt-5-6 14642, 20-opus-5 12410, 30-sonnet-5 10134, 35-haiku-4-5 1325, 40-fable-5 13764, 42-fable-5-1 3358. New file `_to_delete/20261116-core-skills-compression/alaa-prompting-guide/00-source-map-refresh-log.md` (4873 bytes).
   - Not moved, with reasons:
     - The 41 and 11 managed-roles sections and the 41 goal-evidence sentence stay because they are on the keep-list.
     - The 43 safeguard sentence stays because merging it with 41 would widen 41's narrower scope ("to complete a gate").
     - The ownership lines in 50 step 2 and in the 80 task-control text stay as short pointers.
5. **Checker literals changed:** none. The clause checkers bind no text in this skill. G5 holds: both wrappers embed `contract.md` verbatim.
6. **Left for Phase 2:**
   - `skills/sohrab/AGENTS.md` "The wording test" restates the six failure modes that 60 owns.
   - Both repository rules that cite 60 and 41 are unchanged.
7. **Re-review and re-test rules (not changed):**
   - 60:151 requires a new stated reason for each further fix or review round.
   - SKILL.md:57 and 80:45 allow removing a repeated check only when no input changed.
   - 06:73 says unlimited fresh adversarial passes may never converge.
   - contract.md:23 requires the rewriter to walk every cut and restore.
8. **Stale or contradictory (not changed):**
   - 70:30 and 70:36 say the tail is dropped, but 11:80 says the outermost files are dropped. Left verbatim.
   - The Claude frontmatter lists in 80:15 and 41:87 differ. Left verbatim.
   - 60:21 says "Write all three parts" above four items.
   - 90:17 says "defaults refreshed", but the defaults now live in the model files.
   - Retired 35:3 cites a "legacy-replacement rule" that the policy JSON notes do not contain.
9. **Gates (worktree root, `PYTHONDONTWRITEBYTECODE=1 python3 -B`):**
   - validate_sohrab_skill_pack 0, check_skill_index 0, check_fleet_references 0, check_lifecycle_contract 0.
   - In the skill directory: check_rule_writer_grants 0, check_claude_model_policy 0, check_codex_model_policy --agent-root assets/rule-writer/codex 0.
   - cc and codex orchestrators: render_agents --check 0 and validate_pack 0 for each.
   - Criterion 4: a grep of `skills/` finds no retired file name.
   - Criterion 5: the excluded section of 60 is byte-identical to fc9da127.
   - No `__pycache__` directory was created, and the tree is clean.
   - Not run: any other suite. Criterion 6 (Appendix A and C presence) was checked by grep only and is still pending independent review.

## L4b — second pass, alaa-code-intelligence-routing and alaa-low-noise

STATUS: COMPLETE — both skills are rewritten under the second-pass brief, 57 pruned rules are in the ledger, and all six gates exit 0 on the committed tree; the routing skill ends at 80 percent of its start, not "far fewer".
AGENT alaa-implementer-fable; CONFIGURED unknown (definition file not read); REQUESTED claude-fable-5-2 / high; OBSERVED model claude-fable-5-2 (runtime statement), effort unknown.
Skills: loaded before the first edit: /alaa-prompting-guide (60-skill-authoring, *ASD-STE100 style* and *The wording is the mechanism*), /alaa-ponytail full; preloaded /alaa-code-intelligence-routing, /alaa-testing-strategy, /alaa-services-contract, /alaa-trust-gateway-auth. Read testing-strategy `100-test-execution.md` before the gates and workflow `## Lane branches and commits` before the commits (after the ff merge the brief names). 110 and 120 were not triggered.

2. Branch `worktree-agent-ae759aa886871fd05`, worktree `agent-ae759aa886871fd05`, base `37ce87a4` (ff merge confirmed). Tree clean.
   - `bb6c3a3a` refactor(alaa-code-intelligence-routing): rewrite and prune the skill around the operation card
   - `c91e5899` refactor(alaa-low-noise): rewrite and prune the skill, record the L4b ledger
3. Words (measure.py; frontmatter / body / references / other / total):
   - routing: before 105/753/8963/47/9868, after 105/712/7056/47/7920 (-20%).
   - low-noise: before 77/960/1371/29/2437, after 77/714/964/29/1784 (-27%).
4. Files above four fifths, and why:
   - routing `SKILL.md` body 95%: the eight card rows are verbatim (about 265 of 753 words); the rest is the four card-safety rules, the lane-local index grant, authority limits and stop conditions.
   - `80-agent-scoping.md` 97%: owner of grant scoping and read-only MCP enforcement; every sentence is an authority limit.
   - `90-source-map.md` 93%: sources, dates, pinned SHAs, versions and the two local observations.
   - `50-hooks.md` 85%: the deviation register with its figures, the adoption order, rollback and permission rules.
   - `75-serena-repl.md` 87%: the YAML profile, the 2026-11-15 probe and API-filter semantics. `70-project-bindings.md` 85%: two fixed fragments and setup-authority limits.
   - `20` 91% and `30` 89%: small provider-ownership tables. low-noise `workflow-integration.md` 85% (owner of the lane return contract) and `model-output-profiles.md` 83% (two rules became pointers that cost as many words).
5. Pruned rules: P1 28, P2 4, P3 5, P4 5, P5 14, P6 1; plus 2 corrections (the `50-hooks.md` "checker" sentence; the Codex skills URL, now `https://learn.chatgpt.com/docs/build-skills`, dated 2026-11-16). Ledger: `agent-ae759aa886871fd05/artifacts/core-skills-compression-20261116/pruned-L4b.md`.
6. Checker clauses: 0 reworded, 0 deleted. No clause checker binds these skills.
7. Cross-skill restatements:
   - Replaced by pointers: low-noise `model-output-profiles.md` repeated-check removal -> `alaa-prompting-guide references/80-subagent-authoring.md` (the floor sentence stays); calibration evaluation -> prompting-guide `60-skill-authoring.md`. low-noise body plan persistence -> the existing `alaa-workflow references/artifact-lifecycle.md` pointer. Authoring rules in low-noise `90-source-map.md` pruned with the owner named in the ledger.
   - Left: return shape, budgets and "no universal watchdog timeout" (low-noise owns); read-only MCP and grant rules in `80` (routing owns); retry budgets in `10`; one clause in `45` that a focused check does not replace a full-project gate (gate floor).
   - Structure changes inside the routing references: the six fallback bullets of *Finite degraded operation* are merged into the selection table of `10`; generated, runtime, external and cross-repository rows now live only in `30`; the topic map lost its third column.
8. Kept but doubted:
   - routing `10-routing-contract.md:47` "record the missing fact, the failed capability and the guarantee you lose", and its `## Handoff` section; kept because `alaa-workflow references/companion-routing.md:12` consumes the owner and the established fact.
   - routing `SKILL.md` `## Output`: lane contracts own report shape.
   - routing `40-stack-bindings.md:47` (affected tests are candidates) and `:66` (provider memories).
   - routing `70-project-bindings.md:30` "Record the expected semantic owner".
   - low-noise `noise-control-patterns.md:14`: a standing "Delegate a wide sweep" line with no cost or criteria; left for the Phase 3 carry-over walk.
   - low-noise `90-source-map.md:8,10` and routing `90-source-map.md` *Runtime and hook owners*: other `developers.openai.com` links have no fetched redirect evidence; left unchanged.
   - Operation card rows: diff of table lines against `37ce87a4` is empty.
9. Gates, cwd worktree root, `PYTHONDONTWRITEBYTECODE=1 python3 -B`: `scripts/validate_sohrab_skill_pack.py` 0; `scripts/check_skill_index.py` 0; `scripts/check_fleet_references.py` 0; `scripts/check_lifecycle_contract.py` 0; `scripts/check_agent_grants.py` from `alaa-cc-orchestrator` 0 and from `alaa-codex-orchestrator` 0. Criterion 3: `## Operation card` one hit (SKILL.md:15); `## Delegated lanes` one hit (workflow-integration.md:12).
   - Conflict with "once": the six gates ran twice. The first run (all 0) preceded a last round of edits that restored rule force and rows; the second run (all 0) is on the committed tree.

Residual risk: no agent run was observed, so behaviour equivalence rests on a source walkthrough only. Two pointers name prompting-guide files that another lane is rewriting now; I cited fixed file names only. Not run: any other suite, any `codegraph` index command. Independent review is pending at the final boundary. Blockers: none.

## L2b — second pass, alaa-testing-strategy

STATUS: COMPLETE — `alaa-testing-strategy` is rewritten and pruned under the second-pass brief: total 16,133 to 13,047 words (-19%), body 3,412 to 2,502 (-27%); all seven gates exit 0 on the final tree; independent review is pending at the final boundary.
AGENT: alaa-implementer-fable. CONFIGURED model/effort: unknown (definition not observable). REQUESTED: claude-fable-5-2 / high. OBSERVED: model claude-fable-5-2 (runtime environment line); effort unknown. No mismatch observed.

1. Outcome: every file under `skills/sohrab/alaa-testing-strategy/` except `run-low-priority.sh` and the frontmatter description (Phase 3 owns descriptions) was rewritten; checker literals, the normative hash and one contradiction guard follow the text.

2. Branch `worktree-agent-a9c0b6742b793f697`, worktree `agent-a9c0b6742b793f697` (fast-forwarded to `37ce87a4` first). Commits, each by path:
- `ce493f05` refactor(alaa-testing-strategy): rewrite and prune the skill in fewer words
- `832a604e` docs(artifacts): record the pruned rules of lane L2b
- `6e34ceef` fix(alaa-testing-strategy): restore body tokens and the repair budget, rebind the execution pointer

3. Words by `measure.py` (before to after): frontmatter 104 to 104; body 3,412 to 2,502; references 12,406 to 10,381; other 211 to 60; total 16,133 to 13,047. `SKILL.md` is 181 lines.

4. Files above four fifths of their start:
- `70` (86%) and `80` (97%): they received body content (the ten design steps, +180; the report-field content, +215). Their own text fell to about 63% and 77%.
- `100` (92%), `110` (90%), `120` (92%): 7 clauses reworded and 4 deleted there. The remaining sentences are distinct authority limits, numbers, status tokens and exceptions (never-prune classes), and were already one rule per sentence.
- `40` (85%): six level definitions and the claim-to-level table, the vocabulary 18 external files cite.
- `90` (86%), `30` (81%), `50` (81%): three tables each row a decision; `90` also received the detail of non-negotiables 10, 13 and 14.

5. Pruned rules: 21 rows — P1 2, P2 4, P3 1, P4 1, P5 12, P6 1. Ledger: `agent-a9c0b6742b793f697/artifacts/core-skills-compression-20261116/pruned-L2b.md`. It also records six decisions, including the flake resolution: an unclassified case is reported blocked (`references/50-flake.md`), never defaulted to product defect.

6. Checker clauses (`scripts/check_execution_contracts.py`), reworded / deleted / added:
- `REQUIREMENTS`: body 1/0/0; execution 5/1/2 (one clause split in two, one added for the realigned orphan); doctrine 2/0/0; resources 0/1/0; classification 0/2/0. Count 213 to 211.
- `NORMATIVE_DUPLICATES`: execution 4/1/2; resources 0/1/0; classification 0/2/0; doctrine 1/1/0 (orphan moved to execution). Count 105 to 102; SHA-256 recomputed by the script's own function.
- `CONTRADICTIONS`: +1 (the old flake sentence). `workspace`, `continuity`, `economy`, `router`, `flake` untouched. The lead should re-check the six reworded forbidden strings against the packs at integration; no hit at `37ce87a4`.

7. Cross-skill restatements: replaced by nothing new (this skill is the owner). Removed ownership restatements of other skills: prompting-guide, workflow, orchestrators, per-language, controlled-ops rows in `00`. Left: the orchestrator cadence pointer in the tier section and the `100` authority limit, because each routes a real decision.
Owned rule families, for other lanes to point at (`SKILL.md`): tiers `## Scope tiers: how much of the suite runs, and when` line 77; fresh exhaustive run line 88 and validity `### A result stays valid until something named invalidates it` line 92; classification and the concealment ban `### A failing tier is classified before it is repaired` line 109 (ban sentence line 120); CPU and timing `references/110-execution-resources.md`; statuses `references/120-result-classification.md`.

8. Kept or changed with doubt:
- `10` *Anti-patterns* (20 items) and `90` *Review checks* deleted as duplicates; the body pointer to the first went with it.
- `SKILL.md:128` output contract: names, order and tokens in the body, field content in `80` *The report fields*.
- `SKILL.md:180`: "read the topic map first" narrowed to references no body pointer names.
- `SKILL.md:57` non-negotiable 4 says parity suite only, while `30-doubles.md` lists generation as a stronger binding.
- `agents/openai.yaml` `default_prompt` cut to two sentences.
- `50-flake.md` "a rerun-failed-tests step" is forbidden while `100` step 3 reruns failed checks after repair; wording kept.
- `110-execution-resources.md` forwarder paragraph: describes scripts in the orchestrator packs.

9. Gates on the final tree, from the worktree root with `PYTHONDONTWRITEBYTECODE=1 python3 -B`: `validate_sohrab_skill_pack` 0; `check_skill_index` 0; `check_fleet_references` 0; `check_lifecycle_contract` 0; `check_execution_contracts` (skill dir) 0; `check_agent_contracts` cc 0, codex 0. First run was clean; all seven were rerun after the fix commit.

Skills: /alaa-ponytail full, /alaa-low-noise, /alaa-prompting-guide with `60-skill-authoring.md` (*ASD-STE100 style*, *The wording is the mechanism*) before the first edit; `skills/sohrab/AGENTS.md` read before the first edit; /alaa-workflow *Lane branches and commits* read before the first commit. Preloaded /alaa-code-intelligence-routing, /alaa-services-contract, /alaa-trust-gateway-auth: no decision in this lane needed them. /alaa-testing-strategy was the text under edit.
Residual risk: no fixture, comparison or live-agent run (excluded). Criterion 5 was checked by hand only. Boundary conflicts: none; no public route or contract changed.

## L3b — second pass, alaa-workflow

STATUS: COMPLETE — `alaa-workflow` is rewritten and pruned under lane-brief-2; all seven gates exit 0, and the measured cut is 13.6 percent (18,814 to 16,251 words), which is below "far fewer" and is reported as measured.

AGENT: alaa-implementer-fable; CONFIGURED: unknown (no definition file read); REQUESTED: `claude-fable-5-2` / high; OBSERVED: model `claude-fable-5-2` (runtime environment), effort unknown.

1. Predicates: explicit owner selection recorded; task matched it (instruction rewrite plus checker literals). No mismatch.
2. Branch `worktree-agent-a333c58dd978caf56`, worktree `agent-a333c58dd978caf56`, ff-merged to `37ce87a4` first.
   - `854c74bb` docs(alaa-workflow): rewrite and prune the skill text
   - `f8b8c728` docs(alaa-workflow): restore four rules the rewrite cut too far
3. Words (measure.py): body 1104 to 869; references 15766 to 13450; assets 1800 to 1788; total 18814 to 16251.
4. Files above four fifths, and what kept them there:
   - `task-tracking.md` 5645 to 4825: the capability table (about 1170 words, every decision kept, three row merges), seven externally cited sections that root `AGENTS.md` relies on, validator-enforced formats.
   - `workspace-and-integration.md` 2476 to 2217: 17 bound clauses, the 10-step lane section this skill owns and other lanes now point to, the lifecycle rows.
   - `artifact-lifecycle.md` 1845 to 1605: approval and helper formats the scripts enforce.
   - `companion-routing.md` 1024 to 896: the skill-binding format the validator enforces.
   - `review-mode.md` 845 to 833: dense protocol text (`## Finding triage`, tokens cited by both packs); restructured into lists, almost nothing removable.
   - `phase-prompts.md` 907 to 737, `context-curation.md` 393 to 343: small files, each remaining sentence is a rule.
   - Assets: script-read labels, tokens and bound clauses; only two prose lines in `plan-template.md` changed.
   - Below four fifths: `context-continuity.md` (2631 to 1994), `SKILL.md` body.
5. Pruned: P1 5, P2 1, P3 14, P4 2, P5 17, P6 1 rows (several rows group sentences). Ledger: `agent-a333c58dd978caf56/artifacts/core-skills-compression-20261116/pruned-L3b.md`.
6. Checker clauses: reworded 0, deleted 0 in `COLLECTION_SEAMS`, `COLLECTION_CONTRADICTIONS`, `workspace`, `continuity`. Reason: each bound clause is already a minimal rule; I rewrote the text around them. No checker file was touched.
7. Restatements replaced by pointers: never-weaken-assertions and repair/retest (testing-strategy); five reasoning classes and allocation-record fields (orchestrator `routing-matrix.md`); testing reference routing; `$name`/`/name` sigils (prompting-guide 06); lane return shape (low-noise *Delegated lanes*); system-design conditions (one-line summary kept). Left: context-reassurance wording, because only the historical `40-fable-5.md` carries it; handshake step 2 "validate the tree that would land".
8. Kept but doubted:
   - `task-tracking.md:65` `Registration: draft|registered` protocol.
   - `task-tracking.md:39` read before and after `bd close` (root `AGENTS.md` shows the same).
   - `task-tracking.md:33` lease and heartbeat.
   - `task-tracking.md:216` install-together and rollback rule.
   - `context-continuity.md:28` JSON projection rules.
   - `context-continuity.md:113` per-item lane progress record.
   - `context-curation.md:27` run the final gate when empty.
   - `workspace-and-integration.md:51` manifest digest for uncommitted state.
   - `companion-routing.md:25` domain owner list.
   - `assets/phase-template.md:5` `Reasoning and selection reason` now has no definition in this skill.
9. Gates, final text, `PYTHONDONTWRITEBYTECODE=1 python3 -B`: `validate_sohrab_skill_pack` 0, `check_skill_index` 0, `check_fleet_references` 0, `check_lifecycle_contract` 0 (worktree root); `check_execution_contracts` 0 (testing-strategy); `check_agent_contracts` 0 (cc), 0 (codex). Criterion 4: 15 headings, one hit each. Criterion 5: token sets equal in all eight assets. Criterion 7: each cited rule found (claim readback, exit 13, `bd lint` block, `--sandbox`/`--readonly`, close-reason parts, learned-knowledge placement, cross-PC record).

Skills loaded before the first edit: alaa-ponytail (full), alaa-low-noise, alaa-prompting-guide with `60-skill-authoring.md` (both sections); routing, testing-strategy, services-contract and trust-gateway were preloaded. Late: testing-strategy `100-test-execution.md` was read after the first gate run, before the final one.

Residual risks and not run:
- The gates ran three times, not once (two interim runs).
- `init_workflow_files.py` and `validate_workflow_files.py` were not run (excluded); asset safety rests on reading their regexes. Validator lines 1132 to 1532 and the initializer after line 407 were not read.
- Three internal headings changed or went: `## Division of labor`, `## Where task information lives`, `## What this file does not own` (removed), `## Contents, updates, resume and delegation` (now `## Artifact contents`), `## Evidence order` and `## Must-check areas` (merged); a grep found no outside citation.
- Other lanes that turn copies into pointers should target `## Lane branches and commits` step numbers unchanged (1 to 10).

Boundary conflicts: none.

## L5c-b — second pass, orchestrator contract assets and agents

STATUS: COMPLETE — both packs' contract assets, hand-written agents, wrapper descriptions and stack bindings are rewritten from one source text with identical behavioural wording, pruned under the brief with a ledger, re-rendered, and every gate in criteria 1 to 3 exits 0 on the final tree.
AGENT: alaa-implementer-fable. CONFIGURED: none (model-neutral definition). REQUESTED: claude-fable-5-2 / high. OBSERVED: claude-fable-5-2 (system prompt); effort unknown.

1. **Outcome.** The implementation contract and all 26 implementer wrappers end at 76–78% of their start. The specialist agents end at 82–91%, so the "far fewer words" goal is met for the per-dispatch implementer text and only partly for the specialists.

2. **Branch and commits.** Branch `worktree-agent-aa7638c1870d92761`, worktree `agent-aa7638c1870d92761`, fast-forwarded to `fe101a53` first. Tree is clean.
   - `955eec66` refactor(orchestrators): rewrite and prune contract assets and agent definitions
   - `a9f88090` fix(orchestrators): keep the control block causes, mismatch flag and read-only sentence
   Both cover both packs. Brief says one commit per skill; I followed the dispatch.

3. **Words (`measure.py`), before → after.**
   | Pack | Assets | Hand-written agents | Generated agents |
   |---|---|---|---|
   | cc | 4096 → 3429 | 12430 → 10615 | 18096 → 14052 |
   | codex | 4770 → 4052 | 11556 → 9933 | 22673 → 17758 |
   `wc` counts a slash-joined list as one word, and I kept those lists, so this is like for like.

4. **Files above four fifths (47 of 77).**
   - Hand-written specialists and codex reviewer contract (82–91%): frontmatter cannot change; the five shared blocks are at their floor (about 175 words, down from about 250); the rest is a checklist of review dimensions, never-prune limits and output items the lead reads.
   - `alaa-verifier` (90%): six `RUN_ECONOMY` clauses kept verbatim. `alaa-architecture-critic` (86%): seven shared cadence clauses kept verbatim.
   - Planner contracts and planners (85–87%): three cadence literals plus planning rules that each change a proposal.
   - `profile-wrappers.json` (87%): bindings are condition-to-skill routing lists; only tails and repeated sentences went.

5. **Pruned rules.** 30 rows: P1 7, P2 3, P3 3, P4 6, P5 11, P6 0. Also 4 restatements of a loaded skill, 6 relocations, 10 pack alignments, 3 corrections. Ledger: `artifacts/core-skills-compression-20261116/pruned-L5c-b.md`. Row 2 removes one block condition ("pair missing after normalization") under the dispatch's permission to delete that clause.

6. **Checker clauses** (`check_agent_contracts.py`, same edits in both packs).
   - `agent_failures`: 16 → 14; 2 deleted, 5 reworded.
   - `IMPLEMENTER_REQUIREMENTS`: cc 17 → 16, codex 16 → 15; 1 deleted, 2 reworded, plus the cc-only literal reworded. The two checkers stay one clause apart, as before.
   - Unchanged and verbatim in my files: the seven shared `specialist_cadence_failures` clauses, the six `verifier_agent` clauses, "settled decision a later lane or repair owner must know", and the inline `cadence_failures` implementer and planner clauses.

7. **Cross-skill restatements.**
   - Replaced by the one call line: two testing-strategy bullets in the implementation contract, the eight-step procedure in `alaa-test-strategist`, the routing-skill bullet in `alaa-researcher`, the `/alaa-system-design` and `/alaa-algorithms-data-structures` content lists.
   - Left: the lane-commit rule with its citation, the three testing-strategy reference pointers (each names its trigger), the Verification bullets, the operation-card line.

8. **Kept but doubted** (cc paths under `skills/sohrab/alaa-cc-orchestrator/`; codex mirrors).
   - `assets/implementation-contract.md:20` "After editing, inspect the full diff and its callers."
   - `:28` "Never guess a repository fact".
   - `:36` reason clause "running it here pays twice".
   - `:43` "The role name selects no control."
   - `assets/planner-contract.md:9` "Plan no trial ladder, synthetic benchmark or replay".
   - `agents/alaa-architecture-critic.md:29` re-check of infrastructure answers through /alaa-memory-os.
   - `agents/alaa-researcher.md:18` "Go breadth first".
   - `agents/alaa-reviewer.md:34` style-only comment rule.
   - codex `agents/alaa-browser-qa.toml` keeps `$playwright`, unlike every other call site.

9. **Gates, final tree, `PYTHONDONTWRITEBYTECODE=1 python3 -B`, all exit 0.**
   - Root: `validate_sohrab_skill_pack.py`, `check_skill_index.py`, `check_fleet_references.py`, `check_lifecycle_contract.py`.
   - Each pack, in order: `render_agents.py --write`, `--check`, `validate_pack.py`, `check_agent_contracts.py`, `check_agent_grants.py`.
   - `alaa-prompting-guide`: `check_claude_model_policy.py`, `check_codex_model_policy.py --agent-root assets/rule-writer/codex`.
   - Review-only criterion 5, by my own script: every hand-written head differs from `fe101a53` only in `description`; verdict and status token sets and output-item counts are unchanged; no never-prune marker is lost. A first run flagged the read-only sentence of `Effective authority:` as gone from codex read-only roles; `a9f88090` restored it.
   - Not run: install scripts. Independent review is pending at the final boundary.

**Boundary notes for the lead.**
- New shared block text, identical in every file of both packs: see `Task controls:`, `Report metadata`, `Effective authority:` and both `Return protocol` forms in either `assets/implementation-contract.md` and `agents/alaa-reviewer.md`. Agents no longer resolve an omitted control themselves; L5c-a's `model-effort-policy.md` and `agent-catalog.md` should not say they do.
- Critic now cites "Stage A step 4"; align the step number.
- Codex reviewer descriptions live in `render_agents.py` (excluded), so I left the cc `alaa-reviewer` description equal to them.
- `freshness.md`: none of its three corrections lands in my files.
- I ran the gates without first reading testing-strategy `references/100-test-execution.md`.

Skills loaded before the first edit: /alaa-prompting-guide (60 and 80 sections read), /alaa-ponytail full, /alaa-low-noise; preloaded: /alaa-code-intelligence-routing, /alaa-testing-strategy, /alaa-services-contract, /alaa-trust-gateway-auth. Builder and checks are in `/tmp/claude-1000/-home-sohrab-project-skills/75ecedca-09c9-4d1a-998e-2f75020937a5/scratchpad/` (`texts.py`, `build.py`, `verify.py`, `pct.py`).

## L5c-a — second pass, orchestrator SKILL.md and references

STATUS: COMPLETE — both packs' `SKILL.md` and `references/**` are rewritten in identical terms and every gate exits 0, but the cut is about 21 percent, not "far fewer words".
AGENT: alaa-implementer-fable (lane L5c-a). CONFIGURED: none (model-neutral role). REQUESTED: claude-fable-5-2 (`fable`), high. OBSERVED: claude-fable-5-2 per the runtime system context; effort unknown.

1. **Outcome.** Each behavioural rule is stated once, with the same text in both packs. Shared files are generated from the cc text by asserted substitution: 11 files are byte-identical, the rest differ only by runtime hunks. The Stage A capability inquiry is still **step 4**.

2. **Branch and commits.** Branch `worktree-agent-ad830aefde7c5c4f7`, worktree `agent-ad830aefde7c5c4f7`, HEAD after the merge `fe101a53`, tree clean.
   - `eb16a7c9` docs(orchestrators): rewrite and prune SKILL.md and references of the mirrored pair
   - `7ab48c62` fix(orchestrators): restore four safeguards the rewrite dropped

3. **Words (`measure.py`), before → after.**

   | Pack | `SKILL.md` body | References |
   |---|---|---|
   | cc | 2521 → 2001 | 13693 → 10768 |
   | codex | 2512 → 1972 | 14218 → 11471 |

4. **Files that ended above four fifths (`wc`), and why.**
   - `verification-and-gates.md` (cc 3740 → 3040, codex 3881 → 3166): nearly all of it is what the dispatch says the pair must keep (decision and four questions, floors, evidence, after a fix, who fixes, cadence table, stages), and about 75 clauses still bind it.
   - `routing-matrix.md` (cc 3235 → 2592, codex 3373 → 2726): the allocation procedure, admission predicates and every specialist trigger.
   - `delegation-prompts.md` (692 → 582) and every template except `20-design.md`: XML tags that checkers match; only prose around them could go.
   - `SKILL.md` whole file is 80.2 percent in cc because the frontmatter is untouched; the body is under four fifths.
   - Well under: catalog (66 and 74 percent), `model-effort-policy.md` (59 and 60), the two pointer files.

5. **Pruned rules.** Ledger: `artifacts/core-skills-compression-20261116/pruned-L5c-a.md`, 80 rows: P1 8, P2 1, P3 8, P4 1, P5 19, P6 2, plus `OWN` 29 (restated another skill's rule), `DUP` 11 (stays elsewhere in the pack), and 1 row for dropped reason clauses. `OWN` and `DUP` are my labels, not brief criteria.

6. **Checker clauses.** 17 deleted, 0 reworded, same edit in both `check_agent_contracts.py`, no logic change: `CADENCE_REQUIREMENTS` 8, `COLLECTION_REQUIREMENTS` 3, routing tuple in `task_allocation_failures` 3, `GATE_REQUIREMENTS` 1, `orchestrator_failures` 1, skill tuple in `cadence_failures` 1. I reworded none because the surviving bound sentences were already minimal.
   - Kept verbatim because another lane owns the tuple or shares the clause: the `COLLECTION_SEAMS` phrases in routing *Failure routing*, `40-verification.md`, `30-implementation.md` and `failure-taxonomy.md`; the seven shared `<review_boundary>` clauses in `20-design.md` and `60-contract-review.md` (the critic agent needs them too); the testing-strategy citations.

7. **Cross-skill restatements.**
   - Replaced by pointers, by owner (ledger rows):
     - alaa-workflow: 10, 16, 20–24, 26, 27, 29, 33, 69
     - alaa-testing-strategy: 14, 30, 35, 46, 55, 60, 72
     - alaa-prompting-guide: 4, 7, 63, 64
     - alaa-low-noise: 1–3
     - alaa-code-intelligence-routing: 58
     - alaa-system-design: 73
     - alaa-algorithms-data-structures: 74
   - Risk: I checked each owner at `fe101a53` only. If a parallel lane prunes the same rule on its side, it exists nowhere and no gate catches it; grep these rows again after the merges.
   - Left in place:
     - the watchdog sentence in `delegation-prompts.md`, bound by an `if`, not a tuple entry;
     - the push/tag authority limit in gates;
     - the `<return>` wording inside the envelope, since a child does not load the owner;
     - the framework-class tool lists in the catalog, which `80-agent-scoping.md` does not define.

8. **Kept but doubted** (cc paths; codex mirrors):
   - `SKILL.md:97` — the final-report close line (dispatch and check counts, time span).
   - `SKILL.md:103` — pack-maintenance commands in the always-loaded body.
   - `references/routing-matrix.md:72` — the lane rechecks the admission predicates.
   - `references/routing-matrix.md:55` and `:63` — recording rejected pairs and the allocation record.
   - `references/verification-and-gates.md:159` — the Stage E scope and status check.
   - `references/verification-and-gates.md:163` — rerun the final gates if the base advanced.
   - `references/delegation-prompts/40-verification.md:20` — one identical rerun for flake detection.
   - `references/delegation-prompts.md:28` — the invocation read-back.

9. **Gates** (`PYTHONDONTWRITEBYTECODE=1 python3 -B`, final run on the tree that `7ab48c62` commits), all exit 0:
   - root: `validate_sohrab_skill_pack.py`, `check_skill_index.py`, `check_fleet_references.py`, `check_lifecycle_contract.py`;
   - each pack: `render_agents.py --check`, `validate_pack.py`, `check_agent_contracts.py`, `check_agent_grants.py`;
   - `alaa-testing-strategy`: `check_execution_contracts.py`.
   - Review-only, by script: no template tag, verdict or status token, role name or Appendix A heading present at `fe101a53` is missing; each of `## Admission`, `Final report`, `## Batch allocation`, `## All-role task allocation` has one hit per pack.
   - Not run: `render_agents.py --write`, install scripts. Independent review is pending at the final boundary.

**Skills.** Loaded before the first edit: /alaa-prompting-guide (`60-skill-authoring.md` sections read), /alaa-ponytail full, /alaa-low-noise; the four preloaded skills were in context. Late: testing-strategy `references/100-test-execution.md` was read after the first gate run and before the last, because I went straight to the supplied commands.

**Boundary notes for the lead.**
- `CHANGELOG.md` and `VERSION` are untouched (L5c-b).
- `SKILL.md` sections lost their numbers, and routing "Always or normally required" is now "Default roles". Nothing in `assets/` or `agents/` cited either. The critic's "Phase A step 4" should read "Stage A step 4".
- Conflict: the brief asks for one commit per skill, the dispatch for commits covering both packs; I followed the dispatch.
- Restored after a self-check, in `7ab48c62`: the Ent acceptance rule, the compatibility-realization exception, the `bd` flag names, and the native-plan clause.
- Scratch tooling: `/tmp/claude-1000/-home-sohrab-project-skills/75ecedca-09c9-4d1a-998e-2f75020937a5/scratchpad/l5ca/` (`gen.py`, `checker_edits.py`, `checker_edits2.py`, `audit.py`, `measure-before.txt`).

## L1b — second pass, alaa-prompting-guide

STATUS: COMPLETE — `alaa-prompting-guide` is rewritten and pruned under the second-pass brief, the five source corrections are applied, the ledger is committed, and all eleven gates exit 0; the word cut is 15.6 percent for the skill, well short of "far fewer".
AGENT alaa-implementer-fable; CONFIGURED unknown (no definition observable); REQUESTED claude-fable-5-2 / high; OBSERVED model claude-fable-5-2 (system prompt), effort unknown.

1. **Outcome.** Every reference, the `SKILL.md` body, `contract.md` (copied byte-identical into both wrappers) and `dispatch.md` are rewritten. 26 rules pruned and recorded. Policy JSON, `scripts/**`, `agents/openai.yaml` and the `SKILL.md` description are unchanged. No file retired.

2. **Branch, worktree, commits.** Branch `worktree-agent-a4dbb6ed6a8238e99`, worktree `agent-a4dbb6ed6a8238e99`, base `b8a00eb8` (fast-forward done). Tree clean.
   - `430f0944` docs(alaa-prompting-guide): rewrite and prune the skill text, apply five source corrections
   - `b0289c0c` docs(artifacts): record the L1b pruned-rule ledger
   - `6fa2743d` docs(alaa-prompting-guide): restore dates and a rule route lost in the rewrite (repair after self-review; no amend)

3. **Words (measure.py).** Before: frontmatter 89, body 790, references 25,947, assets 4,452, other 49, total 31,327. After: 89, 772, 21,219, 4,316, 49, total 26,445. References −18.2%, total −15.6%. `measure.py` counts whitespace tokens, so each table pipe and list dash counts as a word.

4. **Files above four fifths of their start (after/before words), and why.**
   - `43` 99%: dispatch forbids pruning any fact row or behaviour entry; it was already in short STE sentences.
   - `41` 87%: Appendix C facts plus never-prune numbers, limits, version gates and dated sources fill it; only non-numeric platform prose was prunable (ledger rows 11 to 16).
   - `11` 84%, `90` 89%, `12` 89%, `36` 90%: same cause. `90` is mostly the 27-row selector matrix and the Claude table. `12` also gained the correction C quotes and one blog line.
   - `61` 92%: six new official facts (+110 words) offset the cut.
   - `00-source-map` 100%: URL lists and dates are sources; it gained the redirect example and a 16 November date group.
   - `00-topic-map` 92%: every row is a trigger; none is prunable.
   - `SKILL.md` body 98%: gate commands, exit codes, authority limits and stop conditions; sections were reordered (decision procedure first), not cut.
   - `contract.md` 92%, `dispatch.md` 99%: invariants, stop conditions and dispatch fields are never-prune.
   - Below four fifths: `21` 69%, `50` 69%, `80` 69%, `70` 73%, `60` 75%, `06` 78%, `31` 79%.

5. **Pruned rules: 26.** P1 3, P2 1, P3 1, P4 10, P5 7, P6 4. Ledger: `artifacts/core-skills-compression-20261116/pruned-L1b.md`. It also has the A to E correction rows, the additions with their sources, and a table of removed duplicates (checklists and defect tables) with where each rule still lives.

6. **Checker clauses.** Reworded 0, deleted 0. No clause checker binds this skill. G5 holds (wrappers equal `contract.md`), G6 holds (no model name).

7. **Cross-skill restatements.**
   - Replaced by pointers: the orchestrator role catalog and lead/verifier rules in `90`; the plugin-build reason for the single `/name` form in `06` (pointer to `skills/sohrab/AGENTS.md`).
   - Left: `80` "no lane approves its own change" (this skill owns the authority test); the managed-roles sections of `41` and `11` (Appendix C).
   - Outside my scope, still restating `60`: `skills/sohrab/AGENTS.md` *The wording test* and its "Write all three parts" (60 now says four).
   - Conflict followed per dispatch: the brief's owner table puts `AGENTS.md` chain facts in `11`; the dispatch puts them in `70`. They are in `70`; `11` points there, and the Codex write-back rule moved with them.

8. **Kept but doubted.**
   - `60:132` optional comparative evaluation (owner bans comparisons for skills).
   - `60:35` activation side effect as a fourth description part (freshness.md: unsourced).
   - `41:187` *Choosing a mechanism* list (mostly platform restatement).
   - `41:81` advisor rule 9, advice length.
   - `41:217` and `11:110` near-identical managed-roles sections.
   - `11:66` CSV batch tool; `11:80` slash-command name list.
   - `12:23` planning sentence and "finite enumerated batch".
   - `90:95` reviewer-profile sentence.
   - `80:81` "After you change a dispatch, measure quality".
   - Also: new dates are written "16 November 2026", not ISO, to match the files. Seven references exceed 100 lines with no table of contents (`41`, `60`, `06`, `11`, `70`, `61`, `90`), against the new `61` line; I added none.
   - The two new carry-over rows apply through the existing gate ("only when the target model's reference documents the behaviour"), so I added one dated blog line to `12`; they are not applicable to a Claude-only text unless the owner widens the gate.

9. **Gates, all on the final tree, `PYTHONDONTWRITEBYTECODE=1 python3 -B`.** Root: `validate_sohrab_skill_pack` 0, `check_skill_index` 0, `check_fleet_references` 0, `check_lifecycle_contract` 0. Skill dir: `check_rule_writer_grants` 0, `check_claude_model_policy` 0, `check_codex_model_policy --agent-root assets/rule-writer/codex` 0. Each orchestrator: `render_agents.py --check` 0, `validate_pack.py` 0. No `__pycache__` created.

**Skills.** Loaded before the first edit: `alaa-ponytail` (full), `alaa-low-noise`; preloaded: `alaa-code-intelligence-routing`, `alaa-testing-strategy`, `alaa-services-contract`, `alaa-trust-gateway-auth`. Late: `alaa-workflow references/workspace-and-integration.md` *Lane branches and commits* was read after the first two commits (they conform: by path, no amend); `alaa-testing-strategy references/100-test-execution.md` was read after the first gate run and before the final rerun. `references/routing-matrix.md` profile section not read: the recorded predicates held.

**Residual risk.** Criterion 5 is self-checked only: a token inventory (numbers, dates, backticked names, URLs) before and after shows no number lost, and the lost names are ledger rows 11 to 21 or correction A. Sentence-level behaviour equivalence of the rewrite is unreviewed. The first commit lost three dates and one rule route in `41`, `11` and `12`; `6fa2743d` restores them, so the review should read those three files first. No web fetch was run; the 16 November facts rest on `freshness.md` and the dispatch.
