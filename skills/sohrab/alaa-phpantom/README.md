# Alaa PHPantom — native LSP + global skill + always-on Claude hook

One canonical source directory, compatible with the user's existing global symlink distribution to Claude and Codex. No third-party plugin, MCP, Rust rebuild, Python LSP wrapper, package download, npm, pip or jq required. Uses only an **already installed** PHPantom binary and the existing PHP CLI for the optional syntax hook.

## Origin and loading

Install **the source folder** at:

```text
/home/sohrab/project/skills/skills/sohrab/alaa-phpantom/
```

The existing user's sync script links it into:

```text
~/.claude/skills/alaa-phpantom -> /home/sohrab/project/skills/skills/sohrab/alaa-phpantom/
```

And into the user's current Codex skill directory. Do **not** add a second symlink or copy skill content into each project; the user's existing script does this already.

**Important:** Claude Code v2.1.0+ supports LSP plugins, but recognizing a plugin at `~/.claude/skills/<name>/.claude-plugin/plugin.json` as `@skills-dir` is a *newer* Claude Code feature. Verify support on the installed version; if not recognized, `claude --plugin-dir /home/sohrab/project/skills/skills/sohrab/alaa-phpantom` is the fallback for a local CLI session. Loading a plain skill is not proof that LSP and hooks loaded.

When this **plugin** is loaded, Claude gets:

- Native `phpantom` LSP over stdio (hover/definition/references/diagnostics; read-only LSP tool)
- Root `SKILL.md` as a plugin skill (`/alaa-phpantom:alaa-phpantom`), which is also the same canonical skill exposed by the existing symlink
- Automatic `PostToolUse` -> `Write|Edit` -> `php -l` syntax hook in **every local project** where the plugin is enabled
- CLI through the installed binary, not a plugin file: `phpantom_lsp analyze`, `fix`, `format`, `move`, `init`

Codex gets the same root skill and can use the installed PHPantom CLI through normal shell commands. Claude-only files do not magically provide native LSP or hook support in Codex.

## Binary

The LSP server and CLI run the installed executable directly: `/home/sohrab/.local/bin/phpantom_lsp` (`$HOME/.local/bin/phpantom_lsp`). The plugin bundles no launcher, LSP client, JSON-RPC proxy, or MCP server, and installs nothing.

## Quick check (WSL)

```bash
cd /home/sohrab/project/skills/skills/sohrab/alaa-phpantom
bash scripts/doctor.sh /home/sohrab/project/auth
python3 -m unittest discover -s tests -v  # optional tests, Python stdlib only
claude plugin validate .                  # use installed CLI version that supports this
claude plugin list
```

Inside a new/reloaded Claude Code session:

1. `/plugin` -> Installed: ensure `alaa-phpantom@skills-dir` is loaded; check Errors for LSP conflicts.
2. `/hooks`: check `PostToolUse` `Write|Edit` from this plugin. No per-project edit to `.claude/settings.json` is necessary.
3. Edit a **throwaway** `.php` file and verify `Found N new diagnostic issues` in Claude, or request the LSP tool for definition/references. To test the hook, intentionally syntax-break that test file, see the lint diagnostic, then revert the test change.
4. Test `phpantom_lsp analyze --project-root /home/sohrab/project/auth --severity error` on a small project subset; check installed CLI `--help` first if in doubt.

If a previous version registered the same hook in per-project settings, remove **only that duplicate hook entry** after verifying `/hooks`; retain other hooks.

## Hook behavior and security

The hook reads Claude `PostToolUse` JSON, validates the edited file is under the current `CLAUDE_PROJECT_DIR`, ignores `*.blade.php` and other non-PHP paths, runs `php -l` without a shell, emits syntax errors via stderr and exit code 2, never writes to the project, and otherwise exits silently. It is **not** a project-wide analyzer and does not intercept arbitrary shell-based writes. If PHP CLI is not present, the hook skips gracefully; native Rust PHPantom LSP still works.

Set `ALAA_PHPANTOM_LINT=0` in the launching Claude environment to disable this plugin's syntax check for a session, without disabling LSP. The hook is automatically included with the loaded plugin; it does not wait for the Skill to be explicitly invoked.

## Supported operations

| Capability | Native Claude LSP | Shell CLI (Claude and Codex) |
|---|---|---|
| Definition / Hover / References | Yes, read-only LSP tool | Not directly via CLI |
| Diagnostics | Yes, on edits | `analyze` |
| Apply quick fixes | LSP tool itself is read-only | `fix`, scoped/dry-run first |
| PHP and Blade format | Not an automatic editable LSP tool | `format --check`, then `format` |
| Move class/namespace and references | Not an editable LSP tool | `move --dry-run`, then `move` |
| Project config | `.phpantom.toml` read by server | `init` only when requested |
| Syntax check | Plugin hook | `php -l` |

## Reference versions / sources

- PHPantom primary repo and CLI: https://github.com/PHPantom-dev/phpantom_lsp/blob/main/docs/cli.md
- Official Claude plugin (source comparison): https://github.com/PHPantom-dev/phpantom_claude
- Claude Skills-directory Plugins: https://code.claude.com/docs/en/skills
- Plugin Hooks: https://code.claude.com/docs/en/plugins/components
- LSP plugin schema: https://code.claude.com/docs/en/plugins-reference

## Scope

This is a **local** skill/plugin pack. Offline tests validate the JSON structure and hook behavior only. Do not expect it to affect a Windows-hosted PhpStorm LSP4IJ process, which has separate UNC URI mapping concerns.
