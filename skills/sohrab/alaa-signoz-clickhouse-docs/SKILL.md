---
name: alaa-signoz-clickhouse-docs
description: "SigNoz docs lookup and ClickHouse query execution for dashboards/alerts over OpenTelemetry logs, traces, and metrics. Use for Query Builder v5 routing, search syntax, dashboard variables, field ambiguity, missing spans, trace-quality troubleshooting, and writing/repairing SigNoz ClickHouse SQL. Pair with alaa-observability-soc for signal design, cardinality, exemplars, Sentry, Collector, Vector, or SOC policy decisions."
---

# Alaa SigNoz ClickHouse Docs

Use this skill to choose the right official SigNoz documentation path and to write or repair SigNoz ClickHouse queries for dashboards and alerts over logs, traces, and metrics.

## Quick start

1. Read `references/source-map.md` when the task mentions latest/current docs, schema changes, Query Builder behavior, live query failures, instrumentation versions, Collector versions, or migration.
2. If the task is broad, read `references/00-topic-map.md` first.
3. Classify the task:
   - docs lookup or docs-grounded answer
   - Query Builder/search syntax/variables/field ambiguity
   - ClickHouse SQL writing or repair for logs, traces, or metrics
   - missing-spans or trace-quality troubleshooting
   - mixed task: docs first, then query
4. Load only the matching reference file and answer directly.

## Do not use for

- generic ClickHouse work outside SigNoz schemas
- PromQL-only tasks unless the user needs SigNoz docs routing
- observability design that does not depend on SigNoz docs, UI behavior, or table conventions
- security/SOC policy, Sentry role decisions, cardinality policy, exemplar architecture, Collector/Vector topology, or alert severity policy; use `$alaa-observability-soc`

## Mode routing

| Mode | Use when | Load |
| --- | --- | --- |
| Docs lookup | user asks for the right SigNoz page or a docs-grounded setup answer | `docs-routing.md` plus a specific routing file |
| Instrumentation | OTel SDK, Collector, migration, language/framework setup | `instrumentation-routing.md` |
| Log collection | logs, files, containers, OTLP/HTTP logs, collectors | `log-collection-routing.md` |
| Query Builder | visual query builder, search syntax, filters, formulas, variables, field ambiguity | `query-language-routing.md` |
| Logs SQL | raw ClickHouse panel/alert query over logs | `clickhouse-logs-reference.md` |
| Traces SQL | raw ClickHouse panel/alert query over spans/traces | `clickhouse-traces-reference.md` |
| Metrics SQL | raw ClickHouse panel/alert query over metric samples/time series | `clickhouse-metrics-reference.md` |
| Missing spans | missing parent span, broken trace tree, parent span ID confusion | `observability-guardrails.md` + `clickhouse-traces-reference.md` |
| Sensitive validation | production query safety, panel correctness, schema assumptions | `validation-checklists.md` |

## ClickHouse query operating rules

- First confirm the UI surface. ClickHouse SQL is for SigNoz Dashboards and ClickHouse-backed alerts; Explorers usually use Query Builder/search syntax.
- Identify the signal before writing SQL: logs, traces, or metrics. Do not mix table families without a clear join key and time window.
- Use distributed tables and official SigNoz schema names from the relevant reference. If schema age is uncertain, inspect current docs or live `SHOW TABLES`/`DESCRIBE TABLE` before finalizing.
- Always include a bounded time filter. For logs/traces, include the expected SigNoz bucket filter when required. For metrics, use `{{.start_timestamp_ms}}` and `{{.end_timestamp_ms}}` unless the current docs or dashboard surface proves different variables.
- Prefer indexed/pre-extracted columns over map/JSON access when they exist.
- Use a resource CTE only when filtering on resource attributes; use `GLOBAL IN` where the reference requires it.
- Return the expected panel shape:
  - timeseries: `ts`, `value`
  - value widget: one row named `value`
  - table: labeled columns and bounded `LIMIT`
- Keep placeholders explicit (`{{service_name}}`, `{{attribute_key}}`, `{{metric_name}}`) when exact values are unknown.
- Never include credentials, tokens, raw customer payloads, or destructive SQL in examples.

## Missing-spans workflow

Use SigNoz/live evidence first when available:

1. inspect recent traces for `trace_id`, `span_id`, `parent_span_id`, `name`, `serviceName`, and `spanKind`
2. group by operation and parent span pattern
3. use the anti-join query in `clickhouse-traces-reference.md` if ClickHouse access exists
4. fix instrumentation at source: preserve inbound `traceparent`; do not generate a fake parent span; root the request server span when inbound context is missing/invalid
5. verify with a direct request that has no inbound `traceparent`; it should produce a root/server span with an empty parent span ID

## Output contract

For docs tasks, return the best page first, why it is the best fit, and only the alternates that change the setup path.

For query tasks, return:

- panel type and signal
- assumptions/placeholders
- final SQL in one block
- validation notes: time bounds, schema/table family, variables, resource filters, limits, and any unresolved uncertainty

For query repair, briefly name the issue, provide the corrected query, and avoid a long research diary.

## Stop rules

Make the smallest safe assumption when details are missing. Ask only when the missing detail changes the signal, table family, time variables, schema version, production side effects, or data exposure. Do not invent SigNoz table names, fields, macros, or UI capabilities when current docs or live schema are required.
