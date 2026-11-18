# GPT-6.2 upgrade of the core skills

Date: 2026-11-18. Pack version 8.3.0. Codex model policy 3.0.0.

The six core skills now use the GPT-6.2 generation in Codex. Two of them held model text and
changed: `alaa-prompting-guide` and `alaa-codex-orchestrator`. `alaa-testing-strategy` gained one
rule. `alaa-workflow`, `alaa-code-intelligence-routing` and `alaa-low-noise` hold no model text and
did not change. No agent definition changed.

## Owner direction and decisions

- Active Codex generation: `gpt-6.2-astra`, `gpt-6.2-sol`, `gpt-6.1-terra`, `gpt-6-luna`.
- `gpt-6-astra` and `gpt-6.1-sol` leave ordinary selection.
- The fit table follows the official balanced cells of the refreshed selector.
- Authorized effects: a bounded smoke call per new model, a merge into `main`, and an agent
  installation if a definition changed. No push.

## Sources, all read on 2026-11-18

| Source | Used for |
|---|---|
| [Prompting GPT-6.2 in Codex](https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra) | Effort by depth of investigation, "use subagents as needed", Ultra, lean `AGENTS.md`, shared-machine advice |
| [Latest-model guide](https://developers.openai.com/api/docs/guides/latest-model) | Concise default, propose-and-wait, shorthand in the final answer, API changes, migration effort |
| [Codex models](https://learn.chatgpt.com/docs/models) | IDs, where each model fits, effort starting points, Max and Ultra |
| [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Inheritance, precedence, subagent starting points |
| [Model-selection guide](https://developers.openai.com/api/docs/guides/model-selection) | Eight model and effort pairs |
| Served selector asset `ModelSelection.react.DJwdUSJM.js` | 27 task rows, 81 cells; extracted in [selector-matrix.txt](selector-matrix.txt) |
| API model pages for `gpt-6.2-astra` and `gpt-6.2-sol` | The API rejects effort `none` |
| Host model catalog, client 0.169.0 | Both GPT-6.2 slugs with `low` to `ultra`, default `low` |

The pages were read as raw text. A summarizing fetch was used only to find them.

## Smoke

One `codex exec` call in a read-only sandbox at `low`, CLI 0.166.0, before any eligibility change:
`gpt-6.2-sol` and `gpt-6.2-astra` each returned the requested reply with exit code 0, and the
session header named the requested model and effort. This proves that the host accepts both IDs.
It proves no quality, no calibration and no behavior of a custom agent.

## What changed

**`alaa-prompting-guide`**

- `references/12-gpt-6.md`: the active family, the guide's eight pairs, a new *GPT-6.2 behavior*
  table with the repair for each documented behavior, API-versus-harness facts, subagent starting
  points. The file grew from 808 to 1386 words; the new capability is the behavior table, which
  is the source of every GPT-6.2 carry-over check.
- `references/90-model-selection.md`: all 27 matrix rows regenerated from the asset by script,
  the asset's own caveats, and Codex eligibility with three historical models.
- `references/06-invocation-and-composition.md`: the Codex polarity row states Ultra and
  "use subagents as needed".
- `references/70-agent-instruction-files.md`: a routine how-to decision does not belong in an
  instruction file.
- `references/00-source-map.md`: new sources and dates.
- `assets/codex-model-policy.json` 3.0.0 with `scripts/codex_model_policy.py` and
  `scripts/task_model_controls.py`: two new models, a set of three historical models that must
  stay selection-disabled and that task selection refuses.

**`alaa-codex-orchestrator`** (8.3.0; the Claude pack records no equivalent)

| Fit row | Before | After |
|---|---|---|
| None: an exact transformation | `gpt-6-luna` | unchanged |
| Bounded local decisions | `gpt-6-luna`, ordinary `medium` | `gpt-6.1-terra`: `low`, `medium`, `high`; Luna at the same column only on an explicit user cost priority, recorded as the user's choice |
| Grounded everyday decisions | `gpt-6.1-sol` | `gpt-6.2-sol`; a research lane whose return is a decision or a verdict on a disputed fact starts at `high` |
| Coupled or cross-boundary | `gpt-6.1-sol` | `gpt-6.2-sol` |
| Judgment-dense | `gpt-6.1-sol` | `gpt-6.2-sol` |
| Exceptional model | `gpt-6-astra` | `gpt-6.2-astra` |

- No lane runs at `ultra`: at that effort Codex starts subagents on its own, and a lane starts none.
- The default alias is `sol-6.2-medium`.
- `scripts/check_agent_contracts.py`: two literals follow their sentences.

**`alaa-testing-strategy`**

- `references/110-execution-resources.md` *Service safety and reuse*: before return, stop each
  background process, container and service the run started and remove each temporary file it created, except what a
  declared reuse or a later step needs.

## Carry-over ledger

Method: `alaa-prompting-guide references/60-skill-authoring.md` *Carry-over review for a new model
generation*. A check applies only when every model that loads the file has the behavior
documented; the stale-fact check always applies.

| Scope | Check | Result |
|---|---|---|
| Codex agent contracts, 19 hand-written definitions, delegation prompts, rule-writer | Stale fact | No hit: no model name, effort value or version gate in any definition |
| Same | General concision line | No hit. The output rule is a consumer limit with an exception, not a style line |
| Same | Propose-and-wait repair, self-contained final answer | Not applicable: every definition also runs on Luna and Terra, and no source documents these behaviors for them. The lead applies the repairs in the dispatch of a GPT-6.2 lane, because `SKILL.md` *Dispatch discipline* words each dispatch under the prompting guide |
| Same | Step itinerary, default-behavior instruction | Not re-run. Their source is the skills blog of 16 November 2026, which this upgrade did not change, and the definitions were rewritten and pruned on 2026-11-17 (pack 8.0.0) |
| Codex orchestrator routing | Ultra delegation | Repaired: no lane at `ultra` |
| `alaa-testing-strategy` | Shared-machine advice | CPU and concurrency rules already present; the cleanup rule was absent and was added |
| `alaa-workflow`, `alaa-code-intelligence-routing`, `alaa-low-noise` | Stale fact | No hit: no model text |
| Same | GPT-6.2 behavior checks | Not applicable: both runtimes load these files, and the behaviors are not documented for every loading model |

No rule was removed, so the ledger has no removal row.

## Independent review

One `alaa-instruction-reviewer` pass (dispatched at `opus`, `medium`) read the diff against the raw
vendor texts. It returned four major and seven minor findings, all applied once, with no second
round: the Terra gate and its precedence over later fit rows restored; the Luna cost exception
moved into the priority rule, with the raise from Luna to Terra; the start cell and the research
rule made consistent, with the source caveat on fact checks; the second delegation trigger
(`AGENTS.md` or skill instructions) restored; smaller source-fidelity repairs in `12`, `70`, `90`,
the source map and the cleanup rule. It checked all 81 matrix cells and the short table and found
them clean. It did not assess the API-page, host-catalog and smoke claims.

## Installation

The 28 installed Codex agent definitions were compared with the source by parsed field (`name`,
`description`, `developer_instructions`, `sandbox_mode`): all match, and none carries a model or
effort pin. No definition changed, so no installer ran. The six skills are installed as links to
this repository, so the merge activates them.

## Limits

- The vendor selector is editorial. Its policy note says that the September task scores keep
  their original model identities and that cited results apply to the models and settings tested.
- The Terra pair of the bounded row is uncalibrated here. Its cost is higher than the Luna pair.
- Static gates prove no instruction compliance and no serving identity.
- The Codex main session is configured outside this repository and was on `gpt-6.1-terra` at
  `medium` on this host. It was not changed.

## Open owner items

1. Main-session model in `~/.codex/config.toml` and its setup mirror: keep Terra or move to
   `gpt-6.2-sol`.
2. Whether to add an assume-and-continue sentence to the implementation contract of both packs.
   The carry-over rule marks it not applicable today.
3. Remeasure bounded lanes after one week of sessions: quality and cost of Terra `medium` against
   the earlier Luna `medium`.
