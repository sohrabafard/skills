-- Incremental materialized view template: explicit target table plus the view
-- that populates it. Every <angle-bracket> token is a placeholder.
--
-- Use a materialized view when the shape of the answer differs from the shape of
-- the row. When one table merely needs a second physical ordering, use
-- projection_template.sql instead (references/50-mvs-projections-and-ttl.md).

-- 1) The target table. It is an ordinary table: it needs the tenant column first
--    in its own ORDER BY for exactly the reason the base table does.
CREATE TABLE IF NOT EXISTS database.rollup_table
(
    bucket DateTime,
    project_id String DEFAULT '',
    dimension_column LowCardinality(String) DEFAULT '',
    -- Aggregate states, not finished values. Every reader must use a -Merge
    -- combinator over these columns.
    events AggregateFunction(count),
    unique_events AggregateFunction(uniqExact, String)
)
ENGINE = AggregatingMergeTree
PARTITION BY toYYYYMM(bucket)
ORDER BY (project_id, bucket, dimension_column);

-- 2) Pause and drain the source writer before creating the live view. Keep it
--    paused through backfill and parity. For online backfill, add and prove
--    complementary live/history predicates before applying this template
--    (references/50-mvs-projections-and-ttl.md).
--    Provision the definer with source SELECT and target INSERT first. On first
--    apply and every rerun, verify stored security clauses and effective grants.
--    IF NOT EXISTS leaves an older view definition in place.
CREATE MATERIALIZED VIEW IF NOT EXISTS database.mv_rollup_table
TO database.rollup_table
DEFINER = view_definer_user SQL SECURITY DEFINER
AS
SELECT
    toStartOfHour(event_time) AS bucket,
    project_id,
    dimension_column,
    countState() AS events,
    -- uniqExactState over the per-event identifier, not countState, wherever an
    -- exact count is claimed: a retried insert against a non-replicated table
    -- duplicates rows, and the view re-fires on the duplicate block
    -- (references/30-ingest-and-parts.md).
    uniqExactState(event_id_column) AS unique_events
FROM database.source_table
GROUP BY
    bucket,
    project_id,
    dimension_column;

-- 3) With the writer still paused, backfill bounded partitions. Before retrying
--    an uncertain backfill, reconcile its target range to avoid counting it twice.
-- INSERT INTO database.rollup_table
-- SELECT
--     toStartOfHour(event_time) AS bucket,
--     project_id,
--     dimension_column,
--     countState(),
--     uniqExactState(event_id_column)
-- FROM database.source_table
-- WHERE event_date >= 'partition_start' AND event_date < 'partition_end'
-- GROUP BY bucket, project_id, dimension_column;

-- 4) Read it with -Merge combinators, a tenant predicate, and a bounded window.
-- SELECT
--     bucket,
--     dimension_column,
--     countMerge(events)         AS events,
--     uniqExactMerge(unique_events) AS unique_events
-- FROM database.rollup_table
-- WHERE project_id = {tenant:String}
--   AND bucket >= {from:DateTime} AND bucket < {to:DateTime}
-- GROUP BY bucket, dimension_column;

-- 5) Verify countMerge(events) and uniqExactMerge(unique_events) against the
--    source per rollup key. Resume writes after parity. Insert a fixture batch
--    at the cut and verify each event reaches its rollup exactly once
--    (references/80-proof-and-validation.md).
