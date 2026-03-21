# Laravel clean-code and best-practice guidance

## Contents
- Container, contracts, and facades
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

### Anti-patterns
- Binding every class into the container unnecessarily.
- Pulling dependencies from the container inside business logic.
- Letting a class accumulate many facades and responsibilities.
- Using facades as an excuse to avoid explicit dependencies in growing services.

## Requests, validation, and authorization

### Good defaults
- Use Form Requests for complex validation and request authorization.
- Read validated data from `validated()` or `safe()`.
- Use policies for model or resource authorization.
- Use gates for non-model decisions such as dashboards, admin abilities, or capability checks.
- Keep controllers thin: receive validated input, call the service layer, return resources.

### Anti-patterns
- Reading raw request input in services or repositories.
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
- Keep query composition close to repositories or dedicated query objects when it grows.

### Anti-patterns
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
