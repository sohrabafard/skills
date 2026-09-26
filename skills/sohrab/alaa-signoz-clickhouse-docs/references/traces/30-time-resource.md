# Trace time and resource filtering

Read the [signal prerequisites](../clickhouse-traces-reference.md) before this topic.

## Time variables and the bucket predicate

```sql
WHERE timestamp BETWEEN $start_datetime AND $end_datetime
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
```

`$start_datetime` and `$end_datetime` are `DateTime`; `$start_timestamp` and `$end_timestamp` are
seconds. Traces do **not** use the nanosecond variables that logs use.

## The resource CTE

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
```

`GLOBAL IN`, not `IN`: a plain `IN` evaluates the subquery per shard against that shard's local data,
so the fingerprint set is incomplete and spans go missing with no error.
