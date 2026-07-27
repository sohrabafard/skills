-- MergeTree base-table template.
--
-- Every <angle-bracket> token is a placeholder and must be replaced. This file
-- names no real database on purpose: a template carrying a live database name
-- gets copied verbatim and produces DDL that looks approved. The real analytics
-- database on this platform is created by the ingest-pipeline repository, and
-- only that repository may apply DDL against it (references/10-authority-and-change-path.md).
--
-- Before applying: run scripts/review_clickhouse_ddl.py over the result.

CREATE TABLE IF NOT EXISTS <database>.<table>
(
    -- Tenant dimension. First in ORDER BY, and required in every query.
    -- The ingest pipeline's equivalent column is `project_id String`, sourced
    -- from a gateway-supplied trusted header, never from the request body.
    <tenant_column> String DEFAULT '',

    -- Event time as sent, plus the derived columns the keys use. Deriving them
    -- with MATERIALIZED keeps the partition key and the sort key from ever
    -- disagreeing with the stored timestamp.
    <event_ts_column> UInt64 DEFAULT 0,
    event_time DateTime64(3, 'UTC') MATERIALIZED fromUnixTimestamp64Milli(toInt64(<event_ts_column>)),
    event_date Date MATERIALIZED toDate(event_time),

    -- Repeated string dimensions: LowCardinality below roughly 10,000 distinct
    -- values, with an empty-string default rather than Nullable.
    <dimension_column> LowCardinality(String) DEFAULT '',

    -- Free-form strings and counts: a typed default, not Nullable. Use
    -- Nullable(T) only where a named query must tell "absent" from "empty", and
    -- write that query's name in a comment starting `nullable:` on the column.
    <identifier_column> String DEFAULT '',
    <count_column> UInt32 DEFAULT 0,

    -- One wide provenance column, compressed harder than the defaults because
    -- it is written far more often than it is read.
    <payload_column> String CODEC(ZSTD(3))
)
ENGINE = MergeTree
-- Cluster mode replaces the line above; replication needs ClickHouse Keeper or
-- ZooKeeper 3.4.5+ running first, and the {shard} and {replica} macros defined
-- on every server (references/10-authority-and-change-path.md):
-- ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/<database>/<table>', '{replica}')
PARTITION BY toYYYYMM(event_date)
ORDER BY (<tenant_column>, event_date, <dimension_column>)
SETTINGS index_granularity = 8192;

-- Decisions this template has already made for you, and what changing one costs:
--   1. Tenant column first in ORDER BY. Removing it means every tenant query
--      reads every tenant's granules.
--   2. Monthly partitions. Finer granularity must be justified by showing the
--      retention window divided by the granularity stays under 1,000 partitions.
--   3. Three-element sort key. Add a fourth or fifth only for a query that
--      filters on it and on every element before it.
--   4. No TTL. Retention is a policy decision owned by the pipeline owner and
--      is currently open on this platform (references/50-mvs-projections-and-ttl.md).
