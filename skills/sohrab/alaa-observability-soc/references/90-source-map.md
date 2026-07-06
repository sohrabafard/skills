# Source Map

Use this file when observability guidance depends on current standards, backend behavior, model-runtime behavior, or vendor/tooling behavior.

## Source priority

1. Target repo truth: instrumentation code, logging config, metric names, Collector/Vector config, dashboards, alerts, tests, deployment files, runbooks, current docs, and observed telemetry.
2. Ala platform contracts: this skill and `$alaa-services-contract` for exact Ala service surfaces.
3. Official or primary standards and vendor docs:
   - Agent Skills specification: https://agentskills.io/specification
   - OpenAI Codex skills: https://developers.openai.com/codex/skills
   - OpenAI GPT-5.5 prompt guidance: https://developers.openai.com/api/docs/guides/prompt-guidance
   - Anthropic Claude Code skills: https://code.claude.com/docs/en/skills
   - Anthropic model docs: https://platform.claude.com/docs/en/about-claude/models/overview
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
4. Community posts, issue threads, and Stack Overflow only for troubleshooting observed failures after official docs and repo truth have been checked.

## Checked baseline for this pack

- Open Agent Skills use `SKILL.md` with `name` and `description`; detailed material should be moved to references and loaded only when needed.
- GPT-5.5 prompting favors outcome-first contracts, concise descriptions, retrieval budgets, validation loops, and fewer process-heavy absolute rules.
- Claude Opus 4.8, Sonnet 5, and Fable 5 have model/runtime differences that belong in the app harness or compatibility reference, not as hardcoded business logic in this observability skill.
- OpenTelemetry is the mandatory vendor-neutral contract for Ala traces, metrics, and logs. Profiles are supported in OTel semantic conventions, but enable profiling per runtime/cost/security need rather than treating every service profile stream as a universal minimum.
- Collector resilience depends on queues/retries and, for critical hops, persistent storage or durable queues. A central Collector/SOC exporter outage must not block application traffic.
- Exemplars link aggregate metric points to active traces and are the preferred way to move from percentile latency to representative trace evidence.
- SigNoz is the primary observability backend for OTel logs, traces, metrics, dashboards, and ClickHouse-backed analysis.
- Sentry remains the primary application exception/release/profiling workflow when enabled. Recheck Sentry OTLP behavior before replacing SDK-based exception capture with OTLP-only ingestion.
- Vector remains a good local/sidecar log collection and routing component when disk buffering, transformation, or fan-out is required; recheck sink maturity before relying on beta features.

## Freshness triggers

Re-check primary docs when the task mentions:

- latest/current OpenTelemetry, semantic conventions, Collector config, OTLP, SigNoz, Sentry, Vector, profiling, exemplars, spanmetrics, or log correlation
- package/runtime upgrades, model runtime changes, Fable/Opus/Sonnet/GPT compatibility, skill authoring, or agent invocation behavior
- Sentry OTLP, OpenTelemetry logs/profiles, Collector exporter status, Vector OpenTelemetry sink maturity, or SigNoz schema/query behavior
- security event catalogs, SOC/SIEM egress, retention, customer-specific audit requirements, regulatory constraints, PII handling, or incident evidence
- discrepancies between service traces/logs/metrics and backend UI/query results

## Domain-bounded anti-pattern

Bad: adding a high-cardinality metric label such as raw URL, user ID, token ID, request ID, email, phone, or trace ID because it helps one debugging session.

Good: keep high-cardinality values in logs/traces, expose bounded metric labels, and link signals through `trace_id` or exemplars rather than metric labels.
