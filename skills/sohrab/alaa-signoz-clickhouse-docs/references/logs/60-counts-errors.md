# Log counts and error examples

Read the [signal prerequisites](../clickhouse-logs-reference.md) before this topic.

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
