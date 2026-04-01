# Laravel Service Rules

Apply this file only when the target service is Laravel-based.

## Core rule

For Laravel APIs, treat Resources as the public success-response contract.

- Use Laravel Resources for successful JSON HTTP responses.
- Let services return domain data or small DTOs instead of transport-shaped arrays.
- Let controllers own HTTP status codes and response serialization through `JsonResource` or `ResourceCollection`.
- Keep business logic separate from transport concerns.
- Make the Resource the single place that defines what the client is allowed to see.

## Default behavior

- Preserve existing success envelopes unless the contract is intentionally changed.
- Keep error responses aligned with the current service convention by default.
- Inspect existing repository patterns before changing response serialization.
- Use Laravel Boost `search-docs` first for version-specific Resource guidance.
- Keep docs, examples, and Postman artifacts aligned with the shipped Resource shape when the contract changes.

## Boundary rules

- Do not return `JsonResponse` payload arrays from services.
- Do not let controllers leak raw models, persistence-only attributes, or temporary implementation fields.
- Use DTOs when a stable typed boundary is helpful between service and controller layers.
- Keep Resources focused on transport-safe serialization, not domain behavior.
- Keep controllers thin and deterministic.

## Why this rule exists

This pattern:
- keeps response shapes consistent across endpoints
- makes tests simpler because assertions target a centralized transport shape
- makes docs and Postman easier to synchronize
- prevents accidental leakage of internal IDs, persistence details, or backend-only fields
- makes contract review safer because the success shape is centralized instead of scattered

## Auth reference precedent

The auth repository commit `40d7e6e` is the approved reference precedent for this rule.

That precedent established:
- Resource-first success responses for `/api/*`
- service/domain DTOs under the controller boundary
- controller-owned HTTP status codes and serialization
- preservation of current error conventions
- removal of backend-only public leakage such as `access_token_id`

## Companion skills

- `$alaa-workflow`
  Read when adoption is non-trivial, multi-file, or behavior-changing.
- `$alaa-laravel-architecture`
  Read when controller, service, request, resource, or DTO boundaries change.
- `$alaa-php-clean-code`
  Read when implementing PHP or Laravel code changes.
