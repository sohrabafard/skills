# CI Gates and Predicates

Open this file to add, remove, or reorder a check that can block a merge or a release for a frontend repository, or to change the install command, the lockfile handling, the Node version, or a cache key input.

This file is a **gate register**. Each gate is a predicate, the command that evaluates it, and the artifact it inspects. It contains no provider YAML. How a gate is expressed on a runner — job graph, `rules:`, `needs:`, `cache: key:`, `policy:`, artifact retention and `expire_in`, the runner image reference — belongs to `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`). How the build and runtime images are expressed belongs to `/alaa-docker-production` (`$alaa-docker-production`).

## When the gates run

All gates below run on every merge request whose diff touches `src/**`, `packages/**`, `quasar.config.*`, the lockfile, `package.json`, or the Dockerfile, and on every pipeline that produces a publishable artifact. This skill states *when*; the provider skill states *how the condition is written*.

## The register

| # | Gate | Predicate | Command | Artifact inspected |
|---|---|---|---|---|
| 1 | Frozen install | The install does not modify the lockfile. | `pnpm install --frozen-lockfile`, or `npm ci`, or `yarn install --immutable`, chosen by which lockfile exists | the lockfile, before and after |
| 2 | Node line | The Node running the build satisfies `engines.node` **and** sits on a Node Active-LTS or Maintenance-LTS line. A floating tag such as `node:lts` fails this gate. | `node -p "process.version"` compared against `engines.node` | `package.json`, the CI runner image tag |
| 3 | Package-manager line | The manager and version running the build equal `packageManager` in the root `package.json`, exactly. | `corepack enable && <manager> --version` | `package.json` |
| 4 | Typecheck | The project typechecks with no emit. | `pnpm typecheck` | the source tree |
| 5 | Package contracts | Every workspace package satisfies its export surface. | `/alaa-mono-package` (`$alaa-mono-package`) `scripts/verify-package-entrypoints.mjs` | `packages/*/package.json`, `packages/*/dist` |
| 6 | Artifact contract | The emitted tree satisfies `references/10-build-contract-and-artifacts.md`. **This is the defining gate of this skill.** | `scripts/verify-artifact-contract.mjs <dist-root>` | the emitted build tree |
| 7 | Publish precondition | The publish step asserts the artifact tree exists and is non-empty before uploading. An upload job that assumes a folder exists fails this gate. | gate 6 as a `needs:` predecessor of the upload | the emitted build tree |
| 8 | Provenance | The artifact carries the commit that produced it. | `scripts/verify-artifact-contract.mjs` assertion 6 | the provenance file, the image labels |
| 9 | Publish interlock | At most one pipeline publishes to a given asset root or image tag at a time. | a named exclusive resource on the publishing job | the asset root, the registry tag |

Gate 9 is a frontend gate because only this skill knows that two concurrent publishes to one asset root can interleave hashed files from two builds and leave an HTML document pointing at a file that the other build did not emit. The mechanism that provides exclusivity is the provider's (`resource_group:` on GitLab); the requirement is this skill's. The live `client` frontend pipeline already sets an exclusive resource on its image-build jobs (`read: 2026-07-28`); the asset upload inherits it from the same job.

## Cache-key predicates

These are predicates *on* a key. The key's syntax is the provider's.

- A change to the lockfile changes the key.
- A change to the Node version, the package-manager version, or the base image changes the key.
- A workspace package manifest is an input to the dependency layer, so a change to any `packages/*/package.json` changes the key.
- A stale cache is a candidate cause when the emitted bundle differs between two builds of the same commit. Deleting caches without changing the key does not close that finding; it hides it until the next run.

## Package-manager detection

Never assume a manager. Read the lockfile that exists in the repository, then use that manager's commands. The detection rule and the specifier protocols belong to `/alaa-mono-package` (`$alaa-mono-package`), `references/15-package-manager-modes.md`. This file names only the frozen-install command per manager, in gate 1, because that command is the gate.

## What the runtime image must satisfy

These are obligations on the image, not instructions for writing it. The Dockerfile that satisfies them is `/alaa-docker-production` (`$alaa-docker-production`)'s to author, including layer ordering, dependency-layer inputs, multi-stage separation, and image minimisation.

- The runtime image contains the complete client asset tree and the SSR runtime entry at the paths declared in `references/10-build-contract-and-artifacts.md`.
- The runtime image contains no package manager, no compiler, and no devDependencies. If a single-stage build is unavoidable, name the blocking constraint in the merge request and obtain `/alaa-docker-production` (`$alaa-docker-production`)'s written exemption before merging.
- No build-time environment variable survives into the runtime image except those carrying the client prefix. Every other build argument is consumed during the build stage and absent from the final layer.
- The image is labelled with the commit SHA that produced the bundle. See `references/25-artifact-identity-and-provenance.md`.
