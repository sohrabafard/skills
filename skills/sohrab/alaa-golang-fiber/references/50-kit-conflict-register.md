# Kit Conflict Register

Read this file when you are deciding what a Fiber service must build that a kit service gets for
free, or when you are designing the Fiber-specific kit the project owner named as this skill's
second purpose.

This is the register that justifies the skill's existence. It is written from the `alaa-go-chi`
source, verified **2026-07-26**. It is also the input specification for a Fiber kit: every row is a
capability that kit would have to own, and the last section states the design tension that decides
whether owning it is possible at the performance level Fiber is chosen for.

Kit governance, the phase gate, and the change-request procedure are owned by
`/alaa-go-chi-development` (`$alaa-go-chi-development`). Nothing here authorizes kit work.

## Read this first

Every surface below is `net/http`-shaped. `alaa-go-chi` is built on chi, and chi is a router over
`net/http`; its middleware are `func(http.Handler) http.Handler`, its handlers are
`http.HandlerFunc`, its binder takes an `*http.Request`. Fiber is built on `fasthttp` and shares
none of those types.

So a Fiber service does not "use the kit with a different router". It re-implements each surface, or
it adapts each surface and pays the adaptation cost. The register makes that concrete so the choice
is priced rather than assumed.

## The register

| Surface | What a chi service inherits from the kit | What a Fiber service must build | Cost |
| --- | --- | --- | --- |
| `httpkit` middleware chain | A fixed, ordered chain composed once: recover, correlation, span, access-log/metrics, body-cap. Order is not a service decision, so no service can get it wrong. | The same five layers as Fiber middleware, in the order fixed by `20-routing-middleware-errors.md`, composed in one function so a route cannot opt out. | Moderate to write; high to keep correct. Order drift across services is invisible until an incident, because each service still "has middleware". |
| `httpkit` family-first router | Route registration only through `Trusted`, `Anonymous`, `ProviderFacing`, `Operational`. A route with no declared family does not enter the table: `ErrUnlabeledRoute`. `NewRouter` panics at boot on a nil or typed-nil posture, because a nil posture would run trusted families with no enforcement. | A Fiber registration wrapper that refuses an unlabeled route and fails closed on a missing posture. Fiber's `app.Get` and friends are directly callable, so the wrapper must be the only sanctioned path and a lint or review rule must enforce it. | High. This is the single largest safety gap. On chi the guarantee is structural; on Fiber it degrades to a convention that a one-line `app.Get` bypasses. |
| `httpkit` server bounds | `ReadTimeout` 10s, `WriteTimeout` 30s, `IdleTimeout` 120s, `MaxBodyBytes` 1 MiB, read from validated environment keys and clamped at boot to a permitted range, with `ReadHeaderTimeout` derived from `ReadTimeout`. | The same values into `fiber.Config`, plus the boot-time validation and clamping, plus `Concurrency`, which has no `net/http` counterpart. See `10-fiber-v3-core.md`. | Low to write, high if skipped. All three Fiber timeouts default to `0`, so an omission is unbounded rather than merely non-standard. |
| `httpkit.Bind[T]` | Requires the JSON content type, wraps the body in `http.MaxBytesReader` at the configured cap, calls `DisallowUnknownFields`, and rejects a second JSON document in the same body. One generic function, used everywhere. | A Fiber bind helper adding all four checks around `c.Bind().JSON`. Fiber's binder does none of them; `BodyLimit` caps size only. See `30-validation-testing.md`. | Low to write, easy to under-build. The most likely partial implementation checks size and stops, leaving unknown-field and content-type acceptance wide open. |
| `trustkit` | `TrustCtx` as the typed trust context, the four route postures, gateway proof by constant-time comparison, and fail-closed parsing: a nil permission map panics at boot rather than denying quietly. | The whole surface, over `fiber.Ctx`, satisfying the same contract, with the trust context carried in the request context rather than in `Locals`. | High, and security-critical. This is where a re-implementation is most likely to fail open under a malformed header, which is the exact failure the kit design exists to prevent. |
| `errkit` | One mapper from any Go error to the canonical envelope and status. Codes are append-only. A code not in the finalized known set renders as `INTERNAL`, and the set is fail-closed until boot finalizes it. | The same mapper behind `fiber.Config.ErrorHandler`, plus the code registry and its fail-closed default. See `20-routing-middleware-errors.md`. | Moderate. The registry is the part usually skipped, and skipping it turns any internal code string into a public API contract the first time it renders. |
| `readykit` | `/api/health` and `/api/ready` envelopes, a check registry with stable ordering, three severities (`required`, `degraded`, `informational`), and one shared collector serving both the HTTP routes and the ops CLI. Health never runs a dependency probe. | The same registry and collector, plus Fiber route handlers. Fiber's bundled healthcheck middleware uses different paths and a different body shape, so it is not a shortcut. | Moderate. The severity model and the single shared collector are the parts that get dropped, and dropping them produces a readiness endpoint that disagrees with the ops CLI. |
| `runkit` | The standard process roles as subcommands (`serve`, `consume`, `dispatch`, `relay`, `migrate`, `seed`, `topology`, `ops`, `routes`) and the four-phase ordered shutdown - `stop_intake`, `drain_workers`, `flush_buffers`, `close_pools` - on a 30s budget. | The same role set and the same shutdown ordering, with Fiber's `ListenConfig.GracefulContext` and `ShutdownTimeout` wired into phase one and two. See `10-fiber-v3-core.md`. | Moderate. Mostly transport-independent, which makes this the cheapest surface to port and the best candidate to share between a chi kit and a Fiber kit unchanged. |
| `obskit` | Correlation field injection, bounded log and span-attribute budgets with enforced floors and ceilings so no configuration can strip kit-owned fields, sampling, and metric exemplars. | Correlation middleware satisfying the platform contract on every response including both probes, plus the same budget enforcement. The released `github.com/gofiber/contrib/v3/otel` supplies server spans but not correlation. See `40-production-readiness.md`. | Moderate. The span half is now off-the-shelf; the correlation and budget halves are not, and they are the parts the platform's dashboards and SOC routing actually depend on. |
| `contracttest` | Black-box conformance assertions a service runs against itself: trust boundary, error envelope, readiness, and route inventory. Conformance is proven, not asserted in prose. | The same assertions against a Fiber app. The suite drives the service over HTTP, so much of it ports; the fixtures that construct requests and inspect the router do not. | Moderate, and the highest-leverage item on this list. Without it, every other row is a claim rather than a verified property. |
| `apicontractkit` | The route inventory as the single truth behind the OpenAPI 3.1.0 document and the Postman collection, with probe fixtures. Documentation cannot drift from the router because it is generated from it. | A route-inventory extractor over Fiber's route table feeding the same generator. Fiber exposes its routes, so the extractor is feasible; the family and posture metadata the generator needs does not exist unless the family-first router row above was built. | Moderate, and strictly downstream of the router row. Build the router wrapper first or this cannot exist. |

