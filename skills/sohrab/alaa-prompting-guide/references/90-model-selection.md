# Model Selection and Companion Routing

## Quick comparison

| Model | Runtime / trigger | Default use | Effort | Notable |
|---|---|---|---|---|
| GPT-5.6 `sol` | Codex / `/name` | Frontier Codex work: review, security, architecture, hard implementation | `reasoning.effort` `none`–`max`; `medium` recommended start | Programmatic Tool Calling, persisted reasoning, Pro mode |
| GPT-5.6 `terra` | Codex / `/name` | Balanced default for routine implementation and diagnosis | same range | Best cost/quality for ordinary lanes |
| GPT-5.6 `luna` | Codex / `/name` | High-volume bounded work: exploration, command execution, docs | same range | Cheapest evidence tier |
| Opus 5 | Claude Code / `/name` | Default top tier: leading, review, architecture, subtle bugs, escalated implementation | `low`–`max`; `xhigh` recommended for coding and agentic work | Delegates readily, self-verifies, self-corrects |
| Sonnet 5 | Claude Code / `/name` | Balanced default for routine implementation and evidence lanes | `low`–`max`; `high` default | Literal instruction following; more aggressive tool use |
| Fable 5 | Claude Code / `/name` | Opt-in specialist: genuinely multi-day autonomy, heaviest sustained fan-out | `low`–`max`; `high` default | Refusal domains make it unsuitable for security lanes |

Re-check `references/00-source-map.md` before quoting costs, limits, defaults, or feature gates. Cross-vendor prices are not comparable.

## Decision helper

1. **Pick the runtime first.** It determines trigger syntax, harness features, and which model families are even available. Codex means the GPT-5.6 family; Claude Code means the Claude family.
2. **Within Claude Code**, choose Sonnet 5 for routine implementation and evidence work, and Opus 5 for anything that must exercise independent owner-level judgment — leading, reviewing, challenging a design, or an implementation lane whose design is not yet decided. Reach for Fable 5 only when the work is genuinely multi-day autonomous, and only after confirming it does not touch a refusal domain.
3. **Within Codex**, choose `luna` for bounded execution and evidence, `terra` for normal engineering judgment, and `sol` only for lanes that must themselves make non-obvious design decisions.
4. **Choose effort separately**, using `references/50-effort-and-thinking.md`. Model and effort are different questions and answering them together produces bad answers to both.
5. **Default down when pinning.** Escalation is earned by decision density, not by surface sensitivity or goal importance. A lane that mechanically applies a ratified value or a precise spec is balanced-tier work on any surface; only lanes that must make non-obvious design decisions earn the top tier, and the criterion is recorded wherever the pin is raised. When uncertain, stay lower — gates catch the rare shortfall, and one justified re-dispatch costs less than habitual top-tier defaults.
6. **Match delegation polarity to the target's bias** before writing delegation language for any model — read `references/06-invocation-and-composition.md` for the rule.
7. **Use the runtime's own `/goal`** for a durable objective; the implementations share a name and nothing else — read `references/11-codex-runtime-features.md` or `references/41-claude-code-runtime-features.md` for which is which.
8. **Route durable multi-phase engagements** with plan, state, and phase artifacts to `/alaa-workflow` rather than duplicating that machinery.

## Companion routing

`/alaa-codex-orchestrator` (Codex) and `/alaa-cc-orchestrator` (Claude Code) are the production multi-agent orchestration packs, each carrying a 21-role catalog for its runtime: core lanes (spec analyst, explorer, researcher, test strategist, implementer with a separate escalated implementer, independent verifier, failure analyst, reviewer, documenter) plus conditionally gated specialists (adversarial review, architecture, security, migration, API contract, dependency audit, accessibility, browser QA, performance, observability, release).

The catalog is a menu rather than a fleet — a typical goal fires three to five roles, because every specialist is gated on a stated condition. Breadth costs nothing per run; imprecise triggers do.

Claude pins: Opus 5 at `xhigh` for the lead, review, adversarial review, security, architecture, and escalated implementation; Opus 5 at `high` for spec analysis, migration safety, failure analysis, and API contract review; Sonnet 5 at `high` for routine implementation, test strategy, performance, observability, release, dependency audit, and accessibility; Sonnet 5 at `medium` for exploration, research, documentation, and browser evidence; Sonnet 5 at `low` for deterministic command execution. Sonnet's ceiling is `high` — above it, change the model.

Codex pins: `sol` at `xhigh` for adversarial review only; `sol` at `high` for the main thread, review, security, architecture, and escalated implementation; `sol` at `medium` for spec analysis, migration safety, and contract review; `terra` at `high` for routine implementation, failure analysis, and performance; `terra` at `medium` for test strategy, research, observability, release, dependency audit, and accessibility; `luna` at `medium` for exploration, documentation, and browser evidence; `luna` at `low` for command execution. Terra's ceiling is `high` and Luna's is `medium`.

In both packs the lead never implements or runs heavy suites itself, the verifier executes commands under a low-priority resource policy, and no lane approves its own change. Prefer these packs over hand-writing a fan-out; the lead is always the session's own model.

Other companions:

- `/alaa-workflow`: durable multi-phase plans, phase prompts, resumable state, and the implementation-plus-review cadence.
- `/openai-docs`: freshest GPT-5.6 and Codex guidance when this skill is stale. Use official Anthropic docs for Claude gaps.
- `/alaa-low-noise`: broad prompt research, validation, or long tool-heavy sessions.

## Caveats

Benchmark claims, relative pricing, effort defaults, and the capability ordering among current models are vendor-stated and time-sensitive — a single release can invalidate any ranking here. Re-check `references/00-source-map.md` and the live model pages before treating any ranking here as current.

## Companion references

Read `references/50-effort-and-thinking.md` for the effort decision procedure, the target model's own file for its tuning, `references/11-codex-runtime-features.md` or `references/41-claude-code-runtime-features.md` for harness features, and `references/80-subagent-authoring.md` for turning a model choice into an agent pin.
