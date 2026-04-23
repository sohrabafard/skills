---
name: jitsi-platform-architect
description: "Use this skill when the task is to evaluate, integrate, customize, secure, scale, or deploy self-hosted Jitsi Meet and Jitsi Videobridge for a product platform, especially with external auth or JWT, trust-gateway or OpenFGA-style authorization, Vue or Quasar or Vite frontend embedding (SSR, SPA, or PWA), room lifecycle, webhooks or event-driven analytics, recording or Jibri, Kubernetes or OpenShift, Docker Compose or Swarm, or high-concurrency and SLA planning. Do not use it for end-user meeting help, generic WebRTC theory, or unrelated conferencing products unless making a direct architectural comparison."
---

# Jitsi Platform Architect

## What this skill assumes

- The product is platform-centric and Jitsi is one subsystem inside a larger system.
- Identity, tenancy, billing, policy, and analytics belong to the platform, not to Jitsi.
- The platform may be security-sensitive, multi-tenant, and exposed to large concurrency.
- The answer must separate what is officially supported, what is community-supported, and what is an engineering workaround.

## Use boundaries

Use this skill for:

- architecture and product-fit decisions around Jitsi
- trust-gateway and JWT admission design
- frontend embedding, branding, and feature exposure
- eventing, watch-time analytics, and recording workflows
- Docker, Kubernetes, and OpenShift deployment choices
- scaling, stability, observability, and security reviews

## When NOT to use

- basic end-user instructions for joining or running meetings
- generic browser troubleshooting without a platform angle
- unrelated conferencing tools unless the task explicitly asks for comparison
- direct source-code modifications inside Jitsi itself unless the task is clearly about maintaining a Jitsi fork

## Default stance

- Keep control plane and media plane separate in your reasoning.
- Keep identity and authorization in the platform; Jitsi should consume a narrower meeting-scoped artifact.
- Prefer short-lived room-scoped JWTs over passing raw platform access tokens into Jitsi.
- Prefer the IFrame API for product embedding unless the task truly requires lower-level media control or a custom meeting UI.
- Treat JVB, TURN, and Jibri as separate capacity domains.
- Never promise 99.99% from a topology that still has obvious single points of failure.

## First-pass workflow

1. Classify the request: architecture/auth, frontend/embed, events/analytics, deployment, or reliability/security.
2. Capture the hard constraints: tenants, roles, room lifecycle, recording, concurrency, regions, browser/mobile support, SSR/PWA, cluster privileges, and data retention.
3. Load only the reference files that match the request.
4. Produce a deliverable with explicit decisions, tradeoffs, prerequisites, and risks.
5. Run the validation checklist before finalizing.

## Reference selection

- Architecture, auth, trust-gateway, room lifecycle: `references/architecture-and-auth.md`
- Vue/Quasar/Vite embedding, UI customization, SSR/PWA: `references/frontend-vue-quasar-vite.md`
- Webhooks, event triggers, watch-time analytics, recording signals: `references/events-webhooks-and-analytics.md`
- Docker, Swarm, Kubernetes, OpenShift, and deployment choice: `references/deployment-platforms.md`
- Scale, stability, security, observability, and SLA planning: `references/scaling-stability-security.md`
- Official source priority and freshness rules: `references/source-map.md`

## Working rules

- Make the platform the system of record for rooms, attendance, analytics, policies, and artifacts.
- Do not describe the gateway as authorizing each RTP packet. The gateway decides admission; Jitsi enforces session behavior.
- For self-hosted eventing, assume rich client-side events and component-level hooks, not a universal server-side webhook bus.
- For SSR, never instantiate Jitsi during server render. Load it only in a client-only lifecycle.
- For PWA, treat the meeting route as network-sensitive and design for reconnects, permissions, visibility changes, and heartbeat-based analytics.
- For restricted Kubernetes or OpenShift environments, validate UDP/L4 exposure and pod security constraints before recommending an in-cluster media plane.
- For Docker Swarm, be conservative. Recommend it only when the organization already standardizes on Swarm and understands the UDP/media networking implications.
- When a detail is version-sensitive, re-check the current upstream docs and releases before finalizing the answer.

## Deliverable patterns

Choose the lightest output that still resolves the task:

- Architecture memo: context, topology, auth flow, room lifecycle, event model, risks, phased rollout.
- Frontend integration plan: component pattern, token flow, config overrides, event bridge, cleanup, SSR/PWA caveats.
- Deployment plan: chosen platform, public/private ports, TLS, TURN/JVB/Jibri placement, observability, rollout, rollback.
- Risk review: top failure modes, blockers, validations, and load-test priorities.
- Decision matrix: when to choose Jitsi, when to extend it, and when to compare against classroom-first alternatives.

## Validation checklist

Before finalizing, verify that the answer:

- clearly separates control plane from media plane
- states where JWTs are minted and which claims matter
- states where public UDP terminates and how TURN is provided
- states whether recording is supported, queued, or intentionally omitted
- states whether analytics are client-derived, server-derived, or both
- states whether the proposed deployment can really support multiple JVBs
- calls out cluster-team or infra prerequisites that the app team cannot satisfy alone
- makes the remaining single points of failure obvious

## Common mistakes to avoid

- Treating Jitsi like a normal HTTP microservice.
- Assuming gateway header injection directly controls the media plane.
- Hiding blockers around UDP, host networking, LoadBalancer behavior, or cluster privileges.
- Using client-side events alone for billing-grade watch-time or compliance logs.
- Co-locating Jibri with critical JVB nodes without isolation and queueing.
- Embedding `external_api.js` in SSR output or referencing `window` during server render.
- Exposing JVB private REST or Colibri endpoints publicly.
- Copying outdated scaling tutorials without checking the current handbook.

## Freshness rules

- Prefer the official Jitsi handbook and upstream GitHub repositories first.
- Use `jitsi-contrib` resources for Kubernetes and Helm guidance.
- Use community issues and PRs mainly for operational pitfalls, not as the primary truth source.
- Re-check release state before asserting current chart behavior, config keys, packaging behavior, or deployment limitations.

## Subagent Strategy

When the environment supports multi-agent workflows, split substantial work into at most three focused read-only tracks:

1. architecture/auth and room lifecycle
2. frontend embedding, branding, and analytics/event ingestion
3. deployment, scaling, and operational risk

Merge only converged conclusions and keep unresolved constraints explicit.
