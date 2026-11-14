# Source priority and freshness

Read before asserting actionable gateway/auth behaviour or using a fact older
than your change.

## Priority when sources disagree

1. **Active gateway HAProxy template and values.** Executable authority over all
   sources below, including this skill.
2. **Rendered manifests from the gateway repository.**
3. **The auth repository's `routes/api.php`**, then its `docs/ops/*` contracts, then
   its README.
4. **Gateway docs and README text.**
5. **`alaa-services-contract`** for platform-wide boundaries, header-name freezes,
   envelopes and values; **`alaa-permission-generator`** for the bitmap contract,
   allocation and emitted decoders.
6. **This skill's references**, for the trust doctrine that ties those together.
7. **Primary standards** — RFC 7519 (JWT), RFC 8725 (JWT BCP), RFC 6750 (Bearer),
   RFC 9700 (OAuth 2.0 Security BCP); OpenFGA, HAProxy and Laravel documentation.
8. **Community answers/copied snippets**, only for observed-error troubleshooting
   after checking repositories and primary standards.

HAProxy configuration wins over README drift; fix the README.

Resolve repository-relative paths against the named checkout. Absolute machine
paths are non-portable; this skill carried them until 2026-07-27.

Checker interface: authz-sidecar
`<repo>/docs/integrations/gateway/authz-sidecar-contract.md`.
Canonical model/mapping: authz-openfga `<repo>/platform/openfga/contracts/`.
`entitlement-api` owns business truth/events; `entitlement-projector` owns projection.
Imported pinned bundles are consumer snapshots, never authoring roots; gateway
executable configuration retains edge authority.

## What this skill does not own

`SKILL.md` *When not to use* states what to do when a change lands on one of these grounds.

| Ground | Owner |
|---|---|
| Trusted header **names**, response envelopes, error taxonomy, platform values | `/alaa-services-contract` |
| TOTP proof claim set, step-up response body, purpose naming, client proof caching | `/alaa-services-contract` `references/32-auth-totp-and-step-up-contract.md` |
| The permission bit contract, id allocation, catalog drift, decoders and harness | `/alaa-permission-generator` |
| Fail-closed doctrine, threat classes, security-review triggers | `/alaa-security-review` |
| Timeout shape, retry legality, backoff, circuit breakers, degrade doctrine | `/alaa-reliability-sla` |
| Object-level relations, tuple modelling, OpenFGA model design | vendored `openfga`; `/alaa-services-contract` `references/26-request-time-authorization-openfga.md` |
| Cursor shape, signing, and what a cursor binds | `/alaa-keyset-pagination` |
| HAProxy directives, ACL syntax, SPOE and Lua mechanics | `/alaa-haproxy`, `/alaa-haproxy-lua` |
| Laravel middleware, guard, policy and DTO shape; PHP code shape; Octane request state | `/alaa-laravel-architecture`, `/alaa-php-clean-code`, `/alaa-octane-performance` |
| Telemetry requirement levels and gates; exposure and trusted-proxy delivery | `/alaa-observability-soc`, `/alaa-docker-production`, `/caas-arvan-kuber` |

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

**2026-10-21 user identity policy source.** Auth's existing `users.uuidv7` is the canonical public user ID;
verified JWT `sub` projects to the existing `X-User-Id`. The policy is owned by
`alaa-services-contract` references `25` and `22`. This dated ruling does not verify gateway or consumer
runtime adoption; inspect owning repositories and rendered configuration before making runtime claims.

