# chi API Guide

How to register routes and write handlers in a chi service. The service's package layout is in
`60-service-architecture-patterns.md`; server bounds, decode limits, deadlines, and shutdown are in
`45-failure-behavior-at-the-call-site.md`; this file does not repeat either.

## Which mode you are in

Read `go.mod` first. The two modes differ in what you are allowed to build, not in style:

- **Kit mode** — `go.mod` requires `git.alaatv.com/vk/alaa-go-chi`. The router, the middleware chain, the error
  envelope, the readiness surface, and the server's bounds already exist. Your job is to add routes and handlers to
  them.
- **Standalone mode** — `go.mod` requires `github.com/go-chi/chi/v5` and not the kit. You build those pieces yourself,
  and the kit's shape is the target you build toward.

Every section below marks which mode it governs.

## Route registration — kit mode

**Rule:** register every route through a route family. A route that reaches the mux without a declared family is
rejected at boot with `ErrUnlabeledRoute` (`httpkit/route_inventory.go`, read 2026-07-26) — the router fails closed, so
an unlabelled route is a startup failure, not a silently public endpoint.

**Forbidden:** calling `chi.Router.Get`, `.Post`, `.Handle`, or `.Mount` on the kit's mux directly, and constructing a
second `chi.Router` alongside it. **Rule:** add the route to the family that matches its posture; which posture a route
carries is owned by `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) P2.

## Route registration — standalone mode

**Rule:** build the router in one exported function that takes its dependencies as a struct and returns
`http.Handler`. Nothing else in the service constructs a router.

```go
func NewRouter(deps Deps) http.Handler {
    r := chi.NewRouter()
    r.Use(deps.Recover, deps.Correlation, deps.Trace, deps.AccessLog, deps.BodyCap)

    r.Get("/healthz", deps.Health.Live)
    r.Get("/readyz", deps.Health.Ready)

    r.Route("/api/v1", func(r chi.Router) {
        r.Mount("/users", newUserRoutes(deps))
    })
    return r
}
```

**Rule:** group routes with `Route`, `Group`, and `Mount` by resource or bounded context, one file per group.
**Forbidden:** a single file registering routes for more than one resource.

**Forbidden:** reading a dependency from a package-level variable inside a handler. **Rule:** every dependency arrives
through the handler's struct, constructed once in `NewRouter`'s caller.

## Middleware — kit mode

**Verified fact (`httpkit/middleware.go`, read 2026-07-26):** the chain is fixed and ordered — recover, correlation,
span, access-log and metrics, body cap. It is not configurable, not reorderable, and not partially adoptable.

**Forbidden:** re-adding recovery, request-id, tracing, access logging, metrics, or a body cap in a service. Each one
duplicates a chain layer, and two recoverers or two access logs produce two different answers about the same request.

**Rule:** service-specific middleware mounts inside a route family, which places it after the whole chain, so it runs
with correlation and span context already present.

## Middleware — standalone mode

**Rule:** order the chain outermost-first: recover, then correlation and request id, then tracing span, then access
logging and metrics, then the body cap, then authentication, then route-specific middleware.

The order is forced by three facts, not by taste: recovery must be outermost or a panic in another layer escapes it;
correlation must precede logging and tracing or their records carry no id; the body cap must precede any handler that
reads the body.

**Forbidden:** mounting CORS inside a route group — `github.com/go-chi/cors` is written to run as top-level
middleware and behaves differently anywhere else.

**Forbidden:** using `middleware.Throttle` as a rate limiter. It caps concurrent handler executions in one process and
knows nothing about clients; see `46-chi-under-load.md` for what the platform actually does about admission control.

## Handler shape — both modes

**Rule:** a handler does exactly five things, in this order, and nothing else:

1. bind path, query, and header parameters into a transport struct;
2. decode the body — `httpkit.Bind` in kit mode, the four checks in `45-failure-behavior-at-the-call-site.md`
   section 5 in standalone mode;
3. validate the transport struct;
4. call exactly one use-case method with the request-scoped context;
5. map the result or the error to a response.

**Forbidden:** SQL, Redis calls, broker publishes, business rules, transaction control, or `go func()` inside a
handler. Each has an owner: the repository, the cache decorator, the outbox, the use case, and — for goroutines —
`/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) P9.

**Rule:** keep the transport struct separate from the domain input struct and map between them explicitly. A single
struct shared by the wire and the domain makes every wire change a domain change.

## Error mapping

**Kit mode. Rule:** return a typed `errkit` error from the use case and let the kit's single mapper render it.
**Forbidden:** calling `http.Error`, writing a status code by hand, or building a response envelope in a handler.

**Standalone mode. Rule:** define domain error values in the domain package, map them to status codes and response
shapes in exactly one transport-layer function, and call that function from every handler.
**Forbidden:** a `switch` on error type in more than one handler.

**Forbidden, both modes:** putting a driver error, a validator error, or an error string into a response body. **Rule:**
log the original with the correlation id and return the mapped code. The codes and the envelope shape belong to
`/alaa-services-contract` (`$alaa-services-contract`).

## Health and readiness

**Rule:** expose two distinct endpoints answering two distinct questions — liveness answers "should this process keep
running", readiness answers "should this instance receive traffic now". A readiness check that always mirrors liveness
is not a readiness check.

**Rule:** readiness turns negative before the drain begins, so the load balancer stops sending work before the process
stops accepting it. On the kit that ordering is `runkit`'s `stop_intake` phase and you do not implement it.

**Kit mode. Forbidden:** hand-writing a readiness envelope or a check registry; the kit owns both. Register your
check with the kit's readiness surface and give it a severity. **Verified fact (`rediskit/doc.go`, read 2026-07-26):**
the kit reports Redis readiness at degraded rather than required severity, so a Redis blip does not remove the
instance from rotation.

The path names, the envelope shape, and which dependencies are required versus degraded belong to
`/alaa-services-contract` (`$alaa-services-contract`).

## Testing chi handlers

The test-first sequence is in `63-tdd-and-testing-discipline.md`. What is specific to chi:

**Rule:** test the router, not the handler function, whenever a test depends on a path parameter, a middleware, or a
route family — `chi.URLParam` reads from the routing context, which only exists once the request has passed through
the router.

```go
rec := httptest.NewRecorder()
req := httptest.NewRequest(http.MethodGet, "/api/v1/users/0192f3c1-...", nil)
router.ServeHTTP(rec, req) // the router, so URL params and middleware are real
```

**Rule:** assert the status code, the response body's shape, and the `Content-Type` header. A test that asserts only
the status passes when the envelope is wrong.

**Kit mode. Rule:** the kit's `contracttest` package asserts the trust boundary, the error envelope, readiness, and
the route inventory as black-box HTTP conformance. Run it; do not write a service-local reimplementation of any of
those four assertions.

## Before you call a chi change done

- Every new route is registered through a family (kit) or inside one router construction function (standalone).
- No handler contains SQL, Redis, a publish, a transaction, or a goroutine.
- Every decode goes through `httpkit.Bind` (kit) or carries all four checks from
  `45-failure-behavior-at-the-call-site.md` section 5 (standalone).
- Every error leaves through the single mapper.
- Route-level tests exercise the router, and the kit's contract tests pass.
