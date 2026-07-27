# Redis: the shared contract, verification, and review signatures

Redis is fast and its memory is finite, so keys and TTLs are designed as a schema, not accumulated. This file holds
what is true of Redis in every service on the fleet. The lane files hold the mechanics: Laravel 13 and Octane in
`50-redis-laravel-octane.md`, a Go service on `alaa-go-chi` in `51-redis-golang.md`. Load the one that matches the
service.

## Availability contract (both lanes)

Redis is an optimization. It becomes an availability dependency only if a service is written so that it is. Every
design that adds Redis answers one question before it ships: what does this path do when Redis is slow, flapping,
or gone?

- **A cache read or write error never fails the request.** The path falls through to the source of truth. This is
  also a contract obligation: `alaa-services-contract` `references/22-failure-load-and-deprecation-contract.md`
  requires that a dependency marked `required: false` in `/api/ready` not fail a product request.
- **Redis calls are bounded so a sick Redis costs milliseconds.** Why a timeout, a retry budget, a backoff, or a
  breaker exists and how to shape it is `/alaa-reliability-sla` (`$alaa-reliability-sla`). The env keys and
  defaults for the Redis budgets, and what the kit compiles in today, are `60-configuration-and-kit-gaps.md`. This
  file states no number.
- **Nothing connects to Redis at process start or framework boot as a precondition for serving.** Connections stay
  lazy and probe failures stay non-fatal, so a Redis outage cannot stop workers from booting.
- **Every lock and every limiter states its behaviour when Redis is unreachable, at its call site.** The deciding
  question is `/alaa-reliability-sla`'s: when this dependency cannot answer, does proceeding without it let
  something through that must not get through? Yes makes it a gate that fails closed, and the review belongs to
  `/alaa-security-review` (`$alaa-security-review`). No makes it a contributor that fails open, under
  `/alaa-reliability-sla`. Correctness-critical exclusion is backed by a database constraint, never by Redis alone.
- **Running without the cache is visible.** Emit the fallback signal; do not let a silent fallback double the
  database load unnoticed. The metric, event, log-field, and error-code names are `/alaa-services-contract`
  (`$alaa-services-contract`) `references/24-metric-registry.md`, and when the name you need is not registered
  there you request its registration rather than inventing one. Requirement levels, gates, and alerting are
  `/alaa-observability-soc` (`$alaa-observability-soc`).
- **Cold-cache recovery is designed.** After an outage every key is missing at once; the stampede control below is
  what keeps the database standing while it refills.

## Cache key design

Namespaced and tenant-aware. Shape:

- `{app}:{env}:{tenant}:{resource}:{id}:{version}`
- Example: `comment-service:prod:project_123:thread:01J…:v1`

Rules:

- Include the tenant in every multi-tenant cache key. A key without it serves one tenant's row to another, and the
  response is a well-formed `200`.
- Include a version segment so a shape change can be rolled out by bumping it instead of by flushing.
- Normalize high-cardinality inputs before they enter a key; a raw URL or user-agent string produces unbounded key
  growth that only shows up as memory pressure weeks later.

## TTL discipline

- Every cache entry has an explicit TTL. On the Go kit this is enforced: `rediskit/cache.go:65-67` returns
  `ErrMissingTTL` for a non-positive TTL. Reason: an entry with no expiry outlives the truth it copies, and a
  missed invalidation then never heals.
- Shorter TTLs for volatile data; event-driven invalidation where correctness is strict.
- Spread the expiry of wide fan-out keys so they do not all expire in the same second. The jitter value is a
  platform value and belongs to `alaa-services-contract`
  `references/22-failure-load-and-deprecation-contract.md`; request its registration there if it is not yet
  recorded.
- Never cache in a process-level global as a substitute for a keyed entry. Under a long-lived worker that is a
  cross-request state leak, not a cache.

## Invalidation

- Invalidate at the write path: the write commits to the database first, then the exact affected keys are deleted.
  Delete rather than write-through, unless a measurement says otherwise, because a delete cannot store a value the
  transaction later rolled back.
- Every cached key has a named owner and a named invalidation trigger. A key whose trigger cannot be named is not
  cached.
- For wide fan-out, bump the version segment and let the old keys expire.
- No global flush in production code or in a deploy script. On a shared instance it destroys other concerns'
  data, and the cold-cache stampede that follows can take the database down.

