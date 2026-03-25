# CLI, Vite, and Config

Use this file for Quasar CLI wiring, `quasar.config`, dev/build behavior, routing/bootstrap, and general Vite integration inside a Quasar app.

For exact “how do I wire this?” guidance, pair this file with `11-cli-cookbook-and-examples.md`.

## Covers

- `quasar.config` structure and mode-aware branching
- directory structure, boot files, routing, and Pinia
- Vite extension points inside Quasar CLI
- assets, aliases, env files, ajax requests, API proxying, browser compatibility
- lazy loading, testing/auditing, and build commands
- upgrade-sensitive config surfaces

## Current upstream notes

From the Quasar CLI with Vite upgrade guide and handling docs:

- `@quasar/app-vite` v2 upgrades Quasar CLI to Vite 8.
- The CLI now supports multiple simultaneous `quasar dev` and `quasar build` runs for different modes.
- The CLI itself is ESM and supports `quasar.config` in `.js`, `.mjs`, `.ts`, and `.cjs`.
- `build.envFolder` and `build.envFiles` are now supported.
- Bun is supported as a package manager.
- `build.vitePlugins` gained an additional mode filter parameter for server/client targeting.
- `extendViteConf` can return overrides, not only mutate the config object in place.
- `pwa.injectPwaMetaTags` can be a function.
- `build.htmlMinifyOptions` is available.
- The CLI officially treats Pinia as the store solution; Vuex support was dropped from the CLI integration.

## Default rules

- Treat package manager choice as a repository contract. If the repo uses Yarn workspaces or contains `yarn.lock`, prefer Yarn for installs and script execution.
- Upstream Bun support is useful to know about, but it is not a reason to switch an existing Yarn repo.
- Prefer `defineConfig(ctx => ({ ... }))` and use `ctx.mode.*`, `ctx.dev`, and `ctx.prod` instead of scattering duplicated config branches.
- Prefer returning an object from `extendViteConf` when you can; mutate only when a plugin truly requires it.
- When adding aliases, use Quasar's `build.alias` or merge into `viteConf.resolve.alias` without replacing existing aliases.
- For custom Vue plugin behavior, use `build.viteVuePluginOptions` instead of replacing the Quasar-managed Vue plugin.
- Keep config changes mode-aware. BEX, SSR, PWA, Electron, and mobile modes often need different plugin application or path handling.
- Treat Vite 8 behavior changes as real migration inputs, not as invisible patch releases. Read `70-upstream-deltas-and-live-checks.md` when toolchain behavior changed after package upgrades.

## Common "also load" cases

- Boot files, router, store, or `preFetch` in SSR:
  - also read `20-ssr-pwa-and-security.md`
- BEX, Capacitor, Cordova, or Electron:
  - also read `30-platform-modes.md`
- Monorepo libraries, peer deps, asset inclusion, or tree-shaking:
  - also read `60-guardrails-a11y-performance-monorepo.md`
- Exact `quasar.config`, boot-file, routing, or Vite-extension snippet shape:
  - also read `11-cli-cookbook-and-examples.md`

## Easy-to-miss relationships

- `boot files` are often a config question and an SSR question.
- `routing` is often also about layouts, `preFetch`, or SEO.
- `envFolder` and `envFiles` become risky when SSR or secrets are involved.
- `vitePlugins` problems after upgrades can come from Vite 8 migration behavior, not from Quasar itself.
- If a repo still mentions Vuex in Quasar CLI integration, assume it is legacy and verify whether the app is already on Pinia before editing.
- The agent often knows the concepts here but can still get Quasar-specific function signatures or registration shapes slightly wrong; load `11-cli-cookbook-and-examples.md` when the code shape matters more than the concept.
