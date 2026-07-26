# Fiber v3 Core: App, Config, Context Lifetime, Listener

Read this file when you are about to create a `fiber.App`, set `fiber.Config`, set server bounds,
or start and stop the listener.

Every API name, signature and default below was verified against the official Fiber v3 docs on
**2026-07-26**. Source URLs are listed per claim and collected in `SOURCES.md`.

## Version and import

- Import path: `github.com/gofiber/fiber/v3`.
- Latest released module version at verification: `v3.3.0`, published 2026-05-22
  (https://pkg.go.dev/github.com/gofiber/fiber/v3, verified 2026-07-26).
- Minimum Go version: "Version `1.25` or higher is required."
  (https://docs.gofiber.io/, verified 2026-07-26). If the repository's `go` directive is higher,
  keep it; never regress it.
- Fiber runs on `fasthttp`, not `net/http`. A `net/http` fact is not a Fiber fact. Do not carry
  assumptions across.

## Context value lifetime: the one memory-corruption hazard

Fiber reuses request buffers. The docs state, for `Params`, `Query`, `Get`, `Body`, `Cookies` and
their siblings: "The returned value is valid only within the handler. Do not store references."
(https://docs.gofiber.io/api/ctx, verified 2026-07-26.)

`SKILL.md` states the constraint. This is its scope: a value outlives the handler when it is stored
in a struct, sent to a goroutine, put in a cache, logged after the handler returns, passed to a
worker or a queue, or captured by a closure that outlives the handler. Each of those is readable off
the code, so the rule needs no judgement call.

The copy functions are named. Use them:

- `utils.CopyString(s string) string` for strings.
- `utils.CopyBytes(b []byte) []byte` for byte slices.

Both are documented at https://docs.gofiber.io/api/ctx (verified 2026-07-26).

```go
func (h *NewsHandler) Publish(c fiber.Ctx) error {
	// Retained past the handler, so it is copied at the point of extraction.
	newsID := utils.CopyString(c.Params("id"))

	go h.warmCache(newsID) // safe: newsID owns its own backing array

	return c.SendStatus(fiber.StatusAccepted)
}
```

There is no agent-granted exception to this rule. If a value never leaves the handler frame, no
copy is needed, and that is a property you can read off the code rather than a judgement call:
if the value is only read and returned within the same function body, it does not outlive the
handler.

### `Immutable` is a boot-time service-wide decision

`fiber.Config.Immutable` defaults to `false`
(https://docs.gofiber.io/api/fiber, verified 2026-07-26). Setting it `true` makes Fiber allocate a
copy of every returned value, which costs allocation and throughput on every request and buys
safety globally.

That trade is made once, by the service owner, at boot, for the whole service, and recorded in the
service's `docs/DECISIONS.md`. It is never invoked at a call site as a reason to skip a copy: a
per-site claim that "Immutable is on" cannot be verified at that site, and it silently breaks if the
service later turns `Immutable` off for throughput.

`App.GetString(s string) string` and `App.GetBytes(b []byte) []byte` are the companions to that
decision, not substitutes for copying. They "return `s` unchanged when `Immutable` is disabled or
`s` resides in read-only memory. Otherwise [they return] a detached copy"
(https://docs.gofiber.io/next/api/app, verified 2026-07-26). Because they are no-ops when
`Immutable` is disabled, using them in a service that has not enabled `Immutable` retains a value
that will be overwritten. Use them only in a service whose `Immutable` decision is recorded as
enabled; use `utils.CopyString` / `utils.CopyBytes` everywhere else.

### `fiber.Ctx` is a `context.Context` whose cancellation does nothing

In v3, `fiber.Ctx` implements `context.Context`. It is not a usable cancellation source: "Due to
current limitations in how fasthttp works, `Deadline()`, `Done()` and `Err()` are no-ops."
(https://docs.gofiber.io/api/ctx, verified 2026-07-26.)

The consequence is load-bearing on a platform that requires every outbound call to be bounded:
**passing `c` itself as the `context.Context` for a database query, a Redis command, or an HTTP call
gives that call no deadline and no cancellation on client disconnect.** Derive a real one:

```go
func (h *NewsHandler) Get(c fiber.Ctx) error {
	ctx, cancel := context.WithTimeout(c.Context(), h.readTimeout)
	defer cancel()

	item, err := h.app.GetNews(ctx, utils.CopyString(c.Params("id")))
	if err != nil {
		return err
	}
	return c.JSON(item)
}
```

`c.Context()` returns "a `context.Context` that can be used outside the handler"; `c.RequestCtx()`
returns the `*fasthttp.RequestCtx`
(https://docs.gofiber.io/whats_new, verified 2026-07-26). Deadlines you attach with
`context.WithTimeout` work normally; what does not work is relying on Fiber to cancel for you.

Never pass `fiber.Ctx` into `internal/domain`, `internal/application`, a repository, a worker or a
background job. Those take `context.Context` and plain Go types.

## Server bounds

`fiber.Config` verified at https://docs.gofiber.io/api/fiber on 2026-07-26:

| Field | Type | Fiber default | Why the default is unsafe |
| --- | --- | --- | --- |
| `ReadTimeout` | `time.Duration` | `0` | Unbounded. A client that opens a connection and dribbles a request header holds a connection open forever (slowloris). |
| `WriteTimeout` | `time.Duration` | `0` | Unbounded. A slow reader pins a response and its buffers indefinitely. |
| `IdleTimeout` | `time.Duration` | `0` | Unbounded. Keep-alive connections are never reaped. |
| `BodyLimit` | `int` | `4 * 1024 * 1024` | 4 MiB, larger than the platform request cap. |
| `Immutable` | `bool` | `false` | See the context-lifetime section above. |
| `TrustProxy` | `bool` | `false` | Forwarded headers are not trusted until this is `true`; see `20-routing-middleware-errors.md`. |
| `TrustProxyConfig` | `TrustProxyConfig` | `{}` | No proxies trusted; see `20-routing-middleware-errors.md`. |
| `StructValidator` | `StructValidator` | `nil` | Bind performs no validation; see `30-validation-testing.md`. |
| `ErrorHandler` | `ErrorHandler` | `DefaultErrorHandler` | Renders Fiber's own error shape, not the platform envelope. |

`SKILL.md` requires all four to be set and names `/alaa-services-contract`
(`$alaa-services-contract`) as the owner of their values. For reference, the kit's chi services
run `HTTP_READ_TIMEOUT` 10s, `HTTP_WRITE_TIMEOUT` 30s, `HTTP_IDLE_TIMEOUT`
120s and `HTTP_MAX_BODY_BYTES` 1 MiB, each read from validated environment configuration and
clamped at boot to a permitted range. A Fiber service reads the same environment keys and enforces
the same clamps, because an operator who tunes one service should not need to learn a second
vocabulary.

```go
app := fiber.New(fiber.Config{
	ReadTimeout:     cfg.HTTP.ReadTimeout,
	WriteTimeout:    cfg.HTTP.WriteTimeout,
	IdleTimeout:     cfg.HTTP.IdleTimeout,
	BodyLimit:       int(cfg.HTTP.MaxBodyBytes),
	StructValidator: &structValidator{validate: validator.New()},
	ErrorHandler:    envelopeErrorHandler,
})
```

A config value that arrives out of range fails the boot. Do not clamp silently and do not default
quietly: an operator who sets `HTTP_READ_TIMEOUT=0` intending "no limit" must be told at boot that
the value is rejected, not discover it during an incident.

## Boot order

1. Load and validate configuration; fail the process on any invalid or out-of-range value.
2. Construct the logger, metrics registry and tracer provider.
3. Construct database, cache and external clients.
4. Construct repositories, then application services.
5. Construct the `*fiber.App` with the config above.
6. Register middleware in the order fixed by `20-routing-middleware-errors.md`.
7. Register every route.
8. Start the listener.

Steps 6 and 7 complete before step 8, per the route-registration rule in `SKILL.md`.

Data-layer client choice, pool sizing and cache topology are owned by `/alaa-data-layer`
(`$alaa-data-layer`), and the kit's `rediskit` contract is reached through
`/alaa-go-chi-development` (`$alaa-go-chi-development`). This skill states none of it.

## Listener and shutdown

Verified at https://pkg.go.dev/github.com/gofiber/fiber/v3 and
https://raw.githubusercontent.com/gofiber/fiber/v3.3.0/listen.go on 2026-07-26:

- `func (app *App) Listen(addr string, config ...ListenConfig) error`
- `func (app *App) Shutdown() error`
- `func (app *App) ShutdownWithTimeout(timeout time.Duration) error`
- `func (app *App) ShutdownWithContext(ctx context.Context) error`

`ListenConfig` fields that matter for a production service, with their documented defaults:

| Field | Default | Use |
| --- | --- | --- |
| `GracefulContext` | `nil` | A `context.Context` whose cancellation begins graceful shutdown. Wire it to `SIGINT` and `SIGTERM`. |
| `ShutdownTimeout` | `10 * time.Second` | Budget for draining in-flight requests. `0` disables the timeout and waits forever. |
| `DisableStartupMessage` | `false` | Set `true`; the ASCII banner is noise in structured logs. |
| `EnablePrefork` | `false` | Leave `false`. Prefork forks multiple processes on one port and breaks in-process metric registries, connection pools and readiness state. |
| `ListenerNetwork` | `NetworkTCP4` | Set explicitly if the deployment needs IPv6 or a Unix socket. |

Shutdown order, matching the kit's four ordered phases (`stop_intake`, `drain_workers`,
`flush_buffers`, `close_pools`) on a 30s total budget:

1. Flip readiness to not-ready and let the load balancer drain the pod, before the listener stops.
2. Cancel `GracefulContext` so Fiber stops accepting connections and drains in flight within
   `ShutdownTimeout`.
3. Cancel background workers and wait for them.
4. Flush buffered writes, spans and metrics.
5. Close database pools, cache clients, queue connections and exporters.
6. Log the shutdown result once, with the phase that consumed the budget if any did.

Step 1 precedes step 2. A service that stops the listener first returns connection errors to
traffic the load balancer has not yet stopped sending.

## Hooks

Fiber's startup and shutdown hooks carry lifecycle events only: startup diagnostics, the
readiness flip, and the shutdown result. No business logic runs in a hook, because a hook has no
request context, no trust context and no error path back to a client.

## Custom context

`Ctx` is an interface in v3 with `DefaultCtx` as its implementation, and `NewWithCustomCtx` builds
an app over a custom one (https://docs.gofiber.io/whats_new, verified 2026-07-26). Use a custom
context only to remove duplication that is genuinely at the transport edge, such as a repeated
accessor for a value the trust middleware placed in the request context. Dependencies reach
handlers through constructor injection on the handler struct, never through a custom context.
