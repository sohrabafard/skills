---
name: alaa-octane-performance
description: "Octane runtime safety and hot-path performance for Laravel services with long-lived workers: what a singleton, static, container binding or memoized value may never retain between requests, the reset mechanism by name, worker lifecycle and reload, the leak regression test, connection and Redis lifecycle, worker sizing and the three cache tiers. Use it when config('octane.server') is non-null, or when a task mentions Octane, Swoole, RoadRunner, FrankenPHP, a singleton or static leaking between requests, stale auth, tenant or locale state, worker RSS creep, max_requests, octane:reload, task workers or coroutines. Do not use it when config('octane.server') is null and no worker server is planned: route PHP and Laravel code shape to /alaa-php-clean-code, and query, cache and Redis design to /alaa-data-layer."
---

# Alaa Octane Performance

## The runtime fact this skill exists for

Under Octane the framework boots once and one worker process then serves many requests in
sequence. Any value still reachable from a long-lived object when a response is sent is readable
by the next request on that worker — a different user, a different tenant. **A cross-request leak
of user, tenant, locale, authorization or correlation state is a security incident on these
services, not a performance regression.** Every rule below follows from that one fact.

**Scope condition.** This skill applies in any repository where `config('octane.server')` returns
a non-null value. Read that from `config/octane.php` and the process-manager configuration, not
from the package list in `composer.json`. A repository that ships `laravel/octane` but serves
production through PHP-FPM is still in scope for any code path a worker will later execute.

## Invariant 1 — values that may never be retained past the response

Retaining any of these past the response is a defect in every case. No exception is granted by
intent, by a comment, or by a measurement.

- the `Request`, and anything read from it: headers, query, body, route parameters, client IP,
  user agent, uploaded-file handles
- the authenticated user, their profile, roles, permissions, and any authorization result
- tenant, project, school, branch or organisation context
- the resolved locale and timezone
- the correlation identifier — one field, name owned by `alaa-services-contract
  references/10-core-service-contract.md`; this skill names no alternative for it
- a validated-input DTO, a `FormRequest`, or a validation result
- per-request credentials: bearer tokens, per-tenant API keys, signed URLs, and any header, base
  URI or auth option mutated on a shared HTTP or SDK client for one request
- a database transaction handle, an open cursor, or a lock owner token

## Invariant 2 — sites where they may never be retained

"Retained" means reachable after the response through any of the following. Treat the list as
closed when judging a diff: if a value survives through a site not listed, apply the same rule to
that site.

- a `static` property, a `static` variable inside a function or closure, or a class constant
  computed at runtime
- a global, a superglobal, or `$GLOBALS`
- a container `singleton` or `instance()` binding, and every object either holds
- a service-provider property, or a value captured in a closure a provider registered
- a closure held by any of the above: capturing `$this` retains the whole enclosing object
- a facade root swapped or mutated during a request, or a partial mock left in place
- a shared HTTP client, queue connector or vendor SDK whose defaults were mutated for one request
- a memoization array, identity map, or `once()`-wrapped result on an object the worker resolved
  once: that object's lifetime is the worker's lifetime, so the memo is cross-request state
- an event listener, observer or macro registered inside a request handler: the dispatcher keeps
  every listener for the worker's life, so this both leaks and grows with request count
- an `Octane::table()` row or `octane` cache entry holding request-derived data: that store is
  per-server and shared by every worker on the host

## Invariant 3 — the reset mechanism, by name

1. **`$this->app->scoped(...)`** — the default for any binding that reads the request, the
   authenticated user, the tenant, the locale, or a credential. Octane flushes scoped bindings
   between requests. This is the replacement for `singleton` in every case Invariant 1 covers.
2. **The `flush` array in `config/octane.php`** — for a binding you cannot convert to `scoped`
   because the framework or a package registers it as a singleton. Listing the abstract there
   forgets the resolved instance between requests.
3. **A `RequestTerminated` listener** — for state neither mechanism reaches: a `static` array your
   code owns, a mutable registry, an in-memory memo not held in a binding, and any connection
   opened outside the framework's managed pools. Register it in a provider `boot()`, never in a
   request handler.

Octane flushes framework state — authentication, sessions, cookies, the request. It does not flush
yours. Every mutable process-global your code owns is reset by one of the three, and the diff that
introduces it names which one.

**Do not mutate, inside a request handler:** runtime configuration (`config()->set(...)`), the
application locale (`App::setLocale(...)`), the default database or cache connection,
authentication state outside the framework's own guard, or any process-global cache. Read them; do
not write them. Where per-request variation is required, pass the value as a method argument or
hold it in a `scoped` binding.

