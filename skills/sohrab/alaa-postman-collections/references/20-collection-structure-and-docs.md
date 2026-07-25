# Collection Structure

Read this file when creating a collection, or when deciding how to group requests.

Request documentation is owned by `44-request-documentation-blocks.md`. Saved examples
are owned by `41-response-contract-and-error-coverage.md`. Scripts and tests are owned
by `42-scripts-and-state-capture.md` and `43-response-tests.md`.

## Target format

- Postman Collection Format v2.1 JSON.
- `info` is complete: `name`, `description`, and `schema`.
- `info.schema` is exactly
  `https://schema.getpostman.com/json/collection/v2.1.0/collection.json`.
  `50-insomnia-compatibility-and-free-plan-rules.md` gives the string comparison this
  satisfies and the failure it prevents.
- Preserve an existing `_postman_id`. The official schema recommends keeping the same ID
  for an existing collection, and changing it makes every diff look like a new artifact.

## Core shape

The v2.1 schema centres a collection on `info`, `item`, and optional top-level `event`,
`variable`, and `auth`.

A request item carries one `request`, zero or more attached `response` objects, and
item-level `event`, `variable`, or `description` when needed. Nothing executable belongs
inside `request` itself.

## Structural rules

- One request item per operation.
- Use a folder when it improves bounded-context grouping, auth grouping, or
  reviewability. Use a flat collection when the surface is small and obvious.
- Keep folder depth at two levels. A third level hides requests from the person
  scanning the sidebar.
- Order requests inside a folder so a plain top-to-bottom run works: the request that
  produces a value comes before the requests that consume it.
- Name requests predictably and in one tense: `List Orders`, `Create Order`, `Get Order`.
  No slang, no mixed tense, no internal codename.

## Where a shared fact lives

- **collection description**: the environment contract, the base URL and prefix model,
  the auth model at the boundary, pagination and tenancy conventions, and the short list
  of values a developer must supply before the first request works
- **folder description**: what is true for that context — its shared headers, its shared
  auth, its shared error behaviour
- **request description**: the eight blocks from
  `assets/request-documentation-block.md`

State a fact at one level only. `44-request-documentation-blocks.md` owns the rule for
what a request description must still answer for itself.

## Public-contract coupling

When the repository owns a public HTTP API, the collection and the canonical contract are
two projections of one verified behaviour. Keep operation names, public paths, auth,
parameters, schemas, statuses, error codes, and examples aligned across both, and patch
the generator inputs first when either is generated.
`25-public-api-contract-and-sdk-readiness.md` owns the completeness criteria.

## Parameter and body rules

- Document only fields the code or a verified contract supports.
- Keep request body examples aligned with the current validator and serializer, not with
  older documentation.
- Where API behaviour is non-obvious, the constraint belongs in the request's `## Request`
  block rather than in a comment inside the body.
