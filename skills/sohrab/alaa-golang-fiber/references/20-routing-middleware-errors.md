# Routing, Middleware Order, Errors, Proxy Trust

Read this file when you are about to register routes, order middleware, mount probes, map an error
to a status code, or configure CORS, a rate limiter, or proxy trust.

API names and defaults below were verified against the official Fiber v3 docs on **2026-07-26**;
URLs accompany each claim and are collected in `SOURCES.md`.

## Route registration

- Group routes by API version and by trust posture, and register each group through a single
  function so the posture middleware cannot be omitted by editing one line.
- Handlers bind, validate, call an application service, map the result or error, and return. A
  handler that opens a transaction, issues SQL, calls Redis, or decides a business rule has taken
  work that belongs in `internal/application`.
- Fiber has no equivalent of the kit's family-first router, which refuses to compile a route that
  declares no trust family. On Fiber you build that guarantee yourself or you do not have it; see
  `50-kit-conflict-register.md` for what that costs and what it must satisfy.

The `Add` signature changed between majors and v2 call sites will not compile:

- v2: `Add(method, path string, handlers ...Handler) Router`
- v3: `Add(methods []string, path string, handler any, handlers ...any) Router`

(https://docs.gofiber.io/whats_new, verified 2026-07-26. Full migration set:
`45-v2-to-v3-migration.md`.)

## Middleware order

Register in this order. The order is not stylistic: each layer depends on the ones outside it
having already run.

