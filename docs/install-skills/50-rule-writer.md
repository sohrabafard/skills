# Install the rule-writer agent

## The `alaa-rule-writer` specialist

The two runtimes install this agent by different routes. Claude Code uses a plugin; Codex uses a user-level agent file.

**Claude Code: install the packaged plugin.** From the repository root, preview first; the script
defaults to dry-run and writes nothing:

```bash
python3 scripts/install_claude_rule_writer.py
```

Apply the install or update with:

```bash
python3 scripts/install_claude_rule_writer.py --apply
```

For a separate Claude configuration directory, pass its path explicitly:

```bash
python3 scripts/install_claude_rule_writer.py --apply --claude-home "$HOME/.config/claude"
```

The destination is `skills/alaa-rule-writer` under `--claude-home`, then a non-empty
`CLAUDE_CONFIG_DIR`, then `~/.claude`. The selected Claude home must already contain a readable
`skills/alaa-prompting-guide/SKILL.md`; a symlink to that personal skill is allowed. The script
validates changed candidates with the installed Claude CLI in an isolated temporary config before
publication. A missing CLI, timeout, or validator failure blocks publication. Local catalog
metadata warnings do not block exit `0`; a nonzero validator result does. Validator errors currently
report the exit code without full diagnostic details. Exit `0` means preview or success, `1` means
a conflict or finding, and `2` means an invocation, operational, or validation-tool failure.

An unchanged agent is a no-op and skips validation. The installer preserves an existing matching
manifest, unknown plugin files, and unrelated plugins and settings. An update with a prior agent
prints the exact backup path; restore that file to the agent path to roll back, with no installer or
plugin manager changing the target. If the target had no prior agent, no backup exists: move only
the new `agents/alaa-rule-writer.md` outside plugin discovery. Preserve the existing manifest,
files, and directories. A fresh plugin install has no backup; move only
`skills/alaa-rule-writer` outside plugin discovery to roll it back. Do not copy the wrapper into
`~/.claude/agents` or create an installation sentinel.

Do not edit the target manually or with a plugin manager during `--apply`; the lock coordinates
installer processes only. A customized manifest that requires external files may fail staged
validation. After applying, start a fresh Claude session or run `/reload-plugins`.
In the WSL shell, run `claude plugin details alaa-rule-writer` and confirm
`Agents (1) alaa-rule-writer` in its component inventory. `Skills (0)` is expected for this agent-only package.
This checks discovery, not execution. To use it, ask Claude to delegate a drafted instruction to
`alaa-rule-writer:alaa-rule-writer`. The `/agents` wizard is removed in current Claude Code;
see [subagent usage](https://code.claude.com/docs/en/sub-agents#quickstart-create-your-first-subagent)
and [plugin inspection](https://code.claude.com/docs/en/discover-plugins#see-what-an-installed-plugin-adds-to-your-sessions).

**Codex: one copy, since Codex has no plugin.** Run from the repository root:

```bash
mkdir -p ~/.codex/agents
cp -f skills/sohrab/alaa-prompting-guide/assets/rule-writer/codex/alaa-rule-writer.toml ~/.codex/agents/
```

`cp -f` replaces a differing prior version and keeps no backup, matching both orchestrator packs.
Run `python3 skills/sohrab/alaa-prompting-guide/scripts/check_rule_writer_grants.py` first; exit `0`
is the gate, and `1` or `2` both fail it.
