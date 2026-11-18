# Source Map

This file decides which source wins and when recall is forbidden.

## Source priority

1. Explicit user instructions for the current task.
2. The target host's current tool schemas and effective configuration, for runtime availability.
3. Live official documentation:
   - GPT-6: `https://developers.openai.com/api/docs/guides/latest-model`, `https://developers.openai.com/api/docs/models`, `https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra`, `https://learn.chatgpt.com/docs/models`, `https://learn.chatgpt.com/docs/model-selection`
   - Codex and ChatGPT skills, commands and agent files: `https://learn.chatgpt.com/docs/build-skills`, `https://learn.chatgpt.com/docs/developer-commands`, `https://learn.chatgpt.com/docs/agent-configuration/subagents`, `https://learn.chatgpt.com/docs/agent-configuration/agents-md`, `https://learn.chatgpt.com/docs/config-file/config-reference`, `https://learn.chatgpt.com/docs/agent-approvals-security`, and the pages under `https://developers.openai.com/codex/` for `use-cases/follow-goals`, `subagents` and `config-reference`
   - Claude prompting: `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices` plus the Opus 5.5, Fable 5.2, Haiku 5.5 and Sonnet 5.5 pages under that path
   - Claude facts and runtime: `https://platform.claude.com/docs/en/models/overview`, `https://platform.claude.com/docs/en/build-with-claude/effort`, and the `https://code.claude.com/docs/en/` pages `model-config`, `skills`, `sub-agents`, `env-vars`, `workflows`, `scheduled-tasks`, `permission-modes`, `ultraplan`, `goal` and `desktop`
4. This skill's dated references and local policy. They override no current official capability fact.

Use `/openai-docs` for current OpenAI guidance. Use a community source only as corroboration, after the official sources fail to answer.

**Redirects.** When a documented URL redirects across hosts, cite the destination and update the reference that named the origin. Examples: `developers.openai.com/codex/skills` redirects to the `learn.chatgpt.com` skills page, and `developers.openai.com/codex/guides/agents-md` redirects to `https://learn.chatgpt.com/docs/agent-configuration/agents-md` (16 November 2026).

## Freshness triggers

Re-fetch before you state any of these: a price, a token limit, an effort or verbosity name, a version, a default, a flag, a feature gate, goal or loop behavior, a subagent nesting or concurrency limit, a discovery path, a current-best recommendation, or a fact newer than the citing file's freshness stamp.

In three areas a carried-forward value is a defect, because nothing errors when a prompt requests a capability the harness no longer exposes under that name:

- Claude Code harness version gates and hard limits;
- subagent spawning defaults and depth behavior;
- the exact discovery paths for skills and agent definitions in both runtimes.

## Cross-agent packaging contract

- Keep one portable `SKILL.md` package for Codex and Claude Code, with agent-neutral behavior in `SKILL.md` and `references/`. `agents/openai.yaml` is Codex interface metadata only, and no build rewrites it.
- Runtime and model differences change prompt content, not package format. Before you add a frontmatter key, read `references/61-skill-platform-mechanics.md`.

## Interpretation contract

- Carry a caveat forward as a caveat. Never turn uncertainty into a firm instruction.
- Never infer that something is false from missing evidence. Say that the documentation does not state it, and use a named placeholder, not an invented specific.
- Where official sources or `/alaa-workflow` disagree with this skill, report the drift, follow current official and runtime truth for the task in hand, and reconcile the owning file afterwards. A silent choice leaves two sources of truth and no record of which one was followed.
- For model lifecycle, use the official model-deprecations page. For API ID semantics, use model-ids-and-versions.
- A release summary is weaker evidence than a full system card. The system cards were unavailable after bounded retrieval, so relax no authority or safety gate on a summary.
- Vendor scores and source validation prove no local runtime activation, account access, model equivalence or comparative quality of a profile.
- The advisor platform page was read through a summarizing fetch; re-read it before you quote it. The model-config and sub-agents pages were read to their first 100,000 characters; their later sections keep their earlier dates.

## Latest verification dates

Each reference keeps the date beside the fact it supports. The latest date per source group:

- 18 November 2026: the GPT-6.2 prompting guide, the OpenAI latest-model guide, the Codex models, model-selection and subagents pages, the GPT-6.2 API model pages, the served selector asset and the host model catalog, for the facts dated 18 November 2026 in `12`, `90`, `06` and `70`.
- 17 November 2026: Code `advisor` page, Advisor tool page, Claude model selection, models overview and effort pages, for the facts dated 17 November 2026 in `41`, `50` and `90`.
- 16 November 2026: Codex models page, Codex `AGENTS.md` page, OpenAI skills blog, Claude Code `skills` page, Agent Skills best practices, and the Claude subagent field list.
- 14 November 2026: OpenAI latest-model and model-selection pages; Codex subagents, configuration reference, and sandbox and approvals pages; Claude Fable 5.2 prompting and migration, effort, model selection, and the Code `model-config`, `sub-agents`, `env-vars`, `workflows` and `advisor` pages (`https://code.claude.com/docs/en/advisor`, `https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool`).
- 3 November 2026: Codex Terra pages.
- 9 October 2026: Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5 prompting pages.
- 4 October 2026: Claude Code `goal` and `desktop` pages.
