# Log schema

Read the [signal prerequisites](../clickhouse-logs-reference.md) before this topic.

## Tables

### `distributed_logs_v2`

The log record table. Columns this skill uses:

- `timestamp` — nanoseconds
- `ts_bucket_start` — seconds; the bucket-first key column
- `resource_fingerprint` — join key to the resource table
- `trace_id`, `span_id`
- `severity_text`, `severity_number`
- `body` — the raw record text
- `body_v2`, `body_promoted` — see [body search](40-body-search.md)
- `attributes_string`, `attributes_number`, `attributes_bool` — maps
- `resource` — a native ClickHouse `JSON` column
- `scope_name`, `scope_version`

### `distributed_logs_v2_resource`

Carries `fingerprint`, `labels`, `seen_at_ts_bucket_start`. Use it in a resource-filter CTE, and
only when the query filters on a resource attribute.
