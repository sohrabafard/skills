# ClickHouse Logs Query Reference for SigNoz

Use this file only for SigNoz logs dashboard SQL.

All tables live in the `signoz_logs` database.

## Main tables

### `distributed_logs_v2`

Primary table for logs.
Important columns include:

- `timestamp` (nanoseconds)
- `ts_bucket_start`
- `trace_id`
- `span_id`
- `severity_text`, `severity_number`
- `body`
- `attributes_string`, `attributes_number`, `attributes_bool`
- `resource`
- `scope_name`, `scope_version`

### `distributed_logs_v2_resource`

Use this table in a resource-filter CTE when filtering by resource attributes such as `service.name`, `host.name`, or Kubernetes resource fields.

## Non-negotiable patterns

### 1. Use the correct time variables

Logs use nanosecond timestamps.
Always pair the nanosecond filter with the bucket filter:

```sql
WHERE timestamp >= $start_timestamp_nano
  AND timestamp <= $end_timestamp_nano
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
```

### 2. Use a resource CTE only when needed

If the query filters on a resource attribute, use this shape:

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
  AND ...
```

Do not add the CTE if there is no resource-attribute filter.

### 3. Prefer indexed columns when they exist

| Slower form | Prefer this |
|---|---|
| `attributes_string['method']` | `attribute_string_method` |
| `attributes_number['response.time']` | `attribute_number_response$$time` |
| `attributes_bool['is_error']` | `attribute_bool_is_error` |

### 4. Use `GLOBAL IN`

Always use:

```sql
resource_fingerprint GLOBAL IN __resource_filter
```

## Useful syntax

### Resource attributes in `SELECT` or `GROUP BY`

```sql
resource.service.name::String
resource.k8s.cluster.name::String
```

### Resource attributes in the CTE `WHERE`

```sql
simpleJSONExtractString(labels, 'service.name') = '{{service_name}}'
```

### Attribute access in `WHERE`

```sql
attributes_string['method'] = 'GET'
attributes_number['duration_ms'] > 1000
attributes_bool['is_error'] = true
```

### Check attribute existence

```sql
mapContains(attributes_string, 'container_name')
```

### Convert time for display

```sql
fromUnixTimestamp64Nano(timestamp)
toStartOfInterval(fromUnixTimestamp64Nano(timestamp), INTERVAL 1 MINUTE) AS ts
```

## Panel shapes

### Timeseries

Return `ts` and `value`.

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

Return one row with `value`.

```sql
WITH __resource_filter AS (
    SELECT fingerprint
    FROM signoz_logs.distributed_logs_v2_resource
    WHERE (simpleJSONExtractString(labels, 'service.name') = '{{service_name}}')
      AND seen_at_ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
)
SELECT
    toFloat64(count()) AS value
FROM signoz_logs.distributed_logs_v2
WHERE resource_fingerprint GLOBAL IN __resource_filter
  AND timestamp >= $start_timestamp_nano
  AND timestamp <= $end_timestamp_nano
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
  AND severity_text = 'ERROR'
```

### Table

Return labeled grouped columns.

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
```

## Common query patterns

### Log count per minute grouped by container name

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

### Error logs per service per minute

```sql
WITH __resource_filter AS (
    SELECT fingerprint
    FROM signoz_logs.distributed_logs_v2_resource
    WHERE seen_at_ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
)
SELECT
    toStartOfInterval(fromUnixTimestamp64Nano(timestamp), INTERVAL 1 MINUTE) AS ts,
    resource.service.name::String AS `service.name`,
    toFloat64(count()) AS value
FROM signoz_logs.distributed_logs_v2
WHERE resource_fingerprint GLOBAL IN __resource_filter
  AND timestamp >= $start_timestamp_nano
  AND timestamp <= $end_timestamp_nano
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
  AND severity_text = 'ERROR'
  AND `service.name` IS NOT NULL
GROUP BY `service.name`, ts
ORDER BY ts ASC
```

### Top 10 largest logs for payload auditing

```sql
WITH __resource_filter AS (
    SELECT fingerprint
    FROM signoz_logs.distributed_logs_v2_resource
    WHERE (simpleJSONExtractString(labels, 'service.name') = '{{service_name}}')
      AND seen_at_ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
)
SELECT
    fromUnixTimestamp64Nano(timestamp) AS ts,
    body,
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

## Final checklist

Before finalizing a logs query, check these points:

- correct table: `distributed_logs_v2`
- correct time variables: `$start_timestamp_nano`, `$end_timestamp_nano`, `$start_timestamp`, `$end_timestamp`
- `ts_bucket_start` filter present
- resource CTE only when filtering on resource attributes
- `GLOBAL IN` used for the resource subquery
- indexed columns used where possible
- timeseries ordered by `ts ASC`
- human-readable time conversion used when the panel should display timestamps clearly
