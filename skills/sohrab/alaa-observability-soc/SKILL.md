---
name: alaa-observability-soc
description: "Ops-grade observability + SOC/SIEM integration: structured logs, correlation IDs, OpenTelemetry alignment, cardinality budgets, Sentry guidance, alert signals, runbooks, and evidence-first incident diagnostics."
---

# Purpose
Make the service operable under SLA and defensible when upstream systems fail (DBaaS/LB/SOC).

This skill defines how to design and validate operational signals (logs/metrics/traces/alerts) and the runbooks that make them actionable, with optional guidance for Sentry-based error tracking + performance monitoring in Laravel/Octane environments.

# When to use
- Adding or updating logs, metrics, traces, dashboards, or alerts
- Writing/updating runbooks/SOPs/SLA/SLO guidance
- Integrating with SOC/SIEM workflows and security event cataloging
- Incident/availability analysis and evidence collection
- Enabling or hardening Sentry (error tracking, tracing, releases, profiling) in Laravel/Octane

# Step-by-step workflow (deterministic)
1) Scope the operational goal (what signal, which env, which question/SLO)
2) Inventory existing signals (reuse names/IDs)
3) Define signal contracts (schema + semantics)
4) Update runbooks (detect → mitigate → verify → rollback)
5) Validate end-to-end (emit → ship → query/alert)

# OpenTelemetry alignment (mandatory when OTel is used)
If the service uses OpenTelemetry (traces and/or metrics):
- Use W3C Trace Context propagation (`traceparent`/`tracestate`) end-to-end (HTTP + async boundaries).
- For traces/metrics, prefer OpenTelemetry semantic conventions when available (HTTP, DB, messaging).
- Do not invent attribute names when semconv already defines one.
- Do not rename existing log schemas unilaterally:
    - keep stable log field names if already deployed
    - if needed, add mapping/additional fields rather than breaking ingestion/alerts
- Never put secrets/PII into OTel attributes.

# Cardinality budgets (mandatory)
Unbounded cardinality ruins metrics systems and makes alerts noisy.

## Metrics label allowlist (default)
Allowed labels should come from small, bounded sets. Typical safe labels:
- templated route name (not raw path)
- HTTP method
- status code or status class
- service/env/instance

Disallowed labels (default):
- `user_id`, `project_id` / tenant IDs, raw IPs/emails/device IDs
- raw URLs/query strings/headers
- exception messages as labels

Budget rules:
- Each label should be bounded (ideally < 50 distinct values).
- Avoid combining multiple medium-cardinality labels on one metric.
- Prefer logs (not metrics) for per-user/per-tenant debugging.

## Trace attribute discipline
- Traces can carry richer attributes than metrics, but still avoid raw IDs and PII by default.
- If identifiers are required, prefer short non-reversible fingerprints and only when policy allows.

# Mandatory logging standard (structured JSON)

## Required fields (baseline)
Include at minimum:
- `timestamp` (RFC3339/ISO8601), `level`
- `service`, `service_version`, `env`
- `request_id` and/or `trace_id`
- `project_id` (tenant identifier) when available (logs are the right place; avoid metrics labels)
- `user_id` when allowed (avoid PII; hash if required)
- request identity: `http.method`, `http.path` (or route name), `http.status`
- `duration_ms`
- `code` (stable internal error/decision code)

## Authz denials (403) — response + log alignment
When returning 403:
- Respond with stable `code` + user-facing `message`
- Log the same `code` (+ `ability` when safe)

## PII and secrets
- Never log passwords/secrets/full tokens.
- Prefer logging only token `jti` or a short fingerprint.

# Metrics guidance (SLA-friendly)
- Prefer low-cardinality labels; obey budgets.
- Use explicit units (ms, bytes, count).
- Recommended signals:
    - request rate, error rate, latency (p50/p95/p99)
    - DB error counts and latency buckets
    - queue lag/depth
    - worker RSS and restarts

# SOC deliverable: Security log catalog
Maintain a “security log catalog” that defines:
- event name, severity, required fields, detection intent

