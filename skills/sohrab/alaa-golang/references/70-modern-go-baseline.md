# Modern Go Baseline

Read this before using a language feature, a standard-library API, or a toolchain behaviour you have not confirmed the
repository supports.

## The version this file was written against

Go **1.26**. Every claim below was verified against the official release notes at `https://tip.golang.org/doc/go1.26`
and the language specification at `https://go.dev/ref/spec` on **2026-07-26**. The kit module's directive is
`go 1.26.5` (`alaa-go-chi/go.mod`, read the same day).

This is the only place in this skill that names a Go version. **Rule:** before relying on any statement here, confirm
it against the source named in `SOURCES.md`; a release since 2026-07-26 makes this file stale, not authoritative.

## Read the directive before you write the feature

**Rule:** read the `go` directive in the repository's own `go.mod` before using any feature below. A feature gated on
Go 1.26 requires that directive to be `1.26` or higher; a lower directive makes the compiler reject the code.

**Forbidden:** raising a `go` directive as a side effect of another change. **Rule:** raise it only when the code needs
a feature the current directive forbids, in its own commit, and say in the report which feature required it and which
CI job proves the toolchain is available.

**Forbidden:** lowering a `go` directive.

**Verified fact:** `go mod init` under a 1.26 toolchain writes `go 1.25.0`, one minor below the toolchain, so a fresh
module is compatible with both currently supported releases. **Rule:** leave it there and raise it with
`go get go@1.26.0` only under the rule above.

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

## Runtime and GC

- **Green Tea GC is the default**, reducing GC overhead materially on allocation-heavy programs, with a further gain
  on newer amd64 through vector-instruction scanning. **Forbidden:** setting `GOEXPERIMENT=nogreenteagc` in a
  production image; the default is what upstream tests and hardens, and the opt-out is expected to be removed.
  **Rule:** re-baseline p99 latency and GC metrics after the upgrade, and keep reducing allocation churn — GC cost
  still scales with allocation volume.
- **More slice backing stores stack-allocate.** **Rule:** give `make([]T, n, c)` a concrete length and capacity and do
  not store or return the slice from the function that made it, so escape analysis can keep it on the stack.
- **cgo call overhead dropped about 30%.** **Rule:** keep API services on `CGO_ENABLED=0` for static, distroless,
  cross-compilable builds. **Forbidden:** adopting cgo because its overhead fell; it remains far more expensive than a
  Go call.
- **New scheduler metrics exist under `runtime/metrics`:** goroutine counts by state, thread count, and goroutines
  created. **Rule:** export these instead of polling `runtime.NumGoroutine`. Which of them must be alerted on belongs
  to `/alaa-observability-soc` (`$alaa-observability-soc`).
- **64-bit heap base randomization is on by default.** **Rule:** leave it on.
- **Not new in 1.26:** cgroup-aware `GOMAXPROCS` landed in 1.25 — still set container CPU limits so the runtime has a
  quota to read — and profile-guided optimization has been generally available since 1.21.

## Standard library to reach for

- **`errors.AsType[T]`** — type-safe replacement for the `errors.As(err, &target)` pointer dance. **Rule:** use it in
  new error-mapping code once the directive allows.
- **`slog.NewMultiHandler`** — fans one logger to several sinks without a hand-rolled tee. **Rule:** when a second
  sink is needed, use it; keep the JSON handler as the canonical machine-readable sink.
- **`os/signal.NotifyContext` reports the cause.** Used in `45-failure-behavior-at-the-call-site.md` section 7.
- **`net/http` behaviour changed in three ways that break existing code:** the `Client` scopes cookies to
  `Request.Host`; `ServeMux` trailing-slash redirects are now **307**, preserving method and body; and
  `HTTP2Config.StrictMaxConcurrentRequests` makes HTTP/2 pool behaviour predictable. **Rule:** before upgrading a
  service, search its tests for an assertion on `301` from a trailing-slash redirect and for any cookie behaviour that
  assumed the dial target rather than `Host`.
- **`net/url.Parse` is stricter** and rejects malformed host colons. **Rule:** add URL-parsing tests to any service
  that ingests externally supplied URLs before upgrading it. `GODEBUG=urlstrictcolons=0` restores the old behaviour
  and is a migration window, not a fix — remove it in the same release that adds the tests.
