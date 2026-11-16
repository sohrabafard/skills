# Lane returns

Final reports of the lanes of this work, as returned. Model output, dated 2026-11-17.

## LC — alaa-prompting-guide and alaa-low-noise

STATUS: COMPLETE. Lane LC is done: all nine items are in place, the corrections from sources.md are applied and dated 17 November 2026, and all seven gates exit 0 on the final tree.

AGENT: alaa-implementer-sonnet-high. CONFIGURED: not inspected. REQUESTED: claude-opus-5-5 (alias opus), effort medium. OBSERVED: model claude-opus-5-5 (from the runtime system prompt); effort unknown.

2. Branch, worktree and commits
- Branch: `worktree-agent-a4d9d9f1f90c42af6`. Worktree: `agent-a4d9d9f1f90c42af6`. I fast-forwarded it to `c6fc56b9` as the brief says.
- Commits:
  - fddc76cf feat(alaa-prompting-guide): handle advisor use in Claude prompts and apply dated source corrections
  - fa2e5beb feat(alaa-low-noise): lead with the four context rules and add a command-output budget
  - c4f7a535 fix(alaa-prompting-guide): restore advisor scope and dates and keep claims to their sources
  - 1cb44ace fix(alaa-low-noise): keep inventory in the search-first rule
- The two fix commits apply the advisor's completion review. They are separate commits; nothing was amended.

3. Items
1. Done. `SKILL.md` *Decision procedure* has a new step 6 (line 24).
2. Done. `41` *Prompts for a session that may have an advisor* now has, in order: the reliance paragraph, the four things every prompt does, the table of surface by executor, three surface bullets, and "Rules the table does not carry". The heading is kept. The two Haiku items and the Fable cell keep the page-text-unverified mark. The Sonnet and Opus API cells are limited to coding executors, as the platform page states. Unchanged text keeps its 14 November 2026 date.
3. Done. `41` *Native Advisor* gains dated lines for:
   - Start: `-p`, Agent SDK, desktop from v2.1.260; `/advisor off`; `--advisor` not in `--help`; the background session.
   - Preflight: the platforms, v2.1.300, the excluded clouds and `DISABLE_TELEMETRY`.
   - Pairs: Haiku 5.5 needs v2.1.293; Haiku 4.5 can call the advisor but cannot be one; the advisor must be at least as capable as the executor.
   - The notification when a pair is not accepted, and a subagent whose own model passes the pairing check.
   - `max_tokens`: minimum 1024, start at 2048, none for Managed Agents.
   - The source line now carries the 17 November links.
4. Done. `06` *Kickoff and completion condition* gains one pointer.
5. Done. `50` gains a section *Lowering effort* with four dated facts, each linked to its own page.
6. Done. `90` changes:
   - Five Claude effort-evidence cells now hold Messages API defaults and the effort-page guidance.
   - The Sonnet bullet is reworded. Bullet: the three pages checked state no Claude Code default; model-config was not re-read.
   - The two computer-use rows have T medium in the balanced cell, and the legend gains T = GPT-6.1 Terra.
   - The Terra alternative for "Adapt existing content" is a note under the matrix, because `sources.md` names no column for it.
   - The asset URL is now `BKCv-TnC`.
   - Lines 69 and 12:15 (open or unverified) are unchanged.
7. Done. `12` gains a dated *Subagent inheritance* paragraph.
8. Done. Low-noise `SKILL.md` has a new *First rules* section with the four rules, moved from Part 1 and Part 2. It also has the default command-output budget (about 40 lines per command that enters the context) and the sentence on a lane's own output rule. The progress budget and every other rule are kept.
9. Done. `references/workflow-integration.md` is unchanged, and `## Delegated lanes` is intact.
- `00-source-map.md` gains a 17 November 2026 row.
- Ledger: `artifacts/continuity-and-allocation-20261117/changes-LC.md`.

4. Word counts (before → after)
- `SKILL.md`: 863 → 891
- `41`: 3952 → 4286
- `06`: 1789 → 1814
- `50`: 687 → 774
- `90`: 1535 → 1756
- `12`: 745 → 794
- `00-source-map`: 656 → 695
- low-noise `SKILL.md`: 793 → 886
- `workflow-integration.md`: unchanged

5. Checker clauses: none bind these files, so 0 reworded and 0 deleted.

