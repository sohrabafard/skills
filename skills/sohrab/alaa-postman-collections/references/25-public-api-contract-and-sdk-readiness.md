# Public API Contract And SDK Readiness

Read this file whenever the repository owns a public HTTP API. Public-contract synchronization is mandatory for this skill, even when the user's immediate wording mentions only Postman.

## Outcome

Leave one canonical, machine-readable public API contract and the Postman artifacts synchronized to the same verified external behavior.

Done means another agent can build an SDK without opening service implementation files or guessing:

- externally reachable operations and base paths
- authentication and trusted-context boundaries
- request types and validation rules
- response types for every meaningful status and branch
- normalized errors and retry behavior
- pagination, idempotency, caching, concurrency, and rate-limit semantics
- asynchronous workflows and state transitions
- safe, source-backed examples

OpenAPI 3.1 is preferred when the repository has no stronger canonical format. Preserve an existing canonical format or generator when the repo already owns one.

Prefer the repository's existing contract location. If the repo clearly owns public routes but has no contract convention, create the smallest explicit pack at `docs/contracts/<service>/openapi.yaml` with colocated `examples/` only when external example files add value. In a monorepo, keep the pack under the owning service's documented contract area. Link it from an existing API/docs index when one exists; do not introduce a competing documentation root.

## Boundary and ownership discovery

Before editing:

1. Read the repo-local instructions.
2. Identify the service-local routes and the externally reachable gateway or ingress paths.
3. Identify the canonical contract and whether it is source-authored or generated.
4. Identify contract consumers: frontend, SDK, gateway, tests, Postman, Insomnia, or k6.
5. Identify auth, tenancy/project, error-normalization, and trusted-header owners.

Do not publish service-local diagnostics, internal worker APIs, health routes, metrics, queues, or trusted headers as public SDK operations unless the repository explicitly defines them as public.

If the repository exposes no public HTTP API, state that evidence and keep this reference out of the deliverable. If public ownership is unclear or competing contracts disagree materially, stop and ask instead of inventing a boundary.

## Source-of-truth order

Use the strongest repository-specific source. A common order is:

1. canonical IDL/OpenAPI source or contract generator declared by repo instructions
2. public gateway/ingress route and cross-service contract
3. router plus handlers/controllers, validators, DTOs, serializers, and resources
4. contract, integration, and request tests
5. checked-in runtime fixtures and verified examples
6. existing public contract and Postman artifacts
7. prose documentation

Generated files are evidence, not the editable source. Patch the owning generator or inputs, regenerate, and review the diff.

When sources disagree, record the exact drift. Continue only with the safest verified behavior; never silently choose a convenient shape or preserve stale behavior as canonical.

## Route-and-variant coverage matrix

Build a compact working matrix before editing. Keep it temporary unless the repo already stores such a manifest.

For every public operation, track:

- public method and path, operation identifier, and purpose
- auth mode, scopes/permissions, and caller-visible headers
- path, query, header, cookie, and body inputs
- request variants and discriminators
- success statuses and response variants
- error statuses, stable error codes, and retryability
- pagination, filtering, sorting, expansion, and field-selection behavior
- idempotency, concurrency, caching, and rate-limit behavior
- async acceptance, polling/callback/result flow, and terminal states
- source evidence and matching Postman item/examples

Use the matrix to detect missing routes, branches, schemas, examples, or Postman responses. Do not confuse one example per route with complete variant coverage.

## Request completeness

For each operation, make the canonical contract explicit about:

- exact public path, HTTP method, content types, and operation ID
- required versus optional versus nullable fields
- object closure rules such as `additionalProperties`
- formats and bounds: UUID variant, integer width, decimal precision, timestamp/timezone, string length, array size, and numeric range
- enums, constants, defaults, deprecations, and compatibility aliases
- mutually exclusive, dependent, conditional, or discriminated fields
- nested object variants and polymorphic principals, objects, reasons, commands, or filters
- public identifiers versus internal identifiers
- header/query/body precedence and trusted values that clients must not send
- safe examples for every materially different request variant

Examples do not replace schemas. Schemas do not replace examples.

## Response completeness

Document every caller-relevant outcome, not only the most common `200` response:

