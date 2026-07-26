# Degraded mode — where the response is produced when a dependency is gone

`/alaa-reliability-sla` (`$alaa-reliability-sla`) owns **why** a path degrades or fails. `alaa-services-contract references/10-core-service-contract.md` owns the envelope's keys, and that same skill's `references/22-failure-load-and-deprecation-contract.md` owns every status, code, event name, and value. This file owns **which class in a Laravel tree produces the answer**, which is the part that decides whether two agents implementing the same outage produce the same response.

## One producer

**A failure or degraded response is produced in exactly one place: the framework exception handler, from a domain exception a Service raised.** No Controller assembles one, no Service returns one as data, no middleware invents one for a route group.

The reason is not tidiness. An envelope assembled at each call site diverges at each call site, and the divergence is invisible until a client branches on a field one endpoint omits — see `references/50-failure-recovery.md`, "Envelope drift between endpoints". One producer also means one place attaches the correlation headers required by `alaa-services-contract references/50-laravel-copy-baselines.md`.

Consequences that are checkable:

- A Service signals failure by throwing a typed domain exception carrying the code, not by returning `null`, `false`, an empty collection, or an array with an `error` key. A `null` return is indistinguishable at the Controller from "no such row", so the Controller must guess, and two Controllers guess differently.
- A Controller has no `catch` for a dependency failure. A `catch` in a Controller is how a `503` becomes a `200` with an empty list.
- The handler maps exception to status and code. It does not decide policy; it renders the decision the Service already made.

## The three classes of unreachable dependency

For each, the *values* are the contract's and the *doctrine* is `/alaa-reliability-sla`'s `references/50-degradation.md`. What follows is placement only.

### The database is unreachable

The store implementation's failure surfaces at the repository interface. Nothing above it converts that failure into a success.

- The Repository lets the failure propagate, or wraps it in a typed exception that names the store. It does not return an empty result: an empty result means "no rows", and a read that cannot reach the store knows nothing about rows.
- A Service does not serve a stale cached value in place of a read whose answer must be current. Whether a given route's answer may be stale is a decision `/alaa-system-design` (`$alaa-system-design`) records, not one the Service makes at runtime.
- No layer retries in-process without the deadline and budget from the contract file.

### Redis, or whatever backs the cache, is unreachable

- **The failure is caught in the cache decorator and nowhere else.** The decorator calls the inner repository and the request proceeds. This is the whole reason the seam is where `references/20-composition-and-boot.md` puts it: one `catch`, in one class, for the entire domain.
- No Service, Controller, or Resource carries a branch on cache availability, because a branch there is a second degraded behaviour that no test covers.
- The bound on origin load during a cache outage, and the fallback's own policy, are `alaa-data-layer references/50-redis-laravel-octane.md`'s "Degraded mode" section; the request remains inside the deadline in the contract file.
- Every fallback taken emits the signal in `references/60-telemetry-surfaces.md`. A cache outage that produces correct-looking responses and no signal is invisible until the bill or the latency graph shows it.

### The broker or publisher is unreachable

- The Service's business transaction commits together with its outbox row. A broker that is down does not fail a write that has already been authorized and validated — `references/30-events-and-outbox-seam.md`.
- **What the caller sees depends on how the route classifies the side effect, and the route declares that classification where the route is registered** — not per call site inside a Service. A Service that decides per call whether a publish failure is fatal produces two behaviours for one route across two code paths.
- The classification is `required` or `deferred`; which statuses, codes, and events each produces is fixed in `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`, "When a dependency is unreachable". Which one a given dependency is follows the gate-versus-contributor discriminator owned by `/alaa-security-review` (`$alaa-security-review`): when the dependency cannot answer, does proceeding without it let through something that must not get through? Yes, it is a gate and fails closed; no, it is a contributor and fails open.
- An authorization or entitlement dependency is never compensated for locally: no cached previous allow, no local projection used as an authorization input.

## The response that is forbidden in all three cases

**A success body missing a field the contract promises.** There are exactly two legal outcomes: the field is documented optional and its absence is a normal success, or the route fails with the error envelope. A `200` whose body silently lacks a promised field is a contract violation that every client discovers at a different time, and it is the failure mode that "degraded where necessary" produces when nobody wrote down what degraded means.

Which fields may be absent is part of the route's contract, recorded where `/alaa-system-design` (`$alaa-system-design`) records it and named by `/alaa-services-contract` (`$alaa-services-contract`).

## Readiness

A dependency this service can serve product traffic without is not reported as required by readiness, or a transient blip on an optional dependency removes a healthy instance from rotation. The readiness envelope's shape and its `required` flag are `alaa-services-contract references/10-core-service-contract.md`'s; the key that sets the flag per dependency is in `references/70-config-contract.md`.
