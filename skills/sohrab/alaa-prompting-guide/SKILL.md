---
name: alaa-prompting-guide
description: "Instruction authoring for GPT-6 in Codex and Claude Opus 5.5, Fable 5.2, Sonnet 5.5, or Haiku 5.5 in Claude Code. Use to write, review, repair, and compress prompts, skills, subagent definitions, and AGENTS.md/CLAUDE.md files, or for model and effort capability evidence, thinking calibration, skill invocation, goal composition or rejection, native Claude Advisor, and runtime workflows. Resolve Desktop Code versus Chat or Cowork before writing Claude commands. Do not use as a general coding or refactor skill, and do not extrapolate it to models outside this scope."
---

# Alaa Prompting Guide

Own instruction authoring, model and effort capability evidence, and runtime control mechanics for the stated models and runtimes. The runtime orchestrator owns task allocation and admission for every authority role. Apply it before writing, choosing, reviewing or repairing prompts, skills, subagent definitions, `AGENTS.md` or `CLAUDE.md` files, or pins. Read the current owners, because behavior can invert between generations.

## When NOT to use

- General coding, review or refactoring without instruction or agentic-workflow authoring.
- Retired Claude generations or models outside scope; the historical references are for reference only. GPT tuning outside Codex is excluded, but ChatGPT invocation sigils remain covered for generated prompts.
- Durable multi-phase plans, state and phase prompts: `/alaa-workflow` owns them.
- Per-goal lanes, role prompts and review gates: the runtime orchestrator owns them. A generated prompt names its trigger and goal without restating its contract.

## The rule-writer specialist

Before dispatching `alaa-rule-writer`, read `assets/rule-writer/dispatch.md`, which also owns its task controls. The specialist rewrites an existing draft and returns replacement text. Authorship, decisions, research and edits stay with the caller.

For personal Claude Code installation, and for installing `assets/rule-writer/codex/alaa-rule-writer.toml` into `~/.codex/agents`, follow the repository-root `install-skills.md`. Never write an installation sentinel, and never run the grants checker as an install gate.

After changing `assets/rule-writer/`, run `python3 scripts/check_rule_writer_grants.py`.

## Codex policy validation

When you need to know what a policy file owns or decides, read `references/90-model-selection.md`. Main-session controls stay externally configured. After a change to `assets/codex-model-policy.json` or a pin, run `python3 scripts/check_codex_model_policy.py --agent-root assets/rule-writer/codex` from this skill directory. Repeat `--agent-root` for another pack.

## Claude policy validation

`references/90-model-selection.md` also states what this policy file owns; it sets no role default. After a change to `assets/claude-model-policy.json` or a projection, run `python3 scripts/check_claude_model_policy.py` from this skill directory. The default covers both managed roots. Repeat `--agent-root <path>` for a selected source or generated subset. Use `--policy <path>` for an explicit policy.

The gate needs the repository-root checker's bundled YAML parser. A verified aggregate can discharge an identical covered command, and the orchestrator owns that consolidation. Uncovered managed roots still need their checks. Source agreement proves neither installed activation nor calibration.

All gates exit `0` when clean, `1` on findings and `2` on unavailable proof, including malformed or unreadable input. Either nonzero code blocks the affected completion. Repair the stated cause within the active retry budget, or report blocked. Static checks prove neither live acceptance nor instruction compliance.

## Decision procedure

1. Identify the runtime, surface and model. Ask only for missing facts that change the artifact. A Desktop app name proves no tab's command support.
2. Read `references/00-topic-map.md` before answering, and load only the references whose conditions hold.
3. Resolve version-sensitive facts from sources, never from recall.
4. Draft, then compress, every controlling artifact through `references/60-skill-authoring.md`, including edits and dispatches. Ship the fewest words that preserve behavior. Soft targets yield. Hard limits require equivalent restructuring or a blocked report. Conversational prose is exempt.
5. Choose between a prompt, an instruction file, a skill and a subagent through its routed owner.

For a goal, follow `references/06-invocation-and-composition.md` for the kickoff and the completion condition. `/alaa-workflow` owns plans and the mappings of phases and tasks to skills.

For a rendered Claude condition, run `python3 scripts/check_goal_condition.py --surface claude-desktop-code --condition-file <path>` from this skill directory, substituting the observed surface.

## Principles that govern every artifact this skill produces

**Complete contract.** Define the role, goal, success criteria, constraints, authority and side effects, tools, retrieval, validation, output, stopping and failure behavior.

**One instruction, one owner.** Duplication dilutes the contract. Check each reduction against the same acceptance criteria through `references/60-skill-authoring.md`.

**Model-specific delegation.** Over-delegation needs bounds. Reticence needs authorization. Read `references/06-invocation-and-composition.md` before you tune either.

**Proportional verification.** Preserve focused checks and independent acceptance. Remove a repeated check only when no input changed, nothing failed and no concern is unresolved. A model upgrade proves no correctness. `references/80-subagent-authoring.md` owns the authority test.

**Missing evidence stays unknown.** Say what the source omits, use a named placeholder and preserve caveats.

## Freshness

Before you state a price, limit, effort level, feature or version gate, default, discovery path or current recommendation, refresh the official sources through `references/00-source-map.md`. A generated prompt on a volatile topic must require the executing agent to check freshness.

## Stop

Finish when the usable artifact preserves its intended contract and the required gates pass. When the work is ambiguous, contradictory, unsafe or impossible, state the blocker, ask the smallest resolving question and stop. Source work grants no installation, commit, publication or external mutation authority.

## Style

Use precise, direct technical English unless requested otherwise. Write no emoji, marketing, storytelling, filler or hidden assumptions, and disclose no chain of thought. For work outside this role, provide a prompt or a skill, or obtain explicit confirmation. Deliver a usable artifact unless the user changes the role.
