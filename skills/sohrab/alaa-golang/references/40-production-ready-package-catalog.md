# Package Catalog for This Stack

Read this before adding, replacing, or upgrading a dependency. It names what to reach for in this stack: HTTP APIs
behind a trusted gateway, PostgreSQL, Redis, ClickHouse and RabbitMQ, deployed to Kubernetes or OpenShift.

**Rule:** work this ladder in order and stop at the first step that answers the question:

1. The standard library.
2. A package the kit already provides — check `/alaa-go-chi-development` (`$alaa-go-chi-development`)
   `references/12-kit-capability-map.md` before adding anything that touches transport, storage, messaging,
   observability, or identity.
3. A package already in the repository's `go.mod`.
4. The **default** entry for that role below.
5. A **conditional** entry below, when its stated condition holds.
6. `/golang-popular-libraries` (`$golang-popular-libraries`) for discovery, then `/golang-pkg-go-dev`
   (`$golang-pkg-go-dev`) to check the candidate's versions, licence, importers, and CVEs before proposing it.

**Rule:** apply the change with `/golang-dependency-management` (`$golang-dependency-management`) and run
`govulncheck ./...` afterwards.

**Forbidden:** adding a dependency without saying, in the same message, which complexity it removes and what the
standard library would have cost instead.

## HTTP

`github.com/go-chi/chi/v5` — **default**, supplied by the kit. Which framework a service uses is decided by
`30-http-api-framework-choice.md`, not here; this file adds no framework criterion.

`github.com/go-chi/cors` — **conditional**, when a standalone chi service needs CORS. Mount it top-level
(`31-chi-api-guide.md`).

`github.com/go-chi/httprate`, `golang.org/x/time/rate` — **conditional, and not on the kit.** Admission control is a
kit-owned surface: see `46-chi-under-load.md` before reaching for either. Off the kit, `x/time/rate` is the in-process
token bucket and `httprate` the HTTP-level limiter, and the policy they enforce comes from `/alaa-reliability-sla`
(`$alaa-reliability-sla`).

## Config and logging

`log/slog` — **default**. **Forbidden:** adding a third-party logger to a new service.

`github.com/samber/slog-*` — **conditional**, only as a temporary bridge while migrating a repository off Zap,
Logrus, or Zerolog. On the kit, config loading is `configkit`'s and logging is `obskit`'s; neither is a service
decision.

`github.com/caarlos0/env/v11` — **conditional** for a standalone service whose config is entirely environment.
`github.com/knadh/koanf/v2` — **conditional** when config must come from several sources at once.

## Validation

`github.com/go-playground/validator/v10` — **default** for validating a transport struct after decoding.

`buf.build/go/protovalidate` — **default** when the contract is protobuf-first; the rules belong in the `.proto`.
**Forbidden:** duplicating protobuf validation in hand-written Go.

## Outbound HTTP

`net/http` with an explicitly configured `http.Client` and a shared `Transport` — **default**. Timeouts and deadline
propagation are in `45-failure-behavior-at-the-call-site.md`.

`resty.dev/v3` — **conditional**, when a service makes many structured calls to one API and request building has
become the bulk of the code.

`github.com/sony/gobreaker/v2` — **conditional, and not on the kit.** A breaker is a kit-owned surface
(`46-chi-under-load.md`); off the kit, this is the implementation, and whether a breaker is warranted and with which
thresholds belongs to `/alaa-reliability-sla` (`$alaa-reliability-sla`).

## PostgreSQL

`github.com/jackc/pgx/v5` — **default** driver and pool, and what the kit's `pgkit` wraps.

`github.com/sqlc-dev/sqlc` — **default** when the service writes its own SQL and wants generated typed accessors.

`github.com/pressly/goose/v3` — **default** migration runner, and what the kit's migrate lane uses.

`atlas` — **conditional**, when schema drift detection and migration review are governance requirements rather than
build steps. That choice belongs to `/alaa-data-layer` (`$alaa-data-layer`).

**Forbidden:** an ORM in a PostgreSQL service in this stack. **Rule:** use `pgx` with `sqlc`, or `pgx` with explicit
repository code.

## Redis

`github.com/redis/go-redis/v9` — **default**, and what the kit's `rediskit` wraps. Every rule about how it is used is
in `61-redis-cache-layer.md`.

## ClickHouse

`github.com/ClickHouse/clickhouse-go/v2` — **default**.

`github.com/ClickHouse/ch-go` — **conditional**, on an ingest path where a profile has already shown the higher-level
client to be the bottleneck. **Forbidden:** choosing it without that profile.

## Messaging

`github.com/rabbitmq/amqp091-go` — **default**, and what the kit's `mqkit` wraps.

`github.com/twmb/franz-go` — **not on this fleet.** RabbitMQ is the only broker this platform runs: the exchange
and queue registry holds no Kafka topic, the service kit ships no Kafka package, no `KAFKA_*` environment key exists,
and the registered async metric family is entirely `alaa_queue_*` and `alaa_outbox_*`. Adopting Kafka is an owner
decision, recorded as a kit change request through `/alaa-go-chi-development` (`$alaa-go-chi-development`) before any
service imports a client. Whether a message needs a broker at all and which transport carries it belong to
`/alaa-async-messaging` (`$alaa-async-messaging`). Use this client and no other on the day a service is told to speak
Kafka, because a second Kafka client in the fleet doubles the tuning surface for one transport.

