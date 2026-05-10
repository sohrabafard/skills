# Source Map

Use this file when runtime recovery depends on current tool or OS behavior.

## Source priority

1. Current command error text and active task requirements.
2. Local shell behavior in the current Codex environment.
3. Repo-local `AGENTS.md` and active permissions instructions.
4. Official docs for Git, PowerShell, Docker, or Codex/OpenAI tools when version-sensitive behavior matters.

## Freshness triggers

Verify current behavior before giving durable guidance about:

- Codex app sandboxing or approvals
- OpenAI/Codex tool behavior
- Git safe-directory policy
- Docker Compose on Windows through Git Bash
- PowerShell path, stream, or quoting behavior
