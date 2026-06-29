# Alaa Services Contract Topic Map

Use this file to choose the smallest relevant reference file before loading the full guide.

## Service modes

- `Mode 0 - Skill scope and onboarding view`
  - Use when the task is about whether this skill applies, what it standardizes, how to choose the service mode, auth terms acceptance, auth TOTP setup or step-up routing, or auth-specific frontend routing notes for the `auth` service.
  - Read `05-scope-service-modes-and-auth-routing.md` first.
- `Mode A - Any Ala backend service`
  - Use when the task is about `service` identity, route families, `/api/health`, `/api/ready`, readiness checks, response headers, or observability event naming.
  - Read `10-core-service-contract.md` and `20-operational-and-observability-contract.md` first.
- `Mode A+ - Platform observability directive`
  - Use when the task is about OpenTelemetry exporter setup, OTLP endpoint ownership, queryable `trace_id`, exception delivery to SigNoz when Sentry is absent, Collector gateway topology, Prometheus scrape endpoints, metric-family selection, label/cardinality budgets, queue or dependency instrumentation, exemplars, or a shared telemetry contract across Go, Laravel, HAProxy, Vector, WA, OpenFGA, and future services.
  - Read `20-operational-and-observability-contract.md` and `21-alaa-platform-observability-directive.md`.
- `Mode A++ - Deployment and runtime contract`
  - Use when the task is about Arvan Kubernetes versus Docker ownership, Docker Compose or Docker Swarm support, explicit shared-versus-external Postgres mode selection, shared Docker networking, hard shared-infra reuse, duplicate shared-infra prevention, `DB_PROVISION_*` separation, canonical service DNS aliases, gateway DNS or VIP behavior, key ownership, registry usage, SQLite fast-test support, or the shared `service-ci-kit` GitLab CI/CD baseline and thin-wrapper `.gitlab-ci.yml` model for Ala Laravel services.
  - Read `15-deployment-and-runtime-contract.md` after `10-core-service-contract.md`.
- `Mode B - Laravel backend service`
  - Use when the task is about Laravel API response boundaries, Resources, middleware order, public `project_id` validation and resolution, or Laravel-specific route and command expectations.
  - Read `30-trusted-ingress-and-laravel-contract.md` after the core contract.
- `Mode C - Laravel downstream trusted service`
  - Use when the service sits behind the Ala gateway, consumes sanitized trusted headers, or needs to normalize `X-Project-Id`.
  - Read `30-trusted-ingress-and-laravel-contract.md` and pair with `$alaa-trust-gateway-auth`.
- `Mode C+ - Permission catalog consumer`
  - Use when the task is about `config/permissions.php`, permission names, bitmap ids, generated service permission configs, `X-Access` permission mapping, or catalog drift checks.
  - Read `35-permission-catalog-and-service-configs.md` and pair with `$alaa-trust-gateway-auth`.
- `Mode D - Laravel auth-boundary service`
  - Use when the service itself owns the trust boundary and still must satisfy the same outward trusted-ingress behavior.
  - Read `30-trusted-ingress-and-laravel-contract.md` and `50-laravel-copy-baselines.md`.
- `Mode D+ - Auth TOTP management and forced route step-up`
  - Use when the task is about auth TOTP self-service enrollment, QR or authenticator-app setup, `AUTH_TOTP_ENABLED`, `require_totp:<purpose>`, step-up errors, recovery codes, or SDK/frontend retry behavior.
  - Read `32-auth-totp-and-step-up-contract.md`; pair with `$alaa-trust-gateway-auth` for gateway boundaries and `$alaa-frontend-developer` for client/SDK flows.
- `Mode E - Platform flow and boundaries view`
  - Use when the task is about client -> gateway -> service flow, gateway route prefixes, the canonical gateway service-prefix map, `stripPathPrefix`, public prefixed routes versus service-local routes, frontend/client SDK URL composition, service ownership, the role of `authz-sidecar` or `entitlement-spoa`, `entitlement-api`, `projector`, OpenFGA, `content` versus legacy `vod`, or internal-hop discipline.
  - Read `25-end-to-end-flow-and-boundaries.md`.
- `Mode E+ - Request-time authorization with OpenFGA`
  - Use when the task is about how the per-resource decision is actually made: `authzRouteGroups`, the gateway -> `authz-sidecar`/`entitlement-spoa` `HEAD /internal/authz/check` hop, the OpenFGA `check` call and its `tuple_key`, endpoint-category to `can_*` mapping, canonical object id construction, `grant_*` vs `can_*`, the store/model/label pins, or adding or debugging a protected route.
  - Read `26-request-time-authorization-openfga.md`; pair with `$alaa-trust-gateway-auth`, `$alaa-haproxy`, and `$openfga`.
