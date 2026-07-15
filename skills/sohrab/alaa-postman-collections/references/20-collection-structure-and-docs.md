# Collection Structure And Docs

## Target format

- Produce Postman Collection Format v2.1 JSON.
- Keep the collection `info` block complete and set `info.schema` to the v2.1 schema URL.
- Preserve an existing `_postman_id` when the collection already has one. The official schema notes that maintaining the same ID is recommended for an existing collection.
- Set `info.schema` to the Postman export/import marker `https://schema.getpostman.com/json/collection/v2.1.0/collection.json`. Do not use the schema-host draft URL as the collection marker; it can validate JSON but may make Insomnia report `No importers found for file`.

## Core shape

The official v2.1 schema centers the collection around:

- `info`
- `item`
- optional top-level `event`
- optional top-level `variable`
- optional top-level `auth`

Each request item may carry:

- one `request`
- zero or more attached `response` objects
- item-level `event`, `variable`, or `description` only when needed

## Structural rules

- Keep one request item per operation whenever possible.
- Use folders only when they improve bounded-context grouping, auth grouping, or reviewability.
- Prefer a flat collection when the API surface is small and obvious.
- Keep folder depth shallow. Two levels is usually enough.
- Use predictable naming such as `List Orders`, `Create Order`, `Get Order`, not slang or mixed tense.

## Description rules

Use descriptions at the smallest useful level:

- collection description for overall auth, environment expectations, paging rules, tenancy, and shared conventions
- folder description for bounded-context rules, shared headers, or shared auth details
- request description for request-specific behavior, parameter notes, body expectations, idempotency, pagination, filtering, and important error behavior

For frontend implementation or penetration-test handoff, each request description should also state the verified auth mode, important headers, variable dependencies, success behavior, material error behavior, and any sequencing or state transition the caller must understand. Do not leave this knowledge only in scripts or saved examples.

Prefer plain Markdown that reads well in Postman-generated docs:

- short paragraphs
- short bullet lists
- inline code for variable names, headers, and field names

Do not add decorative Markdown or huge walls of prose.

When the collection is a frontend implementation or penetration-test handoff, every request description must be self-contained enough to use without opening the backend repository. Cover, when applicable:

- purpose and user/business outcome
- public versus service-local path shape
- auth and trusted-context boundary
- prerequisites and workflow dependencies
- path, query, header, and body constraints, including enums and bounds
- success response semantics and any values saved for later requests
- important validation, auth, permission, conflict, rate-limit, and dependency errors
- idempotency, retry, caching, pagination, and side-effect cautions
- security tests such as tenant/project isolation, spoofed trusted headers, IDOR/BOLA, and replay

Move shared rules to folder or collection descriptions, but do not use shared prose as an excuse to leave request-specific behavior undocumented.

## Public-contract coupling

When the repository owns a public HTTP API, treat Postman descriptions and saved responses as readable projections of the canonical public contract, not as a substitute for it.

- keep operation names, public paths, auth, parameters, schemas, statuses, error codes, and examples aligned across both artifacts
- update generator inputs first when either artifact is generated
- attach examples for every meaningful branch identified by the route-and-variant coverage matrix
- preserve contract-important distinctions such as synchronous versus queued responses, create versus replay, empty versus populated lists, and success versus conflict
- record implementation or gateway gaps explicitly instead of encoding a guessed behavior in only one artifact

Use `25-public-api-contract-and-sdk-readiness.md` for the mandatory SDK-completeness criteria.

## Parameter and body notes

- Document only fields the code or verified contract actually supports.
- Add brief notes for required parameters, optional filters, enum values, or mutually exclusive fields when the API behavior is non-obvious.
- Keep request body examples aligned with validators and serializers, not with stale docs.

## Response attachment rules

The v2.1 schema allows multiple responses on the same item. Use that shape directly:

- attach at least one representative success response to every real request item when the collection is intended as a self-contained API contract
- attach important error responses to the same request item when they add value
- avoid duplicating the entire request just to show basic success and error variants

When a saved response is present, keep it coherent:

- the response should match the current route and method
- `originalRequest` should reflect the real request
- status code, headers, and body should match the contract closely enough to be useful

For frontend, pentest, or cross-tool handoffs, attach at least one representative success response to every real request, including bodyless `204` operations. Attach contract-important error examples when the route has validation, auth, authorization, conflict, rate-limit, or dependency behavior that callers must implement or test. Preserve raw HTTP status, headers, body, and `originalRequest` so Postman, Insomnia, and k6 conversion workflows have explicit transport examples.

## Documentation-quality rules

- Write in simple, fluent English for engineers and non-engineers alike.
- Explain auth expectations, tenant headers, pagination, filtering, idempotency, and business constraints when they materially affect request usage.
- Keep descriptions reviewable. If a request description becomes long, split shared guidance upward to the folder or collection level.
