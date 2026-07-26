# Laravel craft this skill owns

## What this file is for

A production Laravel repository ships an upstream agent skill at `.agents/skills/laravel-best-practices/` — `SKILL.md` plus 21 `rules/` files, **not owned by this repository**, re-pulled periodically, removable between runs. Route there for framework mechanics with worked examples: subqueries and indexes (`rules/advanced-queries.md`, `rules/db-performance.md`), queue retry and uniqueness (`rules/queue-jobs.md`), HTTP-client timeout and pooling (`rules/http-client.md`), migration hygiene (`rules/migrations.md`), scheduling flags (`rules/scheduling.md`), error-reporting plumbing (`rules/error-handling.md`), container and facade defaults (`rules/architecture.md`), Form Requests and `validated()` (`rules/validation.md`), folder conventions (`rules/style.md`).

It is **entirely Octane-unaware** — zero mentions of Octane, Swoole, RoadRunner, singletons, or static properties across all 22 files — and silent on repositories, idempotency, and `whenLoaded()`. This file holds only what upstream does not, plus the overrides where upstream is wrong for these services.

## Contents
- Boost as the first inspection layer
- Laravel 13 audit points
- Repository-first persistence
- Partial updates (PATCH semantics)
- Resources and serialization
- Large-dataset traversal
- Transactions, idempotency, and the run-twice proof
- Tests
- Overrides of the upstream skill

## Boost as the first inspection layer

`laravel/boost` exposes Laravel-aware inspection and documentation tools. **Check availability by a command, not by feeling:** run `composer show laravel/boost` (or read `composer.json`); if it resolves, check whether `boost`-prefixed MCP tools are present in the session's tool list.

When both hold, use Boost as the **first** inspection layer before making any assumption about installed packages, schema, routes, config, or runtime — it reads the actual application rather than a guess. When either fails, inspect the repository directly and say so.

Boost tells you what the application *is*. It does not decide anything: explicit user instructions, repo-local rules, this skill, and any triggered companion skill remain the governing source for code shape, naming, refactor mode, and contract preservation.

## Laravel 13 audit points

The dependency bumps and skeleton comparison belong to `/alaa-laravel-upgrade-all-packages` (`$alaa-laravel-upgrade-all-packages`). These points outlive the upgrade and apply whenever you touch the surface named:

- Replace direct references to `VerifyCsrfToken` or `ValidateCsrfToken` with `PreventRequestForgery` when touching middleware config, route exclusions, or tests.
- Cache payloads are arrays and scalars. A class-typed payload requires the class to be listed in `cache.serializable_classes`; add a name to that list only as a recorded interim step while an existing class-typed payload is migrated to arrays, never as the default, and never widen it to a wildcard.
- Laravel 12-era generated cache or session names survive only through explicit `CACHE_PREFIX`, `REDIS_PREFIX`, and `SESSION_COOKIE` config. Do not assume an old framework fallback still applies.
- Code listening to queue events uses `JobAttempted::$exception` (was `$exceptionOccurred`) and `QueueBusy::$connectionName` (was `$connection`).
- Re-check, where the surface exists: domain route precedence, polymorphic pivot table names, `Container::call` nullable defaults, Bootstrap pagination view names, **eager-loaded relation restoration in serialized collections**, `Str` factory reset behavior in tests, and `Js::from` unicode expectations.
- A custom cache store or repository implementing a Laravel cache contract must implement `touch`.
- Do not pass named arguments to Laravel framework methods: parameter names are not covered by Laravel's backwards-compatibility promise.
- `Queue::route(...)` and the queue attributes `#[Tries]`, `#[Backoff]`, `#[Timeout]`, `#[FailOnTimeout]`, `#[DeleteWhenMissingModels]` replace repeated properties or worker flags when they make job policy clearer in one place.
- Laravel 13 attribute-based model/component configuration is adopted repo-wide as a deliberate convention or not at all — never mixed per-file with property-based configuration.
- First-party JSON:API resources are used only where the public contract actually is JSON:API. Do not replace an existing stable envelope with one.
- Laravel AI SDK, semantic search, and vector search are opt-in. Introduce one only when the user asks or the repository already chose it, and route the storage or indexing decision to `/alaa-data-layer` (`$alaa-data-layer`).

