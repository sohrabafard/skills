---
name: alaa-docs-farsi
description: "Use this skill when the task involves README or docs updates or docs and implementation alignment. Do not use it when logic changes with no doc impact."
---




# Alaa Docs Farsi

## Purpose

Use this skill when the task needs the architectural or policy guidance owned by Alaa Docs Farsi.

Keep this top-level file small. Load the references for the full rules, examples, and checklists.

## When to use

- README or docs updates
- docs and implementation alignment
- Postman collection sync
- operational or business-facing repo documentation work

## When NOT to use

- logic changes with no doc impact
- pure inline code annotation passes

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Apply `$alaa-low-noise` when the task is non-trivial.
3. Read `references/00-topic-map.md`.
4. Load only the sections you need from `references/full-guide.md`.
5. Pair with the listed companion skills before making changes outside this skill's ownership.

## Doc impact checklist

- Re-check `README` when install, setup, commands, or workflow expectations changed.
- Re-check the docs directory when architecture, operations, or business-facing behavior changed.
- Re-check API docs when request, response, auth, or error contracts changed.
- Re-check Postman collections when endpoints, examples, or auth flows changed.

## Companion routing

- $alaa-frontend-doc-annotations
  - Pair when the task also touches docblocks and inline code annotations.
- $alaa-php-clean-code
  - Pair when the task also touches backend contract and terminology alignment.

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
