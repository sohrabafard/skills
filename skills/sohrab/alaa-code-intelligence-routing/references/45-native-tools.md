# Native evidence and proof

This guide ships with the skill and depends on no workstation inventory. Select the needed operation, inspect its repository recipe and configuration, and check only its executable with `command -v <tool>`. Check the version and dialect when the operation depends on them. Availability is not compatibility.

Do not install, upgrade or allow package-runner downloads as discovery. Use installed project tooling or report the required gate blocked. Inspect scripts before execution: names such as check or dry-run do not establish harmlessness. Bound the scope and the output, and avoid secret payloads. The examples below are starting points for reads and diagnostics, not universal proof commands. Substitute the actual scoped path and the inspected project recipe.

## CLI versus language-service access

Distinguish the executable, a supported CLI subcommand, a connected LSP or MCP operation, and the bound workspace and document version. A language-server binary or an editor extension proves no agent access. A supported CLI needs no Serena, hooks or MCP. Do not invoke a bare server for a CLI answer: LSP requires initialization, document synchronization and capability handling through an available client. Missing access follows the routing contract. It does not authorize bridge installation or ad hoc client construction as an evidence fallback.

Resolve the Git worktree and the language root, because a nested Composer, module or Python project can differ from the Git root. Run from the intended language root with the matching configuration, build or interpreter environment, and files. Saved-file CLI results do not describe unsaved buffers. Reuse a suitable authorized session bound to that target. Do not switch another client's workspace, and do not provision daemons as discovery.

Batch compatible diagnostics, and scope queries to the needed symbols and files. Rerun only after a relevant change to source, configuration or environment, or for a new uncovered question. Avoid repeated cold loads and a whole-project scan for each small read. Focused checks do not replace mandatory full-project gates. Size concurrency to the available resources and the competing work. Do not run a separate analyzer for each subagent by default.

## Files, literals and syntax

| Need | Candidate and bounded example | Limit or fallback |
|---|---|---|
| Locate paths | `rg --files <scope>`; installed `fd '<name>' <scope>` | Coverage of ignored, hidden and generated files differs. Native shell enumeration is an alternative with explicit coverage |
| Occurrence of a literal, or of text in Markdown or configuration | `rg -n -F -- '<literal>' <scope>`; `rg -n -g '*.md' -- '<pattern>' <scope>` | A miss proves absence only in a demonstrated complete searched scope |
| Known region | Native file read limited to needed lines | Does not prove call or reference coverage |
| Supported syntax pattern | Installed ast-grep with a language-bound and path-bound pattern selected from its help | Syntax matches are not bindings, types or complete references. Native text can supply partial evidence |

Read a bounded region with `sed -n '<first>,<last>p' <path>`. Reuse adequate graph source instead of performing these reads again.

## Structured data and saved working state

- JSON: installed `jq '<specific-selector>' <path>`, or an available language parser.
- YAML: installed yq, after you identify its implementation, version and expression dialect. Never assume that incompatible yq dialects share flags. Use a configured language parser when it is equivalent.
- TOML and other formats: a repository checker or an installed format-aware parser. Regex can locate text, but it cannot validate syntax or effective values.
- Git: `git rev-parse --show-toplevel`, `git branch --show-current`, `git status --short -- <scope>`, `git diff -- <scope>`, `git diff --cached -- <scope>`, `git show <ref>:<path>`. Include untracked scoped files in review, because diff alone omits them.

Parsing proves the selected source data and syntax, not the effective application configuration. Git identifies the saved worktree and history, not the runtime service or environment. Resolve symlinks or root aliases where identity is ambiguous.

## PHP and Laravel

Inspect Composer scripts, installed metadata and the test, static-analysis and formatter configuration. Use installed PHP and Composer, and configured Pest or PHPUnit, PHPStan and Pint, only through the relevant project recipe and scope. A formatter's fix mode writes. Verify a check mode from its help.

`php artisan route:list` can observe registrations only in the intended application and environment after a successful boot. Inspect the filtering and output options in installed help before narrowing. Artisan and Composer scripts may execute project code or reach dependencies; inspect their effects and the task authority. Do not use boot-dependent commands to bypass a known boot failure. A read of a source route or migration supplies intent only.

