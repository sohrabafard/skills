# Security-Sensitive Observability and SOC Checklists

Use this file before approving telemetry, alerts, dashboards, SOC/SIEM forwarding, or production readiness for sensitive Alaa systems.

## 1. Data classification gate

A telemetry change is not ready until every emitted field is classified:

- Public/operational: service name, route template, status code, error code, deployment environment, version, bounded component name.
- Internal but safe: tenant/project ID only if policy permits it, hashed actor ID, request ID, trace ID, span ID, rule/code names, feature flag names.
- Sensitive: email, phone, national ID, address, access token, refresh token, API key, password, session ID, cookie, raw JWT, raw request/response body, file content, payment data, health data, customer-private text.

Rules:

- Do not emit sensitive fields in metric labels, log bodies, span attributes, Sentry contexts, breadcrumbs, alert annotations, or SOC payloads.
- Prefer route templates over raw paths. Prefer error codes over exception messages when messages can contain user input.
- Hash or tokenize actor/customer identifiers only when correlation is required and the hashing strategy is approved.
- When unsure, redact and include a stable internal reference ID that authorized humans can use to query the source system.

## 2. Required correlation fields

Every service-level log, trace, alert, and SOC event should preserve the following when available:

- `service.name`
- `service.version`
- deployment environment (`deployment.environment.name` or the repo’s currently supported equivalent)
- `trace_id`
- `span_id` where applicable
- `request_id` / `X-Request-Id`
- route template or operation name
- bounded status/result code
- UTC timestamp

For security/audit events, also include:

- event category and event action
- decision: `allow`, `deny`, `challenge`, `error`, `audit_only`, or equivalent bounded values
- policy/rule identifier
- actor reference according to the data classification gate
- target resource type and safe target reference
- source system and trust boundary
- reason code and remediation hint when useful

## 3. Cardinality gate

Before adding a metric label, answer yes to all:

- Is the set of possible values bounded and small under normal and attack traffic?
- Is the value stable across releases and tenants?
- Can the label be aggregated meaningfully for SLOs or capacity planning?
- Is the value free of PII/secrets and unsuitable for per-request uniqueness?

If any answer is no, put the value in traces/logs instead and connect it through `trace_id` or an exemplar.

## 4. Fail-open and backpressure gate

Telemetry must not become a product outage vector.

- SDK exporters run asynchronously with bounded memory and timeouts.
- Local Collector/Vector endpoints are preferred over sending every service directly across a slow network path.
- Remote exporter failures use queues/retries and bounded dropping policies.
- SOC/SIEM exporter failures do not block application response paths.
- Collector/Vector self-telemetry exposes queue size, dropped records, export failures, retry counts, and disk usage.
- Critical remote hops use persistent queue/WAL or durable broker when loss tolerance requires it.

## 5. Sentry/SigNoz split

Use SigNoz for OTel-first observability: traces, metrics, logs, dashboards, alert evidence, ClickHouse-backed analysis, and service correlation.

Use Sentry when application exception triage, release tracking, suspect commits, user-impact grouping, profiling workflow, or SDK-level unhandled-error capture matters.

Do not replace Sentry SDK exception capture with OTLP-only ingestion unless current Sentry docs and a live test prove the required behavior. Keep the SDK as the exception source when in doubt.

## 6. SOC/SIEM egress gate

Before forwarding to a customer SOC/SIEM endpoint:

- Define the event catalog and schema version.
- Define tenant/customer routing and isolation rules.
- Redact or transform data before egress.
- Use TLS, authenticated endpoints, and secret-managed credentials.
- Define retry, replay, dead-letter, and drop behavior.
- Define ownership for delivery failures and stale destination credentials.
- Provide a test event and a replay-safe verification procedure.
- Do not send raw application logs wholesale unless explicitly approved; forward curated security/audit events.

## 7. Alert and runbook gate

An alert is production-ready only when it has:

- owner and escalation path
- severity/page decision
- user or business impact statement
- exact query or signal source
- threshold and evaluation window with rationale
- minimum data and no-data behavior
- expected false-positive causes
- runbook with first three checks and rollback/mitigation path
- links to dashboards, trace/log query, and exemplar/trace evidence when relevant

## 8. Production-readiness evidence

For each service, collect evidence for:

- traces: inbound server spans, outbound dependency spans, error status, propagated `traceparent`
- metrics: request rate, error rate, duration histogram with p50/p90/p95/p99, saturation where relevant
- logs: structured JSON, required correlation fields, no secrets/PII, authz denial format, error code fields
- exemplars: latency histogram can link to representative traces or equivalent trace evidence
- alerts: at least the service’s critical SLO/error signals have owners/runbooks
- pipeline: Collector/Vector config validates and self-telemetry is visible
- incident drill: one controlled failure produces trace, metric, log, alert, and if applicable SOC evidence

## 9. Review output template

Use this shape for sensitive-system reviews:

```text
Decision: pass | pass-with-actions | blocked
Scope: services/pipelines/dashboards/alerts reviewed
Required actions:
- ...
Privacy/cardinality findings:
- ...
Incident/SOC evidence findings:
- ...
Validation performed:
- ...
Missing evidence:
- ...
Handoff:
- ...
```
