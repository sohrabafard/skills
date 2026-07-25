# Operational And Observability Contract

This file owns the exact stable observability surfaces that must not drift across Ala services.

Use `21-alaa-platform-observability-directive.md` together with this file when the task needs an `alaa_*` metric family name, an `OTEL_*` variable and its Ala default, a trace or route naming rule, or the current telemetry shape of a specific service. If these two files appear to conflict, this file owns the exact header, log field, event, code, probe-noise, and middleware invariants.

Requirement levels, gates, thresholds, alerts, Collector topology, sampling policy, metric label budgets, and Sentry policy are in neither file. `$alaa-observability-soc` owns them, and it wins on whether a signal is required.

## Exact response headers

The target Ala response-header contract is:
- `X-Request-Id`
- `traceparent`

Rules:
- Do not make `X-Correlation-Id` part of the final contract.
- Do not make `X-Trace-Id` part of the final contract.
- If a service still emits, parses, forwards, tests, or documents `X-Correlation-Id`, migrate it to `X-Request-Id` plus `traceparent` and remove the stale code in the same effort.
- After applying this skill, `X-Correlation-Id` must not appear anywhere in the service: not in code, config, docs, tests, fixtures, Postman artifacts, or emitted response headers.

## Exact `X-Request-Id` rules

Rules:
- Preserve an inbound `X-Request-Id` only when, after trimming leading and trailing whitespace, it matches
  `^[A-Za-z0-9._~-]{8,128}$`. That is one token of URL-safe unreserved characters, at least 8 and at most
  128 of them, with no whitespace, no comma, and no control character.
- Treat any other inbound value as absent, including an empty value, a value with an inner space, a
  multi-value header, and a value outside the length bounds. Do not sanitize it into a passing value,
  because a rewritten id no longer joins to the caller's own logs.
- When the value is absent or was treated as absent, generate a new lowercase UUIDv7.
- Emit `input.validation.failed` at debug level with a stable validation code when an inbound value is
  rejected, so a misbehaving caller is diagnosable without failing its request.
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
- make `trace_id` queryable as its own field in structured logs and OTLP log records
- include `traceparent` in structured logs when it helps propagation debugging, but never force operators to parse it for normal trace lookup
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
- `traceparent` when useful for propagation debugging or async handoff evidence
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
- `dependency.call.failed` for one failed attempt against a downstream dependency
- `dependency.unavailable` when the retry budget for that dependency is exhausted, or when the request
  deadline no longer covers another attempt
- `queue.publish.failed` when a broker publish or its outbox write fails
- `request.shed` when ingress refuses a request because in-flight requests are at the configured maximum

Use these exact code expectations:
- `HTTP_REQUEST_COMPLETED` with `http.request.completed`
- `HTTP_REQUEST_FAILED` with `http.request.failed`
- `SERVICE_NOT_READY` with `service.readiness.failed`
- `SERVICE_READY` with `service.readiness.recovered` when used
- `AUTH_*` codes from `$alaa-trust-gateway-auth` with `auth.context.invalid`
- stable domain denial codes with `authz.denied`
- stable validation codes with `input.validation.failed`
- `DEPENDENCY_CALL_FAILED` with `dependency.call.failed`
- `DEPENDENCY_UNAVAILABLE` with `dependency.unavailable`
- `QUEUE_PUBLISH_FAILED` with `queue.publish.failed`
- `REQUEST_SHED` with `request.shed`

The behaviour these four names describe is defined in `22-failure-load-and-deprecation-contract.md`. This
file owns the names; that file owns when they are emitted.

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

Use `21-alaa-platform-observability-directive.md` for the exact `alaa_*` metric family names and the metric naming and unit-suffix rules. Use `$alaa-observability-soc` for which families a service is required to expose, the label allow and deny lists beyond the request middleware layer, histogram and exemplar policy, and Collector ownership.

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
- derive and expose `trace_id` from the canonical trace context
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
- `trace_id` extractor for logs, OTLP log records, and request attributes
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
