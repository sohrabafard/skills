# Redis in Laravel 13 + Octane (integration, processing, and degraded mode)

Read this when a Laravel service running under Octane adds or changes Redis usage: cache, locks, rate limits,
counters, dedupe, or sessions. The shared availability contract, cache key shape, TTL discipline, invalidation
policy, and the definition of done are in `40-redis-verification-and-anti-patterns.md`; this file adds the Laravel
and Octane mechanics and does not restate them.

Framework-version baseline recorded 2026-07 and **not re-verified in this session**: Laravel 13.x, phpredis 6.3.x,
predis 3.5.x, Redis server 8.x. Every framework API named below — `Cache::flexible`, `Cache::memo`, the `failover`
store, the `CacheFailedOver` event, `Cache::funnel`, `Cache::withoutOverlapping`, `Cache::restoreLock` — is
confirmed present in the service's installed version before it is written into code, through
`references/source-map.md`. Reason: a cache API that does not exist in the installed version fails at runtime on
the first request that reaches it, not at deploy.

Policy difference against the Go lane: in Laravel, Redis serves both database-read caching and processing
primitives — locks, rate limits, counters, dedupe, sessions, queues. A Go service on `alaa-go-chi` caches database
reads only; see `51-redis-golang.md`.

## Step 0 — repository-pattern gate (mandatory, before any caching)

Do not add Redis caching to a service until the repository pattern is complete for the domain being cached.
Reason: caching layered on scattered Eloquent calls cannot be invalidated correctly, because the call sites that
bypass the repository also bypass the invalidation, and readers then see a mix of fresh and stale rows with no
error raised anywhere.

Verify all four in the actual repository, by reading the code, before writing any cache code:

1. Every domain read and write used by the feature goes through a repository class
   (`<Store><Domain>Repository`, e.g. `PostgresCommentRepository`) behind an interface
   (e.g. `CommentRepositoryInterface`).
2. The interface is bound in a service provider `register()` method.
3. No controller and no service calls an Eloquent model or `DB::` directly for that domain.
4. Repository methods accept and return DTOs or models, not raw request arrays.

When any check fails: stop, report the gap, and complete the repository layer first through
`/alaa-laravel-architecture` (`$alaa-laravel-architecture`) for layering and binding and `/alaa-php-clean-code`
(`$alaa-php-clean-code`) for the repository policy and the decorator pattern. Add caching afterwards.

- Do: `CommentRepositoryInterface` → `PostgresCommentRepository` → add a `CachedCommentRepository` decorator, so
  caching is one bounded class with explicit invalidation points.
- Do not: scatter `Cache::remember()` through controllers and services while some paths still query the model
  directly.

## Client and connection baseline

- Use **phpredis** (`REDIS_CLIENT=phpredis`) in production and under Octane. Use predis only where the extension
  cannot be installed.
- Configure client-level retry with jitter in `config/database.php`: `max_retries`, `backoff_algorithm`
  (`decorrelated_jitter`), `backoff_base`, `backoff_cap`. This is what absorbs a transient drop and a
  worker-recycle reconnect. How many retries and how much backoff is `/alaa-reliability-sla`
  (`$alaa-reliability-sla`) `references/20-retries.md` for the doctrine, and `alaa-services-contract`
  `references/22-failure-load-and-deprecation-contract.md` for the values.
- Set explicit `timeout` (connect) and `read_timeout`; the driver defaults are far longer than any request budget.
  The values are the contract file's.
- Use **separate Redis connections**, and separate logical databases or instances, for cache, sessions, queues, and
  locks. Reason: a `FLUSHDB` or an eviction storm on one concern must not destroy the others.
- Set `prefix` per application and environment. An unprefixed keyspace shared between services produces
  cross-service key collisions that read as data corruption.
- With phpredis, prefer `options.serializer = igbinary` or msgpack, and compression for large payloads. Keep the
  payload small regardless: identifiers and DTO arrays, not object graphs.
- The cache instance's eviction policy is `allkeys-lru` or `allkeys-lfu`. Never set an evicting policy on an
  instance that also holds queues or locks, because eviction there silently drops work.

## Boot and register discipline

Redis connections in Laravel are lazy: nothing connects until first use. The classic outage is a service provider
that touches cache or Redis during bootstrap — with Redis down, every request throws, and under Octane the worker
crash-loops before serving anything.

- Keep provider `register()` to container bindings only. In `boot()`, wire events, routes, and observers, and read
  no cache, no session, and no `Redis::`.
- A provider that needs a cached value defers it with `$this->app->booting(...)` or a lazy closure, or reads it at
  first use inside the consuming class with a fallback.
- Do not call `Cache::remember('settings', ...)` inside a provider `boot()`. That converts a cache outage into a
  total outage.
- Wrap any unavoidable boot-time cache read in `try`/`catch` with a safe default and log through the standard
  channel.