| Fact | Verified on | Where |
|---|---|---|
| Gateway verifies the TOTP proof and never blocks; injects three headers only on full validity | 2026-07-27 | gateway `charts/gateway/templates/configmap.yaml:487-583`, `docs/totp-proof-gateway-contract.md:9,51` |
| The three backend-only `X-TOTP-*` names are on the sanitize list, plus a Lua wildcard sweep sparing `X-TOTP-Proof` | 2026-07-27 | gateway `charts/gateway/values.yaml:207-209`, `configmap.yaml:250-254`, `haproxy/lua/authz-sidecar.lua:487-494` |
| Gateway turns a `0` location sentinel and an empty name sentinel into an absent header; `authz-sidecar` refuses an absent `X-Location-*` header before any OpenFGA call | gateway 2026-11-14, authz-sidecar 2026-11-09 | gateway `<repo>/charts/gateway/templates/configmap.yaml`, the `jwt_claim_positive_*` rules; authz-sidecar `<repo>/internal/decision/location.go:82-137`, `<repo>/internal/decision/engine.go:311-313` |
| `X-Location-*` is a decimal integer and `X-User-Id` and `X-Project-Id` are UUIDv7 text; Crockford appears only in OpenFGA object ids, built by `authz-sidecar` and also by the gateway Lua for `X-Authz-Canonical-Object-Id` | 2026-11-11 | gateway `<repo>/charts/gateway/values.yaml:155-169`, `<repo>/haproxy/lua/authz-sidecar.lua:742-757,923-924`; authz-sidecar `<repo>/internal/decision/codec.go:13-37`, `<repo>/internal/decision/principal.go:24-36`, `<repo>/internal/decision/geography_codec.go:65-78` |
| The proof is not single-use and there is no replay table | 2026-07-27 | gateway `docs/totp-proof-gateway-contract.md:52` |
| Auth enforces `require_totp` against its local proof record and `gateway_step_up` against the three `X-TOTP-*` headers; both bind the proof to the active TOTP credential in auth's Redis, so a disable or reset voids it at once on auth routes only | 2026-10-20 | auth `app/Http/Middleware/RequireTotpMiddleware.php`, `app/Http/Middleware/RequireGatewayStepUpProof.php`, `app/Support/Auth/TotpProofBindingVerifier.php` |
| Permission catalog held 130 active permissions, highest bitmap id 130, contiguous from 1 | 2026-07-27 | `alaa-permission-catalog` `catalog/permissions.json` |
| No occurrence of `BYPASS_GATEWAY_PROOF` in the gateway repository's charts, HAProxy assets or docs, nor in auth | 2026-07-27 | case-insensitive search; see `references/30-fail-closed-cases.md` case 8 |
| `X-Project-Id` is injected from the verified `pid` claim whenever the request carried a token the gateway verified, and that holds whether or not the route required authentication | 2026-11-14 | maintainer ruling of 2026-07-31; in gateway source at `0ffc1e5` (`txn.jwt_accepted` gates every injection, `<repo>/charts/gateway/templates/configmap.yaml`). **Not confirmed against the deployed gateway.** Establish the deployed behaviour before acting on this row |
| Every public path takes an optional bearer; a failing one is dropped with no error and no injection; the public lists are the same in every profile | 2026-11-14 | owner ruling of 2026-11-14, recorded in `references/10-verification-and-ingress.md`; gateway local commits `0ffc1e5`, `df5ba2d`, `52f9edd` (Beads `alaa-ev2pd`), `<repo>/docs/BIG_PICTURE.md`. **Deployment not confirmed** |
| The gateway keeps `Authorization` on a public path and deletes it only on a protected one | 2026-11-14 | gateway `<repo>/docs/BIG_PICTURE.md`, `<repo>/docs/readme/70-security-and-auth-contract.md`. Observed gateway behaviour, not an owner ruling |
| Dropped-bearer marker on a public-path response | 2026-11-14 | owner ruling of 2026-11-14. **Decided, not shipped:** uncommitted in the gateway checkout on that date (Beads `alaa-q23xo`). That draft deletes a backend copy on every public-path response, auth's public routes included, as the ruling requires |
| WA ingest: tenant from `X-Project-Id` when present, else from the envelope project; user id only from `X-User-Id`; trusted user and scope discarded on a guest batch | 2026-11-14 | owner ruling of 2026-11-14; wa `<repo>/docs/DECISIONS.md` decision 35, `<repo>/vector/wa-vector.yaml` at `7c21e51` and `8c64286`. **Deployment not confirmed** |
| A request carrying no accepted bearer carries its project id in the request body as `project_id`, sourced from the client's `PROJECT_ID` configuration; the gateway injects no header and reads no body, and the receiving service rejects a body that carries none, except WA ingest, which reads its own envelope field and discards | 2026-07-31 | maintainer ruling, ratified and recorded in `references/10-verification-and-ingress.md`. **Not confirmed against any deployed service.** Establish what the receiving service does today before acting on this row. The matching client-side rule is `alaa-services-contract references/60-frontend-sdk-consumption-contract.md` |
| A tokenless request that has no body carries its project id as a `project_id` query parameter, and a route may scope a read by that value only while it is on the receiving service's explicit read list | 2026-07-31 | maintainer ruling, ratified and recorded in `references/10-verification-and-ingress.md`. Gateway side confirmed in the rendered template: no query-string fetch, `path` matching, `set-path` prefix stripping. **Service side confirmed nowhere.** Establish what the receiving service does today before acting on this row |
| The gateway verifies access JWTs with no revocation lookup, sets `X-Access-Token-Id` from `jti` and deletes any client copy; auth's live-token guard refuses a missing, unknown, revoked or expired token with `401 SESSION_EXPIRED` | 2026-10-20 | gateway `snapshots/alaa-service.haproxy.cfg:226,920` (case-insensitive `revok` absent from it and from `haproxy/`); auth `app/Http/Middleware/RejectRevokedAccessToken.php`, `routes/api.php:59-110` |
| Client address policy: no rate limit by client IP; gateway derives a best-guess address | 2026-11-13 | owner decision, gateway Beads `alaa-2nv79`; rules in `alaa-services-contract references/22-failure-load-and-deprecation-contract.md` and `references/30-trusted-ingress-and-laravel-contract.md`. Gateway implementation confirmed in gateway merge `823e53a` (`<repo>/CHANGELOG.md` Unreleased, `<repo>/docs/BIG_PICTURE.md`) |
| Access-token lifetime is `ACCESS_TOKEN_TTL_MINUTES`, default 15, env-controlled; the owner may lower it to 1 minute in production or raise it under load | 2026-10-20 | auth `config/auth.php:46`; owner ruling of 2026-10-20 |
| TOTP enroll and confirm need an SMS-OTP login younger than `AUTH_TOTP_ENROLL_FRESH_LOGIN_SECONDS` (default 600), dated by the refresh-token family ULID | 2026-10-20 | auth `app/Http/Middleware/RequireFreshTotpEnrollmentLogin.php`, `config/auth.php:120` |

Undated facts predate this table; re-derive them before acting.

## A domain-bounded example

**Good.** `X-Project-Id` behaviour is changing, so inspect the `pid` producer in
auth, the gateway's injection and sanitize blocks, the downstream middleware, the
docs and the Postman examples, and change them together.

**Bad.** A downstream service's local numeric project fixture is taken as evidence
that a client may choose tenant context directly. It is a migration fixture in a
backend-only test path.
