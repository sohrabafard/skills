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
5. Community posts, StackOverflow answers, or issue comments only for troubleshooting a concrete shell/tool failure.

## Freshness triggers

Re-check current behavior when the task mentions:

- latest Codex app, CLI, IDE, terminal, PowerShell, Bash, or Windows behavior
- very large generated logs, new validation runners, or new output caps
- model changes such as GPT-5.5 affecting reasoning or summarization expectations
- subagent fan-out that could flood the parent thread

## GPT-5.5-ready use guidance

- Do not assume a newer model removes the need for bounded reads, concise status, or final validation evidence.
- Use stronger reasoning to decide what not to print, while preserving enough evidence in repo files or final summaries for review.
- Avoid model-specific rituals. Prefer concrete changed paths, command results, and blocker notes.

## Domain-bounded anti-pattern

Bad: pasting a 2,000-line validation log into chat to prove a command ran.

Good: capture the log to a repo-local artifact when useful, read the failing slice, and report the command, result, and artifact path.
