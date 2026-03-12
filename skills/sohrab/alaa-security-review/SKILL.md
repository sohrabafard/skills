---
name: alaa-security-review
description: "Security review gate + deep review: trust boundaries, tenant isolation, authn/authz (incl. JWT/OAuth), validation/injection, secrets/tokens, abuse controls, deps/container hygiene, and prioritized remediation."
---

# Purpose
Perform a security-focused review that results in concrete, testable remediation steps.

This skill has two modes:
1) Fast Gate (high-signal checklist before shipping)
2) Deep Review (threat modeling + deployment hardening + prioritized remediation)

Use Fast Gate by default. Escalate to Deep Review for high-risk changes.

# When to use
- Any authn/authz change (JWT, sessions, permissions, service-to-service auth)
- Any DB query change that could cross tenant boundaries
- Any new endpoint, webhook, or background consumer
- Any file upload/download, URL fetching, or external integration
- Before shipping a substantial change
- After incidents, to prevent recurrence

# Constraints
- Do not add new third-party security products unless explicitly requested.
- Prefer minimal, auditable fixes (avoid broad refactors).
- Never commit secrets. Never log raw tokens.
- If the repo already has a security/error contract, preserve it.

# Fast Gate (default) — quick, practical, high-signal
Run these checks and report PASS/FAIL.

## 1) Trust boundaries (2 minutes)
- What are the inputs? (request body, headers, query params, events, queue payloads)
- What do we trust? (authenticated user, verified tenant context)
- Where can data cross tenants? (any read/write path)

## 2) Authn/authz (tenant-aware)
- Authentication: is the caller correctly authenticated for this route/consumer?
- Authorization: is the action authorized with tenant-aware Policies/Gates?
- Least privilege: service accounts/scoped tokens cannot do more than needed.
- Tenant isolation: every read/write is tenant-scoped, and tenant context is server-derived (never trust client fields blindly).

### JWT quick checks (apply when JWT is used)
- Signature verified; algorithm is pinned (no algorithm confusion, no `alg=none`).
- Algorithm/key compatibility is enforced:
    - reject HMAC tokens when expecting asymmetric keys (and vice versa)
    - reject tokens whose `alg` is not in the allowlist
- `kid` handling is safe:
    - `kid` is treated as an identifier only, never a URL/file path
    - `kid` must resolve to a pre-configured key set (no kid-driven remote fetch)
- Claims validated (at minimum):
    - `iss`, `aud`, `sub`
    - `exp` (expired tokens rejected)
    - `nbf` / `iat` (clock-skew handling defined)
- Access tokens are short-lived (minutes), not hours/days; session continuity uses refresh tokens.
- Tenant boundary claim (e.g., `tid`) rules:
    - `tid` is validated AND never trusted blindly for authorization.
    - server-derived tenant context must match or be verified against server-side permissions.
- Tokens are never logged. If correlation is needed, log only `jti` or a short fingerprint (hash).
- Errors must not leak verification internals (no stack traces; no detailed key/issuer mismatch in client payloads unless policy allows).

### OAuth/OIDC quick checks (apply when OAuth/OIDC is used)
If the service participates in OAuth/OIDC flows (client or resource server):
- Prefer Authorization Code + PKCE (avoid implicit flow).
- Validate redirect URIs strictly (exact match against registered set).
- Enforce `state` (CSRF) and `nonce` (OIDC) where applicable.
- For resource servers: validate `iss`/`aud` and accepted signing algorithms; do not accept tokens from untrusted issuers.

## 3) Injection & validation
- SQL injection: parameterized queries; no string concat in SQL.
- NoSQL injection (if applicable): sanitize operators; do not pass raw user filters to query builders.
- Validation: Form Requests for all write endpoints; normalize inputs.

## 4) Secrets & tokens
- No secrets in code/config committed to git.
- Tokens are not logged; if correlation is needed, log only `jti` or a hash/fingerprint.
- Errors returned to clients do not leak internals (no stack traces).

## 5) Rate limiting & abuse controls
- Rate limit brute-forceable endpoints (login, token refresh, SMS/email, OTP, invite links).
- Consider per-tenant and per-user limits.
- Add protections for expensive endpoints (search, export, large aggregates).

## 6) Data protection
- Do not expose internal IDs unless explicitly intended; prefer `public_id`.
- Minimize PII exposure; mask/redact in logs.
- Ensure safe error messages and stable internal error codes where used.

## 7) Dependencies & container hygiene
- New deps must be OSS/free; do a quick license sanity check.
- Run Composer security checks if available in the repo/tooling.
- If Docker image changes are part of the release pipeline, run an OSS scanner per existing CI policy.

# “Stop the line” findings (must fix before merge)
- Any path that can read/write cross-tenant data (BOLA/IDOR risk)
- Missing authz checks on privileged actions
- Token/secret leakage in logs or responses
- JWT verifier accepts `alg=none` or does not pin algorithms / allowlist
- Missing `iss`/`aud` validation where required
- Unsafe `kid` handling (kid-driven remote fetch, path traversal, unbounded key lookup)
- Long-lived access tokens without refresh rotation/revocation strategy
- Refresh tokens stored insecurely (plaintext DB, browser localStorage) or without rotation/revocation
- Refresh-token replay is not handled (no family/session invalidation on reuse)
- Trusting tenant claims (e.g., `tid`) without server-side verification
- Unvalidated user-controlled URLs leading to SSRF
- Unsafe file upload handling (missing type/size checks; no isolation; unsafe content serving)
- Broken access control on webhooks/consumers (accepting unauthenticated or unverified payloads)

