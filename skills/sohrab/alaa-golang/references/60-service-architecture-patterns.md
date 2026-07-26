# Service Layout and the Repository Boundary

Read this before creating a package, moving a file, or adding a layer. There is one layout in this pack; the import
direction between its layers is in `62-import-direction-and-boundaries.md` and is not repeated here.

## The layout

**Rule:** on a kit service, the generated scaffold is the layout, and you fill its stubs. **Forbidden:** restructuring
a scaffolded service into a different shape, or generating a service and then renaming its directories.

Verified from the kit's `docs/RUNBOOK.md` §6 and §6A, read 2026-07-26:

```text
cmd/<service>/main.go                          config, observability, runkit.New, composition.Configure, app.Execute
internal/domain/                               aggregates, value objects, domain errors, the public-id alias
internal/application/ports.go                  the interfaces the use cases consume
internal/application/<use_case>.go             one file per use case
internal/infrastructure/                       adapters: repositories, clients, publishers
internal/infrastructure/composition/app.go     the wiring seams
internal/health/service                        service-owned readiness checks
db/migrations/                                 goose SQL, picked up by //go:embed
api/                                           generated contract artifacts
```

**Rule:** on a service that is not on the kit, keep the same three roles — domain, application, infrastructure — and
keep whatever directory names the repository already uses. Renaming existing directories to match this file is churn,
not conformance. A service with no existing names uses the names above.

## The composition seams (kit services)

**Verified fact (kit `docs/RUNBOOK.md`, `README.md`, read 2026-07-26):** `internal/infrastructure/composition/app.go`
exposes exactly four seams a service fills, and everything else — subcommands, readiness, lifecycle, graceful
shutdown — stays kit-wired:

| Seam | You put here |
|---|---|
| `NewRouter(...)` | the route families and their routes, replacing the `/__scaffold/*` stubs |
| `serviceComponents(...)` | only the consume, dispatch, and relay roles this service owns |
| `serviceTopology()` | this service's exchange and queue bindings |
| `servicePermissions()` | the catalog-generated permission map, replacing `trustkit.DenyAllPermissions{}` |

**Rule:** keep `cmd/<service>/main.go` as generated. Service assembly goes in `composition/app.go`.

**Forbidden:** leaving a role in `serviceComponents` populated that the service does not own. Empty roles stay
fail-closed; filling one to silence a wiring error opens a path nothing owns.

## Layer ownership

| Layer | Owns | Never contains |
|---|---|---|
| `cmd/<service>` | process start, config load, observability init, lifecycle handoff | business rules, SQL, routes |
| `domain` | entities, value objects, invariants, state transitions, domain errors | any I/O, any framework type, any kit adapter |
| `application` | the flow of one use case, transaction boundaries, cache decisions, idempotency decisions, the ports it consumes | SQL text, HTTP types, broker types |
| `infrastructure` | port implementations, drivers, clients, publishers, the composition root | business rules |
| `health/service` | this service's readiness checks and their severity | anything else |

## The repository boundary

**Rule:** declare the repository interface in `application/ports.go` — the package that calls it — with only the
methods that package calls. Implement it in `infrastructure`.

**Rule:** every repository method takes `ctx context.Context` first and the transaction seam second, so the same
method works inside and outside a unit of work. On the kit that seam is `pgkit.Tx` (verified `pgkit/tx.go`, read
2026-07-26), and `(*pgkit.RuntimePool).InTx` begins, commits on nil, and rolls back on error or panic.

**Rule:** a repository returns domain types and domain or persistence errors. **Forbidden:** a repository returning
`pgx.Rows`, a driver error unwrapped, or a transport DTO.

**Forbidden:** SQL text outside `infrastructure`. **Forbidden:** a repository interface mentioning `pgx`, `chi`,
`http`, or a Redis type in its signature.

**Rule:** a cache sits in front of a repository as a decorator implementing the same port, or inside the use case as
its own port. Which one, and the rules it follows, are in `61-redis-cache-layer.md`.

## The use case

**Rule:** one exported method per use case, taking a context and an input struct, returning a domain result and an
error. It owns the flow: which repositories to call, in what order, inside which transaction, and what to do when one
fails.

**Rule:** a use case must be testable with fakes for every port and no HTTP, database, Redis, or broker. If it is not,
a dependency reached it that should have been a port.

**Forbidden:** a use case publishing to the broker directly. Facts leave through the outbox in the same transaction as
the state that produced them — that contract belongs to `/alaa-golang-clean-code-principles`
(`$alaa-golang-clean-code-principles`) P6 and `/alaa-async-messaging` (`$alaa-async-messaging`).

## Constructing dependencies

**Rule:** wire with plain constructors in the composition root. Each constructor takes its dependencies as arguments
and returns a concrete type.

```go
repo := postgres.NewNewsRepository(pool)
cache := rediscache.NewNewsCache(redis)
uc   := application.NewPublishNews(pool, repo, cache, clock)
h    := httpapi.NewNewsHandler(uc)
```

**Rule:** load a DI-framework skill only when `go.mod` already requires that framework — `/golang-google-wire`
(`$golang-google-wire`), `/golang-uber-dig` (`$golang-uber-dig`), `/golang-uber-fx` (`$golang-uber-fx`),
`/golang-samber-do` (`$golang-samber-do`). **Forbidden:** introducing a DI framework into a service that does not
already require one.

## Patterns this layout composes, and who owns each

Do not derive any of these here. Load the owner.

| Pattern | Owner |
|---|---|
| Transactional outbox; state, outbox and audit in one transaction | `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) P6 · `/alaa-async-messaging` (`$alaa-async-messaging`) |
| Idempotency keys and receipts, proven by a run-twice test | `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) P7 · `/alaa-data-layer` (`$alaa-data-layer`) |
| Two Postgres lanes, transaction pooling, scale tiers | `/alaa-data-layer` (`$alaa-data-layer`) |
| Keyset pagination over a growing table | `/alaa-keyset-pagination` (`$alaa-keyset-pagination`) |
| UUIDv7 public ids and snake_case wire tags | `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) P8 |
| Job queues, worker pools, backpressure | `/golang-concurrency` (`$golang-concurrency`) · `/alaa-async-messaging` (`$alaa-async-messaging`) |
| Consumer acknowledgement points, publisher confirms, dead-lettering, reconnect | `/alaa-async-messaging` (`$alaa-async-messaging`) |
| Rate limiting, circuit breaking, load shedding | `46-chi-under-load.md`, then `/alaa-go-chi-development` (`$alaa-go-chi-development`) |
| Trusted identity, permission bitmap, step-up | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) · P3 |
| Readiness severity, response envelopes, error codes | `/alaa-services-contract` (`$alaa-services-contract`) · P2/P4 |
| Correlation across HTTP and AMQP, metric cardinality, log vocabulary | `/alaa-observability-soc` (`$alaa-observability-soc`) · P11 |
