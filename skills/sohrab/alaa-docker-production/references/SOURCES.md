# Sources

Use this file when Docker, Compose, Swarm, registry, OCI, or container security behavior must be current.

## Freshness triggers

Re-check primary sources when the user asks for latest/current behavior, Dockerfile syntax, BuildKit or buildx behavior, Compose or Swarm compatibility, image provenance, registry behavior, CVEs, Docker Desktop or Engine changes, official image behavior, or production hardening guidance.

## First-check official Docker sources

- Dockerfile reference: https://docs.docker.com/reference/dockerfile/
- Docker build documentation: https://docs.docker.com/build/
- Docker build checks: https://docs.docker.com/build/checks/
- BuildKit documentation: https://docs.docker.com/build/buildkit/
- Docker Compose file reference: https://docs.docker.com/reference/compose-file/
- Docker Compose CLI reference: https://docs.docker.com/reference/cli/docker/compose/
- Swarm mode documentation: https://docs.docker.com/engine/swarm/
- Docker secrets: https://docs.docker.com/engine/swarm/secrets/
- Docker healthcheck reference: https://docs.docker.com/reference/dockerfile/#healthcheck
- Docker Scout and supply-chain docs: https://docs.docker.com/scout/
- Docker Engine release notes: https://docs.docker.com/engine/release-notes/
- Docker Hub official images: https://docs.docker.com/docker-hub/image-library/

## Primary ecosystem sources

- Open Container Initiative image spec: https://github.com/opencontainers/image-spec
- Open Container Initiative runtime spec: https://github.com/opencontainers/runtime-spec
- Open Container Initiative distribution spec: https://github.com/opencontainers/distribution-spec
- SLSA specification: https://slsa.dev/spec/
- Sigstore Cosign docs: https://docs.sigstore.dev/cosign/
- Trivy docs: https://trivy.dev/latest/

## Conflict resolution

1. Running repo files and explicit user constraints.
2. Official Docker docs and release notes.
3. OCI specifications.
4. Primary security tooling docs.
5. This skill's local references.

## Community troubleshooting sources

Use community posts, Stack Overflow answers, and issue comments only for concrete troubleshooting after official docs and local logs fail to explain the symptom. Do not use them as production policy or security guidance.
