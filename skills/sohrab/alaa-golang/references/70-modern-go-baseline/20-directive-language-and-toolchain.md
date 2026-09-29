Version-sensitive claims in this topic depend on [Go version source ledger](../SOURCES.md).

## Read the directive before you write the feature

**Rule:** read the `go` directive in the repository's own `go.mod` before using any feature below. A feature gated on
Go 1.26 requires that directive to be `1.26` or higher; a lower directive makes the compiler reject the code.

**Forbidden:** raising a `go` directive as a side effect of another change. **Rule:** raise it only when the code needs
a feature the current directive forbids, in its own commit, and say in the report which feature required it and which
CI job proves the toolchain is available.

**Forbidden:** lowering a `go` directive.

**Verified fact:** `go mod init` under a 1.26 toolchain writes `go 1.25.0`, one minor below the toolchain, so the generated directive targets the preceding release. This is a 1.26 observation, not a claim about
the current support window; inspect new modules rather than assuming their directive. **Rule:** raise it with
`go get go@<approved-version>` only under the rule above.

**Rule:** `GOEXPERIMENT` is a build-time setting for compiler and runtime experiments; `GODEBUG` is a runtime setting
for compatibility toggles. Setting one where the other was meant produces a flag that silently does nothing — check
which you need before writing it into a Dockerfile, a Makefile, or a manifest.
## Language

- **`new` accepts an expression.** `new(x)` allocates a variable of `x`'s type, initialized to `x`, and returns its
  address; an untyped constant converts to its default type first. `new(int64(300))` yields `*int64`.
  **Rule:** once the directive is `1.26` or higher, build pointer-to-value fields with `new(expr)` rather than a
  `x := v; p := &x` pair or a `ptr[T]`/`ToPtr` helper. It removes the loop-variable-address aliasing bug by
  construction. `new(T)` for a type is unchanged.
- **Self-referential generic constraints compile.** `type Adder[A Adder[A]] interface { Add(A) A }` is now legal.
  **Rule:** use it only where a method must return the concrete implementing type — self-typed builders, fluent APIs,
  numeric or monoid interfaces. **Forbidden:** a generic constraint in a domain, application, or repository port where
  a plain interface expresses the same contract; the port's readability is what those layers are for.
## Toolchain

- **`go fix` is where modernizers live.** It was rebuilt on the `go/analysis` framework that `go vet` uses and ships
  behaviour-preserving fixers for modern idioms and standard-library APIs. **Rule:** run `go fix ./...` on a clean
  worktree as a modernization pass, review the whole diff, and land it as its own commit with no behavioural change
  mixed in. **Forbidden:** committing its output unreviewed — it can touch many files.
- **`//go:fix inline` migrates call sites mechanically.** **Rule:** when deprecating or renaming an exported symbol in
  a shared library, keep a thin equivalent annotated `//go:fix inline` so consumers migrate with `go fix ./...`
  instead of hand-edits.
- **`go tool doc` was deleted.** **Rule:** use `go doc`; update any Makefile, CI step, or image that shells out to the
  old form.
