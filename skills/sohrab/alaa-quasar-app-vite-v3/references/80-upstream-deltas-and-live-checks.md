# Upstream Deltas and Live Checks

Use for “latest”, upgrade, migration, or maintenance work.

## Refresh, authority, freshness

Run `node scripts/check-upstream-versions.mjs`. Manual fallback:

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

Yarn repos may use `yarn info <pkg> version`; the script is preferred because its stable summary is package-manager-neutral.

Authority, highest first: (1) repo `quasar.config`, `package.json`, lockfile, boot/SSR/PWA files, tests—installed `@quasar/app-vite` decides the line; (2) official Quasar docs/CLI-Vite upgrade guide; (3) official Vite/Vue/Router/Pinia/Workbox docs; (4) official npm metadata, GitHub releases, migrations/changelogs; (5) community material only as troubleshooting leads. Community examples never override installed-version or official guidance.

Recheck official sources for “latest/current/upgrade/migration/security/CVE/breaking”; Quasar CLI/Vite/Vue/Router/Pinia/Workbox/Node/package-manager changes; SSR middleware, PWA SW, BEX bridge, Electron/Capacitor, or config-format changes; production-only dev/build mismatches.

## Snapshot: 2026-07-10 npm registry

| Package/line | Stable snapshot |
| --- | --- |
| `quasar` | `2.21.1` |
| `@quasar/app-vite` production | `3.0.1`, published 2026-07-07, `latest`; v3 is production/default for new apps |
| `@quasar/app-vite` maintenance | `2.6.2`, published 2026-06-03, supported approximately until 2027-06 |
| `@quasar/extras` | `2.0.2`, ESM-only with icon-library cuts—audit before bumping |
| `vite` / `vue` / `vue-router` / `pinia` | `8.1.4` / `3.5.39` / `5.1.0` / `3.0.4` (`pinia` v2 or v3 accepted by app-vite v3) |
| `workbox-build` | `7.4.1` |

Stable-first: use stable v3 for new production apps. Migrate v2 deliberately via `10-v2-to-v3-migration.md`, never incidentally; until then pin `^2`. This snapshot expires: the 2026-06-16 snapshot (`3.0.0-rc.3`) became stable v3 within three weeks, so rerun the script.

## Detect app-vite v2 vs v3 first

The two live lines have incompatible imports, config/env/aliases, and folders. Read `package.json` + lockfile before config, boot, env, alias, SSR, PWA, BEX, Electron, or Capacitor advice.

| Signal | `^2.x` maintenance | `^3.x` stable/production |
| --- | --- | --- |
| Latest/status | `2.6.2`, approximately through 2027-06-11 | `3.0.1` since 2026-07-07, `latest`, new-app default |
| Wrapper | `#q-app/wrappers` | `#q-app` |
| Config extensions | `.js` `.mjs` `.ts` `.cjs` | `.js` `.ts` only |
| Constants | `process.env.MODE`, `process.env.DEV`, etc. | `import.meta.env.QUASAR_MODE`, `import.meta.env.QUASAR_DEV`, etc. |
| Env | `build.envFolder`, `build.envFiles` | `build.env.folder`, `build.env.file`, `build.env.clientPrefix` |
| Defines | `build.rawDefine`, `build.env` | `build.define`, `build.defineEnv` |
| Aliases | `src/`, `components/`, `boot/`, `stores/`, `app/`, etc. | `@/` only (`@/components/`, `@/../`, etc.) |
| CLI bundler | esbuild for `/src-*` | Rolldown for `/src-*` |
| Custom SW | `/src-pwa/custom-sw` | `/src-pwa/sw/custom-sw` |
| SSR server | Express scaffold | Hono/Express/Fastify/Koa choice |
| Node floor | 18+ | 22+ (registry floor `22.22.0`) |

✅ Do — report the detected line and use only its shapes. ❌ Don't — mix `#q-app/wrappers` and `#q-app`; each breaks the other line. Match installed repos; if truly unknown/greenfield, explicitly assume stable v3.

```ts
import { defineBoot } from '#q-app/wrappers' // breaks v3
import { defineBoot } from '#q-app' // breaks v2
```

## app-vite v3 breaking summary

Full migration: `10-v2-to-v3-migration.md`; verified deltas: `11-review-and-upgrade-checklist.md`; exact shapes: `22-cli-cookbook-and-examples.md`. Migrate deliberately.

