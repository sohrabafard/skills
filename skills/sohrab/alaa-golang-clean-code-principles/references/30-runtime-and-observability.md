# P9–P11 · Runtime Discipline and Observability

These three principles are what make a service debuggable at 2 a.m.: owned concurrency, explicit configuration,
and telemetry one shared dashboard can read.

## P9 — No Naked Goroutines: Every Concurrent Thing Has an Owner and an Exit

A goroutine exists only inside a worker construct that owns its lifecycle: a bounded pool, `context`
cancellation, a drain wired into `runkit`'s ordered shutdown, and a name in metrics. `go func()` fired from a
handler is a leak, an un-drained buffer, and an invisible failure mode — its panic vanishes, its work dies with
the pod, and no dashboard knows it existed. (Concurrency depth — channels, `errgroup`, race discipline:
`/golang-concurrency` (`$golang-concurrency`), `/golang-context` (`$golang-context`), `/golang-safety`
(`$golang-safety`) through the `/alaa-golang` (`$alaa-golang`) router.)

```go
// WRONG — orphan goroutine: no cancellation, no drain, panics vanish
go func() { flushReceipts(buf) }()

// RIGHT — a worker with a lifecycle, wired into shutdown
func (w *ReceiptFlusher) Run(ctx context.Context) error {
    t := time.NewTicker(w.interval); defer t.Stop()
    for {
        select {
        case <-ctx.Done():
            return w.flush(context.WithoutCancel(ctx)) // final drain
        case <-t.C:
            if err := w.flush(ctx); err != nil { w.metrics.FlushFailures.Inc(); w.log.Error(...) }
        }
    }
}
```

Shutdown is four ordered phases — stop intake, wait for drain, flush, close — and `runkit` gives each phase one
quarter of the total budget, defaulting to 30 s hardcoded in `runkit/lifecycle.go`. A `SHUTDOWN_TIMEOUT` env key
is ratified in the kit's decision register but **not implemented**; there is no such key in `configkit/keys.go`.
Verified against kit source 2026-07-26. A component participates in a phase by implementing that phase's
interface — a worker that implements none is not drained, whatever its `Run` loop does.

**Accepted data loss requires all three of these, named in the pull request.** A buffer that may lose a flush
window on crash is legitimate only when: (1) the service's own design record — a file in the service
repository, cited by path in the PR description — states the maximum number of records and the maximum time
window the buffer may lose; (2) a test proves the buffer is empty after `runkit`'s flush phase completes on
graceful shutdown; (3) a counter metric increments on every dropped record and an alert fires on it. Fewer than
three is a bug, not a design choice. No agent self-certifies data loss.

**Proof.** `go test -race ./...` for the shared state, plus a shutdown test: start the worker, feed it work,
cancel its context, and assert both that `Run` returned and that the buffer is empty and the rows landed.
`goleak` at the end of the package's `TestMain` turns a leaked goroutine into a failing test rather than a
memory graph someone reads later.

## P10 — Config at Boot, Constants for Vocabulary, Nothing Ambient

`os.Getenv` appears in exactly one place: `configkit` loading at boot into a validated struct. Missing or
invalid keys fail the boot, all listed at once, before any port opens. Business code receives config values as
constructor arguments — which is what makes it testable without environment gymnastics. Event names, error
codes, metric names, lane names, and permission names are typed constants, kit-exported where kit-owned, never
inline strings: a typo in an inline string is a silent observability hole no compiler, test, or dashboard will
ever flag.

```go
// WRONG — ambient env read + inline event name, deep in a use case
if os.Getenv("NEWS_TOTP_FORCE") == "true" { log.Info("totp.chek.failed") } // typo ships

// RIGHT — config injected at construction; vocabulary is constants
type TOTPGuard struct{ force bool }
func NewTOTPGuard(cfg Config) *TOTPGuard { return &TOTPGuard{force: cfg.TOTPForce} }
obs.Log(ctx, obskit.EventAuthzDenied, codes.NewsTOTPRequired, ...)
```

**Env-key ownership is fixed.** Keys the kit reads — the `PG_*`, `RABBITMQ_*`, `REDIS_*`, `GATEWAY_PROOF_*`,
`HTTP_*`, `OBSKIT_*` families among them — are kit property. A service never renames one, never prefixes one
with its own name, and never adds a key to a kit-owned family. Service-domain keys are `<SERVICE>_*` and
nothing else. Read the current kit-owned key list from the kit's `CONTRACTS.md` and `configkit/keys.go`; adding
a key to a kit family is a kit change request through `/alaa-go-chi-development` (`$alaa-go-chi-development`).

**Proof.** Two checks. From the service root, `grep -rn --include='*.go' 'os\.Getenv' internal/ cmd/` must
return only the `configkit` wiring site — every other hit is a P10 violation. And a boot test that clears one
required key and asserts the process fails to start with that key named in the error, which proves the key is
actually registered rather than silently defaulted.

## P11 — Observe What You Ship: Bounded Labels, Kit Names, One Correlation Thread

Two things this principle owns, and only two: cardinality discipline and correlation, as applied to kit code.

**Cardinality.** Labels stay bounded — route template, method, status class. Never `user_id`, `project_id`, a
raw path, or error text as a label; an unbounded label is a time-series-database outage on a delay timer.
Identity belongs in logs and traces, never in a label.

```go
// WRONG — unbounded label; this metric will kill the TSDB and the dashboard
httpRequests.WithLabelValues(r.URL.Path, userID).Inc()

// RIGHT — template + class; identity goes in logs/traces, never labels
httpRequests.WithLabelValues(chi.RouteContext(r.Context()).RoutePattern(), statusClass(code)).Inc()
```

**Correlation.** `request_id` and `trace_id` ride every log line; `traceparent` rides every message envelope so
spans survive the broker hop; a consumer continues the producer's trace rather than starting a new one. Sentry
receives panics and programming faults only — never an expected domain error.

**A service never re-exports a kit-owned metric under a service-prefixed name.** The kit-owned name is the name;
the `service` label distinguishes emitters. One renamed metric kills the single shared dashboard the kit exists
to enable. Read the current names from `obskit.KitMetricNames()` and `/alaa-services-contract`
(`$alaa-services-contract`) — never from memory, and never from an example. A change request dated 2026-07-25
proposes prefixing every kit-owned metric name; as of 2026-07-26 it is proposed, not ratified, not implemented.

The rest of observability is owned elsewhere and is not restated here. Which signals a feature is *required* to
emit, the severity rubric, and the definition-of-done gate a shipped feature must pass belong to
`/alaa-observability-soc` (`$alaa-observability-soc`). The *names*
of metrics, events, and error codes belong to `/alaa-services-contract` (`$alaa-services-contract`). Load them;
do not derive a name or a requirement level here.

**Proof.** The kit's `metricname` analyzer flags a raw or re-prefixed kit-owned metric name in Go source; run
`make lint-metricnames` (`go run ./cmd/alaa-metricname-lint .`). Cardinality itself has no analyzer — prove it
with a test that asserts the label-value set of each service-owned metric is drawn from a closed enumeration,
and read the label sets the kit fixes (`obskit.HTTPVariableLabels()` and friends) rather than inventing labels.
Correlation is proven by an end-to-end test that asserts the `request_id` in the HTTP response header appears in
the log line and in the published message envelope for the same operation.
