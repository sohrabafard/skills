# Topic Map

Use this file first when the task is broad or when you are not sure which reference to load.

## Read this file, then jump to one reference

- Official docs page selection and current entry pages:
  - `docs-routing.md`
- OpenTelemetry instrumentation, migration, and Collector choice:
  - `instrumentation-routing.md`
- Log-ingestion path selection:
  - `log-collection-routing.md`
- Query Builder, search syntax, field ambiguity, and dashboard variables:
  - `query-language-routing.md`
- Logs dashboard SQL in ClickHouse:
  - `clickhouse-logs-reference.md`
- Traces dashboard SQL in ClickHouse:
  - `clickhouse-traces-reference.md`
- Generic observability and telemetry-quality guardrails:
  - `observability-guardrails.md`

## Fast routing

- “Which SigNoz page should I read for OpenTelemetry instrumentation?”
  - Start with `instrumentation-routing.md`
- “I already use OpenTelemetry. How do I switch to SigNoz?”
  - Start with `instrumentation-routing.md`
- “How should I send logs to SigNoz?”
  - Start with `log-collection-routing.md`
- “Why is `service.name` ambiguous in SigNoz?”
  - Start with `query-language-routing.md` and then `observability-guardrails.md`
- “Write a ClickHouse panel query for logs.”
  - Start with `clickhouse-logs-reference.md`
- “Write a ClickHouse panel query for traces.”
  - Start with `clickhouse-traces-reference.md`
- “I need both the docs page and the SQL.”
  - Read the relevant routing file first, then the matching ClickHouse reference
- “SigNoz says this trace has missing spans.”
  - Start with `observability-guardrails.md`, then use `clickhouse-traces-reference.md` for the anti-join verification query
