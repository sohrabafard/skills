-- Projection template: a second physical ordering of one table, chosen by the
-- optimizer without any query changing. Every <angle-bracket> token is a
-- placeholder.
--
-- Use a projection only when the base table's ORDER BY is wrong for one access
-- path and you cannot change it. A projection cannot join, cannot filter its own
-- definition, cannot be chained, does not work with FINAL queries, is available
-- only on MergeTree-family engines, and is incompatible with lightweight-deleted
-- rows by default (references/50-mvs-projections-and-ttl.md).

-- 1) Add the projection. This changes the table definition and nothing on disk.
ALTER TABLE <database>.<table>
ADD PROJECTION <projection_name>
(
    SELECT
        <tenant_column>,
        <identifier_column>,
        event_time,
        <dimension_column>
    -- Order the projection for the access path the base table cannot serve. The
    -- tenant column still leads: a projection is not an exemption from tenant
    -- scoping, and a projection ordered without it prunes nothing for a
    -- tenant-filtered query.
    ORDER BY (<tenant_column>, <identifier_column>, event_time)
);

-- 2) Materialize it. This rewrites data and is the expensive step; run it in a
--    window where that IO is acceptable, and say which window in the change
--    request. New parts carry the projection automatically; existing parts do
--    not until this completes.
ALTER TABLE <database>.<table> MATERIALIZE PROJECTION <projection_name>;

-- 3) Prove the optimizer actually uses it, because adding a projection that is
--    never selected is pure write amplification. Run the target query and read
--    the projection name out of the query log:
-- SELECT
--     query,
--     projections,
--     read_rows,
--     formatReadableSize(read_bytes) AS read_bytes
-- FROM system.query_log
-- WHERE type = 'QueryFinish'
--   AND event_time > now() - INTERVAL 10 MINUTE
--   AND query LIKE '%<table>%'
-- ORDER BY event_time DESC
-- LIMIT 20;

-- 4) Rollback is cheap and leaves the base table untouched:
-- ALTER TABLE <database>.<table> DROP PROJECTION <projection_name>;