# Deep Review (escalate when risk is high)
Escalate to Deep Review for:
- auth systems (JWT/session/OAuth), tenant boundaries, file/URL handling, payment-like flows, admin/moderator actions
- new integrations/webhooks/consumers
- changes that alter trust boundaries or data exposure

## 1) Identify trust boundaries & data flows
- Map components and trust zones briefly.
- List “entry points” and “sinks” (DB writes, external calls, file stores).

## 2) Threat modeling (pragmatic)
Cover at minimum:
- authn/authz bypass (BOLA/IDOR, privilege escalation)
- injection (SQL/command/template)
- SSRF and unsafe URL fetching
- unsafe file handling / content-type confusion
- replay attacks / idempotency failures (queues/webhooks/tokens)
- rate-limit bypass and abuse scenarios
- sensitive data leakage (logs/errors/metrics)

## 3) JWT/OAuth design review (when applicable)

### Key management (JWT)
- Prefer asymmetric signing for distributed verification across services.
- Keys must be stored outside the repo (secret mounts / secret manager).
- Rotation expectations:
    - support `kid`
    - allow overlap during rotation
    - pin algorithms and accepted issuers/audiences
- JWKS fetching rules (if used):
    - fetch only from pre-configured issuer metadata, never from token headers
    - cache with bounded TTL and fail closed on unexpected issuer/key set changes

### Claim strategy (JWT)
Define mandatory claims and validation rules:
- `iss`, `aud`, `sub`, `exp`, `nbf`, `iat`
- define clock-skew policy (acceptable drift window)
  Tenant claim (e.g., `tid`) rules:
- must match server-derived tenant context OR be verified against server-side permissions
- never authorize cross-tenant access based on a client-supplied claim alone

### Access token
- Lifetime: short (minutes).
- Contents: minimal; avoid PII.

### Refresh tokens (recommended)
- Use rotation: each refresh issues a new refresh token and revokes the old one.
- Store refresh tokens server-side hashed (like passwords), keyed by `jti`.
- Track: `replaced_by_jti`, `revoked_at`, `expires_at`.
- Optional metadata (privacy-aware): `ip_hash`, `ua_hash`, device/session identifiers if useful.

Refresh replay response (mandatory when rotation exists):
- If a previously-used refresh token is presented again:
    - treat as replay/compromise signal
    - revoke the entire token family/session (and optionally user sessions per policy)
    - require re-authentication
    - emit a security event for SOC detection

### Revocation strategy
- Redis (optional) for fast revocation cache and hot denies.
- DB for durable session state (recommended).

### Sender-constrained options (optional; evaluate)
Where applicable and justified, evaluate sender-constrained tokens to reduce replay risk:
- DPoP-style proof-of-possession
- mTLS-bound tokens
  Only recommend these if the environment supports them; otherwise keep as future-hardening.

### OAuth 2.0 security posture (when OAuth flows exist)
- Prefer Authorization Code + PKCE for public clients.
- Do not use implicit flow.
- Validate redirect URIs strictly; enforce `state` and (OIDC) `nonce`.
- For refresh tokens: rotate + detect replay; define lifetime policy.
- Ensure correct audience/scopes for resource servers (least privilege).

### Testing (minimum)
- Verifier unit tests: invalid signature, wrong `iss/aud`, expired `exp`, future `nbf`.
- Refresh rotation tests: reuse of old refresh fails; replay triggers family/session revocation.
- Multi-tenant tests: tenant A token cannot access tenant B resources.
- `kid` tests: unknown kid fails closed; no remote fetch triggered by kid.

## 4) Deployment hardening review
- TLS termination assumptions, trusted proxy headers, CORS/CSRF where applicable
- container permissions (non-root, read-only FS where possible)
- secret handling (env/secret manager; rotation expectations)
- network exposure (only edge is public; DB/Redis/broker are private)
- safe defaults for debug flags and error reporting

## 5) Output a prioritized remediation list (P0/P1/P2)
For each item include:
- impact/risk
- exact file(s) to change
- specific remediation steps
- how to validate (tests/commands or manual verification)

# Output contract
Always output in this order:
1) `Findings:` bullet list (or “None”)
2) `Stop-the-line:` list (or “None”)
3) `Required fixes:` (P0/P1/P2 if Deep Review; otherwise short list)
4) `Validation:` exact checks/commands and expected outcomes
5) If no issues: **PASS** + what was checked

# Anti-patterns
- Vague recommendations without mapping to code/config files.
- “Rewrite everything for security.”
- Adding new security products/tools without a request or existing policy.
- Logging secrets/tokens/PII.
- Accepting JWT algorithms dynamically (algorithm confusion).
- Unsafe `kid` handling.
- Long-lived access tokens without rotation/revocation.
- Storing refresh tokens in plaintext or in browser localStorage.
- Trusting tenant claims without server-side verification.
