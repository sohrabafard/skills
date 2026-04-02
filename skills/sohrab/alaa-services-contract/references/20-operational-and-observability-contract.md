# Operational And Observability Contract

## Exact response headers

The target Ala response-header contract is:
- `X-Request-Id`
- `traceparent`

Rules:
- Do not make `X-Correlation-Id` part of the final contract.
- Do not make `X-Trace-Id` part of the final contract.
- If a service still emits, parses, forwards, tests, or documents `X-Correlation-Id`, migrate it to `X-Request-Id` plus `traceparent` and remove the stale code in the same effort.
- After applying this skill, no service code, config, docs, tests, or emitted response headers should still contain `X-Correlation-Id`.

## Exact `X-Request-Id` rules

Rules:
- Preserve a nonblank safe inbound `X-Request-Id`.
- Treat a value as safe only if it is one visible token, trimmed, and reasonably bounded in length.
- If absent or invalid, generate a new lowercase UUIDv7.
- Keep it stable for the lifetime of the request.
- Return it on every `/api/*` response including `/api/health`, `/api/ready`, and rendered API error responses.
- Include it in every structured request log and relevant denial or failure log.

## Exact `traceparent` rules

Canonical format:
- `00-{trace_id}-{parent_id}-01`

`trace_id` rules:
- 32 lowercase hexadecimal characters
- non-zero
- generated from secure random 16 bytes when absent or invalid

`parent_id` rules:
- 16 lowercase hexadecimal characters
- non-zero
- generated from secure random 8 bytes when absent or invalid

Incoming `traceparent` rules:
- if valid, preserve it as the canonical trace context for the request
- derive logged `trace_id` from it
- if invalid, do not fail the request only because of this
- treat it as absent and generate a fresh canonical `traceparent`

Response rules:
- always return the canonical `traceparent`
- always return `X-Request-Id`

Logging rules:
- log `trace_id`
- do not require a separate `X-Trace-Id` response header

## Structured log field contract

For logs emitted by middleware or operational flows owned by this skill, include at minimum:
- `timestamp`
- `level`
- `service`
- `service_version`
- `env`
- `event`
- `code`
- `request_id`
- `trace_id`
- `project_id` when available
- `user_id` when available and safe
- `http.method`
- `http.route` or route name
- `http.status`
- `duration_ms`

Keep the field names stable so SOC queries and runbooks remain reusable.

## Event and code naming contract

For request and operational flows owned by this skill, use these exact event names:
- `http.request.completed`
- `http.request.failed`
- `service.readiness.failed`
- `service.readiness.recovered` when a repository explicitly tracks readiness transitions
- `auth.context.invalid`
- `authz.denied`
- `input.validation.failed`

Use these exact code expectations:
- `HTTP_REQUEST_COMPLETED` with `http.request.completed`
- `HTTP_REQUEST_FAILED` with `http.request.failed`
- `SERVICE_NOT_READY` with `service.readiness.failed`
- `SERVICE_READY` with `service.readiness.recovered` when used
- `AUTH_*` codes from `$alaa-trust-gateway-auth` with `auth.context.invalid`
- stable domain denial codes with `authz.denied`
- stable validation codes with `input.validation.failed`

Rules:
- Do not invent alternate names for the same event type.
- Keep `event` and `code` aligned.
- Keep user-facing messages separate from these machine-readable names.

## Probe-noise rule

Rules:
- suppress low-value `http.request.completed` logs for successful `/api/health`
- suppress low-value `http.request.completed` logs for successful `/api/ready`
- keep not-ready responses observable
- keep unexpected failures observable
- if readiness transition tracking exists, use `service.readiness.failed` and `service.readiness.recovered`

## Metrics boundary rule

When the service emits metrics from the request middleware layer, keep labels bounded.

Allowed defaults:
- templated route or route name
- HTTP method
- status code or status class
- service
- env

Forbidden defaults:
- `user_id`
- `project_id`
- raw path
- query string
- exception message as a metric label

## `RequestObservabilityMiddleware` contract

For Laravel services, apply this middleware early on `/api/*` traffic.

Preferred order:
1. `RequestObservabilityMiddleware`
2. tenant or project normalization needed before bindings
3. `SubstituteBindings`
4. `ResolveUserMiddleware` or the equivalent trusted-user normalization layer
5. controller and policy-facing code

Required behavior:
- compute canonical `X-Request-Id`
- compute canonical `traceparent`
- store request-scoped correlation context on the request
- capture request start time
- attach `X-Request-Id` and `traceparent` to API responses
- preserve enough request context for the exception handler to attach the same headers to rendered API error responses
- emit `http.request.completed` or `http.request.failed` with the exact code rules above
- emit bounded-cardinality HTTP metrics when the repository has a metrics boundary

Required support components:
- request context normalizer
- request-id generator and validator
- `traceparent` parser and generator
- route-template or route-name resolver
- request-duration capture
- log-context sharing mechanism
- exception-path header attachment hook
- probe-noise decision logic
- metrics emission boundary

Laravel implementation rules:
- use the current Laravel logging-context sharing mechanism
- keep request state off static properties
- stay Octane-safe
- keep response-header attachment in middleware or Resource response boundaries, not in services
- when middleware rethrows, have the exception handler read the shared request context and attach `X-Request-Id` and `traceparent` to rendered API error responses
- inspect the current stack before reordering middleware blindly
