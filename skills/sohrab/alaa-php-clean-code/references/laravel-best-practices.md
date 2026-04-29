# Laravel clean-code and best-practice guidance

## Contents
- Container, contracts, and facades
- Laravel 13 upgrade and feature policy
- Requests, validation, and authorization
- Resources and serialization
- Eloquent query discipline
- Large dataset processing
- Events, jobs, listeners, and transactions
- Service providers and app structure
- Testing expectations

## Container, contracts, and facades

### Good defaults
- Let Laravel resolve concrete classes automatically when zero-configuration resolution works.
- Bind interfaces to implementations only when the abstraction is real.
- Use contextual binding or contextual attributes for per-consumer differences.
- Prefer constructor injection in classes that are likely to grow.
- Use facades mainly at framework edges or in small orchestration code where they remain clear.
- Avoid named arguments when calling Laravel framework methods unless the repository already made that trade-off intentionally and the surface is proven stable.

### Anti-patterns
- Binding every class into the container unnecessarily.
- Pulling dependencies from the container inside business logic.
- Letting a class accumulate many facades and responsibilities.
- Using facades as an excuse to avoid explicit dependencies in growing services.

## Laravel 13 upgrade and feature policy

### Baseline
- Treat Laravel 13 as the default framework target for new work in this skill pack.
- Pair Laravel 13 with PHP 8.5 unless the repository is pinned lower for a concrete compatibility reason.
- For 12 -> 13 upgrade work, start from the official dependency bumps:
  - `laravel/framework` -> `^13.0`
  - `laravel/boost` -> `^2.0` when installed
  - `laravel/tinker` -> `^3.0` when installed
  - `phpunit/phpunit` -> `^12.0` when installed
  - `pestphp/pest` -> `^4.0` when installed
- Compare framework-owned files against the Laravel 13 skeleton before preserving older bootstrap or config defaults.

### Mandatory audit points
- Replace direct references to `VerifyCsrfToken` or `ValidateCsrfToken` with `PreventRequestForgery` when touching middleware config, exclusions, or tests.
- Audit cache object storage against `cache.serializable_classes`; prefer non-object cache payloads unless an explicit allow-list is justified.
- Preserve Laravel 12 fallback cache or session names only with explicit `CACHE_PREFIX`, `REDIS_PREFIX`, and `SESSION_COOKIE` config.
- If the app listens to queue events, update `JobAttempted::$exceptionOccurred` to `JobAttempted::$exception` and `QueueBusy::$connection` to `QueueBusy::$connectionName`.
- Re-check domain route precedence, polymorphic pivot table names, `Container::call` nullable defaults, Bootstrap pagination view names, eager-loaded relation restoration in serialized collections, `Str` factory reset behavior in tests, and `Js::from` unicode expectations where those surfaces exist.
- If custom cache stores or repositories implement Laravel cache contracts, add support for the `touch` method.

### Laravel 13 feature usage policy
- Use `Queue::route(...)` when queue or connection selection by class would otherwise be repeated across the codebase.
- Prefer queue attributes such as `#[Tries]`, `#[Backoff]`, `#[Timeout]`, `#[FailOnTimeout]`, and `#[DeleteWhenMissingModels]` when they keep job policy clearer than scattered properties or repeated worker flags.
- Use first-party JSON:API resources only when the public contract is actually JSON:API; do not replace an existing stable non-JSON:API envelope by default.
- Treat Laravel AI SDK, semantic search, and vector search as opt-in capabilities. Do not introduce them unless the user asks for them or the repository already chose them, and route storage or indexing decisions through the relevant companion skills.

## Requests, validation, and authorization

### Good defaults
- Use Form Requests for complex validation and request authorization.
- Read validated data from `validated()` or `safe()`.
- Use policies for model or resource authorization.
- Use gates for non-model decisions such as dashboards, admin abilities, or capability checks.
- Keep controllers thin: receive validated input, call the service layer, return resources.
- Call repositories for persistence access; do not compose Eloquent/query-builder reads or writes in controllers.

### Anti-patterns
- Reading raw request input in services or repositories.
- Direct Eloquent/query-builder persistence in controllers.
- Putting validation rules in controllers or service methods when a Form Request is appropriate.
- Mixing authorization, validation, and persistence in one method.

