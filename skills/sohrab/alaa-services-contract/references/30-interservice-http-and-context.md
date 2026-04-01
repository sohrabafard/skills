# Interservice HTTP And Context

## Baseline flow

Treat the default Ala flow like this:
- public client -> gateway -> backend service
- backend service -> backend service only for internal workloads that truly require it
- backend service -> async infrastructure for queue, event, or job delivery when appropriate

Do not let services recreate browser-facing trust assumptions on internal hops.

## Trust-boundary handoff

- Use `$alaa-trust-gateway-auth` as the source-of-truth for gateway-derived identity, trusted headers, tenant or project propagation, and downstream auth semantics.
- Do not redefine trusted auth headers in this skill.
- Do not let one service invent a new internal auth contract that conflicts with the gateway-trust model.

## Correlation and probe traceability

- Preserve `X-Request-Id`, `X-Correlation-Id`, and `traceparent` across internal HTTP hops when the shared stack already supports them.
- Return the same correlation headers from `/api/health` and `/api/ready` when possible so probes remain traceable.
- Keep probe logging low-noise, but do not remove transition logs that are operationally valuable.

## Readiness boundaries

- Prefer direct checks of the service's own required infrastructure and bootstrap state.
- Do not implement `/api/ready` by calling another service's `/api/ready` unless that dependency is an explicit, approved part of rollout semantics.
- Avoid transitive readiness chains that amplify unrelated failures across the platform.
- If a service depends on shared infrastructure such as Redis or RabbitMQ, check that infrastructure directly instead of proxying another app's status.

## HTTP contract discipline

- Keep operational routes separate from product-facing routes.
- Do not require bearer tokens, OTP, or user cookies for operational routes.
- Keep machine-readable fields stable and English-language messages short and operational.
- Prefer one shared operational envelope across Ala services over per-service custom payload shapes.