1. **recover** - `github.com/gofiber/fiber/v3/middleware/recover`,
   `func New(config ...Config) fiber.Handler`
   (https://docs.gofiber.io/middleware/recover, verified 2026-07-26). Register it outermost so a
   panic in any later layer still produces the platform error envelope instead of a dropped
   connection. Leave `EnableStackTrace` at its `false` default in production and send the stack to
   the logger through `StackTraceHandler`; a stack trace in a response body is an information leak.
2. **correlation** - request ID and `traceparent`, before anything that logs or emits a span, so
   every subsequent record carries the same identifiers.
3. **span creation** - see `40-production-readiness.md`.
4. **access log and metrics** - outside the auth layers, so a rejected request is still counted.
5. **body cap** - before any handler reads a body.
6. **trust or gateway posture** - identity, tenant and permission extraction.
7. **rate limit or backpressure**.
8. **handlers**.

CORS sits at position 6 when, and only when, the service owns browser-facing behavior.

### Probes register before the trust layers

`SKILL.md` places the probes ahead of the trust layers. The reason is worth stating once: a probe
that can be failed by a dependency of the thing it is probing reports the wrong answer during
exactly the incident it exists to detect, and a rate-limited probe removes a healthy pod from
rotation under load.

The platform's probe paths are `/api/health` and `/api/ready`. Fiber's bundled healthcheck
middleware (`github.com/gofiber/fiber/v3/middleware/healthcheck`,
`func New(config ...Config) fiber.Handler`, with `LivenessEndpoint`, `ReadinessEndpoint` and
`StartupEndpoint` constants; https://docs.gofiber.io/middleware/healthcheck, verified 2026-07-26)
defaults to different paths and renders its own body shape. Register the platform paths explicitly
and render the platform envelopes; the exact envelope fields are owned by `/alaa-services-contract`
(`$alaa-services-contract`).

## Errors

Handlers and middleware return errors. One place turns an error into a response:
`fiber.Config.ErrorHandler`. Its default is `DefaultErrorHandler`
(https://docs.gofiber.io/api/fiber, verified 2026-07-26), which renders Fiber's own error shape and
not the platform envelope, so every Ala Fiber service replaces it.

- Map each typed domain error to one status code and one stable public error code. The mapping
  lives in the transport package and nowhere else.
- An error whose code is not in the service's registered vocabulary renders as the generic internal
  code. A code that reaches a client is a public contract; an unregistered one must not become one
  by accident.
- Log the internal detail exactly once, at the boundary, with the request ID and trace ID attached.
- Never place SQL text, driver errors, stack traces, secrets, connection strings, trusted-identity
  internals, or the reason an authorization check failed into a response body.
- Return the same envelope shape for every failure, including validation failures, `404`s from the
  router's own not-found handler, and the body-cap rejection. A client that must parse two shapes
  will parse one of them wrong.

## Request ID and correlation

`github.com/gofiber/fiber/v3/middleware/requestid` provides
`func New(config ...Config) fiber.Handler` with `Header` and `Generator` config fields, defaulting
to the `X-Request-ID` header, and exposes `func FromContext(ctx any) string`
(https://docs.gofiber.io/middleware/requestid, verified 2026-07-26).

Read middleware-owned values through the owning package's `FromContext` helper, never through a
string key in `Locals`. The v3 middlewares store their values under unexported context keys
precisely so a string lookup cannot collide or silently return the wrong type
(https://docs.gofiber.io/whats_new, verified 2026-07-26).

The platform's correlation contract is `X-Request-Id` plus `traceparent` on **every** response,
including errors and both probes. Fiber's requestid middleware satisfies the request-ID half and
emits no `traceparent`; the trace half is yours to build. `40-production-readiness.md` states what
it must do, and `50-kit-conflict-register.md` states what it costs.

## Proxy trust

Two config fields, both defaulting to off
(https://docs.gofiber.io/api/fiber, verified 2026-07-26):

- `TrustProxy bool`, default `false`.
- `TrustProxyConfig TrustProxyConfig`, default `{}`, with fields `Proxies` (trusted IPs and CIDR
  ranges), `Loopback`, `Private` and `LinkLocal`.
- `ProxyHeader string`, default `""`, names the header the client IP is read from.

With `TrustProxy` false, Fiber ignores forwarded headers. With it true, Fiber checks the request
against `TrustProxyConfig` before reading proxy headers.

The rule: set `TrustProxy: true` and populate `TrustProxyConfig.Proxies` with the gateway's IPs or
CIDR ranges, taken from deployment configuration. Do not set `Private: true` or `Loopback: true` as
a shortcut in an environment where anything other than the gateway can reach the pod, because those
flags trust an address class rather than a specific peer.

Client IP, host and scheme may be derived from forwarded headers only under that configuration.
Identity, tenant, project and authorization context are never derived from a client-supplied
header under any configuration; they come from the gateway trust contract, owned by
`/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`), with gateway topology owned by
`/alaa-haproxy` (`$alaa-haproxy`).

## CORS

Configure CORS only in a service that a browser calls directly.

- Never combine a wildcard origin with credentials.
- Never write an `AllowOriginsFunc` that returns `true` for every origin. If the allowed set is
  dynamic, resolve it from configuration and reject anything not in that set.
- Read origins from configuration, so a new frontend deployment is a config change and not a code
  change.

## Rate limiting

`github.com/gofiber/fiber/v3/middleware/limiter` provides
`func New(config ...Config) fiber.Handler` with `Max`, `Expiration`, `KeyGenerator`, `Storage`,
`LimitReached` and `LimiterMiddleware`. Its default storage is documented as "An in-memory store for
this process only", and "This module does not share state with other processes/servers by default."
(https://docs.gofiber.io/middleware/limiter, verified 2026-07-26.)

Consequences you must act on:

- A limiter left on default storage in a service running N replicas permits N times its configured
  `Max`. Either say so in the limit's documented value, or set `Storage` to a shared backend.
- Platform-wide limits belong at the gateway. A service-local limiter protects a specific expensive
  endpoint from a caller the gateway already admitted; it is not the platform's rate limit.
- Write `KeyGenerator` over a value the client cannot forge. Keying on a raw client-supplied header,
  or on a client IP read without `TrustProxy` configured, lets any caller rotate its own key and
  bypass the limit entirely.

## Adapting `net/http` middleware

`github.com/gofiber/fiber/v3/middleware/adaptor` converts between the two worlds, including
`HTTPMiddleware(mw func(http.Handler) http.Handler) fiber.Handler` and
`HTTPHandler(h http.Handler) fiber.Handler`
(https://docs.gofiber.io/middleware/adaptor, verified 2026-07-26). The docs state the cost:
"Adapted `net/http` handlers still run with standard library semantics. They don't have access to
`fiber.Ctx`, and the compatibility layer comes with additional overhead compared to native Fiber
handlers."

That overhead is the reason the adaptor is not a general answer to the kit-surface gap. See
`50-kit-conflict-register.md`, which treats it as the central design tension rather than a
convenience.
