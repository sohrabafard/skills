---
name: alaa-observability-soc
description: "Use this skill when the task involves observability architecture, structured logs, OpenTelemetry traces or logs, Prometheus metrics, OTLP/Collector routing, SigNoz, Sentry, profiling, alerting, SOC evidence, incident diagnostics, correlation IDs, trace IDs, or security-log catalogs. Pair it with alaa-services-contract for Ala service work so signal decisions become deterministic platform contracts. Do not use it for feature work with no observability or SOC surface change."
---




# Alaa Observability SOC

## Purpose

Use this skill when the task needs the architectural or policy guidance owned by Alaa Observability SOC.

Keep this top-level file small. Load the references for the full rules, examples, and checklists.

## When to use

- logs, traces, metrics, or alerting work
- correlation IDs or incident evidence requirements
- Sentry integration or cleanup
- SigNoz, OpenTelemetry, OTLP, Collector, Prometheus, profiling, or telemetry-pipeline decisions
- deciding which signal answers which operational question
- operational visibility reviews

## When NOT to use

- feature work with no observability surface change
- pure UI or frontend-only tasks

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Apply `$alaa-low-noise` when the task is non-trivial.
3. Read `references/00-topic-map.md`.
4. Load only the sections you need from `references/full-guide.md`.
5. If the target is an Ala backend, gateway, WA, entitlement, or future Ala service, load `$alaa-services-contract` before making implementation decisions.
6. Pair with the listed companion skills before making changes outside this skill's ownership.

## Ownership boundary

- This skill owns the signal model, SOC evidence model, signal-quality rules, Sentry role, SigNoz role, Collector mental model, alert/runbook quality, and incident diagnostics.
- `$alaa-services-contract` owns Ala-specific hard contracts: `X-Request-Id`, `traceparent`, `trace_id`, route families, `/api/health`, `/api/ready`, `/metrics`, middleware behavior, event/code names, metric names, trusted ingress, deploy topology, and current service boundaries.
- If the two appear to conflict on an Ala service, use `$alaa-services-contract` for exact platform shape and this skill for the underlying observability reasoning.

## Severity rubric

| Signal type | Use when                                                        |
|-------------|-----------------------------------------------------------------|
| log only    | the event is useful for forensics but not actionable on its own |
| metric      | you need durable trend visibility or SLO math                   |
| alert       | a human should investigate within working hours                 |
| page        | the condition is urgent enough to interrupt an operator now     |

## Companion routing

- $alaa-security-review
  - Pair when the task also touches security event semantics and sensitive data controls.
- $alaa-services-contract
  - Pair for Ala services, gateway, WA, entitlement-platform, or future service standardization.
- $alaa-octane-performance
  - Pair when the task also touches long-lived worker observability concerns.

## Reference navigation

- Section map and fast routing:
  - `references/00-topic-map.md`
- Full preserved guidance, rules, examples, and checklists:
  - `references/full-guide.md`

## Maintenance rules

- Keep this file routing-first and plain.
- Put detailed rules into `references/full-guide.md` instead of growing this file.
- Keep the topic map aligned with the actual headings in the full guide.
- Re-check companion-skill routing when ownership boundaries change.
