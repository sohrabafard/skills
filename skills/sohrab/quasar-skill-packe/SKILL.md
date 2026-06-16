---
name: quasar-skill-packe
description: "Routing-first Quasar CLI + Vite skill for Quasar-specific app setup, quasar.config, boot/routing, SSR/PWA, platform modes (BEX, Capacitor, Electron), components, layouts, plugins, and upgrades. Covers both @quasar/app-vite v2 and the newer v3 (import paths, env config, aliases, folder structure differ). Use when Quasar is the decision surface or when the user mentions Quasar, quasar.config, QImg/QTable/QLayout-style symbols, app-vite, or a Quasar upgrade. Do not use it for generic Vue or Vite work that is not Quasar-specific."
---

# Quasar Skill Packe

## Overview

This is a routing-first Quasar skill pack.

Use it when a task is specifically about Quasar or a Quasar-built app. It replaces a large collection of narrow `quasar-*` skills with one focused entry point plus a small set of topic references. The goal is to keep context small while still covering the full Quasar CLI + Vite surface area.

This skill does four jobs:

1. Route the agent to the smallest relevant reference file.
2. Force the agent to load related Quasar topics that are commonly missed.
3. Keep version-sensitive work current by refreshing live upstream data before acting.
4. Detect which `@quasar/app-vite` major (v2 or v3) the repo uses before giving config-shaped advice.

It is written to be consumed by both Claude Opus 4.x and GPT-5 / Codex agents. See `references/90-agent-authoring-and-dual-runtime.md` only when editing the pack itself.

## Stable-first policy (production)

Default to **production-ready stable** releases. For Quasar/Vite work that means:

- **`@quasar/app-vite` v2.x is the stable, production-ready line** (latest stable `2.6.2`). It is the default for new work and the recommendation for any production app.
- **`@quasar/app-vite` v3 (`3.0.0-rc.x`) is pre-release (RC). It has no stable release yet** — only `beta` and `rc` on npm. Cover it and support a repo that already opted in, but **do not recommend migrating a production app to v3 while it is RC**, and do not scaffold new production apps on it unless the user explicitly asks for the pre-release.
- Quasar `2.20.1`, Vite `8.0.16`, Vue `3.5.38`, Vue Router `5.1.0`, Pinia `3.0.4`, Workbox `7.4.1` are all stable; use them freely.

If the user explicitly wants the bleeding edge, say plainly that v3 app-vite is RC and proceed only on their request.

For the **v2-vs-v3 production decision, v3-readiness, or a v2->v3 migration**, use `$alaa-app-vite-quasar` (it owns that playbook). This pack keeps only the summary needed to pick the right per-line code shape.

## Detect the app-vite line first (highest-impact rule)

The two app-vite lines have **different import paths, config formats, aliases, and folder layouts**. Read `@quasar/app-vite` in the repo's `package.json` before giving config, boot, env, alias, SSR, PWA, BEX, Electron, or Capacitor advice — and match the repo, never "upgrade it to v3" by default.

- `^2.x` (stable / production) — uses `#q-app/wrappers`, `.js/.mjs/.ts/.cjs` config, `build.envFolder`/`build.envFiles`, `process.env.MODE`, and legacy aliases (`src/`, `components/`, `boot/`, ...).
- `^3.x` (pre-release / RC) — uses `#q-app`, `.js/.ts` config only, `build.env.{folder,file,clientPrefix}`, `import.meta.env.QUASAR_MODE`, and the single `@/` alias.

✅ Do — confirm the line, give shapes for that line only, and keep a production repo on stable v2 unless the user asks otherwise.

❌ Don't — apply v3 import paths/aliases to a v2 repo (or vice versa), or push a production app onto RC v3. The full split is in `references/70-upstream-deltas-and-live-checks.md`.

## How examples are written in this pack

High-value rules use a `✅ Do` / `❌ Don't` contrast pair: the `✅` is the action the agent should take and why; the `❌` is a realistic mistake and why it is wrong. Treat the `✅` side as the instruction and the `❌` side as a guardrail, not as something to copy.

## Package manager rule

Respect the repository's package-manager contract.

