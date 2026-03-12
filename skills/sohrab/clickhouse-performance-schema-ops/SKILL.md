---
name: clickhouse-performance-schema-ops
description: >
  Use this skill when the task is about ClickHouse architecture, schema design, MergeTree engine choices,
  ORDER BY / PARTITION BY / PRIMARY KEY design, ingestion strategy, async inserts, materialized views,
  projections, TTL, skip indexes, query tuning, system tables, operational troubleshooting, or production
  hardening. Use it for ClickHouse Cloud and self-managed clusters when the answer must reflect ClickHouse's
  columnar OLAP model. Do NOT use it for OLTP schema design, generic ANSI SQL questions that are not
  ClickHouse-specific, or ORM-centric application CRUD work.
---

# Skill: ClickHouse performance, schema, ingest, and operations

Date: 2026-03-01

This skill is optimized for **real-world ClickHouse work**:
- designing MergeTree tables correctly
- choosing ordering and partitioning keys
- selecting an insert strategy that avoids merge pressure and "too many parts"
- deciding between materialized views, projections, TTL, and lightweight deletes
- diagnosing slow queries, mutation backlog, merge pressure, and storage churn
- turning vague ClickHouse asks into a concrete plan, SQL artifacts, and validation steps

## Operating principles

1. **Think like ClickHouse, not like an OLTP database**
   - Primary keys are sparse indexes and define on-disk order.
   - MergeTree parts, background merges, and data layout dominate performance.
   - Avoid porting row-store instincts directly.

2. **Always collect workload facts before prescribing SQL**
   Ask for or infer:
   - deployment: Cloud, self-managed, replicated, object storage, single node, cluster
   - ingest shape: events/sec, rows/insert, concurrent writers, retry behavior
   - query shape: top 5 filters, aggregations, joins, freshness requirements
   - retention: hot window, cold window, delete cadence, TTL expectations
   - correctness: dedup rules, upserts, late-arriving events, need for FINAL
   - pain: slow queries, too many parts, mutations, merge backlog, disk pressure

3. **Bias toward the cheapest mechanism that solves the problem**
   - first: types, ORDER BY, PARTITION BY, insert batching
   - then: materialized columns, skip indexes, materialized views
   - later: projections, specialized engines, refresh pipelines
   - avoid frequent large UPDATE/DELETE mutations when a table-engine or ingest redesign solves it

4. **Every answer must end with explicit outputs**
   Produce one or more of:
   - DDL with comments
   - ingest strategy
   - query rewrite
   - diagnostics SQL
   - rollback/risk notes
   - validation checklist

## Default workflow

### Step 1: classify the workload
Choose one primary mode:
- event/log analytics
- metrics/time-series
- product analytics
- rollup/dashboard acceleration
- mutable fact table / upsert-ish workload
- observability / OTel
- data lake / federation
- hybrid

### Step 2: design the base table
For MergeTree-family tables, decide in this order:
1. **column types**
   - use the narrowest numeric types you can justify
   - use `LowCardinality` for repeated string dimensions when appropriate
   - avoid `Nullable` unless semantics really require it
2. **ORDER BY**
   - optimize for the most common selective filters
   - place lower-cardinality / broader-pruning dimensions earlier when that helps skipping
   - add high-cardinality tie-breakers later only when useful
3. **PRIMARY KEY**
   - by default it matches ORDER BY
   - if needed, use a prefix of ORDER BY to reduce primary-index memory
4. **PARTITION BY**
   - keep it low-cardinality and operationally meaningful
   - do not explode partitions
   - use it for lifecycle/retention and large-scale management, not as a substitute for ORDER BY
5. **ENGINE**
   Choose deliberately:
   - `MergeTree` for append-only
   - `ReplacingMergeTree` when eventual dedup/upsert semantics are needed
   - `CollapsingMergeTree` / `VersionedCollapsingMergeTree` when sign/version models are already present
   - `AggregatingMergeTree` / `SummingMergeTree` only when their maintenance model fits the query plan

