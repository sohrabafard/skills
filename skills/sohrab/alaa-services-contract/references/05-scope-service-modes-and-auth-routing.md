# Scope, Service Modes, And Auth Routing

Use this file when the task is about onboarding an agent to the Ala services contract before code changes start.

## Purpose and use

Use this skill to hard-code the Ala backend service contract across Ala services.

This contract exists so agent outputs stay consistent across services and so operational visibility remains predictable for developers, SOC operators, and platform maintainers.

This skill is intentionally Ala-specific. The portability requirement for this skill is about filesystem independence and reuse across machines, not about being generic to unrelated organizations.

Use it when:
- creating or changing `auth`, `content`, `comment`, `ticket`, `gateway`, `entitlement-platform`, `vod`, `wa`, `notification`, `assessment`, or another Ala backend or platform service
- explaining how a frontend-facing backend sits behind the gateway and inside the wider Ala platform
- standardizing the shared `service-ci-kit` GitLab CI/CD baseline for new or refactored Ala services
- standardizing `/api/health`
- standardizing `/api/ready`
- fixing exact readiness payloads and check naming
- standardizing `X-Request-Id`, `traceparent`, and queryable `trace_id`
- enforcing request and readiness event names and machine-readable codes
- standardizing `RequestObservabilityMiddleware`
- standardizing `ResolveUserMiddleware`
- fixing an `alaa_*` metric family name, an `OTEL_*` variable and its Ala default value, or a route or operation naming rule
- setting an outbound timeout, retry budget, idempotency rule, connection-pool bound, or ingress admission rule for an Ala service
- deprecating and removing any contract surface this skill defines
- aligning Laravel Resource-first `/api/*` success responses
- helping a new Ala service understand the current service landscape, ownership boundaries, and expected interaction model before implementation
- clarifying auth terms acceptance so agents do not search for or invent a retired accept-terms API
- clarifying optional auth TOTP setup, authenticator QR generation, recovery-code handling, and SDK/frontend expectations
- adding, reviewing, or documenting route-level `require_totp:<purpose>` enforcement
- forcing cross-service consistency where agents would otherwise improvise

## Platform ownership picture

Use this picture before code changes when a repo needs platform orientation.

Default Ala flow:
- frontend or public client -> gateway -> backend service
- gateway may call a request-time authorization runtime such as `authz-sidecar` or `entitlement-spoa`
- entitlement-platform keeps fine-grained authorization state through `entitlement-api`, `projector`, and OpenFGA

Plain meaning:
- the gateway owns authentication, spoofed-header removal, and trusted header injection
- entitlement-platform owns route-level fine-grained authorization state and runtime checks when those checks are enabled
- a normal backend service behind the gateway still owns request normalization, business authorization, response shaping, and observability inside the service
- frontend code must use gateway-facing routes and must never generate trusted internal headers

## Service modes

### Mode A - Any Ala backend service

Owns:
- canonical `service` identity
- route family split
- `/api/health`
- `/api/ready`
- readiness naming
- response headers
- request and readiness event naming
- request and readiness log field schema
- Ala service map and interaction orientation for new services

Read next:
- `10-core-service-contract.md`
- `20-operational-and-observability-contract.md`

### Mode A+ - Observability names and values

Adds:
- the `alaa_*` metric family catalog and the metric naming and unit-suffix rules
- `OTEL_*` variable names with their Ala default values
- resource, propagation, and route or operation naming rules
- exception and additional field names, and the never-log list
- Ala Collector placement facts and the current per-service telemetry reality table

Read next:
- `20-operational-and-observability-contract.md`
- `21-alaa-platform-observability-directive.md`
- `$alaa-observability-soc` for every requirement level, gate, threshold, alert, Collector topology, label budget, exemplar decision, and Sentry policy, which this skill does not own

### Mode B - Laravel backend service

Adds:
- route names `api.health` and `api.ready`
- `php artisan ops:ready --json`
- Laravel middleware ordering guidance
- Resource-first `/api/*` success responses

Read next:
- `10-core-service-contract.md`
- `30-trusted-ingress-and-laravel-contract.md`

### Mode A+++ - Failure, load, and deprecation contract

Adds:
- one request deadline computed at ingress and honoured by every outbound call
- Ala outbound timeout defaults per hop
- the retry budget, backoff with full jitter, and the idempotency requirement for a retried call
- what a backend does when `auth`, OpenFGA, or the notification broker is unreachable
- bounded database connection pools and the pool acquire timeout
- the shed-versus-queue rule at ingress
- the procedure for deprecating and removing a contract surface

