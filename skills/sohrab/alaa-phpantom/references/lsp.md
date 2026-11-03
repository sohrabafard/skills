# Native Claude LSP — purpose and limits

- Plugin root `.lsp.json` is loaded automatically **when the plugin itself is enabled**. It does not make a standalone skill into a server by itself.
- `stdio` server command: the already-installed Rust executable at `$HOME/.local/bin/phpantom_lsp`, started directly. `.lsp.json` holds its absolute path.
- Supported extensions follow PHPantom's upstream Claude plugin: `.php`, `.phtml`, `.php3` etc. and `.blade.php`. Match to LSP language IDs `php` or `blade`.
- Claude starts the server upon PHP file activity. The `LSP` tool is **read-only** and provides symbol lookup/navigation. LSP diagnostics are supplied after edits. Do not promise that a writable LSP Code Action endpoint is exposed as a Claude tool merely because PHPantom implements codeActionProvider.
- Use `fix`, `format`, and `move` CLI commands for filesystem mutations. Never present a `php -l` syntax hook as replacing semantic diagnostics.
- Avoid conflict with another enabled PHP LSP plugin. Claude assigns each extension to the first enabled server, and a later one may not receive requests. Check `/plugin` -> Errors and `claude --debug`.
- Claude Code native LSP plugins run in local terminal sessions, including CLI started inside WSL; cloud-hosted sessions do not run plugin language servers. Check Desktop mode compatibility for the version you use.
- Reload plugins (`/reload-plugins`) or create a new session after modifying manifest/LSP/hooks. Use `/plugin` to confirm `alaa-phpantom@skills-dir` and Errors, `/hooks` to confirm global hook, then ask Claude to navigate a PHP symbol and edit a throwaway PHP file.

Sources:
- https://code.claude.com/docs/en/plugins/code-intelligence
- https://code.claude.com/docs/en/plugins/components
- https://github.com/PHPantom-dev/phpantom_claude/blob/main/.lsp.json
