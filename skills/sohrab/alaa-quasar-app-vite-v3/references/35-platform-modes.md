# Platform modes

Use for mode-specific or multi-target Quasar work. First confirm the `@quasar/app-vite` line (`70-...`); v3 changed mode folders/config.

## Routing

| Mode | Concerns | Also load |
|---|---|---|
| SPA | output, lazy loading, routing, SEO trade-offs | `21-cli-vite-and-config.md` |
| SSR | render/hydration/SEO, `ssrContext`, auth mapping, server choice | `31-ssr-pwa-and-security.md` |
| PWA | SW, offline/update/manifest, stale assets | `31-ssr-pwa-and-security.md` |
| BEX | background/content/devtools/popup, bridge, manifest, per-mode `package.json` | `21-cli-vite-and-config.md` |
| Capacitor | native shell, mobile commands/plugins/icons, live-update policy | `21-cli-vite-and-config.md` |
| Cordova | legacy shell/plugins/ecosystem assumptions | `21-cli-vite-and-config.md` |
| Electron | preload/security/Node boundary, packaging/icons | `21-cli-vite-and-config.md` |

## app-vite v3 facts

- Mode dependencies install inside that mode’s `/src-*`; Electron no longer duplicates them into build output.
- SSR scaffolds Hono/Express/Fastify/Koa and adds `/src-ssr/server-assets`.
- BEX requires `/src-bex/package.json` with `"type": "module"`; `chrome` is default (no `-t`). Bridge/file inference were rewritten; Chrome HMR works.
- Capacitor ≤4 was dropped. Replace `capacitor.config.json` with `capacitor.config.ts`/`.js` via `defineCapacitorConfig()`; `quasar dev/build -m ios|android` targets Capacitor.
- Electron packager ≤18 was dropped. Preload uses `.cjs` and `import { quasarRuntime } from '#q-app/electron/preload'`; `/src-electron/electron-assets` and multiple preload scripts are supported.
- SSR dev supports HTTPS; multiple CLI instances may run different modes in one project.

```jsonc
// src-bex/package.json
{ "name": "quasar-bex-app", "version": "1.0.0", "private": true, "type": "module",
  "devDependencies": { "@types/chrome": "^0.1.40" } }
```

In v3 never keep `capacitor.config.json`, a non-`.cjs` Electron preload, or the old `#q-app/electron` preload import.

## Selection/risks

- New mobile: prefer Capacitor unless repo/user requires Cordova. This is inferred from CLI defaults/ecosystem direction, not a Quasar deprecation claim.
- BEX is multi-surface, not SPA-plus-one-file; its messaging, manifest, background/content boundaries, and dynamic assets often change together.
- Electron is frontend + desktop security: context isolation, preload boundary, no remote module.
- SSR+PWA is special because HTML caching interacts with hydration.
- In Yarn repos, prefer Yarn-wrapped mode scripts; do not switch package managers merely because upstream supports Bun/pnpm.
- Mode work usually changes `quasar.config`, so load `21-cli-vite-and-config.md`. Shared source can carry SSR/PWA effects into Capacitor/Cordova/Electron.
- With v3 dependency isolation, one-mode “module not found” may mean wrong install location, not bad code.

For greenfield mobile without Cordova history, scaffold Capacitor; do not add the legacy Cordova shell from memory.