### Step 3: design ingestion
Prefer in this order:
1. **client-side batching** when easy
2. **async inserts** when many writers send small payloads
3. Kafka / queue mediated ingestion when fan-in and backpressure need isolation

Never assume small synchronous inserts are harmless. Watch part counts and merge debt.

### Step 4: optimize for access patterns
Use the lightest tool that matches the need:
- **materialized columns** for reusable derived expressions
- **skip indexes** for additional block pruning when the primary key is not enough
- **materialized views** for ETL, rollups, denormalization, or multi-stage pipelines
- **projections** for single-table alternate layouts and transparent optimizer use
- **TTL** for retention / tiering / column expiration
- **lightweight deletes** or partition drops when operational deletes are unavoidable

### Step 5: diagnostics
Start with evidence, not guesses:
- inspect `system.query_log`, `system.query_thread_log`, `system.parts`, `system.part_log`, `system.mutations`, `system.projections`
- check part counts, mutation queue, merge backlog, row/byte scan volume, selected parts, and read amplification
- if the problem is slow queries, explain why the engine read too much data
- if the problem is ingest, explain why merges could not keep up

## Decision rules the assistant should follow

### ORDER BY / PRIMARY KEY
- favor columns used often in WHERE / PREWHERE and capable of pruning large ranges
- do not promise uniqueness semantics from PRIMARY KEY
- remember PRIMARY KEY can be a prefix of ORDER BY

### PARTITION BY
- choose low-cardinality partitions
- do not partition by high-cardinality user/session IDs
- explain the operational cost of too many partitions and parts

### Inserts
- if writes are frequent and tiny, recommend batching or `async_insert`
- mention idempotent retry strategy and consistent batches when relevant
- call out part explosion risk early

### Mutations
- avoid frequent or large UPDATE/DELETE mutations on high-volume tables
- if mutations are necessary, recommend observability via `system.mutations` and a kill/runbook

### Materialized views vs projections
- choose **materialized views** for ETL, joins, denormalization, rollups, ingestion-time filtering, or explicit target-table control
- choose **projections** for alternate single-table layouts and transparent query acceleration
- explicitly note where projections do *not* fit: joins, filtered definitions, FINAL-heavy patterns, non-MergeTree tables

### OPTIMIZE FINAL
- do not recommend `OPTIMIZE FINAL` casually
- distinguish `OPTIMIZE FINAL` from query-time `FINAL`
- only suggest it for narrow operational edge cases with a warning

## Multi-agent plan (when the task is large)
If multi-agent is enabled, suggest or spawn these roles:
- `schema_modeler`: engine, DDL, ORDER BY, partitioning, TTL
- `ingest_strategist`: insert path, batching, async_insert, queueing, dedup
- `query_profiler`: query_log analysis, EXPLAIN, read amplification, join rewrites
- `storage_ops`: parts, merges, mutations, disk usage, replication, recovery
- `community_risk_reviewer`: scan docs/issues/community wisdom for sharp edges and version-specific gotchas

Use read-only exploration for evidence gathering and keep synthesis in the parent thread.

## Output contract
Every final answer using this skill should contain:
1. **Diagnosis / target state**
2. **Concrete SQL or config**
3. **Why this design matches ClickHouse internals**
4. **Risks / tradeoffs**
5. **Validation steps**
6. **If relevant: rollback plan**

## Included resources
Open only what you need:
- `references/SCHEMA_DESIGN.md`
- `references/INGESTION_AND_PARTS.md`
- `references/QUERY_TUNING.md`
- `references/MVS_PROJECTIONS_TTL.md`
- `references/OPERATIONS_AND_DIAGNOSTICS.md`
- `references/TROUBLESHOOTING.md`
- `references/COMMUNITY_NOTES.md`
- `assets/templates/merge_tree_template.sql`
- `assets/templates/materialized_view_template.sql`
- `assets/templates/projection_template.sql`
- `assets/templates/diagnostic_queries.sql`
- `prompts/AGENT_PROMPT.md`
- `prompts/MULTI_AGENT_PROMPT.md`
