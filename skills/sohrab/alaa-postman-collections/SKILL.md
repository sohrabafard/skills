---
name: alaa-postman-collections
description: "Create, update, synchronize, and validate Postman Collection v2.1 collections, environments, examples, scripts, tests, and request documentation with free-version Insomnia portability. Whenever the repository owns a public HTTP API, also create or synchronize its SDK-ready public API contract with complete source-backed request, response, error, lifecycle, and example coverage. Use for Postman/API-contract handoffs; do not use for generic docs work with no Postman or public-API ownership."
---




# Alaa Postman Collections

## Purpose

Use this skill when Postman artifacts are a primary deliverable or must stay synchronized with a public HTTP API contract.

This skill is Postman-first, SDK-contract-aware, schema-aware, and repository-truth-first. It creates or updates Postman Collection Format v2.1 collections and companion environment files while keeping the artifacts portable to the free version of Insomnia.

When the repository owns a public HTTP API, treat its public API contract and Postman artifacts as coupled projections of the same verified behavior. Do not close the task until both are synchronized and an SDK agent can implement transport, types, errors, pagination, retries, and workflows from the contract without reading service code or guessing.

## When to use

- create or update Postman collections
- create or update Postman environments
- sync Postman artifacts with routes, controllers, validators, serializers, tests, or OpenAPI files
- repair stale request descriptions, examples, tests, variables, or auth inheritance
- validate collection JSON, variable references, or Insomnia import portability
- create or synchronize an SDK-ready public API contract while updating Postman artifacts

## When NOT to use

- generic README or docs work with no Postman ownership
- pure API design work before repository truth exists
- runtime secret-management design outside committed Postman artifacts
- Insomnia-only workspace design when Postman export is not part of the task

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Identify the public API boundary, canonical public contract, and any existing Postman or Insomnia artifacts before editing.
3. Read `references/00-topic-map.md` and always read `references/25-public-api-contract-and-sdk-readiness.md` when the repo owns a public HTTP API.
4. If a repo script or generator owns a contract or collection, update its source inputs and regenerate the derived artifacts instead of hand-editing them.
5. Load only the smallest additional reference files needed for the current repo and task.
6. Prefer minimal updates to existing artifacts over full rewrites.
7. If an existing request or docs claim describes behavior missing from current code, report the gap and route backlog wording to `$alaa-docs-farsi`.
8. Validate contract completeness, Postman consistency, and portability before concluding.

## Deliverables

- a Postman Collection Format v2.1 JSON artifact
- one or more environment JSON artifacts when the repo needs them
- an updated canonical SDK-ready public API contract when the repo owns a public HTTP API
- request descriptions, examples, tests, scripts, variables, and auth inheritance that match the current implementation
- concise validation notes with any explicit contract, implementation, or portability gaps

## Minimal deterministic workflow

1. Discover the public API boundary and behavior truth from gateway contracts, routes, code, verified contracts, tests, and runtime examples.
2. Inspect the canonical public contract plus existing Postman collections and environments for ownership, generators, stable IDs, structure, variables, and auth layout.
3. Build a route-and-variant coverage matrix for every public operation.
4. Update the canonical public contract so every meaningful request, response, error, lifecycle, and workflow branch is source-backed and SDK-usable.
5. Choose the smallest fitting collection structure, variable model, and auth inheritance plan.
6. When artifacts are generated, patch the generator or source inputs first, then regenerate and review the produced diff.
7. Create or update the collection and environment artifacts as projections of the same contract with minimal, reviewable diffs.
8. Validate public-contract completeness, cross-artifact consistency, schemas, variables, scripts, examples, and Insomnia portability before closing.

## Companion routing

- Laravel route, controller, request, resource, or DTO contract work:
  - pair with `$alaa-laravel-architecture`
- PHP naming, consistency, or contract cleanup:
  - pair with `$alaa-php-clean-code`
- gateway, tenant, or trust-header auth behavior:
  - pair with `$alaa-trust-gateway-auth`
- cross-service public path, envelope, error, pagination, or ownership behavior:
  - pair with `$alaa-services-contract`
- security-sensitive auth or authorization ambiguity:
  - pair with `$alaa-security-review`
- broader README, runbook, or docs-page updates:
  - pair with `$alaa-docs-farsi`
- documented-but-not-implemented endpoints or examples:
  - report the gap and let `$alaa-docs-farsi` own `remaining-task.md`

## Reference navigation

- fast routing and smallest-file selection:
  - `references/00-topic-map.md`
- ownership boundaries, source-of-truth order, and stop rules:
  - `references/10-scope-and-trigger-rules.md`
- collection structure, naming, descriptions, and response attachment rules:
  - `references/20-collection-structure-and-docs.md`
- mandatory public-contract synchronization and SDK-readiness rules:
  - `references/25-public-api-contract-and-sdk-readiness.md`
- variables, auth inheritance, and environment guidance:
  - `references/30-variables-auth-and-environments.md`
- examples, scripts, and test-writing rules:
  - `references/40-examples-tests-and-scripts.md`
- free-plan and Insomnia portability constraints:
  - `references/50-insomnia-compatibility-and-free-plan-rules.md`
- validation steps and output contract:
  - `references/60-validation-and-output-contract.md`
- official-first source map and freshness triggers:
  - `references/90-source-map.md`
- repeatable local validation helper:
  - `scripts/validate_postman_artifacts.py`

## Maintenance rules

- Keep this top-level file routing-first and compact.
- Put detailed operational rules in `references/` instead of expanding this file.
- Refresh version-sensitive rules when official Postman, Insomnia, JSON Schema, or API-provider guidance changes.
- Keep helper scripts dependency-light and safe for repo-local use.
- Treat Insomnia compatibility as an explicit validation target, not an assumption.