- all success statuses, including `201`, `202`, `204`, replay, existing-resource, and partial-result behavior
- synchronous versus queued/accepted branches
- populated versus empty collection responses
- pagination envelopes, cursors, totals, and continuation rules
- headers clients must read, such as location, retry, idempotency, ETag, request ID, or rate-limit headers
- lifecycle state, timestamps, version/revision, and next-action links or identifiers
- state enums, legal transitions, terminal states, and invalid-transition errors
- stable error envelope, error-code catalog, field violations, retryability, and dependency failures
- response variants selected by request discriminator, state, or status
- source-backed examples for every materially different response branch

When a queued operation has no public polling, callback, or result endpoint, document that gap explicitly. Do not imply a completion workflow that does not exist.

## Cross-cutting SDK semantics

Make these rules explicit when applicable:

- base URL and gateway prefix versus service-local URL
- bearer, API key, cookie, mTLS, or other auth behavior
- CORS and browser credential requirements
- tenant/project isolation and forbidden client-supplied trusted headers
- idempotency-key generation, scope, retention, replay, and conflict behavior
- safe retry matrix by method/status/error code
- rate-limit status and headers
- cacheability, invalidation, ETag, and client memoization guidance
- pagination and cursor opacity
- optimistic concurrency and preconditions
- date/time, binary/upload, decimal, and lossless `int64` representation
- backward compatibility, versioning, deprecation, and unknown-enum handling
- correlation/request IDs and safe logging/PII rules

Do not hide these semantics only in prose when the contract format can model them. Use prose extensions or companion pages only for rules the machine-readable format cannot express clearly.

## Example coverage

Keep examples deterministic, safe, internally coherent, and portable. Use public-looking placeholders, never real secrets or production data.

Cover every meaningful branch that exists, including as applicable:

- each discriminated request type
- minimum and maximum useful optional-field combinations
- each success response shape/status
- create versus idempotent replay or already-existing result
- synchronous versus asynchronous acceptance
- populated, empty, and paginated results
- validation, unauthenticated, forbidden, not-found, conflict, rate-limit, and dependency errors
- lifecycle transitions such as create, replace/update, revoke/delete, restore, or reconcile

Keep the same example semantics across the canonical contract, Postman saved responses, and standalone JSON/HTTP fixtures. A value changed in one projection must be reconciled in the others.

## SDK-readiness test

Before closing, answer yes with repository evidence to each question:

1. Can an SDK agent enumerate every public operation without inspecting routing code?
2. Can it generate lossless input and output types without inspecting DTOs or serializers?
3. Can it implement every meaningful success and error branch without guessing statuses or envelopes?
4. Can it implement auth, pagination, retries, idempotency, caching, rate limits, and async workflows safely?
5. Can it find at least one coherent example for every meaningful request and response variant?
6. Do Postman operations, schemas, statuses, errors, and examples match the canonical contract?
7. Are all known implementation, gateway, or contract gaps explicit rather than implied as working behavior?

Any `no` is remaining work or an explicit blocker. Do not label the API contract SDK-ready until all applicable answers are `yes`.

## Validation evidence

Prefer repository-native checks, then add the smallest missing deterministic validation:

- validate OpenAPI/IDL syntax and internal references
- compare router or route-manifest operations with public contract operations
- validate every JSON example against its declared schema when practical
- verify discriminator mappings and all referenced schemas
- compare statuses, error codes, headers, and examples with Postman saved responses
- regenerate derived contracts/collections and require a stable second run
- run contract tests or generate a client as a smoke test when the repo supports it
- validate Markdown links and example JSON files
- run `git diff --check`

Report exact commands, counts, and any skipped validation. A parser pass alone does not prove route or variant completeness.

## Stop conditions

Do not close while any of these remain unreported or unresolved:

- a public route is missing from either the canonical contract or Postman collection
- a meaningful request/response/error branch exists only in code or tests
- examples contradict schemas or use internal IDs at a public boundary
- public and service-local paths are conflated
- auth or trusted-header ownership is ambiguous
- generated artifacts were hand-edited without updating their source
- an SDK must guess a status, field, format, error, retry, pagination, or workflow rule