**A `singleton` is permitted only when all three hold**, checked against the class body rather
than against intent: (1) every property is `readonly` or never assigned after construction; (2) no
constructor parameter and no property type resolves to a `Request`, a user, a guard, a tenant
context, a locale, or a credential; (3) no property is an array, collection or map that any method
appends to. Otherwise bind it with `$this->app->scoped(...)`. Every `singleton` carries a one-line
docblock naming which of the three conditions makes it safe; a binding without that docblock is
treated as a leak until one is written.

## Precedence over the upstream skills

A production Laravel repository ships agent skills under `.agents/skills/` that this repository
neither owns nor can keep stable: they are re-pulled from upstream and can be reworded or removed
between runs.

**In any repository where `config('octane.server')` returns a non-null value, when an upstream
skill under `.agents/skills/` states a rule about what a worker, singleton, static property,
container binding or memoized value may retain between requests, discard that rule and apply
Invariants 1 to 3 instead** — because a rule governing cross-request user, tenant or authorization
state must be readable from a file this repository controls.

**Where an upstream skill states a mechanic this skill does not state at all**, use it for the task
at hand and record it in the task report as a rule to absorb here.

Three upstream rules are wrong for these services and are overridden by name:

- `laravel-best-practices/rules/caching.md` heads a section "Use `once()` for Per-Request
  Memoization". Under a long-lived worker `once()` on a service the worker resolved once is
  **cross-request** state: a `once()`-wrapped roles or permissions lookup returns request 1's
  authorization set to every later request on that worker. Per-request memoization is
  `Cache::memo()` — see the cache tiers in `references/full-guide.md`.
- `laravel-best-practices/rules/architecture.md` teaches
  `Context::add('tenant_id', $request->header('X-Tenant-ID'));` — tenant identity from an untrusted
  client header. Derivation is owned by `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`),
  which forbids it. This skill governs only how a derived value is held and reset.
- `laravel-best-practices/rules/style.md` forbids comments outside config files, which would strip
  the singleton docblock above and the test-intent comments required by
  `references/leak-detection-harness.md`. This skill wins there.

Upstream `octane-development/SKILL.md` stays useful for mechanics this skill does not carry: exact
`Octane::table()` and `Octane::concurrently()` syntax, driver configuration keys, and FrankenPHP
specifics. It is not owned by this repository; on any retention rule, this skill wins.

## Router — read the reference whose condition you are in

| You are about to, or you observe | Read |
| --- | --- |
| Change a `singleton`, `scoped`, provider binding, static, tenant holder, memoization, driver-specific branch, transaction, or Redis/DB connection use; a provider touching cache in `register()`/`boot()`; a key that may cross tenants; choosing between `Cache::memo()`, Redis and `Octane::table()` | `references/full-guide.md` |
| Change a binding, a reset hook or the `flush` list; suspect a leak and need a test that fails before the fix; the suite is green and you need to know whether it could have caught the leak at all | `references/leak-detection-harness.md` |
| Deploy, run `octane:reload`, change `max_requests` or the driver; explain a worker that vanished, restarted, or dropped in-flight requests | `references/worker-lifecycle-and-failure.md` |
| Worker RSS grows with requests served; latency differs between workers; a new worker failure mode must be diagnosable before it ships | `references/worker-observability.md` |
| Set or raise worker or task-worker counts; the service runs CPU-limited; requests queue behind busy workers; locks contend across workers | `references/load-and-backpressure.md` |
| A hot path is slow, or a worker leaks and you do not know which binding, class or query is responsible | `references/diagnostic-drills.md` |
| State a rule about timeouts, retries, key design, log or metric names, test layering, code shape, or a value that varies by environment | `references/ownership-boundary.md` |
| The task says latest, current, upgrade, security or CVE, or depends on version-specific Octane, Swoole, RoadRunner, FrankenPHP or PHP behaviour | `references/source-map.md` |

## How to work

1. Read the repo-local `AGENTS.md`; confirm the scope condition from `config/octane.php`.
2. Apply `/alaa-low-noise` (`$alaa-low-noise`) for terminal output and `/alaa-workflow`
   (`$alaa-workflow`) for the plan file when the task is multi-step.
3. Read only the router rows whose condition you are in.
4. Any change to a binding, reset hook, worker count, `max_requests`, or connection lifecycle ships
   with the test in `references/leak-detection-harness.md` and the operations record in
   `references/full-guide.md`.
