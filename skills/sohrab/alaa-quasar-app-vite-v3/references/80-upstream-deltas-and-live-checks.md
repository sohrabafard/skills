# Upstream deltas, version truth, and live checks

You are about to state a version number, plan an upgrade, execute a migration, or maintain this skill. This file is the **single home** of every upstream version fact and of the canonical v2 -> v3 delta table. No other file in this pack restates a version number; where one is needed, it points here.

## 1. Refresh before answering

```bash
node <skill-dir>/scripts/check-upstream-versions.mjs
node <skill-dir>/scripts/check-upstream-versions.mjs --help
node <skill-dir>/scripts/check-upstream-versions.mjs --self-test
```

Exit codes: `0` clean, `2` one or more packages could not be fetched (the rest are still printed), `3` bad usage. Treat `2` as "could not run", never as "clean". Manual fallback when the script cannot run:

```bash
npm view @quasar/app-vite dist-tags
npm view "@quasar/app-vite@^2" version
npm view quasar version
npm view vite version
npm view vue version
npm view vue-router version
npm view pinia version
npm view workbox-build version
```

Yarn repos may use `yarn info <pkg> version`; the script is preferred because its summary is package-manager-neutral.

Authority, highest first: (1) the repo — `quasar.config`, `package.json`, lockfile, boot/SSR/PWA files, tests; the **installed** `@quasar/app-vite` decides the line; (2) official Quasar docs and the CLI-Vite upgrade guide; (3) official Vite/Vue/Router/Pinia/Workbox docs; (4) npm registry metadata, GitHub releases, changelogs; (5) community material as troubleshooting leads only. A community example never overrides installed-version or official guidance.

Recheck official sources whenever the question contains "latest", "current", "upgrade", "migration", "security", "CVE", or "breaking"; whenever Quasar CLI, Vite, Vue, Router, Pinia, Workbox, Node, or the package manager changes; whenever SSR middleware, the PWA service worker, the BEX bridge, Electron/Capacitor packaging, or a config format changes; and whenever dev and production disagree.

## 2. Snapshot: npm registry, read 2026-07-28

| Package / line | Stable | Published | Note |
| --- | --- | --- | --- |
| `@quasar/app-vite` production | `3.2.0` | 2026-07-22 | holds `latest`; new-app default. 3.1.0 landed 2026-07-21 |
| `@quasar/app-vite` maintenance | `2.6.2` | 2026-06-03 | supported approximately until 2027-06 |
| `quasar` (UI) | `2.23.3` | 2026-07-28 | versioned independently of the CLI |
| `@quasar/extras` | `2.0.2` | 2026-07-02 | ESM-only; icon-library cuts require an audit |
| `vite` | `8.1.5` | 2026-07-16 | app-vite 3.2.0 depends on `vite ^8.1.5` |
| `vue` | `3.5.40` | 2026-07-16 | — |
| `vue-router` | `5.2.0` | 2026-07-15 | v5 required by app-vite v3 |
| `pinia` | `4.0.2` | 2026-07-15 | see the peer range below |
| `workbox-build` / `workbox-core` | `7.4.1` | 2026-05-04 | — |

Peer and engine ranges declared by `@quasar/app-vite@3.2.0`, read from the registry manifest on 2026-07-28:

```text
node       ^22.22.0 || ^24 || ^26 || ^28 || ^30
quasar     ^2.21.3
vue        ^3.2.29
vue-router >= 5
pinia      ^2.0.0 || ^3.0.0 || ^4.0.0   (optional peer)
workbox-build >= 7                       (optional peer)
typescript >= 5                          (optional peer)
@capacitor/cli >= 5                      (optional peer)
@electron/packager >= 19; electron-builder >= 22
```

**Pinia 4 is accepted by app-vite 3.2.0.** Do not tell a team the range is `^2 || ^3`; that was the 3.0.x range. Re-read the peer block of the installed version before advising a Pinia bump.

This snapshot expires. Between 2026-07-10 and 2026-07-28 app-vite moved 3.0.1 -> 3.2.0 and Quasar UI moved 2.21.1 -> 2.23.3. Run the script before quoting any number.

## 3. Detect the installed major before any shape advice

Read `package.json` and the lockfile before giving config, boot, env, alias, SSR, PWA, BEX, Electron, or Capacitor advice. A declared range is not proof of the installed version.