Read next:
- `22-failure-load-and-deprecation-contract.md`
- `$alaa-reliability-sla` for the doctrine behind these values

### Mode A++ - Deployment and runtime contract

Adds:
- Arvan Kubernetes versus Docker ownership
- shared `service-ci-kit` GitLab CI/CD baseline for Ala services
- thin-wrapper `.gitlab-ci.yml` and shared-versus-local CI ownership
- shared-versus-external Postgres mode selection
- canonical shared Docker network, shared infra, DNS alias, registry, and runtime-secret rules

Read next:
- `10-core-service-contract.md`
- `15-deployment-and-runtime-contract.md`

### Mode C - Laravel downstream trusted service

Adds:
- exact trusted-header handling
- one normalized actor context
- request and auth facade parity
- `ResolveUserMiddleware` or equivalent downstream normalization layer

Read next:
- `30-trusted-ingress-and-laravel-contract.md`
- `$alaa-trust-gateway-auth`

### Mode C+ - Backend authorization and permission catalog consumer

Applies across backend runtimes when a task touches access decisions, permission bits, generated service-local permission configs, bitmap governance, `X-Access`, `X-User-Roles`, catalog drift, or role-derived behavior.

Adds:
- generated service-local permission configs
- permission bitmap id governance and `X-Access` permission-name mapping
- catalog drift checks and one-service-at-a-time apply discipline
- exact catalog-owned permission checks for backend access decisions
- no new role-based backend decision logic while the provisional freeze remains active
- passive role retention only for documented observability or future-migration needs

Read next:
- `28-backend-permission-authorization-and-role-freeze.md`
- `35-permission-catalog-and-service-configs.md`
- `$alaa-trust-gateway-auth`

### Mode D - Laravel auth-boundary service

Allows:
- request guards or `Auth::viaRequest(...)` instead of a literal downstream `ResolveUserMiddleware`

But still requires:
- the same exact trusted-header semantics
- the same outward auth behavior
- the same observability contract
- the same response contract where applicable

Read next:
- `30-trusted-ingress-and-laravel-contract.md`
- `50-laravel-copy-baselines.md`

### Mode D+ - Auth TOTP management and forced route step-up

Use when the task is about optional TOTP enrollment, authenticator-app setup, QR generation, `AUTH_TOTP_ENABLED`, recovery codes, forced route-level MFA, `require_totp:<purpose>`, or SDK/frontend step-up handling.

Read next:
- `32-auth-totp-and-step-up-contract.md`
- `$alaa-trust-gateway-auth` for gateway trust boundaries and public/internal route separation
- `$alaa-frontend-developer` for SDK and frontend challenge-and-retry behavior

## Auth-specific routing note

- When the task touches the `auth` service and any frontend or frontend-facing identity integration depends on academic form behavior, read `docs/ops/auth-academic-policy-contract.md` in the `auth` repository before planning or editing.
- Treat that document as the canonical frontend integration contract for auth academic policy.
- When auth academic policy changes, update the frontend implementation and any contract-facing docs or Postman artifacts in the same effort.
- Auth terms acceptance is implicit in successful OTP verification and login. Treat `user/accept-terms-and-conditions` as a retired flow, not as a missing current API.
- The frontend may present a non-removable terms notice or required checkbox before OTP request. The backend acceptance moment is successful `POST /api/v3/otp/verify`, when the service creates the authenticated session.
- Do not add or search for a separate accept-terms endpoint, request field, `terms_accepted_at`, `terms_version`, or consent table unless the user explicitly asks to change the legal/audit contract. If they do, treat it as a new product/legal contract change that needs docs, Postman, tests, and migration planning.
- Auth TOTP is optional self-service until a route explicitly attaches `require_totp:<purpose>`. Every rule about `AUTH_TOTP_ENABLED`, enrollment, `otpauth_uri`, recovery codes, proof tokens, and forced-route rollout is owned by `32-auth-totp-and-step-up-contract.md`. Read it there rather than restating it in a service repository.

## Working rule

- Start here when the task is cross-cutting or the target repository is new to the Ala contract.
- When the target is a new or refactored Ala service, read the deployment contract before inventing repo-local GitLab CI behavior.
- When observability design is part of the task, read `21-alaa-platform-observability-directive.md` early instead of treating metrics or tracing as an afterthought.
- After choosing a service mode, move to the smallest contract file that owns the exact rule you need.
- When the task adds or changes an outbound call between services, read `22-failure-load-and-deprecation-contract.md` before writing the client.
