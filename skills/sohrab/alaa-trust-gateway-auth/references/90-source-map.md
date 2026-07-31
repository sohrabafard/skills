# Source priority and freshness

Read this file before asserting any gateway or auth behaviour that a reader might
act on, and whenever a fact in this skill is older than the change you are making.

## Priority when sources disagree

1. **The active HAProxy template and values in the gateway repository.** This is
   what runs, and it wins over everything below it, including this skill.
2. **Rendered manifests from the gateway repository.**
3. **The auth repository's `routes/api.php`**, then its `docs/ops/*` contracts, then
   its README.
4. **Gateway docs and README text.**
5. **`alaa-services-contract`** for platform-wide boundaries, header-name freezes,
   envelopes and values; **`alaa-permission-generator`** for the bitmap contract,
   allocation and emitted decoders.
6. **This skill's references**, for the trust doctrine that ties those together.
7. **Primary standards** — RFC 7519 (JWT), RFC 8725 (JWT BCP), RFC 6750 (Bearer),
   RFC 9700 (OAuth 2.0 Security BCP), the OpenFGA documentation, the HAProxy
   documentation, the Laravel documentation.
8. **Community answers and copied snippets**, only for troubleshooting an observed
   error, and only after the repositories and the primary standards were checked.

If a README and the HAProxy configuration disagree, trust the configuration and
treat the README as drift to fix.

Repository paths in this skill are repository-relative. Resolve them against
wherever your machine keeps the `gateway`, `auth` and `alaa-permission-catalog`
checkouts. A skill that carries an absolute machine path is wrong on every other
machine, and it was wrong here until 2026-07-27.

## Re-check the source when the task mentions any of these

- current gateway behaviour, a JWT claim change, token refresh, trusted headers,
  tenant or project naming, or the auth-service v3 route shape
- HAProxy ACL order, JWT verification, SPOE or SPOA wiring, an OpenFGA model change,
  or `authz-sidecar` / `entitlement-spoa` behaviour
- TOTP step-up: the proof lifetime, the verified claim set, the injected header
  names, or whether the gateway blocks
- a security update, key rotation, an accepted-algorithm change, a token lifetime, a
  replay-handling change, or a public-versus-protected route change
- any permission id, id range, active count or catalog version

## Facts in this skill with a read date

| Fact | Verified on | Where |
|---|---|---|
| Gateway verifies the TOTP proof and never blocks; injects three headers only on full validity | 2026-07-27 | gateway `charts/gateway/templates/configmap.yaml:487-583`, `docs/totp-proof-gateway-contract.md:9,51` |
| The three backend-only `X-TOTP-*` names are on the sanitize list, plus a Lua wildcard sweep sparing `X-TOTP-Proof` | 2026-07-27 | gateway `charts/gateway/values.yaml:207-209`, `configmap.yaml:250-254`, `haproxy/lua/authz-sidecar.lua:487-494` |
| The proof is not single-use and there is no replay table | 2026-07-27 | gateway `docs/totp-proof-gateway-contract.md:52` |
| Auth's `RequireTotpMiddleware` enforces against an auth-local cache marker, not the gateway headers; `X-TOTP` appears nowhere in auth's `app/`, `config/`, `routes/`, `bootstrap/` | 2026-07-27 | auth `app/Http/Middleware/RequireTotpMiddleware.php` |
| Permission catalog held 130 active permissions, highest bitmap id 130, contiguous from 1 | 2026-07-27 | `alaa-permission-catalog` `catalog/permissions.json` |
| No occurrence of `BYPASS_GATEWAY_PROOF` in the gateway repository's charts, HAProxy assets or docs, nor in auth | 2026-07-27 | case-insensitive search; see `references/30-fail-closed-cases.md` case 8 |
| `X-Project-Id` is injected from the verified `pid` claim whenever the request carried a token the gateway verified, and that holds whether or not the route required authentication | 2026-07-31 | maintainer ruling, recorded in `references/10-verification-and-ingress.md`. **Not confirmed against the deployed gateway.** Establish the deployed behaviour before acting on this row |
| A request carrying no token carries its project id in the request body as `project_id`, sourced from the client's `PROJECT_ID` configuration; the gateway injects no header and reads no body, and the receiving service rejects a body that carries none | 2026-07-31 | maintainer ruling, ratified and recorded in `references/10-verification-and-ingress.md`. **Not confirmed against any deployed service.** Establish what the receiving service does today before acting on this row. The matching client-side rule is `alaa-services-contract references/60-frontend-sdk-consumption-contract.md` |

| A tokenless request that has no body carries its project id as a `project_id` query parameter, and a route may scope a read by that value only while it is on the receiving service's explicit read list | 2026-07-31 | maintainer ruling, ratified and recorded in `references/10-verification-and-ingress.md`. Gateway side confirmed in the rendered template: no query-string fetch, `path` matching, `set-path` prefix stripping. **Service side confirmed nowhere.** Establish what the receiving service does today before acting on this row |

A fact without a read date in this skill is older than this table and is re-derived
before it is acted on.

## A domain-bounded example

**Good.** `X-Project-Id` behaviour is changing, so inspect the `pid` producer in
auth, the gateway's injection and sanitize blocks, the downstream middleware, the
docs and the Postman examples, and change them together.

**Bad.** A downstream service's local numeric project fixture is taken as evidence
that a client may choose tenant context directly. It is a migration fixture in a
backend-only test path.
