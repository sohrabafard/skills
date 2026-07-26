# P4–P8 · Domain, Data, and Consistency

These five principles keep the service's inside honest: errors as values, dependencies behind ports, atomicity
where it matters, idempotency everywhere, and explicit wire shapes.

## P4 — Errors Are Domain Values; the Boundary Maps Them Once

Inside domain and application code, return typed `errkit` errors (code, status, meta, retryability) or wrapped
causes (`fmt.Errorf("expanding chunk %d: %w", n, err)`). Exactly one place — the HTTP boundary — maps them to
the canonical `{error:{status,code,message,meta}}` envelope. Never render JSON errors in a use case; never
log-and-swallow; never branch on error text. (Wrapping mechanics, `errors.Is`/`As`, sentinel design:
`/golang-error-handling` (`$golang-error-handling`) through the `/alaa-golang` (`$alaa-golang`) router.)

```go
// WRONG — decision by string matching; breaks on the first reworded message
if strings.Contains(err.Error(), "duplicate") { ... }

// RIGHT — sentinel/typed errors travel; boundaries decide
if errors.Is(err, grants.ErrIdempotencyConflict) {
    return errkit.Conflict("IDEMPOTENCY_CONFLICT")
}
```

Codes are UPPER_SNAKE, stable, and append-only in the service's catalog; renaming a code is a contract change
with a deprecation window, not a refactor. Code *names* are owned by `/alaa-services-contract`
(`$alaa-services-contract`) — read the name from there, do not invent one.

**Proof.** `errkit` fails closed: an error carrying a code nobody registered, an out-of-range status, an empty
message, or metadata that failed its budget is collapsed to the canonical `INTERNAL` envelope rather than
rendered (`errkit/envelope.go`). So a hand-invented code does not silently reach a client — it becomes a 500 you
will see. `contracttest` then asserts the canonical envelope on every error status as black-box HTTP conformance;
run `make contracttest` (`go test ./contracttest/...`).

**Known open contract question — do not resolve it in service code.** `errkit.Validation()` renders
`INPUT_VALIDATION_FAILED` with **400**, `errkit.SemanticValidation()` renders the same code with **422**, and the
kit's `CONTRACTS.md` canonical envelope example shows `"status": 422` for that code while its strict-JSON and
binding sections document 400. The envelope validator accepts both. Verified against kit source 2026-07-26.
Pick the constructor whose status your endpoint's documented contract states, record which you chose, and route
the contradiction itself to `/alaa-services-contract` (`$alaa-services-contract`); file the fix as a change
request through `/alaa-go-chi-development` (`$alaa-go-chi-development`). Do not standardize a service on one
answer and call the question closed.

## P5 — Ports Inward, Adapters Outward, Domain Pure

`domain ← application ← infrastructure`, enforced by import direction. Domain and application packages import
**no** pgx, amqp, chi, Redis, or provider SDK. Every side effect crosses a small interface (port) owned by the
application layer; infrastructure implements it. This is what makes use cases testable with fakes and providers
swappable as data. (Repository-pattern depth and layer discipline: `/alaa-golang` (`$alaa-golang`) references
60 and 62.)

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

Keep ports small and consumer-shaped — what the use case needs, not what the table offers. A port with fifteen
methods is a database interface wearing a costume.

**Proof — say this plainly: the gate does not exist yet.** This is the most mechanically checkable rule in the
skill and no analyzer enforces it. The kit's `linttools` ships five analyzers — `pooledlane`, `metricname`,
`structtag`, `uuiddefault`, `textnorm` — and none checks import direction; `make lint-analysis`, which runs
`cmd/alaa-lint` as a `go vet` vettool, does not include one. Verified against kit source 2026-07-26.

Two things to do about that. Run this in the service's CI now — any output is a P5 violation:

```sh
go list -deps ./internal/domain/... ./internal/application/... \
  | grep -E 'jackc/pgx|rabbitmq/amqp091|go-chi/chi|redis/go-redis|clickhouse-go'
```

And file the real gate: one timestamped change request proposing an import-direction analyzer in `linttools/`,
wired into `cmd/alaa-lint` and `make lint-analysis`, submitted through `/alaa-go-chi-development`
(`$alaa-go-chi-development`) using its change-request template. Until that lands, P5 is enforced by the grep
above and by review — treat it as unenforced, not as enforced.

## P6 — One Transaction, One Truth: Business Write + Outbox + Audit Together

**Scope: services whose system of record is PostgreSQL.** Anything that must be atomically true together goes
through the `Tx` port in one transaction: the state change, its outbox row, its audit row, its receipt.
Publishing to the broker directly from a use case is a correctness bug — lost on rollback, duplicated on retry.
Durable facts leave only via `outboxkit`'s relay.

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

Not every Ala service has Postgres. `wa-api` boots with `configkit`'s `WithoutPostgres` and `WithoutRabbitMQ`
and runs on ClickHouse through `chkit`; there is no transactional outbox on that lane. A service in that shape
states its durability story explicitly in its own design record instead of assuming this principle's machinery
exists. Do not scaffold an outbox onto a service that has no transactional store.

**Pooling-lane corollary.** The pooled runtime lane (`PG_DSN`) never runs DDL, `LISTEN`/`NOTIFY`, session `SET`
GUCs, or cross-transaction advisory locks; those belong to the direct `PG_MIGRATE_DSN` lane. `pgkit`'s distinct
pool types make crossing lanes a compile error, and the kit's `pooledlane` analyzer flags the SQL forms
(`LISTEN`, `NOTIFY`, `SET <guc>`, `pg_advisory_lock`/`pg_advisory_unlock`) in pooled-lane code — it runs under
`make lint-analysis`.

