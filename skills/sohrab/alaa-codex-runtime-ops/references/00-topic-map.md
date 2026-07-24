# Alaa Codex Runtime Ops Topic Map

Use this file to choose the smallest recovery reference. Each entry names the failure classes in `SKILL.md` that it expands.

- `references/10-windows-sandbox-recovery.md`
- sandbox setup or refresh failure
- sandbox-related DNS, registry, package-index, or remote-doc failure
- serial retry after failed parallel reads
- preserving scope after harness errors

- `references/20-command-and-path-discipline.md`
- command-length failure, including `CreateProcessAsUserW failed: 206`
- Windows `EPERM` during validation or build cleanup
- shell syntax, quoting, and path confusion across PowerShell and Git Bash
- Docker named-pipe permission failure
- port binding exclusion or reservation
- escalation boundaries

- `references/30-git-session-and-locked-file-recovery.md`
- Git dubious ownership and `safe.directory` for read-only inspection
- locked session JSONL and transcript audit
- active log scanning safety and evidence classification
- missing Codex app chat, `config.toml`, or global-state diagnosis

- `references/40-project-fallbacks.md`
- Node, Vite, Vitest, Quasar, and Yarn-gate fallbacks recorded from real sessions
- standing maintainer approval for unsandboxed validation gates, and its scope condition
- the `entekhabat-front` `/new` package lane

- `references/90-source-map.md`
- freshness triggers for Codex, shell, OS, and pinned project fallback commands

## Working rule

Recover the blocked command, not the whole world. Keep retries bounded and return to the original task.

## Maintenance

- Keep `SKILL.md` recovery-focused. Project-specific commands belong in `references/40-project-fallbacks.md`, and domain, framework, or repository policy belongs in its own skill.
- Add a failure class only when a recurring Codex or Windows failure appears in real sessions, and give it the same four fields: symptom, diagnosis, smallest retry, escalation or fallback.
- Update examples only from observed sessions, and check historical findings against the current files before editing.
