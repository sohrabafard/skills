---
name: alaa-data-layer
description: "Postgres truth-first data-layer policy for multi-tenant services plus Redis cache and lock guidance, including dedicated Redis lanes for Laravel 13/Octane and Go services with a mandatory repository-pattern gate and Redis-down degraded-mode fallback. Use when schema, migration, query, cache, or Redis behavior changes. Do not use it to introduce a new datastore by default."
---




# Alaa Data Layer

## Purpose

Use this skill when the task needs the data-layer or Redis policy owned by Alaa Data Layer.

Keep this top-level file small. Load the references for the full rules, examples, and checklists.

## When to use

- schema, constraint, or migration design
- tenant boundary or index strategy work
- query, locking, pooling, or projection tuning
- Redis cache, lock, idempotency, or rate-limit design

## When NOT to use

- do not use it to introduce a new datastore that the user did not request
- do not use it for framework-only refactors with no schema, query, or Redis surface

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Apply `$alaa-workflow` when the task is long or risky.
3. Read `references/00-topic-map.md`.
4. Read `references/source-map.md` when latest/current/version/security-sensitive database or Redis behavior matters.
5. Load only the reference file that matches the current decision.
6. Pair with the listed companion skills before changing architecture, security, async, or runtime behavior outside this skill's ownership.

## Fast entry

| Symptom or decision                                    | Start with                                               |
|--------------------------------------------------------|----------------------------------------------------------|
| tenant boundaries, public IDs, or core schema shape    | `references/10-postgres-design-and-tenant-boundaries.md` |
| additive migration rollout, large tables, or indexes   | `references/20-schema-migrations-and-performance.md`     |
| locks, retries, pooling, hot queries, or projections   | `references/30-concurrency-projections-and-pooling.md`   |
| Redis cache, lock, idempotency, or rate-limit behavior | `references/40-redis-verification-and-anti-patterns.md`  |
| Redis in a Laravel 13 / Octane service (integration, fallback, flush discipline) | `references/50-redis-laravel-octane.md` |
| Redis in a Go service (DB-query cache, client config, degraded mode) | `references/51-redis-golang.md` |

## Companion routing

- $alaa-laravel-architecture
  - Pair when the task also changes module boundaries, DTO flow, or public API contracts.
- $alaa-security-review
  - Pair when the task also changes tenant isolation, sensitive data handling, or abuse controls.
- $alaa-async-messaging
  - Pair when projections, outbox consumers, retries, or job safety are part of the design.
- $alaa-octane-performance
  - Pair when hot paths, worker lifetime, or memory reuse affect DB or Redis behavior.
- $alaa-partitioned-table-fk-audit
  - Pair when auditing or hardening a Postgres schema for the id-only-FK-into-a-partitioned-parent bug class (SQLSTATE 42830), or when a migration fails with "no unique constraint matching given keys."
- $alaa-php-clean-code
  - Pair when Laravel Redis work needs the repository policy, decorator pattern, or Octane-safe code shape (the repository gate in `references/50-redis-laravel-octane.md`).
- $alaa-golang
  - Pair for any Go Redis work; its `references/61-redis-cache-layer.md` is the Go cache-pattern authority that `references/51-redis-golang.md` builds on.

## Reference navigation

- Section map and fast routing:
  - `references/00-topic-map.md`
- Official-first source map and freshness triggers:
  - `references/source-map.md`
- Postgres design, integrity, tenant boundaries, and identifier policy:
  - `references/10-postgres-design-and-tenant-boundaries.md`
- Migration rollout, large-table safety, and performance-first schema work:
  - `references/20-schema-migrations-and-performance.md`
- Concurrency, projections, query optimization, and pooling rules:
  - `references/30-concurrency-projections-and-pooling.md`
- Redis patterns, verification rules, and anti-patterns:
  - `references/40-redis-verification-and-anti-patterns.md`
- Redis in Laravel 13 + Octane (repository gate, decorator seam, boot safety, degraded mode):
  - `references/50-redis-laravel-octane.md`
- Redis in Go services (DB-query cache only, go-redis config, degraded mode):
  - `references/51-redis-golang.md`
- Full preserved guidance, rules, examples, and checklists:
  - `references/full-guide.md`

## Maintenance rules

- Keep this file routing-first and plain.
- Put detailed rules into `references/` instead of growing this file.
- Keep the topic map aligned with the actual headings in the full guide.
- Keep every new example, checklist, and anti-pattern in simple English.
