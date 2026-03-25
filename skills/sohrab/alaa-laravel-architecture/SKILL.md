---
name: alaa-laravel-architecture
description: "Alaa-style Laravel 13 architecture: strict layering, DTO boundaries, stable API envelopes, UUIDv7 public_id policy, event-driven side effects via outbox, and upgrade-safe framework defaults."
---

# Purpose
Enforce consistent, production-grade Laravel service design that matches Alaa/comment-service conventions:
- Strict layering (Controller → Service → Repository → Resource)
- Stable request/response contracts (including a user-safe, code-based error envelope)
- DTO/Enum boundaries (no raw arrays between layers)
- UUIDv7 `public_id` as the only external identifier
- Event-driven side effects with listeners + outbox (idempotent, retryable)

This skill is domain-agnostic: it prescribes *how* to design and implement, not which endpoints/entities to build.

# Companion skill boundary
Before writing or refactoring PHP / Laravel code with this skill, read `alaa-php-clean-code` and apply it for:
- clean code and SOLID
- design-pattern selection and anti-pattern avoidance
- PHP 8.x modern features and type safety
- PSR / PER standards
- general PHP / Laravel best practices

This skill remains the source of truth for layering, API contracts, `public_id`, and event / outbox architecture. Do not duplicate or override `alaa-php-clean-code`; use it inside these architecture boundaries.

# When to use
- Building a new Laravel service or module that must match comment-service engineering style.
- Adding or changing endpoints where consistency, maintainability, and testability matter.
- Refactoring for architecture correctness (layering, contracts, naming, boundaries).
- Implementing or adjusting event-driven side effects and outbox publishing rules (at the Laravel layer).

# Constraints
- Prefer minimal diffs; do not rewrite large parts “for cleanliness” unless explicitly requested.
- Keep controllers thin and deterministic; business rules must live in Services.
- Do not introduce new datastores, transports, or frameworks unless the user explicitly requests.
- Do not “standardize” response envelopes by refactoring existing behavior unless the repository already uses the target contract.

# Laravel 13 architecture stance
When the repository targets Laravel 13:
- Keep framework-owned bootstrap, middleware, and exception configuration aligned with the Laravel 13 application skeleton unless the repository has an intentional override.
- Update direct CSRF middleware references to `PreventRequestForgery` when touching middleware exclusions, tests, or bootstrap configuration.
- Compare `bootstrap/app.php`, middleware registration, and framework defaults before copying Laravel 12 boilerplate into new code.
- Prefer first-party JSON:API resources only when the public contract is truly JSON:API. Otherwise, keep the repository's established resource envelope.
- Prefer `Queue::route(...)` or queue attributes when queue routing, retries, or timeout rules become repetitive, but do not force an attribute-first style into a repository that already uses methods consistently.
- When upgrade work touches routing or Eloquent infrastructure, audit domain route precedence, polymorphic pivot table names, eager-loaded relation restoration in serialized model collections, and Bootstrap pagination view names.
- Treat Laravel 13 AI, semantic search, and vector search capabilities as opt-in. If the repository adopts them, route schema and indexing choices through `alaa-data-layer` and keep public contracts explicit.

# Architecture rules (strict)

## Layering responsibilities
**Controller**
- Orchestration only.
- Calls `$request->validated()` (FormRequest) and passes validated data to Service.
- Does not contain business rules or query logic.

**Service / Domain Service**
- Business rules, domain invariants, authorization checks (Policy/Gate).
- Emits domain events for side effects.
- Returns domain objects/DTOs suitable for Resources (not raw arrays intended for API).

**Repository**
- Data access only: query composition, persistence, atomic updates/counters.
- Accepts and resolves `public_id` (UUIDv7) for external references; never exposes internal IDs.

**DTO**
- Boundary object between layers (input/output).
- No raw arrays crossing layer boundaries.

**Resource / Transformer**
- Output mapping only.
- Owns API JSON shape for success responses.

**Policy / Gate**
- Authorization rules.
- Services must call Policy/Gate (do not hide auth decisions in Controllers or Repositories).

**Observer**
- Reacts to model changes (side-effect triggers only).
- Must not contain domain decisions; prefer domain events from Services for user-driven actions.

## Allowed flow
- `Controller -> Service -> Repository -> DB`
- `Controller -> Resource -> JSON`

## Not allowed
- Controller calling Repository directly.
- Service returning raw arrays as API output.
- Repository containing business rules.
- Validation rules inside Controllers or Services.

# API contracts (default Alaa/comment-service shape)

## Request validation (mandatory)
- Every write endpoint uses a **FormRequest**.
- Controller passes only `$request->validated()` to the Service.
- Never embed validation logic inside Controllers or Services.

## Success envelope (mandatory)
- Use a **Resource/Transformer** for all successful responses.
- Single resource:
```json
{
  "data": {
    "id": "<public_id>",
    "...": "..."
  }
}
```
- List response:
    - `data` is an array
    - include pagination metadata when applicable (keep it consistent across endpoints)

