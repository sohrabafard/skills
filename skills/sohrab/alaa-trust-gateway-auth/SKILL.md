---
name: alaa-trust-gateway-auth
description: "Source-of-truth for Ala gateway auth trust: how Bearer JWT enters, what HAProxy verifies, which X-* headers are sanitized or injected, how tenant and trusted profile context are derived, how X-Profile is propagated, and what downstream services must do with trusted context, profile decoding, and local profile storage."
---

# Alaa Trust Gateway Auth

## Purpose

Use this skill when a task touches the Ala gateway trust boundary, trusted headers, JWT-derived identity, tenant context propagation, or auth-service route shape.

Keep this top-level file small. Load the references for the full trust model, route rules, service expectations, and error contracts.

## When to use

- gateway or reverse-proxy auth routing changes
- trusted header, tenant context, or request identity work
- auth-service v3 route, refresh, logout, or profile contract reviews
- downstream service middleware or policy changes behind the gateway

## When NOT to use

- do not use it as a generic auth skill for services that are not behind the Ala gateway
- do not use it without also reading the relevant companion skill for framework, runtime, security, or deployment changes

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Read `references/00-topic-map.md`.
3. Identify whether the task is mainly about routing, header trust, auth-service contract, downstream service behavior, or error semantics.
4. Load only the matching reference file first.
5. Read the required companion skills before suggesting implementation changes outside this skill's trust-boundary ownership.

## Companion routing

- $alaa-security-review
  - Mandatory when JWT verification, tenant isolation, token handling, or header-trust risk is in scope.
- $alaa-laravel-architecture
  - Mandatory when Laravel middleware, request context builders, controllers, or policy flow change.
- $alaa-php-clean-code
  - Pair when the task also changes PHP or Laravel implementation style and local refactor discipline.
- $alaa-octane-performance
  - Mandatory when long-lived workers or request-state reset behavior affect trusted auth context.
- $alaa-observability-soc
  - Pair when deny logs, request correlation, trace propagation, or auth event visibility changes.
- $alaa-docker-production
  - Pair when trusted proxy boundaries, direct exposure, or container-network trust rules change.
- $haproxy-3.2-skill
  - Mandatory when HAProxy ACL order, JWT verification, path stripping, or header mutation changes.
- $caas-arvan-kuber
  - Pair when Arvan or Kubernetes exposure changes affect the public trust boundary.

## Reference navigation

- Section map and fast routing:
  - `references/00-topic-map.md`
- Source priority, rename rules, public vs local routes, and routing order:
  - `references/10-source-priority-and-routing.md`
- What the gateway verifies, trusted header rules, and tenant or user context:
  - `references/20-core-trust-model-and-headers.md`
- Auth-service v3 endpoint contract, client flow, and route families:
  - `references/30-auth-service-v3-and-route-shapes.md`
- Downstream service requirements, policy flow, permission bitmap, and observability:
  - `references/40-downstream-service-rules.md`
- Error contracts, implementation checklist, review checklist, related skills, and anti-patterns:
  - `references/50-error-contract-checklists-and-anti-patterns.md`
- Full preserved guidance, rules, examples, and checklists:
  - `references/full-guide.md`
- Permission bitmap reference asset:
  - `references/permission-bitmap.php`
- Historical request-for-change note:
  - `request-for-change.md`

## Maintenance rules

- Keep this file routing-first and easy to scan.
- Put detailed trust rules into `references/` instead of growing this file again.
- Keep the topic map aligned with the actual headings in the full guide.
- Keep examples and contracts in simple English and preserve exact route or header names when they are normative.
