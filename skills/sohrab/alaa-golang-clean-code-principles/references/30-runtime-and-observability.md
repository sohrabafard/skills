# P9–P11 · Runtime Discipline and Observability

These three principles are what make a service debuggable at 2 a.m.: owned concurrency, explicit configuration,
and telemetry that one shared dashboard can actually read.

## P9 — No Naked Goroutines: Every Concurrent Thing Has an Owner and an Exit

A goroutine exists only inside a worker construct that owns its lifecycle: bounded pool, `context`
cancellation, drain-on-shutdown through `runkit`'s ordered shutdown (stop intake → drain workers → flush
buffers → close pools), and a name in metrics. `go func()` fired from a handler is a leak, an un-drained
buffer, and an invisible failure mode — its panic vanishes, its work dies with the pod, and no dashboard knows
it existed. (Concurrency depth — channels, errgroup, race discipline: `golang-concurrency`, `golang-context`,
`golang-safety` via the `alaa-golang` router.)

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

Accepted-loss semantics (a buffer that may lose one flush window on crash) are legitimate — but only when the
design document says so explicitly and the flush is drained on graceful shutdown. Undocumented loss is a bug.

## P10 — Config at Boot, Constants for Vocabulary, Nothing Ambient

`os.Getenv` appears in exactly one place: `configkit` loading at boot into a validated struct (missing/invalid
keys fail the boot, all listed at once, before any port opens). Business code receives config values as
constructor arguments — which is what makes it testable without environment gymnastics. Event names, error
codes, metric names, lane names, and permission names are typed constants (kit-exported where kit-owned) —
never inline strings, because a typo in an inline string is a silent observability hole that no compiler,
test, or dashboard will ever flag.

```go
// WRONG — ambient env read + inline event name, deep in a use case
if os.Getenv("NEWS_TOTP_FORCE") == "true" { log.Info("totp.chek.failed") } // typo ships

// RIGHT — config injected at construction; vocabulary is constants
type TOTPGuard struct{ force bool }
func NewTOTPGuard(cfg Config) *TOTPGuard { return &TOTPGuard{force: cfg.TOTPForce} }
obs.Log(ctx, obskit.EventAuthzDenied, codes.NewsTOTPRequired, ...)
```

Env-key discipline rides along: kit-read keys (`PG_*`, `RABBITMQ_URL`, `GATEWAY_PROOF_*`, `HTTP_*`) are kit
property and are never renamed or service-prefixed; service domain keys are `<SERVICE>_*`.

## P11 — Observe What You Ship: Bounded Labels, Kit Names, One Correlation Thread

Kit-owned metrics keep kit-owned names (`outbox_depth`, not `news_outbox_depth`) with the `service` label — one
renamed metric kills the single shared dashboard the kit exists to enable. Labels stay bounded: route template,
method, status class — never `user_id`, `project_id`, raw path, or error text (unbounded labels are a
time-series-database outage on a delay timer). `request_id`/`trace_id` ride every log line; `traceparent` rides
every message envelope so spans survive the broker hop; Sentry receives only panics and programming faults,
never expected domain errors. A feature without its dashboard panel, alert, and runbook entry is unfinished —
that is the platform's definition of done, not a nice-to-have. (Signal-model reasoning, SOC evidence, severity
rubric: the `alaa-observability-soc` skill.)

```go
// WRONG — unbounded label; this metric will kill the TSDB and the dashboard
httpRequests.WithLabelValues(r.URL.Path, userID).Inc()

// RIGHT — template + class; identity goes in logs/traces, never labels
httpRequests.WithLabelValues(chi.RouteContext(r.Context()).RoutePattern(), statusClass(code)).Inc()
```

The event/code vocabulary is fixed platform-wide: `http.request.completed|failed`,
`service.readiness.failed|recovered`, `auth.context.invalid`, `authz.denied`, `input.validation.failed` —
services add domain events, never rename these.
