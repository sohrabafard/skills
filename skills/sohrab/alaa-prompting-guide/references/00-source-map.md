# Source Map

Ground every version-sensitive claim here. This file decides which source wins and when recall is forbidden; `references/00-topic-map.md` decides which reference answers a question.

## Source priority

1. Explicit user instructions for the current task.
2. Current target-host tool schemas and effective configuration for runtime availability.
3. Live official documentation:
   - GPT-6: `https://developers.openai.com/api/docs/guides/latest-model`, `https://developers.openai.com/api/docs/models`
   - Codex and ChatGPT skills, commands, and agent files: `https://learn.chatgpt.com/docs/build-skills`, `https://learn.chatgpt.com/docs/developer-commands`, and the Codex pages under `https://developers.openai.com/codex/` for `use-cases/follow-goals`, `subagents`, `guides/agents-md`, and `config-reference`, plus `https://learn.chatgpt.com/docs/agent-configuration/subagents`, `https://learn.chatgpt.com/docs/config-file/config-reference` and `https://learn.chatgpt.com/docs/agent-approvals-security`
   - Claude prompting: `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices` plus the model-specific Opus 5.5, Fable 5.2, Haiku 5.5, and Sonnet 5.5 pages under that path
   - Claude facts and runtime: `https://platform.claude.com/docs/en/models/overview`, `https://platform.claude.com/docs/en/build-with-claude/effort`, and the `https://code.claude.com/docs/en/` pages `model-config`, `skills`, `sub-agents`, `env-vars`, `workflows`, `scheduled-tasks`, `permission-modes`, `ultraplan`, `goal`, and `desktop`
4. This skill's dated references and local policy; they do not override current official capability facts. Use `/openai-docs` for current OpenAI guidance. Use community sources only as corroboration after official sources fail to answer.

When a documented URL redirects across hosts, cite the destination and update the reference that named the origin: the redirect makes the old citation stale even though it still resolves. Example: `developers.openai.com/codex/skills` permanently redirects to the `learn.chatgpt.com` skills page.

## Freshness triggers

Re-fetch before stating any price, token limit, effort or verbosity name, version, default, flag, feature gate, goal or loop behavior, subagent nesting or concurrency limit, discovery path, or current-best recommendation, and before carrying forward any fact newer than the citing file's freshness stamp.

In three areas, carrying a value forward is a defect: Claude Code harness version gates and hard limits, subagent spawning defaults and depth behavior, and the exact discovery paths for skills and agent definitions in both runtimes. Each has changed and silently broken prompts, because nothing errors when a prompt requests a capability the harness no longer exposes under that name.

## Cross-agent packaging contract

- Keep one portable `SKILL.md` package for Codex and Claude Code.
- Keep agent-neutral behavior in `SKILL.md` and `references/`. `agents/openai.yaml` is Codex interface metadata only, and is the one file in a skill that no build rewrites.
- Runtime and model differences change prompt content, not package format. Skill frontmatter surfaces still differ between the runtimes; before you add a frontmatter key, read `references/61-skill-platform-mechanics.md` for which runtime documents it.

## Interpretation contract

Carry caveats forward as caveats. Never convert uncertainty into a firm instruction. Never infer that something is false from an absence of evidence: say the documentation does not state it, and use a named placeholder rather than an invented specific.

Where official sources and `/alaa-workflow` disagree with this skill, report the drift, prefer current official and runtime truth for the task in hand, and reconcile the owning file afterwards, because a silent choice leaves two sources of truth and no record of which one was followed.

For model lifecycle, use the official model-deprecations page. For API ID semantics, use model-ids-and-versions. Release summaries are weaker evidence than full system cards, which were unavailable after bounded retrieval. Vendor scores and source validation do not prove local runtime activation, account access or a profile's comparative quality. The advisor platform page was read through a summarizing fetch, so re-read it before you quote it. The model-config and sub-agents pages were read to their first 100,000 characters; their later sections keep their earlier dates.

## Latest verification dates

Each reference keeps the date beside the fact it supports. The latest date per source group:

- OpenAI latest-model and model-selection pages: 14 November 2026. Codex model list and Terra pages: 3 November 2026.
- Codex subagents, configuration reference, and sandbox and approvals pages: 14 November 2026.
- Claude Fable 5.2 prompting and migration, models overview, effort, model selection, and the Code `model-config`, `sub-agents`, `env-vars`, `workflows` and `advisor` pages (`https://code.claude.com/docs/en/advisor`, `https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool`): 14 November 2026.
- Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5 prompting pages: 9 October 2026.
- Claude Code `goal`, `desktop` and `skills` pages: 4 October 2026.
