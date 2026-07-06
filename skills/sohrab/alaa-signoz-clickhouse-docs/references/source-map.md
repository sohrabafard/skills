# Official-First Source Map

Use this map before answering version-sensitive SigNoz or SigNoz ClickHouse questions. Official SigNoz docs and OpenTelemetry docs outrank examples, blogs, issue threads, Stack Overflow, and other community material.

## Primary sources

- SigNoz docs home: https://signoz.io/docs/
- What is SigNoz: https://signoz.io/docs/what-is-signoz/
- Instrumentation overview: https://signoz.io/docs/instrumentation/
- OpenTelemetry Collector setup: https://signoz.io/docs/tutorial/opentelemetry-collector-binary-usage-in-virtual-machine/
- Log collection: https://signoz.io/docs/logs-management/send-logs/
- Query Builder v5: https://signoz.io/docs/userguide/query-builder-v5/
- Search syntax: https://signoz.io/docs/userguide/search-syntax/
- Field context and data types: https://signoz.io/docs/userguide/field-context-data-types/
- Dashboard variables: https://signoz.io/docs/userguide/manage-variables/
- ClickHouse queries for dashboards and alerts: https://signoz.io/docs/operate/clickhouse/clickhouse-queries/
- Metrics ClickHouse queries: https://signoz.io/docs/userguide/write-a-metrics-clickhouse-query/
- Logs ClickHouse queries: https://signoz.io/docs/userguide/logs_clickhouse_queries/
- Traces ClickHouse queries: https://signoz.io/docs/userguide/writing-clickhouse-traces-query/
- Log-based alerts: https://signoz.io/docs/alerts-management/log-based-alerts/
- SigNoz migration docs: https://signoz.io/docs/migration/
- OpenTelemetry docs: https://opentelemetry.io/docs/
- Agent Skills specification: https://agentskills.io/specification
- OpenAI Codex skills: https://developers.openai.com/codex/skills
- Anthropic Claude Code skills: https://code.claude.com/docs/en/skills

## Checked baseline for this pack

- SigNoz stores observability data in ClickHouse and supports ClickHouse SQL for Dashboards and ClickHouse-backed alerts when Query Builder does not cover the use case.
- Query Builder v5 is the preferred visual interface for logs, traces, metrics, dashboards, and alert rules; use it instead of raw SQL when the user asks for Explorer/search behavior.
- Logs ClickHouse examples use the logs v2 table family. Traces examples use the signoz index v3 table family. Metrics examples use `signoz_metrics` sample/time-series v4 table families, but the metrics docs explicitly warn schemas may change.
- Metrics ClickHouse queries are usually two-step: filter time-series labels/fingerprints, then join to sample data within the time range.
- Current dashboard macros differ by signal family; use the relevant reference file and do not transfer macros blindly across logs, traces, and metrics.

## Freshness triggers

Fetch current official docs or inspect live schema when the task mentions:

- `latest`, current SigNoz schemas, table names, macros, Query Builder v5, dashboard variables, alert behavior, or broken live queries
- metrics ClickHouse SQL, histogram quantiles, p99 latency, RED metrics, `distributed_samples_v4`, or time-series tables
- migration, instrumentation versions, Collector versions, log ingestion behavior, field ambiguity, or missing spans
- a query that will be pasted into a production dashboard/alert, or any query touching customer/security-sensitive data

## Troubleshooting-only sources

Use Stack Overflow, GitHub issues, discussions, and community blogs only to troubleshoot observed failures. Confirm schema, query, instrumentation, and migration guidance against SigNoz or OpenTelemetry docs.
