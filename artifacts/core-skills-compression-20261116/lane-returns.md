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