- Imports/aliases: `#q-app/wrappers` → `#q-app`; aliases → `@/` (`components/` → `@/components/`, `app/` → `@/../`).
- Config: `.js`/`.ts` only; `build.vueOptionsAPI` defaults `false`; `build.analyze`/`build.polyfillModulePreload` removed.
- Env/defines: `build.envFolder`/`envFiles` → `build.env.{folder,file}` + `build.env.clientPrefix` (default `'QCLI_'`); the legacy `process.env.QUASAR-constants` pattern → `import.meta.env.QUASAR_*`; `rawDefine`/`env` → `define`/`defineEnv`.
- Modes: SSR chooses Hono/Express/Fastify/Koa + `serve.devError()`; PWA SW → `/src-pwa/sw/`; BEX needs `/src-bex/package.json`; Capacitor uses `defineCapacitorConfig()`; Electron preload uses `#q-app/electron/preload` and `.cjs`.
- Runtime: Node 22+; `vue-router >= 5`; `pinia ^2 || ^3`; Vite 8 + Rolldown.

## Framework/tool deltas

### Quasar `2.20.x–2.21.x`

Framework and CLI version independently; framework is `2.21.1`. `2.20.0` made UI smaller/faster, improved Rolldown API use, removed legacy Vetur build. `Cookies` expiry changed from `expires` to `MaxAge`. Fixes: `QPopupProxy` false `update:modelValue`, `QDrawer` `hideOnRouteChange`, `QInput type="number"` label overlap, `QDialog` backdrop a11y. `2.21.0`: QTable instance method `getCellValue(colName, row)`, `lb` language pack, language/icon audits. `2.21.1`: Safari macOS page-scroll loss after CSS-based `QDialog` close fixed. No components/deprecations from 2.19–2.21.

### Quasar UI v3

Only planned (input Q3–Q4 2026; hoped Q1 2027), not beta/RC. Do not confuse it with stable CLI `@quasar/app-vite` v3; clarify “Quasar 3”.

### Vite 8 (`8.1.4`)

- Prebundling: Rolldown; `optimizeDeps.esbuildOptions` deprecated/auto-mapped to `optimizeDeps.rolldownOptions`. JS/Oxc replaces esbuild (`oxc`; `build.minify: 'esbuild'` deprecated). CSS defaults to Lightning CSS; escape hatch `build.cssMinify: 'esbuild'`.
- CommonJS default-import may break; escape hatch `legacy.inconsistentCjsInterop: true`. Object `manualChunks` removed; function deprecated for `codeSplitting`.
- `build.rollupOptions` → `build.rolldownOptions` and `worker.rollupOptions` → `worker.rolldownOptions` (deprecated compatibility remains). `rolldown-vite` merged into Vite 8.
- Node remains 20.19+ or 22.12+ (app-vite v3 effectively 22+). Targets: Chrome/Edge 111, Firefox 114, Safari 16.4. Rolldown warns more strictly on circular imports.

### Vue Router 5

Standard 4→5 is nonbreaking; it merges `unplugin-vue-router`. Only IIFE/CDN loses bundled devtools API (irrelevant to bundled Quasar). File routing renames: `unplugin-vue-router/vite` → `vue-router/vite`; `unplugin-vue-router` → `vue-router/unplugin`; data loaders → `vue-router/experimental`. app-vite v3 supports Router 5 filename routing; default programmatic `src/router/` remains unaffected.

### Vue 3.5 / Workbox 7.4

Vue (`3.5.39`): SSR-stable `useId()`; scoped `data-allow-mismatch` (`text`, `children`, `class`, `style`, `attribute`); async-component lazy hydration; `useTemplateRef()`; reactive props destructure. Workbox `7.4.0`/`7.4.1`: maintenance/security dependency bumps + Rollup v4, no InjectManifest/GenerateSW behavior change; safe bump.

## Maintenance and package managers

For dual-runtime editing use `references/91-agent-authoring-and-dual-runtime.md`: keep the routing `SKILL.md` body well under 500 lines; accurate `name`/`description`; literal scoped conflict-free rules; precedence for conflicts; do/don't pairs; no all-caps `CRITICAL`/`MUST` urgency; scripts only for deterministic/repeated refresh.

Keep a repo's manager (Yarn/workspaces or `yarn.lock` means Yarn); registry queries discover versions, not manager policy. pnpm v11 + app-vite v3 needs the previously documented `allowBuilds` entries.

Docs: Vite `vite.dev/llms.txt` and `vite.dev/llms-full.txt`; stable `vite.dev` (not ahead-of-release `main.vite.dev`); Quasar docs for API plus releases/npm for freshness; upgrade guide `quasar.dev/quasar-cli-vite/upgrade-guide/`.
