# Topic Map — the Router

Every row is a situation you can observe before you act. Find the rows that match what you are **about to do**, open
only those, and act. When several rows match, open all of them. Trigger forms are given for both runtimes: Claude Code
`/name`, Codex `$name`.

If no row matches, open `05-what-this-skill-does-not-own.md`: it routes the topic to its owner, or — when nothing
owns it — gives the test that decides whether this skill fills the gap itself.

## Deciding the shape of a service

| You are about to… | Read / load |
|---|---|
| start a new Ala Go service, or answer "chi or Fiber?" | `30-http-api-framework-choice.md` |
| edit a repository whose `go.mod` requires `github.com/gofiber/fiber/v2` or `/v3` | `/alaa-golang-fiber` (`$alaa-golang-fiber`) |
| create a package, move a file, or add a layer to a Go service | `60-service-architecture-patterns.md` |
| add an import to a package under `internal/domain` or `internal/application` | `62-import-direction-and-boundaries.md` |
| build a whole service or feature end to end and you do not yet know which parts apply | read in order: `60-service-architecture-patterns.md`, `31-chi-api-guide.md`, `45-failure-behavior-at-the-call-site.md`, `63-tdd-and-testing-discipline.md` |
| decide how a system splits into services, queues, or bounded contexts | `/alaa-system-design` (`$alaa-system-design`) |

## Writing HTTP

| You are about to… | Read / load |
|---|---|
| register a chi route, write a handler, or construct `http.Server` | `31-chi-api-guide.md` |
| decode a request body, bind query or path parameters, or validate a DTO | `31-chi-api-guide.md` |
| set `ReadTimeout`, `WriteTimeout`, `IdleTimeout`, or a body size limit | `45-failure-behavior-at-the-call-site.md` |
| answer "will chi hold this traffic?", or add rate limiting, an in-flight cap, load shedding, or a circuit breaker | `46-chi-under-load.md` |
| write or change an OpenAPI/Swagger annotation | `/golang-swagger` (`$golang-swagger`) |
| build or change a gRPC service | `/golang-grpc` (`$golang-grpc`) |
| build or change a GraphQL schema or resolver | `/golang-graphql` (`$golang-graphql`) |
| consume a trusted-gateway header, a permission bitmap, or a tenant identity | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |

## Failure, load, and time

| You are about to… | Read / load |
|---|---|
| set a timeout on a pgx, amqp, Redis, or outbound HTTP call | `45-failure-behavior-at-the-call-site.md` |
| pass a `context.Context` into a dependency, or handle its expiry inside a handler | `45-failure-behavior-at-the-call-site.md` |
| write or change shutdown, drain, or signal handling | `45-failure-behavior-at-the-call-site.md` |
| choose a retry count, a backoff curve, a circuit-breaker threshold, a degradation mode, or an SLO window | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| discover the kit lacks a capability your service needs (admission control, ingress deadline, a new env key) | `46-chi-under-load.md`, then `/alaa-go-chi-development` (`$alaa-go-chi-development`) |

## Data, cache, and messaging

| You are about to… | Read / load |
|---|---|
| add a repository, a query, or a transaction boundary | `60-service-architecture-patterns.md`, then `/golang-database` (`$golang-database`) |
| read from or write to Redis | `61-redis-cache-layer.md` |
| change a schema, a migration, a pooling lane, or tenant-scoped access | `/alaa-data-layer` (`$alaa-data-layer`) |
| choose or configure an S3 or MinIO client library | `/alaa-minio-object-storage` (`$alaa-minio-object-storage`) |
| paginate a list endpoint or a query over a growing table | `/alaa-keyset-pagination` (`$alaa-keyset-pagination`) |
| write a queue consumer, a publisher, an outbox relay, or DLQ handling | `/alaa-async-messaging` (`$alaa-async-messaging`) |
| write a path whose cost grows with rows, tenants, retained history, or fan-out per event; or find a database, HTTP, cache, or permission call inside a loop | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) |

## Changing existing code

