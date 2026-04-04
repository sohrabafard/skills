---
name: alaa-trust-gateway-auth
description: "Source-of-truth for Ala gateway auth trust. Use when gateway headers, JWT-derived identity, compact claim mapping, tenant propagation, or downstream trust semantics change. Do not use it as a generic auth skill outside the Ala gateway boundary."
---




# Alaa Trust Gateway Auth

## Purpose

Use this skill when a task touches the Ala gateway trust boundary, trusted headers, compact JWT-derived identity, tenant context propagation, or auth-service route shape.

Keep this top-level file small. Load the references for the full trust model, route rules, service expectations, and error contracts.

## When to use

- gateway or reverse-proxy auth routing changes
- trusted header, tenant context, or request identity work
- compact JWT custom claim reviews
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

## Compact claim map

| Compact key | Meaning                    | Forwarded header         |
|-------------|----------------------------|--------------------------|
| `m`         | mobile                     | `X-USER-MOBILE`          |
| `prm`       | permission bitmap          | `X-ACCESS`               |
| `prv`       | permission catalog version | not forwarded by default |
| `av`        | authorization version      | not forwarded by default |
| `pid`       | public project boundary    | `X-PROJECT-ID`           |
| `fn`        | first name                 | `X-User-Fname`           |
| `ln`        | last name                  | `X-User-Lname`           |
| `loc`       | location bundle            | `X-Location-*`           |

### `loc` sub-keys

| Compact key | Meaning    | Forwarded header        |
|-------------|------------|-------------------------|
| `o`         | ostan      | `X-Location-Ostan`      |
| `sr`        | shahrestan | `X-Location-Shahrestan` |
| `b`         | bakhsh     | `X-Location-Bakhsh`     |
| `sh`        | shahr      | `X-Location-Shahr`      |
| `br`        | shobe      | `X-Location-Shobe`      |
| `sc`        | school     | `X-Location-School`     |

## Header source-of-truth

| Header or context       | Trusted source                 | Notes                                                |
|-------------------------|--------------------------------|------------------------------------------------------|
| `Authorization: Bearer` | public client into the gateway | only the gateway should treat it as raw bearer input |
| `X-PROJECT-ID`          | verified `pid` claim           | trusted project boundary after verification          |
| `X-USER-ID`             | verified `sub` claim           | authenticated user identifier                        |
| `X-USER-MOBILE`         | verified `m` claim             | trusted mobile context                               |
| `X-ACCESS`              | verified `prm` claim           | compact permission bitmap                            |
| `X-ACCESS-TOKEN-ID`     | verified `jti` claim           | access-token id for session alignment                |
| `X-TOKEN-CLIENT-ID`     | verified `aud` claim           | token audience metadata                              |
| `X-TOKEN-ISSUED-AT`     | verified `iat` claim           | token issued-at metadata                             |
| `X-TOKEN-NOT-BEFORE`    | verified `nbf` claim           | token not-before metadata                            |
| `X-TOKEN-EXPIRES-AT`    | verified `exp` claim           | token expiry metadata                                |
| `X-USER-SCOPES`         | verified `scopes` claim        | token scopes metadata                                |
| `X-User-Fname`          | verified `fn` claim            | trusted first-name context                           |
| `X-User-Lname`          | verified `ln` claim            | trusted last-name context                            |
| `X-Location-Ostan`      | verified `loc.o` claim         | trusted location context                             |
| `X-Location-Shahrestan` | verified `loc.sr` claim        | trusted location context                             |
| `X-Location-Bakhsh`     | verified `loc.b` claim         | trusted location context                             |
| `X-Location-Shahr`      | verified `loc.sh` claim        | trusted location context                             |
| `X-Location-Shobe`      | verified `loc.br` claim        | trusted location context                             |
| `X-Location-School`     | verified `loc.sc` claim        | trusted location context                             |

Rules:
- the gateway sanitizes client-supplied copies of these headers before proxying
- the gateway injects trusted headers only from verified claims
- missing optional compact fields are not fabricated
- public and service-facing payloads should continue to use `project_id`; `pid` is the compact JWT claim key
- `prv` and `av` remain raw JWT metadata only unless a future contract explicitly adds a use for them

## Route family expectations

| Route family                          | Auth expectation                                                |
|---------------------------------------|-----------------------------------------------------------------|
| public auth endpoints                 | may accept raw bearer or refresh inputs at the gateway boundary |
| trusted internal or downstream routes | must consume only sanitized trusted context                     |
| local service-only routes             | must not accidentally accept public trust assumptions           |
| health or operational routes          | keep auth expectations explicit and minimal                     |

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
- $alaa-haproxy
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
- Downstream service requirements, policy flow, compact user projection, and permission bitmap:
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
