# Platform Modes

Use this file when the task is mode-specific or the same Quasar app may run in more than one target.

Confirm the `@quasar/app-vite` line first (see `70-...`); v3 changed several mode folder structures and config shapes.

## Mode routing

| Mode | Primary concerns | Always combine with |
| --- | --- | --- |
| SPA | build output, lazy loading, routing, SEO trade-offs | `10-cli-vite-and-config.md` |
| SSR | server render, hydration, SEO, `ssrContext`, auth mapping, server framework choice | `20-ssr-pwa-and-security.md` |
| PWA | service worker, offline, update flow, manifest, stale asset risk | `20-ssr-pwa-and-security.md` |
| BEX | background/content/devtools/popup split, bridge, manifest, per-mode `package.json` | `10-cli-vite-and-config.md` |
| Capacitor | native shell, mobile build commands, runtime plugins, app icons, live update policy | `10-cli-vite-and-config.md` |
| Cordova | legacy mobile shell, plugin constraints, older ecosystem assumptions | `10-cli-vite-and-config.md` |
| Electron | preload scripts, security boundaries, desktop packaging, app icons, Node context | `10-cli-vite-and-config.md` |

## Current upstream notes (app-vite v3)

- **Per-mode dependency isolation:** mode-specific dependencies install inside the `/src-*` folder for that mode. Electron no longer needs its deps duplicated into the build output.
- **SSR:** the CLI asks which server to scaffold (Hono / Express / Fastify / Koa) and adds `/src-ssr/server-assets`.
- **BEX:** requires a `/src-bex/package.json` (`"type": "module"`) and defaults to the `chrome` target (no `-t` flag needed). The Quasar Bridge and file inference were rewritten; Chrome HMR is supported.
- **Capacitor:** v4 and below dropped. `capacitor.config.json` becomes `capacitor.config.ts`/`.js` via `defineCapacitorConfig()`. `quasar dev/build -m ios|android` targets Capacitor.
- **Electron:** packager v18 and below dropped. Preload now imports `import { quasarRuntime } from '#q-app/electron/preload'` and preload files use the `.cjs` extension; `/src-electron/electron-assets` is added. Multiple preload scripts are supported.
- SSR development with HTTPS is supported. Multiple CLI instances can run against the same project in different modes.

✅ Do — in a v3 BEX repo, add `/src-bex/package.json` and rely on the default chrome target.

```jsonc
// src-bex/package.json
{ "name": "quasar-bex-app", "version": "1.0.0", "private": true, "type": "module",
  "devDependencies": { "@types/chrome": "^0.1.40" } }
```

❌ Don't — keep `capacitor.config.json` or a non-`.cjs` Electron preload in a v3 repo, or reference `#q-app/electron` preload imports from the old path. Those shapes were dropped.

## Selection heuristics

- For new mobile work, favor Capacitor unless the repository already relies on Cordova or the user explicitly needs Cordova. This is an inference from current Quasar CLI defaults and ecosystem direction, not a Quasar deprecation statement.
- Treat BEX as a multi-surface app, not a normal SPA with one extra file.
- Treat Electron tasks as both frontend and desktop-security tasks (context isolation, preload boundary, no remote module).
- Treat SSR + PWA together as a special case because HTML caching and hydration risk interact.
- If the repo is Yarn-based, prefer Yarn-wrapped project scripts for mode-specific dev/build flows instead of switching package managers because upstream also supports Bun/pnpm.

✅ Do — for new mobile work in a repo with no Cordova history, scaffold Capacitor.

❌ Don't — add Cordova to a greenfield app just because the model remembers it; it is the legacy shell.

## Easy-to-miss relationships

- Platform tasks almost always require `quasar.config` changes, so read `10-cli-vite-and-config.md`.
- Capacitor, Cordova, and Electron can still be affected by SSR/PWA choices in shared source code.
- BEX tasks often touch messaging, manifest structure, background/content script boundaries, and dynamic asset loading together.
- Mode-specific dependency isolation in v3 means "module not found" in one mode can be an install-location problem, not a code problem.
