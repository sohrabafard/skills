# ClickHouse Logs Query Reference for SigNoz

Read this only for SigNoz dashboard-panel SQL over log records. Logs Explorer uses Query Builder and
search syntax unless the user asked for raw SQL for a panel.

All tables live in the `signoz_logs` database. The rules that hold on every query — the time bound,
the bucket predicate and its reason, the panel shape, the grouping ceiling — are stated once in
`SKILL.md`. This file carries what is specific to logs.

## Tables

### `distributed_logs_v2`

The log record table. Columns this skill uses:

- `timestamp` — nanoseconds
- `ts_bucket_start` — seconds; the bucket-first key column
- `resource_fingerprint` — join key to the resource table
- `trace_id`, `span_id`
- `severity_text`, `severity_number`
- `body` — the raw record text
- `body_v2`, `body_promoted` — see *Searching the body* below
- `attributes_string`, `attributes_number`, `attributes_bool` — maps
- `resource` — a native ClickHouse `JSON` column
- `scope_name`, `scope_version`

### `distributed_logs_v2_resource`

Carries `fingerprint`, `labels`, `seen_at_ts_bucket_start`. Use it in a resource-filter CTE, and
only when the query filters on a resource attribute.

## Time variables and the bucket predicate

```sql
WHERE timestamp >= $start_timestamp_nano
  AND timestamp <= $end_timestamp_nano
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
```

`$start_timestamp_nano` and `$end_timestamp_nano` are nanoseconds; `$start_timestamp` and
`$end_timestamp` are seconds. Mixing the two units silently returns zero rows rather than an error,
which is the most common defect in a hand-written logs panel.

## The resource CTE

```sql
WITH __resource_filter AS (
    SELECT fingerprint
    FROM signoz_logs.distributed_logs_v2_resource
    WHERE (simpleJSONExtractString(labels, 'service.name') = '{{service_name}}')
      AND seen_at_ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
)
SELECT ...
FROM signoz_logs.distributed_logs_v2
WHERE resource_fingerprint GLOBAL IN __resource_filter
```

`GLOBAL IN`, not `IN`: on a clustered install a plain `IN` evaluates the subquery on every shard
against that shard's local data, so the fingerprint set is incomplete and rows go missing without an
error. Omit the CTE entirely when the query filters no resource attribute — it is then pure added
scan.

## Column access

| Instead of | Use | Why |
|---|---|---|
| `attributes_string['method']` | `attribute_string_method` | materialized column, no map lookup per row |
| `attributes_number['response.time']` | `attribute_number_response$$time` | `$$` substitutes `.` in a materialized column name |
| `attributes_bool['is_error']` | `attribute_bool_is_error` | same |

Each materialized column has a companion `attribute_<type>_<key>_exists` of type `Bool`. Test that
rather than `mapContains(attributes_string, 'key')` when the materialized column exists, because the
`_exists` column is a stored value and `mapContains` is a per-row map scan.

A key with no materialized column is still reachable through the map, and
`mapContains(attributes_string, 'container_name')` is the correct existence test there.

Resource attributes read as `resource.service.name::String`. **The `resource` JSON column caps
distinct dynamic paths at 100** (`MaxDynamicPaths: 100` in the schema migrator, identically for
traces). Resource attributes beyond that cap land in the shared dynamic store and are read more
slowly. Do not assume `resource.anything::String` performs like a column on an install with wide
resource attributes; confirm with `DESCRIBE`.

Convert time for display with `fromUnixTimestamp64Nano(timestamp)`, and bucket with
`toStartOfInterval(fromUnixTimestamp64Nano(timestamp), INTERVAL 1 MINUTE) AS ts`.

## Searching the body

`logs_v2` carries three body columns, and the difference between them decides whether a text search
scans or skips:

- `body` — the raw text. **No index.** A `LIKE '%needle%'` over `body` reads every row in range.
- `body_v2` — a ClickHouse `JSON` column with one typed path, `message String`, and
  `MaxDynamicPaths: 0`. It carries four skipping indexes: `ngrambf_v1(4, 15000, 3, 0)` and
  `tokenbf_v1(10000, 2, 0)` over its full-text expression, and the same pair over its paths
  expression.
