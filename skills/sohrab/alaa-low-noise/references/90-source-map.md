# Source Map

Read this file when context or output policy depends on current runtime behavior, shell behavior, or model guidance.

## Source priority

1. The user's requested output shape, especially any explicit request for raw logs, full diffs, or full file contents.
2. Repo-local instruction files (`AGENTS.md`, `CLAUDE.md`), active plan or state artifacts, and the current worktree.
3. This skill: `SKILL.md`, then `references/noise-control-patterns.md`, `references/model-output-profiles.md`, and `references/workflow-integration.md`.
4. Official documentation for the runtime in use:
   - Claude Code: https://code.claude.com/docs/
   - Codex: https://developers.openai.com/codex/
5. Official documentation for the command surface in use:
   - PowerShell: https://learn.microsoft.com/powershell/
   - Git: https://git-scm.com/docs
   - ripgrep: https://github.com/BurntSushi/ripgrep
6. Official prompting and skill guidance when model behavior affects output policy:
   - Anthropic prompting: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
   - Anthropic skill authoring: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
   - OpenAI model guidance: https://developers.openai.com/api/docs/guides/latest-model
   - OpenAI skills: https://developers.openai.com/codex/skills/
7. Community posts, StackOverflow answers, and issue comments only for troubleshooting a concrete shell or tool failure.

## Freshness triggers

Re-check current behavior when the task mentions:

- the latest Claude Code or Codex release, or new tool, terminal, PowerShell, Bash, or Windows behavior;
- very large generated logs, new validation runners, or new output caps;
- a model change affecting reasoning, verbosity, narration, tool eagerness, or delegation polarity — read `references/model-output-profiles.md` first, and re-verify it against the vendor docs when the model is newer than that file;
- subagent fan-out that could flood the parent's context;
- context-window, compaction, or caching behavior, since these change what a long tool result actually costs.

## Standing policy

- Start with the smallest instruction set that reliably preserves task quality, and add a rule only for a demonstrated gap. Repetition costs context without raising compliance.
- Prioritize required facts, evidence, caveats, validation, blockers, and next steps before trimming repetition or optional background. A generic brevity instruction suppresses required artifacts first.
- Treat fewer tokens, calls, or turns as improvements only when the final output still meets its quality bar.
- State the desired output shape positively and explicitly, and avoid model-specific rituals or repeated phrasing.
- Newer models still need bounded reads, reviewable edits, and validation evidence; capability does not remove the discipline.

## Domain-bounded anti-patterns

Bad: pasting a 2,000-line validation log into chat to prove a command ran. Good: capture it to a repo-local artifact when useful, read the failing slice, and report the command, the result, and the path.

Bad: reading six full files to answer a question about one function. Good: search for the symbol, read the bounded range around it, and stop.

## Caveats

The documentation URLs above are current entry points and are restructured periodically; if one 404s, navigate from the vendor's docs root rather than guessing a path. Runtime-specific behavior for Claude Code and Codex diverges between releases, so a rule verified on one runtime is not automatically true on the other. Per-model claims live in `references/model-output-profiles.md` and carry their own caveats and sources; this file only routes to them.

## Sources

- [Claude Code documentation](https://code.claude.com/docs/)
- [Codex documentation](https://developers.openai.com/codex/)
- [Prompting best practices (Claude family)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Agent Skills best practices (Anthropic)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Using the latest model (OpenAI)](https://developers.openai.com/api/docs/guides/latest-model)
- [Skills (Codex)](https://developers.openai.com/codex/skills)
