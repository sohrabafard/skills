# Observability Guardrails

This file distills the most useful generic guardrails from the merged observability skill.
Use it when the official SigNoz docs do not fully answer a design tradeoff.

## Signal choice

- Logs: detail, forensics, request-level evidence, and human-readable context
- Metrics: trends, SLO math, capacity signals, alerts
- Traces: one request or one job across services and dependencies
- Exceptions: stack traces and failure details

## Core OpenTelemetry rules

- Use OpenTelemetry semantic conventions where practical.
- Keep exporter endpoint, protocol, and headers in environment or deployment config, not hard-coded in service code.
- Treat `service.name` as a resource attribute, not a random span or log attribute.
- Preserve W3C trace context across hops when possible.

## Collector rules

Prefer the Collector when you need routing, retries, batching, redaction, fan-out, or centralized credentials.

A good mental model is:

- application emits telemetry
- Collector receives and processes it
- SigNoz stores and visualizes it

## Correlation rules

- Keep `trace_id` queryable in logs.
- If possible, keep `span_id` queryable too.
- Do not put `trace_id`, `span_id`, `user_id`, or other unbounded request identifiers into metric labels.
- If trace-log correlation matters, choose a log path that preserves or injects trace context cleanly.

## Missing-spans guardrails

SigNoz marks a trace as having missing spans when a span's parent span id is not found in the collected trace. Common causes include sampling, dropped spans, or an upstream service that propagates `traceparent` but does not export its own span.

When debugging an Ala service:

- Check whether request server spans have non-empty `parent_span_id` values even when the request had no real exporting upstream span.
- Watch for code that generates a local `traceparent` and then calls an OpenTelemetry extractor with that generated value. That creates a child span whose parent span id was never exported.
- Preserve valid inbound W3C trace context, but do not treat a locally generated fallback `traceparent` as a parent context.
- For missing or invalid inbound `traceparent`, start the request server span as a root span.
- Use the actual started span context for response headers and log correlation when the SDK exposes it; keep generated fallback headers only for telemetry-disabled or fail-open paths.
- Verify the fix with a direct request that sends no `traceparent`: the server span should have an empty parent span id, and child DB or dependency spans should parent to that server span.

## Field-quality rules

- Resource identity belongs in resource fields.
- Request or event detail belongs in span or log attributes.
- If SigNoz reports an ambiguous key such as `service.name`, fix the instrumentation source so the same key is not sent in conflicting contexts.
- Prefer stable field names over ad hoc one-off keys.

## Cardinality and privacy rules

- Avoid high-cardinality metric labels such as raw user IDs, emails, UUIDs, full URLs with IDs, or request IDs.
- Avoid secrets and raw PII in logs, traces, and tags.
- If you need detailed debugging per request, use logs or traces rather than exploding metric labels.

## Helpful defaults

- For service breakdowns, filter by resource attributes.
- For request debugging, make `trace_id` easy to filter in logs.
- For dashboards, start with a small number of high-value dimensions.
- For alerts, prefer stable metric signals over brittle free-text log patterns.
