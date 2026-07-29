# Contract and Boundaries

The default contract for the standard app family on Vue 3 + Quasar + Vite. These are constraints. The only
override is a repo-local `AGENTS.md` rule or an explicit user instruction that contradicts a named line
here; cite the file and line you are overriding.

## Standard app-family contract

- Vue 3 + Quasar + Vite, ESM-first.
- **All new and modified frontend code is TypeScript under `strict`.** Run the gates in
  `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`) `references/00-topic-map.md`.
  JavaScript is permitted only in a file already inside the repo's `allowJs` set. TypeScript 6 is the
  fleet line; TypeScript 7 and its native compiler are not adopted, because Quasar has not declared
  support — that ruling and the toolchain live in that skill, not here.
- Yarn-first when the repo has a `yarn.lock`.
- SSR and PWA may both be on, so a browser-only assumption is never safe by default.

## Hard constraints

- Do not break SSR or introduce a hydration mismatch.
- Do not touch a browser-only API on an SSR render path.
- Do not store per-request mutable state in a module-level singleton.
- Do not perform a drive-by refactor, and do not change root package-manager scripts unless the
  maintainer asked.
- Do not change service-worker caching strategy, public asset paths, or build output contracts as a side
  effect of another change.

## Always optimize for

SSR correctness and hydration safety; deterministic rendering; route-level code splitting and
tree-shaking; accessibility and semantic HTML; SEO-safe SSR output when SSR is on; low operational risk in
build and deploy; and behaviour on a weak network and a slow device.

## Required workflow

Stated once, in `SKILL.md` under "Workflow and maintenance". Do not restate it here or in a review
comment. The proof level it ends on is selected by `05-proof-and-tests.md`.

## SSR auth and session boundary

One line only: before changing auth, protected-route or SSR data-fetch behaviour, read
`21-ssr-auth-and-session-patterns.md`. It owns the five supported postures, the decision order, the
storage rule and the refresh contract. Do not restate any of it here or in a component.

## Browser automation boundary

Static inspection, logs, tests and source reasoning first. The three conditions that open a browser, and
the observation you must name before you do, are gate 5 in `SKILL.md`; the evidence discipline is
`60-browser-debug.md`.

## Package and artifact boundary

Whether a package asset is reachable from an entry, which dependencies are peers, what a package emits,
and where the SSR runtime entry and the browser assets land are all decided by `/alaa-mono-package`
(`$alaa-mono-package`) — `references/10-package-boundary-and-entrypoints.md` for entrypoints,
`references/20-peer-deps-dedupe-and-build-output.md` for the peer-dependency contract,
`references/30-assets-css-and-ssr-client-assets.md` for asset reachability and the `dist/ssr` paths. This
skill consumes that result and does not restate it. When an artifact reaches a server or a CDN,
`/alaa-frontend-devops` (`$alaa-frontend-devops`) `references/00-topic-map.md` owns the delivery gate.

The one thing this skill does state: a route's public or base path has exactly one source of truth in the
app, and it is validated at boot — see `48-config-and-environment.md`.

## Pairing

- Exact Quasar config, component or platform behaviour: `/alaa-quasar-app-vite-v3`
  (`$alaa-quasar-app-vite-v3`) `references/00-topic-map.md`.
- Frontend-facing envelopes, pagination, filters, cache validators: `45-api-and-data-shaping.md`.
- A frontend issue that has become server work: `/alaa-laravel-architecture`
  (`$alaa-laravel-architecture`) or `/alaa-data-layer` (`$alaa-data-layer`).
- Documentation-only passes: `/alaa-frontend-doc-annotations` (`$alaa-frontend-doc-annotations`)
  `references/10-annotation-boundaries.md`.
