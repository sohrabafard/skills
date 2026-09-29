Version-sensitive claims in this topic depend on [Go version source ledger](../SOURCES.md).

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
  to `/alaa-observability-soc`.
- **64-bit heap base randomization is on by default.** **Rule:** leave it on.
- **Not new in 1.26:** cgroup-aware `GOMAXPROCS` landed in 1.25 — still set container CPU limits so the runtime has a
  quota to read — and profile-guided optimization has been generally available since 1.21.
## Standard library to reach for

- **`errors.AsType[T]`** — type-safe replacement for the `errors.As(err, &target)` pointer dance. **Rule:** use it in
  new error-mapping code once the directive allows.
- **`slog.NewMultiHandler`** — fans one logger to several sinks without a hand-rolled tee. **Rule:** when a second
  sink is needed, use it; keep the JSON handler as the canonical machine-readable sink.
- **`os/signal.NotifyContext` reports the cause.** Used in `../45-failure-behavior-at-the-call-site.md` section 7.
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
