# Source Map

Use this file when observability guidance depends on current telemetry standards, backend behavior, or vendor/tooling behavior.

## Source priority

1. Target repo truth: instrumentation code, logging config, metric names, Collector config, Vector config, dashboards, alerts, tests, deployment files, and current docs.
2. Ala platform contract sources: this skill and `$alaa-services-contract` for exact Ala service surfaces.
3. Official or primary observability sources:
   - W3C Trace Context: https://www.w3.org/TR/trace-context/
   - OpenTelemetry docs: https://opentelemetry.io/docs/
   - OpenTelemetry specs: https://opentelemetry.io/docs/specs/
   - OpenTelemetry semantic conventions: https://opentelemetry.io/docs/specs/semconv/
   - Prometheus docs (incl. exemplars): https://prometheus.io/docs/
   - OpenMetrics (exemplars exposition): https://openmetrics.io/
   - OpenTelemetry metrics exemplars spec: https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar
   - Collector spanmetrics connector: https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/spanmetricsconnector
   - Vector docs: https://vector.dev/docs/
   - SigNoz docs: https://signoz.io/docs/
   - Sentry docs: https://docs.sentry.io/
   - Sentry OTLP ingestion (beta, version-sensitive): https://docs.sentry.io/concepts/otlp/
4. Community posts, StackOverflow answers, and vendor blogs only for troubleshooting concrete symptoms or understanding operational tradeoffs after official docs and repo truth are checked.

## Version-sensitive notes (recheck before relying on)

- Sentry OTLP ingestion is open beta and OTLP does not carry errors to Sentry — only the Sentry SDK captures exceptions. Recheck `https://docs.sentry.io/concepts/otlp/` before advising Sentry-via-OTLP. (noted 2026-07)
- Collector selection (OTel Collector vs Vector vs Grafana Alloy) tracks fast-moving tools; recheck when a customer constraint is unusual. (noted 2026-07)

## Freshness triggers

Re-check primary docs when the task mentions:

- latest/current OpenTelemetry, semantic conventions, Collector config, OTLP, Prometheus, SigNoz, Sentry, profiling, source maps, debug IDs, exemplars, or log correlation
- exemplars, OpenMetrics, spanmetrics, metric-to-trace correlation, latency percentiles, or Vector sidecar collection
- package upgrades, runtime upgrades, security event catalogs, alert routing, sampling, retention, or cost controls
- discrepancies between service traces/logs/metrics and the SigNoz UI

## Domain-bounded anti-pattern

Bad: adding a high-cardinality metric label such as raw URL, user id, token id, or request id because it helps one debugging session.

Good: keep high-cardinality values in logs/traces, expose bounded metric labels, and link signals through `trace_id` (as an exemplar on latency histograms, never as a metric label).