| Signal | `^2.x` maintenance | `^3.x` production |
| --- | --- | --- |
| Wrapper import | `#q-app/wrappers` | `#q-app` |
| Config extensions | `.js` `.mjs` `.ts` `.cjs` | `.js` `.ts` only |
| Constants | `process.env.MODE`, `process.env.DEV`, ... | `import.meta.env.QUASAR_MODE`, `import.meta.env.QUASAR_DEV`, ... |
| Env config | `build.envFolder`, `build.envFiles` | `build.env.folder`, `build.env.file`, `build.env.clientPrefix` |
| Defines | `build.rawDefine`, `build.env` injection | `build.define`, `build.defineEnv` |
| Aliases | `src/`, `components/`, `boot/`, `stores/`, `app/`, ... | `@/` only |
| CLI bundler for `/src-*` | esbuild | Rolldown |
| Custom service-worker folder | `/src-pwa/` | `/src-pwa/sw/` |
| SSR server | Express scaffold | Hono / Express / Fastify / Koa choice |
| Node floor | 18+ | 22+ (registry floor `22.22.0`) |

The exact `sourceFiles.pwaServiceWorker` default is owned by `references/32-pwa-injectmanifest-guard.md`; read it there rather than restating it.

✅ Do — report the detected line and use only its shapes. ❌ Don't — mix `#q-app/wrappers` and `#q-app`; each breaks the other line.

```ts
import { defineBoot } from '#q-app/wrappers' // breaks v3
import { defineBoot } from '#q-app'          // breaks v2
```

If the repo is greenfield and no line exists yet, state the assumption explicitly and use v3.

## 4. Canonical v2 -> v3 delta table

This is the only complete statement of the delta set in this pack. Migration sequence and failure recovery: `references/10-v2-to-v3-migration.md`. Executable shapes: `references/22-cli-cookbook-and-examples.md`. Env semantics: `references/20-v3-config-and-features.md`.

| Area | v2 | v3 |
| --- | --- | --- |
| Wrappers | `#q-app/wrappers` (`defineConfig`, `defineBoot`, `defineRouter`, `defineStore`, `defineSsrMiddleware`, `definePreFetch`) | `#q-app` |
| Config file | `.js` `.mjs` `.ts` `.cjs` `.cts` `.mts` | `.js` or `.ts` only |
| Constants | `process.env.{DEV,PROD,DEBUGGING,MODE,TARGET,CLIENT,SERVER}` | `import.meta.env.QUASAR_{DEV,PROD,DEBUG,MODE,TARGET,CLIENT,SERVER}` plus `QUASAR_<MODE>_MODE` flags |
| `index.html` | `<%= process.env.MY_VAR %>` | `<%= importMetaEnv.MY_VAR %>` or `%MY_VAR%` |
| Env config | `build.envFolder`, `build.envFiles`, `build.envFilter` | `build.env.{folder,file,filter,clientPrefix,backendPrefix}`; `clientPrefix` defaults `'QCLI_'` |
| Defines | `build.rawDefine`; `build.env` value injection | `build.define`; `build.defineEnv` |
| Options API | `build.vueOptionsAPI` defaults `true` | defaults `false` |
| Removed build keys | `build.analyze`, `build.polyfillModulePreload`, `cordova.noIosLegacyBuildFlag` | use `rollup-plugin-visualizer` through `build.vitePlugins` |
| Aliases | `src/`, `app/`, `components/`, `layouts/`, `pages/`, `assets/`, `boot/`, `stores/` | sole `@/` -> `/src`; templates use `~@/assets/...` |
| Renamed hooks | `ssr.extendPackageJson`, `pwa.extendManifestJson`, `pwa.injectPwaMetaTags`, `pwa.extendGenerateSWOptions`, `pwa.extendInjectManifestOptions`, `electron.extendPackageJson` | `ssr.extendSSRPackageJson`, `pwa.extendPWAManifestJson`, `pwa.injectPWAMetaTags`, `pwa.extendPWAGenerateSWOptions`, `pwa.extendPWAInjectManifestOptions`, `electron.extendElectronPackageJson` |
| SSR | Express scaffold; `serve.error()` | Hono/Express/Fastify/Koa; `serve.devError()`; `/src-ssr/server-assets` + `resolve.serverAssets()`; webserver built by Rolldown |
| PWA | custom SW in `/src-pwa/` | custom SW in `/src-pwa/sw/`; `/src-pwa/sw/tsconfig.json` extends `../../.quasar/tsconfig.pwa-sw.json`; ESLint glob `src-pwa/sw/**/*.ts` |
| BEX | — | `/src-bex/package.json` with `"type": "module"`; default target `chrome` |
| Capacitor | `capacitor.config.json`; Capacitor <= 4 supported | `capacitor.config.ts`/`.js` via `defineCapacitorConfig()` from `'@quasar/app-vite/capacitor'`; Capacitor <= 4 dropped; the `capacitor` config section loses `appName`, `version`, `description` |
| Electron | packager <= 18 | packager >= 19; preload is `.cjs`; `quasarRuntime` from `#q-app/electron/preload`; `registerQuasarRuntime` from `#q-app/electron/main`; assets in `/src-electron/electron-assets` |
| Boot redirects | thrown `{ url }` or Promise-carried redirect | call `redirect()` and return immediately |
| App Extensions | v2 Index API | `api.compatibleWith('@quasar/app-vite', '^3.0.0')`; `quasar <ext-id> <cmd>` -> `quasar run <ext-id> <cmd>` |
| Mode isolation | shared install | dependencies install under `/src-<mode>`; pnpm v11 needs `allowBuilds` for `rolldown` and friends plus an empty per-mode `pnpm-workspace.yaml` |
| Extend hooks | esbuild configs | `extendSSRWebserverConf`, `extendElectronMainConf`, `extendElectronPreloadConf` receive Rolldown configs; every `extendX()` may be async or return a merge object; `ctx.logger` is available |
| TypeScript | scattered `.d.ts`, `src-pwa/tsconfig.json`, `declare namespace NodeJS` | one root `/env.d.ts` declaring `interface ImportMetaEnv`; `quasar prepare` regenerates `.quasar/` tsconfigs |
| CLI | — | `--no-color` on every command; `quasar build --no-summary`; BEX `-t/--target` defaults `chrome` |

