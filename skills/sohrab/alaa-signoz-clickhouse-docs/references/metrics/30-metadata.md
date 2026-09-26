# Confirming metric metadata

Read the [signal prerequisites](../clickhouse-metrics-reference.md) before this topic.

## Confirming a metric before doing rate or quantile maths

Do not infer a metric's temporality, type or unit from its name. Ask the install:

```sql
SELECT DISTINCT
  metric_name, type, temporality, unit, is_monotonic, description
FROM signoz_metrics.distributed_metadata
WHERE metric_name = {{metric_name}};
```

and for its label keys:

```sql
SELECT DISTINCT attr_name, attr_datatype
FROM signoz_metrics.distributed_metadata
WHERE metric_name = {{metric_name}}
ORDER BY attr_name;
```

`distributed_metadata` holds one row per metric per attribute value, with `first_reported_unix_milli`
and `last_reported_unix_milli`, so it also answers "is this metric still being reported". Check
`distributed_updated_metadata` too when the answer looks wrong: a unit edited in the UI lives there
and overrides the reported one.

This replaces the instruction to "confirm temporality, type and units" with the query that confirms
them. A rule with no method is not followed.