- `Mode E++ - Notification cross-service contract`
  - Use when the task is about how any service sends work to the `notification` service: the `notification.commands` ingress (exchange, queues, routing keys, canonical envelope), the snake_case-everywhere rule (including nested objects), the reserved channel-addressing model, the `entitlement-platform` audience-resolution handshake (`notif.retrieve_users`, `notif.expand_users`, `notif.recipient_chunks`), or the per-service notification matrix.
  - Read `27-notification-service-contract.md` (mirrors the authoritative `notification/docs/async-contracts.md`); pair with `$alaa-async-messaging` and `$alaa-laravel-job-rabbitmq` for producers, `$alaa-golang` for Go producers, and `$alaa-observability-soc` for correlation.
- `Mode F - Frontend coding contract`
  - Use when frontend or host-app code consumes the `@alaa/*` SDK packages, or when building/consuming Page Kit, UI Kit, app-shell, or widgets: which package to import, app-versus-SDK responsibility for trusted headers/token/refresh, public correlation headers, props-in/events-out widget contracts, three-layer data flow, dist-only package boundaries, or island isolation.
  - Read `60-frontend-sdk-consumption-contract.md` for SDK consumption and `65-frontend-page-kit-and-widgets-contract.md` for Page Kit/widgets; pair with `$alaa-frontend-developer`, `$alaa-mono-package`, and `$alaa-security-review`.

## Cross-cutting references

- `26-request-time-authorization-openfga.md`
  - The request-time authorization contract: gateway route groups, the `authz-sidecar`/`entitlement-spoa` `HEAD /internal/authz/check` hop, the OpenFGA `check` request/response, endpoint-category to `can_*` mapping, store/model pinning, and add-a-route plus debug runbooks. Pairs with `25-end-to-end-flow-and-boundaries.md` (which owns the ownership view).
- `27-notification-service-contract.md`
  - Cross-service contract for talking to the `notification` service: the `notification.commands` ingress and canonical envelope (mirrors the authoritative `notification/docs/async-contracts.md`), the snake_case-everywhere rule, the reserved channel-addressing model, the entitlement-owned `notif.*` audience-resolution handshake, the per-service matrix, and Laravel-first/Go producer rules.
- `20-operational-and-observability-contract.md`
  - Exact `X-Request-Id` and `traceparent` rules, structured log field contract, event and code naming, metrics-boundary rules, and `RequestObservabilityMiddleware`.
- `21-alaa-platform-observability-directive.md`
  - Full telemetry architecture, OTLP/Collector responsibilities, SigNoz/Sentry role split, exception fallback rules, Prometheus scrape rules, shared metric catalog, runtime-specific notes, current service reality, and validation rules for observability work.
- `32-auth-totp-and-step-up-contract.md`
  - Auth TOTP optional enrollment, `AUTH_TOTP_ENABLED`, authenticator QR generation from `otpauth_uri`, forced `require_totp:<purpose>` route rollout, client challenge/retry behavior, and SDK contract expectations.
- `40-apply-checklist-and-anti-patterns.md`
  - Use before finalizing a contract change or skill-driven implementation review.
- `50-laravel-copy-baselines.md`
  - Use only when you need copy-oriented Laravel baselines after understanding the owning rules, especially for shared `project_id` / `TrustedProjectContext` validation snippets.
- `60-frontend-sdk-consumption-contract.md`
  - Client-side consumption of the `@alaa/*` SDK: import only `@alaa/sdk` + `@alaa/sdk-vue`, app-versus-SDK ownership of trusted headers/token/refresh, the client trust boundary, and correlation headers.
- `65-frontend-page-kit-and-widgets-contract.md`
  - Page Kit, UI Kit, app-shell, and widget contracts: props-in/events-out, three-layer data flow, dist-only package boundaries, island isolation, and widget security.
- `90-source-map.md`
  - Official-first source map for version-sensitive standards, framework docs, observability docs, and community-source limits.

## Working rule

- Start with the smallest file that owns the rule you need.
- Load `full-guide.md` only when the task is broad enough that split-file navigation would cost more context than it saves.
- When observability design is in scope, treat `20` and `21` as a pair: `20` owns the exact stable surfaces and `21` owns the larger telemetry design.
