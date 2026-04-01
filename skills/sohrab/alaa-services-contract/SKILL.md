---
name: alaa-services-contract
description: "Source-of-truth for hardened Ala backend service contracts. Use when creating or changing backend services such as auth, vod, comment, ticket, or wa; when standardizing `/api/health` or `/api/ready`; when aligning service naming, rollout readiness checks, internal-vs-public route behavior, inter-service request and response expectations, or framework-specific service rules such as Laravel API response contracts; and when an agent needs the canonical contract that all Ala services must follow."
---

# Alaa Services Contract

## Purpose

Use this skill to keep Ala backend services operationally and contractually consistent.

This skill owns shared service-level rules such as:
- service naming
- health and readiness routes
- rollout-grade dependency and bootstrap checks
- internal versus public route expectations
- baseline inter-service HTTP behavior
- Laravel-only API response rules when the target service is Laravel-based

Keep this top-level file small. Read the topic map first, then load only the matching sections from `references/full-guide.md`.

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Read `references/00-topic-map.md`.
3. Identify whether the task is mainly about service naming, health/readiness, inter-service HTTP flow, Laravel-only API response rules, or service adoption.
4. Load only the matching sections from `references/full-guide.md`.
5. Read the required companion skills before changing auth trust, observability, data, async, architecture, docs, or Laravel response boundaries.

## Non-negotiable defaults

- Keep `GET /api/health` and `GET /api/ready` unauthenticated and operational only.
- Treat `/api/ready` as an internal infra and automation contract, not a public client contract.
- Make the `service` field come from `APP_NAME` or a config value derived directly from it. Never return framework names such as `Laravel`.
- Preserve the exact readiness response envelope described in `references/full-guide.md` unless there is an explicit cross-service design decision to change it.
- Add checks for every required dependency or bootstrap invariant the service needs before it can serve rollout-grade traffic.
- Model readiness checks from the real infrastructure of that service. Use `database` for PostgreSQL-style primary database checks and `clickhouse` as a separate check when the service depends on ClickHouse.
- If a service depends on both PostgreSQL and ClickHouse, include both `database` and `clickhouse` in the same readiness payload.
- Keep check names, failure lists, and ordering stable and deterministic.
- Prefer one canonical contract across `auth`, `vod`, `comment`, `ticket`, and `wa`. Document exceptions instead of improvising per service.
- Apply Laravel Resource-first response rules only when the target service is Laravel-based.

## Companion skills

- `$alaa-workflow`
  Pair when applying this skill requires non-trivial, multi-file, or behavior-changing work.
- `$alaa-trust-gateway-auth`
  Mandatory when gateway-derived identity, trusted headers, tenant or project propagation, or downstream trust semantics change.
- `$alaa-observability-soc`
  Pair when correlation headers, logs, traces, probe noise, or alert behavior changes.
- `$alaa-data-layer`
  Pair when readiness checks depend on schema, seed/bootstrap state, Redis state, PostgreSQL state, ClickHouse state, or other persistence invariants.
- `$alaa-async-messaging` and `$alaa-laravel-job-rabbitmq`
  Pair when readiness includes RabbitMQ or queue-plane expectations.
- `$alaa-laravel-architecture`
  Pair when route, controller, service, request, resource, or DTO boundaries change in Laravel services.
- `$alaa-php-clean-code`
  Pair when implementing PHP or Laravel code changes.
- `$alaa-docs-farsi`
  Pair when docs, runbooks, or Postman artifacts must be updated. The preferred output for all documentation is simple, fluent, natural English with complete and correct sentences. Do not create a separate Persian version just because the skill name says `farsi`. If an existing document is already written in Persian, update that same document in place and do not change its language unless the user explicitly asks for it.

## Reference navigation

- Topic map and fast routing:
  `references/00-topic-map.md`
- Full preserved guidance, rules, examples, and checklists:
  `references/full-guide.md`

## Maintenance rules

- Keep the main contract cross-service and framework-agnostic unless a rule is explicitly scoped otherwise.
- Put detailed contract rules into `references/full-guide.md` instead of growing this file.
- Keep the topic map aligned with the actual headings in `references/full-guide.md`.
- Keep the auth service as the first proven reference implementation, then converge the other Ala services toward the same contract.
- Keep route names, payload keys, and status semantics stable once published internally.
- When another skill owns a deeper concern, route to it instead of duplicating its rules here.
