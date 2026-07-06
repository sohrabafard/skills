# ClickHouse Traces Query Reference for SigNoz

Use this file only for SigNoz traces dashboard SQL.

All tables live in the `signoz_traces` database.

## Main tables

### `distributed_signoz_index_v3`

Primary table for spans.
Important columns include:

- `ts_bucket_start`
- `resource_fingerprint`
- `timestamp`
- `trace_id`
- `span_id`
- `name`
- `kind`, `kind_string`
- `duration_nano`
- `status_code`, `status_code_string`
- `attributes_string`, `attributes_number`, `attributes_bool`
- `resource`
- `http_method`, `http_url`, `http_host`
- `db_name`, `db_operation`
- `has_error`

### `distributed_traces_v3_resource`

Use this table in a resource-filter CTE when filtering by resource attributes such as `service.name`, `deployment.environment`, or `k8s.namespace.name`.

### `distributed_signoz_error_index_v2`

Useful when the user asks for exception-event style data rather than general spans.

## Non-negotiable patterns

### 1. Add the bucket filter

Always pair the time filter with the bucket filter:

```sql
WHERE timestamp BETWEEN $start_datetime AND $end_datetime
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
```

The `- 1800` is required because SigNoz stores 30-minute buckets.

### 2. Use a resource CTE only when needed

If the query filters on a resource attribute, use this shape:

```sql
WITH __resource_filter AS (
    SELECT fingerprint
    FROM signoz_traces.distributed_traces_v3_resource
    WHERE (simpleJSONExtractString(labels, 'service.name') = '{{service_name}}')
      AND seen_at_ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
)
SELECT ...
FROM signoz_traces.distributed_signoz_index_v3
WHERE resource_fingerprint GLOBAL IN __resource_filter
  AND ...
```

Do not add the CTE if the query does not filter on resource attributes.

### 3. Prefer indexed or pre-extracted columns

Prefer these over map access when they exist:

| Slower form | Prefer this |
|---|---|
| `attributes_string['http.route']` | `attribute_string_http$$route` |
| `attributes_string['db.system']` | `attribute_string_db$$system` |
| `attributes_string['rpc.method']` | `attribute_string_rpc$$method` |
| `attributes_string['peer.service']` | `attribute_string_peer$$service` |
| `resources_string['service.name']` | `resource_string_service$$name` |

Also prefer pre-extracted columns such as:

- `http_method`
- `http_url`
- `http_host`
- `db_name`
- `db_operation`
- `duration_nano`
- `has_error`

## Resource attribute syntax

### In `SELECT` or `GROUP BY`

```sql
resource.service.name::String
resource.deployment.environment::String
```

### In the CTE `WHERE`

```sql
simpleJSONExtractString(labels, 'service.name') = '{{service_name}}'
```

## Panel shapes

### Timeseries

Return `ts` and `value`.

```sql
WITH __resource_filter AS (
    SELECT fingerprint
    FROM signoz_traces.distributed_traces_v3_resource
    WHERE (simpleJSONExtractString(labels, 'service.name') = '{{service_name}}')
      AND seen_at_ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
)
SELECT
    toStartOfInterval(timestamp, INTERVAL 1 MINUTE) AS ts,
    toFloat64(count()) AS value
FROM signoz_traces.distributed_signoz_index_v3
WHERE resource_fingerprint GLOBAL IN __resource_filter
  AND timestamp BETWEEN $start_datetime AND $end_datetime
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
GROUP BY ts
ORDER BY ts ASC
```

### Value widget

Return one row with `value`.

```sql
WITH __resource_filter AS (
    SELECT fingerprint
    FROM signoz_traces.distributed_traces_v3_resource
    WHERE (simpleJSONExtractString(labels, 'service.name') = '{{service_name}}')
      AND seen_at_ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
)
SELECT
    toFloat64(count()) AS value
FROM signoz_traces.distributed_signoz_index_v3
WHERE resource_fingerprint GLOBAL IN __resource_filter
  AND timestamp BETWEEN $start_datetime AND $end_datetime
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
  AND has_error = true
```

### Table

Return labeled grouped columns.

```sql
WITH __resource_filter AS (
    SELECT fingerprint
    FROM signoz_traces.distributed_traces_v3_resource
    WHERE (simpleJSONExtractString(labels, 'service.name') = '{{service_name}}')
      AND seen_at_ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
)
SELECT
    http_method,
    toFloat64(avg(duration_nano)) AS avg_duration_nano
FROM signoz_traces.distributed_signoz_index_v3
WHERE resource_fingerprint GLOBAL IN __resource_filter
  AND timestamp BETWEEN $start_datetime AND $end_datetime
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
  AND http_method IS NOT NULL
  AND http_method != ''
GROUP BY http_method
ORDER BY avg_duration_nano DESC
```

