---
name: alaa-octane-performance
description: "Laravel Octane (Swoole/RoadRunner) production patterns: Octane-safe memory hygiene, multi-tenant safety, performance-first request paths, capacity-aware worker tuning, and PHP 8.1+ hot-path guidance."
---

# Purpose
Provide deterministic, production-grade guidance for Laravel running under Octane (Swoole/RoadRunner) where workers are long-lived.

Focus:
- Prevent cross-request state leaks (tenant/user/context, caches, singletons)
- Keep request hot paths fast and predictable
- Enforce tenant boundaries reliably under concurrency
- Make async/offload safe (idempotency + retries) without blocking request workers
- Tune workers with explicit assumptions and validate via load testing
- Apply modern PHP 8.1+ patterns that reduce allocations and improve hot-path clarity

This skill complements:
- `alaa-laravel-architecture` (layering, DTO boundaries, API/error contracts)
- `alaa-async-messaging` (queues/outbox/DLQ/idempotency details)
- `alaa-observability-soc` (structured logs, SOC catalog, evidence-first incidents)
- `alaa-workflow` (plan file + minimal terminal output + end-of-task report)

# When to use
- Implementing or refactoring Laravel code running under Octane (controllers/services/jobs/events/listeners)
- Investigating latency/throughput issues (p95/p99), worker RSS creep, or suspicious cross-request behavior
- Designing performance-sensitive endpoints (hot paths)
- Queue/event-driven changes that must remain safe under at-least-once delivery
- Any change where multi-tenancy boundaries must be guaranteed
- Performance-sensitive PHP utilities (serialization, parsing, hot loops) used by the service

# Constraints
- Prefer minimal diffs; do not rewrite large parts “for performance”.
- Do not introduce new transports/datastores unless the user explicitly requests.
- Do not change the API/error envelope unless the repo already uses the target contract.
- If the task is non-trivial, follow `alaa-workflow` and create/update the plan file.

# Octane invariants (mandatory)

## 1) Long-lived workers
Assume request workers are long-lived:
- Never store request-specific data in static properties or global singletons.
- Treat container singletons as cross-request memory unless proven safe.
- Avoid mutating runtime config, locale, auth state, or global caches during a request.

## 2) Tenant/user context hygiene
Multi-tenant systems are especially sensitive under Octane:
- Tenant context (e.g., `project_id` / `tenant_id`) must be derived server-side (trusted), not from untrusted client fields.
- Any “current tenant” holder must be request-scoped and cleared/reset each request.
- If you use a per-request tenant context object, ensure it is not cached as a singleton across requests.
- If caching derived data, include tenant identifier in cache keys (or use tagged caches correctly).

## 3) Cached instances & mutable services
Be defensive with:
- Singleton services that hold “current user/tenant”.
- Static caches keyed too broadly.
- Reused HTTP clients without timeouts or with mutable headers.

If you must keep a singleton:
- Make it immutable and tenant-agnostic.
- Pass tenant/user context explicitly as method args.
- Ensure per-request state lives in request-scoped objects only.

## 4) Reset patterns
If the codebase uses Octane listeners/hooks, prefer explicit reset hooks for:
- per-request in-memory caches
- tenant context holders
- any mutable global registry

# Performance patterns (Laravel-idiomatic)

## Validation and early rejection
- Use Form Requests for validation and early rejection.
- Minimize work before authz + validation completes.

## Authorization
- Use Policies/Gates; checks must be tenant-aware.
- Do not rely on client-submitted tenant identifiers.

## Avoid N+1
- Eager load with `with()` / `load()` where needed.
- Constrain selected columns (`select(...)`) and use `withCount()` when counts are required.
- Prefer repository-level query composition for critical endpoints.

## Transactions
- Use `DB::transaction()` for multi-write invariants.
- Keep transactions short and avoid external IO inside them.
- Prefer row-level atomic updates over “read-modify-write” under concurrency.

## Async offload
- Offload slow/IO-heavy work to queues/listeners.
- Jobs/handlers must be idempotent:
    - use unique constraints, dedupe keys, or idempotency keys
    - expect at-least-once delivery
- Apply bounded retries + backoff (+ jitter) and DLQ strategy (see `alaa-async-messaging`).

## Caching
- Cache only stable, derived data.
- TTL must be explicit.
- Define invalidation hooks (events) or accept eventual consistency intentionally.
- In multi-tenant systems:
    - cache keys must include tenant identifier
    - never share cached data across tenants unless explicitly intended and proven safe