- If the repo is Yarn-based, uses Yarn workspaces, or contains `yarn.lock`, prefer Yarn for installs and script execution.
- Do not switch an existing repo to Bun, pnpm, or npm just because Quasar supports them upstream.
- Upstream package-manager support is a compatibility fact, not a migration recommendation.

## When to use

Use this skill when the task includes any of the following:

- Quasar CLI app setup or migration, including `@quasar/app-vite` v2 -> v3 upgrades
- `quasar.config` changes
- Vite integration inside a Quasar app
- SSR, hydration, `ssrContext`, SSR middleware, SEO, or cookie-to-header auth flows
- PWA, service worker, offline fallback, or Workbox InjectManifest
- Platform modes such as SPA, BEX, Capacitor, Cordova, or Electron
- Quasar components, layouts, plugins, composables, directives, options, or utils
- Quasar package/library packaging in a monorepo
- Quasar or Vite upgrade work
- "latest" or version-sensitive Quasar/Vite/Vue Router questions

## When NOT to use

Do not use this skill when:

- the task is generic Vue work that is not Quasar-specific
- the task is generic Vite work in a non-Quasar project
- the task is pure design or generic frontend polish without Quasar APIs in scope
- a narrower repo-specific skill already owns the exact workflow and Quasar is only incidental

## Working model

This skill is intentionally split into references. Do not load everything by default.

Use this sequence:

1. Read `references/00-topic-map.md` unless you already know the exact topic file.
2. Load only the smallest relevant topic reference.
3. Follow that file's "Also load" guidance before making changes.
4. For any config/CLI/mode/SSR/PWA task, confirm the app-vite line (see above) before writing shapes.
5. If the task is upgrade-related, toolchain-related, or asks for the latest guidance, read `references/70-upstream-deltas-and-live-checks.md` and refresh live data.
6. If the request uses an old `quasar-*` skill name, read `references/80-legacy-skill-coverage.md`.

## Quick routing

- App setup, build config, `quasar.config`, boot files, routing, env files, aliases, proxies, lazy loading, testing, or upgrades:
  - `references/10-cli-vite-and-config.md`
  - `references/11-cli-cookbook-and-examples.md` when exact config or boot-file shape matters
- SSR, hydration, middleware, `ssrContext`, `preFetch`, auth cookies, SEO, PWA, service worker, or offline:
  - `references/20-ssr-pwa-and-security.md`
  - `references/21-pwa-injectmanifest-guard.md` when InjectManifest boundaries or update invariants matter
- SPA vs SSR vs PWA vs BEX vs Capacitor vs Cordova vs Electron:
  - `references/30-platform-modes.md`
- Components or layouts:
  - `references/40-components-and-layouts.md`
- Exact component usage patterns, alternatives, and search terms:
  - `references/41-component-usage-atlas.md`
- Layout shells, `view` semantics, drawers, and routing-with-layouts patterns:
  - `references/42-layout-patterns-and-examples.md`
- Deterministic `QImg` delivery, placeholders, and responsive image sizing:
  - `references/43-image-delivery-and-placeholders.md`
- Plugins, composables, directives, options, or utils:
  - `references/50-plugins-composables-directives-options-utils.md`
  - `references/51-directive-usage-atlas.md` when exact directive behavior or snippet shape matters
  - `references/52-api-usage-atlas.md` when exact plugin/composable/option/util behavior or snippet shape matters
- A11y, performance, monorepo packaging, tree-shaking, or cross-cutting guardrails:
  - `references/60-guardrails-a11y-performance-monorepo.md`
- Latest versions, migration risk, the app-vite v2/v3 split, or skill maintenance:
  - `references/70-upstream-deltas-and-live-checks.md`
- Mapping from legacy single-topic `quasar-*` skills:
  - `references/80-legacy-skill-coverage.md`
- Editing this pack for both Claude and Codex consumers:
  - `references/90-agent-authoring-and-dual-runtime.md`

## Mandatory related-topic rules

Apply these even if the user only names one Quasar surface:

- Any SSR, `preFetch`, router, store, boot, middleware, SEO, QNoSsr, or auth task:
  - Also load `references/20-ssr-pwa-and-security.md`.
- Any custom service worker or InjectManifest task:
  - Also load `references/21-pwa-injectmanifest-guard.md`.
