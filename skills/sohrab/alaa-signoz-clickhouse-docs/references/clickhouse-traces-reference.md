# ClickHouse Traces Query Reference for SigNoz

Read this only for SigNoz dashboard-panel SQL over spans. Traces Explorer uses Query Builder and
search syntax unless the user asked for raw SQL for a panel.

All tables live in the `signoz_traces` database. The rules that hold on every query are stated once
in `SKILL.md`; this file carries what is specific to spans.

## Required query prerequisites

Before writing any span query, read [physical layout](traces/10-physical-layout.md), [schema](traces/20-schema.md), [time/resource filtering](traces/30-time-resource.md), and [column access](traces/40-column-access.md) for sorting/bucket rules, table availability, resource joins and optional JSON evidence.

## Select the remaining topic

- When choosing a panel, read [panel shapes](traces/50-panel-shapes.md) for timeseries, value and table contracts.
- When aggregating errors or duration, read [error/duration examples](traces/60-errors-duration.md) for bounded queries.
- When finding collected children with absent parents, read [missing-parent query](traces/70-missing-parent.md) for the anti-join and its limits.

## What this file does not answer

Which services call which — read `50-service-topology.md`, which describes the endpoint and the
pre-aggregated table SigNoz already maintains for that question. Do not hand-write a self-join over
`distributed_signoz_index_v3` to reproduce it.
