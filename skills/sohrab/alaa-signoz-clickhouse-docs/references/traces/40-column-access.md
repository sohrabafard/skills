# Trace columns and optional JSON

Read the [signal prerequisites](../clickhouse-traces-reference.md) before this topic.

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

## Optional JSON evolution

The released migrations in `../90-versions.md` add `scope`, `attributes` and
`attributes_promoted`; `check-signoz-schema.py` probes them without requiring them on older
installs. Confirm presence, type and population before moving a query from legacy maps.
Query Builder semantic-name resolution does not rename raw stored columns automatically.
Do not treat a missing optional column as a reason to upgrade the consumer.

After `DESCRIBE` confirms the JSON `scope` column, this bounded panel groups by its typed name.
The example remains unverified for a deployment until that evidence is supplied:

```sql
-- UNVERIFIED SCHEMA: signoz_traces.distributed_signoz_index_v3
SELECT scope.name::String AS scope_name, toFloat64(count()) AS value
FROM signoz_traces.distributed_signoz_index_v3
WHERE timestamp BETWEEN $start_datetime AND $end_datetime
  AND ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp
GROUP BY scope_name
ORDER BY value DESC
LIMIT 100
```

If `scope` is absent, use Query Builder's available fields or verified legacy columns;
never fabricate a scope column. The grouping ceiling in the skill still applies.