Minimum recommended events:
- `auth.login.failed`
- `auth.token.invalid`
- `authz.denied` (stable `code`)
- `rate_limit.exceeded`
- `input.validation.failed` (aggregate-level; no payload logging)
- `resource.access.suspicious`

# Evidence-first incident diagnostics
Collect evidence that distinguishes upstream faults from app faults:
- health endpoint outputs + timestamps
- DB connectivity/timeouts
- upstream 502/504 patterns + correlation IDs
- queue lag/depth + consumer health
- CPU/RAM + worker RSS

# Sentry integration (optional; production-friendly)

Use this section when the task is to standardize Observability with Sentry for Laravel 12 + Octane:
- error tracking
- distributed tracing
- release tracking
- profiling (cost-controlled)

## 1) Install packages
```bash
composer require sentry/sentry-laravel
```

If you need SDK-level features:
```bash
composer require sentry/sdk
```

## 2) Laravel / Octane configuration
Publish Sentry config (if used in the repo):
```bash
php artisan vendor:publish --provider="Sentry\\Laravel\\SentryServiceProvider"
```

Example env vars (do not commit real DSNs):
```dotenv
SENTRY_DSN=https://publicKey@o0.ingest.sentry.io/0
SENTRY_ENVIRONMENT=production
SENTRY_RELEASE=app@1.2.3
SENTRY_TRACES_SAMPLE_RATE=0.2
SENTRY_PROFILES_SAMPLE_RATE=0.1
SENTRY_SEND_DEFAULT_PII=false
```

Octane safety (mandatory mindset):
- Ensure Sentry scope/state does not leak between requests.
- Avoid request-scoped state stored in singletons/statics; reset per-request context where appropriate.

## 3) Tracing (distributed tracing)
Enable tracing with a conservative sample rate:
```dotenv
SENTRY_TRACES_SAMPLE_RATE=0.2
```

Add stable tags for key flows (keep low cardinality):
```php
<?php
\Sentry\configureScope(function (\Sentry\State\Scope $scope): void {
    $scope->setTag('flow', 'checkout'); // low-cardinality tag
});
```

## 4) Release tracking (CI-driven)
Prefer injecting release at build/deploy time:
```bash
export SENTRY_RELEASE="app@${GIT_SHA}"
```

If you use `sentry-cli` for releases (and sourcemaps where relevant):
```bash
sentry-cli releases new "${SENTRY_RELEASE}"
sentry-cli releases set-commits "${SENTRY_RELEASE}" --auto
sentry-cli releases finalize "${SENTRY_RELEASE}"
```

Optional: upload sourcemaps (if you have front-end build artifacts):
```bash
sentry-cli releases files "${SENTRY_RELEASE}" upload-sourcemaps ./public/build \
  --ext js --ext map --rewrite
```

## 5) Profiling (cost-controlled)
Enable profiling with a low sample rate:
```dotenv
SENTRY_PROFILES_SAMPLE_RATE=0.1
```

Keep production rates conservative; validate cost/overhead explicitly.

## 6) Compatibility with OpenTelemetry / W3C Trace Context
Regardless of Sentry/OTel, ensure W3C trace context headers are preserved end-to-end:
- `traceparent`
- `tracestate`
- `baggage`

If using gateways/proxies (Nginx/HAProxy/APISIX), ensure they preserve these headers.

## 7) Validation (minimum)
- DSN connectivity: confirm outbound connectivity to Sentry endpoints.
- Test error event:
```php
<?php
throw new \RuntimeException('Sentry test event');
```
Expected: event appears in Sentry project.
- Trace linking:
    - execute an end-to-end request
    - confirm transaction/spans are linked
    - confirm W3C headers are preserved

# Output contract
When applying this skill, output:
1) What changed and why
2) Signal contract(s) (fields/semantics) and where they live (code/docs)
3) Runbook/SOP changes (detect → mitigate → verify → rollback)
4) Validation steps and expected outcomes
5) Operational risks/follow-ups

# Anti-patterns
- Unstructured logs
- Logging secrets/PII
- Debug spam in hot paths
- High-cardinality metric labels
- Alerts without thresholds/noise control/runbook links
- Enabling high Sentry sample rates in production without cost/overhead validation
