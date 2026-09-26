# Trace panel shapes

Read the [signal prerequisites](../clickhouse-traces-reference.md) before this topic.

## Panel shapes

### Timeseries

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

```sql
SELECT
    toFloat64(count()) AS value
FROM signoz_traces.distributed_signoz_index_v3
WHERE timestamp BETWEEN $start_datetime AND $end_datetime
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
  AND has_error = true
```

### Table

Grouped on `name`, which is the fourth sorting-key column, and filtered on `has_error`, which is the
third. Both are index-supported, so this shape is the cheap one; grouping on `http_method` instead
reads it from rows the key range already selected.

```sql
SELECT
    name,
    toFloat64(count()) AS error_spans
FROM signoz_traces.distributed_signoz_index_v3
WHERE timestamp BETWEEN $start_datetime AND $end_datetime
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
  AND has_error = true
GROUP BY name
ORDER BY error_spans DESC
LIMIT 100
```
