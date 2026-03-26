# Purpose
Ship production-grade container configs that are secure, observable, and operable, with deterministic builds and minimal attack surface.

This skill also introduces **release evidence guardrails** (optional, policy-driven):
- record deployed image digests
- generate SBOM / vulnerability scan artifacts in CI (only if your policy allows)

# When to use
- Creating or refactoring Dockerfiles
- Hardening container runtime settings
- Building multi-stage images for release
- Reducing image size and attack surface
- Docker/Compose changes, deployment docs, zero-downtime rollout guidance
- Introducing deterministic pinning and release evidence conventions (policy-driven)

# Defaults (unless repo contradicts)
- Multi-stage builds (builder → runtime).
- Deterministic pinning:
    - Pin runtime base images by major/minor at minimum.
    - Prefer digest pinning for **production releases** (not necessarily for local dev).
    - Do not “float” critical service images (DB/broker/proxy) in production environments.
- Non-root runtime user; least privilege.
- Keep images minimal; only runtime deps in final stage.
- Deterministic builds:
    - enforce lockfiles (`composer.lock`, and `package-lock.json`/`yarn.lock`/`pnpm-lock.yaml` if applicable)
    - avoid network calls during runtime image build except dependency installs
- Read-only filesystem where possible; explicit writable volumes only.
- Healthcheck for every service.
- Secrets via env/secret manager; never committed and never baked into images.

# PHP/Laravel + Octane/Swoole notes
- Ensure required extensions are installed (as needed by the repo): `swoole`, `pdo_pgsql`, `redis`, etc.
- Separate build-time tools (composer, node) from runtime.
- Use OPcache settings appropriate for long-lived workers.
- Healthchecks should be lightweight and must not depend on heavy DB queries.

# Exposure rules
- Only edge proxies are publicly exposed.
- App containers stay on an internal network.
- Document trust boundaries and headers (X-Forwarded-*, correlation IDs).
- Do not publish DB/broker ports publicly in production Compose.

# Security hardening checklist
- Run as non-root.
- Drop Linux capabilities unless explicitly required.
- Prefer an explicit capability baseline (e.g., `cap_drop: [ALL]`) and add back only what is proven necessary.
- Set `no-new-privileges` where supported by the runtime/orchestrator.
- Prefer read-only filesystem; allow writable tmp/cache dirs explicitly.
- No secrets in images; mount via env/secret files.
- Restrict outbound network access where feasible (environment-dependent).
- Prefer OSS scanners in CI (e.g., Trivy) and fail on critical issues **only** if policy requires.

# Deterministic releases & “release evidence” (optional, policy-driven)
If your CI/release policy allows, prefer:
- Recording the exact **image digest** deployed (and where it was deployed).
- Generating an SBOM artifact (image or dependency SBOM) and storing it as a CI artifact.
- Generating a vulnerability scan report and storing it as a CI artifact.
- Keeping a short “release manifest” note (version/tag → digest → environment).

Rules:
- Do not invent policy. If no severity policy exists, do not fail builds by default.
- Do not introduce paid SaaS tooling unless explicitly requested.

# OS tuning (reference-level)
- Surface `nofile` ulimit and relevant sysctls when high-load is required.
- Keep changes minimal and documented (one change at a time).

# Output contract
When making changes, output:
1) Dockerfile(s) and rationale (what changed and why)
2) Runtime settings (ports, user, volumes, env, healthchecks)
3) Determinism notes:
    - what is pinned and why (including any digest pinning decisions)
    - what remains floating and why (if anything)
4) Optional release evidence notes (only if policy allows):
    - which CI artifacts should be produced (SBOM/scan)
    - how to record deployed digests
5) Any rollout notes (restart strategy, zero-downtime considerations)

# Anti-patterns
- Running everything as root
- Publishing DB/broker ports publicly
- Baking secrets into images
- Huge base images with unnecessary build tooling
- Using floating tags without pinning for releases (non-deterministic builds)
- Healthchecks that perform expensive DB queries or mutate state
