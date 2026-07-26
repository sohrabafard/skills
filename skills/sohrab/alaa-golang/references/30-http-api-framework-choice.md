# HTTP Framework Decision

Read the repository's `go.mod` and the user's current request, then apply the **first** row below that matches. There
is no judgment step in this table. Traffic volume, request rate, concurrency, latency target, and SLA figure are not
inputs to it and must not appear in your reasoning about it.

| Observed condition | Do this |
|---|---|
| `go.mod` requires `git.alaatv.com/vk/alaa-go-chi` **and** the user named Fiber in this request | Stop. Reply that the repository is a kit consumer, so its HTTP framework is a kit-owned surface and changing it is a governance decision, not a code change. Route the request through `/alaa-go-chi-development` (`$alaa-go-chi-development`) as a change request. Write no Fiber code unless the user, after reading that, instructs you to proceed anyway. |
| `go.mod` requires `github.com/gofiber/fiber/v2` or `github.com/gofiber/fiber/v3` | Fiber. Load `/alaa-golang-fiber` (`$alaa-golang-fiber`). |
| The user named Fiber in this request and no row above matched | Fiber. Load `/alaa-golang-fiber` (`$alaa-golang-fiber`). |
| The user asked for a prototype, spike, or benchmark and named Fiber as its subject, or the task is building a Fiber-specific kit | Fiber. Load `/alaa-golang-fiber` (`$alaa-golang-fiber`). |
| `go.mod` requires `git.alaatv.com/vk/alaa-go-chi` | chi, supplied by the kit's `httpkit`. Read `31-chi-api-guide.md`. |
| `go.mod` requires `github.com/go-chi/chi/v5` and does not require the kit | chi. Read `31-chi-api-guide.md`; treat the kit's server bounds and middleware chain as the target shape rather than as code you already have. |
| No row above matched, including a new service with no `go.mod` yet | The kit, and therefore chi. Read `31-chi-api-guide.md` and bootstrap the service through `/alaa-go-chi-development` (`$alaa-go-chi-development`). |

## Forbidden

**Forbidden:** selecting Fiber for a service that would otherwise be a kit consumer, on any grounds. The only channel
for that outcome is an owner decision recorded as a change request through `/alaa-go-chi-development` (`$alaa-go-chi-development`).

**Forbidden:** citing expected traffic, request rate, concurrency, p99 latency, or an SLA percentage as a reason for a
framework. Those are admission-control and capacity questions, and none of them is answered by the router library.
**Rule:** when a service's behaviour under load is in question, read `46-chi-under-load.md` — it states what the kit
already bounds, what it does not, and where each missing control is taken.

**Forbidden:** converting a service from chi to Fiber, or from Fiber to chi, as part of another task. **Rule:** perform
a framework migration only when the user asks for that migration in the current request; when a migration would help,
say so and stop.

**Forbidden:** adding a third HTTP router or web framework to an Ala Go repository. **Rule:** the two supported
routers are the kit's chi and Fiber; a service needing something neither provides files a change request through
`/alaa-go-chi-development` (`$alaa-go-chi-development`).

## Why this is settled, and on what date

Settled by the project owner on **2026-07-26**, replacing an earlier rule that routed "large, high-concurrency,
latency-sensitive, or SLA-heavy" services to Fiber.

That earlier rule failed on its own terms. The platform quality bar states that every Ala service carries an SLA above
99.99%, so "SLA-heavy" selected every service, and the rule read literally moved every new Go service off the shared
kit — the exact duplication the kit exists to end. The rule was also written before `alaa-go-chi` existed and never
mentioned it.

The kit is chi-based. A service on the kit inherits validated server bounds, a fixed middleware chain, a router that
refuses an unlabelled route, one error-envelope mapper, and a four-phase shutdown, none of which it has to write or
maintain. A service off the kit writes and maintains all of it alone, and every fix has to be made again in each copy.
That inheritance, not router throughput, is what decides the framework.

`alaa-golang-fiber` stays maintained for exactly two purposes the owner named: building or debugging a service that is
already Fiber, and a possible future Fiber-specific kit. It is not a capacity escape hatch.

Do not re-open this decision from a performance argument. If new evidence contradicts it, record the evidence and take
it to `/alaa-go-chi-development` (`$alaa-go-chi-development`) as a change request; do not resolve it inside a service.
