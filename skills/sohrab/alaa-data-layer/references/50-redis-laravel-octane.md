# Redis in Laravel 13 + Octane (integration, processing, and degraded mode)

Use this file when a Laravel 13.x service (PHP 8.5, Octane with Swoole or FrankenPHP) adds or changes Redis usage: cache, locks, rate limits, counters, dedupe, or sessions.

Verified baseline (2026-07): Laravel 13.x, phpredis 6.3.x (PECL), predis 3.5.x, Redis server 8.x. Re-verify with `references/source-map.md` when versions matter.

Policy difference vs Go: in Laravel, Redis is allowed for **both** DB-read caching **and** processing primitives (locks, rate limits, counters, dedupe, sessions, queues). In Go services Redis stays in front of DB queries only — see `51-redis-golang.md`.

## Step 0 — repository-pattern gate (mandatory, before any caching)

Do not add Redis caching to a service until the repository pattern is complete. Caching layered on scattered Eloquent calls cannot be invalidated correctly and will serve stale or cross-tenant data.

Verify all of these in the actual repo (not from docs) before writing cache code:

1. Every domain read/write used by the feature goes through a repository class (`<Store><Domain>Repository`, e.g. `PostgresCommentRepository`) behind an interface (e.g. `CommentRepositoryInterface`).
2. The interface is bound in a service provider `register()` method.
3. Controllers and services do not call Eloquent models or `DB::` directly for that domain.
4. Repository methods accept/return DTOs or models — not raw request arrays.

If any check fails: stop, report the gap, and complete the repository layer first using `$alaa-laravel-architecture` (layering, binding) and `$alaa-php-clean-code` (repository policy, decorator pattern). Only then add caching.

- ✅ Do: `CommentRepositoryInterface` → `PostgresCommentRepository` → add `CachedCommentRepository` decorator. Caching becomes one bounded class with clear invalidation points.
- ❌ Don't: sprinkle `Cache::remember()` inside controllers or services while some code paths still query the model directly. Those paths bypass the cache and its invalidation, so readers see a mix of fresh and stale data.

## Client and connection baseline

- Use **phpredis** (`REDIS_CLIENT=phpredis`) in production and under Octane. Use predis only when the extension cannot be installed; predis ≥ 3.4 supports retry/backoff via its `Retry` class.
- Configure client-level retry with jitter in `config/database.php` (phpredis): `max_retries`, `backoff_algorithm` (prefer `decorrelated_jitter`), `backoff_base`, `backoff_cap`. This is the first line of defense against transient drops and worker-recycle reconnects.
- Set explicit `timeout` (connect) and `read_timeout`. Defaults are too long for hot paths; a cache read that waits seconds is worse than a DB read. Choose values from your latency budget (typically well under 1 s for reads).
- Use **separate Redis connections** (and ideally separate logical databases or instances) for cache, sessions, queues, and locks. A `FLUSHDB` or eviction storm on one concern must not destroy the others.
- Set `prefix` per app + environment. Never share one unprefixed keyspace between services.
- With phpredis, prefer `options.serializer = igbinary` (or msgpack) and consider `compression = lz4`/`zstd` for large payloads; keep cached payloads small either way (IDs and DTO arrays, not object graphs).
- Cache eviction policy on the cache instance should be `allkeys-lru`/`allkeys-lfu`; never use an evicting policy on an instance that also stores queues or locks.

## Boot and register discipline (crash-safe placement)

Redis connections in Laravel are lazy — nothing connects until first use. The classic crash is a service provider touching cache/Redis during bootstrap: with Redis down, every request (or every Octane worker boot) throws and the app 500-loops.

- ✅ Do: keep provider `register()` to container bindings only. In `boot()`, wire events/routes/observers but do not read cache, sessions, or `Redis::`. If a provider needs a cached value, defer it with `$this->app->booting(...)`/lazy closures, or read at first use inside the consuming class with a fallback.
- ❌ Don't: `Cache::remember('settings', ...)` inside a provider `boot()`. With Redis unreachable this turns a cache outage into a total outage — and under Octane the worker can crash-loop before serving a single request.
- Wrap any unavoidable boot-time cache read in try/catch with a safe default, and log through the standard channel.
- Feature flags / settings needed on every request belong in a class that reads lazily with an in-request memo (`Cache::memo()`), not in provider boot.

## Where cache logic lives (decorator over the repository)

The caching seam is a **decorator** implementing the same repository interface:

