---
name: alaa-services-contract
description: "Hard contract for Ala services and shared frontend packages. Use when cross-service consistency matters for auth, content, comment, ticket, gateway, entitlement-platform, wa, notification, assessment, or future services: health/readiness, service naming, response envelopes, observability, trusted gateway headers, project_id / X-Project-Id / X-Access / X-User-Roles, compact rol claims, permission catalogs, trace/request IDs, event/code naming, Laravel Resource-first /api responses, gateway prefix maps, stripPathPrefix, public-vs-service-local routes, OpenFGA request-time authorization, auth terms, TOTP enrollment/step-up, frontend-gateway-backend flow, Docker/Swarm/Kubernetes runtime, shared infra, registry usage, SQLite fast tests, or service-ci-kit GitLab CI/CD. Also use for @alaa/sdk, @alaa/sdk-vue, Page Kit, UI Kit, app-shell, widgets, @alaa/forms, @alaa/crud, app-vs-SDK trust boundaries, correlation headers, props-in/events-out, three-layer data flow, dist-only packages, and island isolation."
---

# Alaa Services Contract

Use this skill as the hard contract layer for Ala backend services.

This skill is intentionally Ala-specific. It exists to keep Ala services aligned with one exact contract so agent output stays consistent across repositories. Treat the contract here as normative. When a target repository deviates, converge it to this contract or explicitly report the blocker. Do not improvise alternate envelopes, headers, event names, route names, middleware semantics, or repo-local observability contracts.

Keep this top-level file small. Read the reference files for the exact contract and apply steps.

This skill explains how a normal Ala backend fits into the larger platform:
- frontend calls the gateway
- gateway owns authentication, spoofed-header removal, and trusted-header injection
- the gateway may call a request-time authorization runtime such as `authz-sidecar` or `entitlement-spoa`
- entitlement-platform keeps normalized authorization truth in `entitlement-api`, projects derived tuples through `projector`, and serves route-time checks from OpenFGA
- the backend still owns normalized request handling, business authorization, response contracts, and observability inside the service boundary
- `alaa-permission-catalog` is the normative cross-service source for service-local permission configs, while auth remains the runtime JWT issuer and gateway/OpenFGA remain authorization infrastructure

## Identifier boundary and internal mTLS rollout

