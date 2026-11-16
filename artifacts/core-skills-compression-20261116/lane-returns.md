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
