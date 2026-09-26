# Spans with missing parents

Read the [signal prerequisites](../clickhouse-traces-reference.md) before this topic.

### Recent spans whose parent span is missing

Lists spans whose `parent_span_id` is non-empty but which no collected span in the same trace
matches. It tells you **which** spans are orphaned. Read `../40-missing-spans.md` for **why**, which is
what closes the ticket.

```sql
WITH __resource_filter AS (
    SELECT fingerprint
    FROM signoz_traces.distributed_traces_v3_resource
    WHERE (simpleJSONExtractString(labels, 'service.name') = '{{service_name}}')
      AND seen_at_ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
),
__spans AS (
    SELECT trace_id, span_id, parent_span_id, name, kind_string, timestamp
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

This query is bounded by the panel window, so it finds orphans only among spans that arrived inside
it. A parent that fell outside the window looks identical to a parent that was never exported —
widen the window before concluding the latter.
