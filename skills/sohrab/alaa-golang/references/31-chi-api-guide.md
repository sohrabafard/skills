# Chi API Guide

## Table of contents

- Why `chi` fits this stack
- Minimal service shape
- Router construction
- Middleware order
- Trusted gateway integration
- Validation and request decoding
- Error mapping
- Health and readiness
- Timeouts and shutdown
- Observability
- Testing
- Common mistakes

## Why `chi` fits small services in this stack

`chi` is the best default for raw small or simple HTTP APIs in this pack because it keeps you in `net/http`.

That gives you straightforward behavior with:

- `context.Context`
- `http.Server`
- `httptest`
- `otelhttp`
- `promhttp`
- reverse proxies and trusted gateway headers
- standard middleware and standard transports

For small services, that simplicity is more valuable than framework cleverness. For raw large, high-concurrency, or
SLA-heavy services, load `alaa-golang-fiber` ( `$alaa-golang-fiber` ) and consider Fiber instead.

## Minimal service shape

A clean `chi` service usually looks like this:

```text
cmd/<service>/main.go
internal/app/
internal/httpserver/
internal/httpapi/
internal/domain/
internal/repository/
internal/observability/
internal/config/
```

Keep these boundaries clear:

- `main.go` wires dependencies and starts the process
- `httpserver` owns `http.Server`, lifecycle, and shutdown
- `httpapi` owns routes, middleware, request decoding, and response writing
- `domain` owns business rules
- `repository` owns database access behind interfaces
- Redis cache access stays behind use case, repository decorator, or cache abstractions

## Router construction

Build the router once and pass dependencies in explicitly.

```go
func NewRouter(deps Deps) http.Handler {
    r := chi.NewRouter()

    r.Use(middleware.RequestID)
    r.Use(middleware.RealIP)
    r.Use(middleware.Recoverer)
    r.Use(middleware.Timeout(30 * time.Second))

    r.Get("/healthz", deps.HealthHandler.Health)
    r.Get("/readyz", deps.HealthHandler.Ready)

    r.Route("/api/v1", func(r chi.Router) {
        r.Mount("/users", NewUserRoutes(deps))
    })

    return r
}
```

Prefer `Route`, `Group`, and `Mount` over giant flat route files.

## Middleware order

Middleware order matters.

A safe default order is:

1. request ID
2. real IP or trusted forwarding logic
3. panic recovery
4. timeout or deadline middleware
5. auth or trusted-gateway context middleware
6. logging and tracing middleware that should see the final context
7. rate limiting or endpoint-specific controls where needed

Notes:

- put panic recovery before business handlers
- keep timeout middleware early so downstream work sees the deadline
- keep auth and trusted-gateway extraction before handlers that need identity
- do not mount global CORS in the wrong place; `go-chi/cors` is designed as top-level middleware

## Trusted gateway integration

In this platform, many services sit behind a trusted gateway.

That means your `chi` middleware should usually:

- reject or ignore client-supplied internal headers unless they came from the trusted edge
- extract trusted identity and tenant context from the gateway contract, not from raw client claims
- keep that extracted auth context in request context using typed keys or a dedicated request-scoped struct
- avoid re-verifying JWTs in every service unless the service is truly exposed or is part of the auth boundary

Do not smear gateway semantics across every handler. Put them in one middleware layer.

## Validation and request decoding

Keep request decoding and validation at the edge.

A good pattern is:

1. decode request body or params into a transport DTO
2. validate the DTO
3. map to a domain input struct
4. call application logic
5. map result to response DTO

Example skeleton:

```go
type CreateUserRequest struct {
    Email string `json:"email" validate:"required,email"`
    Name  string `json:"name" validate:"required,min=2,max=100"`
}

func (h *Handler) CreateUser(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        writeError(w, r, ErrBadRequest)
        return
    }

    if err := h.validator.Struct(req); err != nil {
        writeValidationError(w, r, err)
        return
    }

    out, err := h.app.CreateUser(r.Context(), app.CreateUserInput{
        Email: req.Email,
        Name:  req.Name,
    })
    if err != nil {
        writeMappedError(w, r, err)
        return
    }

    writeJSON(w, http.StatusCreated, out)
}
```

