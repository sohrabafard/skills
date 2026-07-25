# Response Contract And Error Coverage

Read this file when attaching saved examples to a request, or when deciding which
responses a request must carry.

`25-public-api-contract-and-sdk-readiness.md` owns the canonical machine-readable
contract. This file owns the Postman projection of it: which saved examples exist on
each request item, and how the set of errors is arrived at.

## The coverage rule

Every request item carries:

- one saved example for each success status the route returns, and
- one saved example for every error the route can actually return.

"Actually return" means the error is reachable from this route's own code path. A
generic `4xx` placeholder is not coverage: it teaches a caller to branch on a status
that may never arrive and hides the one that does.

A request with no saved example is not a documented request. A request with only a
`200` example documents the happy path and leaves every failure to be discovered in
production by a frontend developer.

## How to enumerate a route's errors

Do not guess and do not copy another route's list. Walk these four sources in order
and take the union. Each one produces errors the others miss.

1. **Validation rules.** Read the route's validator, request class, or schema. Every
   rule that can fail produces a validation status with a field-level violation. Two
   rules that fail differently and return different codes are two examples, not one.
2. **Authorization gates.** Read every gate the request passes through: unauthenticated,
   authenticated but lacking the permission, authenticated but scoped to another
   tenant or project, and step-up required. These are different statuses with
   different codes and different caller actions; collapsing them into one example
   makes the frontend treat a permission problem as a login problem.
3. **Dependency failures.** Read every outbound call the handler makes — database,
   broker, cache, another service, object storage. Each dependency that can be
   unavailable produces a status the caller must handle, and the retryability of that
   status is part of the contract.
4. **The platform's documented code list.** `alaa-services-contract` owns the exact
   codes, the success and readiness envelopes, and the required response headers.
   Read that skill's `references/10-core-service-contract.md` for the operational
   envelopes and route families, its
   `references/20-operational-and-observability-contract.md` for the `X-Request-Id` and
   `traceparent` header contract and the event and code names, and its
   `references/22-failure-load-and-deprecation-contract.md` for the shed and rate-limit
   statuses and the retry matrix. Trigger that skill as
   `/alaa-services-contract` in Claude Code or `$alaa-services-contract` in Codex when
   any code or envelope is in question.

Never restate the envelope in this skill's files or in a request description. Assert
and document the shape that skill declares. When the route's real response disagrees
with it, that is drift: record it as a gap in the task output and keep the example
matching the shipped behaviour, so the artifact stays usable while the drift is
visible.

## Example naming

Name every saved example `<status> <short condition>`, such as `422 Invalid OTP` or
`403 Missing content.publish permission`. Two constraints make this the name shape:

- Postman's mock server selects an example by name through the
  `x-mock-response-name` header, so the name is an addressable identifier.
- Generated documentation lists examples by name, so a name of `Error` tells a reader
  nothing and forces them to open the body.

One `(status, name)` pair appears at most once on a request. A single status with
several distinct causes gets several examples with distinct names — that is the
normal shape for a validation status, not a defect.

## Coherence rules for a saved example

- `code` is the numeric status. `status` is its reason phrase.
- `originalRequest` reproduces the request that produced it: same method, same URL,
  same headers, same body. A saved example whose `originalRequest` points at a
  different URL documents a request the collection cannot send.
- The body is the real serialized shape, with placeholder values. A `204` and any
  other bodyless status carries an empty body and its real headers, not a fabricated
  JSON body.
- Response headers include the ones the caller must read. `X-Request-Id` appears on
  every example because the platform returns it on every response.
- Values are safe placeholders. A token, a signed URL, a national identifier, or a
  real person's data never appears in a committed example, including inside an error
  body.

## When a route cannot get an error example

Two cases are legitimate, and both are recorded rather than left silent:

- The error exists but its body cannot be produced without inventing business data.
  Attach the example with placeholder values and say in the request's `## Errors`
  table which values are illustrative.
- The route's only failure mode is infrastructure-level and the platform normalizes
  it at the gateway. Say so in the `## Errors` table and name the gateway behaviour.

Anything else is missing coverage. Report it as a gap; do not fabricate an example to
satisfy the gate.

## Mechanical gate

```shell
python3 "$SKILL_DIR/scripts/validate_postman_artifacts.py" path/to/collection.json \
  --env path/to/environment.json \
  --require-success-example \
  --require-error-examples 1
```

`60-validation-and-output-contract.md` holds the full flag set and the exit-code
meanings.
