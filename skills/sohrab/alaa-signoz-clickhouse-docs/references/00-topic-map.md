# Topic Map

Use this file first when the task is broad or when you are not sure which reference to load.

## Read this file, then jump to one reference

- Official docs page selection and current entry pages:
  - `docs-routing.md`
- OpenTelemetry instrumentation, migration, Collector setup, and language/framework paths:
  - `instrumentation-routing.md`
- Log-ingestion path selection:
  - `log-collection-routing.md`
- Query Builder v5, search syntax, field ambiguity, formulas, aggregation, and dashboard variables:
  - `query-language-routing.md`
- Logs dashboard/alert SQL in ClickHouse:
  - `clickhouse-logs-reference.md`
- Traces dashboard/alert SQL in ClickHouse:
  - `clickhouse-traces-reference.md`
- Metrics dashboard/alert SQL in ClickHouse:
  - `clickhouse-metrics-reference.md`
- Generic SigNoz/OTel data-quality guardrails and missing-span reasoning:
  - `observability-guardrails.md`
- Production query safety and validation checklist:
  - `validation-checklists.md`
- Official-first source priority and freshness triggers:
  - `source-map.md`

## Fast routing

- “Which SigNoz page should I read for OpenTelemetry instrumentation?”
  - Start with `instrumentation-routing.md`.
- “I already use OpenTelemetry. How do I switch to SigNoz?”
  - Start with `instrumentation-routing.md`.
- “How should I send logs to SigNoz?”
  - Start with `log-collection-routing.md`.
- “Why is `service.name` ambiguous in SigNoz?”
  - Start with `query-language-routing.md`, then `observability-guardrails.md`.
- “Write a ClickHouse panel query for logs.”
  - Start with `clickhouse-logs-reference.md`.
- “Write a ClickHouse panel query for traces.”
  - Start with `clickhouse-traces-reference.md`.
- “Write a ClickHouse panel query for metrics, request rate, error rate, or p99 latency from metric samples.”
  - Start with `clickhouse-metrics-reference.md`.
- “I need both the docs page and the SQL.”
  - Read the relevant routing file first, then the matching ClickHouse reference.
- “SigNoz says this trace has missing spans.”
  - Start with `observability-guardrails.md`, then use `clickhouse-traces-reference.md` for anti-join verification.
- “Is this query safe/efficient for a sensitive production system?”
  - Load `validation-checklists.md` before finalizing.
