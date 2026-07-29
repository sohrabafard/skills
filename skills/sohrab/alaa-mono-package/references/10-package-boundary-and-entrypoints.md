# Package Boundary and Entrypoints

Open this file to import from another package, when an import reaches into `packages/*/src`, or when beginning work in a lane where only one package or package family is writable.

## The boundary

- Before changing or auditing a package, read the package-local `AGENTS.md` if one exists, even when the shell stays at the repository root. A package-local instruction outranks a general one for that package.
- **No file outside a package may import `packages/<name>/src/**`.** Enforce it with a root `no-restricted-imports` rule. Any exemption is an inline disable carrying the owning issue ID on the same line; an exemption with no issue ID is a violation.
- The root application and every sibling package consume a package through its declared entrypoints only. Which paths those are is the `exports` map, `references/12-exports-map-and-conditions.md`.
- A package's public surface is an interface-segregation decision. The criterion for "small" is checkable: every subpath in `exports` is imported by at least one consumer in the repository, or is documented in the package's `README.md` as an intentionally-published surface with the consumer it exists for. A subpath that is neither is removed.

## Why a source import is not a shortcut

A source import bypasses three things at once, and it bypasses them silently:

- the `exports` map, so the consumer depends on a path the package never promised and may move without warning;
- the package's build, so the consumer compiles the package's source with the *application's* configuration rather than the package's own, which is how a package that builds cleanly produces different output in one consumer than another;
- externalisation and dedupe, so a shared runtime that the package declares as a peer is instead bundled into the application through the source path. The peer contract is `references/20-peer-deps-dedupe-and-build-output.md`.

The symptom is usually none of these directly. It is a package that "works locally", because locally the source is present and the alias resolves.

## The lane guard, at the file level

`SKILL.md` states the three-step guard that constrains writes. This file states what "inside the boundary" means when you check it:

- Inside: files under the named package directory, including its `README.md`, its tests, and its build configuration.
- Inside, when named: any additional path the user listed when opening the lane. If the user named none, the package directory is the whole allowance.
- Outside: sibling packages, the root application, root configuration, the lockfile, and the workspace manifest — regardless of how small the needed change is.

A required fix outside the boundary is reported by exact path and left unmade. Reporting it is the deliverable; making it is the defect.

## Relationship to the delivered artifact

This skill decides what a package declares and what enters the bundling graph. Where the graph's output lands, how it is served, how it is traced to a commit, and how it is rolled back belong to `/alaa-frontend-devops` (`$alaa-frontend-devops`), `references/10-build-contract-and-artifacts.md`.

The one rule that straddles the seam is package assets in the final client asset output. This skill owns whether a package asset is *reachable from an entry*, in `references/30-assets-css-and-ssr-client-assets.md`; that skill owns whether the output *landed where the deployment serves it*. Neither restates the other.
