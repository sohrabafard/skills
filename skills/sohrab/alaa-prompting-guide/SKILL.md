---
name: alaa-prompting-guide
description: Write, review, and repair prompts for GPT-5.5 in Codex and Claude Opus 4.8, Sonnet 5, and Fable 5 in Claude Code. Use for model selection, model-specific prompt tuning, $ vs / skill-trigger syntax, Codex /goal and subagents, and Claude Code /loop, Agent subagents, and Workflow prompts.
---

# Alaa Prompting Guide

## Purpose

This is the shared reference any agent in this pack reaches for before writing a prompt aimed at another model — or at itself, when the model is one of the four covered here. It exists because these four models are new enough that habits carried over from older prompts are often wrong: GPT-5.5 needs re-tuned verbosity/effort, not a ported GPT-5.2 stack; Opus 4.8 under-spawns subagents by default where an older Opus over-spawned; Sonnet 5 rejects `temperature` and manual thinking budgets outright; and Fable 5 is not the creative/persona model its name might suggest — it is Anthropic's new top capability tier, above Opus 4.8. Guessing at any of this produces a plausible-sounding prompt that quietly under- or over-shoots the model's real behavior. Read the model's reference file instead of guessing.

## When NOT to use

- Do not use this as a general coding, review, or refactor skill unless the task is about writing, choosing, reviewing, or repairing a prompt or agentic model workflow.
- Do not extrapolate its guidance to Haiku, older Claude generations, non-Codex GPT surfaces, or other models outside the v1 scope.
- Do not use it instead of `$alaa-workflow` for a full multi-phase implementation/review engagement with plan, state, and phase-prompt artifacts.

## The four models in v1

| Model | Runs in | Trigger for this pack's skills | One-line positioning |
|---|---|---|---|
| GPT-5.5 | Codex app/CLI | `$name` | Flagship reasoning model for agentic coding and long-horizon tool use |
| Claude Sonnet 5 | Claude Code | `/name` | Balanced default — best combination of speed and intelligence |
| Claude Opus 4.8 | Claude Code | `/name` | Highest Opus-tier reasoning; strong at bug-finding and review |
| Claude Fable 5 | Claude Code | `/name` | Anthropic's new top tier, above Opus 4.8, for the hardest and longest-running problems |

Scope is deliberately fixed at these four for v1. If a task needs a fifth model (Haiku, an older Opus/Sonnet generation, a non-Codex GPT surface), say so explicitly rather than silently extrapolating this skill's guidance to a model it was not researched for.

## Know your target runtime before you write a single word

The single most common failure mode this skill exists to prevent: writing `$skill-name` into a prompt headed for Claude Code, or `/skill-name` into a prompt headed for Codex. Neither errors — the reference just sits there as inert text, silently doing nothing. Identify which runtime will actually execute the prompt first, then pick the trigger character, then write the rest. Read `references/05-trigger-syntax.md` before producing any prompt that names another skill, and re-read it any time you catch yourself defaulting to whichever character you personally use most often.

## How to use this skill

1. Identify the target model and the runtime it executes in (Codex for GPT-5.5; Claude Code for all three Claude models). If genuinely unsure which model the prompt is for, ask rather than guessing — the tuning advice differs enough between these four that a wrong guess produces a worse prompt than no guidance at all.
2. Read `references/05-trigger-syntax.md` so every skill reference in the prompt you're about to write uses the right character.
3. Read that model's reference file for tone, effort/verbosity tuning, and prompting techniques: `references/10-gpt-5-5.md`, `references/20-opus-4-8.md`, `references/30-sonnet-5.md`, or `references/40-fable-5.md`.
4. If the prompt needs to invoke an agentic feature — a durable objective, subagents, background/parallel jobs, a recurring check-in — read the matching runtime-feature file: `references/11-codex-runtime-features.md` for Codex, or `references/41-claude-code-runtime-features.md` for Claude Code. Both files include ready-to-use templates; adapt them to the actual task instead of pasting them verbatim.
5. If the task is choosing which of the four models to use, or needs the comparison table, read `references/90-model-selection.md`.
6. If the task is a durable, multi-phase plan that needs a GPT-5.5-implements / Claude-reviews cadence with plan/state/phase-prompt artifacts, stop and hand off to `$alaa-workflow` (Codex-side) or `/alaa-workflow` (Claude-side) instead of rebuilding that machinery here — see the companion-routing note in `references/90-model-selection.md`.

## Explicit permission this skill assumes

Every agentic-feature template in `references/11-codex-runtime-features.md` and `references/41-claude-code-runtime-features.md` is written on the assumption that subagents, parallel work, and background jobs are worth using whenever a task has independent lanes. None of these four models fans out on its own without being asked — Codex "only spawns a new agent when you explicitly ask it to," and Claude Code's Agent tool and Workflow tool behave the same way. When you write a prompt for another agent using this skill, say so explicitly in that prompt rather than assuming the target agent will infer permission from context.

## Freshness discipline

All four models postdate a typical training cutoff. Every claim in the reference files below was pulled from a live official-docs fetch during this skill's own research pass, not from memory — and each reference file's "Caveats" section says exactly which claims are time-sensitive (pricing, exact version gates, specific limits) versus durable (the shape of the effort/verbosity controls, the core behavioral tendencies). Before copying a number from this skill into another document, glance at that caveat section, and re-fetch the live page in `references/00-source-map.md` if the task is genuinely sensitive to being current.

## Reference navigation

- `references/00-source-map.md` — source priority, freshness triggers, what each file owns
- `references/05-trigger-syntax.md` — the `$` vs `/` skill-trigger rule, with the one nuance worth knowing
- `references/10-gpt-5-5.md` — GPT-5.5 model-level prompting
- `references/11-codex-runtime-features.md` — Codex's `/goal`, subagents, `spawn_agents_on_csv`, `AGENTS.md`, Agent Skills
- `references/20-opus-4-8.md` — Claude Opus 4.8 model-level prompting
- `references/30-sonnet-5.md` — Claude Sonnet 5 model-level prompting
- `references/40-fable-5.md` — Claude Fable 5 model-level prompting
- `references/41-claude-code-runtime-features.md` — Claude Code's `/loop`, Agent subagents, Workflow tool, plan mode / Ultraplan, and Claude Code's own `/goal`
- `references/90-model-selection.md` — comparison table, decision helper, companion routing to `$alaa-workflow`
