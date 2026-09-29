# Sources and Freshness Policy

Read this file when you are about to assert any Fiber API name, signature, default, or
version-sensitive behavior.

## The rule

An API claim in this skill carries a source URL and a verification date, or it is a defect. This is
not bookkeeping. The version of this skill that this one replaced asserted Fiber APIs with no source
and no date, and at least one of those assertions was wrong in a way that would not compile:
`fiber.Config.StructValidator` was shown receiving a `*validator.Validate` directly, which does not
satisfy the `Validate(out any) error` interface.

Before you write a Fiber fact, fetch the page. Before you trust a fact already in this skill, check
its date against how long ago Fiber last released.

## Verification state

Existing API claims retain their **2026-07-26** evidence unless individually refreshed. On
**2026-09-29**, the v3.5.0 release and tagged module source verified the new compatibility guidance;
this is not consumer-runtime proof or a revalidation of private-kit facts.

Versions observed at the 2026-09-29 refresh (older companion observations remain labeled):

| Module | Version | Published |
| --- | --- | --- |
| `github.com/gofiber/fiber/v3` | `v3.5.0` | 2026-08-13 |
| `github.com/gofiber/utils/v2` (direct dependency of the above) | `v2.4.1` required by Fiber | v3.5.0 tagged `go.mod` |
| `github.com/gofiber/contrib/v3/otel` | `v1.2.2`, historical observation on 2026-07-26; not refreshed | 2026-07-15 |

Fiber v3.5.0's tagged `go.mod` declares `go 1.25.0`; inspect the consumer directive before adoption.
Release evidence: https://github.com/gofiber/fiber/releases/tag/v3.5.0 and
https://raw.githubusercontent.com/gofiber/fiber/v3.5.0/go.mod (checked 2026-09-29).
Proxy security and the docs/tag disagreement are owned by `20-routing-middleware-errors.md`;
binding precedence by `30-validation-testing.md`; `SkipUnmatchedRoutes` by `10-fiber-v3-core.md`.

## Which page answers which question

Prefer the released-v3 pages. `docs.gofiber.io/next/...` is documentation for the **unreleased**
next version; it is cited here only where the released page did not carry the detail, and each such
citation is marked in the reference file that uses it.

| Question | Page |
| --- | --- |
| Fiber version, install, minimum Go version | https://docs.gofiber.io/ |
| `fiber.Config` fields and defaults, including the server bounds, `Immutable`, `Concurrency`, `TrustProxy`, `TrustProxyConfig`, `ProxyHeader`, `StructValidator`, `ErrorHandler`, `ReadBufferSize` | https://docs.gofiber.io/api/fiber |
| `fiber.Ctx` value lifetime, the copy helpers, `Ctx` as a `context.Context`, `RequestCtx()` | https://docs.gofiber.io/api/ctx |
| `app.Test` and `TestConfig`, `App.GetString`, `App.GetBytes` | https://docs.gofiber.io/next/api/app |
| Binding API, binder set, `StructValidator` behavior on non-struct destinations | https://docs.gofiber.io/api/bind |
| The `StructValidator` interface and its `go-playground/validator` adapter | https://docs.gofiber.io/guide/validation |
| v2-to-v3 changes: `Ctx` interface, `Context()` reversal, `Add` signature, `Locals` to `FromContext`, trust-proxy rename | https://docs.gofiber.io/whats_new |
| Error handling, `fiber.Error`, the `ErrorHandler` contract | https://docs.gofiber.io/guide/error-handling |
| recover middleware | https://docs.gofiber.io/middleware/recover |
| requestid middleware and `FromContext` | https://docs.gofiber.io/middleware/requestid |
| healthcheck middleware and its endpoint constants | https://docs.gofiber.io/middleware/healthcheck |
| CORS middleware | https://docs.gofiber.io/middleware/cors |
| limiter middleware, storage semantics, multi-replica behavior | https://docs.gofiber.io/middleware/limiter |
| `net/http` adaptor and its documented overhead | https://docs.gofiber.io/middleware/adaptor |
| Released versions, publish dates, and module dependency facts | https://pkg.go.dev/github.com/gofiber/fiber/v3 and https://pkg.go.dev/github.com/gofiber/contrib/v3/otel |
| `ListenConfig` struct fields and defaults, and Fiber's own `go` directive | https://raw.githubusercontent.com/gofiber/fiber/v3.3.0/listen.go and https://raw.githubusercontent.com/gofiber/fiber/v3.3.0/go.mod |
| Fiber v3 OpenTelemetry middleware install and registration | https://github.com/gofiber/contrib/blob/main/v3/otel/README.md |

Go testing sources, for the test discipline in `30-validation-testing.md`:
https://pkg.go.dev/testing, https://go.dev/blog/subtests, https://go.dev/doc/security/fuzz/.

## Verifying rather than inferring

- A missing mention is not evidence of absence. If a page does not state a default, say the default
  is unverified; do not infer it from another framework or from an older Fiber major.
- Read the pinned tag, not `main`, when the question is what a released version does. A README on
  `main` can describe unreleased behavior.
- When a fact cannot be verified, write it as unverified in the text and name what would settle it.
  A hedge attached to a rule ("where the platform supports it") is worse than an honest gap, because
  it reads as permission.

## Conflict order

When two sources disagree, the earlier entry wins:

1. Official Fiber documentation for the released major, and the tagged source it documents.
2. Official Go documentation.
3. Platform contracts: `/alaa-services-contract` for names and values,
   `/alaa-trust-gateway-auth` for trust semantics, and
   `/alaa-go-chi-development` for anything kit-governed.
4. `/alaa-golang` for Go depth and framework choice.
5. Vendored public Go skills.
6. Community examples, for reproducing a concrete symptom only - never as the basis for a rule.

A platform contract never loses to a framework default. Where Fiber's default and a value owned by
`/alaa-services-contract` disagree, the contract value is set explicitly
in `fiber.Config` and the disagreement is noted in the service's `docs/DECISIONS.md`.
