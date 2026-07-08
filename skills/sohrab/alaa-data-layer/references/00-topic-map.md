# Alaa Data Layer Topic Map

Use this file to choose the smallest relevant section in [full-guide.md](./full-guide.md).

## Covered sections

- `# Purpose`
- `# When to use`
- `# Hard constraints`
- `# Postgres design policy (Production, Multi-Tenant)`
- `## A) Core principle — write-model is the source of truth`
- `## B) Enforce integrity in the DB (not only in code)`
- `## C) Multi-tenant boundary (must be enforced)`
- `## D) Read performance without corrupting truth`
- `## E) Audit & operations`
- `## F) Identifier naming policy (mandatory)`
- `# Postgres performance principles (performance-first)`
- `# Schema & migration safety checklist`
- `## Phased rollout discipline (default)`
- `## Large tables and lock avoidance`
- `## Partitioning (optional, only when justified)`
- `# Multi-tenant patterns (choose and apply consistently)`
- `## Index patterns (tenant column strategy)`
- `## RLS notes (only if used)`
- `# Concurrency patterns`
- `## Claim/work-queue pattern (Postgres)`
- `## Idempotency (DB-backed)`
- `# Read-models / projections (CQRS-light)`
- `## When to introduce a projection`
- `## Projection types`
- `## Update strategies (choose and document)`
- `# Query optimization workflow (deterministic)`
- `# Connection management (pooling + timeouts)`
- `## PgBouncer transaction-pooling guardrails (high-leverage)`
- `# Redis patterns (cache, locks, rate limiting) for high throughput`
- `## Cache key design (mandatory)`
- `## TTL discipline (mandatory)`
- `## Invalidation strategy (prefer event-driven)`
- `## Locks (baseline)`
- `## Idempotency keys (edge dedupe)`
- `## Rate limiting`
- `## Memory and eviction safety`
- `# Verification / Definition of Done`
- `# Anti-patterns`

## Language-lane references (outside full-guide.md)

These live in their own files, not in `full-guide.md`:

- `40-redis-verification-and-anti-patterns.md` also carries `## Availability and degraded mode (mandatory)` — shared by both lanes.
- `50-redis-laravel-octane.md` — Redis in Laravel 13 + Octane: repository-pattern gate, client/config baseline, boot/register safety, cache decorator, stampede control, processing uses (locks, rate limits, dedupe), invalidation and flush discipline, degraded mode when Redis is down, Octane connection rules.
- `51-redis-golang.md` — Redis in Go services: DB-query-cache-only policy, repository boundary gate, go-redis v9 configuration, degraded mode (error classification, singleflight, circuit breaker), locks and rate limits.

## Working rule

- Read only the sections you need from [full-guide.md](./full-guide.md).
- Use the rendered Markdown outline in `full-guide.md` to jump to the matching heading after you open it.
- Keep this topic map small and update it when major sections are added or renamed.
