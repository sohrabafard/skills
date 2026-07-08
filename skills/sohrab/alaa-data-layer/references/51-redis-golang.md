# Redis in Go services (DB-query cache only, resilient client, degraded mode)

Use this file when a Go service (Go 1.26 era) adds or changes Redis usage.

Verified baseline (2026-07): `github.com/redis/go-redis/v9` v9.21.x (platform default client), `golang.org/x/sync/singleflight`, `sony/gobreaker/v2` v2.4.x, `go-redsync/redsync/v4`, Redis server 8.x. Re-verify with `references/source-map.md` when versions matter.

Pattern authority: `alaa-golang` → `references/61-redis-cache-layer.md` owns cache-aside, key design, TTL, invalidation, stampede, and cache tests for Go. This file adds the platform data-layer policy, client configuration, and the degraded-mode contract. Do not restate 61 — load it.

## Platform policy — cache DB reads, not computation

Go is fast enough that recomputation is almost never the bottleneck; the database is.

- ✅ Do: use Redis as cache-aside in front of repository DB reads (hot lookups, expensive aggregates, high-QPS list heads). Postgres stays the only source of truth.
- ❌ Don't: cache function results, rendered payloads, or business computation outputs whose inputs are already in memory. In Go the recompute is cheaper than the network hop, and every extra cached shape adds an invalidation liability.
- Coordination primitives (locks, rate limits, idempotency keys) are separate, deliberate uses — allowed when the design needs cross-instance coordination, under the rules in `61-redis-cache-layer.md` and `40-redis-verification-and-anti-patterns.md`. They are not "caching" and must not be introduced casually.
- This differs from Laravel, where Redis also serves processing paths (sessions, queues, funnels) — see `50-redis-laravel-octane.md`.

## Repository boundary gate (mandatory)

Same gate as every platform service: caching attaches to the repository seam, never to handlers.

1. The read being cached goes through a repository interface (port) owned by the use case (P5, `$alaa-golang-clean-code-principles`).
2. The cache lives in a repository decorator or the use case — handlers never import the Redis client (`alaa-golang` reference 60/61).
3. If the repository layer is incomplete, stop and finish it first via `$alaa-golang` before adding cache code.

## Client configuration (go-redis v9)

Defaults are tuned for generic workloads, not hot paths. Set these explicitly:

```go
rdb := redis.NewClient(&redis.Options{
    Addr:            cfg.RedisAddr,
    // Fail fast: a cache read must cost milliseconds even when Redis is sick.
    DialTimeout:     1 * time.Second,          // don't go below ~1s on cloud networks
    ReadTimeout:     300 * time.Millisecond,   // from your latency budget
    WriteTimeout:    300 * time.Millisecond,
    // Retries with backoff for transient blips (defaults: 3, 8ms→512ms).
    MaxRetries:      3,
    // Pool: default PoolSize is 10×GOMAXPROCS; size from measured concurrency × latency.
    PoolSize:        cfg.RedisPoolSize,
    MinIdleConns:    cfg.RedisMinIdle,          // avoid cold-dial bursts on spiky traffic
    ConnMaxIdleTime: 5 * time.Minute,
    // PoolTimeout defaults to ReadTimeout+1s — with a bounded pool this is the
    // backstop that turns a hung Redis into a fast error instead of goroutine pileup.
})
```

- Pass a per-call `context.WithTimeout` from the request context; never call Redis with `context.Background()` on a request path.
- Monitor `rdb.PoolStats()` (Hits, Misses, Timeouts, TotalConns) — `redis: connection pool timeout` means slow commands or an undersized pool; fix the cause, don't just raise PoolSize.
- Sizing: `replicas × PoolSize` must stay well under the server's `maxclients` across all services sharing the instance.
- `rueidis` (auto-pipelining, server-assisted client-side caching) is opt-in for extreme-QPS read paths only when the repo explicitly adopts it; go-redis v9 stays the default (`alaa-golang` reference 40).

## Degraded mode — Redis down must not take the service down (mandatory)

The request path must survive a full Redis outage by falling through to Postgres. Cache errors are logged and counted, never returned.