```php
final class CachedCommentRepository implements CommentRepositoryInterface
{
    public function __construct(
        private readonly CommentRepositoryInterface $inner, // PostgresCommentRepository
        private readonly CacheRepository $cache,
    ) {}

    public function findByPublicId(string $tenantId, string $publicId): ?CommentDto
    {
        return $this->cache->remember(
            "comment:{$tenantId}:{$publicId}:v1",
            ttl: now()->addMinutes(10),
            callback: fn () => $this->inner->findByPublicId($tenantId, $publicId),
        );
    }

    public function update(CommentDto $dto): void
    {
        $this->inner->update($dto);                                       // truth first
        $this->cache->forget("comment:{$dto->tenantId}:{$dto->publicId}:v1"); // then invalidate
    }
}
```

Bind it in the provider so callers stay unchanged:

```php
$this->app->bind(CommentRepositoryInterface::class, function ($app) {
    return new CachedCommentRepository(
        $app->make(PostgresCommentRepository::class),
        $app->make('cache')->store(config('cache.default')),
    );
});
```

Rules:

- Postgres stays the source of truth; the decorator never contains business logic or query composition.
- Write methods always write to the DB first, then invalidate (delete) — do not write fresh values into the cache from the write path unless you have measured a reason (read-your-writes via delete is simpler and safer).
- Key shape follows `40-redis-verification-and-anti-patterns.md`: app/env prefix (from config), tenant, resource, id, version segment.
- The decorator is also where degraded mode lives (see below): if the cache store throws, call `$this->inner` directly.

## Cache-aside and stampede control

- Default read pattern: `Cache::remember(key, ttl, fn)` inside the decorator.
- Hot keys with tolerable staleness: `Cache::flexible(key, [fresh, stale], fn)` — serves stale within the window and refreshes after the response, removing synchronous recompute storms.
- Must-be-fresh expensive keys: lock-based dogpile control — `Cache::lock("build:{key}", ttl)->block(...)` or `Cache::withoutOverlapping(...)`; losers wait or serve the previous value.
- Same-request re-reads: `Cache::memo()` (per-request memo; scoped binding, so it resets per Octane request — safe).
- Add TTL jitter (± ~10%) on wide fan-out keys so they do not expire in the same second.
- Cache tags work on Redis but every tag set must stay tenant-scoped; prefer version-bump keys when tag bookkeeping cost is unclear.

## Redis beyond query caching (allowed in Laravel)

Unlike the Go lane, Laravel services may use Redis for processing primitives — with the same degraded-mode duty:

- **Atomic locks**: `Cache::lock()` with owner tokens; pass `$lock->owner()` to queued jobs and `Cache::restoreLock()` there; `$lock->refresh()` to extend mid-run. Short critical sections only — never long workflows.
- **Rate limiting**: `RateLimiter` facade with `'limiter' => 'redis'` in `config/cache.php`; for high-concurrency endpoints rely on the atomic return of `increment()` / `attempt()`. Concurrency caps: `Cache::funnel()`; overlap guards: `Cache::withoutOverlapping()`.
- **Idempotency / dedupe**: `Cache::add($idempotencyKey, ..., $ttl)` (atomic set-if-absent) at the edge; critical side effects (money/legal/audit) additionally need a DB unique constraint — Redis dedupe alone is not durable.
- **Counters / presence / ephemeral state**: fine with TTL and tenant-scoped keys; never as the only copy of business truth.
- **Sessions and queues**: Redis is a valid backend; queue/Horizon decisions belong to `$alaa-async-messaging` (and Horizon is forbidden for RabbitMQ workers — `$alaa-laravel-job-rabbitmq`).

## Invalidation and flush discipline

"Flush on time" means precise, event-driven invalidation — not global flushes.

- Invalidate at the write path: repository write methods (or domain events they emit) delete the exact keys and list/aggregate keys they affect. Every cached key must have a named owner and a named invalidation trigger; if you cannot name the trigger, do not cache it.
- Wide fan-out invalidation: bump the version segment (`:v1` → `:v2`) and let old keys expire via TTL.
- ✅ Do: `Cache::forget()` specific keys, tag-scoped flush of a tenant-scoped tag, or a version bump.
- ❌ Don't: `Cache::flush()`, `FLUSHDB`, or `FLUSHALL` in production code or deploy scripts. On a shared instance this wipes sessions, locks, and other services' data, and the cold-cache stampede can take the DB down.
- Deploys that change cached shapes: bump the version segment (or `CACHE_PREFIX`), never flush.
- TTL is the safety net, not the strategy: every key still gets a TTL so orphaned keys die on their own.

## Degraded mode — keep serving when Redis is down (mandatory)

Redis is an availability dependency only if you make it one. The service must keep serving (slower, degraded) with Redis completely unreachable.

