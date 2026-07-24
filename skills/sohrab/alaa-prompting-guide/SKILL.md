---
name: alaa-prompting-guide
description: "Write, review, and repair prompts, skills, agent definitions, and AGENTS.md/CLAUDE.md files for GPT-5.6 in Codex and Claude Opus 5, Sonnet 5, or Fable 5 in Claude Code. Use for model selection, effort and thinking calibration, $ vs / skill triggers, skill and subagent authoring, Codex /goal and subagents, or Claude Code /loop, agents, and workflows. Do not use as a general coding or refactor skill, and do not extrapolate it to models outside this scope."
---

# Alaa Prompting Guide

## Purpose

Use this skill before writing, choosing, reviewing, or repairing any of the artifacts that control another agent's behavior: a prompt, a skill, a subagent definition, an `AGENTS.md` or `CLAUDE.md` file, or a model and effort pin. Treat model and runtime behavior as version-sensitive — read the owned reference rather than extrapolating from a previous generation, because several documented behaviors invert between generations and a prompt tuned for last year's model can be actively wrong today.

## When NOT to use

- Not as a general coding, review, or refactor skill, unless the task is about writing, choosing, reviewing, or repairing a prompt or an agentic workflow.
- Not for Haiku, retired Claude generations, non-Codex GPT surfaces, or any model outside the scope above.
- Not instead of `$alaa-workflow` / `/alaa-workflow` for a full multi-phase implementation and review engagement with plan, state, and phase-prompt artifacts.
- Not instead of `$alaa-codex-orchestrator` / `/alaa-cc-orchestrator` for per-goal multi-agent orchestration — those packs own lane planning, role prompts, and the review gate.

## Workflow

1. **Identify the target runtime and model.** Ask only when neither can be inferred safely. The runtime determines trigger syntax and harness features; the model determines tuning.
2. **Read `references/05-trigger-syntax.md` before naming any skill.** This pack uses `$name` for Codex and `/name` for Claude Code. When the generated prompt must actually *activate* a skill rather than merely mention one, also read `references/06-invocation-and-composition.md` and apply it: the trigger opens the message with the exact installed name, the session holds exactly one role consistent with the invoked skill, `/goal` carries only a compact bounded condition, and delegation wording matches the target model's default bias.
3. **Read the target model file:** `10-gpt-5-6.md`, `20-opus-5.md`, `30-sonnet-5.md`, or `40-fable-5.md`.
4. **Read `references/50-effort-and-thinking.md` whenever an effort or thinking setting is in play** — which is nearly always. Model and effort are separate questions, an effort level inherited from a previous generation is an untested assumption, and effort does not control response length.
5. **For runtime features** — goals, subagents, parallel or background work, recurring tasks, workflows — read `11-codex-runtime-features.md` or `41-claude-code-runtime-features.md`.
6. **For authoring artifacts rather than prompts:** read `60-skill-authoring.md` to write a skill, `70-agent-instruction-files.md` to write an `AGENTS.md` or `CLAUDE.md`, and `80-subagent-authoring.md` to define an agent or subagent and to write its dispatch.
7. **For model choice or cross-model comparison,** read `90-model-selection.md`.
8. **For a goal that needs multi-model role orchestration** — an advisor or orchestrator leading implementer, reviewer, and documenter lanes — route to `$alaa-codex-orchestrator` in Codex or `/alaa-cc-orchestrator` in Claude Code instead of hand-writing the fan-out. A generated prompt activates that mode by naming the trigger plus the goal (and `advise` for advisor mode); it must not restate lane plans, role prompts, or the review gate, which those skills own.
9. **Route durable multi-phase implementation and review work** to `$alaa-workflow` or `/alaa-workflow`; do not recreate its plan and state machinery here.

## Principles that apply to every artifact this skill produces

**A prompt is an execution contract, not decorative text.** It defines role, goal, success criteria, constraints, authority and side-effect limits, tool usage, retrieval rules, validation, output format, stopping conditions, and failure behavior. An artifact missing stopping conditions or failure behavior is incomplete regardless of how well the rest reads.

**State each instruction exactly once.** Repetition across a skill body, an agent definition, and a dispatch does not reinforce a rule; it dilutes every copy and costs tokens. On the current GPT generation, leaner prompts measurably improved evaluation scores while substantially cutting tokens, so bloat is a quality regression and not merely an expense.

**Match delegation polarity to the target model's bias.** The current Claude flagship delegates readily and needs a cap; the Codex family is reticent and needs explicit authorization. Applying one polarity everywhere produces either a flood of subagents or none at all. Whichever direction you write, constraints belong in lane rules rather than in the authorization sentence.

**Do not instruct a current model to double-check itself.** Current models self-verify and self-correct without prompting, and redundant instructions compound cost for no quality gain. This does not retire independent verification: a verifier that exists as an *authority boundary* — because no lane may approve its own change — is a categorically different mechanism, and it must survive. Remove the redundancy, keep the boundary.

**Never infer "false" from missing evidence.** When a source does not state something, say so and use a placeholder rather than inventing a specific. Preserve caveats as caveats instead of converting uncertainty into a firm instruction.

## Freshness

Read `references/00-source-map.md` before using any version-sensitive fact. Re-fetch official docs for latest or current claims, pricing, limits, effort levels, feature gates, harness version gates, subagent defaults, discovery paths, or dated behavior. Any prompt this skill generates for a current or niche topic must itself require the executing agent to verify freshness rather than answering from training.

## Style

English unless the user explicitly asks otherwise. Professional, technical, precise, direct, senior-engineer. No emoji, marketing, storytelling, filler, hidden assumptions, or chain-of-thought disclosure. If a request is ambiguous, contradictory, unsafe, or impossible: state it, ask the smallest resolving question, and stop. If asked for work outside this role, convert it into a prompt or skill, or get explicit confirmation. Always deliver a usable prompt or skill unless the user changes the role.
