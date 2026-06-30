# Source Map

Use this file when workflow guidance depends on current agent/runtime behavior, model selection, subagent availability, goal mode, compaction, execution-memory policy, or skill format.

## Source priority

1. Explicit user instructions for the current task.
2. Repo-local `AGENTS.md`, active plan/state/phase-prompt files, and current worktree state.
3. This skill's `SKILL.md`, `references/00-topic-map.md`, templates, and validators.
4. System/developer instructions for the active Codex, Claude Code, sandbox, or agent surface.
5. Official or primary documentation for the tool involved, such as:
   - OpenAI Codex skills: https://developers.openai.com/codex/skills
   - OpenAI Codex goals: https://developers.openai.com/codex/use-cases/follow-goals
   - OpenAI Codex subagents: https://developers.openai.com/codex/subagents
   - OpenAI prompt guidance: https://developers.openai.com/api/docs/guides/prompt-guidance
   - Anthropic Claude Code skills: https://code.claude.com/docs/en/skills
   - Anthropic Claude Code subagents: https://code.claude.com/docs/en/sub-agents
   - Anthropic prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
   - Microsoft PowerShell docs: https://learn.microsoft.com/powershell/
   - Git docs: https://git-scm.com/docs
6. Community posts, StackOverflow answers, or forum threads only for troubleshooting a concrete error after primary sources above are exhausted.

## Freshness triggers

Re-check the active environment or official docs when the task mentions:

- latest, current, today, GPT-5.5, Opus 4.8, model routing, effort, reasoning, adaptive thinking, or goal mode
- changed Codex, Claude Code, subagent, background job, worktree, skill, plugin, sandbox, approval, shell, or browser-automation behavior
- changed plan/state file layout, compaction behavior, execution-memory conventions, or assistant-item phase handling
- resuming after a long interruption, compaction, or parallel lane handoff
- safety, security, privacy, legal, financial, medical, or deployment behavior that may have changed

## GPT-5.5 / Codex use guidance

- Prefer outcome-first prompts: define the end state, success criteria, evidence, constraints, and stop rules; do not over-specify process unless order matters.
- Use `/goal` or pursue-goal style for long-running implementation with a durable objective, validation surface, constraints, iteration policy, and blocked stop condition.
- Keep status reports compact: current checkpoint, verified evidence, remaining work, blocker if any.
- Use medium reasoning for ordinary coding and high/xhigh only when the task is genuinely hard, long-horizon, or architecture-sensitive.
- Use parallel reads and subagents when the environment supports them and the work has independent lanes.
- Preserve `phase: commentary` and `phase: final_answer` semantics when the harness exposes assistant-item phases.
- Do not invent GPT-specific commands, hidden capabilities, metrics, or dates. Use placeholders or cite/read sources.

## Claude Opus 4.8 use guidance

- Be clear, direct, and explicit about the desired output and must-check criteria.
- Use XML-style tags for complex review prompts that mix role, context, checks, and output format.
- For agentic/multi-step work, use adaptive thinking and high effort where the environment exposes those controls.
- Claude can orchestrate subagents natively, but avoid overuse for simple single-file or sequential work.
- Ask for self-checking against concrete criteria and gate evidence.
- In reviews, require a general-purpose solution and reject hard-coding to tests.

## Domain-bounded example

Good: a parent agent creates one parent plan, one phase prompt pack, one continuation state, assigns read-only API/docs/runtime lanes, merges findings centrally, validates, and updates state before handoff.

Bad: each lane edits `docs/BIG_PICTURE.md`, parent plan, and `.codex/state` broadly, then the parent chooses the largest diff without reconciling source truth.
