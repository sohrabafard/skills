---
name: alaa-phpantom
description: PHPantom native PHP/Blade language intelligence and Composer/Laravel-aware diagnostics, type and symbol navigation, project analysis, automatic fixes, formatting, namespace/class moves, and safe refactoring. Use for PHP bugs, unknown_class/unknown_member, Hover/Definition/References, PHP completion, PHPantom analyze/fix/format/move, and validating PHP edits. Do not use to choose an evidence owner (/alaa-code-intelligence-routing), for PHP code craft (/alaa-php-clean-code), or to replace a repository's formatter, static-analysis, or test gate. Works as a Claude Code LSP plugin skill or a standalone Codex skill.
---

# Alaa PHPantom — complete PHP language intelligence

PHPantom is an installed **Rust language server**, not an MCP server. Claude Code's plugin automatically supplies the read-only native `LSP` tool and post-edit diagnostics; shell CLI operations perform project-wide checks and **intentional** source mutations. Codex can use this same skill and CLI, but its standard runtime does not gain a native LSP tool merely by loading `.lsp.json`.

## When NOT to use

- Selecting between CodeGraph, Serena, Laravel Boost, and PHPantom: use `/alaa-code-intelligence-routing`, which owns evidence selection.
- Deciding PHP naming, structure, or a refactor's shape: use `/alaa-php-clean-code`.
- Proving completion: run the repository's formatter, static-analysis, and test gates. `analyze` does not run PHPStan, and no PHPantom command replaces a required gate.

## Binary, workspace, and scope

- Work inside the **native Linux/WSL** project path, not a Windows `file://wsl.localhost` workspace URI. For this machine the installed executable is `/home/sohrab/.local/bin/phpantom_lsp` (normally `$HOME/.local/bin/phpantom_lsp`).
- Use the existing PHPantom binary directly at `/home/sohrab/.local/bin/phpantom_lsp` for both native LSP and CLI operations (`analyze`, `fix`, `format`, `move`, `init`). No bundled launcher, wrapper, MCP bridge, or separate PHPantom installation is required.
- The command `phpantom_lsp` may be used when it resolves to the installed binary on `PATH`; otherwise invoke the absolute path. Never download, install, or build another copy.
- Derive the **nearest relevant Composer root** (`composer.json`), not necessarily the git monorepo root. Use `--project-root "$PROJECT_ROOT"` when working outside that directory. `cd` to the root when inspecting/validating.
- Do **not** call the LSP server without arguments from a regular shell for diagnostics: that starts an interactive JSON-RPC process. Use `phpantom_lsp analyze` for batch diagnostics.
- Treat results as evidence: PHPantom can report false positives, particularly with dynamic Laravel behavior. Check Composer autoload, configured stubs, and workspace indexing before assuming a symbol is missing.

## Route by operation

| Intent | Correct interface | Policy |
|---|---|---|
| Inspect definition, references, hover, type and navigation | Claude native `LSP` tool, when available | Read-only; prefer symbolic lookup over text guessing |
| See new diagnostics after edits | Native LSP diagnostics + global `php -l` PostToolUse hook | Do not redundantly run whole-project analysis after every edit |
| Diagnose PHP/Composer/Laravel issues | `phpantom_lsp analyze` | Scope paths first; optionally JSON for processing |
| Remove unused imports / automated source fixes | `phpantom_lsp fix` | First `--dry-run`, then apply only task-appropriate rules/files |
| PHP and Blade formatting | `phpantom_lsp format` | First `--check`, then apply to selected files only |
| Rename/move class or namespace across references/PSR-4 | `phpantom_lsp move` | First `--dry-run`; check destination mappings and remaining warnings |
| Create project-specific configuration | `.phpantom.toml` / `phpantom_lsp init` | Only when useful and explicitly within scope; no automatic init |

## Fast, executable workflow

