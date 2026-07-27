---
name: alaa-data-layer
description: "Postgres-truth data-layer policy for the Ala fleet: which store owns a fact, tenant-scoped schema and index design, migrations that do not lock a live table, query and pool tuning, and Redis run as a cache the request survives losing. Use when changing a table, column, constraint, index, or migration; when a query, lock, pool, or projection is slow or contended; when adding, keying, or invalidating a cache entry, Redis lock, idempotency key, or rate limiter; when deciding what a request does while Postgres or Redis is degraded; and when setting a data-store timeout or pool size. Do not use it to add a datastore nobody asked for, or for a refactor with no schema, query, or cache surface. Route cursor pagination to /alaa-keyset-pagination, ClickHouse schema to /clickhouse-performance-schema-ops, MongoDB to /alaa-mongodb-patterns, outbox and consumer mechanics to /alaa-async-messaging, timeout and retry doctrine to /alaa-reliability-sla."
---

# Alaa Data Layer

Decide which store owns a fact, what shape it takes in Postgres, how it changes under load, and what a request does
when a store is slow or gone. It owns data-store mechanics — schema, constraint, index, migration, query,
transaction, pool, cache key, TTL, invalidation — and no doctrine, no telemetry name, and no platform value beyond
the keys in `references/60-configuration-and-kit-gaps.md`.

## When not to use

A refactor that changes no schema, query, or cache surface. A request to add a datastore nobody asked for — say so
and stop.

## Rules that hold on every task

1. Postgres holds business truth; Redis and ClickHouse hold derived, rebuildable copies. A store that can be
   evicted or flushed cannot be the record of what happened.
2. Read the service's configured lanes before applying a Postgres rule: `alaa-go-chi docs/CONSUMERS.md:23` runs
   `wa-api` on ClickHouse with no pgkit and no rediskit.
3. Every cache entry carries an explicit TTL, enforced at `rediskit/cache.go:65-67`. An entry with no expiry
   outlives the truth it copies.
4. Every index names the query or invariant justifying it. An unjustified index is write cost buying no read.
5. Every migration reverses, or records inside itself why it cannot and how that is mitigated. An irreversible
   migration turns a rollback into an incident.
6. Every tenant-scoped query filters by tenant, and every uniqueness rule on such a table is tenant-aware. The
   failure is a cross-tenant read returning a well-formed `200`.
7. Never invent a metric, log-field, event, or error-code name; take it from `/alaa-services-contract`
   (`$alaa-services-contract`) and request registration there when it is missing. An invented name diverges across
   services.
8. Verify a platform claim against kit source, never a decision log. Two knobs in
   `references/60-configuration-and-kit-gaps.md` are ratified and absent from code.
9. Never commit a connection string, password, or certificate. A credential in git history outlives the commit
   that removed it, so the only fix is rotation.

## References — read the row you match

| You are about to … | Read |
|---|---|
| pick the store for a fact, design a table, or tenant-scope a query or unique key | `references/10-postgres-design-and-tenant-boundaries.md` |
| touch a table that already holds production rows | `references/20-schema-migrations-and-performance.md` |
| tune a query, claim rows, build a projection, size a pool, or handle a saturated Postgres | `references/30-concurrency-projections-and-pooling.md` |
| key, expire, invalidate, lock, or rate-limit in Redis, in any language | `references/40-redis-verification-and-anti-patterns.md` |
| add or change Redis in a Laravel or Octane service | `references/50-redis-laravel-octane.md` |
| add or change Redis in a Go service on `alaa-go-chi` | `references/51-redis-golang.md` |
| set a data-store timeout, pool size, or retry count, or find no environment key for it | `references/60-configuration-and-kit-gaps.md` |
| repeat a version-sensitive claim about Postgres, Redis, pgx, or a Laravel cache API | `references/source-map.md` |

## Not owned here

Timeout, retry, backoff, breaker, backpressure, and degradation doctrine: `/alaa-reliability-sla`
(`$alaa-reliability-sla`). Every platform value this skill does not state, and every telemetry or error-code name:
`/alaa-services-contract` (`$alaa-services-contract`). The ten-point quality bar: `/alaa-project-constitution`
(`$alaa-project-constitution`) `references/quality-bar.md`. Model and effort: `/alaa-prompting-guide`
(`$alaa-prompting-guide`). Every other owner — pagination, ClickHouse, MongoDB, the broker, testing, system
design, kit changes — is named at the rule it governs inside `references/`.
