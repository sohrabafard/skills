# Install the rule-writer agent

## The `alaa-rule-writer` specialist

Claude Code installs this specialist with the shared personal-agent installer. Read [Install
agents](40-agent-installation.md) for Claude home selection, prerequisites, backups, rollback,
conflict handling and Codex orchestrator installation.

From the repository root, preview the writer-only migration:

```bash
python3 scripts/install_claude_agents.py --only alaa-rule-writer
```

After reviewing the preview, apply it:

```bash
python3 scripts/install_claude_agents.py --only alaa-rule-writer --apply
```

The retained compatibility entry point also installs only this agent:

```bash
python3 scripts/install_claude_rule_writer.py
python3 scripts/install_claude_rule_writer.py --apply
```

After applying, start a fresh Claude session. To use the specialist, ask Claude to delegate a
drafted instruction to `alaa-rule-writer`. The `/agents` wizard is removed in current Claude Code;
see [subagent usage](https://code.claude.com/docs/en/sub-agents#quickstart-create-your-first-subagent).

**Codex: install the user-level agent file.** Run from the repository root:

```bash
mkdir -p ~/.codex/agents
cp -f skills/sohrab/alaa-prompting-guide/assets/rule-writer/codex/alaa-rule-writer.toml ~/.codex/agents/
```

`cp -f` replaces a differing prior version and keeps no backup. The grants checker validates the
source definition; it is not a Claude installation gate. From the repository root, run
`python3 skills/sohrab/alaa-prompting-guide/scripts/check_rule_writer_grants.py` when validating
that source definition; exit `0` is clean, `1` reports findings, and `2` means validation could
not run.
