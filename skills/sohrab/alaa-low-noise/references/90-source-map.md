# Source Map

Read this file when context or output policy depends on current runtime, shell or model behavior, which can change.

## Source priority

1. The user's requested output shape, especially any explicit request for raw logs, full diffs or full file contents.
2. Repo-local instruction files (`AGENTS.md`, `CLAUDE.md`), active plan or state artifacts, and the current worktree.
3. This skill: `SKILL.md`, then `references/noise-control-patterns.md`, `references/model-output-profiles.md` and `references/workflow-integration.md`.
4. Official documentation for the runtime in use: [Claude Code](https://code.claude.com/docs/) and [Codex](https://developers.openai.com/codex/).
5. Official documentation for the command surface in use: [Git](https://git-scm.com/docs) and [ripgrep](https://github.com/BurntSushi/ripgrep).
6. Official prompting and skill guidance when model behavior affects output policy: [Prompting best practices (Claude family)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), [Agent Skills best practices (Anthropic)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [Using the latest model (OpenAI)](https://developers.openai.com/api/docs/guides/latest-model) and [Skills (Codex)](https://developers.openai.com/codex/skills/).
7. Community posts, StackOverflow answers and issue comments, only for troubleshooting a concrete shell or tool failure.

## Freshness triggers

Re-check current behavior when the task mentions:

- The latest Claude Code or Codex release, or new tool, terminal or Bash behavior.
- Very large generated logs, new validation runners or new output caps.
- A model change affecting reasoning, verbosity, narration, tool eagerness or delegation polarity. Read `references/model-output-profiles.md`, which routes the model claim to `/alaa-prompting-guide`.
- Subagent fan-out that could flood the parent's context.
- Context-window, compaction or caching behavior, because these change the actual cost of a long tool result.

## Standing policy

- Start with the smallest instruction set that reliably preserves task quality. Add a rule only for a demonstrated gap, because repetition costs context without raising compliance.
- `SKILL.md` *Contract* orders what to preserve before trimming. Reason: generic brevity instructions suppress required artifacts first.
- Treat fewer tokens, calls or turns as improvements only when the final output still meets its quality bar.
- State the desired output shape positively and explicitly. Avoid model-specific rituals and repeated phrasing.
- Keep bounded reads, reviewable edits and validation evidence with newer models; greater capability does not remove this discipline.

## Caveats

- The URLs above are current documentation entry points and can change. If one returns 404, navigate from the vendor's documentation root instead of guessing a path.
- Claude Code and Codex behavior diverges between releases. Verification on one runtime does not automatically apply to the other.
