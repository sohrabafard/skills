# Source Map

Use this file when Postman artifact work depends on current schema behavior, Postman/Insomnia compatibility, or API source truth.

## Source priority

1. Target repo truth: routes, controllers/handlers, validators, DTOs, serializers/resources, OpenAPI files, tests, runtime examples, current docs, and existing Postman/Insomnia artifacts.
2. Ala companion skills for the domain: `$alaa-docs-farsi`, `$alaa-trust-gateway-auth`, `$alaa-security-review`, and framework skills.
3. Official or primary tool docs:
   - Postman Collection Format v2.1 docs: https://schema.postman.com/json/collection/v2.1.0/docs/index.html
   - Postman Collection v2.1 schema: https://schema.getpostman.com/collection/json/v2.1.0/draft-04/collection.json
   - Postman Learning Center: https://learning.postman.com/docs/
   - Insomnia docs: https://docs.insomnia.rest/
   - JSON Schema: https://json-schema.org/
4. Community posts, StackOverflow answers, import/export anecdotes, or issue comments only for troubleshooting a concrete import, schema, or script failure.

## Freshness triggers

Re-check official docs and repo truth when the task mentions:

- latest/current Postman, collection schema, environment format, test sandbox, auth inheritance, script APIs, or Insomnia import/export behavior
- stale examples, changed route paths, changed auth flow, new variables, removed endpoints, or changed response envelopes
- free-plan compatibility, collection import failures, schema validation failures, or secret-handling concerns

## Domain-bounded anti-pattern

Bad: restructuring a whole collection to match a blog's preferred folder layout while losing stable `_postman_id` values and existing examples.

Good: preserve stable IDs, update only stale requests/examples/scripts, and validate JSON, variables, schema, and Insomnia portability.