**Proof.** Write a test that asserts a rolled-back transaction leaves no published fact: run the use case
against real PostgreSQL with a failure injected *after* the outbox write, then assert (a) the aggregate row is
unchanged, (b) `SELECT count(*)` on the outbox table for that aggregate is zero, and (c) the fake or real
publisher recorded no delivery. This test only means something on real Postgres, so it belongs in the
testcontainers lane — the kit's equivalent runs under `make postgres-truth-tier`. A P6 review without this test
has checked the code shape and proven nothing.

## P7 — Idempotency Is a Contract, Not a Hope

Every re-runnable thing is idempotent *by construction* and proven by a test that runs it twice. Retries,
redeliveries, and re-runs are not error cases on this platform — they are the normal consequence of
at-least-once delivery and crash recovery. Code that is only correct when run once is incorrect.

The four kit-and-Go mechanics this skill owns:

- **Seeders** — `seedkit`'s double-run helper asserts identical end state across two runs.
- **Consumers** — a `command_receipts` row deduplicates by idempotency key; a duplicate increments a counter and
  does nothing else. `mqkit`'s ordering contract is receipt and business effect commit *first*, broker ack
  *second*.
- **Upserts** — natural-key `ON CONFLICT`, never a bare insert.
- **Provider calls** — a stable idempotency key derived from a durable id (Bale's `request_id` = the delivery's
  public id, unchanged across retries). Where a provider offers none — Mediana — only a `queued` delivery may
  dispatch, so the state row is the key.

```sql
-- WRONG — bare insert; the second run is a crash or a duplicate
INSERT INTO routing_policies (category, channel, rank, mode) VALUES (...);

-- RIGHT — natural-key upsert; the hundredth run is a no-op
INSERT INTO routing_policies (category, channel, rank, mode) VALUES (...)
ON CONFLICT (category, channel) DO UPDATE SET rank = EXCLUDED.rank, mode = EXCLUDED.mode;
```

**Retry doctrine is not this skill's.** How many attempts, what backoff curve, what timeout budget, how to
degrade, and what to do about an ambiguous timeout (the request that may or may not have landed) belong to
`/alaa-reliability-sla` (`$alaa-reliability-sla`). Read it before choosing a policy. What this skill fixes is
that whatever policy you choose must land on an idempotent target.

Kit facts that constrain that policy, verified against kit source 2026-07-26 — do not assume otherwise:
`mqkit` has no Go-level retry or backoff; a failed delivery is broker-requeued or dead-lettered with a receipt.
`jobkit` does have full-jitter exponential backoff (`jobkit.Backoff`, `jobkit.DeferBackoff`). `rediskit`
disables client retries outright (`MaxRetries = -1`), rejects a non-positive TTL with `ErrMissingTTL`, treats a
missing key as a clean miss rather than an error, uses a 250 ms `DefaultCallTimeout`, and reports `Degraded`
rather than `Required` readiness. The kit has **no ingress request deadline, no rate limiting, no circuit
breaker, no backpressure, no load shedding, and no in-flight cap** — if your design needs one, it does not
exist yet and must be filed, not assumed.

**Proof.** Run it twice and assert the same end state. For seeders that is the kit's own gate,
`make seed-idempotency` (`go test -count=1 -tags testcontainers ./seedkit/... -run TestCheckRunTwice`); mirror
it in the service. For consumers, deliver the same message twice and assert one business effect, one receipt
row, and an incremented duplicate counter. For upserts, execute the statement twice against real PostgreSQL and
assert one row with the second run's values. A P7 claim with no run-twice test is an unproven claim.

## P8 — Explicit JSON, Explicit IDs

Every wire struct carries explicit snake_case `json:"..."` tags **including nested structs**. The platform's
consumers are case-sensitive (`json_decode` in the Laravel services); an untagged nested struct serializes
capitalized and the consumer silently drops the data — the worst failure mode, because nothing errors. Public
ids are UUIDv7 minted via `idkit`, never a `gen_random_uuid()` database default (that is v4 — time-unordered,
breaking the index locality the platform chose v7 for), never `uuid.New()`.

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

Partial updates obey presence, not zero values. A PATCH wire struct distinguishes "field absent" from "field
explicitly set to its zero value" with pointer fields (`*string`, `*int64`, `*bool`) or explicit presence flags.
A zero-guard makes a legitimate empty, zero, or false value un-settable, and **an absent field must never be
treated as "clear it"**.

```go
// WRONG — zero-guard: clients can never clear the title, and absent looks like empty
if in.Title != "" { news.Title = in.Title }

// RIGHT — pointer presence: absent keeps stored state; an explicit value (even "") overwrites
if in.Title != nil { news.Title = *in.Title }
```

**Proof, both halves are real analyzers.** Tags: the kit's `structtag` analyzer flags every exported wire or
message field without an explicit snake_case JSON tag, at every nesting level; run `make lint-structtags`
(`go run ./cmd/alaa-structtag-lint .`). Ids: the kit's `uuiddefault` analyzer flags forbidden UUID defaults in
SQL migrations on the pattern `(?i)\bdefault\s+(gen_random_uuid|uuid_generate_v4)\s*\(\s*\)` and separately
flags a `public_id` minted by either function; run `make lint-no-genrandomuuid`
(`go run ./cmd/alaa-uuid-lint ./db/migrations`). Presence-versus-zero has no analyzer: prove it with a PATCH
test that sends `{"title": ""}` and asserts the stored title became empty, and a second that omits `title` and
asserts the stored title is unchanged.