For PHPantom diagnostics, inspect `phpantom_lsp analyze --help`, then use the verified Composer root and scoped paths, for example `phpantom_lsp analyze --project-root <project-root> --format json <file-or-directory>`. Read structured diagnostics and exit status: findings are not a transport outage. Inspect `.phpantom.toml`, Composer autoload coverage and PHP-version assumptions before interpreting a miss. Consult installed help before `fix`, `format` or `move`. These can write, and symbol rewrites may miss references in strings or configuration. Do not generate configuration or suppress diagnostics to make a check pass.

## Go

Inspect the module, workspace, build tags and repository recipes. Use installed Go build, vet or test, a formatter, a linter or a wrapper only for the named property. Configured gofmt, goimports and gofumpt can write; inspect their check and diff modes. Configured golangci-lint and gotestsum obey their installed configuration, not a generic flag recipe.

For a dependency-metadata or upgrade question, inspect `go.mod`, `go.sum`, applicable `go.work`, replacements, toolchain and directive constraints, and the repository's dependency-management recipe. Use /golang-dependency-management for Go dependency-change mechanics. Inspect the installed Go help and recipe before executing version queries or upgrade or tidy commands, because they can download modules, write manifests or execute tooling. Execute only authorized effects. Survey symbols and call paths only for a separately named compatibility, API-use or impact fact.

Inspect `gopls help <operation>` for exact flags and scope. Installed CLI candidates include
`gopls definition <file.go:line:column>`, `gopls references <file.go:line:column>`,
`gopls implementation <file.go:line:column>`, `gopls call_hierarchy <file.go:line:column>`
and `gopls check <file.go>`. CLI line and column positions are one-based, and columns count UTF-8 bytes. Do not copy another client's position encoding without conversion. Check the error and loading output and the build coverage before interpreting an empty answer. Rename, code actions and import fixes can write; inspect their flags and effects before applying them. Gopls documents its CLI as experimental and inefficient, so use bounded queries under the cost rule above. Its built-in MCP is another possible surface only when it is already configured and exposed, not an automatic setup step. Package loading can invoke Go tooling and fetch dependencies. Honor the authorized runtime and cache policy rather than treating a semantic read as permission to download or change the toolchain. Go tests and builds can launch processes, dependencies and generated work. Select the authorized scoped recipe and resource policy rather than assuming pure reads.

## Python

Inspect the configured Pyright recipe, `pyrightconfig.json` or `pyproject.toml`, the interpreter or virtual environment, imports and exclusions. For a selected diagnostic question, a candidate is `pyright --project <config-or-project-dir> --outputjson <file>...`. Positional files override the configured input set, so this is focused evidence, not a full-project pass. A required project-wide gate uses its unmodified repository recipe. Read JSON diagnostics and exit status: type errors are findings, not provider unavailability. Do not weaken diagnostic levels or create stubs merely to clear findings. Running `pyright-langserver --stdio` starts a protocol server, not a standalone reference-search command.

## Package scripts and proof

Read package-manager scripts and the lockfile and tool configuration. Use installed locked tooling, not an on-demand runner that downloads. Stack owners retain test, type and build policy. A script's success covers only the property and scope actually exercised.

On a missing tool, preserve established evidence and select an available equivalent under the routing contract. For proof, an alternative must demonstrate the same acceptance property in the same environment; otherwise, report the exact mandatory command blocked. Graph suggestions, semantic diagnostics, parsed configuration and docs do not replace native execution.

## Native sources

Tool syntax comes from installed help plus primary documentation: [ripgrep](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md), [fd](https://github.com/sharkdp/fd#readme), [ast-grep](https://ast-grep.github.io/guide/introduction.html), [jq](https://jqlang.org/manual/), [yq](https://github.com/mikefarah/yq#readme), [Git](https://git-scm.com/docs), [Composer scripts](https://getcomposer.org/doc/articles/scripts.md), [Laravel Artisan](https://laravel.com/docs/13.x/artisan), [Go commands](https://pkg.go.dev/cmd/go), [gopls](https://go.dev/gopls/). Examples are portable patterns; project recipes and observed compatibility remain authoritative.