# PHP 8.1+ performance patterns (Octane-friendly)
Use these rules for hot paths and reusable utilities (framework-agnostic code), especially under Octane.

## Core rules
- Add `declare(strict_types=1);` in new PHP files unless repo conventions differ.
- Use typed properties and return types; narrow types where possible.
- Prefer immutable Value Objects and DTOs.
- Prefer `match` and Enums for closed sets.
- Avoid heavy reflection and dynamic magic (`__get`, `__call`) in hot paths.

## Practical performance guidance
- Measure before optimizing; profile if tooling exists.
- Avoid repeated allocations in hot paths:
    - build arrays once and reuse
    - avoid needless copies of large strings/arrays
- Prefer streaming/iterators for large datasets; do not materialize huge arrays unless needed.
- Avoid excessive `json_encode`/`json_decode` churn:
    - validate schema once
    - encode once at the boundary
- Be careful with `DateTime` creation in loops; reuse a `DateTimeImmutable` when safe.

## Error handling
- Throw specific exceptions (domain exceptions) instead of generic `Exception`.
- Put context in structured logs (safe fields), not in exception messages when it risks leaking sensitive data.

## Laravel interop
- Keep framework-agnostic utilities free of facades/service locator.
- Accept dependencies via constructor or explicit arguments.
- For API serialization, prefer Resources/Transformers rather than manual JSON assembly.

## Output contract for micro-optimizations
If you introduce an optimization:
- state the trade-off (readability vs speed/memory)
- show how to verify (benchmark/profiling or at least a test + reasoning)

# Multi-tenancy rules (mandatory)
- Every query and write must be tenant-scoped.
- Never trust `tenant_id`/`project_id` from client input unless it is:
    - derived from a trusted auth token/claims, OR
    - derived from server-side routing (subdomain/host mapping), OR
    - verified against server-side permissions

## Acceptable enforcement approaches (choose one, document it)
1) Middleware sets trusted tenant context + model/global scopes enforce filtering
2) Explicit tenant filtering in Services/Repositories for every read/write
3) Postgres RLS (only if the repo already uses it) with session variables set by middleware

Whatever approach is used:
- Make it testable (feature tests must prove cross-tenant access is impossible).
- Ensure Octane request boundaries do not leak tenant context.

# Error handling & observability (Octane-safe)
- Throw domain exceptions; map to HTTP responses centrally.
- Log structured context:
    - tenant identifier (e.g., `project_id`)
    - user identifier (if available and non-PII)
    - request_id / trace_id / correlation_id
- Never log secrets, passwords, or full tokens.
- For authz denials, prefer stable internal error codes (for alerting), consistent with the repo’s error contract.

For SOC-oriented log catalogs and incident evidence practices, use `alaa-observability-soc`.

# Capacity-aware Octane tuning (starting point; validate with load test)
Always state assumptions (RPS, peak multiplier, headroom). Then start with:
- Request workers (Swoole baseline): `workers ≈ vCPU * 2`
- Task workers (if used): `task_worker_num ≈ vCPU` (adjust if DB is bottleneck)
- `max_requests`: 1000–5000 to cap memory creep (tune based on RSS behavior)

Rules:
- Do not raise workers without considering DB connection limits.
- Change one tuning knob at a time; validate with load tests and metrics.

# Testing expectations
- Add feature tests for endpoints and critical flows (including cross-tenant isolation).
- Add unit tests for pure business logic.
- For bugfixes: add a regression test first, then fix.

Typical verification commands (choose what repo uses):
- `php artisan test`
- `vendor/bin/pest`
- `vendor/bin/phpunit`

Do not claim green unless executed in the target environment.

# Output contract (when applying this skill)
- If multi-step: follow `alaa-workflow` and create/update the plan file.
- Provide:
    1) short plan (or link to plan file) + touched files (paths only)
    2) minimal diffs focused on correctness/performance
    3) tests added/updated
    4) exact run/verify commands and expected outcomes

Never auto-commit.

# Anti-patterns
- Storing tenant/user context in statics/singletons under Octane.
- “Fixing performance” by broad refactors that change unrelated code.
- Blocking request workers on slow IO (external calls, heavy queries) when offload is feasible.
- Cache keys that omit tenant identifier (cross-tenant leakage risk).
- Increasing workers without sizing DB pools/connection limits.
- Infinite retries or non-idempotent jobs/handlers.
