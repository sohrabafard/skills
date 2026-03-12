---
name: alaa-cicd-laravel-postgres
description: "CI/CD for Laravel + Postgres: deterministic pipelines, pinned service containers, stable migration/test bootstrap, caching, quality gates (Pint/PHPStan/tests), flaky-test controls, and optional supply-chain artifacts (SBOM/scan) per policy."
---

# Purpose
Make CI fast, reliable, and aligned with how the service runs in production.

# When to use
- Editing GitHub Actions or GitLab CI configs
- Changing DB services, migrations, or test DB setup
- Updating build/test stages, caching, or artifacts
- Adjusting Docker build usage in CI
- CI failures or flakiness related to Postgres/migrations

# When NOT to use
- Local dev setup only
- Documentation-only changes
- Feature work without CI impact

# Determinism rules (mandatory)
- Pin service container images (especially Postgres) to a specific major/minor (avoid floating tags).
- Ensure `APP_ENV=test` and stable test configuration (explicit env vars; no magic CI-only behavior).
- Fix timezone/locale assumptions:
    - Prefer `TZ=UTC` in CI unless the repo explicitly requires a different timezone.
- Key dependency caches by lockfile hash + runtime version (PHP/Composer/toolchain) to avoid stale or cross-version cache poisoning.
- Avoid non-deterministic seeds and ordering:
    - deterministic fixtures
    - explicit ordering where required
- Avoid external network calls in tests unless explicitly required (and documented).
- If parallelism is enabled:
    - isolate DB/schema per worker or per job to avoid race conditions.

# Step-by-step workflow (deterministic)
1) Identify pipeline files and current conventions
    - Check `.github/workflows/*`, `.gitlab-ci.yml`, and docs
    - Note PHP version, required extensions, and Composer caching strategy
2) Validate DB service configuration
    - Use a Postgres service image that matches production major version (pin it)
    - Add basic health checks and wait-for-db logic
    - Confirm correct `DB_*` env and test database names
3) Ensure test bootstrap is stable
    - Run migrations before tests (e.g., `php artisan migrate --force`)
    - Set `APP_KEY`, `APP_ENV=test`, and safe `CACHE/QUEUE` drivers
    - Avoid parallel jobs racing on the same database unless isolated
4) Keep CI fast and deterministic
    - Cache Composer downloads safely (prefer dependency download cache, not vendor/ unless policy allows)
    - Keep artifacts useful (failed migration output, test logs)
5) Flaky-test controls (recommended)
    - isolate time (TZ=UTC; control “now” in tests where needed)
    - avoid relying on test order; ensure tests are independent
    - avoid shared mutable state across tests

# CI design rules (baseline)
- Cache Composer dependencies safely.
- Run: format/lint → static analysis → tests.
- Use a Postgres service container; run migrations before tests.
- Keep env vars explicit and documented (avoid magic CI-only behavior).

# Optional supply-chain artifacts (P2; only if requested or policy already exists)
If your CI policy allows:
- SBOM generation (dependencies and/or built image)
- Vulnerability scanning of images/deps
- Store SBOM/scan output as CI artifacts for later audit
- Fail build only based on an explicit severity policy (do not invent policy)

# When to stop and ask
- If pipeline changes require credentials or registry tokens
- If deployment steps would change production infrastructure
- If CI failures are caused by external service outages
- If asked to enforce “fail-on-vuln” without a defined policy

# Output contract
When applying this skill, output:
1) Summary of pipeline changes + rationale
2) Which CI stages were affected and why
3) Exact commands executed in CI and expected outcomes
4) Determinism/flaky-test notes (what you changed to reduce flakiness)
5) Optional supply-chain artifacts (what to add if policy allows)
6) Remaining CI risks or follow-up actions

# Anti-patterns
- CI using a different DB engine than production without explicit reason
- Magic env vars not documented anywhere
- Flaky tests due to unordered seed data or time dependencies
- Using unpinned service images or floating tags (non-deterministic CI)
- Failing builds on vulnerabilities without an agreed severity policy
