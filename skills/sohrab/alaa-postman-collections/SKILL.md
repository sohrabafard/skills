---
name: alaa-postman-collections
description: "Use this skill when the task involves Postman collection or environment generation, update, synchronization, validation, examples, tests, scripts, or request documentation, especially when the artifacts must stay importable in the free version of Insomnia. Do not use it for generic docs work with no Postman ownership."
---




# Alaa Postman Collections

## Purpose

Use this skill when Postman artifacts are the primary deliverable.

This skill is Postman-first, schema-aware, and repository-truth-first. It creates or updates Postman Collection Format v2.1 collections and companion environment files while keeping the artifacts portable to the free version of Insomnia.

## When to use

- create or update Postman collections
- create or update Postman environments
- sync Postman artifacts with routes, controllers, validators, serializers, tests, or OpenAPI files
- repair stale request descriptions, examples, tests, variables, or auth inheritance
- validate collection JSON, variable references, or Insomnia import portability

## When NOT to use

- generic README or docs work with no Postman ownership
- pure API design work before repository truth exists
- runtime secret-management design outside committed Postman artifacts
- Insomnia-only workspace design when Postman export is not part of the task

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Inspect the repository truth and any existing Postman or Insomnia artifacts before editing.
3. Read `references/00-topic-map.md`.
4. Load only the smallest reference files needed for the current repo and task.
5. Prefer minimal updates to existing artifacts over full rewrites.
6. Validate before concluding.

## Deliverables

- a Postman Collection Format v2.1 JSON artifact
- one or more environment JSON artifacts when the repo needs them
- request descriptions, examples, tests, scripts, variables, and auth inheritance that match the current implementation
- concise validation notes with any explicit portability gaps

## Minimal deterministic workflow

1. Discover API truth from code, contracts, tests, and runtime examples.
2. Inspect existing Postman collections and environments for stable IDs, structure, variables, and auth layout.
3. Choose the smallest fitting collection structure, variable model, and auth inheritance plan.
4. Create or update the collection and environment artifacts with minimal, reviewable diffs.
5. Validate schema, variables, scripts, examples, and Insomnia portability before closing.

## Companion routing

- Laravel route, controller, request, resource, or DTO contract work:
  - pair with `$alaa-laravel-architecture`
- PHP naming, consistency, or contract cleanup:
  - pair with `$alaa-php-clean-code`
- gateway, tenant, or trust-header auth behavior:
  - pair with `$alaa-trust-gateway-auth`
- security-sensitive auth or authorization ambiguity:
  - pair with `$alaa-security-review`
- broader README, runbook, or docs-page updates:
  - pair with `$alaa-docs-farsi`

## Reference navigation

- fast routing and smallest-file selection:
  - `references/00-topic-map.md`
- ownership boundaries, source-of-truth order, and stop rules:
  - `references/10-scope-and-trigger-rules.md`
- collection structure, naming, descriptions, and response attachment rules:
  - `references/20-collection-structure-and-docs.md`
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
