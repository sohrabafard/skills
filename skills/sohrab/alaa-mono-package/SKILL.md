---
name: alaa-mono-package
description: "Use this skill when the task involves changes under `packages/*`, a package's `exports` map or public entrypoints, internal dependency specifiers, peer dependencies or a duplicated runtime, package CSS and asset emission, workspace build order, clean-island package lanes, package-local `AGENTS.md` instructions, or changes to how the root app consumes an internal package. Do not use it when the task is generic CI or deployment work with no package-boundary impact, or when the question is where a built artifact lands and how it is served, which belongs to alaa-frontend-devops."
---

# Alaa Mono Package

Workspace package contracts: what a package declares, what it emits, and what therefore enters the application's bundling graph.

## When NOT to use

Stop and route when the task has **no package-boundary impact** — generic CI, container or deployment work — or when the question is where a built artifact lands, how it is served, how it is traced to a commit, or how it is rolled back. This skill owns what enters the bundling graph; the seam below names who owns the rest.

## Ownership and the seam

`alaa-mono-package` owns everything that determines what enters the bundling graph — a package's declared exports, its peer contract, its specifiers, and whether its CSS and assets are reachable from an entry — while `/alaa-frontend-devops` (`$alaa-frontend-devops`) owns everything that happens to that graph's output after `build` exits: where it lands, how it is served, how it is traced to a commit, and how it is rolled back.

Exactly one rule straddles that seam: package assets in the final client asset output. This skill owns whether the asset is reachable from an entry (`references/30-assets-css-and-ssr-client-assets.md`); `/alaa-frontend-devops` (`$alaa-frontend-devops`) owns whether the output landed where the deployment serves it (`alaa-frontend-devops` `references/10-build-contract-and-artifacts.md`). Neither restates the other.

Every other owner this skill depends on is listed with its file path in `references/90-companion-boundary.md`. This skill states no version value of its own; it routes every range to its owner.

## Read the lockfile first

Before writing any dependency specifier or running any workspace command, read the lockfile that exists in the repository. The manager decides the syntax, and a specifier written for the wrong manager installs a second copy instead of linking the workspace one. Detect; never assume. The protocols and filter syntax are `references/15-package-manager-modes.md`.

## Three rules that never cost a hop

1. **Never import `packages/<name>/src/**` from outside that package.** It works locally every time, which is why it survives review. What it silently bypasses, and how to enforce the ban, are in `references/10-package-boundary-and-entrypoints.md`.
2. **`vue`, `quasar`, `vue-router`, and `pinia` are peers of every internal package, never dependencies**, and each must resolve to exactly one real path across the workspace.
3. **A package is not done until every condition its `exports` declares has been imported under that condition.** A declared condition pointing at a file that is absent or throws produces no error in the package that declares it; it fails in the consumer. Run `scripts/verify-package-entrypoints.mjs`; exit code 2 means unbuilt or unreadable and is not a pass.

## The clean-island lane guard

Apply this when the user says "clean island", "only this package", "do not change other packages", or when another agent owns a sibling lane.

1. Write down the allowed package path or package family before editing. Every path outside it — the root application, sibling packages, root configuration, the lockfile — is read-only until the user names an additional path.
2. Inspect the changed-file list before and after, including untracked files.
3. If a required fix lies outside the allowance, report the exact path and leave it unmade. Root-application validation runs as a consumer check without editing root-application code.

## Navigation

The router is `references/00-topic-map.md`, and it routes both by what you are about to do and by the symptom you are seeing. Open it, match one row, read that one file.

Model selection and reasoning effort: `/alaa-prompting-guide` (`$alaa-prompting-guide`), `references/50-effort-and-thinking.md`.
