---
name: alaa-golang-fiber
description: "Fiber v3 work in Ala Go systems: building or debugging a service on github.com/gofiber/fiber/v3, app config and server bounds, fiber.Ctx value lifetime and copy rules, routing, middleware order, error mapping, binding and StructValidator, trusted proxy, probes, graceful shutdown, handler tests, and Fiber v2-to-v3 migration. Also holds the register of alaa-go-chi kit surfaces a Fiber service must re-implement, which is the input specification for a possible future Fiber kit. Use when a repo already imports Fiber, or when the project owner has recorded a Fiber exception. Do not use to pick a framework: alaa-golang reference 30-http-api-framework-choice.md owns that decision and alaa-golang owns general Go depth. A new Ala service is an alaa-go-chi kit consumer on chi unless the owner has recorded a Fiber exception through alaa-go-chi-development."
---

# Alaa Golang Fiber

## Charter

This skill exists for exactly two purposes, set by the project owner:

1. Building or debugging a service based on Fiber.
2. Serving as the input specification for a possible future Fiber-specific kit.

It is not a capacity-planning escape hatch and it is not a rival default. The kit
(`alaa-go-chi`) runs on chi. Read `references/50-kit-conflict-register.md` before proposing
any Fiber work that would otherwise be a kit consumer.

## Standing facts, verified 2026-07-26

State these to the user before writing Fiber code for an Ala service. They are facts, not
preferences, and an agent that omits them lets the user assume a precedent that does not exist.

- **No Ala service runs on Fiber.** The kit consumer registry (`docs/CONSUMERS.md` in the
  `alaa-go-chi` repository) lists `news`, `notif`, `entitlement-api`, `tusd` and `wa-api`. Every
  one is chi. The string "Fiber" appears zero times in the whole `alaa-go-chi-development`
  governance skill. A Fiber service on this platform has no production precedent; do not infer
  one from a neighbouring service's code, and do not copy a kit consumer's transport layer and
  assume the Fiber equivalent has been reviewed.
- **Choosing Fiber for a service that would otherwise be a kit consumer is the project owner's
  decision.** It is recorded as a change request through `/alaa-go-chi-development`
  (`$alaa-go-chi-development`). It is never an agent's decision, and never a conclusion drawn
  from a traffic estimate, a benchmark, or a latency target.
- **The framework-choice procedure is owned elsewhere.** `alaa-golang`
  `references/30-http-api-framework-choice.md` (`/alaa-golang`, `$alaa-golang`) is the single
  place that decides chi versus Fiber. This skill states no competing criteria. If you are being
  asked *which* framework to use, you are in the wrong skill: stop and read that file.

## When NOT to use

- You are choosing a framework for a new service. A new Ala service is a chi kit consumer unless the owner
  has recorded a Fiber exception, and that decision is owned elsewhere.
- The repository imports no Fiber and carries no recorded Fiber exception.
- The question is Go craft that would read the same on any HTTP framework. The router below names the owner.

## Router

Read the one file that matches what you are about to do. Do not preload the set.

| You are about to | Read |
| --- | --- |
| Create a `fiber.App`, set `fiber.Config`, set server timeouts or body limit, start or stop the listener | `references/10-fiber-v3-core.md` |
| Register routes, order middleware, mount probes, map an error to a status, configure CORS, a rate limiter, or `TrustProxy` | `references/20-routing-middleware-errors.md` |
| Change a request or response contract, bind a body, wire a `StructValidator`, or write a handler test | `references/30-validation-testing.md` |
| Ship, review, or harden a Fiber service: probes, shutdown, timeouts, concurrency, observability, security | `references/40-production-readiness.md` |
| Upgrade a repo from `github.com/gofiber/fiber/v2` to `/v3`, or read v2-era Fiber code and port it | `references/45-v2-to-v3-migration.md` |
| Decide what a Fiber service must build that a kit service inherits, or design a Fiber kit | `references/50-kit-conflict-register.md` |
| Answer a question that may belong to another skill | `references/55-skill-boundaries.md` |
| Assert any Fiber API name, signature, default, or version-sensitive behavior | `references/SOURCES.md` |