1. **Classify errors first**: `errors.Is(err, redis.Nil)` is a miss (normal). Everything else (dial errors, `context.DeadlineExceeded`, pool timeout) is a cache failure → read from the DB through the inner repository.

```go
func (r *CachedUserRepo) ByID(ctx context.Context, tenantID, id string) (User, error) {
    val, err := r.rdb.Get(ctx, userKey(tenantID, id)).Result()
    switch {
    case err == nil:
        if u, ok := decodeUser(val); ok { return u, nil } // decode failure → treat as miss
    case !errors.Is(err, redis.Nil):
        r.metrics.CacheFallback.Inc() // real failure: count it, fall through
    }
    u, err := r.inner.ByID(ctx, tenantID, id) // DB is the source of truth
    if err != nil { return User{}, err }
    r.setAsync(u) // best-effort SET with its own short timeout; errors only logged
    return u, nil
}
```

2. **Protect the DB during the outage**: with the cache gone, all reads hit Postgres. `singleflight` around the DB load collapses concurrent misses per key per instance — this is what makes "just fall back to the DB" safe at high concurrency.
3. **Stop paying the timeout on long outages**: wrap Redis calls in a circuit breaker (`sony/gobreaker/v2`). Open circuit → skip Redis entirely (straight to DB + singleflight); half-open probes restore caching automatically. Use `IsExcluded` (or equivalent) so caller-side `context.Canceled` does not trip the breaker.
4. **Never block startup on Redis**: construct the client lazily/optimistically; readiness may report Redis state, but liveness and serving must not require it. `Ping` belongs in a background health loop feeding the breaker and metrics, not in `main()` as a fatal check.
5. **Writes during outage**: cache SETs and invalidation DELs are best-effort. Because keys are versioned and TTL-bounded (61), a missed invalidation heals by TTL — that is why every key must have a TTL.
6. **Observability**: emit cache_hit / cache_miss / cache_error / db_fallback / breaker_state metrics (`alaa-golang` 61 vocabulary). A silent fallback that doubles DB load is an incident waiting to be discovered late.
7. **Test it**: unit-test the fallback with a failing fake; integration-test by stopping Redis (Testcontainers) and asserting requests still succeed and the DB sees singleflight-collapsed load. The stop-Redis test is part of the DoD.

- ✅ Do: treat every Redis error except `redis.Nil` as "cache unavailable → use DB", with metrics.
- ❌ Don't: `return err` from a repository read because a cache GET failed — that converts a cache outage into a service outage.
- ❌ Don't: retry Redis in a loop on the request path. The client already retries with backoff; beyond that, fail over to the DB.

## Locks and rate limits (when the design truly needs them)

- Locks: `SET key value NX PX` semantics via `redsync/v4` or raw commands with owner token + check-and-del release. Redis locks are for efficiency (skip duplicate work), not correctness — no fencing tokens exist; correctness-critical exclusion belongs in Postgres (unique constraints, `FOR UPDATE SKIP LOCKED`) per `30-concurrency-projections-and-pooling.md`.
- Rate limits: Lua-based GCRA/sliding-window (e.g. `go-redis/redis_rate/v10` — functional but dormant since 2023; pin and review) or server-side primitives on Redis ≥ 8.8 (`INCREX`). On Redis failure rate limiters fail open with a metric unless the limit guards abuse-critical surface — then document the fail-closed choice.
- Both must define behavior when Redis is down, same as the cache path.

## Verification / Definition of Done (Go + Redis)

In addition to the generic Redis DoD in `40-redis-verification-and-anti-patterns.md` and the test list in `alaa-golang` 61, report:

1. Confirmation that caching fronts DB reads only (no computation caching), attached at the repository decorator/use-case seam.
2. Client config: timeouts, pool sizing rationale, per-call context deadlines.
3. Degraded mode: error classification, singleflight placement, breaker settings, startup independence, and the result of the stop-Redis test.
4. Metrics wired: hit/miss/error/fallback/breaker.

## Companion routing

- `$alaa-golang` — reference 61 (cache authority), 60 (repository seam), 40 (package catalog).
- `$alaa-golang-clean-code-principles` — P5 (no Redis imports in domain/application), P12 (boundary tests).
- `$alaa-observability-soc` — metric and alert vocabulary for fallback/breaker signals.
