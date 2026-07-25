# Source Map

Read before relying on any version-sensitive claim, advisory, standard, or framework behaviour in a review.

Companion skills are written `/name`; under Codex the same skill is `$name`.

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
