# Installation and Auto-Update

## Skill location

Place the complete `alaa-codex-orchestrator` directory in a location Codex scans for skills.

Recommended user installation path:

```text
~/.codex/skills/alaa-codex-orchestrator/
```

On Windows that resolves as:

```powershell
Join-Path $HOME ".codex\skills"
```

This path is field-verified — skills installed there are discovered and trigger normally — and it keeps skills alongside `~/.codex/agents/`, so the whole Codex setup lives under one tree. The official documentation instead lists `$HOME/.agents/skills` for user skills plus `.agents/skills` in the current directory, the parent, and the repository root; those work too. Use `.agents/skills` when the skill should travel with a specific repository rather than follow the user.

One-command installation after extracting the ZIP:

```powershell
& ".\alaa-codex-orchestrator\scripts\Install-AlaaCodexOrchestrator.ps1"
```

On macOS/Linux/WSL:

```bash
./alaa-codex-orchestrator/scripts/install-skill.sh
```

## Automatic agent installation

Every skill activation runs the platform installer:

- Windows: `scripts/Install-AlaaCodexAgents.ps1`
- macOS/Linux/WSL: `scripts/install-agents.sh`

It copies only `agents/*.toml` into:

```text
~/.codex/agents/
```

Behavior:

- creates the target directory when absent;
- skips byte-identical/hash-identical files;
- backs up differing same-named files under `.alaa-codex-orchestrator-backups/<timestamp>/`;
- installs via a temporary file and rename/replace;
- leaves unrelated agents and configuration untouched;
- may require a narrow sandbox approval because `~/.codex` is outside/protected from the repository workspace.

## Manual status check on Windows

```powershell
& "<skill-root>\scripts\Get-AlaaCodexAgentStatus.ps1"
```

## Validate the pack

```bash
python scripts/validate_pack.py
```

## Concurrency recommendation

The skill enforces at most two writing lanes and one heavy command at a time in its orchestration instructions. Codex also supports a global spawned-agent cap in `~/.codex/config.toml` (documented key `max_threads`, default 6; verify against current Codex docs before relying on it):

```toml
[agents]
max_threads = 4
```

The installer intentionally does not edit `config.toml`.

## Updates and rollback

Replacing the skill directory updates the source agent definitions. The next activation updates installed TOMLs and creates backups for changed prior versions. Restore a backup manually only when you intentionally want the previous definitions; the pack never silently rolls back.