- Feature flags and settings needed on every request live in a class that reads lazily with a per-request memo,
  not in provider boot.

## Where cache logic lives — a decorator over the repository

The caching seam is a decorator implementing the same repository interface:

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

- Postgres stays the source of truth. The decorator contains no business logic and composes no queries.
- A write method writes to the database first, then deletes the key. Do not write the fresh value into the cache
  from the write path unless a measurement says otherwise: a delete cannot publish a value the transaction later
  rolled back.
- Key shape follows `40-redis-verification-and-anti-patterns.md`.
- The decorator is also where degraded mode lives: when the cache store throws, call `$this->inner` directly.

## Cache-aside and stampede control

- Default read: `Cache::remember(key, ttl, fn)` inside the decorator.
- Hot keys with tolerable staleness: `Cache::flexible(key, [fresh, stale], fn)` serves stale inside the window and
  refreshes after the response, which removes the synchronous recompute storm.
- Must-be-fresh expensive keys: dogpile control with `Cache::lock("build:{key}", ttl)->block(...)` or
  `Cache::withoutOverlapping(...)`; losers wait or serve the previous value.
- Same-request re-reads: `Cache::memo()`, a per-request memo that resets per Octane request.
- Spread the expiry of wide fan-out keys with jitter; the jitter value belongs to `alaa-services-contract`
  `references/22-failure-load-and-deprecation-contract.md`, per the TTL rule in
  `40-redis-verification-and-anti-patterns.md`.
- Cache tags work on Redis, and every tag set stays tenant-scoped. Prefer a version-bump key where the tag
  bookkeeping cost is not measured.

## Redis beyond query caching (allowed in Laravel)

Unlike the Go lane, a Laravel service may use Redis for processing primitives, under the same degraded-mode duty:

- **Atomic locks**: `Cache::lock()` with owner tokens; pass `$lock->owner()` to a queued job and
  `Cache::restoreLock()` there; `$lock->refresh()` extends mid-run. Short critical sections only.
- **Rate limiting**: the `RateLimiter` facade with `'limiter' => 'redis'` in `config/cache.php`; on a
  high-concurrency endpoint rely on the atomic return of `increment()` or `attempt()`. Concurrency caps:
  `Cache::funnel()`. Overlap guards: `Cache::withoutOverlapping()`.
- **Idempotency and dedupe**: `Cache::add($idempotencyKey, ..., $ttl)` at the edge; a side effect involving money,
  legal record, or audit additionally needs a database unique constraint, because a Redis key can be evicted.
- **Counters, presence, ephemeral state**: acceptable with a TTL and a tenant-scoped key, never as the only copy
  of a business fact.
- **Sessions and queues**: Redis is a valid backend. Queue and Horizon decisions belong to `/alaa-async-messaging`
  (`$alaa-async-messaging`), and Horizon is forbidden for RabbitMQ workers per `/alaa-laravel-job-rabbitmq`
  (`$alaa-laravel-job-rabbitmq`).

## Invalidation and flush discipline

Precise, event-driven invalidation — never a global flush. The policy is in
`40-redis-verification-and-anti-patterns.md`; the Laravel mechanics are:

- Invalidate at the write path: a repository write method, or a domain event it emits, deletes the exact keys and
  the list or aggregate keys it affects.
- Wide fan-out: bump the version segment and let the old keys expire.
- Do: `Cache::forget()` on specific keys, a tenant-scoped tag flush, or a version bump.
- Do not: `Cache::flush()`, `FLUSHDB`, or `FLUSHALL` in production code or a deploy script. On a shared instance
  that wipes sessions, locks, and other services' data, and the cold-cache stampede that follows can take the
  database down.
- A deploy that changes a cached shape bumps the version segment or `CACHE_PREFIX`. It does not flush.

## Degraded mode — keep serving when Redis is down

The service keeps serving, slower, with Redis completely unreachable. The obligation and the fail-open versus
fail-closed question are in `40-redis-verification-and-anti-patterns.md`; below is how Laravel implements it.

1. **Cache**: set the default store to the `failover` driver — `CACHE_STORE=failover` with ordered stores such as
   `['redis', 'array']`, or `['redis', 'database', 'array']` where a database cache table exists. On failure
   Laravel moves down the list and fires `Illuminate\Cache\Events\CacheFailedOver`. Subscribe to that event and
   emit the fallback signal; a silent failover is an outage nobody is measuring.
