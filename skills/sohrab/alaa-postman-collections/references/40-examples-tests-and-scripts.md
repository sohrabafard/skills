# Examples Tests And Scripts

## Examples and saved responses

Use saved responses as attached examples on the real request item.

Good examples:

- a representative success response for each important operation
- a representative validation error when request shape matters
- a representative auth error when auth handling is part of onboarding
- a representative pagination or filtering response when list behavior matters

Rules:

- keep example names meaningful
- keep bodies coherent with the current serializer or response resource
- keep examples small enough to review comfortably
- remove stale or impossible examples when the repo proves they are wrong
- remember that saved examples also feed Postman collection documentation; keep them concise, representative, and contract-focused
- map each meaningful public request and response branch to the canonical public contract; do not leave branch-defining examples only in Postman
- keep example identifiers, formats, enums, status codes, headers, and envelopes consistent across OpenAPI or the repo's equivalent contract and saved Postman responses

For SDK-ready public APIs, representative does not mean happy-path-only. Add source-backed examples for materially different branches such as discriminated request variants, alternate success statuses, idempotent replay, queued work, empty results, pagination, validation, authorization, conflict, rate limiting, and dependency failure when those behaviors exist.

## Test-writing rules

Use `pm.test` for contract-critical checks, not for noisy trivia.

Prefer tests such as:

- expected status code
- content type or key headers
- top-level JSON shape
- presence or type of critical fields
- auth failure behavior when relevant
- pagination fields when relevant
- idempotency-critical headers or fields when relevant

Avoid brittle tests that snapshot whole responses unless the repo already treats exact payloads as the contract.

## Script placement

Use the narrowest shared scope that keeps behavior understandable:

- collection-level scripts for shared setup or shared response assertions
- folder-level scripts for bounded-context logic
- request-level scripts only for request-specific needs

Keep scripts short, readable, and diff-friendly. The official v2.1 schema allows script `exec` content as an array of lines, which is the most reviewable format. Prefer that layout when writing or normalizing scripts.

The executable request-script location is the request item's top-level `event` array. Never place scripts inside `request.event`; that field is outside the v2.1 request schema and clients may display the JSON while silently never executing the script.

## Response-to-variable capture contract

Treat workflow correlation as part of the collection contract:

- identify every token, cookie, public id, operation id/hash, cursor, upload URL/offset, or other response value used by a later request
- add a success-guarded item-level post-response script that saves each dependency automatically
- update rotated values such as access and refresh tokens on every successful rotation
- extract cookies from response cookies or `Set-Cookie` without logging or committing their values
- write to the exported environment with modern `pm.environment.*`; use `pm.collectionVariables.*` only as a documented portable fallback when useful
- validate the proven response envelope and fail with a clear test message when a required dependency is absent instead of silently leaving a stale value
- never overwrite a working variable from an intentional error response
- correlation-only values such as `last_request_id`, `last_traceparent`, and their aggregate-namespaced forms (for example `tusd_last_request_id`) may be captured on error responses because they are needed for investigation
- document the saved variable name and the requests that consume it

Run a dependency audit after editing: for each variable used in a later URL, header, query, or body, prove whether it is user/environment input or is populated by an earlier executable script.

Postman v2.1 executes request-specific scripts from the request item's `event` array. Never place executable scripts under `request.event`; that location may survive JSON generation but is not the item event scope used by Postman or compatible importers. Validators and merge generators should reject or explicitly promote this legacy shape.

## Script lifecycle and runner features

Current Postman scripts can be placed at collection, folder, or request scope.

- Collection-level post-response scripts run for requests in the collection.
- Folder-level post-response scripts run for direct child requests in that folder.
- Request-level scripts should hold request-specific assertions or response-to-variable saves.
- Use pre-request scripts for setup such as dynamic headers, generated values, or request skipping.
- Use post-response scripts for assertions, saved IDs, and response-shape checks.

## Response-to-variable capture contract

When a later request depends on a value returned by an earlier response:

- capture it automatically in the producing request's item-level post-response script
- save to an environment or collection variable that is declared in the committed artifacts
- update only after the expected success status and a valid response shape
- tolerate documented response wrappers or compatibility aliases only when verified from source
- capture tokens, cookies, IDs, cursors, hashes, and upload locations needed by the documented workflow
- avoid hard-coded fixture identifiers in dependent requests when a producing request can supply the real value
- document any contract gap that makes automatic capture impossible instead of inventing a field or route

Runner workflow APIs are powerful but should stay optional:

- `pm.execution.setNextRequest()` changes order only in collection runs, not a normal Send action.
- `pm.execution.skipRequest()` works from pre-request scripts and also affects Collection Runner, Flows, and Postman CLI behavior.
- `pm.execution.runRequest()` can call referenced collection requests, but Postman documents a per-script call limit; avoid making core correctness depend on it.
- Prefer normal collection order and simple saved variables before adding runner-control logic.

Package-library scripts can reduce duplication in Postman workspaces, but they are not a file-portability baseline. Keep committed artifacts self-contained unless the repo also commits the script source and validation path.

## Portability rules for scripts

Write for the Postman sandbox, but avoid unnecessary Postman-only sprawl:

- prefer simple `pm.*` usage
- keep shared helpers explicit and near the requests that use them
- avoid hidden state in globals
- avoid network-calling helper scripts unless the collection truly depends on them
- use short comments only where they materially improve maintainability

Official Insomnia docs state that Postman v2.0 and v2.1 scripts should work when imported, but deprecated Postman interfaces are not supported. Because of that:

- avoid deprecated `postman.*` script APIs
- prefer modern `pm.environment`, `pm.collectionVariables`, `pm.variables`, and `pm.test`
- avoid features whose meaning disappears outside Postman
- be cautious with `pm.execution.*`, package-library imports, Visualizer, Flows, and helper requests when Insomnia portability is a hard requirement

k6 conversion can preserve explicit requests, variables, headers, bodies, and checks, but Postman sandbox correlation must not be the only documentation of a workflow. Keep saved request/response examples and variable dependency notes complete, run a Postman-to-k6 conversion check when k6 is a target, and review the generated script's URLs, auth, bodies, correlation, checks, and environment mapping before claiming k6 readiness.

## Optional advanced features

You may use advanced Postman features only when they add clear value and remain optional:

- Visualizer
- collection or folder helper scripts
- workflow helper requests
- Collection Runner order control
- Postman Package Library scripts
- generated dynamic values

Do not make correctness depend on:

- Visualizer output
- published cloud docs
- monitors
- paid branding or team workspace features
- package-library scripts that are not exported with the collection
- runner data that is not committed as a safe local fixture
