# Redis in a Go service on alaa-go-chi

Read this when a Go service adds or changes Redis usage: a cache in front of a repository read, a lock, an
idempotency key, or a rate limiter.

Every configuration claim below was read from `alaa-go-chi` source in this repository, not from a design document
or a decision log. Re-read the cited file before repeating a claim; `references/source-map.md` says which claims
are version-sensitive. Cache-aside shape, key naming, serialization, and the Go cache test list are
`/alaa-golang` (`$alaa-golang`) `references/61-redis-cache-layer.md`; that file is the pattern authority and this
one does not restate it.

## Platform policy — cache database reads, not computation

- Use Redis as cache-aside in front of repository database reads: hot lookups, expensive aggregates, high-QPS list
  heads. Postgres stays the only source of truth, which `rediskit/doc.go:12-13` states as a kit invariant.
- Do not cache function results, rendered payloads, or business computation whose inputs are already in memory. In
  Go the recompute is cheaper than the network hop, and every extra cached shape adds an invalidation liability
  that outlives the person who added it.
- Locks, rate limits, and idempotency keys are separate deliberate uses under `40-redis-verification-and-anti-patterns.md`,
  not caching, and they are not introduced because Redis happens to be wired.
- A Laravel service may additionally use Redis for sessions, queues, and processing primitives; a Go service on
  this kit may not. See `50-redis-laravel-octane.md` for that lane.

## Repository boundary gate

Caching attaches at the repository seam and nowhere else.

1. The read being cached goes through a repository interface owned by the use case — principle P5 in
   `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`), which forbids a Redis import in
   `domain` or `application`.
2. The cache lives in a repository decorator or the use case. A handler that imports the Redis client fails this
   gate.
3. When the repository layer is incomplete, finish it first through `/alaa-golang` (`$alaa-golang`) and add the
   cache afterwards. Reason: a cache in front of a partial repository has call sites that bypass both the read and
   its invalidation, so readers see a mix of fresh and stale rows with no error anywhere.

## Use the kit client; do not construct your own

`rediskit.NewClient` is the only Redis client a kit consumer builds. `rediskit/config.go:84-85` states that the
timeout, retry, and connection budgets are kit invariants that a deployment URL must not weaken, and
`config.go:86-99` overrides them on every construction. Writing `redis.NewClient(&redis.Options{...})` in a service
therefore produces a second, unreviewed timeout policy on the same shared Redis.

What the kit fixes today, read from source:

| Setting | Value in the kit | Where |
|---|---|---|
| DialTimeout, ReadTimeout, WriteTimeout, PoolTimeout | all `250ms`, one constant | `rediskit/config.go:15,87-90` |
| MaxRetries | `-1`, retries disabled | `rediskit/config.go:91` |
| MinRetryBackoff, MaxRetryBackoff | `-1` | `rediskit/config.go:92-93` |
| DialerRetries | `1` | `rediskit/config.go:94` |
| PoolSize, MaxIdleConns | `32` | `rediskit/config.go:20,96-97` |
| MaxActiveConns | `32`, equal to PoolSize | `rediskit/config.go:23,98` |
| MaxConcurrentDials | `4` | `rediskit/config.go:25,99` |
| MinIdleConns, ConnMaxIdleTime | never set | absent from `rediskit/config.go` |
| ContextTimeoutEnabled | `true` | `rediskit/config.go:86` |

Two consequences follow and neither is optional. The dial budget is 250 ms, which is below what DNS plus TCP plus
TLS costs on a cloud network, so the first command after a pod start or a connection reap can fail on dial alone —
treat that as an expected degradation until `REDIS_DIAL_TIMEOUT` exists, and do not compensate with a retry loop.
The env keys and the corrective change requests are in `60-configuration-and-kit-gaps.md`; the only Redis keys that
exist today are `REDIS_URL`, `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASS`, `REDIS_DB`.

Pass a per-call context derived from the request context. `rediskit` applies its own 250 ms ceiling on top
(`rediskit/client.go:80-82`), so a request that has less budget left than that still governs.

## Degraded mode — Redis down must not take the service down

The request path survives a full Redis outage by falling through to Postgres. This is a contract obligation, not a
local preference: `alaa-services-contract` `references/22-failure-load-and-deprecation-contract.md` requires that a
dependency marked `required: false` in `/api/ready` never fails a product request. `rediskit/readiness.go:17`
registers the Redis check at `SeverityDegraded`, so a Redis blip degrades the pod instead of draining it.

1. **Error classification is already done for you.** `rediskit/cache.go:46-58` returns a missing key as a clean miss
   — `(nil, false, nil)` — and returns a transport error to the caller. Do not re-check for `redis.Nil` in the
   decorator; `rediskit/client.go:88-91` has already translated it.
2. **The fallback decision is yours, and it belongs in the decorator.** `rediskit/doc.go:8-10` places what to cache,
   the cache-aside read path, and single-flight policy in consumer domain code. On a transport error the decorator
   reads through the inner repository and records the failure; it never returns the cache error to its caller,
   because that converts a cache outage into a service outage.
