# Bundling, module format and loading under Vite

## There is no ESM build. Say so plainly.

| Fact | Grade | Source (read 2026-07-28) |
|---|---|---|
| `package.json` has `"main": "dist/shaka-player.compiled.js"` and `"types": "dist/shaka-player.compiled.d.ts"` | `verified` | `.../blob/v5.2.3/package.json` |
| **No `"module"` field, no `"exports"` map, no `"browser"` field, no `.mjs` file anywhere in `dist/`** | `verified` | `package.json` at tag; npm registry read; jsDelivr `dist/` listing |
| The bundle is a hand-written **UMD-ish wrapper**: CommonJS if `exports` exists → AMD if `define.amd` → otherwise `innerGlobal.shaka = exportTo.shaka` | `verified` | `.../blob/v5.2.3/build/wrapper.template.js` |
| Practical consequence: `import shaka from 'shaka-player/dist/shaka-player.ui.js'` works through a bundler's CJS interop, but the module has **no named ESM exports**, and when treated as an ES module its real effect is assigning the `shaka` **global** | `inferred` | wrapper source |
| `"engines"`: Node ≥ 18. License Apache-2.0 | `verified` | `package.json` |
| A general "how to import Shaka under Vite" section | `not documented` — searched all 34 tutorial files and `README.md` for "Vite" on 2026-07-28; the only hit is the transmux-worker tutorial | `not documented` | – |

So: **do not** write `import { Player } from "shaka-player"`. It has no named exports. Import the
default from an explicit `dist/` path and normalize `.default`.

## Which build to import

Five variants × four forms (release, `.debug`, `-es2021`, `-es2021.debug`), each with `.js`, `.map`,
`.externs.js` and `.d.ts` (`verified`, jsDelivr listing at 5.2.3):

| File | Contents |
|---|---|
| `dist/shaka-player.compiled.js` | Core player, **no UI**. This is the package `main`. |
| `dist/shaka-player.ui.js` | Player **+ UI library**. Import this if you use `shaka.ui.Overlay`. |
| `dist/shaka-player.dash.js` / `.hls.js` | Single-format slim builds (no UI, queue, transmuxer, offline, cast, ads). |
| `dist/shaka-player.experimental.js` | Everything, including MSF/MoQT and DASH-JSON — these ship **only** here. |
| `dist/shaka-player.compiled.debug.js` | Logging retained. Use in a lab page, never in production. |
| `dist/shaka-player.transmuxer-worker.js` | Standalone transmux Web Worker. |
| `dist/controls.css` | Legacy UI CSS, custom properties flattened at build time. |
| `dist/controls.modern.css` | **Modern UI CSS, custom properties preserved — use this.** |

**Trap C8.** `"types"` resolves to the **non-UI** `.d.ts` even when you load the UI bundle. UI
consumers reference `dist/shaka-player.ui.d.ts` explicitly or add an ambient declaration.

## Working snippet — a Vite-built Quasar app

```ts
// src/player/shakaLoader.ts — the ONLY file in the repository that imports shaka-player.

import type { ShakaNamespace } from "./shakaTypes";

/** Worker URL. `new URL(..., import.meta.url)` is upstream's own Vite recipe: the
 *  bundler resolves the npm path, copies the worker into the build output and
 *  rewrites the URL at build time. Shaka does NOT auto-detect this. */
const TRANSMUX_WORKER_URL = new URL(
  "shaka-player/dist/shaka-player.transmuxer-worker.js",
  import.meta.url
).toString();

let cached: ShakaNamespace | null = null;

/** Loads Shaka client-side once. Never call this at module top level in SSR. */
export async function loadShaka(): Promise<ShakaNamespace> {
  if (cached) return cached;

  // Explicit dist path: the package `main` is the NON-UI build.
  // No named exports exist; this goes through Vite's CJS interop, so unwrap `.default`.
  const mod = (await import("shaka-player/dist/shaka-player.ui.js")) as { default?: unknown };
  cached = ((mod.default ?? mod) as ShakaNamespace);
  return cached;
}

export function transmuxWorkerUrl(): string {
  return TRANSMUX_WORKER_URL;
}
```

```ts
// Wherever you build the player config:
player.configure("mediaSource.transmuxWorkerUrl", transmuxWorkerUrl());
```

```ts
// src/player/shaka-ui.d.ts — only if module resolution complains about the UI path.
declare module "shaka-player/dist/shaka-player.ui.js";
```

```ts
// CSS: import the modern sheet so --shaka-* stays overridable at runtime.
import "shaka-player/dist/controls.modern.css";
```

## Transmux worker deployment constraints

All `verified` from `.../blob/v5.2.3/docs/tutorials/transmuxing-in-worker.md` (read 2026-07-28):

- Falls back to **main-thread transmuxing silently** when: `transmuxWorkerUrl` is empty; the device
  reports no Worker support (older Tizen/WebOS); `new Worker(url)` throws (CSP, network, MIME); the
  first `postMessage` fails; or the worker does not respond within **30 seconds** for a segment.
- **Tizen, WebOS and Hisense opt out internally** regardless of the setting.
- Must be same-origin, or CORS with `Access-Control-Allow-Origin` (plus
  `Cross-Origin-Resource-Policy: cross-origin` when the page is cross-origin-isolated).
- CSP needs `worker-src 'self'; script-src 'self';`.
- Webpack 4: `import workerUrl from 'shaka-player/dist/shaka-player.transmuxer-worker.js?url'`.
- Static `public/` deployments: copy the file and use an absolute path; upstream suggests *"A small
  build script that copies the file on `postinstall` keeps the worker version in sync with the
  installed package."*
- Upstream refuses auto-detection: *"Shaka does not auto-detect the worker URL… The integrating
  application owns how Shaka is loaded, so the application also owns the worker URL."*

Transmuxing matters when the source is **HLS with MPEG-2 TS segments**, which must be transmuxed to
fMP4. DASH normally does not need it.

## Building from source

Prerequisites (`verified`, `docs/tutorials/welcome.md`): Git ≥ 1.9, Python ≥ 3.5, **JRE ≥ 21**,
NodeJS ≥ 18, and a local web server (browsers restrict `file:///` applications). Build with
`python3 build/all.py` or the provided Docker image. `complete_non_experimental = ['+@complete',
'-@msf', '-@dashJson']`, which is why MSF and DASH-JSON ship only in the experimental build.

**Best practice.** One loader module, one dist path, `.default` unwrapped there, and the worker URL
produced by the same module. Every other file imports your loader.
**Common mistake.** `import shaka from "shaka-player"` and then `shaka.ui.Overlay` — the package
`main` is the non-UI build, so `shaka.ui` is `undefined` at runtime while TypeScript stays quiet
because the shipped `types` entry describes that same non-UI build.
