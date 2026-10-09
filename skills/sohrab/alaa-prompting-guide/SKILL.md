---
name: alaa-prompting-guide
description: "Write, review, repair, and compress prompts, skills, subagent definitions, and AGENTS.md/CLAUDE.md files for GPT-6 in Codex and Claude Opus 5.5, Fable 5.1, Sonnet 5.5, or Haiku 5.5 in Claude Code. Use for model and effort capability evidence, thinking calibration, skill invocation, compact goal conditions, rejected goal prompts, skill and subagent authoring, or runtime workflows. Resolve Desktop Code versus Chat or Cowork before writing Claude commands. Do not use as a general coding or refactor skill, and do not extrapolate it to models outside this scope."
---

# Alaa Prompting Guide

Own instruction authoring, model/effort capability evidence and runtime control mechanics for the stated models and runtimes. The runtime orchestrator owns task allocation and admission for every authority role. Apply before writing, choosing, reviewing or repairing prompts, skills, subagent definitions, `AGENTS.md`/`CLAUDE.md` or pins. Read current owners: behavior can invert between generations.

## When NOT to use

- General coding/review/refactoring without instruction or agentic-workflow authoring.
- Retired Claude generations or models outside scope; historical references support explicit comparisons only. Non-Codex GPT tuning is excluded; ChatGPT invocation sigils remain covered for generated prompts.
- Durable multi-phase plans/state/phase prompts: `/alaa-workflow` owns them.
- Per-goal lanes, role prompts and review gates: the runtime orchestrator owns them. Generated prompts name its trigger and goal without restating its contract.

## The rule-writer specialist

Before dispatching `alaa-rule-writer`, read `assets/rule-writer/dispatch.md`. It rewrites an existing draft and returns replacement text; authorship, decisions, research and edits stay with the caller.

Distributing it is not this skill's job. Under Claude Code the definition ships inside the plugin and loads from the plugin-root `agents/` directory once the plugin is installed or enabled, and the plugin manifest version is the installed agent-pack version: never copy a wrapper into `~/.claude/agents`, never write an installation sentinel, and never run the grants checker as an install gate. Under Codex, `install-skills.md` at this repository's root owns the one command that places `assets/rule-writer/codex/alaa-rule-writer.toml` into `~/.codex/agents`.

Managed wrappers omit model and effort; the orchestrator explicitly selects both controls for each task, including rule-writer. Validate effective controls separately from role authority. After changing `assets/rule-writer/`, run `python scripts/check_rule_writer_grants.py`; after checker changes also run `--self-test`.

## Codex policy validation

`assets/codex-model-policy.json` owns supported-effort snapshots and model-neutral role/artifact registrations. It chooses no task pair; main controls stay externally configured. From this skill directory, after policy/pin changes run `python scripts/check_codex_model_policy.py --agent-root assets/rule-writer/codex`; repeat `--agent-root` for another pack. After corpus changes run `python scripts/check_agent_evals.py`. Add `--self-test` to each changed checker.

## Claude policy validation

`assets/claude-model-policy.json` owns Claude capabilities, model availability conditions and model-neutral role/artifact registrations. Task comparisons remain separate evidence, never role defaults. From this skill directory run
`python scripts/check_claude_model_policy.py` after policy or projection changes; add `--self-test`
after checker changes. Defaults cover both managed roots. Repeat `--agent-root <path>`
for selected source/generated subsets, or use `--policy <path>` for an explicit policy.
Run `python scripts/check_claude_agent_evals.py` for the separate Claude comparison corpus;
add `--self-test` after changing its checker and `--results <path>` to validate evidence.
After shared projection/control changes, run `python scripts/profile_projection.py --self-test`; both policy self-tests cover explicit task controls for every role. These gates require the root checker's bundled YAML parser. A verified aggregate can discharge an identical covered command; the orchestrator owns consolidation. Uncovered managed roots still require checks. Source agreement proves neither installed activation nor calibration.

All gates use `0` clean, `1` findings, `2` unavailable proof (including malformed/unreadable input). Either nonzero blocks the affected completion; repair the stated cause within the active retry budget or report blocked. Static checks prove neither live acceptance nor instruction compliance.

## Decision procedure

1. Identify runtime, surface and model. Ask only for missing facts that change the artifact; a Desktop app name proves no tab's command support.
2. Read `references/00-topic-map.md` before answering; load only references whose conditions hold.
3. Resolve version-sensitive facts from sources, never recall.
4. Draft, then compress every controlling artifact, including edits and dispatches, through `references/60-skill-authoring.md`. Ship the fewest words preserving behavior. Soft targets yield; hard limits require equivalent restructuring or a blocked report. Conversational prose is exempt.
5. Choose prompt, instruction file, skill or subagent through its routed owner.

For a goal, follow `references/06-invocation-and-composition.md` for the compact condition and kickoff; `/alaa-workflow` owns plans and phase/task skill mappings.

For a rendered Claude condition, run `python scripts/check_goal_condition.py --surface claude-desktop-code --condition-file <path>` here, substituting the observed surface. After checker changes also run `--self-test`.

## Principles that govern every artifact this skill produces

**Complete contract.** Define role, goal, success criteria, constraints, authority/side effects, tools, retrieval, validation, output, stopping and failure behavior.

**One instruction, one owner.** Duplication dilutes the contract. Compare reductions against the same acceptance criteria through `references/60-skill-authoring.md`.

**Model-specific delegation.** Over-delegation needs bounds; reticence needs authorization. Read `references/06-invocation-and-composition.md` before tuning either.

**Proportional verification.** Preserve focused checks and independent acceptance. Remove repetition only without changed inputs, failures or unresolved concerns; a model upgrade proves no correctness. `references/80-subagent-authoring.md` owns the authority test.

**Missing evidence stays unknown.** Say what the source omits, use a named placeholder and preserve caveats.

## Freshness

Before stating prices, limits, effort levels, feature/version gates, defaults, discovery paths or current recommendations, refresh official sources through `references/00-source-map.md`. Generated prompts for volatile topics must require executing-agent freshness checks.

## Stop

Finish when the usable artifact preserves its intended contract and required gates pass. For ambiguity, contradiction, unsafe or impossible work, state the blocker, ask the smallest resolving question and stop. Source work grants no installation, commit, publication, external mutation or paid-comparison authority.

## Style

Use precise, direct technical English unless requested otherwise. No emoji, marketing, storytelling, filler, hidden assumptions or chain-of-thought disclosure. For work outside this role, provide a prompt/skill or obtain explicit confirmation. Deliver a usable artifact unless the user changes the role.
