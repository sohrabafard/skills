# Native evidence and proof

Select the operation, inspect its repository recipe and configuration, and check only its executable with `command -v <tool>`. Check the version and dialect when the operation depends on them.

- Never install, upgrade or let a package runner download as discovery. Use the installed project tooling, or report the required gate blocked.
- Inspect a script before you run it: a name such as check or dry-run proves no harmlessness.
- Keep secrets out of commands and their output.
- The commands below are starting points for reads and diagnostics, not proof commands. Substitute the scoped path and the inspected project recipe.

## CLI versus language-service access

- A language-server binary or an editor extension proves no agent access. Access is a supported CLI subcommand, or a connected LSP or MCP operation bound to the intended workspace.
- Do not start a bare server for a CLI answer: LSP needs a client for initialization, document synchronization and capability handling. `pyright-langserver --stdio` starts a protocol server, not a search command.
- Missing access follows the routing contract. It authorizes no bridge installation and no ad hoc client.
- Run from the language root with its configuration and its build or interpreter environment. A nested Composer, module or Python project can differ from the Git root.
- Never switch another client's workspace, and never provision a daemon as discovery.
- Scope each query to the symbols and files you need, and run no whole-project scan for a small read. A focused check does not replace a mandatory full-project gate.
- By default, run no separate analyzer for each subagent.

## Files, structured data and Git

- Text and paths: `rg`, with `-F` for a literal and `-g` for a file type. `rg --files` and installed `fd` differ in their coverage of ignored, hidden and generated files.
- Syntax patterns: installed ast-grep, with a language-bound and path-bound pattern from its help. A syntax match is no binding, type or complete reference list.
- YAML: installed yq, after you identify its implementation, version and expression dialect. Incompatible yq dialects share no flags. A configured language parser is an equivalent.
- Git review: include the untracked files of the scope (`git status --short -- <scope>`), because a diff omits them.

## PHP and Laravel

- Use installed PHP, Composer, Pest or PHPUnit, PHPStan and Pint only through the project recipe and scope. A formatter's fix mode writes: verify its check mode from its help.
- `php artisan route:list` observes registrations only in the intended application and environment, after a successful boot.
- Artisan and Composer scripts can execute project code or reach dependencies. Check their effects against the task authority. Do not use a boot-dependent command to get around a known boot failure.
- PHPantom diagnostics: read `phpantom_lsp analyze --help`, then use the verified Composer root and scoped paths, for example `phpantom_lsp analyze --project-root <project-root> --format json <file-or-directory>`. Findings are not a transport outage: read the structured diagnostics and the exit status. Before you interpret a miss, inspect `.phpantom.toml`, the Composer autoload coverage and the PHP-version assumptions.
- A PHPantom symbol rewrite can miss references in strings or configuration. Read the installed help before `fix`, `format` or `move`.
- Never generate configuration or suppress diagnostics to make a check pass.

## Go

- Configured gofmt, goimports and gofumpt can write: inspect their check and diff modes. Configured golangci-lint and gotestsum obey their installed configuration, not a generic flag recipe.
- For a dependency-metadata or upgrade question, inspect `go.mod`, `go.sum`, an applicable `go.work`, the replacements, the toolchain and directive constraints, and the repository's dependency recipe. Use /golang-dependency-management for the change mechanics.
- Version queries and upgrade or tidy commands can download modules, write manifests or execute tooling. Read the installed Go help and the recipe first, and run only authorized effects.
- Read `gopls help <operation>` for exact flags and scope. Installed CLI candidates: `gopls definition <file.go:line:column>`, `gopls references <file.go:line:column>`, `gopls implementation <file.go:line:column>`, `gopls call_hierarchy <file.go:line:column>` and `gopls check <file.go>`.
- CLI line and column positions are one-based, and columns count UTF-8 bytes. Convert another client's position encoding first.
- Before you interpret an empty answer, check the error and loading output and the build coverage. Rename, code actions and import fixes can write.
- Gopls documents its CLI as experimental and inefficient, so keep its queries bounded. Its built-in MCP is a surface only when it is already configured and exposed, never a setup step.
- Package loading can invoke Go tooling and fetch dependencies, and Go tests and builds can launch processes and generated work. A semantic read grants no permission to download or to change the toolchain: use the authorized scoped recipe, cache policy and resource policy.

## Python

Inspect the configured Pyright recipe, `pyrightconfig.json` or `pyproject.toml`, the interpreter or virtual environment, the imports and the exclusions. A candidate for one diagnostic question is `pyright --project <config-or-project-dir> --outputjson <file>...`. Positional files override the configured input set, so the result is focused evidence, not a full-project pass. A required project-wide gate uses its unmodified repository recipe. Type errors are findings, not provider unavailability: read the JSON diagnostics and the exit status. Never weaken diagnostic levels or create stubs to clear findings.

## Native sources

Tool syntax comes from the installed help and the primary documentation: [ripgrep](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md), [fd](https://github.com/sharkdp/fd#readme), [ast-grep](https://ast-grep.github.io/guide/introduction.html), [jq](https://jqlang.org/manual/), [yq](https://github.com/mikefarah/yq#readme), [Git](https://git-scm.com/docs), [Composer scripts](https://getcomposer.org/doc/articles/scripts.md), [Laravel Artisan](https://laravel.com/docs/13.x/artisan), [Go commands](https://pkg.go.dev/cmd/go), [gopls](https://go.dev/gopls/).
