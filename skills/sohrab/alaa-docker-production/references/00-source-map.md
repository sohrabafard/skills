# Source map and freshness ledger

Use this file when Docker, Compose, Swarm, registry, OCI, or container security behaviour must be
current. It replaces the former `references/SOURCES.md`; the conflict-resolution order and the
community-source restriction below are carried forward unchanged.

## Freshness triggers

Re-check primary sources when the user asks for latest or current behaviour, or when the task
touches Dockerfile syntax, BuildKit or buildx behaviour, Compose or Swarm compatibility, image
provenance, registry behaviour, CVEs, Docker Desktop or Engine changes, official image behaviour, or
production hardening guidance.

**A version written into a file goes stale silently.** Every pinned value in this skill therefore
carries the command or URL that re-derives it, and the checker carries the same table:

```
node scripts/check-image-pinning.mjs --versions
```

That command is the freshness procedure. It prints every value below with its source and its
re-derivation command, and `check-image-pinning.mjs` reports `image-eol-line` when a Compose file
references a language or distribution line that has left support.

## Verification ledger — checked 2026-07-29

| Subject | Value as of 2026-07-29 | Source | Re-derive with |
|---|---|---|---|
| Docker Engine | 29.6.2, released 16 July 2026 (29.6.1 on 26 June, 29.6.0 on 18 June) | https://docs.docker.com/engine/release-notes/29/ | `docker version --format '{{.Server.Version}}'` |
| Docker Compose | v5.3.1, released 7 July 2026. v5.3.0 (2 July) added native init-container support; v5.2.0 (23 June) replaced the state-reconciliation algorithm | https://github.com/docker/compose/releases | `docker compose version` |
| Compose `version:` property | Obsolete. "Only informative"; Compose warns when present and "always uses the most recent schema to validate the Compose file, regardless of the `version` field". `name:` is current and is exposed as `COMPOSE_PROJECT_NAME` | https://docs.docker.com/reference/compose-file/version-and-name/ | Add `version: "3.8"` to a file and run `docker compose config`; the warning is the check |
| Compose interpolation forms | `${VAR:-d}`, `${VAR-d}`, `${VAR:?e}`, `${VAR?e}`, `${VAR:+a}`, `${VAR+a}`; `$$` escapes a literal `$` | https://docs.docker.com/reference/compose-file/interpolation/ | `docker compose config` on a file using each form |
| What interpolation reads | Shell environment; the file named by `--env-file`; otherwise the project `.env`. **Not** the service-level `env_file:` key | https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/ | Put a value only in a service `env_file:` and read it back with `docker compose config` |
| Dockerfile syntax frontend | `# syntax=docker/dockerfile:1` pins the stable major and makes BuildKit "pull the latest stable version of the Dockerfile syntax before the build" | https://docs.docker.com/reference/dockerfile/ | https://hub.docker.com/r/docker/dockerfile/tags |
| `RUN --mount=type=secret` | Stable, not experimental. Dockerfile `RUN --mount=type=secret,id=X[,target=…][,env=VAR]`; CLI `--secret id=X,src=…` and `--secret id=X,env=VAR`; default target `/run/secrets/<id>` | https://docs.docker.com/build/building/secrets/ | `docker build --secret id=t,env=T .` against a one-line Dockerfile |
| SBOM and provenance | "Provenance attestations with the `mode=min` level are added to images by default." Controls: `--provenance=mode=max`, `--provenance=false`, `--sbom=true`, `BUILDX_NO_DEFAULT_ATTESTATIONS` | https://docs.docker.com/build/metadata/attestations/ | `docker buildx imagetools inspect REF --format '{{json .Provenance}}'` |
| Swarm mode status | Current and supported: "Use Swarm mode if you intend to use Swarm as a production runtime environment." Docker *Classic* Swarm — a different product — "is no longer actively developed" | https://docs.docker.com/engine/swarm/ | Read the page for a deprecation banner |
| Swarm rollout defaults | `update_config.order` `stop-first`; `failure_action` `pause`; `monitor` `0s`; `rollback_config.order` `stop-first`, `failure_action` `pause`, `delay` `0s`, `monitor` `0s`, `max_failure_ratio` `0` | https://docs.docker.com/reference/compose-file/deploy/ | Deploy a service with no `update_config` and read `docker service inspect --format '{{json .Spec.UpdateConfig}}'` |
| `HEALTHCHECK` options | `--interval`, `--timeout`, `--start-period`, `--start-interval`, `--retries`. Long-established defaults 30s / 30s / 0s / 5s / 3; `--start-interval` available from Engine 25.0. `HEALTHCHECK NONE` disables any probe inherited from the base image, and Compose `test: ["NONE"]` is the equivalent | https://docs.docker.com/reference/dockerfile/ ; https://docs.docker.com/reference/compose-file/services/ | **Both pages truncate before the option table in their current published form.** Re-derive rather than quote: build an image with a bare `HEALTHCHECK CMD true` and read `docker inspect --format '{{json .Config.Healthcheck}}' IMAGE` |
| Registry mirrors | `"registry-mirrors": ["https://host"]` in `/etc/docker/daemon.json`. Documented limitation: "It's currently not possible to mirror another private registry. Only the central Hub can be mirrored." | https://docs.docker.com/docker-hub/image-library/mirror/ | `docker info --format '{{json .RegistryConfig.Mirrors}}'` |
| OCI image annotations | Predefined keys include `org.opencontainers.image.created`, `.authors`, `.url`, `.documentation`, `.source`, `.version`, `.revision`, `.vendor`, `.licenses`, `.ref.name`, `.title`, `.description`, `.base.digest`, `.base.name` | https://github.com/opencontainers/image-spec/blob/main/annotations.md | `docker inspect --format '{{json .Config.Labels}}' IMAGE` |
| `docker init` | GA, no deprecation notice. Generates `Dockerfile`, `compose.yaml`, `.dockerignore`, `README.Docker.md`. Templates: ASP.NET Core, Go, Java, Node, PHP with Apache, Python, Rust, Other. Its PHP template is Apache-based and is not a starting point for an Octane or Swoole service | https://docs.docker.com/reference/cli/docker/init/ | `docker init --help` |
| Alpine | 3.24 stable (3.24.0, 9 June 2026). Supported: 3.24 to 2028-06-01, 3.23 to 2027-11-01, 3.22 to 2027-05-01, 3.21 to 2026-11-01. 3.20 support ended 2026-04-01 | https://www.alpinelinux.org/releases/ | Read the "supported until" column |
| Debian | 13 "trixie" stable, point release 13.6 (11 July 2026). 12 "bookworm" is oldstable | https://www.debian.org/releases/ | The page names the current stable codename |
| PHP | 8.5 newest (20 Nov 2025). Active support: 8.4 to 2026-12-31, 8.5 to 2027-12-31. Security-only: 8.2 to 2026-12-31, 8.3 to 2027-12-31, 8.4 to 2028-12-31. 8.1 and older EOL | https://www.php.net/supported-versions.php | The page's two tables |
| Node.js | 24 "Krypton" Active LTS since 2025-10-28, maintenance from 2026-10-20, EOL 2028-04-30. 22 "Jod" in maintenance, EOL 2027-04-30. 26 Current since 2026-05-05. 20 and older EOL | https://github.com/nodejs/Release | The release schedule table |
| Trivy | Current; used as the fleet's open-source image scanner | https://trivy.dev/latest/ | `trivy --version` |

