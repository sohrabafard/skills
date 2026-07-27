---
name: alaa-mongodb-patterns
description: "MongoDB mechanism for the Ala fleet: document and collection shape, tenant-scoped compound indexes, TTL and retention, idempotent upserts and bulk writes, read and write concern, pool and timeout settings, and what a caller receives while a primary is being elected. Use when adding or changing a MongoDB collection, document shape, index, TTL rule, schema validator, upsert, bulkWrite, aggregation, change-stream reader, or connection option; when a Mongo query is slow, a document grows without bound, or a replayed message writes twice; and when deciding what a read returns while MongoDB is degraded. Do not use it to add MongoDB to a repository that does not already run it, and do not use it for Postgres or Redis work: those two stores and the store-selection decision itself belong to /alaa-data-layer ($alaa-data-layer), and analytical columnar work belongs to /clickhouse-performance-schema-ops ($clickhouse-performance-schema-ops)."
---

# Alaa MongoDB Patterns

MongoDB mechanism only — document, index, TTL, validator, write, concern, pool, URI option. No doctrine, no
telemetry name, and no platform number is stated here.

## When not to use

The repository does not already run MongoDB and the request did not name it: say so, route the store-selection
decision to `/alaa-data-layer` (`$alaa-data-layer`), and stop. On 2026-07-26 no service in
`alaa-go-chi docs/CONSUMERS.md` runs MongoDB and the kit ships no MongoDB package, so proposing it here adds a
datastore nobody operates.

## Rules that hold on every task

1. Every tenant-owned document carries the tenant key, every query filters on it, and every unique index includes
   it, because the failure is a cross-tenant read returning a well-formed `200`.
2. Every MongoDB call states its deadline, its retry budget, and what the caller receives when it fails, under
   `/alaa-reliability-sla` (`$alaa-reliability-sla`), because an availability target above 99.99% is a claim
   about the failure path.
3. Never put a credential, token, or password in a document; keep it in the secret store the repository already
   uses and take the threat class to `/alaa-security-review` (`$alaa-security-review`), because a database backup
   copies every secret the database holds.
4. Never state a platform number or coin a telemetry name: `/alaa-services-contract`
   (`$alaa-services-contract`) owns both, numbers in `references/22-failure-load-and-deprecation-contract.md`
   and names in `references/24-metric-registry.md`, and a missing name is requested there.

## References

| You are about to … | Read |
|---|---|
| shape a collection or document, bound a growing field, add a validator, or pick a shard key | `references/10-modeling-tenancy-and-collection-shape.md` |
| add or reorder an index, set a TTL rule, or explain a slow query or deep page | `references/20-indexes-ttl-and-query-shape.md` |
| insert, upsert, bulk-load, count, choose a concern, open a transaction, or read a change stream | `references/30-writes-consistency-and-change-streams.md` |
| set a timeout, retry, pool size, read preference, or URI option, or answer a caller while MongoDB is electing, slow, or unreachable | `references/40-failure-configuration-and-observability.md` |
| hand back a design, roll out an index, TTL, or backfill, or decide what proof it needs | `references/50-applying-and-proving.md` |
| repeat a version-sensitive claim about the server, the driver, or the Laravel package | `references/source-map.md` |

## Not owned here

Telemetry requirement levels: `/alaa-observability-soc` (`$alaa-observability-soc`). The ten obligations of the
quality bar: `/alaa-project-constitution` (`$alaa-project-constitution`) `references/quality-bar.md`. Model and
effort: `/alaa-prompting-guide` (`$alaa-prompting-guide`). Store selection, pagination, complexity, the broker,
proof strength, system design, and ClickHouse are named at the rule they govern inside `references/`.
