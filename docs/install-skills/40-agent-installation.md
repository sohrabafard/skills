# Install agents

## Claude Code personal agents

The shared installer installs or updates the repository's personal Claude agents under the
selected Claude home. It defaults to a dry-run, so preview first from the repository root:

```bash
python3 scripts/install_claude_agents.py
```

After reviewing the planned changes, apply them:

```bash
python3 scripts/install_claude_agents.py --apply
```

By default, the installer selects `~/.claude`. `CLAUDE_CONFIG_DIR` selects another configured
home, and `--claude-home PATH` takes precedence over both. The selected home and its parent path
must already exist, and its `skills/alaa-prompting-guide/SKILL.md` must be readable; a symlink to
that skill is allowed. The installer creates `agents/` when needed.

It installs the orchestrator's `agents/*.md` definitions and the canonical `alaa-rule-writer`
agent. Existing matching files are left alone. Differing regular agent files are backed up under
`alaa-agent-backups/install-*/` before replacement. If the legacy `skills/alaa-rule-writer`
plugin is present, the installer validates and archives that whole directory under the same
backup. It preserves unrelated agents, skills, plugins, and settings. A no-op writes nothing.

The installer locks the selected home against another installer process and replaces each agent
file atomically. Its lock uses POSIX `flock`, and archiving the legacy plugin uses a same-filesystem
rename; run it in WSL/Linux. A later error can leave earlier files installed; keep the printed
backups and
preview again before retrying. Exit `0` means a clean preview or successful apply, `1` means a
conflict, and `2` means an operational error. Do not edit the target profile manually or through
a plugin manager while apply runs. After migration, start a fresh Claude session before using the
agents. The inventory checks file installation; they do not prove agent execution.

To restore a backup, inspect its contents and restore only to a vacant destination. Never
overwrite a file created or changed by another tool or session. If a destination is occupied,
compare it with the backup and decide manually which version to keep.

Claude source version 5.0.0 keeps `alaa-implementer-opus` and adds `alaa-implementer-fable` with
separate admission. Do not retire Opus. Inspect installed roles before a future explicitly
authorized update; the shared installer updates present source wrappers but does not prove
activation or remove unrelated files. Read
`skills/sohrab/alaa-cc-orchestrator/references/model-effort-policy.md` and its routing owner before
dispatch. A source update does not install or retire agents on your machine.

## Codex user-level agents

Run from the repository root to materialize the current MCP grants and install Codex agent
definitions:

```bash
bash skills/sohrab/alaa-codex-orchestrator/scripts/install-agents.sh
```

The Codex `agents/*.toml` files are transport-neutral templates. The installer resolves the live
MCP inventory, validates each role's exact grant, and installs the materialized definitions. A
plain copy leaves grants unresolved. Installation changes the user-level agents directory and
requires explicit authorization. For the standalone `alaa-rule-writer` TOML procedure, see
[Install the rule-writer agent](50-rule-writer.md).

## Managed implementation and planning profiles

Before an authorized installation, generate and validate each affected orchestrator's standalone wrappers with its `scripts/render_agents.py --write` and aggregate validator. Edit `assets/implementation-contract.md`, `assets/planner-contract.md` or wrapper metadata, never generated bodies; model/effort pins come only from `/alaa-prompting-guide`. Existing reviewer rendering remains managed. Register all new implementation/planner files through the existing install procedure; source generation is not installation. Confirm actual host availability, configured controls, override precedence and grants before dispatch. A requested profile that cannot be realized blocks; do not silently substitute a model or effort.
