# Source Map

Use this file when workflow guidance depends on current agent/runtime behavior, model selection, subagent availability,
goal mode, compaction, execution-memory policy, or skill format.

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
    - Anthropic prompting best
      practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
    - Microsoft PowerShell docs: https://learn.microsoft.com/powershell/
    - Git docs: https://git-scm.com/docs
6. Community posts, StackOverflow answers, or forum threads only for troubleshooting a concrete error after primary
   sources above are exhausted.

## Freshness triggers

Re-check the active environment or official docs when the task mentions:

- latest, current, today, GPT-5.5, Opus 4.8, model routing, effort, reasoning, adaptive thinking, or goal mode
- changed Codex, Claude Code, subagent, background job, worktree, skill, plugin, sandbox, approval, shell, or
  browser-automation behavior
- changed plan/state file layout, compaction behavior, execution-memory conventions, or assistant-item phase handling
- resuming after a long interruption, compaction, or parallel lane handoff
- safety, security, privacy, legal, financial, medical, or deployment behavior that may have changed

## Model-specific prompting tuning

For GPT-5.5, Claude Opus 4.8, Claude Sonnet 5, or Claude Fable 5 tuning -- effort/verbosity levels, subagent spawning
tendencies, tool-triggering behavior, and the `$` vs `/` skill-trigger syntax -- read `$alaa-prompting-guide` (Codex) or
`/alaa-prompting-guide` (Claude Code) instead of duplicating that guidance here. It is researched from live official
docs and covers all four models this pack uses; this file's job is workflow orchestration, not per-model tuning, and
keeping model tuning in one place avoids the two copies silently drifting apart. Only write model-tuning notes directly
in a plan or phase prompt if `$alaa-prompting-guide`/`/alaa-prompting-guide` is genuinely unavailable in the current
environment, and say so explicitly when you do.

## Domain-bounded example

Good: a parent agent creates one parent plan, one phase prompt pack, one continuation state, assigns read-only
API/docs/runtime lanes, merges findings centrally, validates, and updates state before handoff.

Bad: each lane edits `docs/BIG_PICTURE.md`, parent plan, and `.codex/state` broadly, then the parent chooses the largest
diff without reconciling source truth.
