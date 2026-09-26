# ClickHouse Logs Query Reference for SigNoz

Read this only for SigNoz dashboard-panel SQL over log records. Logs Explorer uses Query Builder and
search syntax unless the user asked for raw SQL for a panel.

All tables live in the `signoz_logs` database. The rules that hold on every query — the time bound,
the bucket predicate and its reason, the panel shape, the grouping ceiling — are stated once in
`SKILL.md`. This file carries what is specific to logs.

## Required query prerequisites

Before writing any log query, read [schema](logs/10-schema.md), [time/resource filtering](logs/20-time-resource.md), and [column access](logs/30-column-access.md) for table availability, bounds, resource joins and stored-field syntax.

## Select the remaining topic

- When searching record text, read [body search](logs/40-body-search.md) for old/new body paths, index limits and release gates.
- When choosing a panel, read [panel shapes](logs/50-panel-shapes.md) for timeseries, value and table output contracts.
- When counting records or errors, read [count/error examples](logs/60-counts-errors.md) for bounded aggregations.
- When auditing record size, read [payload auditing](logs/70-payload-audit.md) for bounded output and grouping limits.
