---
name: alaa-octane-performance
description: "Octane-safe patterns for hot paths, long-lived workers, request-state reset, and performance tuning."
---

# Alaa Octane Performance

## Purpose

Use this skill when the task needs the architectural or policy guidance owned by Alaa Octane Performance.

Keep this top-level file small. Load the references for the full rules, examples, and checklists.

## When to use

- Octane, Swoole, or RoadRunner runtime work
- hot-path request performance
- singleton or worker-state safety
- cross-request leak prevention

## When NOT to use

- standard FPM-only tasks with no Octane concerns
- pure docs work

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Apply `$alaa-low-noise` when the task is non-trivial.
3. Read `references/00-topic-map.md`.
4. Load only the sections you need from `references/full-guide.md`.
5. Pair with the listed companion skills before making changes outside this skill's ownership.

## Companion routing

- $alaa-observability-soc
  - Pair when the task also touches metrics and traces for long-lived workers.
- $alaa-data-layer
  - Pair when the task also touches DB and cache performance decisions.

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
