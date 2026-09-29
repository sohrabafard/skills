Version-sensitive claims in this topic depend on [Fiber sources and freshness](../SOURCES.md).

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
emits no `traceparent`; the trace half is yours to build. `../40-production-readiness.md` states what
it must do, and `../50-kit-conflict-register.md` states what it costs.
