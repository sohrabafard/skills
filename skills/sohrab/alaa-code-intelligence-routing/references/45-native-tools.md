# Native evidence and proof

This guide ships with the skill; it depends on no workstation inventory. Select the needed operation, inspect its repository recipe/configuration, and check only its executable: `Get-Command <tool>` in PowerShell or `command -v <tool>` in POSIX. Check version/dialect when the operation depends on it. Availability is not compatibility.

Do not install, upgrade or allow package-runner downloads as discovery. Use installed project tooling or report the required gate blocked. Inspect scripts before execution: names such as check or dry-run do not establish harmlessness. Bound scope/output and avoid secret payloads. Examples below are read/diagnostic starting points, not universal proof commands; substitute the actual scoped path and inspected project recipe.

## CLI versus language-service access

Distinguish the executable, supported CLI subcommand, connected LSP/MCP operation and bound workspace/document version. A language-server binary or editor extension proves no agent access; a supported CLI needs no Serena, hooks or MCP. Do not invoke a bare server for a CLI answer: LSP requires initialization, document synchronization and capability handling through an available client. Missing access follows the routing contract; it does not authorize bridge installation or ad hoc client construction as evidence fallback.

Resolve the Git worktree and language root; a nested Composer/module/Python project can differ from the Git root. Run from the intended language root with matching configuration, build/interpreter environment and files. Saved-file CLI results do not describe unsaved buffers. Reuse a suitable authorized session bound to that target; do not switch another client's workspace or provision daemons as discovery.

Batch compatible diagnostics and scope queries to needed symbols/files. Rerun only after relevant source/configuration/environment changes or a new uncovered question; avoid repeated cold loads and whole-project scans per small read. Focused checks do not replace mandatory full-project gates. Size concurrency to available resources and competing work; do not multiply analyzers per subagent by default.

## Files, literals and syntax

| Need | Candidate and bounded example | Limit/fallback |
|---|---|---|
| Locate paths | `rg --files <scope>`; installed `fd '<name>' <scope>` | Ignore/hidden/generated coverage differs; native shell enumeration is an alternative with explicit coverage |
| Literal/Markdown/config occurrence | `rg -n -F -- '<literal>' <scope>`; `rg -n -g '*.md' -- '<pattern>' <scope>` | A miss proves absence only in a demonstrated complete searched scope |
| Known region | Native file read limited to needed lines | Does not prove call/reference coverage |
| Supported syntax pattern | Installed ast-grep with language/path-bound pattern selected from its help | Syntax matches are not bindings/types or complete references; native text can supply partial evidence |

In PowerShell a bounded region can use `Get-Content -LiteralPath <path> | Select-Object -Skip <offset> -First <count>`. In POSIX use `sed -n '<first>,<last>p' <path>`. Reuse adequate graph source instead of performing these reads again.

## Structured data and saved working state

- JSON: installed `jq '<specific-selector>' <path>`, or an available language parser.
- YAML: installed yq after identifying its implementation/version and expression dialect; never assume incompatible yq dialects share flags. Use a configured language parser when equivalent.
- TOML and other formats: repository checker or an installed format-aware parser. Regex can locate text, not validate syntax/effective values.
- Git: `git rev-parse --show-toplevel`, `git branch --show-current`, `git status --short -- <scope>`, `git diff -- <scope>`, `git diff --cached -- <scope>`, `git show <ref>:<path>`. Include untracked scoped files in review; diff alone omits them.

Parsing proves selected source data/syntax, not effective application configuration. Git identifies saved worktree/history, not runtime service/environment. Resolve symlinks or root aliases where identity is ambiguous.

## PHP and Laravel

Inspect Composer scripts, installed metadata and test/static/formatter configuration. Use installed PHP/Composer, configured Pest/PHPUnit, PHPStan and Pint only through the relevant project recipe/scope. A formatter's fix mode writes; a check mode must be verified from its help.

`php artisan route:list` can observe registrations only in the intended application/environment after successful boot. Inspect filtering/output options in installed help before narrowing. Artisan and Composer scripts may execute project code or reach dependencies; inspect their effects and task authority. Do not use boot-dependent commands to bypass a known boot failure. A source route/migration read supplies intent only.

