# Source Map

Use this file when runtime recovery depends on current tool or OS behavior.

## Source priority

1. Current command error text and active task requirements.
2. Local shell behavior in the current Codex environment.
3. Repo-local `AGENTS.md` and active permissions instructions.
4. Official docs for Git, PowerShell, Docker, or Codex/OpenAI tools when version-sensitive behavior matters.

## Freshness triggers

Verify current behavior before giving durable guidance about:

- Codex sandboxing, approvals, and escalation keys such as `sandbox_permissions`
- OpenAI/Codex tool behavior and session file layout under `~/.codex`
- Git safe-directory policy
- Docker Compose on Windows through Git Bash
- Git Bash/MSYS IPC and child-process behavior inside and outside the active sandbox
- PowerShell path, stream, or quoting behavior
- the pinned commands in `references/40-project-fallbacks.md`, which track one workspace's scripts and toolchain versions and go stale when those change
