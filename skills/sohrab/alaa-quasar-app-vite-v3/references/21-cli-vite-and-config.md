# CLI, Vite, and config

Use for Quasar CLI wiring, `quasar.config`, dev/build, boot/routing, and Vite integration; pair exact wiring with `22-cli-cookbook-and-examples.md`.

Covers config/mode branches; directories, boot, routing, Pinia; Vite extension points; assets, aliases, env, ajax/proxy, browser targets; lazy loading, tests/audits/builds; upgrade-sensitive surfaces.

## Detect app-vite before editing

Read installed `@quasar/app-vite` in `package.json`; v2/v3 differ in imports, config extensions, env, aliases. Full split/migration: `80-upstream-deltas-and-live-checks.md`.

```text
v3 (^3, stable): #q-app; .js/.ts; build.env.{folder,file,clientPrefix}; @/; Rolldown /src-*
v2 (^2, maintenance): #q-app/wrappers; .js/.mjs/.ts/.cjs; build.envFolder/envFiles; legacy aliases
```

✅ Branch guidance by detected major; new apps use v3. ❌ Never guess one shape or bump v2 incidentally; wrong-line configs fail. Use `10-v2-to-v3-migration.md`.

## Upstream facts

v3 is stable since 3.0.1 (2026-07-07):

- Vite 8; Rolldown, not esbuild, compiles `/src-*`.
- Config only `.js`/`.ts` (`.cjs`/`.mjs`/`.cts`/`.mts` dropped); wrappers `#q-app` (v2: `#q-app/wrappers`).
- Env -> `build.env.{folder,file,clientPrefix}` with default `'QCLI_'`; `build.rawDefine` -> `build.define` (non-strings auto-stringified; wrap string literals); v2 `build.env` injection -> `build.defineEnv`.
- Constants `process.env.*` -> `import.meta.env.QUASAR_*`; only `@/` alias remains.
- `build.vueOptionsAPI` defaults `false`; `build.analyze` and `build.polyfillModulePreload` removed.
- Mode deps install under `/src-*`; Node 22+.
- Pinia v2/v3 is integrated; Vuex is not.

Still true from v2: CLI is ESM and supports simultaneous multi-mode `quasar dev`/`build`; `build.vitePlugins` filters server/client; `extendViteConf` may mutate or return overrides; Bun, pnpm, Yarn, npm are supported.

## Rules

- Package manager is a repo contract: Yarn workspace/`yarn.lock` -> Yarn. Upstream Bun/pnpm support never justifies switching.
- Prefer `defineConfig(ctx => ({ ... }))` with `ctx.mode.*`, `ctx.dev`, `ctx.prod`, not duplicated config branches.
- Prefer return overrides from `extendViteConf`; mutate only when required.
- Add aliases through `build.alias` or merge `viteConf.resolve.alias`; never replace existing aliases.
- Use `build.viteVuePluginOptions` for custom Vue-plugin behavior; do not replace Quasar's plugin.
- Keep config mode-aware: BEX/SSR/PWA/Electron/mobile often need different plugins/paths.
- Treat Vite 8 behavior as migration input; after toolchain upgrades read `80-upstream-deltas-and-live-checks.md`.

```js
// merges; preserves Quasar aliases
build: { alias: { '@features': 'src/features' } }
```

❌ `viteConf.resolve.alias = { ... }` erases Quasar aliases and breaks resolution.

## Also load

- Boot/router/store/`preFetch` with SSR -> `31-ssr-pwa-and-security.md`.
- BEX/Capacitor/Cordova/Electron -> `35-platform-modes.md`.
- Monorepo libraries/peers/assets/tree-shaking -> `70-guardrails-a11y-performance-monorepo.md`.
- Exact config/boot/router/env/Vite shapes -> `22-cli-cookbook-and-examples.md`.

## Relationships easy to miss

- Boot is often config + SSR; routing often includes layout, `preFetch`, SEO.
- `envFolder`/`build.env.folder` and secrets become SSR risks; only client-prefixed vars may enter client bundles.
- `vitePlugins` failures after upgrades may be Vite 8/Rolldown, not Quasar.
- Vuex references imply legacy: verify Pinia before editing.
- Concepts may be familiar while Quasar signatures/imports/registration differ across majors; when shape matters, load `22`.