## Resources and serialization

### Good defaults
- Use API Resources when the response contract matters.
- Use `whenLoaded()` and `whenCounted()` so resources do not trigger surprise queries.
- Keep response shaping in resources, not in controllers or models.

### Anti-patterns
- Returning raw models or collections when the public contract needs stability.
- Triggering relation access inside a resource without loading it first.
- Hiding heavy serialization logic in models.

## Eloquent query discipline

### Good defaults
- Treat eager loading as the default answer to N+1 risk.
- Use `with()`, `load()`, or `loadMissing()` intentionally.
- Use `withCount()`, `withExists()`, and targeted `select(...)` to reduce unnecessary work.
- Consider enabling `preventLazyLoading()` in local, test, or other safe non-production environments if the repo policy allows it.
- Keep query composition inside repositories, using dedicated query objects underneath when repository methods become hard to read.
- Services, jobs, listeners, commands, policies, actions, pipelines, and adapters must call repositories instead of composing Eloquent/query-builder persistence directly.

### Anti-patterns
- Direct Eloquent/query-builder reads or writes outside repositories, except model internals, migrations, factories, seeders, tests, resources reading already-loaded models, or framework glue.
- Accessing dynamic relationship properties inside loops without eager loading.
- Querying from accessors, resources, or casts in ways that hide extra IO.
- Pulling entire models when only a few columns are needed.

## Large dataset processing

### Choose the right tool
- `chunk()`
  - use for batched reads when you are not mutating the key that drives pagination
- `chunkById()`
  - use when the loop may update the same rows being iterated
- `lazy()`
  - use for memory-friendlier streaming where eager loading is not required
- `lazyById()`
  - use when you want lazy streaming and safe ID-based progress while mutating
- `cursor()`
  - use cautiously for one-model-at-a-time iteration
  - remember that it cannot eager load relationships
  - remember that PDO buffering can still make very large traversals expensive

### Anti-patterns
- Using `chunk()` or `lazy()` while updating the driving key or changing the query ordering semantics.
- Using `cursor()` when the code depends on eager-loaded relations.
- Materializing huge collections when a lazy approach is enough.

## Events, jobs, listeners, and transactions

### Good defaults
- Keep side effects decoupled from the main flow when they are slow or external.
- Use queued listeners and jobs for slow work.
- When queued work depends on committed rows, use `afterCommit()` or the queue connection's `after_commit` behavior.
- Keep transaction bodies short and free of external IO.
- Treat jobs and listeners as idempotent where retries are possible.

### Anti-patterns
- Dispatching queued work from inside transactions without commit-aware behavior when the work reads committed data.
- Doing heavy side effects inside the transaction body.
- Relying on unlimited retries or never-restarted workers.

For queue, broker, retry, and DLQ policy, switch to `alaa-async-messaging` or `alaa-laravel-job-rabbitmq`.

## Service providers and app structure

### Good defaults
- Keep service providers focused on wiring and registration.
- Make a provider deferrable when it only registers bindings and the repo benefits from deferred loading.
- When a repository targets Laravel 13, keep `bootstrap/app.php`, middleware registration, and related framework-owned bootstrap files aligned with the Laravel 13 skeleton unless the repo has an intentional override.
- Follow the repository's existing folder structure first.
- Use standard Laravel locations when there is no repo-specific rule:
  - HTTP controllers in `app/Http/Controllers`
  - Form Requests in `app/Http/Requests`
  - API Resources in `app/Http/Resources`
  - Policies in `app/Policies`
  - Providers in `app/Providers`
  - model factories in `database/factories`

### Anti-patterns
- Creating vague `Helpers`, `Utils`, or `Managers` folders as a dumping ground.
- Hiding business logic in service providers.
- Inventing a new top-level structure when the repo already has one.

## Testing expectations
- Add feature tests for endpoint behavior, authorization, and resource shape.
- Add unit tests for pure value objects, strategies, and other isolated logic.
- Add a regression test first for bug fixes when feasible.
- When the repo uses query-count assertions, use them to guard against accidental N+1 or query inflation.

Do not claim tests passed unless you actually ran them in the target environment.
