# Source Map

Read before relying on any version-sensitive claim, advisory, standard, or framework behaviour in a review.

## What this skill does not own

`SKILL.md` *What this skill does not own* keeps the rules that bind every review. This section names each owner and what this skill keeps.

- `/alaa-trust-gateway-auth` owns how *this platform's* tokens and trusted headers are issued, verified, projected, and stripped: the claim set, the header names, the gateway configuration, key distribution. This skill owns the review questions that apply to *any* token system, plus the negative tests in `50-credentials-and-cryptography.md`. Read that skill to learn what this platform's credentials contain. The rules for judging a credential system live here. Every one of them binds a service that has never read it.
- `/alaa-reliability-sla` owns availability-side failure behaviour, as split under the fail-closed doctrine in `SKILL.md`.
- `/alaa-services-contract` owns the wire contracts these invariants instantiate - header names, decision codes, endpoint categories, route registration, permission catalogs. Where a rule here and a contract there describe the same control, that file owns the wire and this file owns the invariant.
- `/alaa-minio-object-storage` owns the object store's own posture: what a bucket policy may grant, how a storage identity is scoped and rotated, which transport carries the bytes, and how long a presigned URL may live. Read it when reviewing a bucket policy, a storage identity, a plaintext hop to an object store, or a presigned URL's lifetime. That skill owns the value the review measures against. This skill owns the verdict.
- `/alaa-observability-soc` owns what a security event contains and how it reaches a SOC. This skill names *that* an event is required at a decision point; its shape is owned there.
- `/alaa-prompting-guide` owns model and effort capability evidence and runtime mechanics; the runtime orchestrator owns actual task allocation for every authority role.
- Report length and noise discipline belong to `/alaa-low-noise`; they are not security decisions and never justify dropping an item.

## Source priority

1. **Target repository truth**: authentication and authorization code, middleware, policies, the permission map, validation schemas, migrations, configuration and its boot validator, tests, deployment manifests, and the repository's current security documentation. Where implementation and documentation disagree, the implementation is what runs - report the drift as a finding and align the documentation before closing.
2. **Companion skills for the boundary in scope**: `/alaa-trust-gateway-auth`, `/alaa-services-contract`, `/alaa-observability-soc`, `/alaa-reliability-sla`, `/alaa-docker-production`, and the stack-specific skills.
3. **Official or primary security sources**:
   - OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
   - OWASP Top 10: https://owasp.org/www-project-top-ten/
   - OWASP API Security Top 10: https://owasp.org/www-project-api-security/
   - OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
   - OAuth 2.0 Security Best Current Practice: https://datatracker.ietf.org/doc/html/rfc9700
   - JWT Best Current Practices: https://datatracker.ietf.org/doc/html/rfc8725
   - NIST Digital Identity Guidelines: https://pages.nist.gov/800-63-4/
   - NVD: https://nvd.nist.gov/
   - GitHub Security Advisories: https://github.com/advisories
   - The framework's or library's own security documentation, for anything about its defaults.
4. **Community posts, answers, exploit write-ups, and blog articles**: usable for reproduction technique and impact research only. They never override a primary standard or repository evidence, and a cost or parameter value taken from one is unverified until checked against the primary source and the target hardware.

## Freshness triggers

Re-check primary sources and advisories when the task mentions: latest, CVE, advisory, exploit, zero-day, dependency upgrade, current best practice, compliance, OAuth, OIDC, JWT, MFA, TOTP, session, refresh token, tenant isolation, SSRF, upload, deserialization, sanitiser, CSP, cookie attribute, constant-time, Argon2, bcrypt, key rotation, secret, or container hardening.

Also re-check when a framework or package version changes anything about authentication, validation, serialisation, template rendering, encryption, hashing, cookies, CORS, CSRF, rate limiting, or HTTP-client redirect and DNS behaviour - a client library's default redirect policy is a control in `30-outbound-fetch-and-files.md`, and defaults move between major versions.

## What a finding must contain

A finding names the route or consumer, the actor who can reach it, the value the actor controls, the control that failed, the file, the impact, and the smallest fix that preserves the repository's architecture. "OWASP says this is risky" with no reachable path attached is not a finding, and reporting it as one spends the reader's trust on nothing.
