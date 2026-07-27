# Failure, Configuration, And Observability

Read this file before setting a timeout, retry count, pool size, read preference, or URI option, and before
deciding what a caller receives while MongoDB is electing a primary, slow, or unreachable. Every server behaviour
stated here was verified against the MongoDB manual on 2026-07-26; the page that settles each one is listed in
`source-map.md`.

Why a deadline exists, how a retry budget is shaped, when to shed load, and what a degraded response owes the
caller are doctrine owned by `/alaa-reliability-sla` (`$alaa-reliability-sla`)
`references/10-deadlines-and-timeouts.md`, `references/20-retries.md`,
`references/40-admission-and-shedding.md`, and `references/50-degradation.md`. The Ala numbers behind them are
owned by `/alaa-services-contract` (`$alaa-services-contract`)
`references/22-failure-load-and-deprecation-contract.md`. This file owns only the MongoDB knobs and behaviours
those decisions are expressed through.

## Failure behaviour

1. Bound every MongoDB operation with an explicit client-side deadline. Without one the caller's timeout is
   whatever the network eventually does, which no contract can state.
2. Set the deadline through the driver's unified per-operation budget (`timeoutMS`) where the driver supports it,
   because a per-operation budget covers server selection, connection checkout, and the round trip as one number
   instead of three that can each be exceeded.
3. Read the driver's own documented default before relying on any timeout you did not set. The manual documents
   `connectTimeoutMS` at 10,000 ms and `socketTimeoutMS` as no timeout by default while noting drivers vary, and
   it does not state a value for `serverSelectionTimeoutMS` on the connection-string page — so the driver's
   documentation, not this file, is the source for the value in force.
4. Leave retryable writes enabled and treat the retry as already spent: the manual states drivers compatible
   with MongoDB 4.2 and later enable them by default and retry once, and that retries continue past once only
   when `timeoutMS` is set. An application retry loop on top multiplies attempts without stating the total.
5. Do not claim retry coverage for a multi-document write: the manual excludes `updateMany`, `deleteMany`, any
   bulk operation containing them, and writes with `w: 0`. Express such work as retryable single-document
   operations when the retry matters, per `30-writes-consistency-and-change-streams.md`.
6. Prove retry behaviour against a replica set rather than a single-node development deployment, per
   `50-applying-and-proving.md`, because the manual states retryable writes require a replica set or sharded
   cluster and are not supported on standalone instances.
7. Leave retryable reads enabled and expect one retry: the manual states drivers compatible with MongoDB Server
   6.0 and later enable them by default and make only one attempt.
8. Give any long-running read its own resume point rather than relying on the driver: the manual excludes
   `getMore`, `mapReduce`, generic `runCommand` reads, and aggregations containing `$out` or `$merge` from
   retryable reads, so a cursor that breaks mid-iteration ends the read.
9. Treat a primary election as a bounded write outage and answer the caller from the degraded path rather than
   waiting: the manual states drivers wait `serverSelectionTimeoutMS` for a new primary and that a retryable
   write fails if failover takes longer.
10. Rely on the deduplication key, not on the driver, for exactly-once effect during failover: the manual warns
    that a client unresponsive for longer than `localLogicalSessionTimeoutMinutes` may have its write retried and
    applied again.
11. Define what each read and write path returns while MongoDB is unreachable — a degraded response, a cached
    value, or a typed failure — and name the error through `/alaa-services-contract`
    (`$alaa-services-contract`). An empty success response is indistinguishable from "no data exists" and hides
    the outage from the caller.
12. Choose the read preference explicitly. The manual's default is `primary`, which means reads stop during an
    election; `secondaryPreferred` keeps reads serving at the cost of staleness, and whether that staleness is
    acceptable for a given read is decided by `/alaa-system-design` (`$alaa-system-design`)
    `references/30-data-and-consistency.md`.

## Configuration surface

1. Set every item below from configuration; none of them is compiled into application code, because a value in
   code is a value no environment can differ on and no incident can change.

| Knob | What it bounds | Varies by environment |
|---|---|---|
| hosts, replica set name, TLS settings, credentials | which deployment is reached and how it is trusted | yes |
| `maxPoolSize`, `minPoolSize`, `maxIdleTimeMS` | concurrent in-flight operations per process | yes |
| `waitQueueTimeoutMS` | how long a caller waits for a free connection | yes |
| `connectTimeoutMS`, `socketTimeoutMS`, `serverSelectionTimeoutMS`, `timeoutMS` | how long a failure takes to surface | yes |
| `readPreference`, `readConcernLevel` | staleness a read may observe | yes |
| `w`, `wtimeoutMS`, `journal` | durability a write must reach | per write class, not per environment |
| `retryWrites`, `retryReads` | whether the driver's single retry is available | no — enabled everywhere |
| `appName` | which service a server-side slow query is attributed to | no — always set |

2. Keep the value itself out of this skill: the Ala number for any timeout, pool size, or retry count is owned by
   `/alaa-services-contract` (`$alaa-services-contract`)
   `references/22-failure-load-and-deprecation-contract.md`, and a value absent there is requested there.
3. Never commit a connection string carrying credentials, and rotate rather than rewrite history when one is
   committed. A credential in git history outlives the commit that removed it; the handling rule is owned by
   `/alaa-security-review` (`$alaa-security-review`) `references/50-credentials-and-cryptography.md`.
4. Request a kit lane before writing a MongoDB client into a Go consumer. On 2026-07-26 `alaa-go-chi` ships
   `pgkit`, `rediskit`, and `chkit` and no MongoDB package, so there is no configured lane for these keys;
   the kit change belongs to `/alaa-go-chi-development` (`$alaa-go-chi-development`).
5. Configure a Laravel service through the framework's database configuration with `mongodb/laravel-mongodb`,
   which requires the `mongodb` PHP extension; the layering rules for where that configuration is consumed are
   owned by `/alaa-laravel-architecture` (`$alaa-laravel-architecture`).

## Concurrency and load

1. Compute total server connections as pool size multiplied by processes multiplied by instances, and check the
   result against the deployment's connection limit before raising a pool. The manual documents `maxPoolSize` at
   100 and `minPoolSize` at 0 by default, so a modest fleet reaches thousands of connections without anyone
   choosing that number.
2. Create one client per process and reuse it. A client per request creates a connection pool per request.
3. Set a wait-queue timeout so pool exhaustion surfaces as a fast, typed failure. Without one, saturation
   presents as unbounded latency, which reads as "the database is slow" while the database is idle.
4. Do not answer saturation by raising the pool alone: a larger pool moves the queue from the client to the
   server. Shedding and admission are decided by `/alaa-reliability-sla` (`$alaa-reliability-sla`)
   `references/40-admission-and-shedding.md`.

## What must be observable

1. Make these six observable for every service using MongoDB: operation latency and error rate by operation and
   collection; connection-pool utilisation and wait time; server-selection and election failures; retry counts;
   backlog of an expiring collection against its stated steady-state size; and the slow-operation surface.
2. Take every metric, log-field, and error name from `/alaa-services-contract` (`$alaa-services-contract`)
   `references/24-metric-registry.md`, and request registration there when the name you need does not exist.
   Never coin one locally, because a locally coined name is invisible to every fleet dashboard.
3. Take the requirement level of each signal — what must exist before merge and what is optional — from
   `/alaa-observability-soc` (`$alaa-observability-soc`) `references/20-instrumentation-gates.md`, and take
   alert thresholds and retention from its `references/40-alerting-slo-retention.md`.
4. Log the operation, collection, outcome, and duration, and never the document payload or the connection
   string. A log line carrying a document carries whatever that document holds.