## Common query patterns

### Error spans per service per minute

```sql
WITH __resource_filter AS (
    SELECT fingerprint
    FROM signoz_traces.distributed_traces_v3_resource
    WHERE seen_at_ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
)
SELECT
    toStartOfInterval(timestamp, INTERVAL 1 MINUTE) AS ts,
    resource.service.name::String AS `service.name`,
    toFloat64(count()) AS value
FROM signoz_traces.distributed_signoz_index_v3
WHERE resource_fingerprint GLOBAL IN __resource_filter
  AND timestamp BETWEEN $start_datetime AND $end_datetime
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
  AND has_error = true
  AND `service.name` IS NOT NULL
GROUP BY `service.name`, ts
ORDER BY ts ASC
```

### Recent spans whose parent span is missing

Use this as a troubleshooting query for SigNoz "missing spans" warnings. It lists spans whose `parent_span_id` is non-empty but no collected span in the same trace has that span id.

```sql
WITH __resource_filter AS (
    SELECT fingerprint
    FROM signoz_traces.distributed_traces_v3_resource
    WHERE (simpleJSONExtractString(labels, 'service.name') = '{{service_name}}')
      AND seen_at_ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
),
__spans AS (
    SELECT
        trace_id,
        span_id,
        parent_span_id,
        name,
        kind_string,
        timestamp
    FROM signoz_traces.distributed_signoz_index_v3
    WHERE resource_fingerprint GLOBAL IN __resource_filter
      AND timestamp BETWEEN $start_datetime AND $end_datetime
      AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
)
SELECT
    child.timestamp,
    child.trace_id,
    child.name,
    child.kind_string,
    child.span_id,
    child.parent_span_id
FROM __spans AS child
LEFT JOIN __spans AS parent
    ON parent.trace_id = child.trace_id
   AND parent.span_id = child.parent_span_id
WHERE child.parent_span_id != ''
  AND (parent.span_id = '' OR parent.span_id IS NULL)
ORDER BY child.timestamp DESC
LIMIT 100
```

For Laravel/PHP services, a common application-side cause is generating a fallback `traceparent` for response/log correlation and then extracting that fallback as the OpenTelemetry parent. Fix the instrumentation so generated or invalid inbound context starts a root server span; only real inbound trace context should be extracted as a parent.

### Average duration by HTTP method for one service

```sql
WITH __resource_filter AS (
    SELECT fingerprint
    FROM signoz_traces.distributed_traces_v3_resource
    WHERE (simpleJSONExtractString(labels, 'service.name') = '{{service_name}}')
      AND seen_at_ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
)
SELECT
    http_method,
    toFloat64(avg(duration_nano)) AS avg_duration_nano
FROM signoz_traces.distributed_signoz_index_v3
WHERE resource_fingerprint GLOBAL IN __resource_filter
  AND timestamp BETWEEN $start_datetime AND $end_datetime
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
  AND http_method IS NOT NULL
  AND http_method != ''
GROUP BY http_method
ORDER BY avg_duration_nano DESC
```

## Final checklist

Before finalizing a traces query, check these points:

- correct table: `distributed_signoz_index_v3`
- correct time variables: `$start_datetime`, `$end_datetime`, `$start_timestamp`, `$end_timestamp`
- `ts_bucket_start` filter present
- resource CTE only when filtering on resource attributes
- `GLOBAL IN` used for the resource subquery
- indexed or pre-extracted columns used where possible
- timeseries ordered by `ts ASC`
- no old `resources_string[...]` access when a better field exists

# 2026 production update

Use this reference only for SigNoz Dashboard/Alert ClickHouse SQL over traces/spans. Traces Explorer uses Query Builder/search syntax unless the user explicitly requests raw SQL for a dashboard/alert.

For sensitive systems:

- Keep the `ts_bucket_start` and timestamp filters aligned with the panel window.
- Prefer route templates, service names, operation names, status codes, and bounded attributes for grouping.
- Do not group by raw URL, user ID, request ID, trace ID, span ID, email, phone, token, or payload-derived values except in a bounded forensic table with explicit approval.
- Use `validation-checklists.md` before finalizing a query for a production dashboard or alert.
