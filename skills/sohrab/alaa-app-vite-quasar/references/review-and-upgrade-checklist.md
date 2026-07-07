# Review and Upgrade Checklist

Use this checklist for code reviews, planning, or migration readiness reviews.

## 1. Fast repository scan

- [ ] Package manager identified from lockfile.
- [ ] `@quasar/app-vite` version identified.
- [ ] `quasar` UI version identified.
- [ ] `vue` and `vue-router` versions identified.
- [ ] Supported modes identified: SPA, PWA, SSR, Capacitor, Electron, BEX.
- [ ] `quasar.config.*` read.
- [ ] `potential-bugs.md` checked when present and relevant.
- [ ] Existing CI/test scripts identified.

For any nontrivial task, emit a concise assessment before the plan or implementation:

```md
Repo assessment:
- Package manager:
- @quasar/app-vite:
- quasar:
- vue / vue-router:
- Modes detected: SPA / SSR / PWA / Capacitor / Electron / BEX
- Current env model: process.env / import.meta.env / mixed
- Alias style: @/ / src / components / mixed
- Testing harnesses:
- Risk flags:

Plan:
1. ...

Validation:
- ...

v3-readiness notes:
- ...
```

## 2. v2 production safety

- [ ] No accidental app-vite v3 upgrade.
- [ ] No unreviewed lockfile churn.
- [ ] No new `vite.config.*` in Quasar CLI app.
- [ ] No generated `.quasar/` edits.
- [ ] No new browser-only code in SSR server path.
- [ ] No client-exposed secrets.
- [ ] No global mutable user/request state.
- [ ] Build/test commands are appropriate for installed mode(s).

## 3. v3-readiness checks

- [ ] New source imports prefer `@/` where repo supports it.
- [ ] No new old-alias imports like `components/`, `stores/`, `pages/` unless preserving local convention is necessary.
- [ ] Existing old-alias imports are documented as migration debt if touched.
- [ ] Env usage is direct/static and easy to codemod.
- [ ] `process.env.*` v2 constants are not destructured or dynamically indexed.
- [ ] Any v3-only syntax is isolated to a migration branch or plan.
- [ ] `#q-app/wrappers` to `#q-app` migration is noted but not forced on v2 unless supported.
- [ ] PWA custom service worker layout is ready to move to `src-pwa/sw/` during v3 migration.
- [ ] Node/runtime constraints are checked before v3.
- [ ] `vue-router` constraints are checked before v3/file-based routing.

## 4. SSR checklist

- [ ] No `window`, `document`, `localStorage`, `sessionStorage`, `navigator` outside client-only guards or mounted hooks.
- [ ] Factories used for API clients with request-specific headers/cookies.
- [ ] Pinia/router/app instances are per request.
- [ ] Hydration-sensitive values are deterministic or client-only.
- [ ] SEO meta handling uses Quasar/Vue-safe APIs.
- [ ] Server assets and runtime secrets stay server-side.

## 5. PWA checklist

- [ ] Service worker and main-thread registration code are separated.
- [ ] Private/auth/payment APIs are not cached by default.
- [ ] Large VOD/media assets are not blindly precached.
- [ ] Update UX is defined.
- [ ] Offline UX is defined.
- [ ] Lighthouse/PWA audit is run on production build when relevant.

## 6. Testing checklist

- [ ] Lint command exists or repo convention documented.
- [ ] Typecheck command exists for TypeScript repos.
- [ ] Unit tests cover changed logic.
- [ ] Component tests mount Quasar plugins where needed.
- [ ] E2E smoke tests cover affected critical flow when practical.
- [ ] Mode builds run for each affected mode.

## 7. Verified v2 -> v3 breaking-change deltas (authoritative)

This is the canonical delta list for this pack. Verified against the official Quasar CLI with Vite upgrade guide (snapshot 2026-06-16, re-confirmed against the stable `3.0.1` guide on 2026-07-08; re-verify for version-sensitive work). v3 is stable since `3.0.1` (2026-07-07) — use this list to execute migrations planned via `$alaa-quasar-app-vite-v3` and to maintain v3 repos.

