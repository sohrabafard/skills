---
name: alaa-prompting-guide
description: "Instruction authoring for GPT-6 in Codex and Claude Opus 5.5, Fable 5.2, Sonnet 5.5, or Haiku 5.5 in Claude Code. Use to write, review, repair, and compress prompts, skills, subagent definitions, and AGENTS.md/CLAUDE.md files, or for model and effort capability evidence, thinking calibration, skill invocation, goal composition or rejection, native Claude Advisor, and runtime workflows. Resolve Desktop Code versus Chat or Cowork before writing Claude commands. Do not use as a general coding or refactor skill, and do not extrapolate it to models outside this scope."
---

# Alaa Prompting Guide

This skill owns instruction authoring, model and effort capability evidence, and runtime control mechanics for the stated models and runtimes. Apply it before you write, choose, review or repair a prompt, a skill, a subagent definition, an `AGENTS.md` or `CLAUDE.md` file, or a pin. Read the current owners: behavior can invert between model generations.

## When NOT to use

- General coding, review or refactoring with no instruction or agentic-workflow authoring.
- Retired Claude generations and models outside scope. GPT tuning outside Codex is excluded; ChatGPT invocation sigils stay covered for generated prompts.
- Durable multi-phase plans, state and phase prompts: `/alaa-workflow` owns them.
- Per-goal lanes, role prompts and review gates, and task allocation and admission for every authority role: the runtime orchestrator owns them. A generated prompt names the orchestrator's trigger and goal and does not restate its contract.

## Decision procedure

1. Identify the runtime, the surface and the model. Ask only for a missing fact that changes the artifact. A Desktop app name proves no tab's command support.
2. Read `references/00-topic-map.md` before you answer, and load only the references whose conditions hold.
3. Resolve a version-sensitive fact from its source, never from recall. Before you state a price, limit, effort level, feature or version gate, default, discovery path or current recommendation, refresh the official source through `references/00-source-map.md`. A generated prompt on a volatile topic requires the executing agent to check freshness.
4. Draft, then compress, every controlling artifact through `references/60-skill-authoring.md`, edits and dispatches included. Ship the fewest words that preserve behavior. A soft target yields. A hard limit requires equivalent restructuring or a blocked report. Conversational prose is exempt.
5. Choose between a prompt, an instruction file, a skill, a script and a subagent through that same reference.
6. For a Claude target, apply `references/41-claude-code-runtime-features.md` section *Prompts for a session that may have an advisor* before you ship a prompt, a system prompt or a dispatch.

For a goal, take the kickoff and the completion condition from `references/06-invocation-and-composition.md`. For a rendered Claude condition, run `python3 scripts/check_goal_condition.py --surface claude-desktop-code --condition-file <path>` from this skill directory, with the observed surface substituted.

## Principles for every artifact

- **Complete contract.** Define the role, goal, success criteria, constraints, authority and side effects, tools, retrieval, validation, output, stop and failure behavior.
- **One instruction, one owner.** Duplication dilutes the contract. Check each reduction against the same acceptance criteria through `references/60-skill-authoring.md`.
- **Model-specific delegation.** Over-delegation needs bounds, and reticence needs authorization. Read `references/06-invocation-and-composition.md` before you tune either.
- **Proportional verification.** Keep focused checks and independent acceptance. Remove a repeated check only when no input changed, nothing failed and no concern is unresolved. A model upgrade proves no correctness. `references/80-subagent-authoring.md` owns the authority test.
- **Missing evidence stays unknown.** Say what the source omits, use a named placeholder and keep caveats.
- **Style.** Write precise, direct technical English unless asked otherwise: no emoji, marketing, storytelling, filler or hidden assumption, and no disclosed chain of thought.

## Stop

- Finish when the usable artifact preserves its intended contract and the required gates pass.
- When the work is ambiguous, contradictory, unsafe or impossible, state the blocker, ask the smallest resolving question and stop.
- For work outside this role, provide a prompt or a skill, or get explicit confirmation first.
- Source work grants no installation, commit, publication or external mutation authority.

## The rule-writer specialist

`alaa-rule-writer` rewrites an existing draft and returns replacement text. Authorship, decisions, research and edits stay with the caller. Before you dispatch it, read `assets/rule-writer/dispatch.md`, which also owns its task controls.

To install it for personal Claude Code, or to install `assets/rule-writer/codex/alaa-rule-writer.toml` into `~/.codex/agents`, follow the repository-root `install-skills.md`. Never write an installation sentinel, and never run the grants checker as an install gate.

## Gates

Run each gate from this skill directory. `references/90-model-selection.md` states what each policy file owns. Neither policy sets a role default, and main-session controls stay externally configured.

- After a change to `assets/rule-writer/`: `python3 scripts/check_rule_writer_grants.py`.
- After a change to `assets/codex-model-policy.json` or a Codex pin: `python3 scripts/check_codex_model_policy.py --agent-root assets/rule-writer/codex`. Repeat `--agent-root` for another pack.
- After a change to `assets/claude-model-policy.json` or a Claude projection: `python3 scripts/check_claude_model_policy.py`. The default covers both managed roots. Repeat `--agent-root <path>` for a selected source or generated subset, and use `--policy <path>` for an explicit policy. This gate needs the repository-root checker's bundled YAML parser.

Each gate exits `0` clean, `1` on findings and `2` on unavailable proof, malformed or unreadable input included. Either nonzero code blocks the affected completion: repair the stated cause within the active retry budget, or report blocked. A verified aggregate can discharge an identical covered command; the orchestrator owns that consolidation, and uncovered managed roots still need their checks. A static check proves no installed activation, calibration, live acceptance or instruction compliance.
