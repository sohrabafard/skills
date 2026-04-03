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

# Runtime mode split & ownership
- Keep primary orchestrator-specific production guidance in the platform-owned skill for that environment.
- Use this skill for the Docker runtime contract across single-host Compose and multi-node Swarm.
- When a repository supports both Docker modes, prefer one explicit wrapper entrypoint such as `scripts/docker/up-local.sh <compose|swarm>`.
- Allow extra aliases such as `dev` or `prod` only when they resolve to an explicit mode and remain documented.
- Fail fast when a requested runtime mode is unsupported instead of silently falling back to another mode.

# Delivery wrapper contract
- Centralize Docker runtime bootstrap in one wrapper instead of scattering repeated manual commands across docs.
- The wrapper should create or reuse shared networks and shared infra only through idempotent steps.
- Validate the rendered Compose model before `docker compose up` or `docker stack deploy`.
- Render any templated configs before deploy and validate them when the runtime supports validation.
- Compose mode may build locally when the repo allows it.
- Swarm mode should prefer prebuilt immutable images and rendered stack files rather than building during deploy.
- Keep wrapper output operational: show selected mode, project or stack name, target image tag, and any required secret or bootstrap prechecks.

# Shared-network & shared-infra pattern
- When services must discover each other across repositories, standardize one shared Docker network name and reuse it across the family.
- When multiple services reuse the same Postgres, Redis, RabbitMQ, ClickHouse, or similar runtime infra, standardize one shared infra identity and reuse it instead of cloning isolated copies by default.
- Create shared primitives if missing only through safe, repeatable bootstrap logic.
- Keep service-owned databases, schemas, users, and grants separate even when infra is shared.
- Ala's concrete example is `alaa-shared-network` plus `alaa-shared-infra`; other systems may use different names but should keep the same stability rule.

# Stable DNS and load-balancing pattern
- Give each HTTP-serving backend one stable internal DNS target and make proxies or upstream callers use that target instead of container instance names.
- In Swarm, prefer service DNS plus VIP semantics such as `endpoint_mode: vip` for HTTP backends that need stable load balancing.
- When a repo uses a multi-service app layout, reserve the canonical alias for the HTTP-serving app service rather than workers or schedulers.
- For PHP/Laravel deployments, a common pattern is service key `platform-app-php` with alias `<service>-platform-app-php`.
- Do not couple HAProxy, Nginx, or another reverse proxy to task IDs, replica names, or node IP lists when stable service DNS is available.

# Registry strategy
- Route public upstream pulls through a configurable pull-through mirror when your environment provides one.
- Keep the mirror configurable through env or build args rather than hardcoded in many files.
- Ala's current normalized default example is `mirror.cdn.ir`.
- Keep first-party images and OCI artifacts in a private registry path and authenticate explicitly in CI and production runtimes.
- Distinguish public-mirror variables from private-registry variables so operators can rotate them independently.
- Do not bake registry credentials into images or committed files.

# Secret and key-material handling
- Generate, sync, or provision runtime secrets before deploy instead of copying them by hand.
- In Compose, use mounted files or equivalent runtime materialization with restrictive permissions.
- In Swarm, prefer external secrets with explicit ownership and file mode when the runtime supports it.
- Keep public-key consumers read-only; only the owning service should manage the corresponding private key.
- Validate secret presence and permissions before starting the main workload.

# PHP/Laravel + Octane/Swoole notes
- Ensure required extensions are installed (as needed by the repo): `swoole`, `pdo_pgsql`, `redis`, etc.
- Separate build-time tools (composer, node) from runtime.
- Use OPcache settings appropriate for long-lived workers.
- Healthchecks should be lightweight and must not depend on heavy DB queries.

# Exposure rules
- Only edge proxies are publicly exposed.
- App containers stay on an internal network.
- Document trust boundaries and headers such as `X-Forwarded-*`, `X-Request-Id`, and `traceparent`.
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
2) Runtime settings (mode, ports, user, volumes, env, healthchecks, secrets)
3) Determinism notes:
    - what is pinned and why (including any digest pinning decisions)
    - what remains floating and why (if anything)
4) Service-discovery and infra notes:
    - shared network and shared infra assumptions
    - canonical DNS aliases or VIP behavior
    - registry mirror versus private-registry paths
5) Optional release evidence notes (only if policy allows):
    - which CI artifacts should be produced (SBOM/scan)
    - how to record deployed digests
6) Any rollout notes (restart strategy, zero-downtime considerations, Compose-versus-Swarm differences)

# Anti-patterns
- Running everything as root
- Publishing DB/broker ports publicly
- Baking secrets into images
- Huge base images with unnecessary build tooling
- Using floating tags without pinning for releases (non-deterministic builds)
- Healthchecks that perform expensive DB queries or mutate state
- Proxying to container instance names when stable service DNS is available
- Building Swarm images ad hoc during deploy when immutable prebuilt images are expected
