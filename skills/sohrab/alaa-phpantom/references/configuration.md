# PHPantom project configuration, Laravel and Composer

PHPantom chooses the Composer project root to resolve `composer.json`, `vendor` and PSR-4 autoload mappings. A monorepo can have several Composer projects; run CLI separately at each Composer root and do not share a single accidental root for all subprojects.

Most repositories need no `.phpantom.toml`; avoid running `phpantom_lsp init` simply to set up this plugin. Existing file is authoritative. Configuration groups described upstream include `[indexing]` (include/exclude and extensions), `[stubs]` (overrides), `[formatting]` (formatter selection), `[phpstan]`, `[laravel.schema]` and `[laravel.migrations]`.

For Laravel, many symbols are inferred from Eloquent relations, scopes, casts, database schemas and migrations. If a class known to Composer is marked `unknown_class`, check filesystem root, valid `vendor/autoload.php`, composer PSR-4 mapping and indexing before changing source. Third-party stubs and generated helpers can be configured deliberately but should not be added without confirming a real need.

For formatting, PHPantom first honors explicit `.phpantom.toml` config, then project dependencies such as `laravel/pint` or PHP CS Fixer, then its built-in formatter. Existing project formatters may execute as subprocesses on format operations; do not treat a format operation as pure static analysis. Blade formatting is chosen separately and may use installed Pint/blade-formatter or built-in reindentation.

If repeated false positives occur, capture a minimal reproduction and versions rather than automatically muting diagnostics or modifying global configuration. Read the current version's own CLI help and the project's `.phpantom.toml` first.

Source: https://github.com/PHPantom-dev/phpantom_lsp/blob/main/docs/configuration.md
