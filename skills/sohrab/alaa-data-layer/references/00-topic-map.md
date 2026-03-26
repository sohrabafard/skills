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

## Working rule

- Read only the sections you need from [full-guide.md](./full-guide.md).
- Use the rendered Markdown outline in `full-guide.md` to jump to the matching heading after you open it.
- Keep this topic map small and update it when major sections are added or renamed.