3. **Bound the origin load during the outage.** With the cache gone, every read reaches Postgres.
   `22-…` requires at most one origin computation per cache key in flight per instance, with later callers waiting
   on it until the deadline. `rediskit/doc.go:9` assigns that single-flight to consumer domain code, and
   `golang.org/x/sync` is an indirect dependency in `go.mod` today, so adopting `singleflight` is a direct
   dependency addition. Take the package decision to `/alaa-golang` (`$alaa-golang`)
   `references/40-production-ready-package-catalog.md`.
4. **Whether to add a circuit breaker is a doctrine question, not a configuration one.** The kit contains no
   breaker: `gobreaker`, `redsync`, `redis_rate`, `rueidis`, and any `CircuitBreaker` symbol are absent from every
   `.go` file, from `go.mod`, and from `go.sum`. Whether this dependency warrants one, and how to shape it, is
   `/alaa-reliability-sla` (`$alaa-reliability-sla`) `references/30-breakers-and-bulkheads.md`. When the answer is
   yes, decide with `/alaa-go-chi-development` (`$alaa-go-chi-development`) whether it belongs in the kit rather
   than in one service, because a breaker built once per service produces a different outage posture per service on
   one shared Redis.
5. **Never block startup on Redis.** Construct the client at boot and let the first command discover the outage.
   The readiness probe already reports Redis state at degraded severity; a fatal `Ping` in `main` converts a Redis
   outage into a fleet-wide crash loop.
6. **Writes during an outage are best-effort.** A missed `Set` costs a later miss and a missed `Delete` heals when
   the TTL expires, which is the reason `rediskit/cache.go:65-67` rejects a `Set` with a non-positive TTL as
   `ErrMissingTTL` rather than storing it.
7. **Whether the dependency fails open or fails closed is one question, asked once per call site.** When this
   dependency cannot answer, does proceeding without it let something through that must not get through?
   `/alaa-reliability-sla` (`$alaa-reliability-sla`) owns that question and the fail-open contributor case;
   `/alaa-security-review` (`$alaa-security-review`) owns the fail-closed gate case. A cache read is always a
   contributor. A rate limiter in front of an abuse-sensitive surface may not be.

## Observability

Wire the kit's ports rather than defining counters. `rediskit/metrics.go` already registers cache-read outcomes
with a bounded `hit|miss|error` label (`CacheResult`, `metrics.go:53-59`), transport operation counts and
durations, and pool statistics; `WithCacheMetrics` and the client's metrics option attach them. A parallel
service-local counter double-counts the same event under a second name.

Metric, log-field, event, and error-code names are `/alaa-services-contract` (`$alaa-services-contract`); its
`references/24-metric-registry.md` is the register. That register lists `alaa_db_*` families for a service with a
database and lists no Redis cache family today, so a service adopting the kit's Redis metrics requests their
registration rather than assuming they are covered. Requirement levels, gates, and alerting belong to
`/alaa-observability-soc` (`$alaa-observability-soc`).

## Locks and rate limits

- A Redis lock is an efficiency device, not a correctness device: it has no fencing token, so a holder paused past
  its TTL and a new holder can both believe they hold it. Correctness-critical exclusion lives in Postgres —
  a unique constraint, or `FOR UPDATE SKIP LOCKED` per `30-concurrency-projections-and-pooling.md`.
- The kit ships no lock and no rate limiter. `redsync` and `redis_rate` are absent from `go.mod` and `go.sum`, so
  either is a new direct dependency; route the package choice to `/alaa-golang`
  `references/40-production-ready-package-catalog.md` and the fail-open or fail-closed decision to the question in
  point 7 above.
- Every lock and every limiter states, at its call site, what happens when Redis is unreachable. A call site that
  does not state it inherits whatever the client library does, which is a decision nobody made.

## Proof this needs before it ships

State the level, then produce it. What counts as a test at each level is `/alaa-testing-strategy`
(`$alaa-testing-strategy`) `references/40-proof-strength.md`; this file states only which level applies.

- The decorator's fallback on a transport error: level 2, a unit test with a fake that returns an error.
- The cache-hit, clean-miss, and invalidate-on-write paths: level 2.
- Service behaviour with Redis actually stopped and then restarted: level 6, against a real Redis. A fallback that
  has only been unit-tested is a claim about a fake, not about the service.

## Companion routing

- `/alaa-golang` (`$alaa-golang`) — `references/61-redis-cache-layer.md` cache-aside authority, `60-…` repository
  seam, `40-…` package catalog.
- `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) — P5 ports, P7 idempotency and its
  run-twice proof, P12 boundary tests.
- `/alaa-go-chi-development` (`$alaa-go-chi-development`) — every change to `rediskit` itself, and the change
  requests in `60-configuration-and-kit-gaps.md`.
- `/alaa-reliability-sla` (`$alaa-reliability-sla`) — timeout, retry, breaker, and degradation doctrine.
