# Upstream Deltas and Live Checks

Use this file for any "latest", upgrade, migration, or maintenance task.

## Refresh workflow

For Quasar/Vite versions, prefer a live check before answering:

```bash
node scripts/check-upstream-versions.mjs
```

If you want manual commands instead:

```bash
npm view quasar version
npm view @quasar/app-vite version
npm view vite version
npm view vue version
npm view vue-router version
npm view workbox-build version
```

## Live snapshot captured on March 25, 2026

From the npm registry:

- `quasar` -> `2.19.1` (published March 24, 2026)
- `@quasar/app-vite` -> `2.5.4` (published March 24, 2026)
- `vite` -> `8.0.2` (published March 23, 2026)
- `vue` -> `3.5.31` (published March 25, 2026)
- `vue-router` -> `5.0.4`
- `workbox-build` -> `7.4.0`

This source pack was built from an older snapshot centered around Quasar `2.18.6`, `@quasar/app-vite` `2.4.0`, Vite `7.3.0`, and Vue `3.5.26`, so version drift is real and should not be ignored.

## Important Quasar CLI with Vite changes

Official Quasar docs and release data highlight these current areas:

- Vite 8 support in `@quasar/app-vite` v2
- multiple simultaneous Quasar CLI dev/build instances
- ESM CLI implementation
- multiple supported `quasar.config` formats
- `envFolder` and `envFiles`
- Bun support
- SSR development with HTTPS
- richer `vitePlugins` targeting
- `extendViteConf` returning overrides
- `injectPwaMetaTags` as a function
- Workbox v7 defaults

## Important Vite 8 migration risks

From the official Vite migration guide:

- dependency optimization now uses Rolldown instead of esbuild
- JavaScript transforms and minification moved to Oxc, with backward-compatibility layers that are deprecated
- CSS minification now uses Lightning CSS
- CommonJS default import behavior is more consistent and may break some packages
- the object form of `manualChunks` is no longer supported
- `build.rollupOptions` is being renamed toward `build.rolldownOptions`

When a Quasar app starts failing only after a toolchain bump, check these migration surfaces before assuming a Quasar regression.

## OpenAI/Codex maintenance rules for this skill

When updating this skill itself:

- Use the OpenAI Docs MCP server first for OpenAI/Codex docs.
- Keep the skill focused on one job and use progressive disclosure.
- Prefer instructions over scripts unless determinism or repeated live refresh is worth it.
- Write trigger descriptions with clear scope so implicit invocation stays accurate.
- Test whether a realistic prompt would load the skill.

From the March 25, 2026 OpenAI docs/cookbook review:

- Agent Skills docs emphasize progressive disclosure and `name`/`description` trigger quality.
- Docs MCP docs recommend adding the OpenAI Docs MCP server and instructing the agent to use it first.
- The Codex Prompting Guide recommends `rg`, tool preference over raw shell when possible, parallel reads, autonomy, and bias to action.
- The same guide explicitly says not to force upfront plans, preambles, or status chatter into the base harness prompt.
- OpenAI's Codex guidance now explicitly notes improved behavior on Windows and PowerShell.

## Helpful doc endpoints

- Vite provides `vite.dev/llms.txt` and `vite.dev/llms-full.txt` for optimized documentation retrieval.
- Vite stable docs live on `vite.dev`; `main.vite.dev` is useful for upcoming changes but may be ahead of the release you are actually using.
- Quasar docs remain authoritative for API usage, but package and release data may move faster than the docs site. Pair Quasar docs with release notes or npm version checks when the user asks for the latest.