Do not leak validator errors or database errors directly to the client.

## Error mapping

Keep one central error-mapping layer.

Do not let every handler decide status codes ad hoc.

A good pattern is:

- domain errors map to stable application error codes
- transport layer maps those codes to HTTP status codes and response envelopes
- logs keep internal detail, responses keep safe detail

Example mapping idea:

```text
ErrBadRequest       -> 400
ErrUnauthorized     -> 401
ErrForbidden        -> 403
ErrNotFound         -> 404
ErrConflict         -> 409
ErrRateLimited      -> 429
ErrUnavailable      -> 503
ErrInternal         -> 500
```

## Health and readiness

Expose both `healthz` and `readyz`.

Use them differently:

- `healthz` answers: is the process alive enough to stay running?
- `readyz` answers: should the platform send this instance new traffic right now?

During shutdown, readiness should flip before the drain window starts.

## Timeouts and shutdown

Use `http.Server` explicitly and keep shutdown deterministic.

```go
srv := &http.Server{
    Addr:              cfg.HTTPAddr,
    Handler:           handler,
    ReadHeaderTimeout: 5 * time.Second,
    IdleTimeout:       60 * time.Second,
}
```

Recommended shutdown order:

1. fail readiness
2. stop accepting new work
3. cancel the root context for workers and background loops
4. call `srv.Shutdown(ctx)`
5. wait for goroutines and worker pools to finish
6. close downstream resources after workers stop using them

Important: `middleware.Timeout` only helps if downstream code respects `ctx.Done()`.

## Observability

A good `chi` service should have all of these from day one:

- request ID propagation
- structured logs with `slog`
- request and dependency metrics
- tracing with OpenTelemetry
- explicit health and readiness endpoints

Useful building blocks:

- `go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp`
- `github.com/prometheus/client_golang/prometheus`
- `github.com/prometheus/client_golang/prometheus/promhttp`
- `github.com/go-chi/chi/v5/middleware`

For request logging, do not stop at a colorful local logger. Make sure logs are structured and production-usable.

## Testing

One reason `chi` fits this stack well is that testing stays simple.

Use `httptest` and build handlers as plain `http.Handler` values.

```go
req := httptest.NewRequest(http.MethodGet, "/api/v1/users/42", nil)
rec := httptest.NewRecorder()
handler.ServeHTTP(rec, req)

if rec.Code != http.StatusOK {
    t.Fatalf("unexpected status: %d", rec.Code)
}
```

Test at three levels:

- handler tests for decoding, validation, auth context, and response codes
- application tests for business logic
- integration tests for database, Redis, and other dependencies

## Common mistakes

### Giant route files

Split routes by bounded context or resource. Use `Mount` and `Route`.

### Fat handlers

Handlers should decode, validate, call app logic, and write responses. They should not hold real business logic.

### Stringly typed context values

Use typed keys or a request-scoped auth/context object.

### Missing server timeouts

Do not rely only on reverse proxies. Configure `http.Server` timeouts explicitly.

### Ignoring `ctx.Done()`

Timeout middleware does not magically stop your work unless your code listens to the context.

### Re-verifying JWTs everywhere

In a trusted-gateway architecture, most services should trust validated upstream context instead of each becoming an auth service.

### Router-level convenience middleware without checking behavior

Examples:

- `RedirectSlashes` can be surprising around proxies and file-serving use cases
- CORS middleware should usually be mounted at the top level, not deep in a route group
- concurrency throttling middleware is not the same thing as per-user or distributed rate limiting

## What to load next

- `golang-context` ( `$golang-context` ) for request lifetime rules
- `golang-observability` ( `$golang-observability` ) for logs, metrics, traces, and profiling
- `golang-testing` ( `$golang-testing` ) for handler and integration testing
- `alaa-trust-gateway-auth` ( `$alaa-trust-gateway-auth` ) when gateway-derived identity is part of the design
