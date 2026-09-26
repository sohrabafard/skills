# Log panel shapes

Read the [signal prerequisites](../clickhouse-logs-reference.md) before this topic.

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
