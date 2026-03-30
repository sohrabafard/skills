---
name: tusd-upload-platform
description: "Design, review, and implement tusd-based upload platforms for resumable uploads, especially when the system must (1) store uploads directly in MinIO or another S3-compatible backend, (2) stage uploads locally and relay them to another tusd or video-provider upload server, (3) enforce application-driven authentication and authorization with hooks plus gateway checks, (4) run behind Nginx or HAProxy under high traffic, HA, observability, and security requirements, or (5) integrate browser-side tus clients in Vue.js + Quasar + Vite applications, including SSR or PWA mode. Use this skill when choosing topology, defining auth flows, configuring hooks, hardening reverse proxies, tuning tusd flags, designing relay workers, planning cleanup, or implementing production client upload flows for tusd. Do not use this skill for generic presigned S3 uploads, non-tus protocols, or low-stakes one-off file transfer advice."
---




# tusd Upload Platform

## Overview

Use this skill to turn tusd into a production upload plane instead of treating it as a standalone binary with a few flags. Focus on five recurring concerns:

1. Choose the right topology for each upload target.
2. Put authorization and ownership checks in the correct places.
3. Keep long-running side effects out of blocking hooks.
4. Pick and harden the right reverse proxy path: Nginx or HAProxy.
5. Make browser-side tus uploads operationally safe for SSR, PWA, observability, and security-sensitive products.

## Start With the Right Path

Classify the request first:

- **Direct-to-MinIO / S3-compatible storage**: Read `references/topologies.md` and `references/snippets.md`.
- **Upload to your own tusd, then relay to another tusd / video provider**: Read `references/topologies.md`, `references/hooks-auth.md`, and `references/security.md`.
- **Mixed platform that needs both paths**: Read `references/decision-matrix.md` first. Default to two separate tusd deployments unless the user explicitly asks for one custom Go service.
- **Proxy or gateway design question**: Always read `references/proxies.md`.
- **Client-side upload implementation**: Always read `references/client-side.md`, then re-read `references/security.md` and `references/observability.md`.
- **High-traffic, HA, or SLA-sensitive deployment**: Always read `references/observability.md`, `references/proxies.md`, and the scaling sections in `references/topologies.md`.
- **Security-sensitive deployment**: Always read `references/security.md` and `references/hooks-auth.md`.

## When NOT to use
- do not use this skill for generic presigned-upload flows, non-tus protocols, or one-off file transfer advice with no resumable-upload platform design
- do not assume stock tusd provides a built-in remote-provider relay backend or cross-instance locking model that it does not document
- do not treat browser upload URLs, provider credentials, or hook payloads as safe to expose outside the platform trust boundary

## Default Recommendations

Apply these defaults unless the user explicitly wants a different trade-off:

- Run **two separate tusd deployments** when the platform needs both MinIO/S3 direct storage and local-staging-plus-relay. Avoid forcing one stock tusd process to behave like multi-storage.
- Use **HTTP hooks** as the default production hook transport. Prefer them over file hooks for clustered deployments and over plugin hooks when shared central state matters.
- Put an **authenticated gateway or reverse proxy in front of tusd for every client method** (`POST`, `PATCH`, `HEAD`, `DELETE`). Do not rely on `pre-create` alone for security-sensitive ownership enforcement.
- Support **either Nginx or HAProxy**. Choose based on existing platform conventions, ingress standards, stickiness strategy, and operational ownership. Do not assume Nginx-only.
- Treat `post-finish` as a **durable job trigger**, not as the place to do large relay, transcoding, malware scanning, or other volatile work inline.
- Treat tus upload URLs as **capability URLs**. If the system must guarantee that resume requests belong to the original actor, add gateway-side ownership checks on every request.
- For browser uploads, have the **application issue an upload session** first. The client should not invent auth state, backend selection, or policy metadata locally.
- In Vue.js + Quasar + Vite apps, keep tus upload logic **client-only** when SSR is enabled, and keep service workers away from upload endpoints when PWA is enabled.
- Restrict **CORS, downloads, and termination** explicitly in production. Do not leave the defaults unreviewed.
- When using S3-compatible storage, budget for **temporary local disk** as well as object storage.

## Non-Negotiable Rules