- Any platform-mode task:
  - Read `references/10-cli-vite-and-config.md` and `references/30-platform-modes.md` together.
- Any component that handles data grids, virtualization, uploads, media, dialogs, menus, responsive layout, or browser APIs:
  - Also load `references/60-guardrails-a11y-performance-monorepo.md`.
- Any task touching browser-only APIs in a universal app:
  - Combine the topic file with `references/20-ssr-pwa-and-security.md`.
- Any version-sensitive or upgrade request:
  - Read `references/70-upstream-deltas-and-live-checks.md` before proposing a fix.
- Any library or workspace package task:
  - Combine `references/10-cli-vite-and-config.md` with `references/60-guardrails-a11y-performance-monorepo.md`.

## Search rules

When searching inside this skill pack:

- Search exact Quasar symbols first:
  - `QTable`, `QImg`, `useMeta`, `useHydration`, `ClosePopup`, `Notify`, `extendViteConf`
- If the symbol is a Quasar config, boot, routing, or Vite-extension surface, also open:
  - `references/11-cli-cookbook-and-examples.md`
- If the symbol is a component or layout primitive, also open:
  - `references/41-component-usage-atlas.md`
- If the symbol is specifically about layout shells, drawers, `view`, or page containers, also open:
  - `references/42-layout-patterns-and-examples.md`
- If the symbol is specifically about `QImg`, placeholders, responsive image candidates, or deterministic image delivery, also open:
  - `references/43-image-delivery-and-placeholders.md`
- If the symbol is a directive, also open:
  - `references/51-directive-usage-atlas.md`
- If the symbol is a plugin, composable, option, or util, also open:
  - `references/52-api-usage-atlas.md`
- Then search task phrases:
  - `boot files`, `ssrContext`, `InjectManifest`, `BEX Bridge`, `envFolder`, `build.env.folder`, `#q-app`
- If the user mentions an old skill name, search `references/80-legacy-skill-coverage.md`
- If you still are not sure, start with:
  - `references/10-cli-vite-and-config.md`
  - `references/20-ssr-pwa-and-security.md`

## Companion routing

- `$alaa-app-vite-quasar`
  - **Require** this for the app-vite **v2 production + v3-readiness/migration** decision: version posture, "should we go v2 or v3", how to write v2 code that migrates cleanly, the full v2->v3 migration playbook, and upgrade/CI guardrails.
  - This pack keeps only a **summary** of the v2/v3 split (enough to pick the right code shape). Route to `$alaa-app-vite-quasar` for the deep migration/readiness work, and stay here for the exact Quasar API/config/component shape it asks for.
- `$alaa-frontend-developer`
  - Pair for broader frontend engineering, SSR auth, data shaping, or release-readiness decisions.
- `$alaa-frontend-devops`
  - Pair when Quasar changes also touch build, Docker, CI, asset paths, or deployment behavior.
- `$alaa-mono-package`
  - Pair when a Quasar package lives in `packages/*` or emits assets for other apps.
- `$alaa-frontend-doc-annotations`
  - Pair for documentation-only comment or JSDoc passes.
- `$openai-docs`
  - Pair when live Codex or OpenAI product behavior influences the workflow.

## Current live snapshot

This snapshot was refreshed on June 16, 2026 and will age over time:

- Quasar (framework): `2.20.1` (stable)
- `@quasar/app-vite` (stable / production): `2.6.2` — **use this line for production**
- `@quasar/app-vite` (pre-release): `3.0.0-rc.3` (RC; no stable release yet — beta + rc only)
- Vite: `8.0.16` (stable)
- Vue: `3.5.38` (stable)
- Vue Router: `5.1.0` (stable)
- Pinia: `3.0.4` (v2 or v3; Vuex is no longer integrated in the CLI)
- Workbox: `7.4.1` (stable)

Refresh this snapshot before any version-sensitive work by running:

```bash
node scripts/check-upstream-versions.mjs
```

## Coverage promise

This skill pack was designed from a source inventory of 224 `quasar-*` skills. Coverage is grouped and mapped in `references/80-legacy-skill-coverage.md` so agents can still search by the old topic names.
