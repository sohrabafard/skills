---
name: tusd-upload-platform
description: "Design, review, implement, and debug high-importance tusd/tus resumable-upload platforms, especially Ala services behind a trust gateway, Vue 3/Quasar/Vite/tus-js-client frontends, PHP/Laravel Octane hook and control-plane services, Go embedded tusd services, gRPC or HTTP hooks, MinIO/S3 or local staging storage, HAProxy/Nginx/API gateway behavior, security, observability, and incident response. Do not use for generic presigned uploads, non-tus protocols, or low-stakes one-off file transfer advice."
---

# tusd Upload Platform

## Mission

Use this skill to turn an agent into a tusd specialist for production architecture, review, development, debugging, and incident response. Treat tusd as an upload data plane inside Ala's gateway-first service architecture, with Vue/tus-js-client as a first-class frontend integration concern.

## When NOT to use

- Do not use for generic presigned upload advice when the tus protocol or tusd runtime is not involved.
- Do not use for non-resumable upload flows unless the task is explicitly comparing them with tus.
- Do not use for low-stakes one-off file transfer guidance that does not need production trust, storage, proxy, or observability design.

## First decisions

1. Classify the task: frontend/Vue, architecture, proxy/gateway, auth/ownership, hooks, PHP/Octane, Go embedding, observability, or incident/debug.
2. Read only the reference files needed for that class from the map below.
3. Re-check official tus, tusd, and tus-js-client sources before version-sensitive, security-sensitive, or uncertain claims.
4. When Ala platform behavior is involved, pair this skill with `$alaa-services-contract`, `$alaa-trust-gateway-auth`, and `$alaa-observability-soc`. Use `$alaa-haproxy` for HAProxy/gateway routing, `$alaa-golang` for Go service design, and the relevant Vue/Quasar skill when frontend implementation changes.

## Non-negotiable rules

- The gateway is the public trust boundary. Browser and mobile clients must never send trusted internal headers such as `X-User-Id`, `X-Project-Id`, `X-Access`, or `X-Access-Token-Id`.
- Vue/tus-js-client code must call an application upload-session API before tus creation. The client must not choose tenant, backend, object key, provider credentials, or trusted identity.
- Do not rely on `pre-create` alone for authorization. Resume, offset, download, and terminate methods also need gateway/service ownership checks.
- Treat tus upload URLs as capability URLs. Avoid storing or logging them unless resume policy requires it and ownership checks still run on every method.
- Do not stream large upload bodies through PHP or Laravel Octane. PHP/Octane should run session, hook, metadata, policy, and workflow control-plane code.
- Do not run relay, scanning, transcoding, or provider-registration work in blocking hooks. Enqueue durable jobs from non-blocking hooks or internal callbacks.
- Do not assume one stock tusd process supports multiple independent storage backends or cross-instance distributed locking.
- Do not expose provider credentials, raw upload URLs, Authorization headers, hook payload secrets, signed internal URLs, filenames, or raw metadata in logs, Sentry, analytics, or user-visible errors.
- Do not use `latest` container tags for production tusd. Pin a version and ideally a digest.

## Default platform shape

- Public client traffic goes to the gateway; the gateway strips spoofable headers, verifies tokens, injects trusted context, optionally calls route-time authz, and forwards to tusd or an embedded Go upload service.
- The application exposes `POST /api/uploads/sessions`; Vue uses the returned endpoint/upload URL, safe metadata, max-size policy, and retry/resume policy.
- Use stock tusd deployments for simple single-storage upload planes. Use an embedded Go service only when routing, custom storage, custom locks, custom middleware, or exact Ala service contracts must be owned in code.
- Use HTTP hooks for most PHP/Octane control-plane integration. Use gRPC hooks when the hook service is Go-heavy, typed contracts matter, and internal gRPC/mTLS is already operational.
- Use separate tusd deployments for distinct storage classes such as `s3-direct` and `local-staging-relay` unless a custom Go multiplexer is explicitly justified.

## Reference map

- `references/source-map.md`: official source priority, current snapshot, and freshness rules.
- `references/decision-matrix.md`: choose between stock tusd, two deployments, relay, and embedded Go.
- `references/topologies.md`: S3/MinIO direct, local staging plus relay, scaling, locking, and cleanup.
- `references/alaa-trust-gateway.md`: Ala gateway trust boundary, trusted headers, ownership checks, and route/method authorization.
- `references/hooks-auth.md`: hook events, hook response rules, auth integration, and queue handoff.
- `references/vue-frontend.md`: Vue 3, Quasar, Vite, Pinia, SSR/PWA, tus-js-client, retry/resume, UX, and frontend review rules.
- `references/client-side.md`: compact browser implementation guide and link to deeper Vue reference.
- `references/proxies.md`: Nginx, HAProxy, API gateway, CORS, buffering, timeouts, forwarded headers, and metrics protection.
- `references/security.md`: hardening, token handling, tenant isolation, CORS, metadata, and secret hygiene.
- `references/observability.md`: logs, metrics, alerts, SLOs, SOC evidence, client telemetry, and readiness.
- `references/constraints.md`: tus protocol and tusd constraints that drive design decisions.
- `references/snippets.md`: commands, templates, and adaptation guidance.

## Assets

Use assets as starting points, not blind copy-paste. Always adapt domains, auth, TLS, storage, timeouts, and version pins.

- `assets/client/useTusUpload.ts`: Vue 3 Composition API composable with tus-js-client retry, resume, pause, cancel, and safe callbacks.
- `assets/client/useUploadQueueStore.ts`: Pinia-style upload queue store for multi-upload screens.
- `assets/client/TusUploadPanel.vue`: Vue single-file component example for file selection and controls.
- `assets/client/uploadTelemetry.ts`: safe frontend telemetry helpers for Sentry or analytics.
- `assets/client/quasar.boot.uploads.ts`
- `assets/client/quasar.boot.sentry.ts`
- `assets/client/quasar.config.snippet.ts`
- `assets/docker-compose/tusd-s3.compose.yaml`
- `assets/docker-compose/tusd-staging.compose.yaml`
- `assets/env/tusd-s3.env.example`
- `assets/env/tusd-staging.env.example`
- `assets/nginx/tusd-reverse-proxy.conf`
- `assets/haproxy/tusd-reverse-proxy.cfg`
- `assets/prometheus/tusd-alert-rules.yml`
- `assets/schemas/upload-record.schema.json`

## Subagent strategy

For large production reviews, use read-only subagents on independent tracks when the environment supports multi-agent workflows: official tusd/tus-js-client versions and docs, Vue/frontend behavior, gateway/authz, proxy/storage, PHP/Octane or Go implementation, and observability/SOC. Consolidate findings into one risk-ranked answer; do not imply the skill automatically enables platform-level multi-agent features.

## Expected output from the agent

For substantial work, return a topology decision, trust/auth model for every tus method, frontend upload-session and tus-js-client flow, hook map, proxy/gateway requirements, storage and cleanup plan, PHP/Octane or Go implementation notes, observability plan, failure handling, and unresolved risks. For debugging, lead with likely root causes and concrete verification commands, browser checks, logs, or request/response fields.
