---
name: logql-generator
description: Generate production LogQL queries for Grafana Loki — log stream selectors, line/label filters, parsers, metric queries, recording rules, and alerting. Use when authoring Loki log analysis, dashboards, or alerts. Do not use for PromQL metrics queries (use the PromQL skills), for Loki server configuration (use `loki-config-generator`), or for generic log analysis that does not require LogQL output.
---

# LogQL Query Generator

## Overview

Generate correct, efficient LogQL through an interactive planning workflow. This
`SKILL.md` is the slim router; the planning template, step-by-step builder, advanced
techniques, parser/function references, and examples live in `references/playbook.md`.
Load reference files (and `examples/`) by their skill-relative path (for example
`references/best_practices.md`) — never hard-code an absolute or pack-prefixed path, so
the skill resolves identically under Claude and Codex.

## Source freshness

- Read `references/source-map.md` before handling latest/current/version-sensitive Loki
  or LogQL behavior, syntax, functions, recording rules, label guidance, or query-runtime differences.
- Treat community posts, Stack Overflow, and issue threads as troubleshooting-only unless
  Grafana Loki docs confirm the guidance.

## When NOT to use

- PromQL metrics queries — use the PromQL skills.
- Loki server configuration — use `loki-config-generator`.
- Generic log analysis that does not require LogQL output.

## Workflow

1. Clarify intent: which streams (labels), what to filter, and whether the result is a log
   query, a metric query, or an alert.
2. Build the stream selector with low-cardinality labels first, then line/label filters,
   then parsers (`logfmt`, `json`, `pattern`, `regexp`).
3. For metrics, wrap with range/aggregation functions; for alerts, emit recording/alerting YAML.
4. Optimize for performance (filter early, avoid high-cardinality label extraction); see
   `references/best_practices.md`.
5. Present the query with a short explanation and assumptions.

Full planning template, step-by-step builder, advanced techniques, and references:
`references/playbook.md`.

## Reference map

- `references/playbook.md` — planning template, query builder, advanced techniques, parser/function reference
- `references/best_practices.md` — LogQL optimization and anti-patterns
- `references/source-map.md` — official-source map for version-sensitive claims
- `examples/` — reusable example queries
