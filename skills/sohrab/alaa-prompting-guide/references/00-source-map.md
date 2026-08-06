# Source Map

Ground every version-sensitive claim here. This file decides which source wins and when recall is forbidden; `references/00-topic-map.md` decides which reference answers a question. They are different jobs and neither restates the other.

## Source priority

1. Explicit user instructions for the current task.
2. The target model's reference plus its runtime reference in this skill.
3. Live official documentation:
   - GPT-5.6: `https://developers.openai.com/api/docs/guides/latest-model`, `https://developers.openai.com/api/docs/models`
   - Codex and ChatGPT skills, commands, and agent files: `https://learn.chatgpt.com/docs/build-skills`, `https://learn.chatgpt.com/docs/developer-commands`, and the Codex pages under `https://developers.openai.com/codex/` for `use-cases/follow-goals`, `subagents`, `guides/agents-md`, and `config-reference`
   - Claude prompting: `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices` plus the model-specific Opus 5, Sonnet 5, and Fable 5 pages under that path
   - Claude facts and runtime: `https://platform.claude.com/docs/en/about-claude/models/overview`, `https://platform.claude.com/docs/en/build-with-claude/effort`, and the `https://code.claude.com/docs/en/` pages `skills`, `sub-agents`, `workflows`, `scheduled-tasks`, `permission-modes`, `ultraplan`, and `goal`
4. `/openai-docs` for current OpenAI guidance. Use community sources only as corroboration after official sources fail to answer.

A redirect is a signal, not a detour: `developers.openai.com/codex/skills` now returns a permanent redirect to the `learn.chatgpt.com` skills page, so a citation to the old path is stale even though it still resolves. When a documented URL redirects across hosts, cite the destination and update the reference that named the origin.

## Freshness triggers

Re-fetch before stating any price, token limit, effort or verbosity name, version, default, flag, feature gate, goal or loop behavior, subagent nesting or concurrency limit, discovery path, or current-best recommendation, and before carrying forward any fact newer than the citing file's freshness stamp.

Three areas are volatile enough that carrying a value forward is a defect rather than a shortcut: harness version gates and hard limits in Claude Code, subagent spawning defaults and depth behavior, and the exact discovery paths for skills and agent definitions in both runtimes. Each has changed in ways that silently broke prompts written against the previous documentation — silently, because nothing errors when a prompt requests a capability the harness no longer exposes under that name.

## Cross-agent packaging contract

- Keep one portable `SKILL.md` package for Codex and Claude Code.
- Keep agent-neutral behavior in `SKILL.md` and `references/`. `agents/openai.yaml` is Codex interface metadata only, and is the one file in a skill that no build rewrites.
- Runtime and model differences change prompt content, not package format. Skill *frontmatter* surfaces are nevertheless asymmetric between the runtimes even where the body is portable; when you are about to add a frontmatter key, read `references/61-skill-platform-mechanics.md` for which runtime documents it.

## Interpretation contract

Carry caveats forward as caveats. Never convert uncertainty into a firm instruction, and never infer that something is false from an absence of evidence — say the documentation does not state it, and use a named placeholder rather than an invented specific.

Where official sources and `/alaa-workflow` disagree with this skill, report the drift, prefer current official and runtime truth for the task in hand, and reconcile the owning file afterwards. Silently choosing a side leaves two sources of truth and no record of which one was followed.

Verified against live documentation on 6 August 2026.
