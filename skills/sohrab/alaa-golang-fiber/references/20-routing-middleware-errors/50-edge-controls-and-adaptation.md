Version-sensitive claims in this topic depend on [Fiber sources and freshness](../SOURCES.md).

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
`../50-kit-conflict-register.md`, which treats it as the central design tension rather than a
convenience.
