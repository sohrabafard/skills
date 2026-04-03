---
name: alaa-services-contract
description: "Hard contract for Ala backend services such as auth, comment, ticket, vod, and wa. Use when an agent must enforce exact Ala service behavior for `/api/health`, `/api/ready`, service naming, response envelopes, RequestObservabilityMiddleware, ResolveUserMiddleware, trusted-header handling, event/code naming, Laravel Resource-first `/api/*` responses, or the Ala deploy contract for Arvan Kubernetes, Docker Compose, Docker Swarm, shared Docker networking, canonical service DNS aliases, auth key ownership, registry usage, and fast-test SQLite support. Use when consistency across Ala services matters more than local preference."
---

# Alaa Services Contract

Use this skill as the hard contract layer for Ala backend services.

This skill is intentionally Ala-specific. It exists to keep Ala services aligned with one exact contract so agent output stays consistent across repositories. Treat the contract here as normative. When a target repository deviates, converge it to this contract or explicitly report the blocker. Do not improvise alternate envelopes, headers, event names, route names, or middleware semantics.

Keep this top-level file small. Read the reference files for the exact contract and apply steps.

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Read `references/00-topic-map.md`.
3. Select the service mode first: any Ala backend, deployment and runtime contract, Laravel backend, Laravel downstream trusted service, or Laravel auth-boundary service.
4. Read the smallest relevant reference file first.
5. Read `references/full-guide.md` when the task is cross-cutting or high-risk.
6. Load the required companion skills before implementation work outside this skill's ownership.

## Hard contract rule

- Enforce the exact contract defined by this skill for Ala services.
- Do not downgrade exact outputs into optional recommendations.
- Do not invent local variants when this skill already defines the contract.
- When this skill replaces a legacy header, field, event, or helper, remove the old implementation instead of keeping stale compatibility code in the service.
- If a repository cannot adopt a rule exactly, stop and report the incompatibility.
- Keep references relative to this skill folder so the skill remains usable on different machines.
- Ala service names such as `auth`, `comment`, `ticket`, `vod`, and `wa` are valid inside this skill because it is intentionally platform-specific.

## Companion routing

Load these companion skills when their concern is in scope:
- `$alaa-trust-gateway-auth`
  - Load when trusted headers, auth error semantics, permission bitmap rules, `X-Profile`, or tenant or project propagation are involved.
- `$alaa-observability-soc`
  - Load when logs, traces, metrics, alerting, event naming, or incident evidence requirements are involved.
- `$alaa-docker-production`
  - Load when the task changes Dockerfiles, Compose or Swarm wrappers, registry plumbing, secret mounting, runtime users, or container hardening.
- `$caas-arvan-kuber`
  - Load when the task changes the Arvan Kubernetes production path, Helm values, OCI charts, or GitLab delivery wiring.
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

## Auth-specific routing

- When the task touches the `auth` service and any frontend or frontend-facing profile integration depends on academic form behavior, read `docs/ops/auth-academic-policy-contract.md` in the `auth` repository before planning or editing.
- Treat that document as the canonical frontend integration contract for auth academic policy.
- When auth academic policy changes, update the frontend implementation and any contract-facing docs or Postman artifacts in the same effort.

## Reference navigation

- topic routing and service-mode selection:
  - `references/00-topic-map.md`
- core service modes, Ala service map, service identity, route families, and exact readiness envelope:
  - `references/10-core-service-contract.md`
- deploy modes, Arvan-versus-Docker ownership, shared network and infra rules, DNS and VIP naming, key ownership, registry contract, and SQLite test support:
  - `references/15-deployment-and-runtime-contract.md`
- end-to-end platform flow, frontend or gateway orientation, and internal-hop boundaries:
  - `references/25-end-to-end-flow-and-boundaries.md`
- exact observability headers, `traceparent`, request logs, event names, and `RequestObservabilityMiddleware`:
  - `references/20-operational-and-observability-contract.md`
- exact trusted-ingress rules, Laravel response boundaries, and `ResolveUserMiddleware`:
  - `references/30-trusted-ingress-and-laravel-contract.md`
- apply checklist, review checklist, and anti-patterns:
  - `references/40-apply-checklist-and-anti-patterns.md`
- copy-oriented Laravel class and helper baselines:
  - `references/50-laravel-copy-baselines.md`
- complete preserved contract in one file:
  - `references/full-guide.md`

## Maintenance rules

- Keep this file routing-first and explicit.
- Keep exact contract details in `references/`.
- Use relative reference paths only.
- Keep exact route names, header names, event names, and code families stable unless the contract is intentionally revised.
- Keep the Ala deploy contract aligned with `alaa-docker-production` and `caas-arvan-kuber` when ownership boundaries change.
- When this skill changes a contract owned jointly with another skill, update that companion skill in the same effort so the pack remains consistent.
