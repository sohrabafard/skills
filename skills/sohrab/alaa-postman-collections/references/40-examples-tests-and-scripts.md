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

## Script lifecycle and runner features

Current Postman scripts can be placed at collection, folder, or request scope.

- Collection-level post-response scripts run for requests in the collection.
- Folder-level post-response scripts run for direct child requests in that folder.
- Request-level scripts should hold request-specific assertions or response-to-variable saves.
- Use pre-request scripts for setup such as dynamic headers, generated values, or request skipping.
- Use post-response scripts for assertions, saved IDs, and response-shape checks.

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
