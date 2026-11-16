# Source Map

Read this file when context or output policy depends on current runtime, shell or model behavior.

## Source priority

1. The user's requested output shape, then repo-local instruction files and active plan or state artifacts, then this skill.
2. Official documentation for the runtime in use: [Claude Code](https://code.claude.com/docs/) and [Codex](https://developers.openai.com/codex/).
3. Official documentation for the command surface in use: [Git](https://git-scm.com/docs) and [ripgrep](https://github.com/BurntSushi/ripgrep).
4. Official prompting and skill guidance, when model behavior affects output policy: [Prompting best practices (Claude family)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), [Agent Skills best practices (Anthropic)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [Using the latest model (OpenAI)](https://developers.openai.com/api/docs/guides/latest-model) and [Skills (Codex)](https://learn.chatgpt.com/docs/build-skills). The Codex skills address was checked 2026-11-16; the other URLs carry no check date.
5. Community posts, StackOverflow answers and issue comments: only to troubleshoot a concrete shell or tool failure.

If a URL returns 404, navigate from the vendor's documentation root; never guess a path. Claude Code and Codex diverge between releases, so a check on one runtime does not hold for the other.

## Freshness triggers

Re-check current behavior when the task involves:

- the latest Claude Code or Codex release, or new tool, terminal or Bash behavior;
- very large generated logs, new validation runners or new output caps;
- a model change that affects reasoning, verbosity, narration, tool eagerness or delegation polarity (read `references/model-output-profiles.md`);
- subagent fan-out that could flood the parent's context;
- context-window, compaction or caching behavior, which changes the cost of a long tool result.

## Standing policy

- `SKILL.md` *Contract* orders what to trim first. Reason: a generic brevity instruction suppresses required artifacts first.
- A newer, more capable model still keeps bounded reads, reviewable edits and validation evidence.