## Repository-first persistence

This is the layering law, stated at language level. The gate itself is in `SKILL.md`.

- **Services, jobs, listeners, commands, policies, actions, pipelines, and adapters call repositories. They do not compose Eloquent or the query builder.** Controllers do not either: a controller receives validated input, calls the service layer, and returns a resource.
- Query composition lives inside repositories, with a dedicated query object underneath when a repository method stops being readable.
- **Allowed exceptions — the complete list.** Direct Eloquent or query-builder use is correct, not a violation, in: Eloquent model relationship definitions; scopes, casts, and accessors that belong on the model; migrations; factories; seeders; test fixtures and database assertions; API Resources reading an already-loaded model; and framework glue where Laravel requires the model API. Nothing else.
- **Enable `Model::preventLazyLoading()` outside production.** `Model::preventLazyLoading(! app()->isProduction())` in `AppServiceProvider::boot()` is the one mechanical guard that turns an unnoticed N+1 into a failing test before it reaches production, so it is on. If the repository deliberately has it off, that is a finding to report, not a reason to leave it off silently.
- A query hidden inside an accessor, a cast, or a resource is a query nobody reading the call site can see. Accessors, casts, and resources do not perform IO.

Eager-loading mechanics, column selection, `withCount()`/`withExists()`, and index choice: upstream `rules/db-performance.md` and `rules/advanced-queries.md`. Whether a growing path needs a bound at all: `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`).

## Partial updates (PATCH semantics)

- Decide field by field **by key presence**: `$request->has('title')`, `array_key_exists()` on `validated()`, or `$request->safe()->only(...)` restricted to keys actually sent.
- A legitimate `0`, `false`, `''`, or `null` sent by the client **must overwrite**; an omitted field **must keep** the current value. `$data['x'] ?? $model->x` breaks the first rule and is the single most common silent data-loss bug in a PATCH handler.
- Where the contract distinguishes *clearing* a field from *not touching* it, encode absent-versus-null in the DTO explicitly — an optional wrapper, a sentinel, or separate presence flags. A nullable property alone cannot express both.

## Resources and serialization

Response shaping lives in an API Resource, never in a controller and never in a model. Do not return a raw model or collection where the public contract must stay stable, and do not hide heavy serialization logic in a model. The mandatory relation-and-count guard is in `SKILL.md` under Laravel defaults; envelope and field naming belong to `/alaa-services-contract` (`$alaa-services-contract`).

## Large-dataset traversal

Upstream `rules/db-performance.md` and `rules/collections.md` own the enumeration of `chunk`, `chunkById`, `lazy`, `lazyById`, and `cursor` with examples. Two facts they do not carry:

- **When the loop may update the rows it is iterating, `chunkById()` or `lazyById()` is required.** `chunk()` and `lazy()` page by OFFSET, so a row the loop mutates shifts the window and rows get skipped or processed twice — silently, with no error.
- **`cursor()` is not free of memory pressure.** PDO buffers the full result set by default, so a very large traversal can still exhaust memory even though only one model is hydrated at a time; and `cursor()` cannot eager-load, so relation access inside the loop is an N+1.

## Transactions, idempotency, and the run-twice proof

- **Transaction bodies stay short and contain no external IO.** An HTTP call, a queue dispatch, or a file write inside a transaction holds a database connection for the duration of someone else's outage.
- **Idempotency is a contract, not a hope.** Retries, redeliveries, and re-runs are the normal consequence of an at-least-once queue and of crash recovery, so code that is only correct when run once is incorrect. Use natural-key upserts (`updateOrCreate`, an `ON CONFLICT`-shaped operation) rather than a bare insert for any re-runnable write.
- **Prove it with a run-twice test.** Run the job, listener, consumer, or seeder twice against the same state and assert the second run is a no-op: same end state, no duplicate row, no duplicate side effect. A re-runnable unit without this test is unproven.

