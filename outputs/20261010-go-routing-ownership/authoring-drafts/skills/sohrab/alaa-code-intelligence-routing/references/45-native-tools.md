# Native evidence and proof

This guide ships with the skill; it depends on no workstation inventory. Select the needed operation, inspect its repository recipe/configuration, and check only its executable: `Get-Command <tool>` in PowerShell or `command -v <tool>` in POSIX. Check version/dialect when the operation depends on it. Availability is not compatibility.

Do not install, upgrade or allow package-runner downloads as discovery. Use installed project tooling or report the required gate blocked. Inspect scripts before execution: names such as check or dry-run do not establish harmlessness. Bound scope/output and avoid secret payloads. Examples below are read/diagnostic starting points, not universal proof commands; substitute the actual scoped path and inspected project recipe.

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

## Go

Inspect module/workspace/build tags and repository recipes. Use installed Go build/vet/test, formatter/linter or wrapper only for the named property. Configured gofmt/goimports/gofumpt can write; inspect check/diff modes. Configured golangci-lint/gotestsum obey their installed configuration, not a generic flag recipe.

For a dependency-metadata or upgrade question, inspect `go.mod`, `go.sum`, applicable `go.work`,
replacements, toolchain/directive constraints and the repository's dependency-management recipe.
Use /golang-dependency-management for Go dependency-change mechanics. Inspect the installed Go
help and recipe before executing version queries or upgrade/tidy commands: they can download modules,
write manifests or execute tooling. Execute only authorized effects. Do not survey symbols or call
paths unless a separately named compatibility, API-use or impact fact requires that evidence.

Direct configured gopls follows the routing contract's recorded capability gap, with build context
and the operation verified. Bounded native edits and missing diagnostics follow
`references/10-routing-contract.md`; semantic-provider absence alone does not require setup.
Go tests/builds can launch processes, dependencies and generated work; select the authorized scoped
recipe and resource policy rather than assuming pure reads.

## Package scripts and proof

Read package-manager scripts and lockfile/tool configuration; use installed locked tooling, not an on-demand runner that downloads. Stack owners retain test/type/build policy. A script's success covers only the property and scope actually exercised.

On a missing tool, preserve established evidence and select an available equivalent under the routing contract. For proof, an alternative must demonstrate the same acceptance property and environment; otherwise report the exact mandatory command blocked. Graph suggestions, semantic diagnostics, parsed configuration and docs do not replace native execution.

## Native sources

Tool syntax comes from installed help plus primary documentation: [ripgrep](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md), [fd](https://github.com/sharkdp/fd#readme), [ast-grep](https://ast-grep.github.io/guide/introduction.html), [jq](https://jqlang.org/manual/), [yq](https://github.com/mikefarah/yq#readme), [Git](https://git-scm.com/docs), [Composer scripts](https://getcomposer.org/doc/articles/scripts.md), [Laravel Artisan](https://laravel.com/docs/13.x/artisan), [Go commands](https://pkg.go.dev/cmd/go), [gopls](https://go.dev/gopls/). Examples are portable patterns; project recipes and observed compatibility remain authoritative.
