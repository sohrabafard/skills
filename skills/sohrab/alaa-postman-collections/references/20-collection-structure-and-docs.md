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
- request-level `event`, `variable`, or `description` only when needed

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

Prefer plain Markdown that reads well in Postman-generated docs:

- short paragraphs
- short bullet lists
- inline code for variable names, headers, and field names

Do not add decorative Markdown or huge walls of prose.

## Parameter and body notes

- Document only fields the code or verified contract actually supports.
- Add brief notes for required parameters, optional filters, enum values, or mutually exclusive fields when the API behavior is non-obvious.
- Keep request body examples aligned with validators and serializers, not with stale docs.

## Response attachment rules

The v2.1 schema allows multiple responses on the same item. Use that shape directly:

- attach representative success responses to the real request item
- attach important error responses to the same request item when they add value
- avoid duplicating the entire request just to show basic success and error variants

When a saved response is present, keep it coherent:

- the response should match the current route and method
- `originalRequest` should reflect the real request
- status code, headers, and body should match the contract closely enough to be useful

## Documentation-quality rules

- Write in simple, fluent English for engineers and non-engineers alike.
- Explain auth expectations, tenant headers, pagination, filtering, idempotency, and business constraints when they materially affect request usage.
- Keep descriptions reviewable. If a request description becomes long, split shared guidance upward to the folder or collection level.
