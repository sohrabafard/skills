---
name: alaa-laravel-architecture
description: "Use this skill when the task involves layer boundary changes or controller, service, request, resource, or DTO contract work. Do not use it when pure coding-style cleanup with no architectural surface change."
---




# Alaa Laravel Architecture

## Purpose

Use this skill when the task needs the architectural or policy guidance owned by Alaa Laravel Architecture.

Keep this top-level file small. Load the references for the full rules, examples, and checklists.

## When to use

- layer boundary changes
- controller, service, request, resource, or DTO contract work
- public ID or route-binding policy changes
- event, outbox, or cross-module contract changes

## When NOT to use

- pure coding-style cleanup with no architectural surface change
- pure infra or CI tasks

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Apply `$alaa-low-noise` when the task is non-trivial.
3. Read `references/00-topic-map.md`.
4. Read `references/source-map.md` when latest/current/version/security-sensitive Laravel architecture behavior matters.
5. Load only the sections you need from `references/full-guide.md`.
6. Pair with the listed companion skills before making changes outside this skill's ownership.

## Architecture decisions

| If the decision is about...       | Default choice                                                                                           |
|-----------------------------------|----------------------------------------------------------------------------------------------------------|
| DTO vs Resource vs Model exposure | DTOs and Resources for boundaries; do not expose Eloquent models directly across public contracts        |
| Service vs Action vs Job          | Service/Action for synchronous domain flow; Job only when async delivery or queue semantics are required |
| public IDs or route binding       | public IDs stay stable and should not leak storage-specific keys                                         |
| cross-module events               | preserve explicit contracts and outbox-safe boundaries                                                   |

## Companion routing

- $alaa-php-clean-code
  - Pair when the task also touches local code style and refactor discipline.
- $alaa-trust-gateway-auth
  - Pair when the task also touches gateway-derived identity and trusted header semantics.
- $alaa-data-layer
  - Pair when the task also touches schema, query, and transaction decisions.

## Reference navigation

- Section map and fast routing:
  - `references/00-topic-map.md`
- Official-first source map and freshness triggers:
  - `references/source-map.md`
- Full preserved guidance, rules, examples, and checklists:
  - `references/full-guide.md`

## Maintenance rules

- Keep this file routing-first and plain.
- Put detailed rules into `references/full-guide.md` instead of growing this file.
- Keep the topic map aligned with the actual headings in the full guide.
- Re-check companion-skill routing when ownership boundaries change.
