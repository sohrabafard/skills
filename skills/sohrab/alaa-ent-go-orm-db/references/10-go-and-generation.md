# Go baseline and Ent generation

## Select versions

Require **Go 1.27.3 or newer** in the consumer project. For new projects, select the current verified stable Go release.
[Downloads](https://go.dev/dl/) identified **1.27.3** on **2026-11-05**; refresh before selecting or changing the toolchain.
Inspect `go.mod`, `go.work`, build tags, CI/images, and `GOTOOLCHAIN`. Prepare a scoped upgrade when the project is below baseline.
Do not lower this requirement or upgrade unrelated modules. Ent's module directive does not change the consumer baseline.
The `go` directive sets the minimum; `toolchain` suggests a compiler, not an upper bound. Account for workspace precedence.
Pin verified CI/image versions through project policy. Automatic toolchain download requires existing installation authority.

Ent **v0.14.6** was the latest [released version](https://github.com/ent/ent/releases/tag/v0.14.6) verified on **2026-11-05**.
Preserve a supported project version unless the task requires an upgrade. Resolve current releases before choosing a new dependency.
Align runtime/generator versions. Inspect `replace`, forks, templates, hooks, and generation commands first.
Prove generator compatibility through generation/tests, not the installed Go version alone.

## Check the baseline without installing

From the skill root:

```bash
python3 scripts/check_go_baseline.py --project /path/to/module
```

Requires Python 3.10+, readable project files, and installed Go. Select another binary with `--go /absolute/path/to/go`.
The helper reads module/workspace directives and runs only `GOTOOLCHAIN=local go version`.
It performs no writes, downloads, or database access. JSON distinguishes the local compiler from unexercised automatic selection.
Exit codes: `0` baseline met; `1` definite violation; `2` unavailable proof. None proves build or database compatibility.
Without Python, inspect the same directives and run the local version command manually.

Optional `--releases-json /path/to/releases.json` accepts trusted [Go release metadata](https://go.dev/dl/?mode=json).
Record retrieval date. The helper reports newer stable releases without selecting/downloading them; it cannot establish metadata freshness.

## Reproducible setup and generation

[Adoption](15-ent-adoption.md) owns project/schema integration; [runtime](70-runtime-testing.md) owns PostgreSQL driver/client setup.
For authorized setup, the following example pins the verified Ent version using Go tool dependencies:

```bash
go get entgo.io/ent@v0.14.6
go get -tool entgo.io/ent/cmd/ent@v0.14.6
go tool ent new User
go tool ent generate ./ent/schema
```

Initialize only a missing module with `go mod init` and the resolved module path. Preserve existing modules/workspaces.
Run inside that module; create only missing schemas. Commands write files and may download dependencies.
Substitute a newer verified compatible version in both dependency commands together.
`go tool ent` requires the tool directive; the runtime dependency alone does not register it.
Preserve an intentional separate tools module when its version alignment is verified.

For standard generation, a directive in `ent/generate.go` can use `//go:generate go tool ent generate ./schema`.
Run it from the module root with `go generate ./ent`; do not bypass existing project generation conventions.
Preserve a custom `ent/entc.go` when it configures extensions/templates; its usual root invocation is `go run -mod=mod ent/entc.go`.
`entc.Generate` requires the schema path, `*gen.Config`, and options. Verify release-specific imports and flags.
New ignored generator files use `//go:build ignore` followed by a blank line. Regenerate generated files; never repair them manually.
Inspect module and generated diffs for unrelated changes, then run scoped tests.
When deterministic generation is required, a second run must produce no new scoped diff; preserve unrelated dirty files.

## Adapt examples deliberately

| Upstream pattern | Required adaptation |
| --- | --- |
| Old Go/module/image baseline | Apply the baseline and verified toolchain selection above |
| CLI installation through plain `go get`; unpinned `@latest`/`@master`; broad `go get -u ./...` | Use a verified tool directive, module-pinned `go run`, or authorized pinned installation; restrict updates to scope |
| Intentional `tools.go` CLI import | Preserve if compatible; prefer tool directives for new setup |
| Startup `Schema.Create`, reset/drop, `AutoApprove` | Follow [migrations](50-migrations.md); deployed schemas need reviewed versioned changes |
| SQLite, hardcoded DSNs, disabled TLS | Adapt through [runtime](70-runtime-testing.md) to the actual PostgreSQL environment |
| Request queries with background context, panic-style calls, or ignored errors | Propagate caller deadlines and classify errors; reserve panic helpers for suitable tests/tools |
| Raw SQL, savepoints, or optional integrations | Verify selected-release APIs and parameters through [queries](30-ent-queries.md), [transactions](60-transactions-security.md), or [advanced Ent](80-advanced-ent.md) |
| Development-only API such as Blob in the reviewed snapshot | Check released source; never infer support from a documentation page |

Keep compatible older code and serialization behavior. New Go or JSON APIs alone do not justify a rewrite.
If Go, dependencies, or source evidence is unavailable, continue independent design and identify the exact unrun generation/build commands.
Resolve documentation conflicts through [source retrieval](00-sources.md).

Consult [Go toolchain selection](https://go.dev/doc/toolchain) when selection differs from the module directive.
Consult [tool dependencies](https://go.dev/doc/modules/managing-dependencies#tools) and [Ent generation](https://entgo.io/docs/code-gen/) when changing generation mechanics.
