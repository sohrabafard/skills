# Alaa Go Gap Coverage

Use this file after routing to the closest installed public Go skill.

This reference covers local production rules that are not fully owned by one public `golang-*` skill.

## Vendor orchestrator boundary

- Use `golang-how-to` ( `$golang-how-to` ) for broad Go skill selection and overlap disambiguation.
- Use this file for Alaa-specific rules after the vendor skill set is selected.
- Do not let generic vendor guidance override trusted-gateway, repository, Redis cache, TDD, observability, security, or
  service-contract rules from this pack.
- Do not run `golang-how-to` configure mode unless the user explicitly asks to force-load Go skills in project agent
  config.

## Service lifecycle

- Keep `main` small: parse config, build dependencies, wire transports/workers, start supervisors, and wait for shutdown.
- Use `signal.NotifyContext` for process cancellation.
- Every goroutine needs an owner, cancellation path, and error-reporting path.
- Use explicit startup and shutdown timeouts.
- Treat health and readiness separately.

## Framework boundary

- Use chi for raw small/simple HTTP services.
- Use `$alaa-golang-fiber` for Fiber repos, explicit Fiber requests, and raw large/high-concurrency services.
- Keep framework types at the transport edge.
- Do not migrate frameworks casually.

## Repository pattern

- DB-backed services must use repository pattern.
- Put repository interfaces at use case boundaries.
- Put database implementations in infrastructure/repository packages.
- Pass `context.Context` to repository methods.
- Do not put SQL in handlers.
- Do not put Redis in handlers.

Read `60-service-architecture-patterns.md`.

## Redis cache layer

- Treat Redis as a cache layer unless the repo says otherwise.
- Use cache-aside by default.
- Make keys, TTLs, invalidation, stampede protection, and error policy explicit.
- Cache failures usually fall back to the database.
- Do not cache authorization decisions unless TTL and invalidation are explicitly designed.

Read `61-redis-cache-layer.md`.

## TDD and tests

- Write or update a failing test before behavior-changing code.
- Implement the smallest passing change.
- Refactor only after tests pass.
- Run focused tests, then `go test ./...`.
- Run `go test -race ./...` for cache, goroutines, workers, or shared state.

Read `63-tdd-and-testing-discipline.md`.

## Configuration and secrets

- Prefer typed config structs with startup validation.
- Keep `os.Getenv` and flag parsing near the edge.
- Fail fast on missing required config.
- Use defaults only for non-sensitive local-development values.
- Never log secrets, tokens, passwords, connection strings with credentials, or trusted identity headers.

## Trusted gateway and service contracts

- Do not trust client-supplied identity, tenant, profile, or authorization context.
- Consume trusted gateway headers only where the platform contract says the service is behind the trusted gateway.
- Keep auth parsing, tenant resolution, and authorization decisions explicit and testable.
- Preserve service-contract endpoints such as health, readiness, metrics, and version/build metadata when they exist.
- Route response shape, observability, and header semantics to `alaa-services-contract` and `alaa-trust-gateway-auth` when they matter.

## Data, async, and migrations

- Prefer `pgx` plus `sqlc` for PostgreSQL services that own SQL directly.
- Make transactions explicit at use case boundaries.
- For RabbitMQ or Kafka, design idempotency keys, retry backoff, confirms/acks, DLQ behavior, and shutdown handling before writing consumers.
- Choose migration tooling per repo: `goose` for simple SQL sequences, Atlas when drift control and review workflows matter.

## Dependency fallback

When no public Go skill owns the decision:

1. Start with the standard library.
2. Check `40-production-ready-package-catalog.md`.
3. Check `30-enterprise-shortlist.md`.
4. Verify official package docs or primary project docs from `SOURCES.md`.
5. Add a dependency only when it removes real complexity, improves correctness, or matches an existing repo standard.
