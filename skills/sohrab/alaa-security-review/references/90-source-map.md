# Source Map

Use this file when a security review depends on current security guidance, dependency advisories, framework behavior, or standards.

## Source priority

1. Target repo truth: authn/authz code, middleware, policies, validation, migrations, config, tests, deployment files, logs, and current security docs.
2. Ala companion skills for the boundary in scope: `$alaa-trust-gateway-auth`, `$alaa-services-contract`, `$alaa-observability-soc`, `$alaa-docker-production`, and framework-specific skills.
3. Official or primary security sources:
   - OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
   - OWASP Top 10: https://owasp.org/www-project-top-ten/
   - OWASP API Security Top 10: https://owasp.org/www-project-api-security/
   - OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
   - OAuth 2.0 Security Best Current Practice: https://datatracker.ietf.org/doc/html/rfc9700
   - JWT Best Current Practices: https://datatracker.ietf.org/doc/html/rfc8725
   - NIST Digital Identity Guidelines: https://pages.nist.gov/800-63-4/
   - NVD: https://nvd.nist.gov/
   - GitHub Security Advisories: https://github.com/advisories
4. Community posts, StackOverflow answers, exploit writeups, or blog posts only as troubleshooting or impact research. Do not let them override primary standards or repo evidence.

## Freshness triggers

Re-check primary sources and advisories when the task mentions:

- latest, CVE, advisory, exploit, dependency upgrade, zero-day, current best practice, compliance, OAuth, JWT, OIDC, MFA, session, refresh token, tenant isolation, SSRF, upload, secret, or container hardening
- framework or package version changes that affect auth, validation, serialization, encryption, hashing, cookies, CORS, CSRF, or rate limiting

## Domain-bounded anti-pattern

Bad: "OWASP says this is risky" without mapping the finding to a reachable route, trust boundary, data asset, and testable remediation.

Good: identify the route, actor, trusted source, failing control, impact, and the smallest fix that preserves the repo's architecture.
