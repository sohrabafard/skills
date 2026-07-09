# Model Selection and Companion Routing

## Quick comparison

| Model | Runtime/trigger | Default use | Effort | Runtime features |
|---|---|---|---|---|
| GPT-5.6 | Codex / `$name` | Codex work; Sol for frontier, Terra for balance, Luna for volume | `reasoning.effort`: none–max; medium default | Codex `/goal`; explicit subagents/batch |
| Sonnet 5 | Claude Code / `/name` | ordinary coding and agentic work | `effort`: low–max; high default | Claude `/goal`, `/loop`, agents |
| Opus 4.8 | Claude Code / `/name` | deep architecture, review, subtle bugs | `effort`: low–max; high default | same Claude runtime |
| Fable 5 | Claude Code / `/name` | hardest, longest, most ambiguous work | adaptive `effort`: low–xhigh | same runtime; strongest sustained fan-out |

Re-check `00-source-map.md` before quoting costs, limits, defaults, or feature gates. Cross-vendor prices are not directly comparable; among the three Claude tiers, Sonnet is lower, Opus middle, and Fable highest at the referenced research time.

## Decision helper

1. Pick the runtime first; it determines trigger syntax and runtime features. In this v1 scope, Codex means GPT-5.6.
2. In Claude Code, choose Sonnet for routine work, Opus for reasoning-heavy architecture/review, and Fable only after Opus is insufficient or the work needs multi-day autonomy, heavy vision/doc analysis, or frontier synthesis.
3. Use the runtime's own `/goal` for a durable objective; Codex and Claude implementations are not interchangeable.
4. Authorize independent lanes explicitly and require parent synthesis.
5. Route durable GPT-5.6 implementation plus Claude review engagements with plan/state/phase artifacts to `$alaa-workflow` instead of duplicating its machinery.

## Companion routing

- `$alaa-workflow`: durable multi-phase plans, phase prompts, state, and GPT-5.6 implementation plus Claude review cadence.
- `$openai-docs`: freshest GPT-5.6/Codex guidance when this skill is stale; use official Anthropic docs for Claude gaps.
- `$alaa-low-noise`: broad prompt research, validation, or long tool-heavy sessions.
