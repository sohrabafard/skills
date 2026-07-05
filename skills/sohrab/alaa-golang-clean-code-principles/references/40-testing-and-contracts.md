# P12–P13 · Testing and Cross-Service Contracts, plus the Pre-Commit Checklist

## P12 — Tests Prove Behavior at the Boundary You Own

Three tiers, each proving a different boundary, none substituting for another:

- **Use-case tests** run against fakes at ports, table-driven. Where business rules *are* the product (news's
  grant rules and visibility predicate; notification's routing and etiquette rules), the tables are exhaustive —
  every permission × audience combination, every suppression path.
- **Infrastructure tests** run against real Postgres/RabbitMQ via testcontainers. Anything with
  Postgres-specific SQL (`ON CONFLICT`, `SKIP LOCKED`, partial indexes, jsonb) is *only* tested here. The
  SQLite fast lane exists strictly inside its fence (portable-SQL query sets, build-tagged, never a CI
  substitute — kit framework §5.3).
- **`contracttest`** runs in every service's CI against the service's own router — correlation headers,
  canonical envelope on every error status, strict-JSON behavior, readiness exactness, metric-name rules. This
  is where "no dual behavior" is *proven*, not reviewed.

Behavior changes start with a failing test. (TDD cadence: `alaa-golang` reference 63; table/testify mechanics:
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

The anti-pattern to refuse: a test that mocks the thing it claims to test (mocking the repository *inside* a
repository test, mocking the envelope renderer inside a contract test). Fakes stand in for what you *don't*
own in this test; the boundary under test is always real.

## P13 — Cross-Service Knowledge Travels as Contracts, Never as Reach-Ins

A service that wants another domain's data uses its API or its events — never its tables, never a copied
predicate, never a guessed payload. Shared logic that *must* be byte-identical across services (the audience
conjunction) lives in the kit (`audiencekit`) precisely so a second implementation cannot exist. Command and
event field enumerations are exhaustive by contract, and producer/consumer lists are compared by a drift test.

Unknown external facts — a provider's batch ceiling, an account's header format, an id-to-recipient mapping —
are marked (`NEEDS_MEDIANA_CONFIRMATION`, `[gap]`, `[question]`) and carried visibly until confirmed. An honest
`[gap]` outranks a plausible guess, always: the guess ships a silent wrong behavior; the marker ships a visible
to-do. (Exact platform contracts — envelopes, headers, queues, readiness: the `alaa-services-contract` skill.)

```go
// WRONG — reaching into another service's table because "it's right there"
rows, _ := pool.Query(ctx, `SELECT mobile FROM auth.users WHERE ostan_id = $1`, ostanID)

// RIGHT — the owning contract: consume the projection command / call the owning API
//   user_projection.upsert.v2 feeds the local projection; expansion reads the local copy.
```

## The Pre-Commit Checklist

Run this before every commit/PR in an Ala Go service; it is the whole skill in twelve lines.

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
