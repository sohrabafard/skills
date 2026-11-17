# Continuity, allocation fit, advisor handling and output reach — report

Four behaviour changes are in place on branch `work/continuity-and-allocation` and every static
gate exits 0: Beads use that is safe for parallel agents and resumable from Beads alone,
allocation of model and effort by fit, advisor handling in every Claude prompt, and an output
rule in every agent definition. Both orchestrator packs are at version 7.1.0. The change added
about 10,000 words to the seven core skills; the section *Size* says where and why.

Work ran on 2026-11-17. Beads root: `alaa-prgpl`. Design: `plan.md` in this directory.

## What changed

**Beads (`alaa-workflow`, root `AGENTS.md`).**
- A plan has the shape its size needs: one issue, or a root with leaf tasks, and a phase
  milestone only at a real barrier. Each leaf names its owned paths.
- Ownership rests on the assignee and the status. The heartbeat duty is gone: the Beads 1.3.2
  source shows that a claim by another actor on an in-progress issue fails whatever the lease.
  `bd reclaim` is no longer adopted; one guarded transfer is the only takeover.
- A dispatched write lane claims its leaf with its own actor and appends a checkpoint when its
  position changes and before it returns. The lead closes the leaf after it reconciles the diff.
- Position is a five-line checkpoint block in `notes` (Position, Next, Blockers, Evidence,
  Touched). Knowledge is tagged comments (fact, assumption, ruled-out, read-first, env, trap,
  decision). The root block also names the lead and each live lane.
- The always-loaded binding block fell from 1,220 to 575 words and now carries the resume
  trigger: at session start, after a compaction, and whenever the agent cannot name its
  position, run `bd list --status=in_progress --label <label> --assignee <actor>` and
  `bd show <id>`. Its canonical text is `alaa-workflow/assets/beads-binding-template.md`.

**Allocation (both orchestrator packs).** The lead records two facts per lane, the judgment
left to the lane and its search and length, and reads the pair from a fit table. A pair that is
too strong and a pair that is too weak are both defects. The table has a tie rule between its
first rows, a rule for roles that implement nothing, a named ordinary level per row, and a last
column that needs a recorded measured gain. A lane that returns light raises the pair for the
remaining work, and a lane that finishes trivially lowers it; completed work is not replayed.
The recorded owner decisions stay: no pins, no trial ladder, no quotas, role names select no
pair, an explicit user choice may depart from the table.

**Advisor (`alaa-prompting-guide`).** The decision procedure applies the advisor section to
every prompt for a Claude model. That section is now one table, surface by executor model. On
the Claude Code surface every cell is "write nothing by default", and the rule against copying
timing or weight blocks there is explicit. Four things hold for every Claude prompt: goal,
constraints and acceptance in the prompt text; a decision written before it is acted on; a
saved deliverable before the completion consultation; no dependence on the advisor. In the
Claude Code pack the lead consults a present advisor before it ratifies the plan and before the
final report.

**Output (`alaa-low-noise`, every agent definition).** All 70 agent definitions carry one
output rule and the return-length default. `alaa-low-noise` leads with its four highest-value
rules and sets a default of about 40 lines of command output per command.

**Dated source corrections, 17 November 2026.** Advisor platforms, versions and `max_tokens`
facts in `41`; the lowering rule in `50`; Claude effort evidence, two matrix rows and the
selector asset URL in `90` and in `assets/codex-model-policy.json` (added to the scope by the
owner); Codex subagent inheritance in `12`.

## Size

Source words exclude generated agents, `CHANGELOG.md` and scripts (`measure.py` of the
compression work).

| Skill | Before this work | After | Change |
|---|---|---|---|
| `alaa-workflow` | 16,270 | 18,779 | +2,509 |
| `alaa-cc-orchestrator` | 27,308 | 30,618 | +3,310 |
| `alaa-codex-orchestrator` | 28,509 | 31,805 | +3,296 |
| `alaa-prompting-guide` | 26,544 | 27,449 | +905 |
| `alaa-low-noise` | 1,784 | 1,894 | +110 |
| other two skills | 20,986 | 20,986 | 0 |
| Total | 121,401 | 131,531 | +10,130 |

