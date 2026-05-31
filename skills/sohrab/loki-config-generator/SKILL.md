---
name: loki-config-generator
description: Generate production Grafana Loki server configurations (storage, schema, ruler, limits, compactor) and Grafana Alloy log-collection configs. Use when creating Loki deployments, configuring Loki servers, or building log-aggregation systems. Do not use for writing LogQL queries (use `logql-generator`), for PromQL metrics queries or alert expressions, or for non-Loki logging stacks unless you are converting them to Loki configuration.
---

# Loki Configuration Generator

## Overview

Generate production-ready Grafana Loki server configurations and Grafana Alloy
log-collection configs (Promtail is deprecated since 3.4 — use Alloy). This `SKILL.md`
is the slim router; the configuration workflow, production checklist, monitoring
recommendations, Helm deployment, and full examples live in `references/playbook.md`.
Load reference files by their skill-relative path (for example
`references/loki_config_reference.md`) — never hard-code an absolute or pack-prefixed
path, so the skill resolves identically under Claude and Codex.

## Source freshness

- Read `references/source-map.md` before handling latest/current/version/security-sensitive
  Loki, Alloy, Helm, storage, schema, ruler, or Promtail-migration behavior.
- Treat community posts, Stack Overflow, and issue threads as troubleshooting-only unless
  Grafana Loki or Alloy docs confirm the guidance. Current stable referenced: Loki 3.6.x.

## When NOT to use

- Writing LogQL queries — use `logql-generator`.
- PromQL metrics queries or alert expressions.
- Non-Loki logging stacks unless converting them to Loki configuration.

## Workflow

1. Determine deployment mode (monolithic, simple-scalable, microservices) and target Loki version.
2. Read `references/best_practices.md` and `references/loki_config_reference.md` before generating.
3. Generate the config: `schema_config` (current `tsdb`/`v13`), object storage, limits,
   compactor, ruler, and caching — avoid deprecated keys.
4. For log collection, generate a Grafana Alloy config (not Promtail).
5. Apply the production checklist (retention, replication, limits, auth, WAL) and add
   monitoring recommendations.
6. Provide Helm deployment notes and usage instructions.

Full workflow, production checklist, monitoring, Helm, and complete examples:
`references/playbook.md`.

## Reference map

- `references/playbook.md` — configuration workflow, production checklist, monitoring, Helm, examples
- `references/loki_config_reference.md` — Loki config-block reference
- `references/best_practices.md` — Loki best-practice ruleset
- `references/source-map.md` — official-source map for version-sensitive claims
