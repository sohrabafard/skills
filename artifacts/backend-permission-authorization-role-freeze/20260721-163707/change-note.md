# Backend permission authorization and role freeze

Timestamp: `2026-07-21 16:37:07 Asia/Tehran`

## Decision recorded

- Ala backend services use catalog-owned permission bits from trusted `X-Access` for coarse access decisions.
- Contract-defined OpenFGA checks remain authoritative where resource-level authorization applies.
- User roles remain non-authoritative passive metadata until `alaa-services-contract` explicitly finalizes and activates backend role semantics.
- No new backend role resolver, role-to-permission mapping, role-derived fallback, policy, scope, response, route, validation, feature, workflow, or side-effect decision is allowed during the freeze.
- Optional role retention is limited to documented observability or future-migration use and must remain isolated from authorization.

## Validation target

The top-level router, topic map, focused references, Laravel copy baseline, review checklist, and merged full guide must expose the same decision without contradictory role-derived backend guidance.

## Validation result

- `skill-creator/scripts/quick_validate.py`: passed for `alaa-services-contract`.
- Merged-guide containment: passed for the changed end-to-end, role-freeze, trusted-ingress, permission-catalog, checklist, and Laravel-baseline references.
- Stale baseline scan: no optional role-derivation helper, service-local derived-role baseline, or `TrustedActorContext::$role` remains in this skill.
- `git diff --check`: passed; Git reported only the repository's expected LF-to-CRLF working-copy warnings.
- Repository-wide `scripts/validate_sohrab_skill_pack.py`: still reports unrelated pre-existing failures in other skill folders; it reports no error for `alaa-services-contract`.
