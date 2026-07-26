# P12–P13 · Testing and Cross-Service Contracts

## P12 — Tests Prove Behavior at the Boundary You Own

Three tiers, each proving a different boundary, none substituting for another:

- **Use-case tests** run against fakes at ports, table-driven. Where business rules *are* the product (news's
  grant rules and visibility predicate; notification's routing and etiquette rules), the tables are exhaustive:
  every permission × audience combination, every suppression path.
- **Infrastructure tests** run against real PostgreSQL, RabbitMQ, Redis, or ClickHouse via testcontainers.
  Anything with store-specific SQL — `ON CONFLICT`, `FOR UPDATE SKIP LOCKED`, partial indexes, `jsonb` — is
  **only** tested here. The SQLite fast lane exists strictly inside its fence: portable-SQL query sets,
  build-tagged, never a substitute for the real-store lane in CI.
- **`contracttest`** runs in every service's CI against the service's own router, as black-box HTTP. It asserts
  the trust boundary, the canonical error envelope on every error status, readiness exactness, and the route
  inventory. This is where "no dual behavior" is *proven*, not reviewed.

Behavior changes start with a failing test.

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

**The one substitution to refuse:** never fake the boundary the test exists to prove. A `contracttest` run whose
envelope renderer, router, or trust middleware has been replaced by a stand-in proves nothing — it asserts that
the stand-in behaves like itself. Fakes stand in for what you do *not* own in this test; the boundary under test
is always the real one.

Everything else about testing is owned elsewhere and is not restated here: which layer a given behavior should
be tested at, when a fake beats a stub beats a mock, flake control, and coverage policy belong to
`/alaa-testing-strategy` (`$alaa-testing-strategy`). Table and assertion mechanics belong to `/golang-testing`
(`$golang-testing`) and `/golang-stretchr-testify` (`$golang-stretchr-testify`) through the `/alaa-golang`
(`$alaa-golang`) router; the TDD cadence is `/alaa-golang` (`$alaa-golang`) reference 63.

**Proof.** `contracttest` is P12's own gate and it is real: `make contracttest` (`go test ./contracttest/...`)
in the service, plus the trust-boundary assertions (`contracttest.AssertTrustBoundary` and the TOTP challenge
assertions) that `make totp-contract` exercises in the kit. A service whose CI does not run `contracttest`
against its own router has not satisfied P12 regardless of its unit-test count.

## P13 — Cross-Service Knowledge Travels as Contracts, Never as Reach-Ins

A service that wants another domain's data uses its API or its events — never its tables, never a copied
predicate, never a guessed payload. Shared logic that *must* be byte-identical across services (the audience
conjunction) lives in the kit (`audiencekit`) precisely so a second implementation cannot exist. Command and
event field enumerations are exhaustive by contract.

```go
// WRONG — reaching into another service's table because "it's right there"
rows, _ := pool.Query(ctx, `SELECT mobile FROM auth.users WHERE ostan_id = $1`, ostanID)

// RIGHT — the owning contract: consume the projection command / call the owning API
//   user_projection.upsert.v2 feeds the local projection; expansion reads the local copy.
```

**The `[gap]` discipline.** An external fact you have not read from an authoritative source is unknown, and an
unknown ships as a visible marker, never as a plausible value. Mark it `[gap]`, `[question]`, or
`NEEDS_<PROVIDER>_CONFIRMATION` in the code, the payload comment, and the pull-request description, and carry it
until someone confirms it. This applies to a provider's batch ceiling, an account's header format, an
id-to-recipient mapping, a queue name, a rate limit, a retry ceiling — anything you would otherwise write from
inference. A guess ships a silent wrong behavior; a marker ships a visible to-do. An honest `[gap]` outranks a
plausible guess, always. Exact platform contracts — envelopes, headers, queues, readiness — are owned by
`/alaa-services-contract` (`$alaa-services-contract`); read the fact from there before marking it unknown.

**Proof — say this plainly: the gate does not exist yet.** There is no producer/consumer message-type drift test
in the kit. Verified against kit source 2026-07-26: the nearest gates are `apicontractkit.CoverageDiff`, run by
`make api-contract` (`go test ./apicontractkit/...`), which proves the router's route inventory and the authored
OpenAPI spec agree on routes, methods, and path parameters; and `make tier2-drift`, which proves generated files
still match their generator. Neither compares what one service publishes against what another consumes.

Two things to do about that. Until the gate exists, prove the pair by hand in the producing service: a test that
marshals each command and event struct and asserts the resulting JSON key set equals a checked-in golden file,
plus the same golden file vendored into the consuming service's test — a rename then fails on both sides instead
of failing silently in production. And file the real gate: one timestamped change request proposing a
message-type registry with a drift test comparing declared producers against declared consumers, submitted
through `/alaa-go-chi-development` (`$alaa-go-chi-development`) using its change-request template.
