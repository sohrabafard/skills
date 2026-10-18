# Binding, Validation, and Tests

Read this file when you are about to change a request or response contract, bind a body, wire a
`StructValidator`, or write a handler test.

API names and defaults were verified against the official Fiber v3 docs on **2026-07-26**.

## Binding

Fiber v3 binds through a chained API. `c.Bind().JSON(&dto)` binds a JSON body; the binder set is
`Body`, `JSON`, `Form`, `Query`, `Header`, `Cookie`, `URI` and `All`
(https://docs.gofiber.io/api/bind, verified 2026-07-26).

```go
type Person struct {
	Name string `json:"name"`
	Pass string `json:"pass"`
}

app.Post("/", func(c fiber.Ctx) error {
	p := new(Person)
	if err := c.Bind().JSON(p); err != nil {
		return err
	}
	return c.JSON(p)
})
```

Rules:

- Bind into a transport DTO declared in the transport package. Never bind into a domain entity: a
  binder that writes directly into a domain type lets an unvalidated client field reach a business
  invariant.
- Give every DTO field an explicit `json` tag at every nesting level. An untagged field takes Go's
  default key casing, which is not the platform's wire casing.
- Convert the DTO into an application-layer input type after validation, and pass that inward.
- Treat a bind failure and a validation failure as different outcomes: a bind failure means the
  request could not be parsed, a validation failure means it parsed and violated a rule. They carry
  different public error codes.
- Do not bind into a map or any non-struct destination. Fiber "only runs `StructValidator` for
  struct destinations (or pointers to structs). Binding into maps and other non-struct types skips
  the validator step" (https://docs.gofiber.io/api/bind, verified 2026-07-26) - so a map
  destination is an unvalidated request body.

### Multiple binding sources (v3.5.0)

`Bind().All()` accepts a top-level `binding_source` tag to set source precedence, cached by struct
type; omitted sources are excluded and invalid names fail binding. Use a single-source binder
for a single-source contract. For a combined DTO, state the accepted order and test conflicting
values from URI, body, query, headers and cookies; do not infer precedence from field order.
Binding precedence grants no authority: keep trusted identity separate from request DTOs and apply
`/alaa-trust-gateway-auth` when a client selector conflicts with trusted context.

Verified 2026-09-29: https://github.com/gofiber/fiber/releases/tag/v3.5.0 and
https://docs.gofiber.io/api/bind/#custom-precedence. Earlier v3 consumers must check their tag
before using `binding_source`.

### What Fiber's binder does not do

Before implementing a Fiber bind helper, read `/alaa-golang`
`references/45-failure-behavior-at-the-call-site.md` section 5 for the four decode checks and kit binder
contract. Fiber's binder does not supply that contract; `fiber.Config.BodyLimit` covers only its size
bound. Add the missing checks in one transport helper called by every handler, so a handler cannot forget
one. `50-kit-conflict-register.md` records the surface and its cost.

## The `StructValidator` adapter

`fiber.Config.StructValidator` defaults to `nil`
(https://docs.gofiber.io/api/fiber, verified 2026-07-26), which means bind performs no validation
until you set it. The interface requires one method: `Validate(out any) error`
(https://docs.gofiber.io/guide/validation, verified 2026-07-26).

`go-playground/validator/v10` does **not** satisfy that interface. It exposes
`Struct(s any) error` - a different method name - so passing a `*validator.Validate` straight into
`fiber.Config.StructValidator` does not compile. Write the adapter:

```go
package transport

import (
	"github.com/go-playground/validator/v10"
	"github.com/gofiber/fiber/v3"
)

// structValidator adapts go-playground/validator to fiber.StructValidator.
// The interface requires Validate(out any) error; validator exposes
// Struct(s any) error, so the two are not interchangeable without this shim.
type structValidator struct {
	validate *validator.Validate
}

func (v *structValidator) Validate(out any) error {
	return v.validate.Struct(out)
}

func newApp(errorHandler fiber.ErrorHandler) *fiber.App {
	return fiber.New(fiber.Config{
		StructValidator: &structValidator{validate: validator.New()},
		ErrorHandler:    errorHandler,
	})
}
```

Construct the `*validator.Validate` once at boot and reuse it. It caches struct reflection metadata,
so a per-request `validator.New()` throws that cache away on every request.

The error the adapter returns reaches `fiber.Config.ErrorHandler`. Map
`validator.ValidationErrors` there into the platform's validation envelope, keyed by the public
field name from the DTO's `json` tag rather than the Go field name, so renaming a Go field does not
change the public contract.

## TDD

Before changing behavior, follow `/alaa-golang` `references/63-tdd-and-testing-discipline.md` for the
complete owed-test sequence, isolated failure confirmation and stop/report path; its `SKILL.md`
validation gate owns native commands, general race triggers and broad-check authority.
`/alaa-testing-strategy` owns test obligation, layer, fixtures and coverage.

## Handler tests

`func (app *App) Test(req *http.Request, config ...TestConfig) (*http.Response, error)`, with
`TestConfig` defaulting to `Timeout: time.Second, FailOnTimeout: true`
(https://docs.gofiber.io/next/api/app, verified 2026-07-26).

The 1s default is a trap in two directions. A handler that legitimately takes longer - one hitting a
container-backed database on a cold start - fails the test as a timeout rather than as its real
behavior. And a test that sets `Timeout: 0` to make that stop disables the bound entirely, so a
handler that hangs blocks the suite instead of failing it. Set an explicit `Timeout` that is
comfortably above the handler's real budget and leave `FailOnTimeout: true`.

Cover, per route:

- the success status and the exact response body shape;
- every mapped domain error and the status and public code it produces;
- validation failure shape, including which field names appear;
- the body-cap rejection and the wrong-content-type rejection;
- `X-Request-Id` and `traceparent` present on success **and** on error responses;
- panic recovery producing the platform envelope rather than a dropped connection;
- the trust posture: an unauthenticated call, an authenticated call missing the permission, and an
  authenticated call with it.

## Unit and integration tests

Unit-test `internal/domain` and `internal/application` with no Fiber import at all. If a test in
those packages needs Fiber, the layering has leaked and that is the bug to fix first.

Prefer hand-written fakes for small interfaces. Use a mock only when the interaction itself - call
count, ordering, arguments - is the behavior under test.

Use real PostgreSQL, Redis or a real proxy only when the behavior depends on real storage, driver
or network semantics. A test that spins up a container to assert a pure mapping function is slow
without being more truthful.

## Race and fuzz

- Apply `/alaa-golang`'s race gate and command authority. Fiber adds one trigger: a changed code path
  retaining any value derived from `fiber.Ctx`, including copied values. Race detection does not prove
  buffer-copy safety directly; it catches the concurrent access that usually accompanies buffer reuse.
- Fuzz parsers, codecs, validators and any surface that reads untrusted input. Keep fuzz targets
  fast, deterministic and free of persistent global state.
