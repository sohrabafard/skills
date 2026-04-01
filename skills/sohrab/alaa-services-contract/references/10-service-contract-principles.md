# Service Contract Principles

## Scope

This skill governs shared operational contracts for Ala backend services such as:
- `auth`
- `vod`
- `comment`
- `ticket`
- `wa`

Apply the same contract to new Laravel backend services unless an approved exception is documented.

Choose readiness checks from the real infra of each service. Do not assume every service uses the same database or bootstrap stack.
- Use `database` for PostgreSQL-style primary database checks.
- Use `clickhouse` as a separate readiness check when the service depends on ClickHouse.
- If a service needs both, include both checks.
- Example: `auth` may check `database` plus Passport bootstrap, while `wa` may need `clickhouse` instead of `database`, or both if its architecture requires both stores.

## Canonical service identity

- `service` must be a stable machine-readable service identifier derived from `APP_NAME`.
- Expected examples are `auth`, `vod`, `comment`, `ticket`, and `wa`.
- Do not return framework, vendor, or runtime names such as `Laravel`.
- Do not decorate the value with environment names, version strings, or human-facing labels.
- If the application also needs a display name, keep it out of health and readiness payloads.

## Route family expectations

| Route family | Purpose | Public client use? | Notes |
| --- | --- | --- | --- |
| Public API routes | Product-facing browser, mobile, or partner behavior | Yes, when documented | Keep these independent from operational probes. |
| Trusted internal routes | Downstream or gateway-derived trusted context | No | Use `$alaa-trust-gateway-auth` as the source-of-truth. |
| Operational routes | Liveness, readiness, rollout checks, smoke probes | No | Keep auth expectations explicit and minimal. |

## Operational scope

- `GET /api/health` and `GET /api/ready` exist for gateway, ingress, orchestrator, runtime validation scripts, smoke checks, and automated tests.
- End-user clients should not depend on these routes for product behavior.
- `/api/ready` may be called by a gateway or an orchestrator, but the contract must not assume one specific caller. It is an operational probe.
- Keep operational routes available without access tokens, OTP, or end-user session state.

## Successful `/api/*` JSON envelope

Apply these rules to every successful JSON response under `/api/*` unless an approved exception is documented:

- Every successful `/api/*` JSON response MUST include a top-level `data` key.
- If the response returns one resource or one compound result, `data` MUST be an object.
- If the response returns a collection, `data` MUST be an array.
- Nested child resources MUST stay inline inside the parent object and MUST NOT be wrapped again with their own `data` key.
- Top-level `meta` MAY be used for transport metadata such as success messages.
- Top-level `links` MUST be reserved for real document-navigation concerns such as pagination or `self` or `describedby` links.
- Do not embed transport-level `links` inside profile or resource payload objects.
- Keep this envelope stable across Ala services so docs, SDKs, tests, and downstream consumers can rely on one success shape.

## Laravel baseline

For Laravel services, standardize these defaults unless the repository already documents a different shared pattern:
- route names: `api.health` and `api.ready`
- `GET /api/health` for process-level liveness
- `GET /api/ready` for rollout-grade readiness
- `php artisan ops:ready --json` backed by the same readiness collector when feasible
- feature tests for both healthy and not-ready paths
