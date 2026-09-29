Version-sensitive claims in this topic depend on [Fiber sources and freshness](../SOURCES.md).

## Route registration

- Group routes by API version and by trust posture, and register each group through a single
  function so the posture middleware cannot be omitted by editing one line.
- Handlers bind, validate, call an application service, map the result or error, and return. A
  handler that opens a transaction, issues SQL, calls Redis, or decides a business rule has taken
  work that belongs in `internal/application`.
- Fiber has no equivalent of the kit's family-first router, which refuses to compile a route that
  declares no trust family. On Fiber you build that guarantee yourself or you do not have it; see
  `../50-kit-conflict-register.md` for what that costs and what it must satisfy.

The `Add` signature changed between majors and v2 call sites will not compile:

- v2: `Add(method, path string, handlers ...Handler) Router`
- v3: `Add(methods []string, path string, handler any, handlers ...any) Router`

(https://docs.gofiber.io/whats_new, verified 2026-07-26. Full migration set:
`../45-v2-to-v3-migration.md`.)
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
3. **span creation** - see `../40-production-readiness.md`.
4. **access log and metrics** - outside the auth layers, so a rejected request is still counted.
5. **body cap** - before any handler reads a body.
6. **trust or gateway posture** - identity, tenant and permission extraction.
7. **rate limit or backpressure**.
8. **handlers**.

CORS sits at position 6 when, and only when, the service owns browser-facing behavior.

### Probes register before the trust layers

`../SKILL.md` places the probes ahead of the trust layers. The reason is worth stating once: a probe
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