1. **Cache**: set the default store to Laravel 13's `failover` driver — `CACHE_STORE=failover` with ordered stores, e.g. `['redis', 'array']` (or `['redis', 'database', 'array']` if a DB cache table exists). On Redis failure Laravel silently moves down the list and fires `Illuminate\Cache\Events\CacheFailedOver` — subscribe to it and alert; failover must be visible, not silent.
2. **What failover does NOT cover** — handle each explicitly:
   - Raw `Redis::` facade calls, locks, and `RateLimiter` on a Redis limiter still throw `RedisException` / `Predis\...\ConnectionException`. Wrap them: on connection failure, rate limiters **fail open** (allow the request, emit a metric), locks fall back to a DB-backed lock or to skipping the optimization — decide and document per call site; only fail closed where the lock guards correctness (then also back it with a DB constraint).
   - Sessions on Redis: an outage logs everyone out or 500s. Either accept and document it, or keep sessions on another store for services that must survive Redis loss.
   - Queues on Redis: producers throw on dispatch. Decide per job: try/catch with outbox/DB fallback, or accept the failure. (RabbitMQ-backed services are unaffected.)
3. **Decorator fallback**: the cache decorator catches store exceptions and calls the inner repository directly — a cache error must never surface to the caller:

```php
try {
    return $this->cache->remember($key, $ttl, $fetch);
} catch (\Throwable $e) {          // connection refused, timeout, serialization
    report($e);                     // once per burst; add a metric
    return $fetch();                // direct DB read — service stays up
}
```

4. **Fail fast, not slow**: short connect/read timeouts plus phpredis `max_retries` + `backoff_algorithm=decorrelated_jitter`. A hanging Redis must cost milliseconds, not seconds, per request. For long outages add a cheap circuit breaker (cached "redis-down-until" flag in the `array` store per worker) so every request does not pay the timeout.
5. **Boot safety**: with the boot/register discipline above, a Redis outage cannot prevent workers from booting.
6. **Recovery**: when Redis returns, the app resumes automatically (lazy connections + failover order). Expect a cold-cache stampede: `Cache::flexible` and dogpile locks on hot keys keep the DB safe during warm-up.
7. **Test it**: the DoD includes actually stopping Redis (`docker stop redis`) and verifying: requests still succeed (degraded), no worker crash-loop, alert fired, and recovery is clean when Redis restarts. An untested fallback is a rumor.

## Octane-specific rules

- Connections (DB and Redis) live as long as the worker. That is good for latency, but: do not capture a `Redis`/connection object inside your own singletons — resolve via the facade/manager per use so client retry/reconnect logic applies after worker recycles.
- Octane is known to leave Redis connections lingering after request termination (laravel/octane#1094). Watch `connected_clients` on the server; if it grows with uptime, add an `OperationTerminated`/`RequestTerminated` listener that disconnects the Redis manager, mirroring the commented-out DB disconnect in `config/octane.php`.
- Worker recycling (`--max-requests`) closes and reopens connections; phpredis `persistent` + `persistent_id` reduces reconnect cost across recycles.
- Size it: `workers × (Redis connections per worker)` must stay well under the server's `maxclients`, across all services sharing the instance.
- Swoole's `octane` store and `Octane::table()` are per-server, RAM-only complements — never a substitute for the shared Redis cache in multi-replica deployments.
- Never memoize cross-request state in statics/globals as a "free cache" — that is the Octane state-leak bug class; per-request memoization is `Cache::memo()`, cross-request caching is Redis. Details: `$alaa-octane-performance`.

## Verification / Definition of Done (Laravel + Redis)

In addition to the generic Redis DoD in `40-redis-verification-and-anti-patterns.md`, report:

1. Repository gate: evidence the repository layer was verified complete (or the gap that was fixed first).
2. Placement: which decorator(s) cache which repository methods; confirmation no controller/service calls Redis or `Cache::` for domain data directly.
3. Config: client (phpredis), retry/backoff values, timeouts, prefix, store separation (cache vs session vs queue vs locks).
4. Invalidation map: each cached key → the write path/event that invalidates it.
5. Degraded mode: failover store order, `CacheFailedOver` alerting, fail-open/fail-closed decision per lock and rate limiter, and the result of the stop-Redis test.
6. Octane: connection growth checked; no Redis usage in provider `register()`/`boot()`.

## Companion routing

- `$alaa-laravel-architecture` — repository interfaces, binding, layering (must be complete before caching).
- `$alaa-php-clean-code` — decorator pattern, repository policy, Octane-safe code shape.
- `$alaa-octane-performance` — worker lifecycle, connection reuse, memory behavior.
- `$alaa-async-messaging` / `$alaa-laravel-job-rabbitmq` — queues, Horizon boundaries, job middleware.
- `$alaa-security-review` — when cached data crosses tenant or trust boundaries.