| You are about to… | Read / load |
|---|---|
| find a definition, caller, package surface, implementation, or diagnostic | `/alaa-code-intelligence-routing` (`$alaa-code-intelligence-routing`): Serena for the known Go symbol; direct `/golang-gopls` (`$golang-gopls`) only for one recorded unavailable, unhealthy, or missing-operation fallback |
| rename, move, extract, or inline across more than one file | `/golang-refactoring` (`$golang-refactoring`) for the process, `/alaa-code-intelligence-routing` (`$alaa-code-intelligence-routing`) for the semantic actuator, plus the skill that defines the target shape |
| change behaviour of any kind | `63-tdd-and-testing-discipline.md` |
| debug a panic, a deadlock, a leak, or output nobody can explain | `/golang-troubleshooting` (`$golang-troubleshooting`) |
| investigate slowness | `/golang-observability` (`$golang-observability`) first, then `/golang-benchmark` (`$golang-benchmark`), then `/golang-performance` (`$golang-performance`) |
| pick between two Go skills that both look right, or work a task that spans several Go concerns | `11-orchestration-and-overlap-guide.md` |

## Language, tooling, and dependencies

| You are about to… | Read / load |
|---|---|
| use a language or standard-library feature you have not confirmed the repo's `go` directive supports | `70-modern-go-baseline.md` |
| raise a `go` directive, or run a modernization pass over existing code | `70-modern-go-baseline.md`, then `/golang-modernize` (`$golang-modernize`) |
| add, upgrade, pin, or remove a dependency | `40-production-ready-package-catalog.md`, then `/golang-dependency-management` (`$golang-dependency-management`) |
| look up a published package's versions, symbols, importers, licence, or CVEs | `/golang-pkg-go-dev` (`$golang-pkg-go-dev`) |
| load a vendor `golang-*` skill, or find out whether one exists for your topic | `10-installed-golang-skills.md` |
| configure `golangci-lint`, add an analyzer, or write a `//nolint` | `/golang-lint` (`$golang-lint`) |
| build or change a CLI | `/golang-cli` (`$golang-cli`) |

## Platform, delivery, and governance

| You are about to… | Read / load |
|---|---|
| write or review Go in a repository whose `go.mod` requires `git.alaatv.com/vk/alaa-go-chi` | `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`), after the phase gate in `SKILL.md` |
| change a kit surface, file a kit change request, or check the active scope phase | `/alaa-go-chi-development` (`$alaa-go-chi-development`) |
| write a metric name, an env key, an error code, an event name, a status code, a timeout value, or a window | `/alaa-services-contract` (`$alaa-services-contract`) |
| add a log field, a metric, a span, a dashboard, or an alert | `/alaa-observability-soc` (`$alaa-observability-soc`) |
| change authentication, authorization, tenant isolation, secret handling, or crypto | `/alaa-security-review` (`$alaa-security-review`) with `/golang-security` (`$golang-security`) |
| add or rename a permission name or bitmap id | `/alaa-permission-generator` (`$alaa-permission-generator`) |
| decide what "done" or "production ready" means for this change | `/alaa-project-constitution` (`$alaa-project-constitution`) |
| decide what kinds of tests a change needs, or design a test strategy for a service | `/alaa-testing-strategy` (`$alaa-testing-strategy`) |
| reach a platform, delivery, CI, container, Kubernetes, docs, or workflow companion | `20-sohrab-companions.md` |
| brief a subagent, or answer any question about model, effort, thinking budget, or runtime capability | `/alaa-prompting-guide` (`$alaa-prompting-guide`) |

## Facts and freshness

| You are about to… | Read / load |
|---|---|
| state a version number, a release behaviour, or any claim that could have changed since this skill was written | `SOURCES.md`, and verify against the primary source it names |
| answer "does this skill own that?", or decide a Go question you have found no vendor skill and no owner for | `05-what-this-skill-does-not-own.md` — apply its gap test, then report the decision |
| add, change, or remove a reference file inside this skill | `05-what-this-skill-does-not-own.md`, section "Maintaining this skill's own files" |

## Reading policy

Open the rows that match and stop. Do not open a reference because it sounds related; every rule in this skill lives
in exactly one file, so a rule you cannot find here is a rule this skill does not have.
