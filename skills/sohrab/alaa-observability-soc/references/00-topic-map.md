# Alaa Observability SOC Topic Map

Use this file to choose the smallest relevant section in `full-guide.md`.

## Covered sections

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
- `## 1) Install packages`
- `## 2) Laravel / Octane configuration`
- `## 3) Tracing (distributed tracing)`
- `## 4) Release tracking (CI-driven)`
- `## 5) Profiling (cost-controlled)`
- `## 6) Compatibility with OpenTelemetry / W3C Trace Context`
- `## 7) Validation (minimum)`
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
- `references/90-source-map.md`

## Working rule

- Read only the sections you need from `full-guide.md`.
- Read `90-source-map.md` before relying on version-sensitive observability, SigNoz, Sentry, or OTel guidance.
- Keep this topic map small and update it when major sections are added or renamed.
