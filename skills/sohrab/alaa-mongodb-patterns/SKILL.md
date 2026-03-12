---
name: alaa-mongodb-patterns
description: "MongoDB schema/index/write patterns for multi-tenant, event-driven workloads (idempotent writes, TTL, compound indexes, bounded documents) without introducing new datastores."
---

# Purpose
Provide production-grade MongoDB guidance for multi-tenant, event-driven services:
- model documents around real query patterns (not “perfect normalization”)
- keep documents bounded (avoid unbounded arrays)
- build compound indexes aligned to filters + sorts
- implement idempotent ingestion/writes (unique keys + upserts)
- use TTL and retention safely for ephemeral data
- avoid operational foot-guns (write amplification, hot partitions, multi-doc transactions)

# When to use
Use this skill ONLY when:
- the repository already uses MongoDB, OR
- the user explicitly requests MongoDB design/changes.

Examples:
- designing collections for comment timelines, event ingestion, analytics write models
- adding/changing indexes and query patterns
- implementing TTL, dedupe, idempotent writes
- considering change streams (only if enabled) for reactive pipelines

If the repo is Postgres-only and the user did not request MongoDB, DO NOT propose adding MongoDB. Use `alaa-data-layer` instead.

# Hard constraints
- Do NOT introduce MongoDB to a repo that does not already use it unless the user explicitly requests.
- Always include tenant isolation (`tenantId` or equivalent) on tenant-owned documents.
- Every index must be justified by a concrete query pattern.
- Keep documents bounded in size; avoid unbounded arrays and unbounded growth fields.
- Never store secrets/tokens in MongoDB unless the repo has explicit encryption-at-rest and access-control assumptions.
- Prefer minimal diffs; do not refactor unrelated code.

# Core modeling principles
- Design around query patterns and data access paths.
- Optimize for operational safety:
    - predictable document size
    - predictable index set
    - explicit retention rules
- Avoid “clever” polymorphic documents that explode index complexity.

## Bounded documents (mandatory)
Avoid:
- unbounded arrays of comments/reactions/events inside a single document
- storing full timelines inside one document

Prefer:
- one document per entity (comment/event)
- or bucketed documents with hard caps (size/time window) when justified and explicitly enforced
- Keep each document comfortably below MongoDB's 16MB hard limit; reject/split/bucket before growth approaches the limit.

# Multi-tenant rules (mandatory)
- Include `tenantId` (or `projectId`) in every tenant-owned document.
- Most queries should start with `tenantId` to keep index selectivity high.
- Prefer compound indexes that start with tenantId.

## Sharding hotspot guardrails (when sharding is used)
- Avoid monotonic shard keys (`createdAt`, sequence-like IDs) that can concentrate writes on a single shard.
- Prefer distribution-friendly shard keys and validate chunk distribution/hotspot behavior under expected write load.

Default compound index shapes:
- `{ tenantId: 1, createdAt: -1 }` (feeds/timelines)
- `{ tenantId: 1, businessKey: 1 }` (lookups / invariants, often unique)

# Index patterns (deterministic)
General rule:
- equality fields first, then range/sort fields
- keep index count minimal on write-heavy collections

Examples:
```js
// timeline/feed
db.comments.createIndex({ tenantId: 1, contentId: 1, createdAt: -1 });

// idempotent event ingestion
db.events.createIndex({ tenantId: 1, eventKey: 1 }, { unique: true });

// TTL for ephemeral tokens/logs
db.tokens.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 });
```

## TTL usage
Use TTL for ephemeral data only:
- one-time tokens
- short-lived sessions (if policy allows)
- temporary logs/trace artifacts (not audit logs)

Rules:
- TTL index must be explicit and documented.
- TTL is not instant; design with eventual deletion in mind.
- Never rely on TTL for strict security revocation; implement explicit revocation checks.

# Write patterns (event-driven friendly)

## Idempotent upsert (preferred for ingestion)
Use a unique key (tenant + business key) to prevent duplicates.
```js
db.events.updateOne(
  { tenantId, eventKey },
  { $setOnInsert: { tenantId, eventKey, createdAt: new Date(), payload } },
  { upsert: true }
);
```

## Batch ingestion
Prefer `bulkWrite` for batches to reduce round trips:
- group by collection + index strategy
- keep batches moderate size; handle partial failures explicitly

## Write concern (correctness vs performance)
- Default to `w: "majority"` when correctness matters.
- If performance demands lower durability, document the trade-off explicitly.

## Counters/aggregates
- Avoid hot-spot counters with heavy contention.
- Prefer:
    - periodic aggregation jobs (stream to analytical store like ClickHouse), OR
    - bounded atomic `$inc` on documents designed to avoid hot partitions

# Transactions & consistency
- Avoid multi-document transactions unless you truly need them (they increase latency and operational coupling).
- Prefer single-document atomic updates where possible.
- If you must use transactions:
    - keep them short
    - avoid external IO inside transactions
    - document failure modes and retries

# Schema validation (recommended)
Use MongoDB schema validation (JSON schema) when:
- you have multiple writers or evolving schemas
- you need to prevent accidental writes of malformed documents

Rules:
- validate critical fields: tenantId, timestamps, business keys
- keep schemas versioned and documented

# Change streams (optional)
Use change streams only if enabled and justified:
- reactive pipelines
- near-real-time projections
- audit-like streaming into other systems

Rules:
- treat stream consumption as at-least-once
- implement consumer idempotency
- handle resume tokens and replays

# Query review checklist (before adding an index)
1) Write the query pattern explicitly:
    - filter fields, sort fields, expected cardinality
2) Confirm tenant scoping (`tenantId` first).
3) Add the minimum index that satisfies the filter+sort.
4) Re-check write amplification:
    - each extra index slows writes
5) Validate with real-ish data volume where possible.

# Output contract (when applying this skill)
When using this skill, always output:
1) Proposed collection schema (fields + intent) and boundedness rules
2) Query patterns (the exact queries you are optimizing for)
3) Required indexes and why each exists
4) Write pattern choice (insert vs upsert vs bulkWrite) + idempotency approach
5) TTL/retention rules (if any)
6) Risks (write amplification, hot partitions, doc growth) + mitigations
7) Verification steps (queries to run, what metrics to watch)

# Anti-patterns
- Proposing MongoDB for a Postgres-only repo without explicit request.
- Unbounded arrays or ever-growing documents.
- Indexing “just in case” without a concrete query pattern.
- Storing large payloads in hot collections when IDs suffice.
- Depending on TTL for strict security revocation.
- Non-tenant-scoped queries in multi-tenant systems.
- Infinite retries in consumers; no dedupe key for at-least-once delivery.
