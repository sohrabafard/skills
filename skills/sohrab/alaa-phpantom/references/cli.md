# PHPantom CLI quick reference (upstream docs, refreshed 2026-11-03)

The same installed executable, `$HOME/.local/bin/phpantom_lsp`, runs both the native LSP server (no arguments) and independent CLI operations (`analyze`, `fix`, `format`, `move`, `init`).

## Analyze (read only)

```bash
phpantom_lsp analyze [PATH...] --project-root "$PWD" --severity all --format json
phpantom_lsp analyze app/ --severity warning --no-colour
phpantom_lsp analyze app/Domain/ --code unknown_class --code unknown_member --format json
phpantom_lsp analyze app/ --exclude-code unused_import --no-colour
```

`[PATH...]` accepts multiple files or directories. `--severity all|warning|error`, `--code`, `--exclude-code`, `--format table|github|json`, `--project-root`, `--debug`, verbosity flags, `--no-colour`. Exit `0`: no diagnostics; `1`: diagnostics found; `2`: invalid/missing path. Distinguish code `1` from tool failure.

Common codes: `syntax_error`, `unknown_class`, `unknown_member`, `partial_union_member`, `unknown_function`, `argument_count_mismatch`, `missing_implementation`, `scalar_member_access`, `invalid_member_access`, `unused_import`, `unreachable_code`, `deprecated_usage`. Avoid the old names `argument_count`, `implementation_error` and `deprecated` when you filter `analyze` output.

## Fix (writes files unless dry-run)

```bash
phpantom_lsp fix app/Domain/Foo.php --rule unused_import --dry-run --project-root "$PWD"
phpantom_lsp fix app/Domain/Foo.php --rule unused_import --project-root "$PWD"
phpantom_lsp fix app/Domain/ --rule deprecated --dry-run --project-root "$PWD"
```

Flags: `[PATH]` (one file or directory; the default is the entire Composer project), repeatable `--rule`, `--dry-run`, `--project-root`, `--no-colour`. Documented native rules: `unused_import` and `deprecated` (for annotated replacements). Omitting `--rule` runs all *preferred native* rules; omit it only after you inspect the scope. `--with-phpstan` is described as future functionality upstream; do not claim it works without testing your version.

Exit `0`: applied/no fixes; `1`: failure; `2`: dry-run found fixable changes (no write).

## Format (writes files unless --check)

```bash
phpantom_lsp format app/Domain/Foo.php --check --project-root "$PWD"
phpantom_lsp format app/Domain/Foo.php --project-root "$PWD"
phpantom_lsp format resources/views/example.blade.php --check --project-root "$PWD"
```

Flags: `[PATH...]`, `--check`, `--project-root`, `--format table|github|json`, `--no-colour`; Blade built-in reindenter accepts `--indent-size` and `--use-tabs`. Exit `0`: all formatted/applied; `1`: read/format/write failure; `2`: `--check` found unformatted files (no write). Formatting delegates to an already-available project formatter, such as Pint, when the project configures one.

## Move (cross-file write unless dry-run)

```bash
phpantom_lsp move --dry-run --project-root "$PWD" 'App\Old\Widget' 'App\New\Widget'
phpantom_lsp move --project-root "$PWD" 'App\Old\Widget' 'App\New\Widget'
phpantom_lsp move --dry-run --project-root "$PWD" app/Old/Widget.php app/New/Widget.php
```

`FROM` and `TO` are full class/namespace names or PSR-4 paths. Flags: `--dry-run`, `--format table|github|json`, `--project-root`, `--no-colour`. Exit `0`: applied or valid dry-run; `1`: an invalid or incompatible move, or a write error. `TO` is the **entire** class destination, not just the parent namespace.

Review warnings for paths and strings outside semantic rewrite (Blade, YAML, config strings, baselines, routing strings). `move` is designed to make no partial change for a rejected destination; still review `git diff` when it completes. `move` works within one Composer root; coordinate a move across projects separately.

## Init

`phpantom_lsp init` generates a default `.phpantom.toml`; this is a file mutation. Prefer to keep the existing config, and run `init` only when the task needs project-specific configuration. Always check `phpantom_lsp <cmd> --help` in the installed version.

Source: https://github.com/PHPantom-dev/phpantom_lsp/blob/main/docs/cli.md
