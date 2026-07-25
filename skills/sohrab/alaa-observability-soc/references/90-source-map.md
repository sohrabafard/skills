# Source Map

Load when observability guidance depends on a current standard, a backend behaviour, or a vendor or tooling behaviour
that may have changed.

## Source priority

1. **Target repo truth.** Instrumentation code, logging config, metric names, Collector and Vector config, dashboards,
   alerts, tests, deployment files, runbooks, current docs, and observed telemetry. Repo truth outranks every table in
   this skill.
2. **Platform contracts.** `/alaa-services-contract` (`$alaa-services-contract` in Codex) for every Alaa name and value;
   this skill for every requirement level, gate, and reason.
3. **Official or primary standards and vendor docs:**
   - W3C Trace Context: https://www.w3.org/TR/trace-context/
   - OpenTelemetry docs: https://opentelemetry.io/docs/
   - OpenTelemetry specs: https://opentelemetry.io/docs/specs/
   - OpenTelemetry semantic conventions: https://opentelemetry.io/docs/specs/semconv/
   - OpenTelemetry Collector resiliency: https://opentelemetry.io/docs/collector/resiliency/
   - OpenTelemetry Collector exporters: https://opentelemetry.io/docs/collector/components/exporter/
   - OpenTelemetry exemplars: https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar
   - Prometheus docs, including exemplar storage: https://prometheus.io/docs/
   - OpenMetrics exemplar exposition: https://openmetrics.io/
   - SigNoz docs: https://signoz.io/docs/
   - Sentry docs: https://docs.sentry.io/
   - Sentry OTLP ingestion: https://docs.sentry.io/concepts/otlp/
   - Vector docs: https://vector.dev/docs/
   - Vector OpenTelemetry sink: https://vector.dev/docs/reference/configuration/sinks/opentelemetry/
4. **Community posts, issue threads, and Stack Overflow** only to explain an observed failure, and only after the two
   sources above have been checked.

## Checked baseline for this pack

- OpenTelemetry is the mandatory vendor-neutral contract for Alaa traces, metrics, and logs. Profiles exist in the
  semantic conventions but are opt-in per service, not a fleet minimum.
- Collector resilience rests on sending queues and retries, and on persistent storage or a durable queue for hops where
  loss is unacceptable. A central Collector or SOC exporter outage must never block application traffic.
- Exemplars are the supported way to link an aggregate metric point to a representative trace, and the only
  cardinality-safe one.
- SigNoz is the primary backend for OTel logs, traces, metrics, dashboards, and ClickHouse-backed analysis.
- Sentry remains the exception, release, and source-map workflow where enabled. Re-check Sentry's OTLP behaviour before
  anyone proposes replacing SDK-based exception capture with OTLP-only ingestion.
- Vector remains the right local and sidecar agent where disk buffering, transformation, or fan-out is needed; check sink
  maturity before depending on a beta feature.

## Freshness triggers

Re-check primary docs when the task mentions:

- the latest or current behaviour of OpenTelemetry, the semantic conventions, Collector config, OTLP, SigNoz, Sentry,
  Vector, profiling, exemplars, span metrics, or log correlation
- Sentry OTLP ingestion, OpenTelemetry logs or profiles, Collector component stability, Vector OpenTelemetry sink
  maturity, or SigNoz schema and query behaviour
- native histograms, tail-sampling processor behaviour, or exemplar support on a specific scrape or push path
- security-event catalogs, SOC or SIEM egress, retention, customer-specific audit requirements, regulatory constraints,
  PII handling, or incident evidence
- a discrepancy between what a service emits and what the backend UI or a query returns

## Domain-bounded anti-pattern

Bad: adding a high-cardinality metric label — raw URL, user ID, token ID, request ID, email, phone, or trace ID — because
it helps one debugging session.

Good: keep the high-cardinality value in the trace or log, keep metric labels inside the budget in
`30-quantitative-budgets.md`, and link the two through an exemplar.
