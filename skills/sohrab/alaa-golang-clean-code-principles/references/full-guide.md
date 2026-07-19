# Full Guide — The Thirteen Kit-Era Principles in One File

Read this when the task is broad: a feature end to end, a package-level review, or onboarding to an Ala Go
service. For targeted tasks, the split files (`10-`, `20-`, `30-`, `40-`) are faster. This file is the
preserved whole; the split files must never contradict it.

Scope: every Go service on `alaa-go-chi` — news, notification v2, entitlement-platform after adoption, and all
future services. The one-sentence summary: *the kit writes shared things once; your service writes only its
domain; every boundary is a small interface; every identity, error, and side effect is explicit.*

---

## P1 — The Kit Writes It Once

If a concern is kit-owned — envelope, middleware chain, readiness, trusted headers, outbox, jobs, seeding,
envelope codec, UUIDv7, audience predicate — service code **calls** the kit; it never re-implements,
wraps-and-renames, or "temporarily" copies it. A hand-rolled copy is how dual behavior is born, and dual
behavior is the bug class the kit exists to kill.

```go
// WRONG — hand-rolled error response; drifts from the canonical envelope on day one
func (h *Handler) Create(w http.ResponseWriter, r *http.Request) {
    if err := h.uc.Create(r.Context(), in); err != nil {
        w.WriteHeader(422)
        json.NewEncoder(w).Encode(map[string]any{"code": "VALIDATION", "msg": err.Error()})
    }
}

// RIGHT — errkit domain error, one kit mapper renders {error:{status,code,message,meta}}
func (h *Handler) Create(w http.ResponseWriter, r *http.Request) {
    in, err := httpkit.Bind[CreateNewsRequest](r)
    if err != nil { httpkit.RespondError(w, r, err); return }
    out, err := h.uc.Create(r.Context(), in)
    if err != nil { httpkit.RespondError(w, r, err); return }
    httpkit.Respond(w, r, http.StatusCreated, out)
}
```

Corollary: if the kit's shape doesn't fit, that is a kit PR or a recorded drift — never a local fork (kit
escape-hatch rule).

## P2 — Route Posture Is Declared, Never Implied

Every route belongs to exactly one family — `Trusted`, `Anonymous`, `ProviderFacing`, `Operational` — declared
in the router builder. A route whose trust posture must be inferred from its handler body is a security review
failure, not a style issue.

```go
// WRONG — posture invisible; is this authenticated? project-scoped? nobody can tell from here
r.Post("/api/v1/news", h.Create)

// RIGHT — posture, permission, and step-up requirements read like a sentence
routes.Trusted(r, func(t chi.Router) {
    t.With(
        trustkit.RequirePermission(perm.NewsUserCanSendToHisShobe),
        trustkit.RequireTOTP("news.insert"),
    ).Post("/api/v1/news", h.Create)
})
```

## P3 — TrustCtx or Nothing: No Raw Headers Past the Edge

Identity, project, permissions, location, and TOTP metadata are parsed **once** by `trustkit` into an immutable
`TrustCtx`. Handlers, use cases, and repositories never touch `r.Header`, never re-parse `X-Access`, and never
accept identity from body or query on trusted routes (root's explicit `project_id` is authorized by the root
permission *first*). Identity types are settled: `X-Project-Id` = UUIDv7 string, `X-User-Id` = positive int64.

```go
// WRONG — re-parsing trusted headers deep in a use case; type drift and spoofing bugs live here
func (uc *CreateNews) Handle(r *http.Request) error {
    projectID, _ := strconv.Atoi(r.Header.Get("X-Project-Id")) // int?! it's a UUIDv7
    ...
}

// RIGHT — one typed context, injected; the use case never sees HTTP
func (uc *CreateNews) Handle(ctx context.Context, tc trustkit.TrustCtx, in CreateNewsInput) error {
    if !tc.Can(perm.NewsUserCanSendPublic) && in.Visibility == VisibilityPublic {
        return errkit.Denied("NEWS_AUDIENCE_SCOPE_DENIED")
    }
    ...
}
```

## P4 — Errors Are Domain Values; the Boundary Maps Them Once

Inside domain/application code, return typed `errkit` errors (code, status, meta, retryability) or wrapped
causes (`fmt.Errorf("expanding chunk %d: %w", n, err)`). Exactly one place — the HTTP boundary — maps them to
the envelope. Never render JSON errors in a use case; never log-and-swallow; never stringly-match error text.
(Mechanics: `golang-error-handling` via the alaa-golang router.)

```go
// WRONG — decision by string matching; breaks on the first reworded message
if strings.Contains(err.Error(), "duplicate") { ... }

// RIGHT — sentinel/typed errors travel; boundaries decide
if errors.Is(err, grants.ErrIdempotencyConflict) {
    return errkit.Conflict("IDEMPOTENCY_CONFLICT")
}
```

