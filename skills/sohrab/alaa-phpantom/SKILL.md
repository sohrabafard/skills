---
name: alaa-phpantom
description: PHPantom native PHP/Blade language intelligence and Composer/Laravel-aware diagnostics, type and symbol navigation, project analysis, automatic fixes, formatting, namespace/class moves, and safe refactoring. Use for PHP bugs, unknown_class/unknown_member, Hover/Definition/References, PHP completion, PHPantom analyze/fix/format/move, and validating PHP edits. Do not use to choose an evidence owner (/alaa-code-intelligence-routing), for PHP code craft (/alaa-php-clean-code), or to replace a repository's formatter, static-analysis, or test gate. Works as a Claude Code LSP plugin skill or a standalone Codex skill.
---

# Alaa PHPantom — complete PHP language intelligence

PHPantom is an installed **Rust language server**, not an MCP server. In Claude Code the plugin supplies the read-only native `LSP` tool and post-edit diagnostics. Shell CLI operations perform project-wide checks and **intentional** source mutations. Codex can use this skill and the CLI, but its standard runtime gains no native LSP tool from `.lsp.json`.

## When NOT to use

- Selecting between CodeGraph, Serena, Laravel Boost, and PHPantom: use `/alaa-code-intelligence-routing`, which owns evidence selection.
- Deciding PHP naming, structure, or a refactor's shape: use `/alaa-php-clean-code`.
- Proving completion: run the repository's formatter, static-analysis, and test gates. `analyze` does not run PHPStan, and no PHPantom command replaces a required gate.

## Binary, workspace, and scope

- Work inside the **native Linux or WSL** project path, not a Windows `file://wsl.localhost` workspace URI.
- Run the installed binary `$HOME/.local/bin/phpantom_lsp` directly for native LSP and for the CLI operations (`analyze`, `fix`, `format`, `move`, `init`). It needs no bundled launcher, wrapper, MCP bridge or separate installation.
- Use the bare command `phpantom_lsp` when it resolves to that binary on `PATH`. Otherwise invoke the absolute path. Never download, install or build another copy.
- Find the **nearest relevant Composer root** (the directory holding `composer.json`), not necessarily the git monorepo root. In this skill `$PROJECT_ROOT` means that root in the target repository. Pass `--project-root "$PROJECT_ROOT"` when you work outside that directory. `cd` to the root when you inspect or validate.
- Do **not** start the LSP server without arguments from a regular shell for diagnostics, because that starts an interactive JSON-RPC process. Use `phpantom_lsp analyze` for batch diagnostics.
- Treat results as evidence: PHPantom can report false positives, particularly with dynamic Laravel behavior. Check Composer autoload, configured stubs and workspace indexing before you conclude that a symbol is missing.

## Route by operation

| Intent | Correct interface | Policy |
|---|---|---|
| Inspect definition, references, hover, type and navigation | Claude native `LSP` tool, when available | Read-only; use symbolic lookup instead of text guessing |
| See new diagnostics after edits | Native LSP diagnostics and the global `php -l` PostToolUse hook | Do not run whole-project analysis after every edit |
| Diagnose a PHP, Composer or Laravel issue | `phpantom_lsp analyze` | Scope paths first; use JSON when a tool processes the output |
| Remove unused imports or apply automated source fixes | `phpantom_lsp fix` | `--dry-run` first, then apply only the rules and files the task needs |
| Format PHP and Blade | `phpantom_lsp format` | `--check` first, then apply to selected files only |
| Rename or move a class or namespace across references and PSR-4 | `phpantom_lsp move` | `--dry-run` first; check destination mappings and remaining warnings |
| Create project-specific configuration | `.phpantom.toml` or `phpantom_lsp init` | Only when useful and explicitly within scope; never init automatically |

## Fast, executable workflow

1. Identify the target **Composer root** and the targeted changed files. Review `git status --short` and the existing uncommitted changes. Use the current working tree as the baseline. Never discard someone else's edits.
2. For an unclear symbol or type, use Claude's native `LSP` lookup where present. The LSP tool is **read-only**; it does not fix source code. When it is unavailable, including in Codex, use a scoped `analyze`, inspect definitions with the regular file tools, and state the limitation.
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
5. For formatting, **check first**, then apply to precisely scoped targets. Formatting may delegate to an *already-installed* Pint, php-cs-fixer, phpcbf or blade-formatter, according to project configuration:

   ```bash
   phpantom_lsp format app/Service/Foo.php --check --project-root "$PWD"
   phpantom_lsp format app/Service/Foo.php --project-root "$PWD"
   ```

   A `format --check` exit code `2` indicates changes are needed, not an execution failure. Avoid whole-repo format sweeps unrelated to the task.
6. For a class or namespace move, preview it and verify the **full destination name**, the PSR-4 mapping, the number of affected files, and leftover references in strings, config and Blade:

   ```bash
   phpantom_lsp move --dry-run --project-root "$PWD" 'App\Old\Widget' 'App\New\Widget'
   phpantom_lsp move --project-root "$PWD" 'App\Old\Widget' 'App\New\Widget'
   ```

   Bash single quotes preserve each namespace backslash. Never claim the move is complete if PHPantom reports unresolved external references.
7. Validate the result: inspect `git diff --check`, review the scoped `git diff`, run the focused tests and static checks relevant to the task, and re-run a targeted `analyze` and `format --check`. Do not present existing diagnostics as newly introduced ones.

## Multi-agent working tree considerations

- In a shared worktree, use `fix`, `format`, and `move` only while coordinating writes to overlapping files. If another agent modified the target between preview and apply, re-run preview and review the diff.
- Never run a project-wide `fix` or `format` on a task scoped to individual files. A namespace move is inherently project-wide; coordinate the move and communicate affected paths.
- The PostToolUse syntax hook is **read-only**. It processes only Claude `Write` and `Edit` events on `.php` files (not `.blade.php`), and needs no `jq` or install. It does not catch a write made through `Bash`. The loaded Claude plugin registers the hook whether or not this skill was invoked.
- Respect read-only, Plan, and user approval constraints. If instructed to implement, execute the approved scoped change after preview rather than asking for blanket approval repeatedly. Never auto-fix or auto-format from a hook.

## References — read only the one whose condition you are in

| You are about to | Read |
|---|---|
| pass a flag to `analyze`, `fix`, `format`, `move` or `init`, or interpret its exit code | `references/cli.md` |
| rely on the native `LSP` tool, its lifecycle or its post-edit diagnostics | `references/lsp.md` |
| choose the Composer root, edit `.phpantom.toml`, or configure Laravel, Blade or stubs | `references/configuration.md` |
| diagnose an unknown class, a missing binary, a WSL or UNC URI mismatch, or a server or hook conflict | `references/troubleshooting.md` |

When a CLI flag differs from this documentation, follow the installed version's `phpantom_lsp <subcommand> --help`.