## Error envelope (stable code + safe message)
By default (if the repo already uses this pattern), use a consistent, user-safe error object:
```json
{
  "error": {
    "status": 403,
    "code": "COMMENT_EDIT_WINDOW_EXPIRED",
    "message": "You can edit your comment only within 10 minutes of posting.",
    "meta": {
      "ability": "update"
    }
  }
}
```

### Error rules
- `code` must be stable and `UPPER_SNAKE_CASE`.
- `message` is safe for users (English, i18n-ready).
- `meta` contains only safe, non-sensitive context.
- Authorization denials should be observable (see “AuthorizationDenied event” below).

> If the repository already uses pure RFC 7807 (`type/title/detail` etc.), do not change it; keep the existing contract and only add missing fields (like `code`) if it matches repo conventions.

## Public ID policy (mandatory)
- All external/public identifiers must be UUIDv7 `public_id`.
- API responses must expose `public_id` as `id` (never expose internal numeric IDs).
- Route binding and request filters must accept `public_id` and resolve internally in Repository.
- Repositories may keep internal numeric IDs, but those are never part of public contracts.

## Persistence naming vs public contract naming
- Keep persistence naming and external API naming as separate concerns.
- Persistence-facing identifiers MUST stay lower_snake_case:
    - table names
    - column names
    - index and constraint names
    - raw Eloquent attribute names used by Repositories, Services, factories, seeders, and DB assertions
- Resources and transformers own outward serialization and may emit a different public field name when the contract requires it.
- Do not mirror camelCase or presentation-driven API names into schema identifiers just to reduce mapping code.
- When a public contract preserves an existing camelCase field, keep the translation at the Resource / DTO / Request boundary and keep the underlying persistence layer canonical.

## Pagination & filtering
- Support `per_page` with a sane upper bound.
- Map filters into DTOs (e.g., `<Domain>FilterData`) rather than passing raw arrays.

# Naming conventions (default)
- Service: `<Domain>Service` (e.g., `CommentService`)
- Repository: `<Store><Domain>Repository` (e.g., `PostgresCommentRepository`)
- DTO: `<Domain>Data`, `<Domain>FilterData`
- Events: past tense, domain-specific (e.g., `CommentCreated`, `ReactionAdded`)
- Enums: single-responsibility, descriptive (e.g., `CommentStatus`)
- Factory: `<Thing>Factory` (only when creation logic is non-trivial)

# Event-driven & outbox rules (Laravel layer)

## Domain events
- Emit domain events from **Services** (not from Controllers).
- Event names are past-tense and domain-specific.
- Use an Enum for event type values to avoid string drift.
- Bind events to listeners in `EventServiceProvider`.

## Listeners
- Listeners perform side effects (persist outbox, broadcast, external webhook, analytics).
- Listener class names should start with `Persist` or clearly describe the side effect.
- Prefer queued listeners (`ShouldQueue`) for IO work.

## Outbox pattern (if present in the repo)
- Persist every domain event into `outbox_events`.
- State machine (typical):
    - `pending`, `processing`, `published`, `failed`
- Claim/publish pattern (typical):
    - transaction + `FOR UPDATE SKIP LOCKED`
- Retries:
    - bounded attempts + backoff (config-driven)
- Idempotency:
    - every event must carry a stable idempotency key
    - consumers must assume at-least-once delivery

## Optional realtime
- Broadcasting is an optional driver behind a stable interface.
- Domain logic must not depend on a specific driver implementation.

## Observers vs Events
- Observer reacts to model changes (e.g., status/meta updates) and may emit events.
- Service is the primary source of domain events for user-driven actions.

## AuthorizationDenied event (observability hint)
When returning 403 with a stable `code`, emit a lightweight domain/telemetry event (e.g., `AuthorizationDenied`) that includes:
- `code`
- `ability` (safe)
- `project_id` / tenant identifier (safe)
- correlation/request id (if available)
  Do not include secrets or PII.

# Recommended workflow (deterministic)
1) Identify endpoints / use-cases and their domain objects.
2) Define DTOs for inputs (validated) and filters.
3) Implement Services:
    - enforce invariants
    - call Policy/Gate for authorization
    - emit domain events for side effects
4) Implement Repositories:
    - data access only
    - align indexes with query patterns (do not add speculative indexes)
5) Implement Resources:
    - produce stable `data` envelope
    - expose `public_id` as `id`
6) Add/adjust tests for behavior changes (do not claim passing unless executed).
7) Update docs (if needed) to reflect the contract and error codes.

# Anti-patterns
- “God controller” with validation, authorization, queries, and business rules mixed together.
- Passing arrays between layers instead of DTOs.
- Repositories containing business rules or authorization decisions.
- Exposing internal IDs or accepting them in public APIs.
- Emitting events before DB commit or without outbox durability (when outbox exists).
- Infinite retries, non-idempotent handlers, or DLQ-less designs.