## Absolute rules

Each rule below is a constraint. None of them has an agent-granted exception. Where an exception
exists, the rule names who grants it and in what record.

- **Copy every `fiber.Ctx`-derived value before it outlives the handler.** Values from `Params`,
  `Query`, `Get`, `Body`, `Cookies` and their siblings are valid only inside the handler. Wrap
  each one in `utils.CopyString` or `utils.CopyBytes` at the point you take it. `Immutable` is a
  boot-time, service-wide `fiber.Config` decision made once by the service owner; it is never a
  reason to skip a copy at an individual call site. Details and the mechanism:
  `references/10-fiber-v3-core.md`.
- **Set `ReadTimeout`, `WriteTimeout` and `IdleTimeout` in `fiber.Config` on every service.** All
  three default to `0`, which means unbounded. An unset value is a slowloris-open server. Take the
  values from `/alaa-services-contract` (`$alaa-services-contract`); do not invent them.
- **Set `BodyLimit` in `fiber.Config` explicitly.** Its default is 4 MiB, which is larger than the
  platform's request cap.
- **Never cache an authorization decision.** An exception is granted by `/alaa-security-review`
  (`$alaa-security-review`) in a recorded decision that states the TTL, the invalidation trigger
  and the revocation path. Absent that record, resolve authorization per request.
- **Register `/api/health` and `/api/ready` before any auth, trust, gateway-proof or rate-limit
  middleware**, so a probe cannot be failed by a dependency of the thing it is probing.
- **Register every route before the listener starts.** Route-inventory and contract checks read the
  route table once at boot; a route added afterwards is invisible to them and ships unverified.
- **Retry only idempotent operations, under a bounded budget.** The retry, timeout, backoff and
  degradation doctrine is owned by `/alaa-reliability-sla` (`$alaa-reliability-sla`); the numbers
  are owned by `/alaa-services-contract` (`$alaa-services-contract`).
- **Keep `fiber` types out of `internal/domain`, `internal/application` and repository code.** The
  transport package converts; nothing below it imports Fiber.
- **Write or update a failing test before a behavior-changing edit**, then run the focused test,
  then `go test ./...`, and add `go test -race ./...` when the change touches shared state,
  caches, goroutines or workers.
- **Never edit anything under `vendor/`.**
- **Route model, reasoning-effort and runtime-capability questions to `/alaa-prompting-guide`
  (`$alaa-prompting-guide`).** Do not name a model in this skill or in work produced from it.

## Package layout

A Fiber service uses the same package layout as a kit service and differs only at the transport
adapter. Uniformity across the fleet outranks local optimality: an operator, a reviewer and an
auditor should be able to open any Ala Go service and find the same shape.

The layout itself is owned by `alaa-golang` `references/60-service-architecture-patterns.md`
(`/alaa-golang`, `$alaa-golang`): `internal/domain/`, `internal/application/` with its ports file,
`internal/infrastructure/composition/`, and a health service package. Read it there; this skill
does not restate it.

The Fiber-specific seam is one package: the transport adapter that owns the `*fiber.App`, its
`fiber.Config`, the middleware chain, route registration, request DTOs, and the `ErrorHandler` that
renders the platform error envelope. Everything that package exposes inward is a plain Go type or a
`context.Context`.

## Maintenance rules

- Keep this file routing-first. Detail belongs in `references/`.
- Every Fiber API name, signature or default asserted anywhere in this skill carries a source URL
  and a verification date, per `references/SOURCES.md`. An unsourced API claim is a defect.
- State each instruction exactly once across the whole skill. If a rule needs to be visible in two
  places, put it in one and link the other.
- Write cross-skill references in both trigger forms, `/skill-name` and `$skill-name`, and name
  the owning skill beside any path you point at.
- Keep this skill ASCII-only unless a source path or product name requires otherwise.