6. Plan items that the sources made impossible or unwise
- Boundary conflict: `alaa-prompting-guide/assets/codex-model-policy.json:33` still cites the `DJkmSLnH` asset, which now returns 404. The policy JSON is outside my scope, so I did not change it.
- Old rule 3 (name consultation points only on a long multi-step task) is not in the dispatch's keep list. I kept it in the *Claude Code surface* bullet, because removing it would weaken a rule with no plan item to allow that. The new pointer in `06` relies on it.
- `50`: the dispatch states the skipped-check risk at low effort for any model. `sources.md` ties it to Haiku at `low`. I kept the dispatch's general wording.

7. Rules kept but doubted
- `41` Native Advisor: "Haiku 4.5 can call the advisor but cannot act as one". It is correct to the page, but Haiku 4.5 is outside the active set.
- `90`: the Codex default lines in model references `31` and `43` cite model-config of 14 November, which nobody re-checked on 17 November.

8. Gates (final tree, run once after the fixes, all with `PYTHONDONTWRITEBYTECODE=1 python3 -B`)
- From the worktree root: `validate_sohrab_skill_pack` 0, `check_skill_index` 0, `check_fleet_references` 0, `check_lifecycle_contract` 0.
- From `skills/sohrab/alaa-prompting-guide`: `check_rule_writer_grants` 0, `check_claude_model_policy` 0, `check_codex_model_policy --agent-root assets/rule-writer/codex` 0.
- The criterion 3 greps each return 1 hit. The `SKILL.md` hit is step 6 of the decision procedure.
- I made no web fetch, as the dispatch requires. The independent review at the final boundary is pending.

Skills: I loaded `/alaa-ponytail` (full) and `/alaa-prompting-guide` before the first edit, and read the `60-skill-authoring.md` sections *ASD-STE100 style* and *The wording is the mechanism*. The system preloaded `/alaa-code-intelligence-routing`, `/alaa-testing-strategy`, `/alaa-services-contract` and `/alaa-trust-gateway-auth`. I ran no `bd` command.

## LA — alaa-workflow and the root binding block

STATUS: COMPLETE — Workstream 1 items 1 to 7, both advisor pointers, the 449-word binding block and its template are implemented and committed; all seven gates exit 0.
AGENT: alaa-implementer-fable. CONFIGURED: not inspected. REQUESTED: claude-fable-5-2, effort high. OBSERVED: model claude-fable-5-2 (runtime banner); effort unknown.

**1. Outcome.** See the STATUS line. Criterion 5 was walked from the two files as three agents (same session after a compaction, new lead session, lane with no known actor): each reaches a command, a position and a takeover or no-transfer decision. That walk is my own review, not an independent one.

**2. Branch, worktree, commits.**
- Branch `worktree-agent-a51757d2174be56ef`, worktree `agent-a51757d2174be56ef`, fast-forwarded to `c6fc56b9`.
- `4d829169` feat(alaa-workflow): make Beads use parallel-safe, lighter and resumable
- `cff0f5e6` fix(alaa-workflow): let a new session find its earlier work on resume
- Tree clean. Ledger: `artifacts/continuity-and-allocation-20261117/changes-LA.md`.

**3. Plan items** (paths under `skills/sohrab/alaa-workflow/`).
- W1.1 plan shape: done, `references/task-tracking.md` `## Beads-native execution plan`. One rule covers every native "phase" mention: with no phase, the root takes its place. `Final phase` is the last phase ID or the root ID.
- W1.2 ownership: done, `## Agent identity and ownership`. Heartbeat and TTL read removed with reason and date. Close is `bd lint`, then close; the pre-read only after a resume, outage or transfer. Registration checks are `bd dep cycles` plus one ready query.
- W1.3 lanes: done, same two sections. Dispatch carries actor, binding reference, leaf ID and `claim`; read-only stays `none`; lead closes with its own actor; rejected leaf gets a `discovered-from` follow-up.
- W1.4 continuity: done, `references/context-continuity.md`. I1 in `## Status and position`; I2 and I3 in `## Task resume and phase resume`; takeover (three conditions, one guarded transfer) in `task-tracking.md`.
- W1.5 capability table: done. Adopted rows plus one reject row; every dated line kept, one 2026-11-17 line added.
- W1.6 block: done, root `AGENTS.md` between the markers only; `assets/beads-binding-template.md` added, with one triggered pointer in `## Select before tracking-dependent work`. `init_workflow_files.py` reads templates by name (line 72), so it does not render or reject the new asset.
- W1.7 low-noise: done, `SKILL.md` Start step 5 and `references/companion-routing.md` *Core companions*.
- Advisor pointers: done, `references/phase-prompts.md` and `assets/phase-prompts-template.md`; no token and no bound sentence changed.