- A service may use private database identifiers for service-local storage, joins, ordering, and pagination. A signed opaque cursor may carry such an identifier, but APIs, URLs, events, SDKs, logs intended as public references, and other externally visible contracts must expose only the owning domain's public identifier.
- Systems outside the owning service database boundary, including OpenFGA, use the canonical public identifier or the contract-defined reversible object identifier derived from it. Do not require another service to resolve or depend on a private database identifier.
- Internal service-to-service mTLS is deliberately deferred as a coordinated platform rollout until the major system components and internal route contracts are complete. Do not make a feature or service rollout depend on bespoke per-service mTLS terminators, sidecars, certificate mounts, Services, or NetworkPolicies unless the user explicitly reactivates that work or a production exposure requires a new security decision.
- During the deferral, keep internal routes private, preserve spoofing defenses and documented trusted-ingress rules, and describe the temporary network or header trust assumption accurately. A private network or an identity header is not cryptographic service identity.
- Read `references/25-end-to-end-flow-and-boundaries.md` for the exact boundary rules.

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Read `references/00-topic-map.md`.
3. Select the repository role first: frontend-facing backend behind gateway, internal backend, auth-boundary service, or authz-runtime or control-plane service.
4. Then select the service mode: any Ala backend, deployment and runtime contract, Laravel backend, Laravel downstream trusted service, or the platform observability directive.
5. Read the smallest relevant reference file first.
6. Read `references/21-alaa-platform-observability-directive.md` whenever the task includes telemetry design, OpenTelemetry, OTLP logs/traces, Prometheus, metric catalogs, exception delivery, SigNoz, Sentry, queue or DB instrumentation, collector topology, or cross-runtime observability alignment between Go, Laravel, HAProxy, Vector, and OpenFGA.
7. Read `references/full-guide.md` when the task is cross-cutting, high-risk, or you need the preserved whole-contract view in one file.
8. Load the required companion skills before implementation work outside this skill's ownership.
9. Load `$alaa-crockford-base32-codecs` when the task needs shared Crockford Base32 or UUIDv7 helper assets across runtimes.
10. For any Laravel request body, query parameter, or DTO field named `project_id`, read `references/30-trusted-ingress-and-laravel-contract.md` before editing validation or resolution code.
11. For any permission config, bitmap id, `config/permissions.php`, Go `permissions_gen.go`, generated TypeScript `permission-catalog.ts`, `catalog/services.json` descriptor, `X-Access` decoding, or drift-check task, read `references/35-permission-catalog-and-service-configs.md` and pair with `$alaa-permission-generator` and `$alaa-trust-gateway-auth`. When the consumer is the frontend, also read `references/60-frontend-sdk-consumption-contract.md` for the UI-hint boundary.
12. For gateway-facing route prefixes, the canonical service-prefix map, `stripPathPrefix`, compact `rol` to `X-User-Roles` projection, frontend/client SDK URL composition, or public-path versus backend-local route shape, read `references/25-end-to-end-flow-and-boundaries.md` and pair with `$alaa-trust-gateway-auth`; also load `$alaa-haproxy` when actual gateway config or rendered HAProxy behavior matters.
13. For auth TOTP setup, QR/`otpauth_uri`, optional enrollment, forced route-level MFA, `AUTH_TOTP_ENABLED`, `require_totp:<purpose>`, signed step-up proof tokens, local proof caching, or gateway `X-TOTP-Proof` verification, read `references/32-auth-totp-and-step-up-contract.md`; pair it with `$alaa-trust-gateway-auth` and `$alaa-frontend-developer` when public clients, SDKs, or gateway route behavior are involved.
14. For frontend or host-app code consuming the `@alaa/*` SDK packages, read `references/60-frontend-sdk-consumption-contract.md`; for Page Kit, UI Kit, app-shell, or widget work, read `references/65-frontend-page-kit-and-widgets-contract.md`. Pair both with `$alaa-frontend-developer` and `$alaa-mono-package`, and with `$alaa-security-review` for any trust-boundary-adjacent change.
15. For request-time fine-grained authorization — adding or debugging a protected route, `authzRouteGroups`, the `authz-sidecar`/`entitlement-spoa` `HEAD /internal/authz/check` hop, the OpenFGA `check` call, endpoint-category to `can_*` mapping, canonical object ids, or the store/model pins — read `references/26-request-time-authorization-openfga.md`; pair with `$alaa-trust-gateway-auth`, `$alaa-haproxy` (gateway route config or Lua), and `$openfga` (model or tuples).
16. For how any service sends work to the `notification` service — the `notification.commands` ingress (exchange, queues, routing keys, and the canonical `message_id`/`message_type`/`producer_service`/`idempotency_key`/`payload` envelope), the snake_case-everywhere rule (including nested objects), the reserved channel-addressing model, the `entitlement-platform` audience-resolution handshake (`notif.retrieve_users` / `notif.expand_users` / `notif.recipient_chunks`), or the per-service notification matrix — read `references/27-notification-service-contract.md` (it mirrors the authoritative `notification/docs/async-contracts.md`); pair with `$alaa-async-messaging` and `$alaa-laravel-job-rabbitmq` for producers, `$alaa-golang` for the Go producer message structs, and `$alaa-observability-soc` for correlation.

## When NOT to use

- Do not use for purely local feature work that does not affect shared Ala service contracts.
- Do not use for purely visual or design polish when no package-boundary, SDK-consumption, trust-boundary, or observability contract is in scope; use `$alaa-frontend-developer` (and `$frontend-skill` for art-direction-heavy UI) for pure UI design.
- Do not use to override a repository-specific blocker; report the incompatibility instead.

## Hard contract rule

- Enforce the exact contract defined by this skill for Ala services.
- Do not downgrade exact outputs into optional recommendations.
- Do not invent local variants when this skill already defines the contract.
- Do not treat logs, traces, metrics, or exception evidence as optional for long-lived Ala services.
- When this skill replaces a legacy header, field, event, or helper, remove the old implementation instead of keeping stale compatibility code in the service.
- If a repository cannot adopt a rule exactly, stop and report the incompatibility.
- Keep references relative to this skill folder so the skill remains usable on different machines.
- Ala service names such as `auth`, `content`, `comment`, `ticket`, `vod`, and `wa` are valid inside this skill because it is intentionally platform-specific.

## Companion routing

Load these companion skills when their concern is in scope:
- `$alaa-trust-gateway-auth`
  - Load when trusted headers, auth error semantics, compact claim semantics, or tenant or project propagation are involved.
- `$alaa-permission-generator`
  - Load when registering, generating, applying, or validating catalog-owned Laravel or Go permission maps.
- `$alaa-observability-soc`
  - Load when logs, traces, metrics, alerting, incident evidence requirements, or security-log catalog work are in scope.
- `$alaa-haproxy`
  - Load when gateway route prefixes, `stripPathPrefix`, path rewriting, HAProxy ACL/backend routing, or rendered gateway behavior are in scope.
- `$alaa-golang`
  - Load when a Go service must implement this contract with Chi, OTLP, Prometheus, or service-runtime patterns that are already standardized in Ala.
- `$alaa-docker-production`
  - Load when the task changes Dockerfiles, Compose or Swarm wrappers, registry plumbing, secret mounting, runtime users, or container hardening.
