# Platform Modes

Use this file when the task is mode-specific or the same Quasar app may run in more than one target.

## Mode routing

| Mode | Primary concerns | Always combine with |
| --- | --- | --- |
| SPA | build output, lazy loading, routing, SEO trade-offs | `10-cli-vite-and-config.md` |
| SSR | server render, hydration, SEO, `ssrContext`, auth mapping | `20-ssr-pwa-and-security.md` |
| PWA | service worker, offline, update flow, manifest, stale asset risk | `20-ssr-pwa-and-security.md` |
| BEX | background/content/devtools/popup split, bridge, manifest, mode-specific build files | `10-cli-vite-and-config.md` |
| Capacitor | native shell, mobile build commands, runtime plugins, app icons, live update policy | `10-cli-vite-and-config.md` |
| Cordova | legacy mobile shell, plugin constraints, older ecosystem assumptions | `10-cli-vite-and-config.md` |
| Electron | preload scripts, security boundaries, desktop packaging, app icons, Node context | `10-cli-vite-and-config.md` |

## Current upstream notes

From the Quasar CLI with Vite upgrade guide:

- BEX support was heavily redesigned, including a rewritten Quasar Bridge and better file inference.
- BEX HMR is supported for Chrome.
- Electron can now load multiple preload scripts.
- SSR development with HTTPS is supported.
- The shorthand `quasar dev/build -m ios` and `-m android` now target Capacitor instead of Cordova.
- Multiple Quasar CLI instances can run against the same project in different modes.

## Selection heuristics

- For new mobile work, favor Capacitor unless the repository already relies on Cordova or the user explicitly needs Cordova. This is an inference from current Quasar CLI defaults and ecosystem direction, not a Quasar deprecation statement.
- Treat BEX as a multi-surface app, not a normal SPA with one extra file.
- Treat Electron tasks as both frontend and desktop-security tasks.
- Treat SSR + PWA together as a special case because HTML caching and hydration risk interact.

## Easy-to-miss relationships

- Platform tasks almost always require `quasar.config` changes, so read `10-cli-vite-and-config.md`.
- Capacitor, Cordova, and Electron can still be affected by SSR/PWA choices in shared source code.
- BEX tasks often touch messaging, manifest structure, background/content script boundaries, and dynamic asset loading together.
