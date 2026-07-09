# Source Map

Use this file when low-noise behavior depends on current shell behavior, Codex surface behavior, or model-use expectations.

## Source priority

1. The user's requested output shape, especially any request for raw logs, full diffs, or full file contents.
2. Repo-local `AGENTS.md`, active task plan/state files, and the current worktree.
3. This skill's `SKILL.md`, `references/noise-control-patterns.md`, and `references/workflow-integration.md`.
4. Official tool documentation for the command surface in use:
   - PowerShell: https://learn.microsoft.com/powershell/
   - Git: https://git-scm.com/docs
   - ripgrep: https://github.com/BurntSushi/ripgrep
5. Official skill and prompting guidance when model behavior affects output policy:
   - OpenAI skills: https://developers.openai.com/codex/skills/
   - OpenAI model guidance: https://developers.openai.com/api/docs/guides/prompt-guidance
   - Anthropic skill authoring: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
   - Anthropic prompting: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
6. Community posts, StackOverflow answers, or issue comments only for troubleshooting a concrete shell/tool failure.

## Freshness triggers

Re-check current behavior when the task mentions:

- latest Codex app, CLI, IDE, terminal, PowerShell, Bash, or Windows behavior
- very large generated logs, new validation runners, or new output caps
- model changes affecting reasoning, summarization, or verbosity expectations
- subagent fan-out that could flood the parent thread

## Current model-use guidance

- Start with the smallest instruction set that reliably preserves task quality; add rules only for a demonstrated gap.
- Prioritize required facts, evidence, caveats, validation, blockers, and next steps before trimming repetition or optional background. Generic brevity instructions can suppress required artifacts.
- Treat fewer tokens, calls, or turns as improvements only when the final output still meets its quality bar.
- State desired output positively and explicitly; avoid model-specific rituals and repeated phrasing.
- Re-check this guidance when models change. Newer models still need bounded reads, reviewable edits, and validation evidence.

## Domain-bounded anti-pattern

Bad: pasting a 2,000-line validation log into chat to prove a command ran.

Good: capture the log to a repo-local artifact when useful, read the failing slice, and report the command, result, and artifact path.