- **Free wins requiring no code change:** `io.ReadAll` allocates less and returns a minimally sized slice;
  `fmt.Errorf` is cheaper for unformatted strings; `bytes.Buffer.Peek(n)` gives lookahead without consuming.

## Testing

- **`t.ArtifactDir()` with `go test -artifacts`** writes golden files, captured payloads, and failure dumps to a
  persistent directory, unlike the auto-cleaned `t.TempDir()`. **Rule:** use it for anything a CI job must upload, and
  point the pipeline's artifact step at `-outputdir`.
- **`for b.Loop() { … }`** no longer blocks inlining of the loop body. **Rule:** write benchmarks with `b.Loop` rather
  than `for i := 0; i < b.N; i++`, and re-baseline any existing `b.Loop` benchmark after upgrading, because its
  numbers changed.
- **`testing/cryptotest.SetGlobalRandom`** is how deterministic crypto is done now. **Forbidden:** linking it into a
  production binary.
- **Not changed by 1.26:** `testing/synctest`, `testing.T.Context`, and fuzzing. **Rule:** verify their API against the
  1.24 and 1.25 notes, not the 1.26 page.

## Security-relevant changes

Go 1.26 changes TLS defaults, deprecates several legacy `GODEBUG` toggles ahead of tighter 1.27 defaults, makes crypto
key generation ignore caller-supplied randomness, deprecates PKCS#1 v1.5 encryption padding, adds `crypto/hpke` and KEM
interfaces, and ships a new FIPS 140-3 module version.

**Rule:** two of these are mechanical and yours to apply:

- Remove any custom `rand.Reader` passed into `crypto/rand.Prime`, `crypto/dsa.GenerateKey`,
  `crypto/ecdh.Curve.GenerateKey`, or `crypto/ed25519.GenerateKey` — it is now a no-op, so code that looks
  deterministic no longer is. Replace deterministic test usage with `testing/cryptotest.SetGlobalRandom`.
- Replace `go tool`-era manual `Certificate.Leaf` population, which 1.27 makes unnecessary.

**Rule:** everything else in this paragraph — which TLS minimum version a service sets, whether a legacy cipher or key
exchange may be re-enabled, whether FIPS enforcement applies, which padding a service may use — is a posture decision
owned by `/alaa-security-review` (`$alaa-security-review`). Take it there. **Forbidden:** setting
`tls.Config.CurvePreferences`, `MinVersion`, or any `GODEBUG` TLS toggle on your own judgement.

## Experiments

**Forbidden:** shipping any `GOEXPERIMENT`-gated package or behaviour in a production build. That covers
`goroutineleakprofile`, `simd`, `runtimesecret`, and `jsonv2`.

**Rule:** `GOEXPERIMENT=goroutineleakprofile` belongs in staging, soak, and CI runs, where a goroutine permanently
blocked on a concurrency primitive is exactly what you want reported. Enable it there and nowhere else.

**Rule:** production JSON stays on `encoding/json` until `encoding/json/v2` is promoted out of experiment; confirm its
status on pkg.go.dev before proposing adoption.

## Adoption rules

1. Match the repository's directive; raise it only for a feature the code uses, in its own commit, with the reason
   stated.
2. Run `go fix ./...` with `gofmt`, `go vet`, and `golangci-lint` as a reviewed pass; never blind-commit it.
3. Use `new(expr)` for pointer-to-value fields once the directive allows it.
4. Use `errors.AsType[T]` in new error mapping and `context.Cause` in the shutdown path.
5. Leave Green Tea GC and heap-base randomization on; re-baseline latency and GC metrics after upgrading.
6. Export the new scheduler metrics; take alert thresholds from `/alaa-observability-soc` (`$alaa-observability-soc`).
7. Add URL-parsing tests before upgrading a service that ingests external URLs.
8. Take every TLS, cipher, padding, and FIPS decision to `/alaa-security-review` (`$alaa-security-review`).
9. Write persistent test output to `t.ArtifactDir()`; benchmark with `b.Loop` and re-baseline.
10. Keep every experiment out of production builds.
