# Platform modes

You are about to add or change a Quasar mode, ship to more than one target, or explain a failure that appears in one mode only. Confirm the installed `@quasar/app-vite` line first — `references/80-upstream-deltas-and-live-checks.md` §3 — because v3 changed mode folders and mode config.

## Mode pairings

This table pairs a mode with the files that answer mode-specific questions. Skill-level routing is `references/00-topic-map.md`.

| Mode | Concerns | Also load |
|---|---|---|
| SPA | output, lazy loading, routing, SEO trade-offs | `references/21-cli-vite-and-config.md` |
| SSR | render and hydration, SEO, `ssrContext`, auth mapping, server choice, render failure | `references/31-ssr-pwa-and-security.md`, `references/34-frontend-failure-and-degradation.md` |
| PWA | service worker, offline, update, manifest, stale assets | `references/32-pwa-injectmanifest-guard.md`, then `references/30-service-worker-excellence.md` |
| BEX | background, content, devtools, popup, bridge, manifest, per-mode `package.json` | `references/21-cli-vite-and-config.md` |
| Capacitor | native shell, mobile commands, plugins, icons, live-update policy | `references/21-cli-vite-and-config.md`, `references/45-browser-apis-and-permissions.md` §5 |
| Cordova | legacy shell, plugins, ecosystem assumptions | `references/21-cli-vite-and-config.md` |
| Electron | preload and Node boundary, packaging, icons | `references/21-cli-vite-and-config.md` |

## app-vite v3 mode facts

- Mode dependencies install inside that mode's `/src-<mode>` folder; Electron no longer duplicates them into the build output.
- SSR scaffolds Hono, Express, Fastify, or Koa and adds `/src-ssr/server-assets`.
- BEX requires `/src-bex/package.json` with `"type": "module"`; `chrome` is the default target, so `-t` is not needed for it. The bridge and file inference were rewritten and Chrome HMR works.
- Capacitor 4 and below were dropped. Replace `capacitor.config.json` with `capacitor.config.ts` or `.js` via `defineCapacitorConfig()`; `quasar dev|build -m ios|android` targets Capacitor.
- Electron packager 18 and below were dropped. The preload is `.cjs` and imports `{ quasarRuntime }` from `#q-app/electron/preload`; `/src-electron/electron-assets` and multiple preload scripts are supported.
- SSR dev supports HTTPS, and multiple CLI instances may run different modes in one project.

```jsonc
// src-bex/package.json
{ "name": "quasar-bex-app", "version": "1.0.0", "private": true, "type": "module",
  "devDependencies": { "@types/chrome": "^0.1.40" } }
```

In v3, never keep `capacitor.config.json`, a non-`.cjs` Electron preload, or the old `#q-app/electron` preload import. The full delta table is `references/80-upstream-deltas-and-live-checks.md` §4.

## Selection and risks

- New mobile work uses Capacitor unless the repository or the user requires Cordova. This follows the CLI defaults and ecosystem direction; it is not a Quasar deprecation claim.
- BEX is multi-surface, not an SPA plus one file: its messaging, manifest, background and content boundaries, and dynamic assets usually change together.
- Electron is frontend plus desktop security: context isolation, the preload boundary, and no remote module.
- SSR plus PWA is special because HTML caching interacts with hydration. Enable the combination deliberately, never as a side effect of another change, and only after the update UX, the credentialed-request cache exclusions, the hydration behaviour, the SSR deployment, and the CI build commands are all defined.
- In Yarn repositories use the Yarn-wrapped mode scripts; upstream support for Bun or pnpm never justifies switching.
- Mode work usually changes `quasar.config`, so load `references/21-cli-vite-and-config.md`. Shared source can carry SSR or PWA effects into Capacitor, Cordova, and Electron.
- With v3 dependency isolation, a "module not found" that appears in one mode only usually means the dependency was installed in the wrong location, not that the code is wrong.
- Native permission behaviour differs from web permission behaviour in every mode with a native shell; the split is `references/45-browser-apis-and-permissions.md` §5.

For greenfield mobile with no Cordova history, scaffold Capacitor; do not add the legacy Cordova shell from memory.

Search: `quasar dev -m`, `src-bex`, `src-capacitor`, `src-electron`, `src-ssr`, `defineCapacitorConfig`, `electron preload cjs`, `mode isolation`, `module not found in one mode`, `SSR plus PWA`.
