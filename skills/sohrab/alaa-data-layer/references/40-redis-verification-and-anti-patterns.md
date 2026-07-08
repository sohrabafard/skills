# Redis patterns (cache, locks, rate limiting) for high throughput
Use Redis deliberately for caching, rate limiting, and distributed coordination.
Redis is fast, but memory is finite; design keys and TTLs as a first-class schema.

Language lanes (load the one that matches the service):
- Laravel 13 + Octane integration, processing uses, and degraded mode: `50-redis-laravel-octane.md`
- Go services (DB-query cache only, client config, degraded mode): `51-redis-golang.md`

Both lanes share the availability contract below.

## Availability and degraded mode (mandatory)
Redis is an optimization, not an availability dependency. Every design that adds Redis must answer: "what happens when Redis is slow, flapping, or completely down?"

Baseline rules for every service, any language:
- A cache read/write error must never fail the request; fall through to the source of truth (DB).
- Short connect/read timeouts + bounded retries with jitter; a sick Redis must cost milliseconds, not seconds.
- No hard Redis dependency at process startup or framework boot; connections stay lazy and probe failures stay non-fatal.
- Locks and rate limiters must have a documented fail-open or fail-closed decision per call site; correctness-critical exclusion is backed by DB constraints, never by Redis alone.
- Fallback must be observable: a metric/alert fires when the service is running without its cache.
- Cold-cache recovery is designed (stampede control), not hoped for.
- The stop-Redis test is part of the Definition of Done: stop Redis, verify the service still serves, then verify clean recovery.

## Cache key design (mandatory)
Use namespaced, tenant-aware keys. Recommended shape:
- `{app}:{env}:{tenant}:{resource}:{id}:{version}`
  Example:
- `comment-service:prod:project_123:thread:01J...:v1`

Rules:
- Always include tenant in multi-tenant caches.
- Always include a version segment (`v1`, `v2`) to enable safe “version bump” invalidation.
- Normalize high-cardinality inputs (avoid raw URLs/user agents as-is).

## TTL discipline (mandatory)
- Every cache key MUST have an explicit TTL.
- Prefer short TTLs for volatile data.
- If correctness is strict, prefer event-driven invalidation (below) over long TTLs.
- Never rely on in-process globals for caching under Octane; caching must be explicit and key-based.

## Invalidation strategy (prefer event-driven)
- Keep invalidation rules close to the write path:
    - On write: emit domain event → invalidate relevant keys.
- Avoid global flushes in production.
- If tags are used (when available), document tag semantics and tenant isolation.
- Prefer “version bump” invalidation for wide fan-out keys when precise invalidation is too expensive:
    - move `:v1` → `:v2` in the key schema and let old keys expire.

## Locks (baseline)
Use Redis locks for short critical sections, not for long workflows.
- `SET key value NX PX <ttl_ms>`

Mandatory:
- TTL = worst-case critical section time + buffer
- retry with backoff + jitter
- define behavior on failure (return error vs queue retry)

Failure modes to document:
- lock not acquired (contention)
- lock expires mid-work (TTL too low)
- process crash (lock released via TTL)

## Idempotency keys (edge dedupe)
For “exactly-once-like” behavior at the edge:
- Write a dedupe key with TTL:
    - `SET idempo:<key> <result_ref> NX EX <seconds>`
      But for critical side effects (money/legal/audit):
- also enforce dedupe with a DB unique constraint (preferred)

## Rate limiting
Prefer token bucket or sliding window.
Rules:
- limits must be tenant-aware (and user-aware if required)
- use atomic operations (Lua script or known atomic patterns)
- document:
    - scope (per IP / per user / per tenant)
    - window/refill rate
    - reject behavior (HTTP status + stable internal error code)

## Memory and eviction safety
- Monitor:
    - `maxmemory` and eviction policy
    - hit rate, evictions, key cardinality, top memory keys
- Avoid storing large payloads; store IDs and fetch from DB when needed.
- Avoid unbounded key growth:
    - add TTL
    - normalize keys
    - cap lists/sets by trimming

Operationally useful commands (examples):
- `INFO memory`
- `MEMORY STATS`
- `SCAN 0 MATCH <pattern> COUNT 1000` (sampling, not full scan in prod peak)
- `SLOWLOG GET`

# Verification / Definition of Done
When applying this skill, output (at minimum):
1) Truth vs projection decision:
- which tables are truth, which are projections (if any)
- any intentional denormalization and the measured query evidence for it
2) The exact query patterns driving indexes (or a short list of endpoints/jobs).
3) Proposed schema/index/constraint changes + why (tie each to a query/invariant).
4) Migration-safe steps (online/lock notes; phased rollout; rollback).
5) If projections/derived fields exist:
- update strategy (async/outbox vs trigger)
- idempotency/dedupe strategy
- rebuild/refresh strategy (if materialized)
6) If PgBouncer is used:
- pool mode (session vs transaction) and any session-state hazards
- prepared-statement stance (validated or avoided)
7) If Redis is involved:
- key formats + TTL choices
- invalidation hooks (which writes/events invalidate which keys)
- lock/rate-limit patterns + timeouts
- failure modes + what to monitor
8) How to verify:
- Postgres: `EXPLAIN (ANALYZE, BUFFERS)` (and `pg_stat_statements` if available)
- Redis: hit rate/evictions/key growth signals from your ops tooling

# Anti-patterns
- Treating Redis as a source of truth for business data.
- A cache/lock/limiter error that propagates as a request failure (Redis outage becomes service outage).
- Touching Redis during framework boot or process startup so that a Redis outage prevents the app from starting.
- Global flushes (`FLUSHALL`, `FLUSHDB`, framework-level cache flush) in production code or deploy scripts.
- Caching on top of an incomplete repository layer (code paths that bypass the cache and its invalidation).
- Adding speculative indexes “just in case”.
- Denormalizing truth tables without measured evidence and documentation.
- OFFSET pagination on large tables.
- Unbounded Redis keys (no TTL).
- Cache keys that omit tenant identifier (cross-tenant leakage risk).
- Non-tenant-scoped queries in multi-tenant systems.
- Cross-tenant reads/writes through non-audited code paths.
- Long transactions that include network IO.
- `CREATE INDEX CONCURRENTLY` inside a transaction.
- Using Redis alone for idempotency on critical side effects without DB dedupe.
- Using Redis locks for long workflows (lock TTL will betray you).
