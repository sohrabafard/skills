---
name: tusd-upload-platform
description: Design, review, and implement tusd-based upload platforms for resumable uploads, especially when the system must (1) store uploads directly in MinIO or another S3-compatible backend, (2) stage uploads locally and relay them to another tusd or video-provider upload server, (3) enforce application-driven authentication and authorization with hooks plus gateway checks, or (4) run under high traffic, HA, observability, and security requirements. Use this skill when choosing topology, defining auth flows, configuring hooks, hardening reverse proxies, tuning tusd flags, designing relay workers, planning cleanup, or producing production deployment templates for tusd. Do not use this skill for generic presigned S3 uploads, non-tus protocols, or low-stakes one-off file transfer advice.
---

# tusd Upload Platform

## Overview

Use this skill to turn tusd into a production upload plane instead of treating it as a standalone binary with a few flags. Focus on four recurring concerns:

1. Choose the right topology for each upload target.
2. Put authorization and ownership checks in the correct places.
3. Keep long-running side effects out of blocking hooks.
4. Design for concurrency, observability, and failure recovery from the start.

## Start With the Right Path

Classify the request first:

- **Direct-to-MinIO / S3-compatible storage**: Read `references/topologies.md` and `references/snippets.md`.
- **Upload to your own tusd, then relay to another tusd / video provider**: Read `references/topologies.md`, `references/hooks-auth.md`, and `references/security.md`.
- **Mixed platform that needs both paths**: Read `references/decision-matrix.md` first. Default to two separate tusd deployments unless the user explicitly asks for one custom Go service.
- **High-traffic, HA, or SLA-sensitive deployment**: Always read `references/observability.md` and the scaling sections in `references/topologies.md`.
- **Security-sensitive deployment**: Always read `references/security.md` and `references/hooks-auth.md`.

## Default Recommendations

Apply these defaults unless the user explicitly wants a different trade-off:

- Run **two separate tusd deployments** when the platform needs both MinIO/S3 direct storage and local-staging-plus-relay. Avoid forcing one stock tusd process to behave like multi-storage.
- Use **HTTP hooks** as the default production hook transport. Prefer them over file hooks for clustered deployments and over plugin hooks when shared central state matters.
- Put an **authenticated gateway or reverse proxy in front of tusd for every client method** (`POST`, `PATCH`, `HEAD`, `DELETE`). Do not rely on `pre-create` alone for security-sensitive ownership enforcement.
- Treat `post-finish` as a **durable job trigger**, not as the place to do large relay, transcoding, malware scanning, or other volatile work inline.
- Treat tus upload URLs as **capability URLs**. If the system must guarantee that resume requests belong to the original actor, add gateway-side ownership checks on every request.
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

## Working Method

When using this skill, follow this sequence:

1. Read `references/decision-matrix.md` to choose the platform shape.
2. Read `references/topologies.md` for the chosen path.
3. Read `references/hooks-auth.md` before designing auth, custom headers, or lifecycle automation.
4. Read `references/security.md` for any public, multi-tenant, or security-sensitive setup.
5. Read `references/observability.md` before proposing HA, SLOs, metrics, alerts, or SOC logging.
6. Read `references/snippets.md` and copy from `assets/` when generating concrete configs.

## What to Deliver

For any substantial tusd design or implementation answer, produce all of the following unless the user asked for a narrower scope:

- A clear topology choice and why it fits the stated constraints.
- The auth model for `POST`, `PATCH`, `HEAD`, and `DELETE`.
- The hook event map: which hook does what, what must stay fast, and what is queued.
- Storage behavior and cleanup plan.
- Reverse proxy and network assumptions.
- Observability plan: logs, metrics, alerting, correlation IDs.
- Failure handling and retry model.
- Open risks and operational caveats.

## Reference Map

- `references/decision-matrix.md`: Read first when choosing between one service, two services, S3 direct, or local relay.
- `references/topologies.md`: Read for end-to-end architecture, state transitions, and scaling trade-offs.
- `references/hooks-auth.md`: Read for hook selection, request ownership, queue patterns, and client-visible responses.
- `references/constraints.md`: Read when you need the non-negotiable tusd behaviors that drive the architecture.
- `references/security.md`: Read for hardening, token handling, CORS, tenant isolation, and safer defaults.
- `references/observability.md`: Read for Prometheus metrics, JSON logs, alert suggestions, SLO guidance, and profiling.
- `references/snippets.md`: Read when writing commands, configs, gateway examples, or deployment templates.

## Assets

Reuse these templates instead of inventing them from scratch:

- `assets/docker-compose/tusd-s3.compose.yaml`
- `assets/docker-compose/tusd-staging.compose.yaml`
- `assets/env/tusd-s3.env.example`
- `assets/env/tusd-staging.env.example`
- `assets/nginx/tusd-reverse-proxy.conf`
- `assets/prometheus/tusd-alert-rules.yml`
- `assets/schemas/upload-record.schema.json`

When generating concrete output, adapt these templates to the user’s domains, image tags, secret management, ports, and infrastructure conventions.
