---
name: alaa-observability-soc
description: "Observability/SOC signal architecture for Alaa services: OpenTelemetry traces, metrics, logs, profiles, exemplars, SigNoz/Sentry roles, Collector/Vector topology, alerting, SOC/SIEM egress, correlation IDs, trace IDs, and security evidence. Use for telemetry design, production-readiness audits, incident diagnostics, signal quality, privacy, cardinality, and auditability decisions. Pair with alaa-signoz-clickhouse-docs for SigNoz docs lookup or ClickHouse SQL."
---

# Alaa Observability SOC

## Purpose

Use this skill to design, review, or troubleshoot Alaa observability and SOC evidence. It owns the signal model,
security-event evidence model, telemetry privacy rules, Sentry/SigNoz role split, Collector/Vector topology,
alert/runbook quality, and incident-diagnostic reasoning.

Keep this file routing-first. Load references only when the task needs the detail.

## Activate for

- OpenTelemetry traces, metrics, logs, profiles, OTLP, Collector, Vector, SigNoz, Sentry, Prometheus, exemplars, or
  telemetry pipeline work
- correlation IDs, `traceparent`, `trace_id`, request IDs, incident evidence, audit logs, security-log catalogs,
  SOC/SIEM egress, or customer SOC forwarding
- SLOs, latency percentiles, RED/USE signals, alerts, pages, runbooks, cardinality budgets, sampling, retention, or
  telemetry cost controls
- production-readiness or security-sensitive reviews where missing/unsafe telemetry can hide incidents or expose
  sensitive data

## Do not use for

- feature work with no observability, incident, audit, or SOC signal change
- pure frontend/UI tasks unless the task includes RUM, tracing, error capture, or security-event evidence
- SigNoz ClickHouse SQL authoring or docs-page selection; use `$alaa-signoz-clickhouse-docs`

## Operating rules

1. Read repo-local `AGENTS.md` and current service docs before changing behavior.
2. For Ala backend, gateway, WA, entitlement, or future service standardization, pair with `$alaa-services-contract`
   before implementation decisions.
3. Read `references/00-topic-map.md`, then the smallest relevant section of `references/full-guide.md`.
4. For current or version-sensitive claims, use `references/90-source-map.md` and prefer official primary docs plus repo
   truth.
5. For security-sensitive systems, load `references/91-sensitive-system-checklists.md` before approving design, alerts,
   events, egress, or production readiness.
6. When authoring or updating skills, prompts, or model-runtime instructions, load
   `references/95-model-runtime-compatibility.md`.

## Platform invariants

- Every Alaa service emits standard OpenTelemetry traces, metrics, and logs over OTLP or an approved local pipeline.
  Treat this as production readiness, not an optional enhancement.
- Latency histograms used for SLO/debugging must preserve a path from aggregate latency to representative traces through
  exemplars or an equivalent trace-linking mechanism.
- Telemetry must be fail-open for product traffic. A broken backend, Collector, Vector sidecar, or SOC/SIEM destination
  must not block the hot path.
- Secrets, credentials, tokens, session values, raw PII, unrestricted payloads, and customer-private content do not
  belong in logs, span attributes, metric labels, alert annotations, Sentry contexts, or SOC exports.
- Metric labels stay low-cardinality and bounded. High-cardinality values belong in traces/logs and are linked through
  `trace_id`, not metric labels.
- Security/audit events must be structured, queryable, timestamped, and correlated to trace/request identity wherever
  technically possible.

## Ownership and companion routing

- `$alaa-services-contract` owns exact Alaa service surfaces: headers, middleware behavior, route families,
  health/readiness endpoints, metric/event names, trusted ingress, deploy topology, and current service boundaries.
- This skill owns why each signal exists and whether the signal model is safe, debuggable, cost-aware, and SOC-ready.
- `$alaa-signoz-clickhouse-docs` owns SigNoz docs routing and ClickHouse SQL execution over logs, traces, and metrics.
  Hand off query writing, panel SQL repair, missing-span anti-joins, and SigNoz table-schema questions.
- `$alaa-security-review` should be paired when event semantics, policy decisions, customer data, authn/authz, abuse, or
  incident response overlap with security controls.

## Severity rubric

| Signal type | Use when                                                                        |
|-------------|---------------------------------------------------------------------------------|
| log only    | Useful for forensics or debugging but not actionable alone                      |
| metric      | Durable trend/SLO math or alerting on rate, duration, saturation, or errors     |
| alert       | A human should investigate within the defined response window                   |
| page        | Urgent enough to interrupt an operator immediately                              |
| SOC event   | Security/audit evidence must be retained, routed, or shared with a customer SOC |

## Output contract

For reviews or designs, return:

- decision or recommendation
- affected services/pipelines
- required signals and exact correlation fields
- privacy/cardinality constraints
- alert/runbook or SOC/SIEM impact
- validation evidence or the smallest missing evidence
- companion skill handoff, if query execution or code changes are outside this skill

## Stop rules

Make progress from repo truth and safe assumptions. Ask only when the missing detail would materially change security
posture, data exposure, production side effects, or schema compatibility. If evidence is missing, state the gap and give
the safest bounded recommendation rather than inventing a metric, field, table, customer, or retention promise.
