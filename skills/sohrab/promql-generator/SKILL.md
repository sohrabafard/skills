---
name: promql-generator
description: Generate production PromQL queries, recording rules, and alerting rules — including native histograms (Prometheus 3.x) and SLO / error-budget / burn-rate patterns. Use when authoring Prometheus queries, monitoring dashboards, or alert/recording rules. Do not use for LogQL log queries (use `logql-generator`), for validating existing PromQL with no generation need (use `promql-validator`), or for non-Prometheus observability where PromQL output is not required.
---

# PromQL Query Generator

## Overview

Generate correct, production-grade PromQL through an interactive planning workflow. This
`SKILL.md` is the slim router; the planning template, native-histogram guidance, SLO/burn-rate
patterns, advanced techniques, and examples live in `references/playbook.md`. Load reference
files by their skill-relative path (for example `references/promql_patterns.md`) — never
hard-code an absolute or pack-prefixed path, so the skill resolves identically under Claude
and Codex.

## Source freshness

- Read `references/source-map.md` before handling latest/current/version-sensitive
  Prometheus, PromQL, native histogram, feature-flag, function, operator, recording-rule,
  or alerting behavior.
- Treat community posts, Stack Overflow, and issue threads as troubleshooting-only unless
  Prometheus docs confirm the guidance.

## When NOT to use

- LogQL log queries — use `logql-generator`.
- Validating existing PromQL with no generation need — use `promql-validator`.
- Non-Prometheus observability where PromQL output is not required.

## Workflow

1. Clarify intent: metric(s), metric type (counter/gauge/histogram/summary), labels,
   time window, and whether this is a query, recording rule, or alert.
2. Pick the correct pattern (rate/increase, aggregation, histogram quantiles, native
   histograms, SLO/burn-rate) from `references/promql_patterns.md`.
3. Build the query with correct function/operator usage (`references/promql_functions.md`,
   `references/metric_types.md`).
4. Validate logic and label matching; hand off to `promql-validator` for deep checks.
5. For rules, produce recording/alerting YAML with sensible names, `for`, and labels.
6. Present the query with a short explanation and any assumptions.

Full planning template, native-histogram and SLO patterns, and worked scenarios:
`references/playbook.md`.

## Reference map

- `references/playbook.md` — interactive planning template, native histograms, SLO/burn-rate, advanced techniques, scenarios
- `references/promql_patterns.md` — reusable query patterns
- `references/promql_functions.md` — function/operator reference
- `references/metric_types.md` — metric-type semantics
- `references/best_practices.md` — PromQL best practices
- `references/source-map.md` — official-source map for version-sensitive claims
