---
name: alaa-frontend-devops
description: "Use this skill when the task involves CI or pipeline gates for a frontend repository, Dockerfile or Compose changes that affect frontend build or runtime delivery, the build artifact contract, public path or asset base, cache policy, build provenance, what may be compiled into a client bundle, or a frontend deploy failure or rollback. Do not use it when the task is frontend logic only and has no build or deploy impact, or when the task is package-boundary specific and belongs to alaa-mono-package."
---

# Alaa Frontend DevOps

Frontend delivery: what a build must emit, and what happens to that artifact afterwards — where it lands, how it is served, how it is traced to a commit, and how it is undone.

## When NOT to use

Stop and route when the task has **no build, artifact, serving or deploy impact**; when it is package-boundary work — an `exports` condition, a peer contract, a specifier, or whether an asset is reachable from an entry; or when it is how a gate is *expressed* on a runner, in an image or as a proxy directive rather than what the gate asserts. The ownership section below names each owner.

## Ownership: stack versus platform

`alaa-frontend-devops` owns the frontend delivery gate register — for each gate, the predicate it asserts, the command that evaluates it, and the artifact it inspects — and writes no provider YAML and no Dockerfile: `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) owns how a gate is expressed on a runner and decides no gate, `/alaa-docker-production` (`$alaa-docker-production`) owns how the build and runtime images and any Compose file are expressed and decides no gate, and `/alaa-haproxy` (`$alaa-haproxy`) owns how a cache or routing decision is expressed as a directive and decides no policy.

Seam with the package graph: `/alaa-mono-package` (`$alaa-mono-package`) owns everything that determines what enters the bundling graph — a package's declared exports, its peer contract, its specifiers, and whether its CSS and assets are reachable from an entry. This skill owns everything that happens to that graph's output after `build` exits.

Every other owner this skill depends on is listed with its file path in `references/90-companion-boundary.md`. Do not write in another owner's ground: state the obligation the frontend needs, and route.

## Three rules that never cost a hop

1. **A client bundle is a public artifact.** Every emitted chunk is downloadable by anyone, permanently, and minification conceals nothing. No credential, key, internal hostname, or personal datum may reach one. What is allowed, and the gate that proves it, is `references/35-client-bundle-security.md`.
2. **Every shipped artifact carries the commit that produced it.** If you cannot answer "which commit produced the bundle currently serving production" from the deployment alone, rollback is a guess. The provenance file and its keys are `references/25-artifact-identity-and-provenance.md`.
3. **Verify outputs, not exit codes.** A build that exits 0 has proved nothing about what it emitted. Run `scripts/verify-artifact-contract.mjs <dist-root>` and read the exit code: 0 passes, 1 is a contract failure, 2 means the tree could not be read and is not a pass.

## Before you finish

A delivery change ships with its rollback unit, its rollback command, its precondition, and its irreversible part written down. "Be ready to describe what to revert" is not a rollback path. See `references/40-verification-and-rollback.md`.

## Navigation

The router is `references/00-topic-map.md`. Open it, match your situation to one row, read that one file.

Model selection and reasoning effort: `/alaa-prompting-guide` (`$alaa-prompting-guide`), `references/50-effort-and-thinking.md`.