1. Identify the target **Composer root** and targeted changed files. Review current `git status --short` and existing uncommitted changes. Use the current working tree as the baseline; never discard someone else's edits.
2. For an unclear symbol/type, use Claude's native `LSP` lookup where present. The LSP tool is **read-only**, not a source-code-fix endpoint. If unavailable (including Codex), use scoped `analyze`, inspect definitions via regular file tools, and state the limitation.
3. For diagnostics use:

   ```bash
   phpantom_lsp analyze app/ --project-root "$PWD" --severity warning --format json
   phpantom_lsp analyze app/Service/Foo.php --project-root "$PWD" --code unknown_class --no-colour
   ```

   A non-zero `analyze` exit can mean diagnostics found (`1`) rather than server failure.
4. For automatic fixes, **preview before writing** and restrict the first pass to a file or narrow directory. Use specific native rules when possible:

   ```bash
   phpantom_lsp fix app/Service/Foo.php --rule unused_import --dry-run --project-root "$PWD"
   phpantom_lsp fix app/Service/Foo.php --rule unused_import --project-root "$PWD"
   ```

   `fix --dry-run` returns `2` when it found fixable changes; that is an expected preview outcome. Do not enable `--with-phpstan` unless the installed version and existing project setup explicitly support it; the upstream CLI documentation calls that integration future-facing.
5. For formatting, **check first**, then apply to precisely scoped targets; formatting may delegate to *already-installed* Pint/php-cs-fixer/phpcbf/blade-formatter according to project configuration:

   ```bash
   phpantom_lsp format app/Service/Foo.php --check --project-root "$PWD"
   phpantom_lsp format app/Service/Foo.php --project-root "$PWD"
   ```

   A `format --check` exit code `2` indicates changes are needed, not an execution failure. Avoid whole-repo format sweeps unrelated to the task.
6. For class/namespace moves, preview and verify the **full destination name**, PSR-4 mapping, number of affected files, and leftover strings/config/Blade references:

   ```bash
   phpantom_lsp move --dry-run --project-root "$PWD" 'App\Old\Widget' 'App\New\Widget'
   phpantom_lsp move --project-root "$PWD" 'App\Old\Widget' 'App\New\Widget'
   ```

   Bash single quotes preserve each namespace backslash. Never claim the move is complete if PHPantom reports unresolved external references.
7. Validate the result: inspect `git diff --check`, review scoped `git diff`, run focused tests/static checks relevant to the task, and re-run targeted `analyze` and `format --check`. Do not mask existing diagnostics as newly introduced ones.

## Multi-agent working tree considerations

- In a shared worktree, use `fix`, `format`, and `move` only while coordinating writes to overlapping files. If another agent modified the target between preview and apply, re-run preview and review the diff.
- Never run project-wide `fix`/`format` on a task scoped to individual files. A namespace move is inherently project-wide; coordinate the move and communicate affected paths.
- The PostToolUse syntax hook is **read-only**. It only processes Claude `Write`/`Edit` events on `.php` (not `.blade.php`), without `jq` or installs. It does not catch arbitrary `Bash`-based writes. The hook is registered automatically as part of the loaded Claude plugin, irrespective of whether this skill was invoked.
- Respect read-only, Plan, and user approval constraints. If instructed to implement, execute the approved scoped change after preview rather than asking for blanket approval repeatedly. Never auto-fix or auto-format from a hook.

## References (read the relevant one rather than loading all)

- `references/cli.md` — exact command flags and exit-code semantics for analyze, fix, format, move, init.
- `references/lsp.md` — Claude native LSP behavior, lifecycle, diagnostics and boundaries.
- `references/configuration.md` — Composer root and PHPantom `.phpantom.toml`, Laravel/Blade and stubs.
- `references/troubleshooting.md` — unknown classes, binary missing, WSL/UNC URI, debugging and conflicts.

Always prefer the installed version's `phpantom_lsp <subcommand> --help` if a CLI flag differs from this documentation.
