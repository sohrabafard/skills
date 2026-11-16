# Core skill pack compression — report

The seven core skills now hold 121,401 source words, down from 163,554 (26 percent less), and
the generated agent definitions hold 32,294 words, down from 42,953 (25 percent less). Every
static gate exits 0 on the final tree. The reduction is below the "far fewer words" goal; the
section *What limits the reduction* says why and lists what the owner can still decide.

Work ran 2026-11-16 to 2026-11-17 on branch `work/core-skills-compression`. Beads root:
`alaa-v8rg1`. Plan: `plan.md` in this directory, with its addendum of 2026-11-17.

## Result by skill

Source words exclude generated agents, `CHANGELOG.md` and scripts. Numbers come from
`measure.py`; `baseline.md` and `final.md` hold the full tables.

| Skill | Baseline | After pass 1 | Final | Change |
|---|---|---|---|---|
| `alaa-testing-strategy` | 18,973 | 16,133 | 13,055 | -31% |
| `alaa-cc-orchestrator` | 34,657 | 32,869 | 27,308 | -21% |
| `alaa-codex-orchestrator` | 35,267 | 33,765 | 28,509 | -19% |
| `alaa-workflow` | 19,449 | 18,814 | 16,270 | -16% |
| `alaa-code-intelligence-routing` | 10,178 | 9,868 | 7,931 | -22% |
| `alaa-low-noise` | 2,675 | 2,437 | 1,784 | -33% |
| `alaa-prompting-guide` | 42,355 | 31,327 | 26,544 | -37% |
| Total | 163,554 | 147,213 | 121,401 | -26% |

Text that is paid on every dispatch or activation:

| Text | Baseline | Final | Change |
|---|---|---|---|
| cc `assets/implementation-contract.md` (rendered into 11 implementer agents) | 1,438 | 1,047 | -27% |
| `alaa-testing-strategy/SKILL.md` body (preloads into 13 agents) | 3,986 | 2,510 | -37% |
| `alaa-cc-orchestrator/SKILL.md` body | 2,564 | 2,001 | -22% |
| `alaa-workflow/SKILL.md` body | 1,116 | 872 | -22% |
| `alaa-low-noise/SKILL.md` body | 965 | 714 | -26% |
| `alaa-code-intelligence-routing/SKILL.md` body (preloads into 31 agents) | 753 | 723 | -4% |
| `alaa-prompting-guide/SKILL.md` body | 797 | 772 | -3% |
| Generated agents, both packs | 42,953 | 32,294 | -25% |

## What was done

**Pass 1 (Opus 5.5, medium), compress and retire.** Six lanes removed duplicates inside each
skill and retired six superseded model references of `alaa-prompting-guide` (7,801 words) and
its dated refresh log into `_to_delete/20261116-core-skills-compression/alaa-prompting-guide/`.
Each retired file arrived at its original size. The lanes reworded almost no checker-bound
sentence, so rule-dense files fell 3 to 15 percent.

**Owner decision, 2026-11-17.** The owner chose a second pass that rewrites every sentence and
prunes rules under six criteria, with a ledger, written by Fable 5.2 at high effort.

**Pass 2 (Fable 5.2, high), rewrite and prune.** Six lanes rewrote every file under
`lane-brief-2.md`. They also moved cross-skill restatements to one owner and applied the
corrections from `freshness.md`. Both orchestrator packs moved to version 7.0.0, because rule
pruning is a behaviour change.

**Pruned rules.** About 240 rows in six ledgers, each with file, rule, criterion and deleted
checker clause: `pruned-L1b.md` (prompting guide), `pruned-L2b.md` (testing), `pruned-L3b.md`
(workflow), `pruned-L4b.md` (routing and low-noise), `pruned-L5c-a.md` (orchestrator bodies and
references), `pruned-L5c-b.md` (contracts and agents). To restore a rule, take its sentence from
`main` before the merge commit and put it back with its checker clause.

