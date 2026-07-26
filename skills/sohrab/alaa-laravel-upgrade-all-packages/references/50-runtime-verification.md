# Post-Upgrade Runtime Verification

## When this file applies

Any one of these makes every check below mandatory:

- `config('octane.server')` is non-null, or a worker server is planned.
- The moved set includes `laravel/framework`, or a queue, cache, database, Redis or AMQP client.
- The moved set includes an HTTP client, a telemetry SDK, a Collector component, a logger, or a Sentry package.
- The moved set changes a `php` or `ext-*` platform requirement.

The reason is a runtime fact no test suite reproduces: under a long-lived worker the framework boots once and one process then serves many requests, so a dependency move changes worker-boot behaviour and connection lifetime, and a suite running one request per process never reaches the second request on a worker. Worker lifecycle, reload and drain semantics, the leak harness, connection lifecycle, worker sizing and cache tiers are owned by `/alaa-octane-performance` (`$alaa-octane-performance`). This file adds only what is specific to a dependency having just moved, and states no threshold of its own.

## 1. The worker boots

Start the runtime and confirm a worker serves one real request. A bump that changes a service provider's boot path, a deferred provider's registration, or an auto-discovery manifest fails here and nowhere else, because the test suite boots the framework differently and passes.

Proof level: `host-to-Docker smoke` at minimum, `in-runtime service proof` for a framework or server bump, named from `/alaa-controlled-ops` (`$alaa-controlled-ops`) `references/40-validation-and-release-gates.md`. The runtime comes up through `/service-runtime-kit-governance` (`$service-runtime-kit-governance`); a runtime that will not start is handled by the rule in `20-breaking-change-detection.md`.

## 2. The second request on the same worker

Send the same authenticated request repeatedly against a single worker and compare responses field by field, with attention to anything derived from identity: the authenticated subject, the tenant, the locale, the timezone, the permission or role set. Any drift between request 1 and request N is cross-request state and a hard failure of this gate, not a performance observation.

Two rules from the upstream `laravel-best-practices/` skill -- not owned by this repository, see `90-ownership-boundary.md` -- are actively wrong here and are overridden by name:

- `rules/caching.md` heads a section "Use `once()` for Per-Request Memoization". Under a long-lived worker the object lifetime of a service the worker resolved once **is the worker lifetime**, so `once()` on such a service is cross-request state: a `once()`-wrapped roles or permissions lookup returns request 1's authorization set to every later request on that worker. A bump that introduces, moves or newly memoizes such a lookup fails this gate.
- `rules/architecture.md` teaches `Context::add('tenant_id', $request->header('X-Tenant-ID'));`, taking tenant identity from an untrusted client header. Tenant derivation, trusted headers and JWT verification are `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`), which forbids it. After a bump touching request handling, authentication or the container, re-verify that tenant identity is still derived where that skill requires.

## 3. Memory behaviour

Compare steady-state worker RSS and the recycling rate against the pre-sweep baseline from `20-breaking-change-detection.md`. Growth per request the baseline did not show is a leak this bump introduced, and its regression test belongs in `/alaa-octane-performance` (`$alaa-octane-performance`) `references/leak-detection-harness.md`. No number appears here: the mechanism is that skill's and every platform value is `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`.

## 4. Connection lifetime

A database, Redis or AMQP client bump can change pooling, keepalive and reconnect behaviour without changing a call signature. Two observables:

- After an idle period longer than the server's idle timeout, the next request on the same worker still succeeds. A client that stopped reconnecting passes every test and fails the first quiet night in production.
- A forced dependency restart mid-run is followed by successful requests without a worker restart.

Deadline, retry and reconnect doctrine is `/alaa-reliability-sla` (`$alaa-reliability-sla`); every value is the contract file above; Redis under a long-lived worker is `/alaa-data-layer` (`$alaa-data-layer`) `references/50-redis-laravel-octane.md`, whose repository-pattern gate at "Step 0" applies before any caching change a bump forces.

## 5. Telemetry keeps its shape

A telemetry SDK, Collector component, logger or Sentry bump can rename a field, change a span name, alter a default sample rate or drop an attribute, and no test asserts on any of it. Emit one request through the upgraded stack and confirm every signal the service is required to emit is still present, still named the same, still the same type.

This file states neither which signals are required nor what they are called. Requirement levels and the gates that block a ship are `/alaa-observability-soc` (`$alaa-observability-soc`) `references/20-instrumentation-gates.md`; every field, metric, event and code name is `/alaa-services-contract` (`$alaa-services-contract`) `references/24-metric-registry.md` and `alaa-services-contract references/20-operational-and-observability-contract.md`. On conflict, SOC wins on whether a signal is required and the contract wins on what it is called. What this file owns is the trigger: a dependency move is itself an occasion to re-check the shape, which neither owner can know.

A changed default sample rate is the quiet case worth naming -- the signal is still present, dashboards still populate, and the tail the SLA depends on is gone.

## 6. New code is not live until workers restart

A worker holds the booted application, so an upgraded dependency is not serving traffic until workers are recycled, and neither is a revert. Drain semantics and the ordered deploy sequence are `/alaa-octane-performance` (`$alaa-octane-performance`) `references/worker-lifecycle-and-failure.md`, "Graceful deploy sequence". Report which worker generation the gate evidence came from; evidence from a pre-bump generation proves nothing about the bump.
