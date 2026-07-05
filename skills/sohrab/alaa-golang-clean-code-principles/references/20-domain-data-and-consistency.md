# P4–P8 · Domain, Data, and Consistency

These five principles keep the service's inside honest: errors as values, dependencies behind ports, atomicity
where it matters, idempotency everywhere, and explicit wire shapes.

## P4 — Errors Are Domain Values; the Boundary Maps Them Once

Inside domain/application code, return typed `errkit` errors (code, status, meta, retryability) or wrapped
causes (`fmt.Errorf("expanding chunk %d: %w", n, err)`). Exactly one place — the HTTP boundary — maps them to
the canonical `{error:{status,code,message,meta}}` envelope. Never render JSON errors in a use case; never
log-and-swallow; never stringly-match error text. (Wrapping mechanics, `errors.Is`/`As`, sentinel design: the
`golang-error-handling` skill via the `alaa-golang` router.)

```go
// WRONG — decision by string matching; breaks on the first reworded message
if strings.Contains(err.Error(), "duplicate") { ... }

// RIGHT — sentinel/typed errors travel; boundaries decide
if errors.Is(err, grants.ErrIdempotencyConflict) {
    return errkit.Conflict("IDEMPOTENCY_CONFLICT")
}
```

Codes are UPPER_SNAKE, stable, append-only in the service's catalog (`docs/errors-events-observability.md`);
renaming a code is a contract change with a deprecation window, not a refactor.

## P5 — Ports Inward, Adapters Outward, Domain Pure

`domain ← application ← infrastructure`, enforced by import direction. Domain and application packages import
**no** pgx, amqp, chi, Redis, or provider SDKs. Every side effect crosses a small interface (port) owned by the
application layer; infrastructure implements it. This is what makes use cases testable with fakes and providers
swappable as data. (Repository-pattern depth and layer discipline: `alaa-golang` references 60/62.)

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

Keep ports small and consumer-shaped (what the use case needs, not what the table offers); a port with fifteen
methods is a database interface wearing a costume.

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

Pooling-lane corollary (kit framework §5.2): the pooled runtime lane (`PG_DSN`) never runs DDL, `LISTEN/NOTIFY`,
session GUCs, or cross-transaction advisory locks — those belong to the direct `PG_MIGRATE_DSN` lane, and
`pgkit`'s distinct pool types make crossing lanes a compile error, not a code-review catch.

## P7 — Idempotency Is a Contract, Not a Hope

Every re-runnable thing is idempotent *by construction* and proven by a test that runs it twice: seeders (the
`seedkit` double-run helper asserts identical end state), consumers (`command_receipts` dedupe — duplicates
increment a counter and do nothing), receipt upserts (`ON CONFLICT`), provider retries (Bale `request_id` =
delivery public_id, stable across retries; where a provider offers no idempotency key — Mediana — only a
`queued` delivery may dispatch, and ambiguous timeouts follow the per-message-class retry policy).

```sql
-- WRONG — bare insert; the second run is a crash or a duplicate
INSERT INTO routing_policies (category, channel, rank, mode) VALUES (...);

-- RIGHT — natural-key upsert; the hundredth run is a no-op
INSERT INTO routing_policies (category, channel, rank, mode) VALUES (...)
ON CONFLICT (category, channel) DO UPDATE SET rank = EXCLUDED.rank, mode = EXCLUDED.mode;
```

The reasoning to internalize: retries, redeliveries, and re-runs are not error cases in this platform — they are
the *normal* consequence of at-least-once delivery and crash recovery. Code that is only correct when run once
is incorrect.

## P8 — Explicit JSON, Explicit IDs

Every wire struct carries explicit snake_case `json:"..."` tags **including nested structs**. The platform's
consumers are case-sensitive (`json_decode` in the Laravel services); an untagged nested struct serializes
capitalized and the consumer silently drops the data — the worst failure mode, because nothing errors. The CI
lint catches it; you should not need the lint. Public ids are UUIDv7 minted via `idkit`, never
`gen_random_uuid()` database defaults (that is v4 — time-unordered, breaking the index-locality the platform
chose v7 for), never `uuid.New()`.

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
