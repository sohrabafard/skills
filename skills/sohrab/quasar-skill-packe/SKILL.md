---
name: quasar-skill-packe
description: "Use this skill for Quasar CLI + Vite work when the task touches Quasar app setup, quasar.config, SSR/PWA, platform modes (SPA, BEX, Capacitor, Cordova, Electron), Quasar components, layouts, plugins, composables, directives, utils, or Quasar/Vite upgrades. This skill routes the agent to the smallest relevant references, surfaces related topics that are easy to miss, and tells the agent how to refresh live upstream guidance before version-sensitive changes."
---

# Quasar Skill Packe

## Overview

This is a routing-first Quasar skill pack.

Use it when a task is specifically about Quasar or a Quasar-built app. It replaces a large collection of narrow `quasar-*` skills with one focused entry point plus a small set of topic references. The goal is to keep context small while still covering the full Quasar CLI + Vite surface area.

This skill does three jobs:

1. Route the agent to the smallest relevant reference file.
2. Force the agent to load related Quasar topics that are commonly missed.
3. Keep version-sensitive work current by refreshing live upstream data before acting.

## When to use

Use this skill when the task includes any of the following:

- Quasar CLI app setup or migration
- `quasar.config` changes
- Vite integration inside a Quasar app
- SSR, hydration, `ssrContext`, SSR middleware, SEO, or cookie-to-header auth flows
- PWA, service worker, offline fallback, or Workbox InjectManifest
- Platform modes such as SPA, BEX, Capacitor, Cordova, or Electron
- Quasar components, layouts, plugins, composables, directives, options, or utils
- Quasar package/library packaging in a monorepo
- Quasar or Vite upgrade work
- "latest" or version-sensitive Quasar/Vite questions

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
4. If the task is upgrade-related, toolchain-related, or asks for the latest guidance, read `references/70-upstream-deltas-and-live-checks.md` and refresh live data.
5. If the request uses an old `quasar-*` skill name, read `references/80-legacy-skill-coverage.md`.

## Quick routing

- App setup, build config, `quasar.config`, boot files, routing, env files, aliases, proxies, lazy loading, testing, or upgrades:
  - `references/10-cli-vite-and-config.md`
- SSR, hydration, middleware, `ssrContext`, `preFetch`, auth cookies, SEO, PWA, service worker, or offline:
  - `references/20-ssr-pwa-and-security.md`
- SPA vs SSR vs PWA vs BEX vs Capacitor vs Cordova vs Electron:
  - `references/30-platform-modes.md`
- Components or layouts:
  - `references/40-components-and-layouts.md`
- Plugins, composables, directives, options, or utils:
  - `references/50-plugins-composables-directives-options-utils.md`
- A11y, performance, monorepo packaging, tree-shaking, or cross-cutting guardrails:
  - `references/60-guardrails-a11y-performance-monorepo.md`
- Latest versions, migration risk, or skill maintenance:
  - `references/70-upstream-deltas-and-live-checks.md`
- Mapping from legacy single-topic `quasar-*` skills:
  - `references/80-legacy-skill-coverage.md`

## Mandatory related-topic rules

Apply these even if the user only names one Quasar surface:

- Any SSR, `preFetch`, router, store, boot, middleware, SEO, QNoSsr, or auth task:
  - Also load `references/20-ssr-pwa-and-security.md`.
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
- Then search task phrases:
  - `boot files`, `ssrContext`, `InjectManifest`, `BEX Bridge`, `envFolder`, `envFiles`
- If the user mentions an old skill name, search `references/80-legacy-skill-coverage.md`
- If you still are not sure, start with:
  - `references/10-cli-vite-and-config.md`
  - `references/20-ssr-pwa-and-security.md`

## Current live snapshot

This snapshot was refreshed on March 25, 2026 and will age over time:

- Quasar: `2.19.1` (published March 24, 2026)
- `@quasar/app-vite`: `2.5.4` (published March 24, 2026)
- Vite: `8.0.2` (published March 23, 2026)
- Vue: `3.5.31` (published March 25, 2026)
- Vue Router: `5.0.4`
- Workbox: `7.4.0`

Refresh this snapshot before any version-sensitive work by running:

```bash
node scripts/check-upstream-versions.mjs
```

## Coverage promise

This skill pack was designed from a source inventory of 224 `quasar-*` skills. Coverage is grouped and mapped in `references/80-legacy-skill-coverage.md` so agents can still search by the old topic names.
