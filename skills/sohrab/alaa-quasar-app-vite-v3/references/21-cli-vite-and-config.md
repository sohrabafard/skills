# CLI, Vite integration, and config wiring

You are about to add a Vite plugin, extend the Vite config, add an alias, configure a dev proxy, change browser targets, or wire the Quasar CLI. Pair exact text with `references/22-cli-cookbook-and-examples.md`.

Detect the installed `@quasar/app-vite` major before writing any config: `references/80-upstream-deltas-and-live-checks.md` §3 carries the signal table and §4 the full v2/v3 delta set. This file states no version numbers and no delta rows.

✅ Do — branch guidance by the detected major; new apps use v3. ❌ Don't — guess a shape or bump v2 incidentally; a config written for the wrong line fails at startup, and the error names a Vite internal rather than the real cause.

## Still true across both lines

The CLI is ESM and supports simultaneous multi-mode `quasar dev` and `quasar build`. `build.vitePlugins` filters plugins by server or client. `extendViteConf` may mutate the config or return an override object. Bun, pnpm, Yarn, and npm are all supported by upstream — which is not a reason to change the one this repository uses.

## Rules

- **The package manager is a repository contract.** A Yarn workspace or a `yarn.lock` means Yarn. Upstream support for another manager never justifies switching during a Quasar task.
- Prefer one `defineConfig(ctx => ({ ... }))` using `ctx.mode.*`, `ctx.dev`, and `ctx.prod` over duplicated config branches.
- Prefer returning an override object from `extendViteConf`; mutate only when the change cannot be expressed as an override.
- **Add an alias through `build.alias`, or merge into `viteConf.resolve.alias`. Never assign to `viteConf.resolve.alias`** — assignment erases Quasar's own aliases and every framework import stops resolving.
- Use `build.viteVuePluginOptions` for custom Vue-plugin behaviour; do not replace Quasar's plugin.
- Keep the config mode-aware: BEX, SSR, PWA, Electron, and mobile targets often need different plugins and paths.
- After a toolchain upgrade, read `references/80-upstream-deltas-and-live-checks.md` §5 before attributing a failure to a component.

```js
// merges; preserves Quasar's aliases
build: { alias: { '@features': 'src/features' } }
```

```js
// erases Quasar's aliases and breaks resolution
extendViteConf (viteConf) { viteConf.resolve.alias = { '@features': 'src/features' } }
```

## Also load

- Boot, router, store, or `preFetch` with SSR -> `references/31-ssr-pwa-and-security.md`.
- BEX, Capacitor, Cordova, or Electron -> `references/35-platform-modes.md`.
- Bundle output, chunking, and Vite 8 behaviour -> `references/70-guardrails-a11y-performance-monorepo.md`.
- Workspace libraries, peers, exports maps, and asset reachability -> `/alaa-mono-package` (`$alaa-mono-package`).
- Exact config, boot, router, env, and Vite text -> `references/22-cli-cookbook-and-examples.md`.

## Relationships easy to miss

- Boot is often config plus SSR; routing often carries layout, `preFetch`, and SEO.
- `build.env.folder` and secrets become SSR risks; only client-prefixed variables may enter a client bundle (`references/20-v3-config-and-features.md`).
- A `vitePlugins` failure after an upgrade is usually Vite 8 or Rolldown, not Quasar.
- A Vuex reference implies legacy code; confirm Pinia before editing state.
- Concepts transfer across majors while Quasar's signatures, imports, and registration do not. When the shape matters, load `22`.

Search: `quasar.config`, `defineConfig`, `extendViteConf`, `vitePlugins`, `build.alias`, `resolve.alias`, `viteVuePluginOptions`, `ctx.mode`, `dev proxy`, `browser targets`, `package manager contract`.