- `$caas-arvan-kuber`
  - Load when the task changes the Arvan Kubernetes production path, Helm values, OCI charts, or GitLab delivery wiring.
- `$alaa-gitlab-ci-cd`
  - Load when `.gitlab-ci.yml`, GitLab validation, kit ref bumps, or pipeline debugging are in scope for an Ala service that should follow the shared `service-ci-kit` baseline.
- `$alaa-laravel-architecture`
  - Load when Laravel middleware, controllers, resources, DTOs, or service boundaries change.
- `$alaa-php-clean-code`
  - Load before implementing or refactoring PHP or Laravel code.
- `$alaa-data-layer`
  - Load when readiness checks depend on PostgreSQL, Redis, ClickHouse, bootstrap data, or persistence invariants.
- `$alaa-async-messaging` and `$alaa-laravel-job-rabbitmq`
  - Load when readiness or runtime behavior depends on RabbitMQ, queues, or workers.
- `$alaa-docs-farsi`
  - Load when docs, Postman artifacts, or runbooks change.
- `$alaa-frontend-developer`
  - Load for frontend/host architecture: the three-layer client split, SSR auth/session, and data shaping for any approved host surface.
- `$alaa-mono-package`
  - Load for any `@alaa/*` package boundary, exports, dedupe, asset-contract, or extraction decision, including promoting a helper onto the `@alaa/sdk` public surface.
- `$alaa-security-review`
  - Load for any client-side trust-boundary, token, refresh, header, or raw-HTML/sanitization change.
- `$alaa-signoz-clickhouse-docs`
  - Load when client correlation/event fields must align with how SigNoz/ClickHouse query them downstream.
- `$alaa-frontend-doc-annotations`
  - Load for the documentation pass on the public surface the host or a package adds.
- `$alaa-quasar-app-vite-v3`
  - Load for exact Quasar component/SSR shapes and the `@quasar/app-vite` build posture in widget/host work.

## Auth-specific routing

- When the task touches the `auth` service and any frontend or frontend-facing identity integration depends on academic form behavior, read `docs/ops/auth-academic-policy-contract.md` in the `auth` repository before planning or editing.
- Treat that document as the canonical frontend integration contract for auth academic policy.
- When auth academic policy changes, update the frontend implementation and any contract-facing docs or Postman artifacts in the same effort.
- Auth terms acceptance is implicit in successful OTP verification and login. The retired `user/accept-terms-and-conditions` flow must not be revived or searched for as the current API. The frontend may show a non-removable terms notice or checkbox before OTP request; the backend acceptance moment is successful `POST /api/v3/otp/verify`. Do not invent a separate accept-terms API, request field, or persistence column unless the user explicitly asks to change the legal/audit contract.
- Auth TOTP is optional self-service until a route explicitly attaches `require_totp:<purpose>`. When `AUTH_TOTP_ENABLED=true`, clients can expose setup and recovery-code flows; when disabled, clients should treat the TOTP API as unavailable, not as a generic missing route. The backend returns `secret` and `otpauth_uri` for setup; clients generate the QR code from `otpauth_uri`. Forced route rollout must document the purpose, signed proof-token target, client cache and retry behavior, gateway `X-TOTP-Proof` verification, downstream `X-TOTP-*` metadata, and Postman/OpenAPI examples.

## Frontend coding contract

This is the client-side half of the platform contract: how frontend and host-app code is allowed to consume the
`@alaa/*` SDK and widget packages so the trust boundary, refresh ownership, and package layering established for the
backend are not silently broken from the client. It complements the gateway/trusted-header orientation in
`references/25-end-to-end-flow-and-boundaries.md`.

- For SDK consumption (which package to import, app-versus-SDK responsibility, trusted headers, token/refresh,
  correlation headers), read `references/60-frontend-sdk-consumption-contract.md`. The load-bearing rules:
  - Frontend/host code imports the SDK only through `@alaa/sdk` (factory + types) and `@alaa/sdk-vue` (Vue composables).
    Never import `@alaa/sdk-core` or a domain SDK from app code; if a helper is needed, expose it on `@alaa/sdk` first.
  - The SDK owns trusted-header rejection, token attach, and single-flight refresh. The app never re-implements or
    duplicates those (including no redundant app-side trusted-header guard). The app sends only `Authorization: Bearer`,
    `X-Request-Id`, and `traceparent`; the opaque token never lands in a cookie, SSR HTML, or SSR state.
- For Page Kit, UI Kit, app-shell, and widgets, read `references/65-frontend-page-kit-and-widgets-contract.md`. The
  load-bearing rules:
  - Define the public contract first (props in / events out / types), then build behind it.
  - Widgets are props-in / events-out and own no host singletons (store, SDK, token, trusted headers, router); data
    flows presentation -> flow composable -> store -> SDK, so a widget never calls the SDK or a service directly.
  - Consume packages through public `dist`/entry exports and `link:` deps only; keep `vue`/`quasar` as peers; assets
    must reach `dist/ssr/client/assets`; do not wire island packages into legacy lanes without explicit migration
    approval; render untrusted HTML only through the sanctioned sanitizer.
