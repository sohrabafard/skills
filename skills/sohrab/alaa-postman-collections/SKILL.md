---
name: alaa-postman-collections
description: "Create, update, synchronize, and validate Postman Collection v2.1 collections and environments so every request carries saved examples for its success case and for every error it can actually return, a post-response script that captures tokens and ids into the variables later requests consume, tests that would fail against a broken implementation, and documentation a frontend developer and a security tester can both work from — while the artifact stays importable into Insomnia. Use for Postman collections, environments, examples, scripts, tests, request documentation, mock servers, Insomnia portability, and proving a collection matches the repository's public API contract. Do not use for generic docs work with no Postman ownership, or to decide what a public contract says: on a Laravel service that is /alaa-laravel-public-api-contract-pack ($alaa-laravel-public-api-contract-pack)."
---

# Alaa Postman Collections

## Purpose

Use this skill when Postman artifacts are a primary deliverable or must stay synchronized
with a public HTTP API contract. It is Postman-first, schema-aware, and
repository-truth-first, and it produces Collection Format v2.1 collections and environment
files that stay importable into Insomnia. It owns the Postman projection of a public API and
proves that projection matches the canonical contract; it does not decide what the contract
says. `references/25-public-api-contract-and-sdk-readiness.md` names the owner per case.

## When to use

- create or update Postman collections or environments
- sync Postman artifacts with routes, controllers, validators, serializers, tests, or
  OpenAPI files
- add or repair examples, scripts, tests, request documentation, variables, or auth
- set up a mock server, or judge whether one is worth defining
- validate collection JSON, variable references, secret safety, or Insomnia portability
- prove a collection covers every operation the repository's public contract declares

## When NOT to use

- generic README or docs work with no Postman ownership
- pure API design work before repository truth exists
- runtime secret-management design outside committed Postman artifacts
- Insomnia-native workspace modeling with no Postman export requirement
- deciding a Laravel service's contract, versioning, or deprecation policy

## What complete means

A list of requests is not a collection. Seven properties make it one. Read only the owning
files the current task touches.

1. **Response contract.** An example per success status and per error the route can return.
   → `references/41-response-contract-and-error-coverage.md`
2. **Scripts that carry state.** Nothing copied by hand, every capture behind a guard.
   → `references/42-scripts-and-state-capture.md`, `assets/token-capture-post-response.js`
3. **Tests on every response.** Status, envelope, content type, correlation header, subject.
   → `references/43-response-tests.md`, `assets/response-tests-post-response.js`
4. **Documentation per request.** Eight headings a frontend developer and a security tester
   can both work from without opening the backend repository.
   → `references/44-request-documentation-blocks.md`, `assets/request-documentation-block.md`
5. **Mock servers.** Only when one is worth defining, driven by the examples that exist.
   → `references/45-mock-servers.md`
6. **Environment completeness.** Every variable declared, every secret typed and
   placeholdered, no committed value that is really a generator's constant.
   → `references/30-variables-auth-and-environments.md`
7. **Insomnia compatibility.** Only constructs the Insomnia import path preserves.
   → `references/50-insomnia-compatibility-and-free-plan-rules.md`

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Identify the public API boundary, who owns the canonical contract, and any existing
   Postman or Insomnia artifacts before editing.
3. Read `references/00-topic-map.md` to pick the smallest set of reference files, and read
   `references/25-public-api-contract-and-sdk-readiness.md` when the repo owns a public API.
4. Follow the ordered workflow in `references/10-scope-and-trigger-rules.md`, which also
   holds the generated-artifact rule and the stop-and-ask conditions.
5. Prefer a minimal update to an existing artifact over a rewrite.
6. Validate before concluding. `references/60-validation-and-output-contract.md` holds both
   scripts' flags, all three exit-code tables, and what each failure obliges you to do.

## Deliverables

- a Collection Format v2.1 JSON artifact meeting all seven properties above
- one or more environment JSON artifacts when the repo needs them
- parity evidence against the canonical public contract when the repo owns a public API
- validation notes naming the exact commands, exit codes, and every contract,
  implementation, or portability gap

## Other references

- ownership, the ordered workflow, source-of-truth order, stop rules:
  `references/10-scope-and-trigger-rules.md`
- public-contract parity and SDK readiness:
  `references/25-public-api-contract-and-sdk-readiness.md`
- aggregate collections, and a repository holding its own copy of a script from here:
  `references/70-aggregate-collections-and-consumer-repos.md`
- official-first source map and freshness triggers: `references/90-source-map.md`

## Companion routing

Skills are named bare below. Trigger the ones you need with the prefix your runtime uses:
`/name` in Claude Code, `$name` in Codex; this skill is `/alaa-postman-collections` and
`$alaa-postman-collections`.

- response envelopes, error codes, and required response headers: `alaa-services-contract`
- what a Laravel service's public contract says, and its versioning, deprecation, and route
  inventory: `alaa-laravel-public-api-contract-pack` owns those; this skill proves the
  collection matches them
- test design, and what makes an assertion defend against a broken implementation:
  `alaa-testing-strategy`
- the complexity bound a check or a generated collection holds as it grows:
  `alaa-algorithms-data-structures`
- Laravel route, controller, request, resource, or DTO code: `alaa-laravel-architecture`
- PHP naming, consistency, or contract cleanup: `alaa-php-clean-code`
- gateway, tenant, or trust-header auth behaviour: `alaa-trust-gateway-auth`
- security-sensitive auth or authorization ambiguity: `alaa-security-review`
- repository documentation, including `<repo>/README.md`, `<repo>/docs/BIG_PICTURE.md`,
  `<repo>/docs/api-summary.md`, and `<repo>/remaining-task.md`: `alaa-repo-docs` owns
  those; this skill owns documentation inside the Postman artifact
- model or reasoning-effort choice: route it to `alaa-prompting-guide`; this skill pins no
  model

## Maintenance rules

- Keep this file routing-first. Operational rules belong in `references/`; fill-in
  templates belong in `assets/`. State every rule in exactly one file.
- New mechanical rules go into `scripts/validate_postman_artifacts.py`, not into
  `scripts/audit_collection_contract.py`, because a consumer repository holds a
  byte-identical copy of the auditor that cannot be updated from here.
- Every assertion either script ships carries a fixture in `test/fixtures/` that violates it.
  `scripts/selftest.py` runs them under `--self-test`; a rule with no red fixture is decoration.
- Refresh version-sensitive rules when official Postman, Insomnia, JSON Schema, or
  API-provider behaviour changes, and carry the verification date with the claim.
- Treat Insomnia compatibility as a validation target, not an assumption.