2. **What failover does not cover**, each handled explicitly:
   - Raw `Redis::` facade calls, locks, and a Redis-backed `RateLimiter` still throw `RedisException` or
     `Predis\...\ConnectionException`. Wrap them, and decide per call site with the fail-open versus fail-closed
     question in `40-…`: a rate limiter in front of an ordinary endpoint fails open and emits a signal; a limiter
     guarding an abuse-critical surface fails closed and the decision is reviewed by `/alaa-security-review`
     (`$alaa-security-review`); a lock that guards correctness is additionally backed by a database constraint.
   - Sessions on Redis: an outage logs every user out or returns `500`. Either accept it and record that in the
     service's runbook, or keep sessions on another store.
   - Queues on Redis: producers throw on dispatch. Decide per job whether the dispatch falls back to an outbox row
     or the failure surfaces. A RabbitMQ-backed service is unaffected.
3. **Decorator fallback**: the decorator catches store exceptions and calls the inner repository, so a cache error
   never reaches the caller:

```php
try {
    return $this->cache->remember($key, $ttl, $fetch);
} catch (\Throwable $e) {          // connection refused, timeout, serialization
    report($e);                     // once per burst; emit the fallback signal
    return $fetch();                // direct DB read — the service stays up
}
```

4. **Fail fast, not slow**: short connect and read timeouts plus phpredis retry with decorrelated jitter, so a
   hanging Redis costs milliseconds per request rather than seconds. Whether a long outage additionally warrants a
   breaker, and how to shape it, is `/alaa-reliability-sla` (`$alaa-reliability-sla`)
   `references/30-breakers-and-bulkheads.md`; the values are `alaa-services-contract` `references/22-…`.
5. **Boot safety**: with the boot and register discipline above, a Redis outage cannot stop a worker from booting.
6. **Recovery**: lazy connections and the failover order restore caching automatically. Expect a cold-cache
   stampede; `Cache::flexible` and dogpile locks on hot keys are what keep the database standing during warm-up.
7. **Bound the origin load**: `alaa-services-contract` `references/22-failure-load-and-deprecation-contract.md`
   requires at most one origin computation per cache key in flight per instance, with later callers waiting on it
   until the deadline. That is what makes "fall back to the database" safe at production concurrency.

## Octane-specific rules

- Connections live as long as the worker. Do not capture a `Redis` or connection object inside your own
  singletons; resolve through the facade or manager per use, so client retry and reconnect logic applies after a
  worker recycle.
- Octane can leave Redis connections lingering after request termination (laravel/octane#1094). Watch
  `connected_clients`; if it grows with uptime, add a `RequestTerminated`/`OperationTerminated` listener that
  disconnects the Redis manager, mirroring the commented-out database disconnect in `config/octane.php`.
- Worker recycling via `--max-requests` closes and reopens connections; phpredis `persistent` with `persistent_id`
  reduces the reconnect cost across recycles.
- `workers × connections-per-worker` stays well under the server's `maxclients`, counted across every service
  sharing the instance. The connection ceiling itself is `/alaa-octane-performance` (`$alaa-octane-performance`).
- Swoole's `octane` store and `Octane::table()` are per-server, RAM-only complements, never a substitute for the
  shared Redis cache in a multi-replica deployment.
- Never memoize cross-request state in a static or a global as a free cache. That is the Octane state-leak bug
  class, owned by `/alaa-octane-performance`; per-request memoization is `Cache::memo()`, and cross-request
  caching is Redis.

## Definition of done (Laravel + Redis)

In addition to the shared list in `40-redis-verification-and-anti-patterns.md`, report:

1. Repository gate: the evidence that the layer was verified complete, or the gap that was closed first.
2. Placement: which decorators cache which repository methods, and confirmation that no controller or service
   reaches `Cache::` or `Redis::` for domain data.
3. Config: client, retry and backoff values, timeouts, prefix, and the separation of cache, session, queue, and
   lock connections.
4. Invalidation map: each cached key against the write path or event that invalidates it.
5. Degraded mode: the failover store order, `CacheFailedOver` alerting, the fail-open or fail-closed decision per
   lock and per limiter, and the result of stopping Redis.
6. Octane: connection growth checked, and no Redis usage in provider `register()` or `boot()`.

Which proof level each claim needs is `/alaa-testing-strategy` (`$alaa-testing-strategy`)
`references/40-proof-strength.md`. The decorator fallback is provable at level 2 with a throwing fake; item 5's
stop-Redis result is level 6 and is produced against a real Redis, stopped and restarted.

## Companion routing

- `/alaa-laravel-architecture` (`$alaa-laravel-architecture`) — repository interfaces, binding, layering.
- `/alaa-php-clean-code` (`$alaa-php-clean-code`) — decorator pattern, repository policy, Octane-safe code shape.
- `/alaa-octane-performance` (`$alaa-octane-performance`) — worker lifecycle, connection ceiling, memory behaviour.
- `/alaa-async-messaging` (`$alaa-async-messaging`), `/alaa-laravel-job-rabbitmq` (`$alaa-laravel-job-rabbitmq`) —
  queues, Horizon boundaries, job middleware.
- `/alaa-security-review` (`$alaa-security-review`) — cached data crossing a tenant or trust boundary.
