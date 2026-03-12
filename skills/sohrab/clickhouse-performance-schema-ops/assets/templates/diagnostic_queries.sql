
-- Common diagnostics

-- Part counts by table
SELECT
    database,
    table,
    count() AS active_parts,
    sum(rows) AS rows,
    formatReadableSize(sum(bytes_on_disk)) AS bytes_on_disk
FROM system.parts
WHERE active
GROUP BY database, table
ORDER BY active_parts DESC;

-- Part counts by partition
SELECT
    database,
    table,
    partition,
    count() AS active_parts,
    sum(rows) AS rows
FROM system.parts
WHERE active
GROUP BY database, table, partition
ORDER BY active_parts DESC
LIMIT 100;

-- Recent mutations
SELECT
    database,
    table,
    mutation_id,
    command,
    create_time,
    is_done,
    latest_fail_reason
FROM system.mutations
ORDER BY create_time DESC
LIMIT 100;

-- Slow / expensive queries
SELECT
    event_time,
    query_duration_ms,
    read_rows,
    formatReadableSize(read_bytes) AS read_bytes,
    result_rows,
    result_bytes,
    memory_usage,
    query
FROM system.query_log
WHERE type = 'QueryFinish'
ORDER BY event_time DESC
LIMIT 50;

-- Recent part events
SELECT
    event_type,
    database,
    table,
    partition_id,
    rows,
    formatReadableSize(bytes_uncompressed) AS uncompressed,
    event_time
FROM system.part_log
ORDER BY event_time DESC
LIMIT 100;
