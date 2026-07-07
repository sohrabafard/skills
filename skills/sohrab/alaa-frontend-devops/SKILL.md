---
name: alaa-frontend-devops
description: "Use this skill when the task involves CI workflow changes for a frontend repository or Dockerfile or Compose changes that affect frontend build or runtime delivery. Do not use it when the task is frontend logic only and has no build or deploy impact."
---




# Alaa Frontend DevOps

## Purpose

Use this skill for frontend delivery work that can break the build, artifact contract, or deployed runtime even when the code change looks small.

This skill owns:

- CI and pipeline safety for SSR or PWA frontends
- Docker and container build discipline for frontend delivery
- artifact and public-path contracts
- reverse proxy and remote asset serving concerns
- deploy-time verification, rollback, and cache-safety checks

## When to use

Use this skill when the task includes any of the following:

- CI workflow changes for a frontend repository
- Dockerfile or Compose changes that affect frontend build or runtime delivery
- asset output issues, missing chunks, or bad client asset paths
- remote asset hosting or CDN-style asset base changes
- reverse proxy, cache header, or asset serving problems
- SSR runtime delivery issues caused by build, deploy, or infra configuration

## When NOT to use

Do not use this skill when:

- the task is frontend logic only and has no build or deploy impact
- the task is purely visual design or browser QA
- the task is package-boundary specific and belongs to `$alaa-mono-package`

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Apply `$alaa-low-noise`.
3. Read `references/00-source-map.md` when the task is version-sensitive, security-sensitive, or about current deploy behavior.
4. Read `references/10-build-contract-and-artifacts.md` first for delivery-contract work.
5. Load only the smallest additional reference file needed for the task.
6. Validate in the same environment shape that would catch the delivery risk.

## Verification matrix

| Delivery shape   | Must verify                                                                          |
|------------------|--------------------------------------------------------------------------------------|
| SPA              | final asset paths, cache headers, and fallback routing                               |
| SSR              | server entry, client manifest, cookies/session flow, and hydration-safe deploy shape |
| PWA              | service worker scope, update UX, offline boundaries, and asset versioning            |
| package-consumer | emitted JS/CSS assets, peer dependencies, and import paths                           |

## Companion routing

- Frontend implementation policy and SSR behavior:
  - pair with `$alaa-frontend-developer`
- Workspace package asset emission or `packages/*` boundaries:
  - pair with `$alaa-mono-package`
- Quasar config, platform mode, or exact Quasar build behavior:
  - pair with `$alaa-quasar-app-vite-v3`
- Documentation-only deployment notes or inline doc updates:
  - pair with `$alaa-frontend-doc-annotations`
- Current OpenAI or Codex product facts that affect build or tool integration:
  - pair with `$openai-docs`

## Reference navigation

- Official-first source priority, freshness triggers, and community-troubleshooting boundary:
  - `references/00-source-map.md`
- Build contract, artifact rules, SSR runtime entry, and final asset expectations:
  - `references/10-build-contract-and-artifacts.md`
- CI, Docker, cache keys, install layers, and deterministic builds:
  - `references/20-ci-docker-and-cache.md`
- Reverse proxies, public path, remote assets, and runtime serving:
  - `references/30-proxies-public-path-and-remote-assets.md`
- Verification, release checks, rollback, and deployment-safe closeout:
  - `references/40-verification-and-rollback.md`

## Maintenance rules

- Keep this skill focused on frontend delivery and deploy safety.
- Prefer one-hop references instead of growing this file.
- Keep examples plain and portable; do not hard-code one repo unless the example is explicitly repo-scoped.
- Re-check official sources before updating version, security, or current-behavior guidance.
- If current OpenAI or Codex guidance affects tool usage or maintenance advice, re-check `$openai-docs` before updating this skill.