**Checker clauses.** No checker logic changed. In the module-level tuples of the three clause
checkers, literal counts moved from 748 to 718: `CADENCE_REQUIREMENTS` 36 to 28,
`COLLECTION_REQUIREMENTS` 17 to 14, `GATE_REQUIREMENTS` 24 to 23, `IMPLEMENTER_REQUIREMENTS`
minus 1 in each pack; `REQUIREMENTS` 213 to 211, `NORMATIVE_DUPLICATES` 105 to 102 and
`CONTRADICTIONS` 19 to 20 in the testing checker, with its SHA-256 recomputed. Inline tuples
inside checker functions, which `measure.py` does not count, also lost clauses in each pack:
`agent_failures` 16 to 14, the routing tuple of `task_allocation_failures` minus 3,
`orchestrator_failures` minus 1, and the skill tuple of `cadence_failures` minus 1. Each
deletion has a ledger row.

## Deliberate behaviour changes

| Change | Where | Source or reason |
|---|---|---|
| Rule pruning under criteria P1 to P6 | all seven skills | Owner decision 2026-11-17; ledgers |
| "Keep the whole report under 40 lines" became a default with an exception | contract assets | Hard style limit, `43-fable-5-2.md` *Style limits* |
| An intermittent failure that stays unclassified is reported blocked, no longer defaulted to a product defect | `alaa-testing-strategy references/50-flake.md` | Resolves a contradiction with the `SKILL.md` stop condition. The reviewer asks the owner to confirm, because the old default kept the test in the suite as the reproduction |
| An agent no longer resolves an omitted model or effort itself; it reports the field as omitted | every agent definition | The lead normalizes controls (`model-effort-policy.md`) |
| Two carry-over rows added: default-behaviour instruction, step-by-step itinerary | `60-skill-authoring.md` | OpenAI skills blog, fetched 2026-11-16 |
| Six official authoring facts added (500-line body, important text first, one-level references, table of contents past 100 lines, third-person description, name rules) | `61-skill-platform-mechanics.md` | Claude Code skills page and Agent Skills best practices, fetched 2026-11-16 |
| Pre-existing divergences between the two packs aligned to the stronger form | agent definitions | `pruned-L5c-b.md`, alignment rows |

Corrections from the official-source check: the `AGENTS.md` chain drops the files nearest the
working directory, not the outermost (`70`, with `11` pointing to it); one subagent frontmatter
list, in `80`; the GPT-6.1 Sol sentence in `12` now quotes the models page; the Codex skills URL
in `alaa-low-noise`; a sentence in `50-hooks.md` that named a checker that does not exist.

## Review

One independent review ran, as two read-only `alaa-instruction-reviewer` lanes over disjoint
scopes. Their full reports are in `lane-returns.md`.

| Scope | Verdict | Findings | Disposition |
|---|---|---|---|
| Orchestrator pair | APPROVED-WITH-NITS | 6 minor, 9 nits | Five minor findings fixed; the 40-line default kept as intended; nits recorded only |
| Testing, workflow, routing, low-noise, prompting guide | CHANGES-REQUESTED | 3 major, 6 minor, 8 nits | All three major and five minor findings fixed; the flake default left for the owner; nits recorded only |

Fixed in commit `d2e4638b`: two prohibitions restored at the testing owner sentence (hard-coding
an expected result, lowering a review standard); two Beads readbacks that guard against data
loss; the `/loop` limits; the observation time of a tested state; a narrowed trigger; one output
field; the "model choice grants no authority" limit; the grant-inspection step; one final
success criterion; the planner's read-only Bash limit. No confirmation pass ran, by the owner's
standing rule.

Every pass-2 lane also made its own repair commit that restored rules it had cut too far. That
pattern, and the three major findings, show that unintended loss was a real risk of this work.

## Verification

All of these exit 0 on the final tree, run once after the last change:
`scripts/validate_sohrab_skill_pack.py`, `scripts/check_skill_index.py`,
`scripts/check_fleet_references.py`, `scripts/check_lifecycle_contract.py`;
`alaa-testing-strategy/scripts/check_execution_contracts.py`; in each orchestrator pack
`render_agents.py --check`, `validate_pack.py`, `check_agent_contracts.py`,
`check_agent_grants.py`; in `alaa-prompting-guide` `check_rule_writer_grants.py`,
`check_claude_model_policy.py`, `check_codex_model_policy.py --agent-root assets/rule-writer/codex`.

