# Alaa Codex Runtime Ops Topic Map

Use this file to choose the smallest recovery reference.

- `references/10-windows-sandbox-recovery.md`
- sandbox refresh or setup failures
- serial retry after failed parallel reads
- preserving scope after harness errors

- `references/20-command-and-path-discipline.md`
- command-line length failures
- PowerShell and Git Bash path handling
- quoting and batching on Windows
- Windows reserved/excluded host ports blocking Docker or localhost binds
- escalation boundaries

- `references/30-git-session-and-locked-file-recovery.md`
- `git safe.directory` for read-only inspection
- locked Codex session JSONL files
- active log scanning safety
- session transcript audits and evidence classification
- missing Codex app chat/config/global-state diagnosis

- `references/90-source-map.md`
- freshness triggers for Codex, shell, and OS behavior

## Working rule

Recover the blocked command, not the whole world. Keep retries bounded and return to the original task.
