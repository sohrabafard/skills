---
name: alaa-docker-production
description: "Use this skill when the task involves production Dockerfile hardening, Docker Compose or Docker Swarm delivery patterns, registry mirror or private-registry strategy, shared-network or shared-infra container runtime design, secret and healthcheck handling, image size, or deterministic production container guidance. Do not use it when pure app logic changes."
---




# Alaa Docker Production

## Purpose

Use this skill when the task needs the architectural or policy guidance owned by Alaa Docker Production.

Keep this top-level file small. Load the references for the full rules, examples, and checklists.

## When to use

- Dockerfile or Compose hardening
- Docker Compose or Docker Swarm delivery mechanics
- image size or attack-surface reduction
- runtime user, healthcheck, or secret handling changes
- registry mirror, private-registry, or OCI-pull behavior
- shared network or shared infra container runtime design
- release evidence or deterministic image work

## When NOT to use

- pure app logic changes
- non-containerized local-only tasks

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Decide whether the task is generic Docker delivery work, Ala-specific service-contract work, or Arvan Kubernetes delivery work.
3. Read `references/00-topic-map.md`.
4. Read `references/SOURCES.md` when the task depends on latest Docker, Compose, Swarm, OCI, registry, or security behavior.
5. Load only the sections you need from `references/full-guide.md`.
6. Pair with the listed companion skills before making changes outside this skill's ownership.

## Troubleshooting map

| If the failure looks like...                | Start with                                     |
|---------------------------------------------|------------------------------------------------|
| build-stage errors or dependency drift      | image-build and deterministic-runtime sections |
| runtime crash or missing extension          | runtime contract and container-user sections   |
| permissions or writable-path issues         | non-root user and filesystem guidance          |
| healthcheck, startup, or readiness mismatch | healthcheck and release-evidence sections      |
| service discovery or proxy misrouting       | DNS alias and shared-network sections          |
| Swarm rollout or image pull problems        | runtime-mode split and registry sections       |

## Companion routing

- $alaa-services-contract
  - Pair when the task also changes Ala-specific deploy expectations, canonical service aliases, key ownership, or service bootstrap rules.
- $caas-arvan-kuber
  - Pair when the task touches the primary Arvan Kubernetes production path, Helm values, OCI charts, or GitLab rollout mechanics.
- $alaa-cicd-laravel-postgres
  - Pair when the task also touches pipeline alignment for image builds.
- $alaa-security-review
  - Pair when the task also touches runtime hardening and secret handling.
- $alaa-minio-object-storage (`/alaa-minio-object-storage` in Claude Code)
  - Pair when the task decides what a MinIO container's bucket, policy, lifecycle rules, or credentials must be, as opposed to how the container is expressed.

## Reference navigation

- Section map and fast routing:
  - `references/00-topic-map.md`
- Full preserved guidance, rules, examples, and checklists:
  - `references/full-guide.md`
- Official-first Docker, OCI, registry, and security source map:
  - `references/SOURCES.md`

## Maintenance rules

- Keep this file routing-first and plain.
- Put detailed rules into `references/full-guide.md` instead of growing this file.
- Keep the topic map aligned with the actual headings in the full guide.
- Keep generic Docker and Swarm mechanics here; move Ala-specific service-family hard constraints into `alaa-services-contract`.
- Re-check official Docker and OCI sources when latest, current, version, or security behavior matters.
- Re-check companion-skill routing when ownership boundaries change.