## P5 — Ports Inward, Adapters Outward, Domain Pure

`domain ← application ← infrastructure`, enforced by import direction. Domain and application packages import
**no** pgx, amqp, chi, Redis, or provider SDKs. Every side effect crosses a small interface (port) owned by the
application layer; infrastructure implements it. This is what makes use cases testable with fakes and providers
swappable as data. (Depth: `alaa-golang` references 60/62.)

```go
// WRONG — SQL in the use case; untestable without a database, unswappable forever
func (uc *PublishNews) Handle(ctx context.Context, id int64) error {
    _, err := uc.pool.Exec(ctx, `UPDATE news SET status='published' WHERE id=$1`, id)
    ...
}

// RIGHT — a port the use case owns, an adapter Postgres implements
type NewsRepo interface {
    Publish(ctx context.Context, tx pgkit.Tx, id int64) (News, error)
}
```

## P6 — One Transaction, One Truth: Business Write + Outbox + Audit Together

Anything that must be atomically true together goes through the `Tx` port in one transaction: the state change,
its outbox row, its audit row, its receipt. Publishing to the broker directly from a use case is a correctness
bug (lost on rollback, duplicated on retry) — durable facts leave only via `outboxkit`'s relay.

```go
// WRONG — publish inside the use case; a rollback after Publish() = a lie on the wire
uc.publisher.Publish(ctx, broadcastCmd)
return uc.repo.Publish(ctx, id)

// RIGHT — same transaction writes state + outbox; the relay does the wire
return uc.tx.InTx(ctx, func(tx pgkit.Tx) error {
    if _, err := uc.repo.Publish(ctx, tx, id); err != nil { return err }
    if err := uc.outbox.Write(ctx, tx, outboxkit.Row{
        Exchange: "notification.commands", RoutingKey: "news.broadcast.v1", Payload: cmd,
    }); err != nil { return err }
    return uc.audit.Write(ctx, tx, auditRow)
})
```

Corollary (kit framework §5.2): the pooled runtime lane never runs DDL, `LISTEN/NOTIFY`, session GUCs, or
cross-transaction advisory locks — those belong to the direct `PG_MIGRATE_DSN` lane, and `pgkit`'s types make
crossing a compile error.

## P7 — Idempotency Is a Contract, Not a Hope

Every re-runnable thing is idempotent *by construction* and proven by a test that runs it twice: seeders (the
`seedkit` double-run helper), consumers (`command_receipts` dedupe — duplicates increment a counter and do
nothing), receipt upserts (`ON CONFLICT`), provider retries (Bale `request_id` = delivery public_id, stable
across retries; where a provider offers no key — Mediana — only a `queued` delivery may dispatch).

```sql
-- WRONG — bare insert; the second run is a crash or a duplicate
INSERT INTO routing_policies (category, channel, rank, mode) VALUES (...);

-- RIGHT — natural-key upsert; the hundredth run is a no-op
INSERT INTO routing_policies (category, channel, rank, mode) VALUES (...)
ON CONFLICT (category, channel) DO UPDATE SET rank = EXCLUDED.rank, mode = EXCLUDED.mode;
```

## P8 — Explicit JSON, Explicit IDs

