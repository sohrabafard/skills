# Supply Chain and Package Provenance

Open this file to add a dependency from outside the workspace, to enable an install script, or to answer a question about lockfile integrity or about tracing a built package to a commit.

## Install scripts

A package's install script runs with the developer's and the runner's full privileges, before any code review of what it does, on every machine that installs. It is the shortest path from a compromised transitive dependency to a compromised laptop.

**Rule: install scripts are denied by default and allowed by name.** Where the manager supports an allow-list, the list is the record: an entry means someone decided this package needs to compile or download at install, and the entry names it. Where the manager has no allow-list, automated installs pass the manager's ignore-scripts flag and any package that genuinely needs one is documented in the repository's `AGENTS.md` with the reason.

*(The live `client` repository uses pnpm's `allowBuilds` map in `pnpm-workspace.yaml`, currently listing eight names, and enforces the manager with an `only-allow pnpm` preinstall hook. `read: 2026-07-28`.)*

Adding a name to that list is a supply-chain decision, not a build fix. Record in the merge request what the script does and why the package cannot work without it.

## Lockfile integrity

- The lockfile is committed, and every automated install is frozen. The commands are in `references/15-package-manager-modes.md`.
- A change to the lockfile is reviewed as a change, not skimmed as noise. The reviewable facts are: which packages were added, which versions moved, and whether any registry host changed. A lockfile diff that adds a package nobody named in the merge request is the finding.
- A dependency's integrity hash changing while its version does not means the registry served different bytes for the same version. Stop; do not refresh the lockfile to make it match.
- No internal package is installed from anywhere but the workspace. An internal name that resolves to a registry tarball means a workspace specifier was written wrong, and the application is running published code while the repository shows source. `scripts/verify-package-entrypoints.mjs` asserts the specifier form.

## Publication surface

Every internal package that is not published declares `"private": true`. A package intended for publication declares `publishConfig` with the registry it belongs to, so a mis-scoped name cannot reach the public registry by default. The `files` array lists exactly what is published; anything not listed does not ship, which is the mechanism that keeps source, fixtures, and internal notes out of a published tarball.

## Version stamping

A built package must be traceable to the commit that produced it. Each package's build emits `dist/.package-info.json` carrying:

| Key | Value |
|---|---|
| `name` | the package name |
| `version` | the version in the manifest at build time |
| `commit` | the full commit SHA of the workspace |
| `builtAt` | ISO 8601 UTC timestamp |

Without it, a `dist/` on disk cannot be distinguished from a `dist/` built two branches ago, which is the ambiguity behind every "it works locally" report. The artifact-level equivalent for the whole application — `build-info.json`, image labels, sourcemap policy — is `/alaa-frontend-devops` (`$alaa-frontend-devops`), `references/25-artifact-identity-and-provenance.md`. Two records, two scopes: a package's stamp answers "which commit built this `dist/`", the artifact's answers "which commit is serving production".

Nothing secret goes in either file. A package stamp is published with the package.

## Threat classification

Whether a given finding is an incident, what its severity is, whether a dependency must be removed or pinned or replaced, and whether disclosure is required belong to `/alaa-security-review` (`$alaa-security-review`). This file states what the workspace must do by default. Classification of an actual compromise is not a package decision.
