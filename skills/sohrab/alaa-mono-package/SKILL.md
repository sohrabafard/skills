---
name: alaa-mono-package
description: "Use this skill when the task involves changes under `packages/*`, clean-island package lanes, package-local `AGENTS.md` instructions, or changes to how the root app consumes an internal package. Do not use it when the task is generic CI or deployment work with no package-boundary impact."
---




# Alaa Mono Package

## Purpose

Use this skill to protect workspace package boundaries in frontend monorepos.

This skill owns:

- `packages/*` consumption rules
- clean-island package write boundaries
- dist-only package entrypoints
- peer dependency and dedupe expectations
- package CSS and asset emission into the final browser build
- verification of missing-chunk and missing-asset problems caused by package boundaries

## When to use

Use this skill when the task includes:

- changes under `packages/*`
- clean-island package lanes where only one package or package family is writable
- changes to how the root app consumes an internal package
- package build output or entrypoint changes
- package CSS, font, image, or asset emission
- missing assets or missing chunks related to internal packages

## When NOT to use

Do not use this skill when:

- the task is generic CI or deployment work with no package-boundary impact
- the task is frontend logic only inside the root app
- the repo does not use workspace packages

## Quick start

1. Read the repo-local `AGENTS.md`.
2. If the task touches or consumes a package, search for and read the nearest package-local `AGENTS.md` even when working from the root app.
3. Capture the explicit writable package boundary before editing; when the user says "clean island", "only this package", "do not change other packages", or another agent owns sibling worktrees, treat sibling packages, the root app, `src/*`, legacy files, and root config as read-only unless the user widens scope.
4. Read `references/00-source-map.md` when the task is version-sensitive, package-manager-sensitive, or security-sensitive.
5. Read `references/10-package-boundary-and-entrypoints.md`.
6. Load only the smallest additional reference file needed for the issue.
7. Validate with a real build output check instead of trusting config alone.

## Package-manager modes (detect first; never assume yarn)

Read the lockfile before giving any dependency-linking, command, or build-order advice — the manager decides the syntax:

- **pnpm** (`pnpm-lock.yaml` + `pnpm-workspace.yaml`): internal deps use the **`workspace:*`** protocol (`"@alaa/<x>": "workspace:*"`, or `workspace:^` for published packages). **Never write `link:` or a `file:`/relative path.** Members come from the `packages:` glob in `pnpm-workspace.yaml`. Commands: `pnpm --filter <pkg> <script>`, `pnpm -r <script>` (recursive, topological), `pnpm --filter "<pkg>..." build` (package + its dependents), `pnpm dlx`. pnpm's isolated (non-flat) `node_modules` blocks phantom deps, so declare every used dependency explicitly.
- **yarn Berry (v2+)** (`.yarnrc.yml`): internal deps use `workspace:^` / `workspace:*`; commands are `yarn workspace <pkg> <script>` / `yarn workspaces foreach`.
- **yarn classic (v1)** / **npm**: internal deps are `link:` / `file:` or `*` resolved by the `workspaces` field; commands are `yarn workspace <pkg> <script>` / `npm -w <pkg> run <script>`.

**Migration rule:** when a package is ported from a different-manager repo, rewrite its internal specifiers to the TARGET manager before it lands. Porting into a pnpm repo means every `link:../x` / `link:packages/x` becomes `workspace:*`; carrying a `link:` into a pnpm workspace is a boundary defect, not a stylistic choice. Peer-dependency and `resolve.dedupe` rules (§20) still apply on top of this — the manager decides the *specifier*, not whether `vue`/`quasar` stay peers.

## Build order

When a package consumes another workspace package through a public entrypoint or export subpath, build upstream packages first and consumers second.

- Derive order from the dependency graph: framework-free/core/model packages -> domain packages/adapters -> aggregate packages -> UI packages -> playground/root app.
- Do not let source aliases, test aliases, or tsconfig paths hide missing upstream `dist`; package-local build/check scripts should either build required upstream packages first or fail with a clear message.
- After building a consumer package, validate the built entrypoint from `dist` imports successfully, then check CSS/assets. This catches packages that pass source tests but fail as dist-only consumers.
- In a pnpm workspace, `pnpm -r build` runs the whole graph in dependency (topological) order, and `pnpm --filter "<pkg>..." build` builds a package plus its dependents — prefer these over a hand-maintained order script.

## Package-only lane guard

Use this guard when a task is part of parallel package work or the user freezes the write surface to one package.

1. Write down the allowed package path or package family before editing.
2. Inspect the live diff before and after changes with a changed-file list, including untracked files.
3. If a required fix appears outside the allowed package, stop and report the exact outside file instead of editing it.
4. Before final response, verify every changed file is inside the allowed package boundary or is an explicitly allowed package-owned doc/test/build artifact.
5. If root-app validation is needed, run it as a consumer check without changing root-app code.

## Symptom map

| Symptom                                       | Likely cause to check first                        |
|-----------------------------------------------|----------------------------------------------------|
| peer dependency conflict                      | package boundary or peer version contract drift    |
| missing CSS in consumer app                   | asset emission or package export wiring            |
| wrong SSR asset path                          | public-path or dist contract mismatch              |
| duplicate runtime dependency                  | workspace hoisting or peer vs dependency confusion |
| package works locally but fails after publish | dist-only artifact or export-map mismatch          |

## Companion routing

- Frontend implementation policy:
  - pair with `$alaa-frontend-developer`
- Build, artifact, or deployment contract issues:
  - pair with `$alaa-frontend-devops`
- Quasar config or Vite bundling behavior:
  - pair with `$alaa-quasar-app-vite-v3`
- Packages consumed by a Quasar app-vite v3 app (peer expectations: `vue-router >= 5`, `pinia ^2 || ^3`, Node 22+, Vite 8/Rolldown) or a v2->v3 migration touching `packages/*`:
  - pair with `$alaa-quasar-app-vite-v3`

## Reference navigation

- Official-first source priority, freshness triggers, and community-troubleshooting boundary:
  - `references/00-source-map.md`
- Package boundaries, entrypoints, and dist-only consumption:
  - `references/10-package-boundary-and-entrypoints.md`
- Peer dependencies, dedupe, and package build output:
  - `references/20-peer-deps-dedupe-and-build-output.md`
- CSS, asset emission, and final browser asset placement:
  - `references/30-assets-css-and-ssr-client-assets.md`
- Audit steps and validation loop:
  - `references/40-audit-and-verification.md`

## Maintenance rules

- Keep this skill about package contracts, not generic frontend logic.
- Keep examples portable across monorepos.
- Treat community package-manager notes as troubleshooting-only until official docs and local artifacts confirm them.
- Re-check bundler and package-manager guidance before changing the dependency rules in this skill.
