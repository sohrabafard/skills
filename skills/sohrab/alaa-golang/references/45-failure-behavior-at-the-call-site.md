# Failure Behaviour at the Call Site

The Go mechanics of time and failure inside one process: how a deadline reaches a dependency call, how a server is
bounded, how a body is read, how cancellation is told apart from expiry, and how a drain finishes.

Two things are deliberately absent from this file and must stay absent:

- **Doctrine** — whether to retry, how many times, with what backoff, when to break a circuit, when to degrade. Load
  `/alaa-reliability-sla` (`$alaa-reliability-sla`).
- **Values** — the deadline for a route class, the timeout for a dependency, the error code returned when the budget
  is spent, the header that carries a deadline. Load `/alaa-services-contract` (`$alaa-services-contract`).

This file states neither. It states only what the Go code must look like once the doctrine and the values are known.

## 1. The request budget

**Verified fact, read from `alaa-go-chi` source on 2026-07-26: the kit has no ingress deadline.** `httpkit` bounds how
long the server will spend reading, writing, and idling a connection, but it computes no request-scoped budget and
puts no deadline into the request context. A handler's `r.Context()` is cancelled when the client disconnects or the
server's own write bound trips — not at a budget the service chose.

A change request exists — `docs/change-requests/2026-07-25-ingress-deadline-helper.md` in the kit repository, status
`proposed`, blocked on the gateway publishing the deadline header's name, unit, and format. **Do not invent that
header name, and do not implement a kit-shaped helper inside a service.**

**Rule:** a service on the kit that makes any outbound call establishes its own request budget in service code: at the
start of the handler, derive one `context.WithTimeout` from `r.Context()`, and pass that derived context — never
`r.Context()` directly, never a fresh one — to every dependency call the request makes. Take the budget value from
`/alaa-services-contract` (`$alaa-services-contract`); take nothing about it from this file. When the kit ships the helper, delete the local
version and adopt the kit's (P1: the kit writes it once).

**Forbidden:** `context.Background()` or `context.TODO()` anywhere on a request path. **Rule:** every context on a
request path descends from `r.Context()`, with the one exception in section 8, which names its own condition.

## 2. Every dependency call takes the request's context

**Rule:** pass the request-scoped context as the first argument to every call that leaves the process or blocks:

