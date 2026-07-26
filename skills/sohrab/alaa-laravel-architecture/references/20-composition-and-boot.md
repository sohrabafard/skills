# Composition and boot — the seam, the binding, and why placement is an availability property

## Every repository is an interface plus a store-named implementation

The interface is what makes the layer substitutable: it is what a test replaces, and it is the only surface a cache decorator can wrap without any caller changing.

```php
interface CommentRepositoryInterface
{
    public function findByPublicId(string $tenantId, string $publicId): ?CommentData;
    public function create(CommentData $data): CommentData;
}

final class PostgresCommentRepository implements CommentRepositoryInterface { /* data access only */ }
```

```php
public function register(): void
{
    $this->app->bind(CommentRepositoryInterface::class, PostgresCommentRepository::class);
}
```

A Service depends on the interface. A Service that names a concrete repository cannot be given a decorated, faked, or re-pointed implementation, so the seam exists in the type system only.

Which call sites must go through a repository at all is `/alaa-php-clean-code`'s (`$alaa-php-clean-code`) mandatory repository policy, whose wording is the authority. Whether a domain's repository layer is **complete enough to cache** is decided by the mandatory "Step 0 — repository-pattern gate" in `alaa-data-layer references/50-redis-laravel-octane.md`. Neither test is restated here.

## The cache seam sits on the interface, and nowhere else

Caching is a decorator implementing the same repository interface and wrapping the store implementation. It is bound in place of the store implementation, so no caller learns that caching exists:

```php
$this->app->bind(CommentRepositoryInterface::class, function ($app) {
    return new CachedCommentRepository(
        $app->make(PostgresCommentRepository::class),
        $app->make('cache')->store(config('cache.default')),
    );
});
```

This skill owns **where the seam sits**. Three consequences follow from the location alone:

1. Controllers, Services, and Resources never call `Cache::` or `Redis::` for domain data. There is no branch on cache state anywhere above the interface, so there is no path that reads around the cache and no path that forgets to invalidate.
2. The decorator holds no business rule and no query composition. A rule inside the decorator executes only on a cache miss, which makes the service's behaviour depend on cache state.
3. The decorator is the only place a cache failure is caught, which is what makes `references/40-degraded-mode.md` implementable in one class.

**Cache policy is not owned here.** Key design, TTL, invalidation strategy, write-versus-delete on the write path, stampede control, and Redis-down cache behaviour are `alaa-data-layer references/50-redis-laravel-octane.md`'s, and it wins on all five.

Binding the decorator for a domain whose repository layer is incomplete produces cache entries that no write path invalidates. That is the defect in `references/50-failure-recovery.md`, "Stale reads behind a bypassed decorator" — and the reason the enable flag in `references/70-config-contract.md` defaults to off.

## `register()` and `boot()` — placement decides whether the service starts

This is not a style split. A provider that performs I/O converts a dependency outage into a *boot* failure, and a process that cannot boot cannot serve the degraded response it was designed to serve. Under a long-lived worker it is worse: the worker crash-loops before answering a single request, so the outage is total rather than partial.

**`register()`** holds container bindings only: `bind`, `singleton`, `scoped`, contextual bindings, and config merging. It resolves no service — a service resolved here is constructed before the providers it depends on have finished registering — and it reads no config value another provider may still change.

**`boot()`** holds wiring only: event-to-listener bindings, route model bindings, observers, gates and policies, macros, publishing.

**Neither performs I/O.** No cache read, no `Redis::`, no database query, no HTTP call, no filesystem read.

### Work that seems to need to happen early

- **Needs a resolved service at bootstrap:** wrap it in an `$this->app->booting(...)` or `$this->app->booted(...)` closure so it runs late and lazily. Resolution inside a binding closure is already deferred and is correct.
- **Needs a stored or cached value on every request:** read it at first use inside the consuming class, not in a provider. On failure, return the declared default from `references/70-config-contract.md` **and emit the fallback signal in `references/60-telemetry-surfaces.md` on every fallback taken.** A silent default turns a cache or config outage into a response that is wrong and looks healthy — which is undetectable, and therefore worse than the outage.
- **Only registers bindings and is heavy:** declare it deferrable, so the container constructs it on first resolution instead of on every boot. Provider placement is this skill's ground; the container API that carries it is framework-owned, and `references/source-map.md` names the source to confirm it against.

### The observable that decides compliance

Stop Redis and the database, start the application's workers, and issue a request. **Every worker boots and the service answers** — with the responses `references/40-degraded-mode.md` specifies, which for most routes is a failure envelope rather than a success. A provider that prevents a worker from booting has its work in the wrong place, whatever the work is.

`scripts/architecture-gate.sh` checks `L4-provider-io` and `L5-provider-resolve-in-register` fail a build on the mechanical forms of both defects.
