# Scope And Trigger Rules

Use this file before editing anything.

## Skill ownership

This skill owns:

- Postman collection JSON artifacts
- Postman environment JSON artifacts
- request descriptions inside Postman collections
- Postman examples, saved responses, scripts, tests, variables, and auth inheritance
- portability notes and validation notes for Postman-to-Insomnia import

This skill does not own:

- broad README or runbook updates
- API behavior design that is not yet implemented
- live secret management outside committed artifacts
- Insomnia-native workspace modeling that has no Postman export requirement

## Strong triggers

Use this skill when the request includes work such as:

- "create or update the Postman collection"
- "sync Postman with the current API"
- "generate environments"
- "add examples or tests to the collection"
- "make it import cleanly into Insomnia"
- "validate the Postman artifact"

## Source-of-truth order

Use this order unless the repo proves a stronger contract source:

1. routes, controllers, handlers, DTOs, validators, serializers, resources, and contract tests
2. request tests, integration tests, and runtime examples checked into the repo
3. verified OpenAPI files or other checked-in machine-readable contracts
4. existing Postman artifacts
5. README and prose docs

If code and docs disagree, trust code and verified contracts over stale prose.

## Discovery checklist

Inspect the smallest relevant set of sources:

- routes or transport definitions
- controllers, handlers, or service entrypoints
- request validators and response serializers
- DTOs, resources, and schema classes
- request tests, contract tests, or fixtures
- OpenAPI files when present
- README, docs, and example cURL blocks
- existing `*.postman_collection.json`, `*.postman_environment.json`, or Insomnia exports

## Hard constraints

- Never invent endpoints, methods, parameters, fields, auth flows, or error cases.
- Never commit real secrets.
- Never treat guessed examples as verified facts.
- Never rewrite a collection from scratch without checking whether a minimal update is safer.
- Never make correctness depend on Postman Vault, cloud publishing, monitors, or paid-only features.
- Keep all prose, comments, request descriptions, and example names in simple English.

## Update-vs-create rule

- If a Postman collection already exists, inspect it first and update it minimally when safe.
- Preserve stable collection and request IDs when they already exist and still map to the same operations.
- Remove stale examples, headers, variables, or scripts only when the repo clearly proves they are wrong.
- Create new artifacts only when none exist or the current files are beyond safe repair.

## Stop and ask

Stop and ask when any of the following would force risky guessing:

- code, tests, and docs disagree on request or response shape
- auth behavior is unclear and the ambiguity has security impact
- missing environment details would materially change collection structure or auth modeling
- critical example values cannot be inferred safely without inventing business data
- multiple competing collections exist and the canonical artifact is unclear
