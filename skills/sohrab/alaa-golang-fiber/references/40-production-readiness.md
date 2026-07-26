# Production Readiness: Load, Observability, Security

Read this file when you are about to ship, review, or harden a Fiber service.

Server bounds, boot order, listener and shutdown sequencing live in `10-fiber-v3-core.md`.
Middleware order, probe placement, proxy trust and rate limiting live in
`20-routing-middleware-errors.md`. This file does not restate them.

## Readiness semantics

- `/api/health` answers "is this process alive" and runs no dependency probe, ever. A health check
  that calls the database turns a database blip into a pod restart storm.
- `/api/ready` answers "can this pod serve useful traffic" and reports each registered dependency
  check with its severity. A check whose loss must remove the pod from rotation returns not-ready;
  a check whose loss leaves the service serving a degraded but correct response reports its state
  without failing readiness.
- Which dependency carries which severity is a service decision recorded in the service's
  `docs/DECISIONS.md` at the time the dependency is added, not inferred at review time. The exact
  envelope fields, check-item shape and readiness codes are owned by `/alaa-services-contract`
  (`$alaa-services-contract`).

## Concurrency and load

This is the section that justifies choosing Fiber at all, so it names mechanisms rather than
intentions. Pool sizes and cache topology are owned by `/alaa-data-layer` (`$alaa-data-layer`);
retry, backoff and degradation doctrine by `/alaa-reliability-sla` (`$alaa-reliability-sla`);
every numeric value by `/alaa-services-contract` (`$alaa-services-contract`).