- Pair both with `$alaa-frontend-developer`, `$alaa-mono-package`, and `$alaa-security-review`; pair the SDK file with
  `$alaa-trust-gateway-auth` and (for telemetry) `$alaa-observability-soc` / `$alaa-signoz-clickhouse-docs`; document
  the public surface with `$alaa-frontend-doc-annotations`.

## Reference navigation

- skill scope, use cases, service-mode selection, and auth-specific routing:
  - `references/05-scope-service-modes-and-auth-routing.md`
- topic routing and service-mode selection:
  - `references/00-topic-map.md`
- core service modes, Ala service map, service identity, route families, and exact readiness envelope:
  - `references/10-core-service-contract.md`
- deploy modes, Arvan-versus-Docker ownership, shared `service-ci-kit` GitLab CI/CD baseline, shared-versus-external Postgres rules, hard shared-infra reuse, DNS and VIP naming, key ownership, registry contract, and SQLite test support:
  - `references/15-deployment-and-runtime-contract.md`
- exact observability headers, `traceparent`, request logs, event names, and `RequestObservabilityMiddleware`:
  - `references/20-operational-and-observability-contract.md`
- full telemetry architecture, OpenTelemetry collector gateway rules, Prometheus scrape rules, shared metric catalog, and cross-runtime observability guidance:
  - `references/21-alaa-platform-observability-directive.md`
- end-to-end platform flow, frontend or gateway orientation, service ownership, and internal-hop boundaries:
  - `references/25-end-to-end-flow-and-boundaries.md`
- request-time fine-grained authorization: the gateway -> `authz-sidecar` -> OpenFGA path, exact `HEAD /internal/authz/check` and OpenFGA `check` contracts, endpoint-category to `can_*` mapping, store/model pinning, and runbooks for adding or debugging a protected route:
  - `references/26-request-time-authorization-openfga.md`
- notification cross-service contract: the `notification.commands` ingress (exchange, queues, routing keys, canonical envelope), the snake_case-everywhere rule, the reserved channel-addressing model, the `entitlement-platform` audience-resolution handshake (`notif.retrieve_users` / `notif.expand_users` / `notif.recipient_chunks`), and the per-service notification matrix (mirrors the authoritative `notification/docs/async-contracts.md`):
  - `references/27-notification-service-contract.md`
- exact trusted-ingress rules, Laravel response boundaries, `ResolveUserMiddleware`, and how backend business auth fits after gateway allow:
  - `references/30-trusted-ingress-and-laravel-contract.md`
- central permission catalog, generated service configs, drift checks, apply phases, and service-extraction bitmap rules:
  - `references/35-permission-catalog-and-service-configs.md`
- canonical public `project_id` UUIDv7 handling, `TrustedProjectContext` helper naming, and copy-oriented Laravel validation baselines:
  - `references/30-trusted-ingress-and-laravel-contract.md`
  - `references/50-laravel-copy-baselines.md`
- apply checklist, review checklist, and anti-patterns:
  - `references/40-apply-checklist-and-anti-patterns.md`
- copy-oriented Laravel class and helper baselines:
  - `references/50-laravel-copy-baselines.md`
- frontend/host consumption of the `@alaa/*` SDK packages, app-versus-SDK responsibility, client trust boundary, token/refresh ownership, and correlation headers:
  - `references/60-frontend-sdk-consumption-contract.md`
- Page Kit, UI Kit, app-shell, and widget contracts: props-in/events-out, three-layer data flow, dist-only package boundaries, island isolation, and widget security:
  - `references/65-frontend-page-kit-and-widgets-contract.md`
- official-first source map and freshness triggers:
  - `references/90-source-map.md`
- complete preserved contract in one file:
  - `references/full-guide.md`

## Maintenance rules

- Keep this file routing-first and explicit.
- Keep exact contract details in `references/`.
- Use relative reference paths only.
- When a normative rule changes in a split reference file, update `references/full-guide.md` in the same patch so the preserved whole-guide view stays complete.
- Do not strand normative Ala rules in only one document. Keep `references/00-topic-map.md`, the split references, and `references/full-guide.md` aligned.
- Keep exact route names, header names, event names, code families, metric names, and observability field names stable unless the contract is intentionally revised.
- Keep the Ala deploy contract aligned with `alaa-docker-production` and `caas-arvan-kuber` when ownership boundaries change.
- When this skill changes a contract owned jointly with another skill, update that companion skill in the same effort so the pack remains consistent.
