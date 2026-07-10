# Review and upgrade checklist

Use for reviews, plans, and migration readiness.

## Contents
Repository scan · v2 safety · v3 readiness · SSR · PWA · tests · canonical deltas · migration template.

## 1. Repository scan
- [ ] Lockfile identifies package manager.
- [ ] `@quasar/app-vite` version identified.
- [ ] `quasar` UI version identified.
- [ ] `vue` and `vue-router` versions identified.
- [ ] Modes identified: SPA, PWA, SSR, Capacitor, Electron, BEX.
- [ ] `quasar.config.*` read.
- [ ] Relevant `potential-bugs.md` checked when present.
- [ ] CI/test scripts identified.

Before any nontrivial plan/implementation, emit:

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
- [ ] No new `vite.config.*` in a Quasar CLI app.
- [ ] No generated `.quasar/` edits.
- [ ] No browser-only code in SSR server paths.
- [ ] No client-exposed secrets.
- [ ] No global mutable user/request state.
- [ ] Build/test commands match installed modes.

## 3. v3 readiness
- [ ] New imports prefer `@/` where supported.
- [ ] No new `components/`, `stores/`, `pages/` aliases unless local compatibility requires them.
- [ ] Touched legacy aliases are documented migration debt.
- [ ] Env access is direct/static/codemod-friendly.
- [ ] v2 `process.env.*` is neither destructured nor dynamically indexed.
- [ ] v3-only syntax stays on a migration branch/plan.
- [ ] `#q-app/wrappers` -> `#q-app` is noted, not forced on unsupported v2.
- [ ] Custom PWA SW can move to `src-pwa/sw/` during migration.
- [ ] Node/runtime requirements checked before v3.
- [ ] `vue-router` requirements checked before v3/file routing.

## 4. SSR
- [ ] `window`, `document`, `localStorage`, `sessionStorage`, `navigator` appear only behind client guards/mounted hooks.
- [ ] API-client factories carry request headers/cookies.
- [ ] Pinia/router/app instances are per request.
- [ ] Hydration-sensitive values are deterministic or client-only.
- [ ] Meta uses Quasar/Vue-safe APIs.
- [ ] Server assets and runtime secrets remain server-side.

## 5. PWA
- [ ] SW and main-thread registration are separate.
- [ ] Private/auth/payment APIs are not cached by default.
- [ ] Large VOD/media is not blindly precached.
- [ ] Update UX is defined.
- [ ] Offline UX is defined.
- [ ] Relevant production build gets Lighthouse/PWA audit.

## 6. Tests
- [ ] Lint exists or convention is documented.
- [ ] TS repos typecheck.
- [ ] Unit tests cover changed logic.
- [ ] Component tests mount required Quasar plugins.
- [ ] Practical E2E smoke covers affected critical flow.
- [ ] Every affected mode builds.

## 7. Canonical v2 -> v3 deltas
Verified against the official Quasar CLI with Vite upgrade guide (2026-06-16 snapshot, reconfirmed for stable `3.0.1` on 2026-07-08); refresh for version-sensitive work. v3 has been stable since 3.0.1 (2026-07-07). Use with `10-v2-to-v3-migration.md`.

- Imports: `#q-app/wrappers` -> `#q-app` globally, including `defineConfig`, `defineBoot`, `defineRouter`, `defineStore`, `defineSsrMiddleware`, `definePreFetch`.
- Config extensions: `.js`/`.ts` only; `.cjs`/`.mjs`/`.cts`/`.mts` dropped.
- Constants: `process.env.{DEV,PROD,DEBUGGING,MODE,TARGET,CLIENT,SERVER}` -> `import.meta.env.QUASAR_{DEV,PROD,DEBUG,MODE,TARGET,CLIENT,SERVER}`; confirm doubtful names against the guide.
- Env: `build.envFolder`/`build.envFiles` -> `build.env.folder`/`build.env.file`; `build.env.clientPrefix` defaults `'QCLI_'`, never `'QUASAR_'`; only client-prefixed vars enter the bundle.
- Define: `build.rawDefine` -> `build.define` (non-strings auto-`JSON.stringify`; wrap string literals, e.g. `JSON.stringify('1.0.0')`); v2 `build.env` injection -> `build.defineEnv` (always stringifies and prefixes `import.meta.env.`).
- Defaults/removals: `build.vueOptionsAPI` now `false`; remove `build.analyze` (use `rollup-plugin-visualizer`) and `build.polyfillModulePreload`.
- Aliases: only `@/` -> `/src`; map `src/`->`@/`, `components/`->`@/components/`, `layouts/`->`@/layouts/`, `pages/`->`@/pages/`, `assets/`->`@/assets/`, `boot/`->`@/boot/`, `stores/`->`@/stores/`, `app/`->`@/../`.
- SSR: select Hono/Express/Fastify/Koa; add `/src-ssr/server-assets`; `serve.error()` -> `serve.devError()`.
- PWA: custom SW -> `/src-pwa/sw/`; `sourceFiles.pwaServiceWorker` defaults `'src-pwa/sw/custom-sw'`.
- BEX: `/src-bex/package.json` with `"type": "module"`; default target `chrome`.
- Capacitor: v4 and below dropped; `capacitor.config.json` -> `capacitor.config.ts`/`.js` via `defineCapacitorConfig()`.
- Electron: packager <=18 dropped; preload imports `{ quasarRuntime }` from `#q-app/electron/preload`, preload is `.cjs`, assets move to `/src-electron/electron-assets`.
- Boot: call `redirect()` and return immediately; async is allowed, later execution is not.
- AEs: v2 support removed/new Index API; `quasar <ext-id>` -> `quasar run <ext-id>`.
- Mode isolation: deps install under `/src-*`; pnpm v11 needs `allowBuilds: { rolldown: true, unrs-resolver: true }`.
- Engines/peers: Node 22+; `quasar ^2.16.0`, `vue ^3.2.29`, `vue-router >= 5`, `pinia ^2 || ^3`; Vite 8 + Rolldown underneath.

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