`github.com/ThreeDotsLabs/watermill` — **conditional**, only where a team has decided to adopt its eventing
abstraction across services. **Forbidden:** adding it for a single consumer.

## gRPC and protobuf

`google.golang.org/grpc` — **default** for a gRPC service.

`connectrpc.com/connect` — **conditional**, when one schema must serve Go backends, browsers, and gRPC-Web clients
without a hand-written bridge.

`buf` — **default** for protobuf lint, breaking-change detection, and generation. **Forbidden:** raw `protoc`
command lines in a repository that has more than one `.proto`.

`github.com/grpc-ecosystem/go-grpc-middleware/v2` — **conditional**, when interceptor composition has outgrown
hand-written interceptors.

`go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc` — **default** for gRPC tracing.

## GraphQL

`github.com/99designs/gqlgen` — **default**, schema-first with generated resolver contracts.

`github.com/graph-gophers/graphql-go` — **conditional**, only when the repository already standardizes on it.

## Observability

`go.opentelemetry.io/otel` and the Go SDK — **default** for traces and context propagation.
`go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp` — **default** for HTTP instrumentation.
`github.com/prometheus/client_golang/prometheus` and `.../promhttp` — **default** for metrics and their endpoint.

On the kit, all four are wired by `obskit` and the fixed middleware chain. **Forbidden:** instrumenting HTTP again in
a kit service.

## Identity and security

`github.com/coreos/go-oidc/v3/oidc` — **conditional**, only in a service that itself verifies OIDC tokens.

`github.com/golang-jwt/jwt/v5` — **conditional**, only in a service that owns an authentication boundary.
**Forbidden:** adding JWT verification to a service that sits behind the trusted gateway; see
`/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`).

`github.com/MicahParks/keyfunc/v3` — **conditional**, when a service that already verifies JWTs must fetch keys from
a JWKS endpoint.

## Testing

`testing` and `net/http/httptest` — **default**.

`github.com/stretchr/testify` — **conditional**, when the repository already uses it.

`github.com/testcontainers/testcontainers-go` — **default** for a test that needs a real Postgres, Redis,
ClickHouse, or RabbitMQ.

`github.com/DATA-DOG/go-sqlmock` — **conditional**, for asserting the exact SQL a repository emits. **Forbidden:**
using it to prove a query returns correct results — that needs a real database.

## Repository tools

`gopls` — **default** language server; reached through `/golang-gopls` (`$golang-gopls`).
`golangci-lint` — **default** lint runner. **Rule:** pin its version in CI.
`govulncheck` — **default** vulnerability gate.
`buf` — **default** in any protobuf repository.

## CLI and scheduling

`github.com/spf13/cobra` — **conditional**, for a tool with a command tree. **Forbidden:** adding it for a service's
one or two subcommands; on the kit those are already generated.

`github.com/robfig/cron/v3` — **conditional**, for in-process scheduling when an external scheduler is not available.
**Rule:** state the job's owner, its overlap policy, and its shutdown behaviour in the same change.

## Dependency injection

Plain constructors — **default** (`60-service-architecture-patterns.md`).

`github.com/samber/do/v2` — **conditional**, only when `go.mod` already requires it.

`github.com/google/wire` — **not for new work.** The repository was archived in 2025. **Rule:** on an existing Wire
service, keep it and load `/golang-google-wire` (`$golang-google-wire`).

## Utilities

`github.com/google/uuid` — **conditional** for a standalone service. **Forbidden:** using it to mint a public
identifier on a kit service; UUIDv7 public ids come from the kit's `idkit`
(`/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) P8).

## Beyond the default stack

Reach here only when the standard library, the kit, a `golang-*` skill, and every entry above leave the decision open.

- `k8s.io/client-go` — when the service itself must read or mutate Kubernetes resources.
- `sigs.k8s.io/controller-runtime` — when the service is a controller or operator. **Forbidden:** a hand-written
  reconcile loop in a service that is part of the cluster control plane.
- `ko` — build tool, when fast single-binary container builds matter more than a hand-written Dockerfile. The
  production image decision belongs to `/alaa-docker-production` (`$alaa-docker-production`).
- `goreleaser` — release tool, for multi-platform binaries, archives, checksums, and publishing.

**Rule:** `buf`, `ko`, and `goreleaser` are tools, not runtime dependencies. Pin them in tool directives or install
steps. **Forbidden:** importing any of them from production code.

## Not in this stack

**Forbidden** in a new Ala Go service, each with its replacement:

| Instead of | Use |
|---|---|
| an ORM for PostgreSQL | `pgx` with `sqlc` or explicit repository code |
| a third HTTP framework | the framework `30-http-api-framework-choice.md` selects |
| a runtime DI container | constructors in the composition root |
| a low-level data client chosen up front | the official higher-level client, until a profile says otherwise |
| a helper library that wraps context, timeouts, or error handling | the standard library call, written out |
