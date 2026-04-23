# Source Map

Use this file when gateway trust guidance depends on standards, current gateway/auth repo behavior, or current authorization-runtime behavior.

## Source priority

1. Current Ala repositories: gateway config/templates, auth routes/controllers/services/tests, entitlement-platform model/runtime docs, service-local middleware, Postman artifacts, and current docs.
2. This skill's split references and `$alaa-services-contract` for platform-wide service boundaries.
3. Official or primary standards and product docs:
   - JWT: https://datatracker.ietf.org/doc/html/rfc7519
   - JWT Best Current Practices: https://datatracker.ietf.org/doc/html/rfc8725
   - OAuth 2.0 Bearer Token Usage: https://datatracker.ietf.org/doc/html/rfc6750
   - OAuth 2.0 Security Best Current Practice: https://datatracker.ietf.org/doc/html/rfc9700
   - OpenFGA docs: https://openfga.dev/docs/
   - HAProxy docs: https://www.haproxy.com/documentation/
   - Laravel docs: https://laravel.com/docs
4. Community examples, StackOverflow answers, or copied snippets only for troubleshooting an observed error after repo truth and primary docs are checked.

## Freshness triggers

Re-check current repos and official docs when the task mentions:

- latest/current gateway behavior, JWT claim changes, token refresh, trusted headers, tenant/project naming, or auth-service v3 route shape
- HAProxy ACL order, JWT verification, SPOE/SPOA, OpenFGA model changes, or `authz-sidecar`/`entitlement-spoa`
- security updates, key rotation, accepted algorithms, token lifetimes, replay handling, or public/protected route changes

## Domain-bounded example

Good: when `X-Project-Id` behavior changes, inspect the JWT `pid` producer, gateway header injection, downstream middleware, docs, and Postman examples before editing one layer.

Bad: treating a downstream service's local numeric project id fixture as proof that clients may choose tenant context directly.