- `body_promoted` — a `JSON` column holding paths promoted out of the record.

So: **express a body search against `body_v2` so the bloom-filter indexes can skip granules, and
keep `body` for display.** The ngram index is built at n=4, so a substring shorter than four
characters cannot use it and degrades to a full scan — search for a longer fragment, or a whole
token so the token index applies.

Confirm these columns exist first: they arrive with a SigNoz upgrade, an install behind it has only
`body`, and `scripts/check-signoz-schema.py` reports which are present.

## Panel shapes

### Timeseries

```sql
WITH __resource_filter AS (
    SELECT fingerprint
    FROM signoz_logs.distributed_logs_v2_resource
    WHERE (simpleJSONExtractString(labels, 'service.name') = '{{service_name}}')
      AND seen_at_ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
)
SELECT
    toStartOfInterval(fromUnixTimestamp64Nano(timestamp), INTERVAL 1 MINUTE) AS ts,
    toFloat64(count()) AS value
FROM signoz_logs.distributed_logs_v2
WHERE resource_fingerprint GLOBAL IN __resource_filter
  AND timestamp >= $start_timestamp_nano
  AND timestamp <= $end_timestamp_nano
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
GROUP BY ts
ORDER BY ts ASC
```

### Value widget

```sql
SELECT
    toFloat64(count()) AS value
FROM signoz_logs.distributed_logs_v2
WHERE timestamp >= $start_timestamp_nano
  AND timestamp <= $end_timestamp_nano
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
  AND severity_text = 'ERROR'
```

### Table

```sql
SELECT
    resource.service.name::String AS `service.name`,
    toFloat64(count()) AS value
FROM signoz_logs.distributed_logs_v2
WHERE timestamp >= $start_timestamp_nano
  AND timestamp <= $end_timestamp_nano
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
GROUP BY `service.name`
ORDER BY value DESC
LIMIT 100
```

## Worked queries

### Log count per minute by container

```sql
SELECT
    toStartOfInterval(fromUnixTimestamp64Nano(timestamp), INTERVAL 1 MINUTE) AS ts,
    attributes_string['container_name'] AS container_name,
    toFloat64(count()) AS value
FROM signoz_logs.distributed_logs_v2
WHERE timestamp >= $start_timestamp_nano
  AND timestamp <= $end_timestamp_nano
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
  AND mapContains(attributes_string, 'container_name')
GROUP BY container_name, ts
ORDER BY ts ASC
```

### Error records per service per minute

No resource CTE here: the query breaks *down* by service rather than filtering *to* one, so a CTE
over every fingerprint in the window would widen the key range instead of narrowing it.

```sql
SELECT
    toStartOfInterval(fromUnixTimestamp64Nano(timestamp), INTERVAL 1 MINUTE) AS ts,
    resource.service.name::String AS `service.name`,
    toFloat64(count()) AS value
FROM signoz_logs.distributed_logs_v2
WHERE timestamp >= $start_timestamp_nano
  AND timestamp <= $end_timestamp_nano
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
  AND severity_text = 'ERROR'
  AND `service.name` IS NOT NULL
GROUP BY `service.name`, ts
ORDER BY ts ASC
```

### Largest records, for payload auditing

```sql
WITH __resource_filter AS (
    SELECT fingerprint
    FROM signoz_logs.distributed_logs_v2_resource
    WHERE (simpleJSONExtractString(labels, 'service.name') = '{{service_name}}')
      AND seen_at_ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
)
SELECT
    fromUnixTimestamp64Nano(timestamp) AS ts,
    length(body) AS size_bytes,
    trace_id,
    span_id
FROM signoz_logs.distributed_logs_v2
WHERE resource_fingerprint GLOBAL IN __resource_filter
  AND timestamp BETWEEN $start_timestamp_nano AND $end_timestamp_nano
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
ORDER BY size_bytes DESC
LIMIT 10
```

It returns the size and the correlation ids but not `body`, because the records it surfaces are by
construction the ones most likely to hold a payload. Add `body` only once the requester has said the
panel may display customer text.
