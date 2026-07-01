# Claude Sonnet 5

API model id `claude-sonnet-5`. Anthropic's balanced default: "the best combination of speed and intelligence," the mid-tier workhorse between Opus 4.8 (highest reasoning) and Haiku 4.5 (fastest/cheapest). Anthropic calls it "the most agentic Sonnet model yet," with performance close to Opus 4.8 at lower prices — the largest gains over Sonnet 4.6 are in sustained multi-step tool use, unprompted self-verification, root-cause debugging in brownfield code, and finishing tasks that previously stalled halfway. 1M-token context (default and max, no smaller variant), 128k max output. First Sonnet-tier model with real-time cybersecurity refusal safeguards (a normal `stop_reason: "refusal"`, not an error).

This is the right **default** model for ordinary coding/agentic work in this pack — reach for Opus 4.8 when the task is unusually reasoning-heavy or review-oriented, and for Fable 5 only when the task genuinely needs the highest capability tier (see `references/90-model-selection.md`).

## Effort and thinking

`effort` is the primary lever, not `temperature`/`top_p`/`top_k` (all rejected with a 400 on Sonnet 5) and not manual thinking budgets (`budget_tokens` also rejected — a 400). **Sonnet 5 defaults to `high` effort.** Levels: `max` (no token-spend constraint, frontier problems), `xhigh` (recommended for Sonnet 5's hardest coding/agentic tasks and long agent loops over ~30 minutes), `high` (default — complex reasoning/coding/agentic where quality beats speed/cost), `medium` (balanced step-down, roughly comparable to Sonnet 4.6 at high), `low` (efficient, some capability reduction — suited to high-volume/latency-sensitive work and subagents).

**Adaptive thinking is on by default** — a change from Sonnet 4.6, where omitting `thinking` ran without it. Disable explicitly with `thinking: {type: "disabled"}` if you need it off. Because thinking now counts against the same `max_tokens` output cap, leave generous headroom at `high`/`xhigh`/`max`, or a tight cap can produce a response that's almost all thinking followed by a truncated answer. Sonnet 5's new tokenizer also produces roughly 30% more tokens for the same text than Sonnet 4.6's — recount any budgets tuned on the older model.

## Tone

Concise and natural by default (shared with the current Claude generation): direct, fact-based progress reports, less verbose recaps, may skip a summary after tool calls and move straight to the next action — ask explicitly if you want a post-tool-use summary. Response length scales to task complexity, recalibrated versus Sonnet 4.6 (shorter on simple lookups, longer on genuinely open-ended analysis); re-tune style prompts against this new baseline rather than assuming old Sonnet 4.6 phrasing transfers unchanged. Prefer positive style examples over "don't do X" instructions.

## Prompting techniques that matter most

- Be explicit when you want action versus a suggestion — Sonnet 5 follows literal instructions more strictly and will not silently generalize an instruction from one item to the rest of a task ("apply this to every section, not just the first" must be stated).
- With thinking disabled, Sonnet 5 is less likely to reach for tools on its own — if you must run with thinking off, add an explicit nudge on when to use tools. Raising effort also measurably increases tool-use frequency.
- For review/coding harnesses tuned on older models, expect Sonnet 5 to follow conservative filtering instructions ("only report high-severity issues") more faithfully — this can look like a recall drop even though it investigated just as thoroughly. If you want full coverage, explicitly separate "find everything, including low-confidence items" from a distinct filtering stage.
- For a single well-specified interactive task, front-load intent and constraints in the first turn at `xhigh`/`high` effort — requirements trickled in over many turns cost more efficiency on this model than on prior ones.
- For frontend/design work, generic negative instructions ("don't use that color") tend to just shift Sonnet 5 to a different fixed default rather than producing real variety — and temperature can no longer be used for stylistic variation. Give a concrete visual spec, or ask for several distinct directions to choose from.
- Golden rule from the shared family guidance: if a colleague with minimal context would be confused by the instruction, so will Claude — be as clear and direct as with a new teammate.
- Use 3–5 well-structured `<example>` tags for few-shot steering on complex or format-sensitive tasks; use XML tags to separate instructions/context/input.
- For long-context tasks (20k+ tokens), put long documents near the top of the prompt with the actual query/instructions at the end — cited as up to ~30% quality improvement from this ordering alone.

## Agentic notes

Sonnet 5 tracks remaining context/token budget through a conversation (context awareness). For long-running/multi-context-window work, tell it explicitly that context will be auto-compacted so it should not wrap up early; use a memory tool or structured state files (tests.json-style plus a progress.txt) and commits as checkpoints; give it verification tools (Playwright, computer use) so it can self-check without constant human feedback. It runs parallel/independent tool calls aggressively by default — steerable up or down with an explicit instruction. Prompt it to ask before hard-to-reverse or shared-system actions (force-push, `rm -rf`, dropping tables, posting externally) unless you specifically want it to act autonomously on those too.

## Caveats

Pricing (`$3/$15` per MTok, introductory `$2/$10` through Aug 31, 2026) and the ~30% tokenizer-size claim are time-sensitive figures stated by Anthropic at research time — re-check before quoting them elsewhere. "Defaults to `high` effort" is confirmed for the Claude API and Claude Code; do not assume every third-party surface matches without checking.

## Sources

- [Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5)
- [Prompting best practices (Claude family)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [What's new in Claude Sonnet 5](https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5)
- [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Effort (parameter reference)](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Introducing Claude Sonnet 5](https://www.anthropic.com/news/claude-sonnet-5)

## Companion reference

For Claude Code's shared agentic features (`/loop`, Agent subagents, Workflow tool, plan mode / Ultraplan, Claude Code's own `/goal`), read `references/41-claude-code-runtime-features.md` next.
