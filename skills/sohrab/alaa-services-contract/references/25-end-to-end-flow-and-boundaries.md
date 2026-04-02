# End-To-End Flow And Boundaries

Use this file when the task is about how the Ala platform fits together end-to-end, especially for onboarding an agent or a frontend developer to the shared system shape.

## Baseline platform flow

Treat the default Ala flow like this:
- public client or frontend -> gateway -> backend service
- backend service -> backend service only for internal workloads that truly require a synchronous hop
- backend service -> async infrastructure for queue, event, or job delivery when appropriate

Rules:
- do not let services recreate browser-facing trust assumptions on internal hops
- keep route ownership clear so frontend, gateway, and backend work stay aligned
- prefer direct ownership boundaries over convenience coupling across service internals

## Frontend and gateway orientation

Rules:
- frontend clients call documented gateway-facing routes, not service-local routes discovered from backend repos
- frontend clients must never generate or rely on trusted internal headers such as `X-Project-ID`, `X-User-Id`, `X-Access`, or `X-Profile`
- trusted headers belong to the gateway-to-service contract, not the public client contract
- if a route is operational, frontend clients must not treat it as product behavior

Route-shape reminder:
- gateway-facing routes may include a service prefix such as `/auth`, `/comment`, `/ticket`, `/vod`, or `/wa`
- service-local routes may differ after gateway prefix stripping
- use `$alaa-trust-gateway-auth` for exact trusted-ingress and prefix-strip behavior when the task depends on those details

## Operational caller expectations

`GET /api/health` and `GET /api/ready` exist for:
- gateway and ingress probes
- orchestrators and rollout automation
- runtime validation scripts
- smoke checks
- automated tests

Rules:
- end-user clients should not depend on these routes for product behavior
- `/api/ready` is an operational contract and must not turn into a login helper, feature flag probe, or frontend preflight endpoint
- the contract must not assume one specific operational caller

## Internal hop discipline

Rules:
- preserve `X-Request-Id` and `traceparent` across internal HTTP hops
- keep operational routes separate from product-facing routes
- do not proxy another service's `/api/ready` unless that dependency is an explicit approved rollout requirement
- if a service depends on shared infrastructure such as Redis or RabbitMQ, check that infrastructure directly instead of proxying another app's status
- if a frontend or service needs domain behavior from another service, prefer that service's public API or events over direct table coupling

## Why this file exists

This file gives one concise picture of:
- what the public client is allowed to do
- what the gateway owns
- what backend services own
- where async boundaries belong

That helps agents keep frontend, gateway, and backend work consistent instead of treating each repository as an isolated system.
