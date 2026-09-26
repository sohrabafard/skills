# Log payload auditing

Read the [signal prerequisites](../clickhouse-logs-reference.md) before this topic.

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