- `pgxpool.Pool.Query`, `QueryRow`, `Exec`, `Begin`, and every `pgx.Tx` method.
- Every `redis.Client` call (the kit's `rediskit` already applies its own per-call bound; see section 3).
- Every `amqp091` publish and every consumer handler's downstream work.
- Every outbound HTTP call, via `http.NewRequestWithContext`. **Forbidden:** `http.Get`, `http.Post`,
  `client.Get`, `client.Post`, and `http.NewRequest` on a request path — none of them carries a context.

**Rule:** a function that performs or transitively causes any of the above takes `ctx context.Context` as its first
parameter. A function that stores a context in a struct field is wrong; pass it as an argument.

## 3. Clamping a per-attempt timeout

An attempt's own timeout and the remaining request budget are two different limits, and the smaller one governs.

**Rule:** before each attempt, compute the remaining budget from the deadline and clamp:

```go
// perAttempt is this dependency's own default, from alaa-services-contract.
func attemptCtx(ctx context.Context, perAttempt time.Duration) (context.Context, context.CancelFunc, error) {
    deadline, ok := ctx.Deadline()
    if !ok {
        // No request budget is set, so the attempt's own bound governs.
        c, cancel := context.WithTimeout(ctx, perAttempt)
        return c, cancel, nil
    }
    remaining := time.Until(deadline)
    if remaining <= 0 {
        return nil, nil, errBudgetSpent // mapped at the boundary; the code comes from alaa-services-contract
    }
    c, cancel := context.WithTimeout(ctx, min(perAttempt, remaining))
    return c, cancel, nil
}
```

**Rule:** when the remaining budget is smaller than the next attempt's own timeout, do not start the attempt. Return
the boundary error instead. Starting a call you know cannot finish burns a connection and a dependency slot for
nothing.

**Verified fact (`rediskit/config.go`, `rediskit/cache.go`, read 2026-07-26):** the kit's Redis client applies a
250 ms per-call timeout of its own and sets `MaxRetries = -1`, which disables the client library's internal retries.
A Redis call therefore fails fast and fails once. Do not add a retry loop around it in service code; see
`61-redis-cache-layer.md` for what a service does with that failure.

## 4. The complete server bound set

A partially-bounded `http.Server` has an unbounded path. All four bounds are set together or none of them means
anything.

**Verified fact (`httpkit/config.go`, read 2026-07-26):** a service on the kit gets this from `httpkit` already, from
validated environment with clamps enforced at boot. The shape below is what the kit constructs, and it is what a
non-kit chi service must construct for itself:

```go
srv := &http.Server{
    Addr:              cfg.Addr,
    Handler:           handler,
    ReadTimeout:       cfg.ReadTimeout,  // HTTP_READ_TIMEOUT
    ReadHeaderTimeout: cfg.ReadTimeout,  // the kit sets this equal to ReadTimeout; it is not separately configurable
    WriteTimeout:      cfg.WriteTimeout, // HTTP_WRITE_TIMEOUT
    IdleTimeout:       cfg.IdleTimeout,  // HTTP_IDLE_TIMEOUT
    // MaxHeaderBytes is deliberately left unset: net/http already applies its own 1 MiB default.
}
```

Environment keys the kit reads, with the default and the accepted range it clamps to at boot — read from
`httpkit/config.go` on 2026-07-26, and re-read from that file before relying on any of them:

| Key | Default | Accepted range |
|---|---|---|
| `HTTP_READ_TIMEOUT` | `10s` | `1s` – `300s` |
| `HTTP_WRITE_TIMEOUT` | `30s` | `1s` – `900s` |
| `HTTP_IDLE_TIMEOUT` | `120s` | `1s` – `1800s` |
| `HTTP_MAX_BODY_BYTES` | 1 MiB | 1 KiB – 64 MiB |

**Forbidden:** writing a duration literal into an `http.Server` field, a middleware, or a client on a kit service.
**Rule:** read the bound from configuration; on the kit, that is `httpkit`'s config, not a constant in your package.

**Forbidden:** claiming that a per-route body-cap override, a 100 MiB ceiling, `SHUTDOWN_TIMEOUT`,
`SHUTDOWN_GRACE_HINT`, or any `JOB_*`, `OUTBOX_*`, or `PG_ROLLBACK_TIMEOUT` key exists. As of 2026-07-26 each of these
is ratified in the kit's decision register and **not implemented in source**. **Rule:** before naming any kit
environment key in code, a comment, a document, or an answer, find it in kit source; ratification is not
implementation.

## 5. Reading a request body

Four checks are needed on every JSON decode: a bounded number of bytes, a rejected unknown field, a required content
type, and a rejected second document in the same body. Which of them you write depends on the mode.

**Kit mode — verified fact (`httpkit/bind.go`, `httpkit/middleware.go`, read 2026-07-26):** the kit performs all four.
The middleware chain caps the body at `HTTP_MAX_BODY_BYTES`, and `httpkit.Bind[T](r)` requires the JSON content type,
wraps the body in `http.MaxBytesReader` at the configured cap, calls `DisallowUnknownFields`, rejects a trailing
second document, and returns an `errkit` error that the single envelope mapper renders.

**Rule:** in a kit service, decode with `httpkit.Bind[T](r)` and return its error unchanged to the kit's responder.

```go
req, err := httpkit.Bind[createNewsRequest](r)
if err != nil {
    httpkit.RespondError(w, r, err)
    return
}
```

**Forbidden:** constructing a `json.Decoder` on `r.Body` in a kit service. It re-implements a kit surface (P1) and
loses at least one of the four checks every time.

**Rule:** `httpkit.BindWith[T](r, httpkit.AllowUnknownFields())` is the only sanctioned way to accept undeclared
fields. Use it only on a ProviderFacing route whose payload shape is defined by an external provider rather than by
Ala. It keeps the body cap. **Forbidden:** using it on a Trusted, Anonymous, or Operational route.

**Standalone mode. Rule:** write the four checks yourself; nothing else supplies them:

```go
func (h *Handler) Create(w http.ResponseWriter, r *http.Request) {
    if ct := r.Header.Get("Content-Type"); !strings.HasPrefix(ct, "application/json") {
        writeError(w, r, errUnsupportedMediaType)
        return
    }
    r.Body = http.MaxBytesReader(w, r.Body, maxCreateBodyBytes) // from config, not a literal

    dec := json.NewDecoder(r.Body)
    dec.DisallowUnknownFields()

    var req createRequest
    if err := dec.Decode(&req); err != nil {
        // A too-large body surfaces as *http.MaxBytesError; an undeclared field surfaces as a decode error.
        writeError(w, r, mapDecodeError(err))
        return
    }
    if dec.More() { // a second JSON document in the same body
        writeError(w, r, errBadRequest)
        return
    }
    // ...
}
```

**Forbidden:** `json.NewDecoder(r.Body).Decode(&req)` as a single expression in any mode. It has none of the four
checks and cannot be given them afterwards.

**Forbidden:** returning the decoder's error text to the client in any mode. **Rule:** log the original with the
correlation id and return the mapped code; the codes belong to `/alaa-services-contract`
(`$alaa-services-contract`).

## 6. When a dependency's context expires

A handler must be able to say which of three things happened, because each has a different correct response.

**Rule:** classify with `errors.Is` against `context.DeadlineExceeded` and `context.Canceled`, and read the reason
with `context.Cause`:

| What happened | How you detect it | What the handler does |
|---|---|---|
| The client went away | `errors.Is(err, context.Canceled)` and `r.Context().Err() != nil` | Stop work. Write nothing — no one is reading. Do not log it as a service error. |
| The request budget was spent | `errors.Is(err, context.DeadlineExceeded)` and `context.Cause(ctx)` is your budget's cause | Stop work. Return the boundary's dependency-unavailable response; the code comes from `/alaa-services-contract` (`$alaa-services-contract`). |
| The dependency itself timed out inside its own attempt bound | `errors.Is(err, context.DeadlineExceeded)` and the request budget still has time left | Apply the doctrine from `/alaa-reliability-sla` (`$alaa-reliability-sla`) — retry, degrade, or fail — and return its outcome. |

**Rule:** attach a cause when you create the budget, so the second and third rows are distinguishable at all:
`ctx, cancel := context.WithTimeoutCause(r.Context(), budget, errRequestBudgetSpent)`.

**Forbidden:** treating a cancelled request as a failed request in metrics or alerts. A client hanging up is not the
service failing, and counting it as one makes every alert on that signal untrustworthy.

**Forbidden:** writing a partial response and then abandoning it on context expiry. **Rule:** complete the work into a
buffer or a value first and write the response in one call, so an expiry either produces the whole response or the
error response, never half of each.

## 7. Shutdown: telling a signal from a deadline

Both a shutdown signal and an expired deadline cancel a context, and `ctx.Err()` says `context.Canceled` for one and
`context.DeadlineExceeded` for the other — which is not enough to know *which* signal, or *whose* deadline.

**Rule:** create the process context with `signal.NotifyContext`, which cancels with a cause, and read the cause when
you log or branch:

```go
ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
defer stop()

<-ctx.Done()
log.InfoContext(ctx, "shutdown started", slog.String("cause", context.Cause(ctx).Error()))
```

`context.Cause` names the signal, so an orchestrated `SIGTERM` rollout and an operator's `SIGINT` are distinguishable
in the logs of the same service. **Rule:** log the cause at the start of shutdown; without it a shutdown that took too
long cannot be attributed afterwards.

**Verified fact (`runkit/lifecycle.go`, read 2026-07-26):** on the kit, shutdown is owned by `runkit` and runs four
ordered phases — `stop_intake`, `drain_workers`, `flush_buffers`, `close_pools` — each receiving one quarter of a
total budget hardcoded at 30 seconds. **Forbidden:** a service on the kit implementing its own shutdown sequencing,
signal handling, or drain ordering; register your component with `runkit` instead. **Rule:** if 30 seconds is wrong
for your service, that is a kit-owned value — file a change request through `/alaa-go-chi-development`
(`$alaa-go-chi-development`).

## 8. The final drain

Work that must finish *because* shutdown started cannot use a context that shutdown cancelled — flushing a metrics
buffer, writing a last audit row, acknowledging a message already committed.

**Rule:** for that work only, derive with `context.WithoutCancel` from the cancelled context, then immediately bound it
with its own timeout:

```go
drainCtx, cancel := context.WithTimeout(context.WithoutCancel(ctx), flushBudget)
defer cancel()
if err := buffer.Flush(drainCtx); err != nil { /* log; do not block exit */ }
```

`WithoutCancel` keeps the context's values — correlation id, trace id, logger — while dropping the cancellation, so
the drain's work stays correlated with the request or run that produced it.

**Forbidden:** `context.WithoutCancel` anywhere except a drain that shutdown itself triggered. Everywhere else it
removes the only mechanism that stops the work, and the result is a goroutine that outlives its owner.

**Forbidden:** `context.WithoutCancel` without a following `WithTimeout`. An uncancellable, unbounded context is how a
graceful shutdown becomes a hung process and then a `SIGKILL`.

## 9. What to check before you call this done

- Every dependency call on the path reached takes a context descended from `r.Context()`.
- Every per-attempt timeout is the smaller of its own default and the remaining budget.
- The `http.Server` has all four bounds, sourced from configuration.
- Every decode goes through `httpkit.Bind` (kit) or carries all four checks in section 5 (standalone).
- Client-cancelled and budget-expired are distinguishable at the boundary and are reported differently.
- Shutdown logs its cause; any drain uses `WithoutCancel` plus a timeout, and nothing else does.
