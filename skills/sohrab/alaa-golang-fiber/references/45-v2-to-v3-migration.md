# Migrating Fiber v2 to v3

Read this file when you are about to upgrade a repository from `github.com/gofiber/fiber/v2` to
`github.com/gofiber/fiber/v3`, or when you are reading v2-era Fiber code and porting it.

Every change below was verified against https://docs.gofiber.io/whats_new and the linked pages on
**2026-07-26**.

## Sort the breakage before you touch anything

Most of the v2-to-v3 delta is a compile error, and a compile error is safe: the toolchain finds it
for you. The migration risk is concentrated in the small set of changes that keep compiling and
change meaning. Handle that set first, deliberately, with tests; then let the compiler drive the
rest.

| Change | How it fails | Handle it |
| --- | --- | --- |
| `c.Context()` return type reversed | **Silently** - still compiles, different object | First. See below. |
| `Locals("key")` for middleware-owned values | **Silently** - compiles, returns nil | First. See below. |
| `ProxyHeader` unset after the trust-proxy rename | **Silently** - client IP is wrong, not absent | First. See below. |
| `Add` signature | Compile error | Let the compiler find them |
| Config field renames | Compile error | Let the compiler find them |
| Middleware import paths | Compile error | Let the compiler find them |

## The three silent ones

### 1. `c.Context()` reversed meaning

- **v2**: `c.Context()` returned the underlying `*fasthttp.RequestCtx`.
- **v3**: `c.Context()` "returns a `context.Context` that can be used outside the handler". The
  `fasthttp.RequestCtx` moved to `c.RequestCtx()`.

`*fasthttp.RequestCtx` satisfies `context.Context`, so a v2 call site like
`repo.Find(c.Context(), id)` compiles before and after the upgrade while handing the repository a
different object with different cancellation behavior. Nothing in the build output points at it.

Audit every `c.Context()` call site by hand during the migration. Do not rely on the compiler and do
not rely on tests that assert only status codes - the difference shows up as a query that is not
cancelled when the client disconnects, which a passing test will not notice.

While you are in those call sites, apply the v3 cancellation rule from `10-fiber-v3-core.md`: `c`
itself is a `context.Context` whose `Deadline()`, `Done()` and `Err()` are no-ops, so a real
deadline comes from `context.WithTimeout(c.Context(), ...)`.

### 2. `Locals` to `FromContext`

v3 middlewares store their values under unexported context keys and expose typed accessors -
`requestid.FromContext(c)`, `csrf.TokenFromContext(c)` and their siblings - specifically so a string
key cannot collide across packages.

A v2 call site that reads `c.Locals("requestid")` still compiles in v3 and returns nil, because
nothing writes that string key any more. Downstream that becomes an empty request ID in every log
line, or a panic in a type assertion.

Replace every `Locals` read of a middleware-owned value with the owning package's `FromContext`
helper. `Locals` remains correct for values your own application code both writes and reads.

### 3. Trusted proxy rename plus `ProxyHeader`

- **v2**: `EnableTrustedProxyCheck bool` and `TrustedProxies []string`.
- **v3**: `TrustProxy bool` and `TrustProxyConfig`, whose `Proxies` field carries the list, alongside
  `Loopback`, `Private` and `LinkLocal`.

The rename is a compile error, so you will find it. What you will not be told is that in v3
"`ProxyHeader` must be set to read client IPs from proxy headers", and its default is `""`. A
migration that translates the two old fields and stops leaves proxy trust enabled while client IP
resolution silently falls back to the socket peer - which behind a gateway is the gateway, for every
request. Set `ProxyHeader` in the same edit, and assert the resolved client IP in a test that sends
the forwarded header through a trusted peer.

Full field semantics: `20-routing-middleware-errors.md`.

## The compile-error set

**`Ctx` is now an interface.** `DefaultCtx` is its implementation and `NewWithCustomCtx` builds an
app over a custom one. Code that stored a `*fiber.Ctx` now stores a `fiber.Ctx`; the pointer is
gone. Handler signatures become `func(c fiber.Ctx) error`.

**`Add` changed shape.**

- v2: `Add(method, path string, handlers ...Handler) Router`
- v3: `Add(methods []string, path string, handler any, handlers ...any) Router`

The method parameter is a slice, and the first handler is a separate argument from the rest.

**Config renames** that matter to an Ala service: `EnableTrustedProxyCheck` and `TrustedProxies` to
`TrustProxy` and `TrustProxyConfig` as above. Re-read the whole `fiber.Config` literal against the
current field table in `10-fiber-v3-core.md` rather than translating field by field - the migration
is the natural moment to discover that `ReadTimeout`, `WriteTimeout` and `IdleTimeout` were never
set in the v2 config either.

**Middleware import paths** move from `github.com/gofiber/fiber/v2/middleware/...` to
`github.com/gofiber/fiber/v3/middleware/...`. Third-party middleware is a separate decision per
package: `github.com/gofiber/contrib/otelfiber/v2` is v2-only and its v3 replacement is a different
module, `github.com/gofiber/contrib/v3/otel`. See `40-production-readiness.md`.

**Testing.** v3's `app.Test` takes `config ...TestConfig` with `Timeout` and `FailOnTimeout` fields
(https://docs.gofiber.io/next/api/app, verified 2026-07-26). Port every `app.Test` call site and set
an explicit `Timeout`; see `30-validation-testing.md` for why the default is a trap.

## Toolchain

Fiber v3.3.0 declares `go 1.25.0` and the docs state "Version `1.25` or higher is required"
(https://raw.githubusercontent.com/gofiber/fiber/v3.3.0/go.mod and https://docs.gofiber.io/, both
verified 2026-07-26). Raise the repository's `go` directive to at least `1.25` as the first commit
of the migration, run the full suite on the new toolchain, and only then start the Fiber upgrade.
Two toolchain-and-framework changes in one commit make a bisect useless.

`github.com/gofiber/utils/v2` is a direct dependency of Fiber v3.3.0 at `v2.0.6` and is where
`CopyString` and `CopyBytes` live
(https://raw.githubusercontent.com/gofiber/fiber/v3.3.0/go.mod, verified 2026-07-26). Confirm the
import path against the repository's own `go.mod` before writing it, because the module has its own
release line.

## Order of work

1. Raise the `go` directive to 1.25 or higher. Run the suite. Commit.
2. Add or fix handler tests for every route that has none, on v2, so the migration has a baseline
   that can fail. A migration without this step cannot distinguish "ported correctly" from
   "compiles".
3. Change the import paths and let the compiler enumerate the breakage. Do not fix anything yet.
4. Fix the three silent changes above, by hand, with a test for each.
5. Fix the compile errors.
6. Set the server bounds from `10-fiber-v3-core.md` if the v2 config lacked them.
7. Run the focused tests, then `go test ./...`, then `go test -race ./...`.
8. Re-verify proxy trust, correlation headers and the error envelope against live traffic in a
   non-production environment before promoting.

A framework major upgrade is architecture work, not routine cleanup. On an `alaa-go-chi` consumer it
is a change request through `/alaa-go-chi-development` (`$alaa-go-chi-development`) before any of
the above begins.
