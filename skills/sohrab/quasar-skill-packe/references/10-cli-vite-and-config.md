# CLI, Vite, and Config

Use this file for Quasar CLI wiring, `quasar.config`, dev/build behavior, routing/bootstrap, and general Vite integration inside a Quasar app.

For exact "how do I wire this?" guidance, pair this file with `11-cli-cookbook-and-examples.md`.

## Covers

- `quasar.config` structure and mode-aware branching
- directory structure, boot files, routing, and Pinia
- Vite extension points inside Quasar CLI
- assets, aliases, env files, ajax requests, API proxying, browser compatibility
- lazy loading, testing/auditing, and build commands
- upgrade-sensitive config surfaces

## Detect the app-vite line before editing config

`@quasar/app-vite` v2 and v3 have different import paths, config extensions, env keys, and aliases. Read the installed version in `package.json` first. The full split table and migration list live in `70-upstream-deltas-and-live-checks.md`.

✅ Do — branch your guidance on the detected major; for production prefer the stable v2 line.

```text
v2 (^2.x, STABLE/production): `#q-app/wrappers`, `.js/.mjs/.ts/.cjs` config, build.envFolder/envFiles, legacy aliases
v3 (^3.0.0-rc.x, RC):         `#q-app`, `.js`/`.ts` config, build.env.{folder,file,clientPrefix}, @/ alias, Rolldown under /src-*
```

❌ Don't — give one config shape "from memory" without checking, or move a production app from stable v2 onto RC v3 by default; the wrong line produces a `quasar.config` that fails to load.

## Current upstream notes

`@quasar/app-vite` v3 (`3.0.0-rc.x`, still **RC** — not a stable release) introduced these. They matter when reading/maintaining a repo already on v3 or planning an explicitly requested migration. Treat them as real migration inputs, not invisible patch behavior:

- The CLI bundles **Vite 8** and compiles `/src-*` with **Rolldown** instead of esbuild.
- `quasar.config` is **`.js` or `.ts` only** (`.cjs`/`.mjs`/`.cts`/`.mts` dropped). Wrappers import from **`#q-app`** (was `#q-app/wrappers`).
- Env config moved under **`build.env`** (`folder`, `file`, `clientPrefix` default `'QCLI_'`). `build.rawDefine` -> `build.define` (non-string values are auto-`JSON.stringify`ed; wrap string literals yourself); `build.env` -> `build.defineEnv`.
- Quasar constants are read as **`import.meta.env.QUASAR_*`** (was `process.env.*`).
- Path aliases collapse to a single **`@/`** (-> `/src`).
- `build.vueOptionsAPI` defaults to **`false`**; `build.analyze` and `build.polyfillModulePreload` removed.
- Per-mode dependency isolation: mode deps install in `/src-*` folders. Node **22+**.
- Pinia is the store (v2 or v3). Vuex is not integrated in the CLI.

These carry over from v2 and are still true in v3:

- The CLI is ESM and supports multiple simultaneous `quasar dev`/`quasar build` runs for different modes.
- `build.vitePlugins` supports a server/client run filter; `extendViteConf` may mutate or return overrides.
- Bun, pnpm, Yarn, and npm are all supported package managers.

## Default rules

- Treat package manager choice as a repository contract. If the repo uses Yarn workspaces or contains `yarn.lock`, prefer Yarn for installs and script execution.
- Upstream Bun/pnpm support is useful to know about, but it is not a reason to switch an existing Yarn repo.
- Prefer `defineConfig(ctx => ({ ... }))` and use `ctx.mode.*`, `ctx.dev`, and `ctx.prod` instead of scattering duplicated config branches.
- Prefer returning an object from `extendViteConf` when you can; mutate only when a plugin truly requires it.
- When adding aliases, use Quasar's `build.alias` or merge into `viteConf.resolve.alias` without replacing existing aliases.
- For custom Vue plugin behavior, use `build.viteVuePluginOptions` instead of replacing the Quasar-managed Vue plugin.
- Keep config changes mode-aware. BEX, SSR, PWA, Electron, and mobile modes often need different plugin application or path handling.
- Treat Vite 8 behavior changes as real migration inputs. Read `70-upstream-deltas-and-live-checks.md` when toolchain behavior changed after package upgrades.

✅ Do — keep one mode-aware config function and reuse Quasar's alias merge.

```js
build: {
  alias: { '@features': 'src/features' }, // merges; existing aliases stay
}
```

❌ Don't — overwrite `viteConf.resolve.alias = { ... }` inside `extendViteConf`; that erases Quasar's own aliases and breaks resolution.

## Common "also load" cases

- Boot files, router, store, or `preFetch` in SSR:
  - also read `20-ssr-pwa-and-security.md`
- BEX, Capacitor, Cordova, or Electron:
  - also read `30-platform-modes.md`
- Monorepo libraries, peer deps, asset inclusion, or tree-shaking:
  - also read `60-guardrails-a11y-performance-monorepo.md`
- Exact `quasar.config`, boot-file, routing, env, or Vite-extension snippet shape:
  - also read `11-cli-cookbook-and-examples.md`

## Easy-to-miss relationships

- `boot files` are often a config question and an SSR question.
- `routing` is often also about layouts, `preFetch`, or SEO.
- `envFolder`/`build.env.folder` and secrets become risky when SSR is involved; only client-prefixed vars should reach the client bundle.
- `vitePlugins` problems after upgrades can come from Vite 8 / Rolldown migration behavior, not from Quasar itself.
- If a repo still mentions Vuex in Quasar CLI integration, assume it is legacy and verify whether the app is already on Pinia before editing.
- The agent often knows the concepts here but can still get Quasar-specific function signatures, import paths, or registration shapes slightly wrong, especially across the v2/v3 boundary; load `11-cli-cookbook-and-examples.md` when the code shape matters more than the concept.
