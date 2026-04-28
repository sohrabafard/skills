# Alaa Go Gap Coverage

Use this file after routing to the installed public Go skill that most closely matches the task.

This reference covers local decisions that are intentionally not owned by a single public `golang-*` skill, or where the
installed skill has only shallow trigger guidance.

## Service lifecycle

- Keep `main` small: parse config, build dependencies, wire transports/workers, start supervisors, and wait for shutdown.
- Use `signal.NotifyContext` for process cancellation and pass the derived context into servers, workers, clients, and
  background loops.
- Every goroutine needs an owner, a cancellation path, and an error-reporting path. Prefer `errgroup` for related work.
- Use explicit startup and shutdown timeouts. Do not rely on process exit to close HTTP servers, database pools, queues,
  or telemetry exporters.
- Treat health and readiness separately: health means the process is alive; readiness means it can serve useful traffic.

## Configuration and secrets

- Prefer typed config structs with validation at startup.
- Keep `os.Getenv` and flag parsing near the edge; pass typed config into packages.
- Fail fast on missing required config. Use defaults only for non-sensitive, documented local-development values.
- Never log secrets, tokens, passwords, connection strings with credentials, or trusted identity headers.
- For containerized services, prefer env-first config; use richer config libraries only when multiple sources are real.

## Trusted gateway and service contracts

- Do not trust client-supplied identity, tenant, profile, or authorization context.
- Consume trusted gateway headers only where the platform contract says the service is behind the trusted gateway.
- Keep auth parsing, tenant resolution, and authorization decisions explicit and testable.
- Preserve service-contract endpoints such as health, readiness, metrics, and version/build metadata when they exist.
- Route cross-service response shape, observability, and header semantics to `alaa-services-contract` and
  `alaa-trust-gateway-auth` when they matter.

## GraphQL production baseline

Use `golang-graphql` ( `$golang-graphql` ) for trigger-level routing, then apply these local rules until that skill has
full body guidance.

- Prefer `github.com/99designs/gqlgen` for schema-first APIs with typed generated resolver contracts.
- Keep resolvers thin. Put authorization, use cases, loaders, and repository logic outside generated resolver methods.
- Add query complexity, depth, pagination, and timeout controls before exposing GraphQL to untrusted clients.
- Use dataloaders or batched repository calls for relation-heavy fields. Treat N+1 queries as a correctness and latency
  issue, not just an optimization.
- Map GraphQL errors deliberately. Do not leak internal error strings, SQL details, secrets, or authorization reasons.
- Keep subscriptions behind explicit connection, auth, backpressure, and shutdown rules.

## Data, async, and migrations

- Prefer `pgx` plus `sqlc` for PostgreSQL services that own SQL directly.
- Make transactions explicit at use-case boundaries; avoid hidden transaction behavior inside generic helpers.
- For Redis, distinguish cache, coordination, lock, and rate-limit uses in code and tests.
- For RabbitMQ or Kafka, design idempotency keys, retry backoff, confirms/acks, DLQ behavior, and shutdown handling before
  writing consumers.
- Choose migration tooling per repo: `goose` for simple SQL sequences, Atlas when drift control and review workflows
  matter.

## Validation and release checks

- Start with `go test ./...`; add `go test -race ./...` for goroutines, channels, shared state, or caches.
- Use `golang-lint` ( `$golang-lint` ) for `golangci-lint`, `go vet`, analyzer policy, and `nolint` hygiene.
- Run `govulncheck ./...` after dependency changes and before release-sensitive work.
- Use benchmarks and profiles only after identifying a real hot path or regression.
- For delivery changes, route CI to `golang-continuous-integration` and platform rollout to the relevant Sohrab companion.

## Dependency decision fallback

When no public Go skill owns the decision:

1. Start with the standard library.
2. Check `40-production-ready-package-catalog.md`.
3. Check `30-enterprise-shortlist.md`.
4. Verify official package docs or primary project docs from `SOURCES.md`.
5. Add a dependency only when it removes real complexity, improves correctness, or matches an existing repo standard.