What is paid most often moved in both directions: the always-loaded Beads block lost 645
words; the implementation contract that every implementer loads grew from 1,047 to 1,294
words, and each other agent definition grew by about 80 to 130 words (the output rule, and for
write lanes the task-tracking block). A reviewer dedicated to word economy read every added
block; its seven confirmed cuts are applied. The lead read the two shared agent blocks after
the repair and found no sentence that carries no obligation.

## Review

The owner turned on ultracode during this work, so the single review of the plan became three
workflows.

| Workflow | Agents | Result |
|---|---|---|
| `review-lc-changes` | 79 | 16 findings confirmed by at least two of three verifiers, 9 refuted; all 16 applied (`review-lc.md`) |
| `review-continuity-and-allocation` | 171 | 43 findings confirmed (2 blocker, about 30 major, 11 minor), 17 refuted; six blind walks (`review-main.md`) |
| `fix-review-findings` | 16 | two writers, two verifiers per group, one repair round, four repeated walks; 14 items stayed open after the second verification, 13 applied by the lead and 1 kept with its reason (`repair.md`) |

The two blockers: the binding block had weakened "explicit user authorization for that scope"
for other-project work, and the new output rule told the verifier to alter supplied commands.
Both are fixed.

**Blind fit-table walks.** Walkers on two models chose a pair for seven sample lanes from each
pack's text alone. After the repair, in the Claude Code pack both walkers gave: exact rename,
Haiku 5.5 medium; source comparison, Sonnet 5.5 medium; everyday feature, Sonnet 5.5 medium;
cross-service refactor, Opus 5.5 high; judgment-dense rewrite, Opus 5.5 high; long migration
with a settled runbook, Sonnet 5.5 high. They differed on the second-lens review (Opus or
Sonnet, both high), because the lane text did not state the hardest decision under review. The
Codex walkers agreed on five of seven lanes and gave the official balanced cells where the
official matrix has a row.

One expected pair of the plan was wrong. The plan expected Fable 5.2 for a migration that runs
for hours. The review showed that this let duration alone select the strongest model, against
the recorded owner rule. Duration now selects the effort only.

**Cold-start walks.** Two agents (Opus 5.5 and Haiku 5.5) started with no memory, the new
binding block and read-only `bd` commands on the live hub. Both found the root of this work,
its position and its next action from `bd list` and `bd show`. Both also reported what the
lead's own records lacked at that moment: a checkpoint written before the last merge, no
`Lane:` lines, and an authority that had changed in the notes but not in the root field. The
rules that prevent each of these are now in the text.

## Verification

Sixteen gates exit 0 on the final tree: the four root checkers; `check_execution_contracts.py`;
in each pack `render_agents.py --check`, `validate_pack.py`, `check_agent_contracts.py`,
`check_agent_grants.py`; the three prompting-guide checkers. One checker literal was reworded,
identically in both packs; no checker logic changed.

Not verified:

- Live agent behaviour. The walks are source walkthroughs by agents, not observed runs of the
  orchestrator or of a compacted session.
- Three advisor items stay "page-text unverified", because the fetch tool summarised the page.
  The OpenAI Terra guidance URL and the Codex models page quotation were not re-fetched.
- Whether a Codex write lane's sandbox can reach the Beads hub, and whether `bd unclaim` by a
  non-holder succeeds. The text tells the lane to report a failed write and the lead to expect
  a refusal.
- The reviewers had no web access and judged vendor facts against `sources.md` only.

## Open items for the owner

- Allow-list. The new flag order is `bd --sandbox <subcommand> ... --actor <actor>`. The
  owner's user-level allow-list, read on 2026-11-17, covers that order for `create`, `update`,
  `close`, `dep add` and `unclaim`, but has no entry for `bd --sandbox comments add`, so a
  tagged knowledge comment can ask for permission. The project allow-list of this repository
  lists the other order. No settings file was changed; the template lists the entries.
- Other repositories keep the old binding block. Their cited headings still exist and their
  `--append-notes` command stays correct. Rolling the new block out is a separate task.
- `skills/sohrab/AGENTS.md` still says "Write all three parts" for a description; `60` lists four.
- An external write role, such as the Ent specialist, carries no task-tracking block, so its
  dispatch gives the Beads action `none` and the lead writes its checkpoint from the return.
- The fit table cannot be gated. The walks are the only evidence that a lead reads it as
  intended, and the review-lens lane stays ambiguous when a dispatch does not state the hardest
  decision under review.
