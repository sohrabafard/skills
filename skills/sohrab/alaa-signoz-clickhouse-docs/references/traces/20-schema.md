# Trace schema

Read the [signal prerequisites](../clickhouse-traces-reference.md) before this topic.

## Tables

### `distributed_signoz_index_v3`

The span table. Columns this skill uses:

- `ts_bucket_start`, `resource_fingerprint`
- `timestamp`
- `trace_id`, `span_id`, `parent_span_id`
- `name`
- `kind`, `kind_string`
- `duration_nano`
- `status_code`, `status_code_string`
- `has_error`
- `attributes_string`, `attributes_number`, `attributes_bool`
- `resource`
- `http_method`, `http_url`, `http_host`
- `db_name`, `db_operation`

### `distributed_traces_v3_resource`

Carries `fingerprint`, `labels`, `seen_at_ts_bucket_start`. Use it in a resource-filter CTE, and only
when the query filters on a resource attribute.

### `distributed_signoz_error_index_v2` — conditional, confirm before use

The current schema migrator does **not** create this table; it is a v2-era table that is present on
installs upgraded from that era and may be absent on a fresh install. Confirm it before writing SQL
against it:

```sql
SHOW TABLES FROM signoz_traces LIKE 'distributed_signoz_error_index_v2';
```

If it returns nothing, answer exception questions from `distributed_signoz_index_v3` filtered on
`has_error = true` instead, and say which table you used.