Values that could not be retrieved verbatim are marked as such in the table rather than asserted.
The `HEALTHCHECK` option defaults are the one such row: they are well established and the current
documentation pages truncate before the table, so this skill states the re-derivation command
instead of quoting a page it could not read.

## First-check official Docker sources

- Dockerfile reference: https://docs.docker.com/reference/dockerfile/
- Docker build documentation: https://docs.docker.com/build/
- Docker build checks: https://docs.docker.com/build/checks/
- BuildKit documentation: https://docs.docker.com/build/buildkit/
- Build secrets: https://docs.docker.com/build/building/secrets/
- Build attestations: https://docs.docker.com/build/metadata/attestations/
- Cache optimisation: https://docs.docker.com/build/cache/optimize/
- Compose file reference: https://docs.docker.com/reference/compose-file/
- Compose deploy specification: https://docs.docker.com/reference/compose-file/deploy/
- Compose interpolation: https://docs.docker.com/reference/compose-file/interpolation/
- Compose CLI reference: https://docs.docker.com/reference/cli/docker/compose/
- Swarm mode documentation: https://docs.docker.com/engine/swarm/
- Docker secrets: https://docs.docker.com/engine/swarm/secrets/
- Docker healthcheck reference: https://docs.docker.com/reference/dockerfile/#healthcheck
- Docker Scout and supply-chain docs: https://docs.docker.com/scout/
- Docker Engine release notes: https://docs.docker.com/engine/release-notes/
- Docker Hub official images: https://docs.docker.com/docker-hub/image-library/
- Registry mirror: https://docs.docker.com/docker-hub/image-library/mirror/

## Primary ecosystem sources

- Open Container Initiative image spec: https://github.com/opencontainers/image-spec
- Open Container Initiative runtime spec: https://github.com/opencontainers/runtime-spec
- Open Container Initiative distribution spec: https://github.com/opencontainers/distribution-spec
- SLSA specification: https://slsa.dev/spec/
- Sigstore Cosign docs: https://docs.sigstore.dev/cosign/
- Trivy docs: https://trivy.dev/latest/
- Alpine Linux releases: https://www.alpinelinux.org/releases/
- Debian releases: https://www.debian.org/releases/
- PHP supported versions: https://www.php.net/supported-versions.php
- Node.js release schedule: https://github.com/nodejs/Release

## Conflict resolution

1. Running repo files and explicit user constraints.
2. Official Docker docs and release notes.
3. OCI specifications.
4. Primary security tooling docs.
5. This skill's local references.

## Community troubleshooting sources

Use community posts, Stack Overflow answers, and issue comments only for concrete troubleshooting
after official docs and local logs fail to explain the symptom. Do not use them as production policy
or security guidance.