Every wire struct carries explicit snake_case `json:"..."` tags **including nested structs** (the platform's
consumers are case-sensitive; an untagged nested struct silently drops data — the lint catches it, you
shouldn't need the lint). Public ids are UUIDv7 minted via `idkit`, never `gen_random_uuid()` defaults, never
v4.

```go
// WRONG — nested struct untagged → serializes "Audience":{"OstanID":…} → consumer silently drops it
type BroadcastCmd struct {
    ProjectID string `json:"project_id"`
    Audience  struct{ OstanID *int }
}

// RIGHT — every field, every level
type Audience struct {
    OstanID *int    `json:"ostan_id"`
    UserIDs []int64 `json:"user_ids"`
}
type BroadcastCmd struct {
    ProjectID string   `json:"project_id"` // canonical public UUIDv7, same value as X-Project-Id
    Audience  Audience `json:"audience"`
}
```

Corollary — partial updates obey presence, not zero values: PATCH wire structs use pointer fields
(`*string`, `*int64`) or presence flags so "absent" (keep stored state) and "explicit zero/empty"
(overwrite) stay distinguishable; `if in.Title != ""` as an update guard is the Go twin of the
truthiness-merge bug.

## P9 — No Naked Goroutines: Every Concurrent Thing Has an Owner and an Exit

A goroutine exists only inside a worker construct that owns its lifecycle: bounded pool, `context`
cancellation, drain-on-shutdown through `runkit`'s ordered shutdown, and a name in metrics. `go func()` fired
from a handler is a leak, an un-drained buffer, and an invisible failure mode. (Depth: `golang-concurrency`,
`golang-context`, `golang-safety` via the alaa-golang router.)

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

## P10 — Config at Boot, Constants for Vocabulary, Nothing Ambient

`os.Getenv` appears in exactly one place: `configkit` loading at boot into a validated struct. Business code
receives config values as constructor arguments. Event names, error codes, metric names, lane names, and
permission names are typed constants (kit-exported where kit-owned) — never inline strings, because a typo in
an inline string is a silent observability hole.

```go
// WRONG — ambient env read + inline event name, deep in a use case
if os.Getenv("NEWS_TOTP_FORCE") == "true" { log.Info("totp.chek.failed") } // typo ships

// RIGHT — config injected at construction; vocabulary is constants
type TOTPGuard struct{ force bool }
func NewTOTPGuard(cfg Config) *TOTPGuard { return &TOTPGuard{force: cfg.TOTPForce} }
obs.Log(ctx, obskit.EventAuthzDenied, codes.NewsTOTPRequired, ...)
```

## P11 — Observe What You Ship: Bounded Labels, Kit Names, One Correlation Thread

Kit-owned metrics keep kit-owned names (`outbox_depth`, not `news_outbox_depth`); labels stay bounded (route
template, method, status class — never user_id, project_id, raw path, or error text); `request_id`/`trace_id`
ride every log line; `traceparent` rides every envelope; Sentry receives only panics and programming faults. A
feature without its dashboard, alert, and runbook entry is unfinished (the platform's definition of done).

```go
// WRONG — unbounded label; this metric will kill the TSDB and the dashboard
httpRequests.WithLabelValues(r.URL.Path, userID).Inc()

// RIGHT — template + class; identity goes in logs/traces, never labels
httpRequests.WithLabelValues(chi.RouteContext(r.Context()).RoutePattern(), statusClass(code)).Inc()
```

## P12 — Tests Prove Behavior at the Boundary You Own

Use-case tests run against fakes at ports (table-driven — where business rules are the product, the tables are
exhaustive). Infrastructure tests run against real Postgres/RabbitMQ via testcontainers (SQLite fast lane only
inside its fence). Every service runs `contracttest` in CI — that is where "no dual behavior" is *proven*, not
reviewed. Behavior changes start with a failing test. (TDD: `alaa-golang` reference 63; mechanics:
`golang-testing`, `golang-stretchr-testify`.)

```go
// RIGHT — the shape of an Ala use-case test: table + fake port + errkit assertion
func TestCreateNews_GrantRules(t *testing.T) {
    cases := []struct{ name string; perms []string; audience Audience; wantCode string }{
        {"shobe author pins own shobe", []string{perm.SendToHisShobe}, Audience{ShobeID: ptr(31)}, ""},
        {"shobe author pins foreign ostan", []string{perm.SendToHisShobe}, Audience{OstanID: ptr(12)}, "NEWS_AUDIENCE_SCOPE_DENIED"},
    }
    for _, c := range cases {
        t.Run(c.name, func(t *testing.T) { /* fake repo, TrustCtx fixture, assert errkit code */ })
    }
}
```

## P13 — Cross-Service Knowledge Travels as Contracts, Never as Reach-Ins

A service that wants another domain's data uses its API or its events — never its tables, never a copied
predicate, never a guessed payload. Shared logic that *must* be identical (the audience conjunction) lives in
the kit (`audiencekit`) so a second implementation cannot exist. Unknown external facts are marked
(`NEEDS_MEDIANA_CONFIRMATION`), never invented — an honest `[gap]` outranks a plausible guess, always.

---

## The Pre-Commit Checklist

- [ ] Nothing kit-owned re-implemented locally (P1); route postures declared (P2).
- [ ] No raw trusted headers past the edge; identity types UUIDv7-project / int64-user (P3).
- [ ] Errors are typed values mapped once at the boundary (P4).
- [ ] Imports flow inward only; side effects behind ports (P5).
- [ ] Atomic truths share one transaction; facts leave via the outbox (P6).
- [ ] Everything re-runnable proven idempotent by a run-twice test (P7).
- [ ] Every wire field tagged snake_case; every public id UUIDv7 via idkit (P8).
- [ ] Every goroutine owned, cancellable, drained (P9).
- [ ] Config injected at boot; vocabulary as constants (P10).
- [ ] Metrics bounded and kit-named; correlation threads unbroken; dashboards/alerts/runbook exist (P11).
- [ ] Failing test first; fakes at ports; contracttest green (P12).
- [ ] No reach-ins; shared logic in the kit; unknowns marked, never invented (P13).
