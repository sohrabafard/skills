# Troubleshooting checklist

## Claude only sees a standalone skill, not LSP or hooks

Ensure your canonical `alaa-phpantom` folder contains `.claude-plugin/plugin.json`, `.lsp.json`, `hooks/hooks.json` and root `SKILL.md`. Your existing symlink under `~/.claude/skills/alaa-phpantom` must point at that folder, not just `SKILL.md`. Restart or `/reload-plugins`; check `claude plugin list`, `/plugin` Installed and Errors, `/hooks`. The plugin is `alaa-phpantom@skills-dir` in a user skills directory. Policies can block skills-directory plugins; the standalone skill may still load.

## LSP does not start

Run `bash scripts/doctor.sh "$PROJECT_ROOT"` from the plugin folder, where `$PROJECT_ROOT` is the Composer root of the target repository. Check the existing binary with `$HOME/.local/bin/phpantom_lsp --version`. The plugin installs nothing. Check `claude --debug` and `/plugin` Errors for conflicts with other PHP servers.

## Incorrect classes, especially Carbon\\CarbonImmutable

From the WSL project root (`$PROJECT_ROOT`, the Composer root of the target repository):

```bash
cd "$PROJECT_ROOT"
php -r 'require "vendor/autoload.php"; var_dump(class_exists("Carbon\\CarbonImmutable"));'
"$HOME/.local/bin/phpantom_lsp" analyze app/ --project-root "$PWD" --code unknown_class --format json
```

If Composer resolves it but PHPantom doesn't, examine the LSP workspace root, the indexing, the Composer metadata, and `vendor/`. For a **Windows-hosted editor** that opens Linux files through `\\wsl.localhost`, sending `file://wsl.localhost/...` to a Linux LSP server may cause URI/workspace path mismatches; that issue is separate from Claude Code running **inside** native WSL. No proxy is needed for the latter.

## Duplicate or conflicting hooks

Plugin hooks are registered on plugin load, independent of skill invocation. If you already put the old lint hook in per-project `.claude/settings.json` or `.claude/settings.local.json`, remove only that duplicate entry after confirming `/hooks` shows the new one; leave unrelated project hooks untouched. The global plugin hook matches `Write|Edit` only. Bash-based file modifications are outside its event scope. Set `ALAA_PHPANTOM_LINT=0` in the Claude process environment if you need to disable this specific syntax check temporarily.

## Multi-agent in one worktree

Coordinate bulk fixes and rename or move operations; re-preview if another agent may have changed overlapping files. A read-only syntax hook is safe to run for each agent, but applying multiple format or move operations concurrently is not automatically safe.

Sources:
- https://code.claude.com/docs/en/plugins/loading
- https://github.com/PHPantom-dev/phpantom_claude
