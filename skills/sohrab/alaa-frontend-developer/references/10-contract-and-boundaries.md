# Contract and Boundaries

This file defines the default contract for the standard app family that uses Vue 3 + Quasar + Vite. Treat these as defaults, not universal laws: if a repo-local `AGENTS.md` or explicit user instruction differs, that higher-priority rule wins.

## Standard app-family contract

- Vue 3 + Quasar + Vite frontend stack
- ESM-first
- JavaScript plus JSDoc by default unless the repo already standardizes on TypeScript
- Yarn-first behavior when the repo uses Yarn or has `yarn.lock`
- SSR and PWA may both be enabled, so browser-only assumptions are not safe by default

## Always optimize for

- SSR correctness and hydration safety
- deterministic rendering
- minimal bundle size
- route-level code splitting and lazy loading
- Quasar tree-shaking friendliness
- accessibility and semantic HTML
- SEO-safe SSR output when SSR is enabled
- low operational risk in build and deploy flows
- compatibility with weaker networks and mobile devices

## Hard constraints

- Do not break SSR or introduce hydration mismatches.
- Do not rely on browser-only APIs during SSR render paths.
- Do not add unnecessary complexity or hidden side effects.
- Do not perform drive-by refactors.
- Do not change root package-manager scripts unless explicitly requested by maintainers.
- Do not silently change service-worker caching strategy, public asset paths, or build output contracts.

## Required workflow defaults

1. Read repo-local `AGENTS.md`.
2. Apply `$alaa-low-noise`.
3. Inspect existing patterns before changing behavior.
4. Identify the root cause or decision point before choosing a fix.
5. Make the smallest safe change.
6. Run the lightest meaningful verification or write a concrete manual verification plan.

## SSR auth boundary

Default app-family assumption:

- Access tokens live in HttpOnly cookies at the SSR layer.
- When the server-side frontend calls backend APIs, it maps the cookie token to:
  - `Authorization: Bearer <token>`
- That mapping stays server-side only.
- Do not expose tokens to client JavaScript, serialized HTML, or initial state.

If the repo uses a different auth contract, repo-local rules override this default.

## Browser automation boundary

- Prefer static inspection, logs, and source reasoning unless:
  - the user explicitly asks for browser validation, or
  - a higher-priority repo rule requires browser reproduction before fixing
- When browser work is allowed, use isolated sessions and collect only the smallest evidence set that proves the issue

## Monorepo and package boundary

When the repo uses workspace packages:

- Root apps should consume package entrypoints, not package source files directly.
- Packages should emit stable dist outputs.
- Shared dependencies such as `vue` and `quasar` should be externalized, typically via `peerDependencies`.
- Runtime CSS and assets must stay in the bundling graph so final browser assets land in the final client-assets output.

## Build and artifact contract

Default app-family deployment contract:

- SSR runtime entry remains `dist/ssr/index.js`
- Final browser assets must be emitted under `dist/ssr/client/assets`
- If the app serves assets remotely, keep one canonical public/base-path source of truth and treat changes as deployment-critical

## Pairing guidance

- Exact Quasar config, component, or platform behavior:
  - Pair with `$quasar-skill-packe`
- CI, Docker, proxy, or deploy-artifact issues:
  - Pair with `$devops-engineer`
- `packages/*` boundaries, asset emission, or externalization:
  - Pair with `$monorepo-packages-contract-guard`
- API envelope or pagination/filtering design:
  - Pair with `$api-designer`
- SSR auth boundary or cookie/header flows:
  - Pair with `$ssr-auth-guard`
