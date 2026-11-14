# Claude Fable 5.2

Use this file for current Fable prompting. `references/42-fable-5-1.md` and `references/40-fable-5.md` are historical. Fable 5.2 and Mythos 5.2 are one model; Mythos stays excluded from active selection and custom profiles. The runtime orchestrator selects Fable from task evidence. A role title, a vendor ranking or availability selects nothing, and no source claim proves local superiority.

## Facts

Refresh each row from its source before you quote it.

| Fact | Value on 14 November 2026 | Source |
|---|---|---|
| API ID | `claude-fable-5-2`; Amazon Bedrock uses `global.anthropic.claude-fable-5-2` | Models overview |
| Effort levels | `low`, `medium`, `high`, `xhigh`, `max` | Effort |
| Default effort | Claude API `high`; Claude Code `medium` | Effort; model configuration |
| Minimum Claude Code | 2.1.321 | Model configuration |
| `fable` alias | Fable 5.2, except Claude apps gateway sessions, which resolve to Fable 5 unless `ANTHROPIC_DEFAULT_FABLE_MODEL` is set | Model configuration |
| Thinking | Adaptive, always on | Models overview |
| Data retention | 30-day retention required; no zero-data-retention arrangement unless Anthropic authorizes it | Migration guide |

The selection guide starts most workloads on Opus 5.5. It names Fable 5.2 for demanding reasoning, long-horizon agentic work, and work that still falls short on Opus 5.5 at `xhigh` or `max`. `references/90-model-selection.md` owns that evidence.

## Effort

- Most of the capability gain is present at `high`. Above `high`, gains are uneven and depend on the task.
- `medium` fits interactive coding and everyday work. `low` fits well-specified tasks and high-volume subagents. Use `xhigh` only for the hardest long-running work with a measured gain. Use `max` to measure the ceiling.
- Effort barely changes reply length. Control length and tone in the prompt.
- A line such as "answer directly without deliberating" does not stop thinking at `medium` and above. Remove the line and lower the effort.
- Early stops are more frequent at `low` and `medium`. For agentic work at those levels, add the finish rule below.
- An effort setting tuned on Fable 5.1 or Opus 5.5 is untested here. `references/50-effort-and-thinking.md` owns the decision procedure.

## Behaviours that change what you write

Apply a rule below only when the target harness shows the behaviour, or when the artifact was written for an earlier model. Each added text costs tokens; the figures are vendor measurements.

**Early stop.** On long multistep work the model can end a turn by listing what remains, by offering to continue, or at an ordinary obstacle such as a timeout. State the finish rule: complete the work the user asked for; diagnose errors, timeouts and failing tools, and work through them; leave a deliberate blocker alone and report it; keep the confirmation step for risky or irreversible actions. Vendor cost: about 30% more output tokens.

**Approvals.** The model treats a rule that contains "never" as absolute, and it follows approval rules closely. When the agent must keep responsibility for an action, write "ask for approval before deleting files", not "never delete files". Name the exact actions that need approval. A broad category held back routine work in vendor tests. Name the routine steps that need no approval. Reply to an approval request with the exact action, not with "continue".

**Accumulated caution.** Memory, notes and instruction files collect cautions over time, and the model wrote some of them. They cause approval requests the task does not need, mostly when several agents work together. Delete a caution whose reason no longer holds. Give every absolute rule its scope and its reason. Narrow a stop condition such as "stop and review at the first error" to the failures that need a person.

**Code ownership.** With no ownership statement, the model adds to the existing structure, even when that duplicates code. With "You are the owner and long-term maintainer of this codebase", it consolidates duplicates and makes changes nobody asked for; a scope rule in the same prompt does not cancel that. Use the ownership sentence only when restructuring is wanted. In a scoped lane, omit it and name the existing helper the lane must reuse.

**Delegation.** `references/06-invocation-and-composition.md` owns the polarity rule for this model.

**Progress text.** During long tool runs the model writes little user-facing text. Where a person follows the run, ask for a one-line opening, a one-line update every few tool calls, and a closing recap that stands alone. An unattended lane needs none of these.

**Final reports.** The reader has not seen the tool calls or the files. Require the key points first, a self-contained message, plain full sentences, no abbreviation invented during the work, prose where ideas connect, and bullets for separate items.

**Style limits.** The model follows writing-style rules closely. A hard limit such as "20 words or fewer in every sentence" makes its prose choppy. State a style rule as a default and name its exception.

**Token budget in the prompt.** A budget shown in prompt text changes how much the model spends. In vendor tests a large budget raised cost with equal results. Show no token budget in a prompt or a dispatch. The API task-budget feature is a separate control.

**Reasoning in the reply.** A request to reproduce internal reasoning in the response can be refused with category `reasoning_extraction`. Ask for conclusions, evidence and decisions. Never ask for the reasoning transcript.

## API and safety boundaries

- **Preserved thinking.** A change to `system`, `tools` or an earlier message, followed by a request that returns thinking blocks, fails the prefix check with a 400 error. Keep history append-only and put new instructions in the newest turn. Claude Code, the Agent SDK and Managed Agents manage history themselves. These are API facts; do not invent matching Claude Code keys.
- **Model switches.** Fable 5.1 and Opus 5.5 cannot read Fable 5.2 thinking blocks. After a router switch or a safeguard fallback away from Fable 5.2, the next turns run without that reasoning.
- **Advisor.** A Fable 5.2 executor accepts only Fable 5.2 or Mythos 5.2 as its advisor. `references/41-claude-code-runtime-features.md` owns the pair table.
- **Computer use.** `computer_20251124` returns a 400 error except on Amazon Bedrock. Use `computer_toolset_20260801`.
- **Safeguards.** Refusal categories are `cyber`, `bio`, `frontier_llm`, `reasoning_extraction` and `general_harms`. Read `references/41-claude-code-runtime-features.md` before selection, because fallback can change the serving model. Never bypass a safeguard or install a local fallback. Keep refusal, fallback and unknown serving identity visible in reports.

## Sources and limits

Verified 14 November 2026. The behaviour statements are vendor test results; local calibration is unrun. The system card was not read, so no gate is weakened on its account.

- [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2)
- [Fable 5.2 migration guide](https://platform.claude.com/docs/en/models/fable-5-2/migration-guide)
- [Models overview](https://platform.claude.com/docs/en/models/overview)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Claude Code model configuration](https://code.claude.com/docs/en/model-config)
- [Fable 5.2 and Mythos 5.2 release](https://www.anthropic.com/claude-fable-and-mythos-5-2)
