# Query Language Routing

Use this file for SigNoz Query Builder v5, search syntax, filtering, aggregation, formulas, field ambiguity, and dashboard variables.

## Pick the right surface

- Logs Explorer, Traces Explorer, and Metrics Explorer: prefer Query Builder/search syntax, not raw ClickHouse SQL.
- Dashboards: use Query Builder when it can express the panel; use ClickHouse SQL only for custom panels that Query Builder cannot cover.
- Alerts: use Query Builder first when supported; use ClickHouse alert queries only when the alert type/surface explicitly supports them.
- If the user says “SQL”, “ClickHouse”, “dashboard query”, “panel query”, or gives existing SQL, route to the signal-specific ClickHouse reference.

## Best pages

- Query Builder v5: https://signoz.io/docs/userguide/query-builder-v5/
- Search syntax: https://signoz.io/docs/userguide/search-syntax/
- Field context and data types: https://signoz.io/docs/userguide/field-context-data-types/
- Dashboard variables: https://signoz.io/docs/userguide/manage-variables/
- ClickHouse queries for dashboards and alerts: https://signoz.io/docs/operate/clickhouse/clickhouse-queries/

## Query Builder v5 guidance

Use Query Builder for:

- service/operation/status filters
- log body search and simple log aggregations
- trace/span filtering, grouping, and percentile charts
- metric temporal/spatial aggregation
- multi-query formulas such as error-rate ratios
- dashboards and alerts where the visual builder expresses the logic

Do not answer a Query Builder task with ClickHouse SQL unless the user explicitly asks for SQL or the requested dashboard/alert requires raw ClickHouse.

## Filtering rules

- Use explicit field filters for traces and metrics.
- Log full-text search can search log bodies without specifying a field; quote phrases where the docs require it.
- Combine filters with `AND` unless the user asks for broader matching.
- Use field context/data type docs when the same field name can appear in resource attributes, span attributes, log attributes, or top-level columns.

## Aggregation rules

- Logs/traces support statistical aggregations, percentiles such as p50/p90/p95/p99, and rates in Query Builder.
- Metrics use temporal aggregation plus spatial aggregation; choose function based on metric type: gauge, counter, histogram, or exponential histogram.
- Prefer formulas for ratios: error rate, success rate, saturation ratio, or “bad / total”.
- Apply group-by only to bounded-cardinality fields. Avoid raw URL, user ID, trace ID, request ID, email, phone, or token values.

## Dashboard variables

Use variables to avoid hardcoded values in reusable dashboards.

- Keep variable names clear, for example `service_name`, `env`, `operation`, `status_code`.
- Use the macro syntax documented for the current surface. Do not convert dashboard variables into ClickHouse macros unless the relevant reference confirms the exact syntax.
- In raw ClickHouse queries, preserve SigNoz default time variables exactly as documented for that signal.

## Field ambiguity

When a field is ambiguous:

1. Prefer top-level/pre-extracted columns when the schema reference lists them.
2. Use explicit context when Query Builder requires it.
3. For SQL, choose the right map/JSON access expression from the signal-specific reference.
4. If the source instrumentation is wrong, fix instrumentation rather than masking it with query hacks.

## Answer shape

- Name the surface: Query Builder, Logs Explorer, Traces Explorer, Metrics Explorer, Dashboard ClickHouse, or Alert ClickHouse.
- Give the filter/aggregation/formula or SQL route.
- Mention when the user must switch to the signal-specific ClickHouse reference.