**4. Words before → after (`wc -w`).**
- `AGENTS.md` block with markers: 1220 → 449
- `references/task-tracking.md`: 4837 → 5546. Gained: plan sizing, lane ownership, takeover, lead close, and the batch and sync rules moved out of the block.
- `references/context-continuity.md`: 1994 → 2559. Gained: I1, I2, I3 and the tag column.
- `SKILL.md` 987 → 1003; `companion-routing.md` 896 → 928; `phase-prompts.md` 737 → 758; `phase-prompts-template.md` 664 → 685; `beads-binding-template.md` new, 778.

**5. Checker clauses.** Reworded 0, deleted 0, in every tuple. No bound sentence changed; no checker file edited.

**6. Plan against sources.**
- I3 as fixed has a gap, and other lanes copy it. A new session can name its actor, but that actor is new, so the `--assignee` list is empty. I added: on an empty list, list again without `--assignee` and take the issue that the user, dispatch or handoff names. LB's copy of I3 needs the same sentence.
- I1 says the lead keeps `Lane:` lines, but notes are appended. I added: the `Lane:` lines belong to the root block and only the last block's lines are live.
- Takeover uses the guarded transfer in place of `bd reclaim`, as you directed.
- Flag order. The old block wrote `bd --sandbox --actor "<actor>" <subcommand>`, which the project allow-list matches. The owner section and the user's global tool-use rule put `--actor` after the subcommand, which the user-level allow-list matches (`Bash(bd --sandbox update *)`). I aligned the new block and template to the owner section. Neither list covers `comments add`; the project list lacks `dep add`, `search` and `dep cycles`. The template states this as information.
- The template keeps the absolute hub path on its `Expected workspace` line. That sits against the no-machine-path rule of `skills/sohrab/AGENTS.md`; the root exception names only the binding's line. Owner decision.
- Block rules removed with no new home: the mandatory read of `.agents/skills/beads/SKILL.md`, "recheck after a workspace or connection change", "other-project dependency reads are allowed", the session-end report list, and the Quick Reference list.
- I2 says "any actor"; I wrote "any actor that may write to Beads", because a `none` lane runs `--readonly`.

**7. Rules kept but doubted.**
- `task-tracking.md:187`: the `bd reclaim` row still requires an expired lease in `bd show`, while line 33 says to read no lease.
- Same row: with no heartbeats, every long-lived claim looks stale to a bare `bd reclaim`. The row forbids the bare form; that prohibition now carries more weight.
- `task-tracking.md:31`: read, claim, read back is three commands; the claim is already atomic.
- `task-tracking.md:79`: the rejected leaf stays unclosed while its repair is only a `discovered-from` follow-up, so dependents wait on a leaf that no edge ties to the repair.
- `task-tracking.md:83`: `bd ready --parent <root-id>` with phases present; I did not check that it descends.
- `task-tracking.md:33`: `lease.go` is cited by name only; `sources.md` gives no directory.

**8. Gates** (final tree `cff0f5e6`, `PYTHONDONTWRITEBYTECODE=1 python3 -B`, no resource limits).
- Worktree root: `scripts/validate_sohrab_skill_pack.py` 0; `scripts/check_skill_index.py` 0; `scripts/check_fleet_references.py` 0; `scripts/check_lifecycle_contract.py` 0.
- `skills/sohrab/alaa-testing-strategy`: `scripts/check_execution_contracts.py` 0.
- `alaa-cc-orchestrator` and `alaa-codex-orchestrator`: `scripts/check_agent_contracts.py` 0 each.
- Each kept heading returns one anchored `grep` hit. Block and template are equal after the `__PROJECT__` substitution.
- Not run: `init_workflow_files.py`, `validate_workflow_files.py`, any `bd` write, any other suite. Live agent behaviour is unproved.

Skills loaded before the first edit: `/alaa-prompting-guide` (with `60-skill-authoring.md` *ASD-STE100 style* and *The wording is the mechanism*), `/alaa-ponytail` full, `/alaa-low-noise`; `/alaa-testing-strategy` and `/alaa-code-intelligence-routing` were preloaded. Not read: testing-strategy `100`, `110` and `120` references, and the routing-matrix profile section; the lane ran only the supplied commands and no repair was needed. Blockers and boundary conflicts: none. Independent review is pending at the final boundary.
