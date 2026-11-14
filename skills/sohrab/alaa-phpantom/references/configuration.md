# PHPantom project configuration, Laravel and Composer

PHPantom chooses the Composer project root to resolve `composer.json`, `vendor` and PSR-4 autoload mappings. A monorepo can have several Composer projects; run the CLI separately at each Composer root, and do not run it from one root for all subprojects.

Most repositories need no `.phpantom.toml`; avoid running `phpantom_lsp init` simply to set up this plugin. An existing `.phpantom.toml` is authoritative. Configuration groups described upstream include `[indexing]` (include/exclude and extensions), `[stubs]` (overrides), `[formatting]` (formatter selection), `[phpstan]`, `[laravel.schema]` and `[laravel.migrations]`.

For Laravel, many symbols are inferred from Eloquent relations, scopes, casts, database schemas and migrations. If a class known to Composer is marked `unknown_class`, check the filesystem root, that `vendor/autoload.php` is valid, the Composer PSR-4 mapping and the indexing before you change source. Third-party stubs and generated helpers can be configured deliberately, but they should not be added until you confirm a real need.

For formatting, PHPantom first honors explicit `.phpantom.toml` config, then project dependencies such as `laravel/pint` or PHP CS Fixer, then its built-in formatter. Existing project formatters may execute as subprocesses on format operations; do not treat a format operation as pure static analysis. Blade formatting is chosen separately and may use an installed Pint or blade-formatter, or the built-in reindentation.

If repeated false positives occur, capture a minimal reproduction and versions rather than automatically muting diagnostics or modifying global configuration. Read the current version's own CLI help and the project's `.phpantom.toml` first.

Source: https://github.com/PHPantom-dev/phpantom_lsp/blob/main/docs/configuration.md