## 5. Framework and tool deltas

### Quasar UI 2.18 -> 2.23

- 2.18: QTable `table-row-style-fn`, `table-row-class-fn`, `grid-style-fn`, `grid-class-fn`; QMenu/QBtnDropdown `no-esc-dismiss`; `evt.qAvoidFocus`; pure-CSS icons.
- 2.19: Rolldown/lightningcss/oxlint modernisation; Baseline widely-available floor (Chrome/Edge 111+, Firefox 114+, Safari/iOS 16.4+); `date/getMinDate`/`getMaxDate` return `Date` — a behaviour change.
- 2.20: smaller and faster build; `Cookies` switched from `expires` to `Max-Age`; `QPopupProxy` no longer emits `update:modelValue` from `useAnchor()`.
- 2.21: QTable `getCellValue(colName, row)`; 2.21.1 fixed Safari page-scroll loss after a CSS-based QDialog close.
- **2.22.0 (2026-07-21) and 2.23.0-2.23.3 (2026-07-24 to 2026-07-28) are not yet read.** Their release notes are UNVERIFIED here; read them live before asserting that a component, prop, or deprecation does or does not exist in 2.22 or later, and before claiming that nothing changed.

### Quasar UI v3

Planned only (input Q3-Q4 2026; hoped Q1 2027); no beta or RC on the registry. Do not confuse it with the stable CLI `@quasar/app-vite` v3. When a user says "Quasar 3", ask which one they mean.

### Vite 8

Prebundling uses Rolldown; `optimizeDeps.esbuildOptions` is deprecated and auto-mapped to `optimizeDeps.rolldownOptions`. Oxc replaces esbuild for JS transform and minify (`build.minify: 'esbuild'` deprecated). CSS minification defaults to Lightning CSS; escape hatch `build.cssMinify: 'esbuild'`. CommonJS default-import interop is stricter; escape hatch `legacy.inconsistentCjsInterop: true`. `build.rollupOptions` -> `build.rolldownOptions` and `worker.rollupOptions` -> `worker.rolldownOptions`, old names deprecated-compatible. Object-form `manualChunks` is removed and the function form is deprecated for `codeSplitting`; the code pair is in `references/70-guardrails-a11y-performance-monorepo.md`. Default targets rose to Chrome 111 / Firefox 114 / Safari 16.4. Rolldown warns more strictly on circular imports.

### Vue Router 5

Standard 4 -> 5 is non-breaking and merges `unplugin-vue-router`. Only IIFE/CDN loses the bundled devtools API, which is irrelevant to bundled Quasar. File-routing renames: `unplugin-vue-router/vite` -> `vue-router/vite`; `unplugin-vue-router` -> `vue-router/unplugin`; data loaders -> `vue-router/experimental`. app-vite v3 supports Router 5 filename routing through `build.filenameBasedRouting`; the default programmatic `src/router/` is unaffected.