## The load-bearing tension

Fiber v3 can adapt `net/http` middleware. `github.com/gofiber/fiber/v3/middleware/adaptor` exposes
`HTTPMiddleware(mw func(http.Handler) http.Handler) fiber.Handler` and
`HTTPHandler(h http.Handler) fiber.Handler`, among others
(https://docs.gofiber.io/middleware/adaptor, verified 2026-07-26). Every kit middleware in the
register above has exactly that shape, so on paper the whole chain can be adapted and reused.

The docs price it: "Adapted `net/http` handlers still run with standard library semantics. They
don't have access to `fiber.Ctx`, and the compatibility layer comes with additional overhead
compared to native Fiber handlers."

That overhead is the `net/http` allocation path - constructing an `http.Request`, an
`http.ResponseWriter` and their headers per request - which is precisely the cost Fiber exists to
avoid. So the choice collapses to two honest options and one dishonest one:

1. **Re-implement each surface natively on `fiber.Ctx`.** Keeps the performance argument intact.
   Costs the whole register above, and creates a second implementation of every security-critical
   contract that must be kept in step with the chi one, forever.
2. **Adapt the kit surfaces through `adaptor`.** Costs almost nothing to build and inherits every
   contract correctly. Reintroduces the `net/http` allocation path on the request hot path, which
   removes the reason Fiber was chosen.
3. **Adapt the surfaces and still claim Fiber's performance profile.** This is the failure mode to
   name explicitly, because it is the path of least resistance and it produces a service that is
   slower than the chi equivalent while carrying a second framework's operational surface.

A Fiber kit is only worth building if option 1 is worth its cost for a specific, measured workload.
That measurement - a benchmark of the real service shape, with the real middleware chain, against
the chi equivalent - is the first deliverable of any Fiber kit proposal, not a step to be taken
after the design is agreed.

State this tension to the project owner whenever Fiber is proposed for a service that would
otherwise be a kit consumer. It is the substance of the decision, and it is his to make.

## Using this file as the Fiber kit specification

If the owner commissions a Fiber kit, the register is its scope, and the following are its
acceptance criteria rather than aspirations:

- **The router row is the first milestone and gates the rest.** Until an unlabeled route cannot
  enter the table and a missing posture fails the boot, nothing built on top of it can be trusted,
  and `apicontractkit`'s Fiber equivalent cannot exist at all.
- **`contracttest` ports before the surfaces it tests are considered done.** A surface is complete
  when the conformance suite proves it, not when it compiles.
- **`runkit` is shared, not forked.** It is the one surface in the register that is essentially
  transport-independent. A Fiber kit that forks the process roles and the shutdown phases creates
  two operational vocabularies for one platform, and the operator pays for that every incident.
- **`errkit`, `readykit` and the trust contract are shared at the contract level even where the
  implementation differs.** The envelope shape, the code registry semantics, the readiness severity
  model and the trust context's meaning are platform contracts owned by `/alaa-services-contract`
  (`$alaa-services-contract`) and `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`). A Fiber
  kit implements them; it does not redefine them.
- **Every surface carries a benchmark against its chi equivalent.** The kit exists to buy
  performance. A surface that does not measurably do so should adapt the chi implementation through
  `adaptor` instead, and the register should record that it did.
