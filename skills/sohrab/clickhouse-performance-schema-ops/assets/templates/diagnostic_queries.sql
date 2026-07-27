-- Diagnostic queries for the playbooks in references/60-operations-and-diagnostics.md.
-- Run the one the playbook names and paste its result before proposing a change.
-- Replace <angle-bracket> tokens. These are read-only; none of them modifies state.
--
-- Check first that the log tables are enabled on this server, so an empty result
-- reads as "logging is off" rather than "nothing happened":
SELECT name, engine FROM system.tables
WHERE database = 'system'
  AND name IN ('query_log', 'query_thread_log', 'part_log', 'metric_log');

-- ---------------------------------------------------------------------------
-- Playbook: TOO_MANY_PARTS, or part counts climbing
-- ---------------------------------------------------------------------------

-- Parts per table.
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

-- Parts per partition. This is the query that separates "too many partitions"
-- from "inserts are too small": many partitions with few parts each is the
-- first, one partition with hundreds of parts is the second.
SELECT
    database,
    table,
    partition,
    count() AS active_parts,
    sum(rows) AS rows,
    formatReadableSize(sum(bytes_on_disk)) AS bytes_on_disk,
    min(rows) AS smallest_part_rows
FROM system.parts
WHERE active AND database = '<database>'
GROUP BY database, table, partition
ORDER BY active_parts DESC
LIMIT 100;

-- Rows per insert as actually observed, against the published bar of at least
-- 1,000 rows per insert and around one insert per second.
SELECT
    toStartOfMinute(event_time) AS minute,
    count() AS inserted_parts,
    sum(rows) AS rows,
    round(sum(rows) / count()) AS rows_per_part
FROM system.part_log
WHERE event_type = 'NewPart'
  AND database = '<database>' AND table = '<table>'
  AND event_time > now() - INTERVAL 1 HOUR
GROUP BY minute
ORDER BY minute DESC;

-- Merges running right now, with their memory use.
SELECT
    database, table, elapsed, progress, num_parts,
    formatReadableSize(memory_usage) AS memory_usage,
    result_part_name
FROM system.merges
ORDER BY elapsed DESC;

-- ---------------------------------------------------------------------------
-- Playbook: a mutation is not finishing
-- ---------------------------------------------------------------------------

SELECT
    database, table, mutation_id, command, create_time,
    is_done, parts_to_do, latest_fail_reason, latest_fail_time
FROM system.mutations
WHERE is_done = 0 OR latest_fail_reason != ''
ORDER BY create_time DESC
LIMIT 100;

-- ---------------------------------------------------------------------------
-- Playbook: one query is slow
-- ---------------------------------------------------------------------------

-- Read amplification: read_rows / result_rows is the number to look at first.
SELECT
    event_time,
    query_duration_ms,
    read_rows,
    result_rows,
    if(result_rows = 0, NULL, round(read_rows / result_rows)) AS read_per_returned,
    formatReadableSize(read_bytes) AS read_bytes,
    formatReadableSize(memory_usage) AS memory_usage,
    normalized_query_hash,
    substring(query, 1, 400) AS query
FROM system.query_log
WHERE type = 'QueryFinish'
  AND event_time > now() - INTERVAL 1 HOUR
  AND has(databases, '<database>')
ORDER BY read_bytes DESC
LIMIT 50;

-- The same query before and after a change, matched on its normalized hash.
-- This is the evidence a performance claim needs: bytes read, not wall time.
SELECT
    normalized_query_hash,
    count() AS runs,
    round(avg(read_rows)) AS avg_read_rows,
    formatReadableSize(avg(read_bytes)) AS avg_read_bytes,
    round(avg(query_duration_ms)) AS avg_ms
FROM system.query_log
WHERE type = 'QueryFinish'
  AND normalized_query_hash = <hash>
  AND event_time > now() - INTERVAL 1 DAY
GROUP BY normalized_query_hash;

-- Queries that failed, including limit trips such as max_result_rows and
-- max_execution_time (references/70-failure-and-degradation.md).
SELECT
    event_time, exception_code, exception, substring(query, 1, 300) AS query
FROM system.query_log
WHERE type != 'QueryFinish' AND event_time > now() - INTERVAL 1 HOUR
ORDER BY event_time DESC
LIMIT 50;

-- ---------------------------------------------------------------------------
-- Playbook: disk growing faster than rows
-- ---------------------------------------------------------------------------

SELECT
    database, table, active,
    count() AS parts, sum(rows) AS rows,
    formatReadableSize(sum(bytes_on_disk)) AS bytes_on_disk
FROM system.parts
WHERE database = '<database>'
GROUP BY database, table, active
ORDER BY table, active DESC;

-- Compression achieved per column: a wide String where a LowCardinality belongs
-- shows up here first.
SELECT
    name,
    type,
    formatReadableSize(sum(data_compressed_bytes)) AS compressed,
    formatReadableSize(sum(data_uncompressed_bytes)) AS uncompressed,
    round(sum(data_uncompressed_bytes) / nullIf(sum(data_compressed_bytes), 0), 1) AS ratio
FROM system.parts_columns
WHERE active AND database = '<database>' AND table = '<table>'
GROUP BY name, type
ORDER BY sum(data_compressed_bytes) DESC;

-- ---------------------------------------------------------------------------
-- Schema drift: does the deployed table still match the DDL file?
-- ---------------------------------------------------------------------------

SELECT name, type, default_kind, default_expression, position
FROM system.columns
WHERE database = '<database>' AND table = '<table>'
ORDER BY position;

SELECT engine, partition_key, sorting_key, primary_key, sampling_key
FROM system.tables
WHERE database = '<database>' AND name = '<table>';

-- ---------------------------------------------------------------------------
-- Effective settings on this server, rather than a quoted default
-- ---------------------------------------------------------------------------

SELECT name, value, changed, description
FROM system.settings
WHERE name IN (
    'max_execution_time', 'max_result_rows', 'result_overflow_mode',
    'timeout_overflow_mode', 'readonly', 'async_insert', 'wait_for_async_insert'
);

SELECT name, value, description
FROM system.merge_tree_settings
WHERE name IN (
    'parts_to_delay_insert', 'parts_to_throw_insert', 'max_parts_in_total',
    'non_replicated_deduplication_window'
);

-- Grants actually held by the configured role. This is the artifact that settles
-- whether the read role is SELECT-only (references/85-access-and-configuration.md).
SHOW GRANTS FOR <user>;
