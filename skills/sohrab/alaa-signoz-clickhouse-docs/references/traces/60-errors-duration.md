# Trace errors and duration examples

Read the [signal prerequisites](../clickhouse-traces-reference.md) before this topic.

### Error spans per service per minute

No resource CTE here: the query breaks *down* by service rather than filtering *to* one, so a CTE
over every fingerprint in the window would widen the key range instead of narrowing it.

```sql
SELECT
    toStartOfInterval(timestamp, INTERVAL 1 MINUTE) AS ts,
    resource.service.name::String AS `service.name`,
    toFloat64(count()) AS value
FROM signoz_traces.distributed_signoz_index_v3
WHERE timestamp BETWEEN $start_datetime AND $end_datetime
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
  AND has_error = true
  AND `service.name` IS NOT NULL
GROUP BY `service.name`, ts
ORDER BY ts ASC
```

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
  AND http_method != ''
GROUP BY http_method
ORDER BY avg_duration_nano DESC
LIMIT 100
```
