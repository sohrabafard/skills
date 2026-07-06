# Alaa Observability SOC Topic Map

Use this file to choose the smallest relevant reference for the task.

## Core routing

- Top-level activation, invariants, companion routing, and output contract:
  - `../SKILL.md`
- Full preserved guidance, examples, and domain rules:
  - `full-guide.md`
- Official-first source map and freshness triggers:
  - `90-source-map.md`
- Security-sensitive production/SOC checklists:
  - `91-sensitive-system-checklists.md`
- Cross-model skill/runtime compatibility for GPT-5.5/Codex, Opus 4.8, Sonnet 5, and Fable 5:
  - `95-model-runtime-compatibility.md`

## `full-guide.md` section index

- `# Purpose`
- `# When to use`
- `# Ownership and precedence`
- `# Step-by-step workflow (deterministic)`
- `# Signal decision matrix`
- `# Platform tool roles`
- `# OpenTelemetry and OTLP contract`
- `# OpenTelemetry alignment (mandatory for every Alaa service)`
- `# Collector architecture`
- `# SigNoz and Sentry role split`
- `# Cardinality budgets (mandatory)`
- `## Metrics label allowlist (default)`
- `## Trace attribute discipline`
- `# Mandatory logging standard (structured JSON)`
- `## Required fields (baseline)`
- `## Trace query fields`
- `## Authz denials (403) — response + log alignment`
- `## PII and secrets`
- `# Metrics guidance (SLA-friendly)`
- `# Trace guidance`
- `# Exceptions and Sentry`
- `# Profiling`
- `# SOC deliverable: Security log catalog`
- `# Evidence-first incident diagnostics`
- `# Sentry integration (optional; production-friendly)`
- `# Laravel 13 observability audit points`
- `# Output contract`
- `# Anti-patterns`
- `# Latency percentiles`
- `# Exemplars and metric-to-trace correlation`
- `# Per-application Vector sidecar collection`
- `# The central Collector must never become a bottleneck`
- `# SOC / SIEM egress`
- `# Collector selection (OTel Collector vs Vector vs Grafana Alloy)`
- `# Working with the SigNoz execution skill`
- `# 2026 security-sensitive additions`
- `## Profiles signal positioning`
- `## Service readiness evidence`
- `## Collector and Vector resilience validation`
- `## Safe SOC/SIEM forwarding model`

## Fast routing

- “Should this be a log, metric, trace, alert, Sentry event, or SOC event?”
  - `full-guide.md` → signal decision matrix, platform tool roles, and security-sensitive additions
- “Is this safe for a customer/security-sensitive system?”
  - `91-sensitive-system-checklists.md`
- “Can we add this metric label?”
  - `full-guide.md` → cardinality budgets and `91-sensitive-system-checklists.md` → cardinality gate
- “How do we link p99 latency to the trace that caused it?”
  - `full-guide.md` → latency percentiles and exemplars
- “Should Sentry receive OTLP directly?”
  - `full-guide.md` → Sentry/SigNoz role split and `90-source-map.md` freshness triggers
- “Write the SigNoz SQL or pick the SigNoz docs page.”
  - Hand off to `$alaa-signoz-clickhouse-docs`