Also checked: each heading cited from outside its skill still exists (script over 189 files);
each of the seven `task-tracking.md` headings that the root `AGENTS.md` cites has one hit.
A number inventory compared every numeric token (numbers, versions, dates) in the 178 changed
files before the work with the seven skills now: four tokens are gone, all intended (the stale
`4.0.0` version line, the names of two retired files, one example pull-request number). The
inventory proves that a number still exists somewhere in the pack, not that it stayed at each
site. `git diff --name-status` between `main` and this branch shows no deleted file.

Not verified:

- Live agent behaviour. No agent run was observed; the gates prove structure and source
  agreement only.
- `alaa-workflow/scripts/init_workflow_files.py` and `validate_workflow_files.py` were not run.
  Template safety rests on an unchanged `{{token}}` set.
- The reviewers did not read: most cc agents and every codex agent, `profile-wrappers.json`,
  the delegation-prompt templates, the clause edits in the two `check_agent_contracts.py` files,
  and about half of the references of the five other skills (listed in their reports).
- The OpenAI API model pages and the model-selection guide were not re-fetched; the Luna and Sol
  selector cells in `12-gpt-6.md` keep their older dates.

## What limits the reduction

The remaining text is mostly of four kinds that the brief protected: authority limits and
approval rules; numbers, version gates and dated sources; decision tables where each row is a
decision; and sentences that a checker binds. The frontmatter descriptions were left unchanged,
because they are activation text and hold under one percent of the words.

Further reduction needs owner decisions. Candidates, each kept in this work:

| Candidate | Where | Why it was kept |
|---|---|---|
| Beads registration protocol (`Registration: draft` then `registered`, read-backs of every node) | `alaa-workflow references/task-tracking.md` | Recorded owner policy |
| Claim lease and heartbeat; read before and after `bd close` | same | Recorded owner policy; root `AGENTS.md` shows the same sequence |
| The capability table of adopted and rejected `bd` commands (about 1,170 words) | same | Each row is a decision; root `AGENTS.md` cites the section |
| Content digest of an uncommitted tested state; JSON projection rules; per-item lane progress | `alaa-workflow` | Evidence identity rules |
| Allocation record: rejected cheaper pair with its failed predicate, source row and date | orchestrator `routing-matrix.md` | Allocation doctrine of the pair |
| The lane rechecks admission predicates; the lead reads back each invocation | orchestrator pair | Dispatch safeguards |
| Final-report close line (dispatch count, check count, time span) | orchestrator `SKILL.md` | Report contract |
| Pack-maintenance commands in the always-loaded body | orchestrator `SKILL.md` section on checks | Could move to a reference |
| Near-identical managed-roles sections | `41` and `11` of the prompting guide | Appendix C keep-list |
| Optional comparative evaluation | `60-skill-authoring.md` | The owner bans comparisons for skills; this section may be removable |
| The about 30 clauses that still bind sentences in each `check_agent_contracts.py` tuple | both packs | Checker redesign was out of scope |

Rules that make an agent re-review, re-test or re-confirm were listed by each lane and not
changed. The lists are in `lane-returns.md` (items 6 or 7 of each first-pass return).

## Open items

- Confirm or revert the flake default (table above).
- `skills/sohrab/AGENTS.md` says "Write all three parts" for a description; `60` now lists four.
  That file was out of scope.
- The two new carry-over rows apply only where a model's own reference documents the behaviour.
  Only `12-gpt-6.md` does. A fetched Anthropic source would let the rows apply to Claude models.
- Seven references of the prompting guide exceed 100 lines and have no table of contents, which
  the new line in `61` asks for.
- One ledger row points at `11-codex-runtime-features.md` for the call-at-limit failure, which
  that file does not state; the behaviour stays in the codex `SKILL.md`.
