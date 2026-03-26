---
name: alaa-docker-production
description: "Production Docker and Compose hardening for Laravel and PHP services."
---

# Alaa Docker Production

## Purpose

Use this skill when the task needs the architectural or policy guidance owned by Alaa Docker Production.

Keep this top-level file small. Load the references for the full rules, examples, and checklists.

## When to use

- Dockerfile or Compose hardening
- image size or attack-surface reduction
- runtime user, healthcheck, or secret handling changes
- release evidence or deterministic image work

## When NOT to use

- pure app logic changes
- non-containerized local-only tasks

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Apply `$alaa-low-noise` when the task is non-trivial.
3. Read `references/00-topic-map.md`.
4. Load only the sections you need from `references/full-guide.md`.
5. Pair with the listed companion skills before making changes outside this skill's ownership.

## Companion routing

- $alaa-cicd-laravel-postgres
  - Pair when the task also touches pipeline alignment for image builds.
- $alaa-security-review
  - Pair when the task also touches runtime hardening and secret handling.

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