The idempotency contract itself and the retry doctrine belong to `/alaa-reliability-sla` (`$alaa-reliability-sla`); the values to `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`; queue and broker mechanics to `/alaa-async-messaging` (`$alaa-async-messaging`) and `/alaa-laravel-job-rabbitmq` (`$alaa-laravel-job-rabbitmq`), with upstream `rules/queue-jobs.md` for framework mechanics.

## Tests

`/alaa-testing-strategy` (`$alaa-testing-strategy`) owns every test *decision*: what makes a test a test, which layer a behaviour belongs at, whether a double is honest, the proof level a claim reaches, and whether an intermittent failure is a product defect or a broken test. It deliberately owns no framework construct, which leaves Pest and PHPUnit idiom to this skill. Three conditions govern that split:

1. **Pest syntax, `test()`/`it()` choice, dataset form, `arch()` form, browser-test form, and runner flags come from the upstream `pest-testing` skill** at `.agents/skills/pest-testing/SKILL.md` — not owned by this repository. Follow it for syntax.
2. **The database-refresh decision does not come from `pest-testing`.** That file never mentions `LazilyRefreshDatabase`; its sibling upstream `laravel-best-practices/rules/testing.md` does, and prefers it over `RefreshDatabase`. Use `LazilyRefreshDatabase` unless the suite needs a migration on every run, and state which you chose.
3. **Upstream's "do not remove tests without approval" does not survive contact with `/alaa-testing-strategy`**, which requires a test that passes both with and without the mechanism it claims to protect to be repaired or deleted in the same change. On that conflict `/alaa-testing-strategy` wins, and the repair or deletion is named in the report.

Two PHP-side obligations this skill owns outright:

- **A bug fix starts with a failing test that reproduces the bug.** Write the reproduction first and watch it fail against the unfixed code. If you cannot make it fail, you have not located the bug — stop and report what is missing rather than changing code and hoping.
- **Where the repository has query-count assertions, a changed read path carries one.** It is the only assertion that catches an N+1 or query inflation reintroduced by a later refactor.

For a leak-prone Octane change, the regression test and what it must assert belong to `/alaa-octane-performance` (`$alaa-octane-performance`).

## Overrides of the upstream skill

Upstream `laravel-best-practices/` is not owned by this repository. Where it contradicts the rules below, the named owner wins and upstream is overridden by name:

| Upstream rule | Why it is wrong for these services | Owner that wins |
|---|---|---|
| `rules/architecture.md`, "Use `Context` for Request-Scoped Data": `Context::add('tenant_id', $request->header('X-Tenant-ID'));` | Derives tenant identity from an untrusted client header, in a form an agent will copy verbatim. Tenant identity comes from the verified gateway assertion, never from a raw request header. | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| `rules/caching.md`, "Use `once()` for Per-Request Memoization" | Mislabelled under a long-lived worker: `once()` memoizes for the *object's* lifetime, and the object lifetime of a service the worker resolved once **is the worker lifetime**. A `once()`-wrapped roles or permissions lookup returns request 1's authorization set to every later request that worker serves. Memoize per request only inside an object the request itself created, and key it by tenant. | `/alaa-octane-performance` (`$alaa-octane-performance`) |
| `rules/style.md`, "No Unnecessary Comments" — comments only in config files | Would strip the invariant docblocks, side-effect notes, and test-intent comments this pack requires. Extract-and-name still applies to a comment explaining *what* unclear code does; a comment stating *why* — an invariant, a provider quirk, a unit or timezone assumption — stays. | `documentation-and-artifacts.md` in this skill |
