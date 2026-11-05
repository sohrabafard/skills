# Go baseline and Ent code generation

## Contents

- [Version decision](#version-decision)
- [Read-only baseline check](#read-only-baseline-check)
- [Reproducible generation](#reproducible-generation)
- [Modernize upstream examples](#modernize-upstream-examples)
- [Unavailable evidence](#unavailable-evidence)

## Version decision

The minimum supported consumer baseline for this skill is **Go 1.27.3**.
On **2026-11-05**, the official download and release-history pages identify Go 1.27.3 as the latest stable release.
It was released on 2026-10-19. Refresh those pages before choosing or changing a toolchain.

For a new project, select the current stable Go release, never below the minimum above.
Inspect existing projects' `go.mod`, `go.work`, build tags, CI, build images, and selected toolchains.
Flag a lower baseline and prepare the required upgrade. Do not silently lower this minimum or upgrade unrelated modules.
An older module directive in Ent itself does not lower the consumer application's requirement.

The `go` directive declares the minimum toolchain and language version. A `toolchain` directive suggests a toolchain; it is not an upper bound.
Use `go 1.27.3` for today's minimum. Set a newer verified minimum when the project adopts it.
Pin the selected compiler in CI and images through project policy. Do not invent an image tag or digest.
Inspect `GOTOOLCHAIN` and workspace precedence. Automatic toolchain download is an installation side effect and requires existing authorization.

Sources: [Go downloads](https://go.dev/dl/), [release history](https://go.dev/doc/devel/release), [toolchain selection](https://go.dev/doc/toolchain).

## Read-only baseline check

Run the optional standard-library-only helper from the skill root:

```bash
python3 scripts/check_go_baseline.py --project /path/to/module
```

Prerequisites: Python 3.10 or newer, a readable module directory, and an installed Go executable.
Use `--go /absolute/path/to/go` when the intended compiler is not on `PATH`.
The helper reads module/workspace directives and runs only `GOTOOLCHAIN=local go version`.
It neither writes files, downloads tools, nor connects to databases.
JSON output distinguishes the installed compiler from automatic toolchain selection, which it does not exercise.

Exit `0` means the inspected baseline meets the minimum; `1` means a definite violation; `2` means unavailable proof.
Do not interpret `0` as a build, dependency, or PostgreSQL compatibility test.
If Python is unavailable, inspect the same files and `GOTOOLCHAIN=local go version` manually.

Optionally pass `--releases-json /path/to/releases.json` containing trusted output from `https://go.dev/dl/?mode=json`.
The helper reports a newer stable release without selecting or downloading it. Record that metadata's retrieval date.
The helper does not establish freshness; refresh the official source when choosing an upgrade.

## Reproducible generation

Ent **v0.14.6** is the latest released Ent version verified on 2026-11-05.
Preserve the project's supported version unless an upgrade is required or requested.
Pin runtime and generator to the same module version. Avoid a global generator from an unknown release.
Inspect `replace` directives, forks, generator hooks, templates, and `go:generate` commands before executing them.

For authorized new-project dependency setup, this versioned example uses Go's tool dependency support:

```bash
go get entgo.io/ent@v0.14.6
go get -tool entgo.io/ent/cmd/ent@v0.14.6
go tool ent new User
go tool ent generate ./ent/schema
```

Run from the module root. These commands change module/generated files and may download dependencies.
Resolve a newer Ent release before substituting its version; keep runtime and generator aligned.
`go tool ent` requires its tool directive. Merely requiring Ent as a runtime dependency does not register the tool.
Preserve an existing separate tools module if its version alignment is verified.

Preserve a project-local `ent/entc.go` generator when it configures extensions or templates.
Its typical invocation is `go run -mod=mod ent/entc.go` from the project root.
The API is `entc.Generate(schemaPath, *gen.Config, options...)`; do not omit the configuration argument.
Use `//go:build ignore` with a blank line in a new ignored generator file.
Derive flags and imports from the selected release. Regenerate generated files instead of hand-editing them.

Review `go.mod`, `go.sum`, and generated diffs for unrelated changes.
Run the relevant tests. If deterministic generation is required, confirm a second run produces no new scoped diff.
Preserve unrelated dirty-tree work; do not require or manufacture a globally clean worktree.

Sources: [Go tool dependencies](https://go.dev/doc/modules/managing-dependencies#tools), [Ent generation](https://entgo.io/docs/code-gen/), [Ent releases](https://github.com/ent/ent/releases).

## Modernize upstream examples

Preserve compatible older code. Change examples only for verified language, API, dependency, security, or operational reasons.

| Source pattern | Treatment for this skill's consumer |
| --- | --- |
| Historical Go directive, toolchain, CI image, or bootstrap | Apply the baseline above to module, workspace, CI, and build image |
| `go get` described as installing a CLI | Use a verified tool directive, module-pinned `go run`, or authorized version-pinned installation |
| `@latest`, `@master`, or `go get -u ./...` | Resolve and pin compatible versions; restrict upgrades to the task |
| `tools.go` blank import retaining a CLI | Preserve if intentional; prefer the supported tool directive for new setup |
| Startup `client.Schema.Create(ctx)` | Restrict to isolated development; use versioned migrations for deployed schemas |
| SQLite, hardcoded DSNs, disabled TLS, `AutoApprove`, or reset commands | Adapt to PostgreSQL and actual authorization; no production copy-paste |
| `context.Background()` in a request query | Propagate caller context and a bounded deadline |
| `log.Fatal`, panic-style `SaveX`/`OnlyX`, or ignored errors | Return and classify service errors; restrict panic-style calls to suitable tests/tools |
| Legacy imports, flags, or extension examples | Verify against selected released source before generation |
| `tx.ExecContext("SAVEPOINT user_created")` | Supply `ctx` and verify raw-SQL feature support and transaction ownership |
| Raw SQL with assumed `?` conversion | Use dialect-aware builders and bound parameters; `sql.ExprP` is not placeholder translation |
| Master-only Blob APIs | Gate on released support; the bundled blob-storage page is development-only for v0.14.6 |

New Go language/library features are optional modernization opportunities, not a reason to rewrite stable Ent code.
Preserve serialization contracts; do not switch JSON packages solely to look current.
Modernize optional gRPC/GraphQL APIs only after checking their connection/error semantics and dependencies.

## Unavailable evidence

Without Go, Ent source, or generation dependencies, continue independent design/source inspection.
Report generation/compilation as untested and provide the exact commands needed in the consuming environment.
When official documentation and cached examples conflict, use selected released source and record the discrepancy.
The installed Go version alone cannot prove generator compatibility; generation and tests supply that evidence.
