---
name: alaa-cicd-laravel-postgres
description: "Deterministic Laravel CI/CD guidance for Postgres-backed services."
---

# Alaa CI/CD Laravel Postgres

## Purpose

Use this skill when the task needs the architectural or policy guidance owned by Alaa CI/CD Laravel Postgres.

Keep this top-level file small. Load the references for the full rules, examples, and checklists.

## When to use

- CI workflow edits
- test bootstrap or Postgres service changes
- quality-gate or cache-key updates
- pipeline flakiness or determinism issues

## When NOT to use

- feature changes with no pipeline impact
- docs-only tasks

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Apply `$alaa-low-noise` when the task is non-trivial.
3. Read `references/00-topic-map.md`.
4. Load only the sections you need from `references/full-guide.md`.
5. Pair with the listed companion skills before making changes outside this skill's ownership.

## Companion routing

- $alaa-docker-production
  - Pair when the task also touches image-build and runtime alignment.
- $alaa-observability-soc
  - Pair when the task also touches CI evidence and release visibility.

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
