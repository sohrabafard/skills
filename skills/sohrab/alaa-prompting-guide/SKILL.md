---
name: alaa-prompting-guide
description: Write, review, and repair prompts for GPT-5.6 in Codex and Claude Opus 4.8, Sonnet 5, or Fable 5 in Claude Code. Use for model selection, model-specific tuning, $ vs / skill triggers, Codex /goal and subagents, or Claude Code /loop, agents, and workflows.
---

# Alaa Prompting Guide

## Purpose

Use this skill before writing, choosing, reviewing, or repairing a prompt for GPT-5.6 in Codex or Claude Opus 4.8, Sonnet 5, or Fable 5 in Claude Code. Treat model/runtime behavior as version-sensitive: read the owned reference instead of extrapolating from older models.

## When NOT to use

- Do not use this as a general coding, review, or refactor skill unless the task is about writing, choosing, reviewing, or repairing a prompt or agentic model workflow.
- Do not extrapolate its guidance to Haiku, older Claude generations, non-Codex GPT surfaces, or other models outside the v1 scope.
- Do not use it instead of `$alaa-workflow` for a full multi-phase implementation/review engagement with plan, state, and phase-prompt artifacts.

## Workflow

1. Identify the target runtime and model. Ask only when neither can be inferred safely.
2. Read `references/05-trigger-syntax.md` before naming any skill: this pack uses `$name` for Codex and `/name` for Claude Code.
3. Read the target model file: `10-gpt-5-6.md`, `20-opus-4-8.md`, `30-sonnet-5.md`, or `40-fable-5.md`.
4. For goals, subagents, parallel/background work, or recurring tasks, also read `11-codex-runtime-features.md` or `41-claude-code-runtime-features.md`.
5. For model choice or cross-model comparison, read `90-model-selection.md`.
6. Route durable multi-phase implementation/review work to `$alaa-workflow` or `/alaa-workflow`; do not recreate its plan/state machinery here.

When a prompt authorizes delegation, background work, or parallel lanes, state that permission explicitly and require the parent agent to reconcile results. Do not assume any covered runtime will infer fan-out permission.

## Freshness

Read `references/00-source-map.md` before using version-sensitive facts. Re-fetch official docs for latest/current claims, pricing, limits, effort levels, feature gates, or dated behavior; preserve any caveat instead of converting uncertainty into a firm instruction.