For PHPantom diagnostics, inspect `phpantom_lsp analyze --help`, then use the verified Composer root and scoped paths, for example `phpantom_lsp analyze --project-root <project-root> --format json <file-or-directory>`. Read structured diagnostics and exit status: findings are not a transport outage. Inspect `.phpantom.toml`, Composer autoload coverage and PHP-version assumptions before interpreting a miss. Consult installed help before `fix`, `format` or `move`; these can write, and symbol rewrites may miss string/configuration references. Do not generate configuration or suppress diagnostics to make a check pass.

## Go

Inspect module/workspace/build tags and repository recipes. Use installed Go build/vet/test, formatter/linter or wrapper only for the named property. Configured gofmt/goimports/gofumpt can write; inspect check/diff modes. Configured golangci-lint/gotestsum obey their installed configuration, not a generic flag recipe.

For a dependency-metadata or upgrade question, inspect `go.mod`, `go.sum`, applicable `go.work`,
replacements, toolchain/directive constraints and the repository's dependency-management recipe.
Use /golang-dependency-management for Go dependency-change mechanics. Inspect the installed Go
help and recipe before executing version queries or upgrade/tidy commands: they can download modules,
write manifests or execute tooling. Execute only authorized effects. Survey symbols/call paths only for a separately named compatibility, API-use or impact fact.

Inspect `gopls help <operation>` for exact flags and scope. Installed CLI candidates include
`gopls definition <file.go:line:column>`, `gopls references <file.go:line:column>`,
`gopls implementation <file.go:line:column>`, `gopls call_hierarchy <file.go:line:column>`
and `gopls check <file.go>`. CLI line/column positions are one-based and columns count UTF-8
bytes; do not copy another client's position encoding without conversion. Check error/loading
output and build coverage before interpreting an empty answer. Rename/code actions/import fixes
can write; inspect flags and effects before applying them. Gopls documents its CLI as experimental
and inefficient; use bounded queries under the cost rule above. Its built-in MCP is another
possible surface only when already configured and exposed, not an automatic setup step.
Package loading can invoke Go tooling and fetch dependencies; honor the authorized runtime/cache
policy rather than treating a semantic read as permission to download or change the toolchain.
Go tests/builds can launch processes, dependencies and generated work; select the authorized scoped
recipe and resource policy rather than assuming pure reads.

## Python

Inspect the configured Pyright recipe, `pyrightconfig.json` or `pyproject.toml`, interpreter/virtual
environment, imports and exclusions. For a selected diagnostic question, a candidate is
`pyright --project <config-or-project-dir> --outputjson <file>...`; positional files override the
configured input set, so this is focused evidence, not a full-project pass. A required project-wide
gate uses its unmodified repository recipe. Read JSON diagnostics and exit status; type errors
are findings, not provider unavailability. Do not weaken diagnostic levels or create stubs merely
to clear findings. Running `pyright-langserver --stdio` starts a protocol server, not a standalone
reference-search command.

## Package scripts and proof

Read package-manager scripts and lockfile/tool configuration; use installed locked tooling, not an on-demand runner that downloads. Stack owners retain test/type/build policy. A script's success covers only the property and scope actually exercised.

On a missing tool, preserve established evidence and select an available equivalent under the routing contract. For proof, an alternative must demonstrate the same acceptance property and environment; otherwise report the exact mandatory command blocked. Graph suggestions, semantic diagnostics, parsed configuration and docs do not replace native execution.

## Native sources

Tool syntax comes from installed help plus primary documentation: [ripgrep](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md), [fd](https://github.com/sharkdp/fd#readme), [ast-grep](https://ast-grep.github.io/guide/introduction.html), [jq](https://jqlang.org/manual/), [yq](https://github.com/mikefarah/yq#readme), [Git](https://git-scm.com/docs), [Composer scripts](https://getcomposer.org/doc/articles/scripts.md), [Laravel Artisan](https://laravel.com/docs/13.x/artisan), [Go commands](https://pkg.go.dev/cmd/go), [gopls](https://go.dev/gopls/). Examples are portable patterns; project recipes and observed compatibility remain authoritative.
