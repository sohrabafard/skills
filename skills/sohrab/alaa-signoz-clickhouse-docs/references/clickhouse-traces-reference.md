# ClickHouse Traces Query Reference for SigNoz

Read this only for SigNoz dashboard-panel SQL over spans. Traces Explorer uses Query Builder and
search syntax unless the user asked for raw SQL for a panel.

All tables live in the `signoz_traces` database. The rules that hold on every query are stated once
in `SKILL.md`; this file carries what is specific to spans.

## The physical layout, and what every rule here follows from

Read from the SigNoz schema migrator on 2026-07-30, for `signoz_index_v3`:

```
PartitionBy: toDate(timestamp)
OrderBy:     (ts_bucket_start, resource_fingerprint, has_error, name, timestamp)
TTL:         toDateTime(timestamp) + toIntervalSecond(1296000)          -- 15 days
```

and for `traces_v3_resource`:

```
PartitionBy: toDate(seen_at_ts_bucket_start)
OrderBy:     (labels, fingerprint, seen_at_ts_bucket_start)
TTL:         toDateTime(seen_at_ts_bucket_start) + INTERVAL 1296000 SECOND + INTERVAL 1800 SECOND DELETE
```

Re-derive with:

```bash
curl -s https://raw.githubusercontent.com/SigNoz/signoz-otel-collector/main/cmd/signozschemamigrator/schema_migrator/traces_migrations.go \
  | grep -n 'OrderBy\|PartitionBy\|TTL:'
```

Four things follow, and they are the reason behind rules this skill used to assert bare:

1. **`ts_bucket_start` is the first key column**, so a query without a `ts_bucket_start` predicate
   cannot use the primary index at all and reads every part in the date partition. This is why the
   bucket predicate is not optional, and it is a stronger reason than "SigNoz stores 30-minute
   buckets".
2. **`resource_fingerprint` is second**, so filtering resources through the CTE plus `GLOBAL IN`
   turns a resource-attribute filter into a primary-key range. It is also why adding the CTE when
   the query filters no resource attribute makes the query slower rather than safer: an unfiltered
   fingerprint set widens the key range instead of narrowing it.
3. **`has_error` and `name` are third and fourth**, so filtering or grouping on `has_error` or `name`
   is index-supported. Filtering on `http_method`, `duration_nano`, `status_code` or a map key is
   not — those are read from the rows the key range already selected. Order the predicates that way.
4. **The resource table's TTL is the index table's TTL plus exactly 1800 seconds.** That margin is
   the same 1800 the bucket predicate uses, and it is what keeps a resource row alive long enough to
   join a span at the oldest edge of the retention window. It is a designed safety margin, not a
   coincidence.

`python3 scripts/check-signoz-schema.py --dsn URL` asserts that the sorting key still begins
`ts_bucket_start, resource_fingerprint`. If that assertion fails, every rule above needs rewriting
before any query does.

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

## Column access

| Instead of | Use |
|---|---|
| `attributes_string['http.route']` | `attribute_string_http$$route` |
| `attributes_string['db.system']` | `attribute_string_db$$system` |
| `attributes_string['rpc.method']` | `attribute_string_rpc$$method` |
| `attributes_string['peer.service']` | `attribute_string_peer$$service` |
| `resources_string['service.name']` | `resource_string_service$$name` |

`attribute_string_messaging$$system`, `attribute_string_messaging$$operation`,
`attribute_string_rpc$$system` and `attribute_string_rpc$$service` exist on the same convention.

Read resource attributes as `resource.service.name::String`. As with logs, the `resource` JSON column
caps distinct dynamic paths at 100.

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

## Worked queries

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

### Recent spans whose parent span is missing

Lists spans whose `parent_span_id` is non-empty but which no collected span in the same trace
matches. It tells you **which** spans are orphaned. Read `40-missing-spans.md` for **why**, which is
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

## What this file does not answer

Which services call which — read `50-service-topology.md`, which describes the endpoint and the
pre-aggregated table SigNoz already maintains for that question. Do not hand-write a self-join over
`distributed_signoz_index_v3` to reproduce it.
