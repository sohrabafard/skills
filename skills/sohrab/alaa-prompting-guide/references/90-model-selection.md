# Model Selection and Companion Routing

## Quick comparison

|                                                | GPT-5.5                                                                            | Claude Sonnet 5                                                                    | Claude Opus 4.8                                                                    | Claude Fable 5                                                                                                |
|------------------------------------------------|------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| Runtime in this pack                           | Codex app/CLI                                                                      | Claude Code                                                                        | Claude Code                                                                        | Claude Code                                                                                                   |
| Skill trigger                                  | `$name`                                                                            | `/name`                                                                            | `/name`                                                                            | `/name`                                                                                                       |
| Positioning                                    | Flagship reasoning model for agentic coding/tool-use                               | Balanced default: best speed/intelligence combination                              | Highest Opus-tier reasoning; strong at bug-finding/review                          | New top tier, above Opus 4.8; hardest/longest-running problems                                                |
| Reach for it when                              | The task runs inside Codex, or needs `/goal` / `spawn_agents_on_csv` batch fan-out | Default choice for ordinary coding/agentic work                                    | The task is unusually reasoning-heavy, architecture-sensitive, or is a review pass | The task is at the edge of what Opus 4.8 reliably handles, or must sustain itself autonomously for many hours |
| Effort/reasoning control                       | `reasoning.effort`: none/low/medium(default)/high/xhigh                            | `effort`: low/medium/high(default)/xhigh/max                                       | `effort`: low/medium/high(default)/xhigh/max                                       | `effort`: low/medium/high(default)/xhigh (adaptive thinking only)                                             |
| Durable-objective feature                      | Codex `/goal` (thread-scoped state machine, evidence-checked)                      | Claude Code `/goal` (Stop-hook + evaluator model) — same name, different mechanism | same as Sonnet 5                                                                   | same as Sonnet 5                                                                                              |
| Recurring/interval feature                     | none found in Codex docs                                                           | `/loop`                                                                            | `/loop`                                                                            | `/loop`                                                                                                       |
| Subagent delegation                            | explicit only; `default`/`worker`/`explorer` roles, `max_depth` 1 by default       | Agent tool; nested up to depth 5; foreground or background                         | same as Sonnet 5                                                                   | same as Sonnet 5, and documented as more reliable at sustaining parallel subagents than Opus 4.8              |
| Cost tier (per official docs at research time) | not directly comparable (different vendor pricing model)                           | lowest of the three Claude models                                                  | mid                                                                                | highest — steep premium over Opus 4.8                                                                         |

Do not treat the cost/effort figures as permanently fixed — see each model's own reference file for the exact numbers
and their "Caveats" section, and re-check `references/00-source-map.md` before quoting a price or limit elsewhere.

## Decision helper

1. **Is the target runtime Codex or Claude Code?** This is not optional — it decides the trigger character (
   `references/05-trigger-syntax.md`) and which feature set applies (`references/11-*` vs `references/41-*`). If the
   runtime is Codex, the model is GPT-5.5 by definition in this pack's v1 scope.
2. **If the runtime is Claude Code, which of the three models fits the task?**
    - Ordinary coding, refactors, most agentic tool-use → **Sonnet 5**.
    - Deep architecture decisions, multi-step production-readiness review, anything where finding subtle bugs matters
      more than speed → **Opus 4.8**.
    - A problem that has already resisted Opus 4.8, a multi-day autonomous run, or work at genuinely frontier
      difficulty → **Fable 5**, and expect to pay for it.
3. **Does the task need a durable objective that outlives one prompt?** Use the runtime's own `/goal` (Codex or Claude
   Code — they are not interchangeable, see each runtime file) rather than trying to simulate persistence with a single
   giant prompt.
4. **Does the task decompose into independent lanes?** Authorize subagents/parallel work explicitly — none of these four
   models fans out on its own without being asked.
5. **Is this a durable, multi-phase plan that needs a GPT-5.5-implements / Claude-reviews cadence with
   plan/state/phase-prompt artifacts?** Stop here and hand off to `$alaa-workflow` instead of building that structure ad
   hoc — it already owns phase prompt packs, continuation state, and the Opus review-prompt shape. This skill's job is
   making any single prompt to any of the four models good; `$alaa-workflow`'s job is orchestrating a whole multi-phase
   engagement across two of them. Do not duplicate its plan/state machinery here.

## Companion routing

- `$alaa-workflow` — durable multi-phase plans, phase prompt packs, GPT-5.5-implement + Claude-review cadence,
  subagent/parallel-lane orchestration across a whole engagement.
- `$openai-docs` (Codex-side system skill) — freshest GPT-5.5/Codex specifics when this skill's own Codex references are
  stale; no equivalent bundled skill exists on the Claude side, so lean on `references/20-*` through `references/41-*`
  plus the official Anthropic docs in `references/00-source-map.md`.
- `$alaa-low-noise` — pair with any non-trivial prompt-writing session that risks noisy logs or oversized status
  chatter, same as every other skill in this pack.
