---
name: alaa-postman-collections
description: "Create, update, synchronize, and validate Postman Collection v2.1 collections and environments so every request carries saved examples for its success case and for every error it can actually return, a post-response script that captures tokens and ids into the variables later requests consume, tests that would fail against a broken implementation, and documentation a frontend developer and a security tester can both work from — while the artifact stays importable into Insomnia. Whenever the repository owns a public HTTP API, also create or synchronize its SDK-ready public API contract with complete source-backed request, response, error, lifecycle, and example coverage. Use for Postman collections, environments, examples, scripts, tests, request documentation, mock servers, and Insomnia portability work; do not use for generic docs work with no Postman or public-API ownership."
---

# Alaa Postman Collections

## Purpose

Use this skill when Postman artifacts are a primary deliverable or must stay synchronized
with a public HTTP API contract.

It is Postman-first, SDK-contract-aware, schema-aware, and repository-truth-first. It
produces Postman Collection Format v2.1 collections and companion environment files that
stay importable into Insomnia.

When the repository owns a public HTTP API, its public contract and its Postman artifacts
are two projections of one verified behavior. Do not close the task until both are
synchronized and an SDK agent can implement transport, types, errors, pagination, retries,
and workflows from the contract without reading service code.

## When to use

- create or update Postman collections or environments
- sync Postman artifacts with routes, controllers, validators, serializers, tests, or
  OpenAPI files
- add or repair examples, scripts, tests, request documentation, variables, or auth
- set up a mock server, or judge whether one is worth defining
- validate collection JSON, variable references, secret safety, or Insomnia portability
- create or synchronize an SDK-ready public API contract while updating Postman artifacts

## When NOT to use

- generic README or docs work with no Postman ownership
- pure API design work before repository truth exists
- runtime secret-management design outside committed Postman artifacts
- Insomnia-native workspace modeling with no Postman export requirement

## What complete means

A list of requests is not a collection. Seven properties make it one. Each line names the
condition that sends you to its owning file; read only the ones the current task touches.

1. **Response contract.** Every request carries a saved example for each success status and
   for every error it can actually return, enumerated from validation rules, authorization
   gates, dependency failures, and the platform's documented code list — never guessed.
   → `references/41-response-contract-and-error-coverage.md`
2. **Scripts that carry state.** No value is ever copied by hand between two requests. A
   token request captures the token in its own post-response script and writes the variable
   the next request already references.
   → `references/42-scripts-and-state-capture.md`, `assets/token-capture-post-response.js`
3. **Tests on every response.** Status, envelope, content type, the correlation header, and
   the field the request exists to produce. A test that still passes against a plausible
   broken implementation is not a test.
   → `references/43-response-tests.md`, `assets/response-tests-post-response.js`
4. **Documentation per request.** Eight headings a frontend developer and a security tester
   can both work from without opening the backend repository.
   → `references/44-request-documentation-blocks.md`, `assets/request-documentation-block.md`
5. **Mock servers.** Only when one is worth defining, driven by the saved examples that
   already exist, with names and variables that keep it usable.
   → `references/45-mock-servers.md`
6. **Environment completeness.** Every referenced variable declared, every secret typed as
   a secret and carrying a placeholder, and a stated split between per-developer and shared
   values.
   → `references/30-variables-auth-and-environments.md`
7. **Insomnia compatibility.** The output stays a valid Postman v2.1 collection and carries
   only constructs the Insomnia path preserves.
   → `references/50-insomnia-compatibility-and-free-plan-rules.md`

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Identify the public API boundary, the canonical public contract, and any existing
   Postman or Insomnia artifacts before editing.
3. Read `references/00-topic-map.md` to pick the smallest set of reference files, and always
   read `references/25-public-api-contract-and-sdk-readiness.md` when the repo owns a public
   HTTP API.
4. If a repo script or generator owns a contract or collection, update its source inputs and
   regenerate rather than hand-editing the output.
5. Prefer a minimal update to an existing artifact over a rewrite.
6. If an existing request or docs claim describes behavior the current code does not
   implement, report the gap and route backlog wording to `alaa-docs-farsi`.
7. Validate before concluding. `references/60-validation-and-output-contract.md` holds both
   scripts' flags, both exit-code tables, and what each failure obliges you to do.

## Deliverables

- a Postman Collection Format v2.1 JSON artifact meeting all seven properties above
- one or more environment JSON artifacts when the repo needs them
- an updated canonical SDK-ready public API contract when the repo owns a public HTTP API
- validation notes naming the exact commands, exit codes, and any explicit contract,
  implementation, or portability gap

## Minimal deterministic workflow

1. Discover the public API boundary and behavior truth from gateway contracts, routes, code,
   verified contracts, tests, and runtime examples.
2. Inspect the canonical contract plus existing collections and environments for ownership,
   generators, stable IDs, structure, variables, and auth layout.
3. Build a route-and-variant coverage matrix for every public operation, including each
   error each route can return.
4. Update the canonical public contract so every meaningful request, response, error,
   lifecycle, and workflow branch is source-backed and SDK-usable.
5. Choose the smallest fitting collection structure, variable model, and auth plan.
6. When artifacts are generated, patch the generator or its inputs first, then regenerate
   and review the produced diff.
7. Create or update the collection and environment artifacts as projections of the same
   contract, with minimal reviewable diffs.
8. Audit variable dependencies: prove every `{{variable}}` is either captured by a script or
   declared operator input.
9. Validate, then report against the output contract.

## Other references

- ownership boundaries, source-of-truth order, and stop rules:
  `references/10-scope-and-trigger-rules.md`
- mandatory public-contract synchronization and SDK-readiness rules:
  `references/25-public-api-contract-and-sdk-readiness.md`
- multi-service aggregate collections, and a repository holding its own copy of a script
  from this skill: `references/70-aggregate-collections-and-consumer-repos.md`
- official-first source map and freshness triggers: `references/90-source-map.md`

## Companion routing

Skills are named bare below. Trigger the ones you need with the prefix your runtime uses:
`/name` in Claude Code, `$name` in Codex. This skill itself is `/alaa-postman-collections`
and `$alaa-postman-collections`.

- the platform's response envelopes, error codes, and required response headers:
  pair with `alaa-services-contract`
- Laravel route, controller, request, resource, or DTO contract work:
  pair with `alaa-laravel-architecture`
- PHP naming, consistency, or contract cleanup:
  pair with `alaa-php-clean-code`
- gateway, tenant, or trust-header auth behavior:
  pair with `alaa-trust-gateway-auth`
- security-sensitive auth or authorization ambiguity:
  pair with `alaa-security-review`
- broader README, runbook, or docs-page updates:
  pair with `alaa-docs-farsi`
- documented-but-not-implemented endpoints or examples:
  report the gap and let `alaa-docs-farsi` own `remaining-task.md`
- model or reasoning-effort choice for any agent doing this work:
  route the question to `alaa-prompting-guide`; this skill pins no model

## Maintenance rules

- Keep this file routing-first and compact. Detailed operational rules belong in
  `references/`; fill-in templates belong in `assets/`.
- State every rule in exactly one file and leave a pointer where it used to be.
- New mechanical rules go into `scripts/validate_postman_artifacts.py`, not into
  `scripts/audit_collection_contract.py`, because a consumer repository holds a
  byte-identical copy of the auditor that cannot be updated from here.
- Refresh version-sensitive rules when official Postman, Insomnia, JSON Schema, or
  API-provider behavior changes, and carry the verification date with the claim.
- Keep helper scripts dependency-light and safe for repo-local use.
- Treat Insomnia compatibility as a validation target, not an assumption.
