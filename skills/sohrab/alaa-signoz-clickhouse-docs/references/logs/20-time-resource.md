# Log time and resource filtering

Read the [signal prerequisites](../clickhouse-logs-reference.md) before this topic.

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