- Never expose upstream provider tokens, API keys, or service-owned upload credentials to browsers or mobile apps.
- Never recommend synchronous relay-to-upstream inside a blocking hook.
- Never make the `pre-finish` response the only source of truth for the final asset URL or provider ID.
- Never assume built-in tusd lockers protect uploads across multiple instances.
- Never depend on hook execution order except for the documented guarantees.
- Never use file hooks as the primary production pattern for a horizontally scaled cluster unless the user explicitly accepts per-instance hook execution.
- Never invent a direct built-in "remote tusd storage backend" for stock tusd. If the user needs that behavior, recommend a relay worker or a custom Go datastore/handler design.
- Never let SSR code, server-render code, or service workers touch browser-only tus primitives by accident.
- Never send raw upload URLs, Authorization headers, cookies, or provider tokens into Sentry, analytics, or user-visible logs.

## Working Method

When using this skill, follow this sequence:

1. Read `references/decision-matrix.md` to choose the platform shape.
2. Read `references/topologies.md` for the chosen path.
3. Read `references/proxies.md` before proposing Nginx, HAProxy, gateway auth, or load-balancer behavior.
4. Read `references/hooks-auth.md` before designing auth, custom headers, or lifecycle automation.
5. Read `references/security.md` for any public, multi-tenant, or security-sensitive setup.
6. Read `references/client-side.md` before proposing browser or app-side tus logic.
7. Read `references/observability.md` before proposing HA, SLOs, metrics, alerts, or SOC logging.
8. Read `references/snippets.md` and copy from `assets/` when generating concrete configs.

## Companion routing

- `$alaa-frontend-developer`
  - Pair for browser upload UX, SSR-safe client flows, or auth/session handling.
- `$quasar-skill-packe`
  - Pair when the client lives in a Quasar app and the issue is Quasar-specific.
- `$alaa-haproxy`
  - Pair when HAProxy termination, stickiness, or request forwarding behavior matters.
- `$caas-arvan-kuber`
  - Pair when the deployment target is Arvan CaaS or Kubernetes constraints drive the design.
- `$alaa-observability-soc`
  - Pair when SLOs, alerts, or security logging are part of the platform design.

## What to Deliver

For any substantial tusd design or implementation answer, produce all of the following unless the user asked for a narrower scope:

- A clear topology choice and why it fits the stated constraints.
- The proxy choice and why Nginx or HAProxy is the better fit for the stated environment.
- The auth model for `POST`, `PATCH`, `HEAD`, and `DELETE`.
- The hook event map: which hook does what, what must stay fast, and what is queued.
- The client upload flow: session creation, resume strategy, cancellation policy, and SSR/PWA handling when relevant.
- Storage behavior and cleanup plan.
- Reverse proxy and network assumptions.
- Observability plan: logs, metrics, alerting, correlation IDs, SOC routing, and client exception hygiene.
- Failure handling and retry model.
- Open risks and operational caveats.

## Reference Map

- `references/decision-matrix.md`: Read first when choosing between one service, two services, S3 direct, or local relay.
- `references/topologies.md`: Read for end-to-end architecture, state transitions, and scaling trade-offs.
- `references/proxies.md`: Read for Nginx vs HAProxy selection, forwarded headers, buffering rules, timeouts, and stickiness.
- `references/hooks-auth.md`: Read for hook selection, request ownership, queue patterns, and client-visible responses.
- `references/client-side.md`: Read for Vue.js + Quasar + Vite client uploads, SSR/PWA constraints, tus-js-client defaults, and Sentry-safe error reporting.
- `references/constraints.md`: Read when you need the non-negotiable tusd and tus protocol behaviors that drive the architecture.
- `references/security.md`: Read for hardening, token handling, CORS, tenant isolation, client resume risk, and safer defaults.
- `references/observability.md`: Read for Prometheus metrics, JSON logs, alert suggestions, SLO guidance, client telemetry, and SOC logging.
- `references/snippets.md`: Read when writing commands, configs, gateway examples, client code stubs, or deployment templates.

## Assets

Reuse these templates instead of inventing them from scratch:

- `assets/docker-compose/tusd-s3.compose.yaml`
- `assets/docker-compose/tusd-staging.compose.yaml`
- `assets/env/tusd-s3.env.example`
- `assets/env/tusd-staging.env.example`
- `assets/nginx/tusd-reverse-proxy.conf`
- `assets/haproxy/tusd-reverse-proxy.cfg`
- `assets/client/useTusUpload.ts`
- `assets/client/quasar.boot.uploads.ts`
- `assets/client/quasar.boot.sentry.ts`
- `assets/client/quasar.config.snippet.ts`
- `assets/prometheus/tusd-alert-rules.yml`
- `assets/schemas/upload-record.schema.json`

When generating concrete output, adapt these templates to the user's domains, image tags, secret management, ports, infrastructure conventions, Quasar mode selection, and telemetry stack.
