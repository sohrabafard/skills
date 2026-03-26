---
name: alaa-mongodb-patterns
description: "Use this skill when the task involves MongoDB collections, indexes, or write patterns or TTL, compound indexes, or bounded document design. Do not use it when repos that are still Postgres-only."
---




# Alaa MongoDB Patterns

## Purpose

Use this skill when the task needs the architectural or policy guidance owned by Alaa MongoDB Patterns.

Keep this top-level file small. Load the references for the full rules, examples, and checklists.

## When to use

- MongoDB collections, indexes, or write patterns
- TTL, compound indexes, or bounded document design
- idempotent writes or event-style MongoDB flows

## When NOT to use

- repos that are still Postgres-only
- tasks that introduce MongoDB without explicit approval

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Apply `$alaa-low-noise` when the task is non-trivial.
3. Read `references/00-topic-map.md`.
4. Load only the sections you need from `references/full-guide.md`.
5. Pair with the listed companion skills before making changes outside this skill's ownership.

## Rollout checklist

- Rehearse TTL index changes with expected expiry delay and operational visibility.
- Treat compound index additions as rollout work, not just schema text.
- Keep backfills idempotent and resumable before running them at scale.
- Re-check query plans after each index or TTL change instead of assuming the new shape helped.

## Companion routing

- $alaa-data-layer
  - Pair when the task also touches cross-store contract and ownership decisions.
- $alaa-security-review
  - Pair when the task also touches tenant and trust-surface checks.

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