- Wrapper import: `#q-app/wrappers` -> `#q-app` (global search/replace; affects `defineConfig`, `defineBoot`, `defineRouter`, `defineStore`, `defineSsrMiddleware`, `definePreFetch`).
- `quasar.config` extensions: `.js`/`.ts` only (`.cjs`/`.mjs`/`.cts`/`.mts` dropped).
- Quasar constants: `process.env.{DEV,PROD,DEBUGGING,MODE,TARGET,CLIENT,SERVER}` -> `import.meta.env.QUASAR_{DEV,PROD,DEBUG,MODE,TARGET,CLIENT,SERVER}` (same `QUASAR_` prefix pattern; confirm exact names against the upgrade guide if in doubt).
- Env config: `build.envFolder`/`build.envFiles` -> `build.env.folder`/`build.env.file`; new `build.env.clientPrefix` (default `'QCLI_'`; do not use `'QUASAR_'`). Only client-prefixed vars reach the client bundle.
- Define: `build.rawDefine` -> `build.define` (non-string values are auto-`JSON.stringify`ed, like a friendlier Vite `define`; wrap string literals yourself, e.g. `JSON.stringify('1.0.0')`); `build.env` -> `build.defineEnv` (sugar that always stringifies and prefixes keys with `import.meta.env.`).
- Defaults: `build.vueOptionsAPI` now `false`; `build.analyze` removed (use `rollup-plugin-visualizer`); `build.polyfillModulePreload` removed.
- Path aliases: only `@/` remains (-> `/src`). `src/`->`@/`, `components/`->`@/components/`, `layouts/`->`@/layouts/`, `pages/`->`@/pages/`, `assets/`->`@/assets/`, `boot/`->`@/boot/`, `stores/`->`@/stores/`, `app/`->`@/../`.
- SSR: scaffold picks Hono / Express / Fastify / Koa; new `/src-ssr/server-assets`; middleware hook `serve.error()` -> `serve.devError()`.
- PWA: custom SW moves to `/src-pwa/sw/`; config key `sourceFiles.pwaServiceWorker` defaults to `'src-pwa/sw/custom-sw'`.
- BEX: requires `/src-bex/package.json` (`"type": "module"`); defaults to the `chrome` target.
- Capacitor: v4 and below dropped; `capacitor.config.json` -> `capacitor.config.ts`/`.js` via `defineCapacitorConfig()`.
- Electron: packager v18 and below dropped; preload `import { quasarRuntime } from '#q-app/electron/preload'`, preload files `.cjs`; new `/src-electron/electron-assets`.
- Boot `redirect()` must return immediately after the call (may be async, but return right after).
- App Extensions: v2 support removed (new Index API); `quasar <ext-id>` -> `quasar run <ext-id>`.
- Per-mode dependency isolation: mode deps install in `/src-*` folders; pnpm v11 needs `allowBuilds: { rolldown: true, unrs-resolver: true }`.
- Engines/peers: Node 22+; peers `quasar ^2.16.0`, `vue ^3.2.29`, `vue-router >= 5`, `pinia ^2 || ^3`. Under the hood: Vite 8 + Rolldown.

## 8. Migration plan template

```md
# app-vite v3 Migration Plan

## Current state
- @quasar/app-vite:
- quasar:
- Node:
- package manager:
- modes:

## Blocking requirements
- Node/runtime:
- vue-router:
- package manager:
- CI images:

## Required source migrations
- #q-app/wrappers -> #q-app:
- aliases -> @/:
- process.env -> import.meta.env.QUASAR_*:
- quasar.config build/env changes:
- mode-specific package.json moves:
- PWA src-pwa/sw changes:
- SSR architecture changes:
- Capacitor config changes:

## Risk assessment
- Production risk:
- SSR/PWA risk:
- CI/CD risk:
- rollback plan:

## Validation matrix
- SPA build:
- PWA build:
- SSR build/start:
- unit tests:
- e2e smoke:
- manual QA:
```
