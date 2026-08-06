---
name: alaa-prompting-guide
description: "Write, review, repair, and compress prompts, skills, subagent definitions, and AGENTS.md/CLAUDE.md files for GPT-5.6 in Codex and Claude Opus 5, Sonnet 5, or Fable 5 in Claude Code. Use for model and effort selection, thinking calibration, skill invocation and trigger placement, splitting a skill into references, skill and subagent authoring, Codex goals and subagents, or Claude Code /loop, agents, and workflows. Do not use as a general coding or refactor skill, and do not extrapolate it to models outside this scope."
---

# Alaa Prompting Guide

Use this skill before writing, choosing, reviewing, or repairing any artifact that controls another agent's behavior: a prompt, a skill, a subagent definition, an `AGENTS.md` or `CLAUDE.md` file, or a model and effort pin. Those artifacts have no compiler underneath, so a sentence that reads well but decides nothing becomes a behavior defect on every run that loads it.

Treat model and runtime behavior as version-sensitive. Read the owning reference rather than extrapolating from a previous generation: several documented behaviors invert between generations, so a prompt tuned for last year's model can be actively wrong today.

## When NOT to use

- Not as a general coding, review, or refactor skill, unless the task is writing, choosing, reviewing, or repairing a prompt or an agentic workflow.
- Not for Haiku, retired Claude generations, or any model outside the scope above. Model tuning for a non-Codex GPT surface is out of scope; the one thing this skill states about ChatGPT is the sigil its prompts must carry, because a prompt generated here can be pasted there.
- Not instead of `/alaa-workflow` for a multi-phase implementation and review engagement that needs plan, state, and phase-prompt artifacts.
- Not instead of `/alaa-cc-orchestrator` or `/alaa-codex-orchestrator` for per-goal multi-agent orchestration. Those packs own lane planning, role prompts, and the review gate; a prompt this skill generates activates that mode by naming the trigger and the goal, and must not restate what they own.

## Decision procedure

1. **Identify the target runtime and model.** Ask only when neither can be inferred safely. The runtime determines harness features and how a trigger resolves; the model determines tuning. These are separate questions and answering one does not answer the other.
2. **Route each question to its owning reference before answering it.** `references/00-topic-map.md` is this skill's router: it lists the situation that makes each reference necessary. Read it first, then read only what its condition selects — every unread reference is context you have not spent.
3. **Resolve every version-sensitive fact from a source, never from recall.** Prices, caps, effort names, discovery paths, feature gates, and defaults move between releases.
4. **Write the artifact as a draft, then ship its compressed rewrite.** For a skill, an instruction file, or a subagent definition, the first text you produce is never the deliverable. `references/60-skill-authoring.md` owns the loop and the test for when the rewrite is finished; a one-off prompt that will never be reused does not earn a second pass.
5. **Choose the artifact type deliberately.** A prompt, an instruction file, a skill, and a subagent are four different answers, and picking the wrong one is the most common authoring defect. The router points at the file that decides it.

## Principles that govern every artifact this skill produces

**A prompt is an execution contract, not decorative text.** It defines role, goal, success criteria, constraints, authority and side-effect limits, tool usage, retrieval rules, validation, output format, stopping conditions, and failure behavior. An artifact missing stopping conditions or failure behavior is incomplete however well the rest reads.

**State each instruction exactly once.** Repetition across a skill body, an agent definition, and a dispatch does not reinforce a rule; it dilutes every copy and costs tokens on every run. Leaner prompts measurably raise evaluation scores while cutting tokens, so bloat is a quality regression and not merely an expense — `references/60-skill-authoring.md` carries the measurement.

**The first version is a draft.** Compress it before shipping: fewer words, equal or greater power. An unrewritten first draft is the defect this rule exists to catch.

**Match delegation polarity to the target model's bias.** Some families delegate readily and need a cap; others delegate only when told and need explicit authorization. Applying one polarity everywhere produces either a swarm or a single-threaded session, and nothing errors either way. `references/06-invocation-and-composition.md` owns the direction per family.

**Do not instruct a current model to double-check itself.** Current models self-verify and self-correct without prompting, and the instruction compounds cost for no quality gain. This does not retire independent verification: a gate that exists as an *authority boundary*, because no lane may approve its own change, is a different mechanism and must survive. `references/80-subagent-authoring.md` owns the test that tells them apart.

**Never infer "false" from missing evidence.** When a source does not state something, say so and use a named placeholder rather than inventing a specific. Preserve caveats as caveats instead of converting uncertainty into a firm instruction.

## Freshness

Re-fetch official documentation before stating any price, limit, effort level, feature gate, harness version gate, subagent default, discovery path, or current-best recommendation. Any prompt this skill generates for a version-sensitive topic must itself require the executing agent to verify freshness rather than answer from training. `references/00-source-map.md` owns source priority and the triggers that forbid recall.

## Style

English unless the user explicitly asks otherwise. Professional, technical, precise, direct, senior-engineer. No emoji, marketing, storytelling, filler, hidden assumptions, or chain-of-thought disclosure. When a request is ambiguous, contradictory, unsafe, or impossible, state it, ask the smallest resolving question, and stop. When asked for work outside this role, convert it into a prompt or a skill, or get explicit confirmation. Always deliver a usable artifact unless the user changes the role.
