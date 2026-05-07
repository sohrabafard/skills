# Redis Cache Layer

Use this file when a Go service uses Redis as a cache for database-backed data.

## Core rule

Redis is a cache layer, not the source of truth, unless the repository explicitly says otherwise.

The database owns correctness. Redis improves latency, reduces database load, and helps absorb read traffic.

## Default pattern: cache-aside

Use cache-aside by default:

1. read from Redis
2. on hit, return cached value
3. on miss, read from DB through repository
4. store a serialized DTO in Redis with TTL
5. return the DB result

Keep this behind a use case, repository decorator, or cache abstraction. Do not call Redis directly from handlers.

## Key design

Use typed key builders:

```go
func UserByIDKey(projectID, userID string) string {
    return "v1:project:" + projectID + ":user:" + userID
}
```

Rules:

- include a version prefix
- include tenant/project scope when relevant
- normalize raw input before using it in keys
- avoid unbounded key cardinality
- document the data owner and invalidation rule

## TTL policy

- volatile data: short TTL
- stable reference data: longer TTL
- negative cache entries: very short TTL
- add jitter to avoid synchronized expiry
- do not use infinite TTL unless invalidation is proven

## Invalidation

After writes:

- update or delete affected cache keys
- invalidate list/query caches that include the changed entity
- use versioned keys when exact invalidation is too complex
- use event-driven invalidation only when event reliability and replay are designed

## Stampede protection

Protect expensive misses:

- use `singleflight` for in-process duplicate suppression
- use Redis locks only when cross-instance suppression is worth the complexity
- keep lock timeouts short
- never let lock failure corrupt correctness

## Error policy

Cache read failure usually falls back to DB. Cache write failure usually logs and increments metrics but does not fail the request.

Fail the request only when the cache is explicitly contract-critical.

## Security rules

- Do not cache secrets, tokens, passwords, or raw credentials.
- Do not cache authorization decisions unless TTL, invalidation, and revocation behavior are explicit.
- Do not use client-controlled values as trusted cache scopes.
- Avoid logging full keys if they contain user or tenant identifiers.

## Observability

Record:

- cache hit count
- cache miss count
- cache error count
- cache latency
- DB fallback count
- invalidation count
- stampede suppression count when used

## Tests

Required tests:

- cache hit
- cache miss
- stale or expired value
- invalidation after write
- Redis down fallback
- serialization failure
- concurrent miss behavior

Use fakes for unit tests. Use real Redis or Testcontainers only when behavior depends on real Redis semantics.
