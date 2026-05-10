# Git, Session, And Locked File Recovery

## Git dubious ownership

For read-only inspection in a repo that reports dubious ownership, prefer command-local trust:

```bash
git -c safe.directory='<repo-path>' -C '<repo-path>' status --short
```

Do not write global Git config unless the user asks for a persistent machine-level fix.

## Active session JSONL files

When scanning `~/.codex/sessions`, active JSONL files may be locked by the running Codex app.

Use a shared-read approach when available, or skip and report the active locked file if it cannot be read safely. Do not kill Codex or truncate sessions to complete a scan.

## Session scan hygiene

- Prefer filename/session metadata dates over filesystem modified time when the user asks for a date window.
- Keep broad scans read-only.
- Deduplicate forked subagent/session evidence before turning it into a skill update.
- Compare historical findings against current skill files before editing.