### Vue 3.5 and Workbox 7.4

Vue 3.5: SSR-stable `useId()`; scoped `data-allow-mismatch` (`text`, `children`, `class`, `style`, `attribute`); async-component lazy hydration; `useTemplateRef()`; reactive props destructure. Workbox 7.4.0/7.4.1 are maintenance and security dependency bumps plus Rollup v4, with no `InjectManifest` or `GenerateSW` behaviour change — a safe bump.

## 6. Verify live before answering

- Any "latest", "current", or post-snapshot claim.
- Quasar UI 2.22 and 2.23 release notes (see above).
- `@quasar/app-vite` 3.1 and 3.2 changelogs: config keys added or changed since 3.0, and whether §4 is still complete.
- Browser claims in `30`, `40`, `45`, dated 2026-07-08: Baseline status, iOS/Safari cadence, permission UI, grant expiry, auto-revocation, `<geolocation>` rollout.
- Still UNVERIFIED at 2026-07-28: Static Routing API outside Chromium; Declarative Web Push in Chromium; `@quasar/testing-*` extension v3 compatibility; the exact default dotenv file list; exact Safari grant-expiry windows; the `<geolocation>` recovery percentage; camera and microphone permission elements.
- **Resolved on 2026-07-28:** `@quasar/app-vite@3.2.0` still declares `bin: { quasar: "./bin/quasar.js" }` (registry manifest), and `quasar describe` ran against the live `client` checkout on installed 3.0.0. The exact-API authority chain in `references/05-authority-and-api-lookup.md` holds. Re-check this whenever a new app-vite major appears.

Use only quasar.dev, the `quasarframework/quasar` GitHub releases, the npm registry, MDN, web.dev, developer.chrome.com, and webkit.org. A community post is a troubleshooting hint, never a migration rule.

## 7. Skill maintenance

- When any upstream version, import path, config key, or folder changes: search the whole pack for the old string and update every occurrence plus the snapshot date in §2. Updating only the snapshot leaves the pack contradicting itself.
- Never snapshot component, directive, or plugin API output into a file. `scripts/query-installed-quasar-api.mjs` stays version-neutral and delegates to the target project's own CLI.
- If `latest` for `@quasar/app-vite` becomes v4, reassess the whole posture of this skill, not only the numbers.
- After changing `scripts/query-installed-quasar-api.mjs`: run `--self-test`, then run it against one installed app-vite v2 project and one v3 project, confirm the reported app-vite and Quasar versions match the projects' package metadata, confirm the missing-project failure message is actionable, and run both a narrow symbol query and a `list` query — one output shape is insufficient.
- After changing `scripts/check-upstream-versions.mjs`: run `--self-test`, then a live run, and confirm that a single unreachable package still prints the other results and exits `2`.

## 8. Posture history

- 2026-07-06/07: app-vite `3.0.0` then `3.0.1`; v3 became stable after beta and RC from 2026-05-06. v2 `2.6.2` entered maintenance, approximately through 2027-06.
- 2026-07-08: absorbed the retired `quasar-skill-packe` (Quasar shapes, atlases, modes, guardrails) and `alaa-app-vite-quasar` (v2 playbook, deltas, testing, CI).
- 2026-07-10: became a control plane rather than an API mirror — exact APIs route to the project-local `quasar describe`; atlases keep intent, alternatives, gotchas, and search vocabulary; no MCP is required.
- 2026-07-28: the SSR/PWA playbook (33) and the maintenance file (90) were retired into this file and into `30`/`31`/`32`/`22`; failure, observability, step-up, and operations references added; the delta set and the version snapshot consolidated here.

## 9. Package managers

A repo's package manager is a contract: a Yarn workspace or `yarn.lock` means Yarn. Registry queries discover versions, not manager policy; upstream support for Bun or pnpm never justifies switching during a Quasar task. pnpm v11 with app-vite v3 needs the `allowBuilds` entries in §4.

Docs: `vite.dev/llms.txt` and `vite.dev/llms-full.txt`; stable `vite.dev`, not the ahead-of-release `main.vite.dev`; Quasar docs for API plus releases and npm for freshness; the upgrade guide at `quasar.dev/quasar-cli-vite/upgrade-guide/`.

Search: `latest version`, `dist-tags`, `peer range`, `pinia 4`, `Node engines`, `v2 v3 delta`, `Rolldown`, `Oxc`, `Lightning CSS`, `rolldownOptions`, `filenameBasedRouting`, `serve.devError`, `defineCapacitorConfig`, `upgrade guide`.