**Bound connection admission.** `fiber.Config.Concurrency` is "Maximum number of concurrent
connections", default `256 * 1024`
(https://docs.gofiber.io/api/fiber, verified 2026-07-26). That default is orders of magnitude above
what any database pool behind it can serve, so the default turns a traffic spike into a queue of
requests all waiting on a pool that will time them out. Set it to a number the service's slowest
downstream can actually absorb.

**Bound per-handler concurrency with a semaphore, and shed rather than queue.** Use
`golang.org/x/sync/semaphore.Weighted` or a buffered-channel token for any expensive handler.
Acquire with `TryAcquire`, not `Acquire`: on failure return `503` with `Retry-After` immediately.
Blocking on acquisition converts a concurrency limit into an unbounded latency queue, which fails
the SLA while reporting success.

**Bound fan-out.** Use `errgroup.Group` from `golang.org/x/sync/errgroup` with `WithContext` for
cancellation and `SetLimit(n)` for the bound. A bare `go f()` per request is unbounded goroutine
growth by construction.

**Collapse cache-miss stampedes with `singleflight`.** `golang.org/x/sync/singleflight`'s
`Group.Do`, keyed by the cache key, makes N concurrent misses on the same key produce one
downstream call. Add jitter to the TTL when the key set is written in a batch, so entries created
together do not expire together and recreate the stampede on a schedule. Cache a negative result
with a short TTL so a miss on a nonexistent key does not hit the database on every request.

**Do not put a single mutex on a hot path.** For read-mostly state, swap an immutable snapshot
through `atomic.Pointer[T]`, so readers never block. For a keyed structure, shard into N mutexes
indexed by a hash of the key. Reach for `sync.Map` only in the two cases its documentation names:
a key written once and read many times, or disjoint key sets per goroutine.

**Know what a fasthttp buffer bounds.** `ReadBufferSize` defaults to `4096` and "This also limits
the maximum header size" (https://docs.gofiber.io/api/fiber, verified 2026-07-26). A service behind
a gateway that appends several trusted headers plus a large `Authorization` value can exceed 4 KiB
of headers and fail the request before any handler runs. Size it against the real header set the
gateway produces, and test that case.

**Measure before optimizing serialization or allocation.** Fiber is chosen for allocation behavior,
which makes it exactly the place where an unmeasured "optimization" gets waved through. Take a
`pprof` profile under representative load first; the profile names the file to change.

## Observability

**The OpenTelemetry situation, verified 2026-07-26.** An official Fiber v3 OpenTelemetry middleware
exists and is released: `github.com/gofiber/contrib/v3/otel`, latest `v1.2.2` published 2026-07-15,
first stable `v1.0.0` published 2026-02-08, documented as "Compatible with Fiber v3"
(https://pkg.go.dev/github.com/gofiber/contrib/v3/otel and
https://github.com/gofiber/contrib/blob/main/v3/otel/README.md, both verified 2026-07-26). It is
installed with `go get -u github.com/gofiber/contrib/v3/otel`, imported as
`fiberotel "github.com/gofiber/contrib/v3/otel"`, and registered with
`app.Use(fiberotel.Middleware())`.

The older `github.com/gofiber/contrib/otelfiber/v2` targets Fiber v2 and is not the v3 package. Do
not import it into a v3 service and do not cite it as evidence that v3 tracing is unavailable.

**What that package does not give you.** It creates server spans. It does not implement this
platform's correlation contract, which requires `X-Request-Id` and `traceparent` on **every**
response, including error responses and both probes, with an inbound `traceparent` validated
through the installed `TraceContext` propagator, normalized by reinjection, and replaced with a
fresh valid context plus a bounded warning signal when it is missing or malformed. A Fiber v3
service therefore ships the released span middleware **and** its own correlation middleware, sitting
outside it, that satisfies the contract. Do not describe the service as correlation-complete on the
strength of the span middleware alone.

If the service is a kit consumer, that correlation middleware is a kit change request through
`/alaa-go-chi-development` (`$alaa-go-chi-development`), not service-local code, because a
correlation contract implemented once per service drifts once per service.

**Always-on signals**, with names, cardinality budgets and requirement levels owned by
`/alaa-observability-soc` (`$alaa-observability-soc`):

- structured JSON logs carrying request ID and trace ID on every record;
- request rate, error rate, latency distribution and saturation;
- dependency latency and error counts for database, cache and queue;
- cache hit, miss and error counts;
- server spans from the middleware above, with exemplars linking metrics to traces.

Label cardinality is bounded at the point the label is constructed. A label built from a path
parameter, a user ID, or a client-supplied header is an unbounded label; use the route template.

Profiler endpoints are never exposed on the public listener. Bind them to an operational route
behind the gateway-only network boundary.

## Security

Each of these is a constraint. Where an exception exists, the named skill grants it in a recorded
decision; the agent does not.

- **Never derive identity, tenant, project or authorization context from a client-supplied header.**
  It comes from the gateway trust contract, owned by `/alaa-trust-gateway-auth`
  (`$alaa-trust-gateway-auth`).
- **The authorization-caching prohibition in `SKILL.md` applies here.** Its reason: a cached grant
  outlives the revocation that was supposed to end it, and the window is invisible in logs, so the
  failure is discovered by an auditor rather than by monitoring.
- **Fail closed on every trust decision.** A missing, malformed or unparseable trust header denies
  the request. A parse failure that falls through to "no restrictions" is the failure mode this
  rule exists to prevent, and it is easy to write by accident in Go because the zero value of a
  permission set grants nothing only if you wrote it that way.
- **Never log a secret, token, cookie, password, credentialed connection string, or a trusted
  identity header value.** Redact at the logger, not at each call site: a redaction rule applied per
  call site is a rule that will be forgotten at the next call site.
- **Return the public error envelope, never the internal failure.** The mapping lives in
  `20-routing-middleware-errors.md`.

Threat modelling, authz design and the security review itself are owned by `/alaa-security-review`
(`$alaa-security-review`).

## Pre-ship verification

Each row is a check to run and the file that owns the rule behind it. Run them all before calling a
Fiber service ready for the platform's `99.99%+` SLA.

| Check | Rule owned by |
| --- | --- |
| Boot rejects an out-of-range config value instead of defaulting | `10-fiber-v3-core.md` |
| `ReadTimeout`, `WriteTimeout`, `IdleTimeout`, `BodyLimit`, `Concurrency` all set from config | `10-fiber-v3-core.md`, this file |
| Every retained `Ctx`-derived value passes through `utils.CopyString` / `utils.CopyBytes` | `10-fiber-v3-core.md` |
| No outbound call receives `c` itself as its `context.Context` | `10-fiber-v3-core.md` |
| Shutdown flips readiness before the listener stops, and drains within budget | `10-fiber-v3-core.md` |
| Probes registered before the trust and rate-limit layers | `20-routing-middleware-errors.md` |
| `TrustProxy` true with an explicit `TrustProxyConfig.Proxies` set | `20-routing-middleware-errors.md` |
| Limiter storage matches the replica count, or the limit's documented value says it is per-replica | `20-routing-middleware-errors.md` |
| `StructValidator` set and its adapter compiles | `30-validation-testing.md` |
| Handler tests cover error mapping, validation shape, panic recovery and correlation headers | `30-validation-testing.md` |
| `go test -race ./...` passes | `30-validation-testing.md` |
| Span middleware and correlation middleware both present | this file |
| No unbounded goroutine, no unbounded queue, no single hot-path mutex | this file |
