# Redis Cache Layer

Read this before writing any Redis call. Every rule here is absolute; none has an exception.

All kit facts below were read from `alaa-go-chi` source on **2026-07-26** and must be re-read from source before being
relied on.

## What Redis is here

**Rule:** Redis holds a copy of data whose source of truth is elsewhere. The database is correct; Redis is fast.

**Rule:** if a value must survive its own expiry, must be readable after a Redis restart, or is the only place a fact
exists, it is not cache and this file does not govern it. Take that design to `/alaa-data-layer`
(`$alaa-data-layer`) before writing the code.

## Failure behaviour — the two rules that have no exception

**Verified fact (`rediskit/config.go`, read 2026-07-26):** the kit sets `MaxRetries = -1`, which disables the client
library's internal retries, and applies a 250 ms per-call timeout. A Redis call therefore fails fast, once.

**Rule:** a failed cache read is a miss. Read from the source of truth, serve the response, and record the error. The
request succeeds.

**Rule:** a failed cache write is logged and counted, and the request succeeds. The kit's own position is explicit
(`rediskit/doc.go`): a Redis error never fails an already-committed write.

**Forbidden:** returning an error to a client because a Redis call failed. **Forbidden:** any wording that makes this
conditional — no cache is "critical enough" to fail a request, because a cache that can fail a request is a source of
truth wearing a cache's name, and that design belongs to `/alaa-data-layer` (`$alaa-data-layer`) before any code is written.

**Forbidden:** a retry loop, a backoff wrapper, or an extended timeout around a kit Redis call. The client already
decided not to retry, and re-adding retries multiplies latency during exactly the incident the fast failure was
designed for. **Rule:** pass the request-scoped context (`45-failure-behavior-at-the-call-site.md` section 2) and let
the call fail.

**Verified fact (`rediskit/doc.go`, read 2026-07-26):** the kit reports Redis readiness at degraded severity, not
required, so a Redis outage does not remove the instance from rotation. **Rule:** your service's behaviour must match
that promise — a service that cannot serve without Redis contradicts its own readiness contract.

## TTL

**Verified fact (`rediskit/cache.go`, read 2026-07-26):** the kit rejects a write with a non-positive TTL, returning
`ErrMissingTTL`. Every cache entry expires.

**Rule:** every write passes a positive TTL chosen for that key's data, not a shared default constant.

**Rule:** add jitter to the TTL of any key written in bulk or written on a schedule, so entries created together do
not expire together.

**Rule:** cache a negative result — a lookup that found nothing — with a TTL shorter than the positive result's, so a
repeated miss does not become a repeated database read.

**Forbidden:** persisting a cache entry with no expiry. If the data must not expire, see the second rule of this file.

## A miss is not an error

**Verified fact (`rediskit/cache.go`, read 2026-07-26):** the kit's cache reports a miss as a miss, never as an error.

**Forbidden:** comparing against `redis.Nil`, string-matching an error message, or treating a miss as a failure to
log. **Rule:** branch on the kit's miss signal, fall through to the source of truth, and record a miss — not an error.

## Where the cache lives

**Rule:** every Redis call sits behind a use case, a repository decorator, or a cache type with its own interface.
**Forbidden:** a Redis client reachable from a handler, a domain package, or a transport package — see
`62-import-direction-and-boundaries.md`.

## Keys

**Rule:** build every key in one exported function per entity, in the package that owns the cached data:

```go
func UserByIDKey(projectID uuid.UUID, userID int64) string {
    return "v1:project:" + projectID.String() + ":user:" + strconv.FormatInt(userID, 10)
}
```

**Rule:** every key carries a version segment, so a change to the cached value's shape is a new key space rather than
a deserialization failure against stale entries.

**Rule:** every key carries the tenant or project scope of the data it holds. **Forbidden:** a key whose scope comes
from a client-supplied value that was not validated against the caller's identity — that is a cross-tenant read.

**Forbidden:** a key segment built from unvalidated free-text input. **Rule:** key segments are ids, enum values, or
normalized values with a known finite domain; anything else lets a caller mint unlimited keys.

**Forbidden:** logging a whole key when its segments contain user or tenant identifiers. **Rule:** log the key's
prefix and the entity id separately as structured fields.

## Invalidation

**Rule:** the code that writes the source of truth also invalidates every key derived from it, in the same use case,
after the transaction commits.

**Rule:** when a write changes an entity that appears in list or query caches, invalidate those too, or version the
key space so they become unreachable. Listing the affected caches is part of designing the write, not a follow-up.

**Forbidden:** invalidating from a broker event as the only mechanism. Event-driven invalidation adds a window in
which the cache is wrong and depends on delivery; it is an addition to direct invalidation, never a replacement. The
delivery and replay semantics belong to `/alaa-async-messaging` (`$alaa-async-messaging`).

## Stampede

**Rule:** when a miss triggers work that is expensive enough to matter under concurrency, suppress duplicate work in
process with `golang.org/x/sync/singleflight`, keyed by the cache key.

**Rule:** use a Redis lock only when duplicate work across instances is the proven problem, and give it a TTL shorter
than the work it guards. **Forbidden:** a lock whose failure to acquire changes the answer the request returns —
correctness never depends on the lock; only duplicated effort does.

## Security

**Forbidden:** caching a secret, a token, a password, a credential, or a raw trusted header.

**Forbidden:** caching an authorization decision. Permission state changes and revocation must take effect
immediately; a cached "yes" outlives the revocation that should have stopped it. Take any need to cache authorization
to `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) and `/alaa-security-review` (`$alaa-security-review`)
before writing code.

## Signals

**Rule:** every cache emits hits, misses, errors, and source-of-truth fallbacks as separate counters, and cache call
latency as a histogram. Which of these must exist before a change merges belongs to `/alaa-observability-soc`
(`$alaa-observability-soc`); their names belong to `/alaa-services-contract` (`$alaa-services-contract`).

**Forbidden:** a metric label carrying a cache key, an entity id, or any value whose domain is not finite and small.

## Tests

**Rule:** a change to cache behaviour is not done until these six cases have tests: hit, miss, expiry, invalidation
after a write, Redis unreachable (the request still succeeds), and a serialization failure (the request still
succeeds).

**Rule:** use a fake for the cache interface in unit tests. Use a real Redis — via the repo's existing container
test setup — only for behaviour that depends on Redis semantics itself: TTL expiry, eviction, and lock behaviour.
