---
name: alaa-laravel-public-api-contract-pack
description: Use this skill when a Laravel service needs a source-backed public client API contract pack, TypeScript SDK input docs, `docs/contracts/<service>` artifacts, OpenAPI/Postman parity, route inventory, or public-vs-trusted header boundary extraction. Keep the work docs-only unless the user explicitly asks for code changes, and mark unproven behavior as `NEEDS_BACKEND_CONFIRMATION` or `not_implemented` instead of inventing contracts.
---

# Laravel Public API Contract Pack

## Purpose

Build Laravel public client-facing API contract packs from executable repository truth, so SDK/frontend engineers can rely on the docs without reading backend source.

## When to use

- The user asks for a complete public API contract pack for a Laravel service.
- The output is intended for a TypeScript SDK, frontend integration, Postman, Insomnia, or OpenAPI consumer.
- Existing docs, Postman, OpenAPI, routes, or tests may be out of sync and need source-backed reconciliation.
- The task needs explicit separation between public client inputs and trusted gateway/backend-only headers.

## When NOT to use

- The task is not about a Laravel service public API surface.
- The user asks to implement backend behavior rather than document the public contract.
- The task is only a narrow Postman edit; use `$alaa-postman-collections`.
- The task is only gateway trust semantics; use `$alaa-trust-gateway-auth`.

## Workflow

1. Confirm the service name and target path, usually `docs/contracts/<service>`.
2. Read repo-local `AGENTS.md`, existing contract docs, route files, tests, Postman/OpenAPI artifacts, and any public API audit commands.
3. Build a route inventory from executable truth first:
   - route declarations
   - `php artisan route:list` when available
   - controller actions, form requests, resources, middleware, policies, and public API tests
4. Treat prose docs as hypotheses until routes/tests/controllers support them.
5. Keep the pack docs-only unless the user explicitly expands scope to code, tests, or runtime behavior.
6. Mark uncertainty visibly:
   - `NEEDS_BACKEND_CONFIRMATION` for behavior that exists but cannot be proven from current repo truth
   - `not_implemented` for requested or documented surfaces with no executable route/controller support
7. Align OpenAPI, Postman, examples, schemas, auth notes, and error docs to the same source-backed contract.
8. End with exact validation commands and results.

## Source priority

Prefer evidence in this order:

1. live framework inspection and route inventory
2. public API tests and repo-native audit commands
3. route/controller/request/resource/middleware/policy source
4. existing OpenAPI and Postman artifacts
5. existing docs and comments
6. memory or prior runs, only after current repo truth is checked

## Public boundary rules

- Public clients call the gateway or public service entrypoint, not trusted backend-only routes.
- Do not require public clients to send trusted headers such as `X-Internal-Service`, backend `X-User-Id`, or internal `X-Access` unless current public contract truth proves it.
- If direct local backend testing needs trusted headers, label that as backend-only local testing, not public SDK input.
- Keep gateway/cookie/rate-limit/session uncertainty explicit when the repo does not prove it.
- Preserve public `project_id` UUIDv7 expectations and keep internal numeric tenant/project keys out of public examples.

## Deliverables

Follow the user-requested tree or the existing repository convention. When no convention exists, include the smallest useful set:

- contract overview and route inventory
- authentication and boundary notes
- endpoint groups with request, response, error, and example payloads
- schema/type notes for SDK generation
- OpenAPI YAML and Postman collection/environment when requested or already present
- validation and drift-check notes

## Validation

Use the smallest meaningful proof available:

- JSON parse for Postman/environment artifacts
- YAML parse for OpenAPI artifacts
- `php artisan route:list` or repo-native route inventory
- public API audit commands when present
- targeted public API tests when the task allows tests
- `git diff --check`

If validation is blocked, record the exact command and blocker instead of implying success.

## Companion routing

- `$alaa-workflow` for multi-file contract packs, automation runs, or durable handoff.
- `$alaa-php-clean-code` and `$alaa-laravel-architecture` when the user expands scope from docs to Laravel code.
- `$alaa-services-contract` for cross-service response envelopes, health/readiness, observability, and shared Ala conventions.
- `$alaa-trust-gateway-auth` for trusted header, gateway, JWT, project, and permission-boundary decisions.
- `$alaa-postman-collections` for collection/environment generation or parity fixes.
