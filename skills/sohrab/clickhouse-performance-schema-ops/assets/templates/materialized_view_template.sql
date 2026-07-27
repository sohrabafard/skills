-- Incremental materialized view template: explicit target table plus the view
-- that populates it. Every <angle-bracket> token is a placeholder.
--
-- Use a materialized view when the shape of the answer differs from the shape of
-- the row. When one table merely needs a second physical ordering, use
-- projection_template.sql instead (references/50-mvs-projections-and-ttl.md).

-- 1) The target table. It is an ordinary table: it needs the tenant column first
--    in its own ORDER BY for exactly the reason the base table does.
CREATE TABLE IF NOT EXISTS <database>.<rollup_table>
(
    bucket DateTime,
    <tenant_column> String DEFAULT '',
    <dimension_column> LowCardinality(String) DEFAULT '',
    -- Aggregate states, not finished values. Every reader must use a -Merge
    -- combinator over these columns.
    events AggregateFunction(count),
    unique_events AggregateFunction(uniqExact, String)
)
ENGINE = AggregatingMergeTree
PARTITION BY toYYYYMM(bucket)
ORDER BY (<tenant_column>, bucket, <dimension_column>);

-- 2) The view. It fires on each block inserted into the source from now on, and
--    sees nothing already present. History is a separate backfill, step 3.
CREATE MATERIALIZED VIEW IF NOT EXISTS <database>.mv_<rollup_table>
TO <database>.<rollup_table>
AS
SELECT
    toStartOfHour(event_time) AS bucket,
    <tenant_column>,
    <dimension_column>,
    countState() AS events,
    -- uniqExactState over the per-event identifier, not countState, wherever an
    -- exact count is claimed: a retried insert against a non-replicated table
    -- duplicates rows, and the view re-fires on the duplicate block
    -- (references/30-ingest-and-parts.md).
    uniqExactState(<event_id_column>) AS unique_events
FROM <database>.<source_table>
GROUP BY
    bucket,
    <tenant_column>,
    <dimension_column>;

-- 3) Backfill one partition at a time, oldest first, verifying each before the
--    next. A single INSERT ... SELECT over a full raw table is the memory
--    failure everyone has already had.
-- INSERT INTO <database>.<rollup_table>
-- SELECT
--     toStartOfHour(event_time) AS bucket,
--     <tenant_column>,
--     <dimension_column>,
--     countState(),
--     uniqExactState(<event_id_column>)
-- FROM <database>.<source_table>
-- WHERE event_date >= '<partition_start>' AND event_date < '<partition_end>'
-- GROUP BY bucket, <tenant_column>, <dimension_column>;

-- 4) Read it with -Merge combinators, a tenant predicate, and a bounded window.
-- SELECT
--     bucket,
--     <dimension_column>,
--     countMerge(events)         AS events,
--     uniqExactMerge(unique_events) AS unique_events
-- FROM <database>.<rollup_table>
-- WHERE <tenant_column> = {tenant:String}
--   AND bucket >= {from:DateTime} AND bucket < {to:DateTime}
-- GROUP BY bucket, <dimension_column>;

-- 5) Parity proof before this ships: compare the backfilled partition's
--    aggregates against the same aggregate computed from the source, then insert
--    one new batch and show it lands in both (references/80-proof-and-validation.md).