## Locks

Redis locks bound a short critical section. They are an efficiency device: there is no fencing token, so a holder
paused past its TTL and a new holder can both believe they hold the lock.

- `SET key value NX PX <ttl_ms>`, with an owner token, and a release that checks the token before deleting.
- The TTL covers the worst-case critical section plus a margin, because a lock that expires mid-work is
  indistinguishable from no lock at all.
- Retry with backoff and jitter; shaping that is `/alaa-reliability-sla` `references/20-retries.md`.
- Document three failure modes at the call site: not acquired, expired mid-work, holder crashed.
- Correctness-critical exclusion lives in Postgres — a unique constraint, or `FOR UPDATE SKIP LOCKED` per
  `30-concurrency-projections-and-pooling.md`.

## Idempotency keys at the edge

- `SET idempo:<key> <result_ref> NX EX <seconds>` gives set-if-absent dedupe at the edge.
- For a side effect involving money, legal record, or audit, the dedupe is additionally enforced by a database
  unique constraint. Reason: a Redis key can be evicted under memory pressure, and an evicted dedupe key means the
  side effect runs twice.

## Rate limiting

- Token bucket or sliding window, computed atomically — a Lua script or a known-atomic command sequence. A
  read-then-write limiter under-counts at exactly the concurrency it exists to control.
- Limits are tenant-aware, and user-aware where the surface needs it.
- State the scope, the window or refill rate, and the reject behaviour at the call site. The HTTP status and the
  stable error code for a rejection are `/alaa-services-contract`.

## Memory and eviction safety

- Watch `maxmemory`, the eviction policy, hit rate, evictions, key cardinality, and the largest keys.
- Store identifiers and small DTOs, not object graphs; fetch the rest from the database.
- Cap growth: TTL on every key, normalized keys, trimmed lists and sets.
- Useful commands: `INFO memory`, `MEMORY STATS`, `SCAN 0 MATCH <pattern> COUNT 1000` for sampling, `SLOWLOG GET`.
  Do not run an unbounded `SCAN` or a `KEYS` during peak.

## Definition of done

Report these, and produce the proof rather than describing it. Which level of proof each claim needs is
`/alaa-testing-strategy` (`$alaa-testing-strategy`) `references/40-proof-strength.md`; this file states which
claims need proving.

1. Truth versus projection: which tables are truth, which are derived, and the measured evidence behind any
   deliberate denormalization.
2. The query patterns driving each proposed index, tied to an endpoint or a job.
3. The schema, index, and constraint changes, each tied to a query or an invariant.
4. The migration steps with their lock behaviour, phasing, and rollback, per
   `20-schema-migrations-and-performance.md`.
5. For projections: update strategy, dedupe strategy, and rebuild or refresh strategy.
6. For PgBouncer: the pool mode, the session-state hazards checked, and the prepared-statement stance per
   `30-concurrency-projections-and-pooling.md`.
7. For Redis: key formats, TTLs, the invalidation trigger for each key, the lock and limiter behaviour when Redis
   is down, and the signals emitted.
8. Verification actually run: `EXPLAIN (ANALYZE, BUFFERS)` for the queries, and the service serving correctly with
   Redis stopped and then restarted. An untested fallback is a rumour, so this one is proven against a real Redis,
   not a fake.

## Review signatures

What these look like in a diff, so they are caught before they ship:

- A `try`/`catch` around a cache call whose `catch` rethrows or returns the error to the caller.
- A cache read in a service provider, a constructor, an `init`, or a health-check-free startup path.
- `FLUSHALL`, `FLUSHDB`, or a framework-level cache flush anywhere outside a test.
- `Cache::remember(` or a Redis client call inside a controller, a handler, or a service that also has a
  repository for the same domain — those call sites bypass the invalidation the decorator performs.
- A cache key literal with no tenant segment and no version segment.
- A `Set` or `SETEX` with no TTL argument, or a TTL computed from a nullable that can reach zero.
- A retry loop around a Redis command on the request path.
- A new index in a migration with no query named in the same change.
- A `CREATE INDEX CONCURRENTLY` inside a transaction-wrapped migration.
- A transaction that performs an HTTP call, publishes to a broker, or sleeps.
