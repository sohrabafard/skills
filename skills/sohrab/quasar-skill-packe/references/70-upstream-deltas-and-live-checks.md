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

In a Yarn-based repo, these registry lookups can also be done with Yarn if you want the command style to stay aligned with the project:

```bash
yarn info quasar version
yarn info @quasar/app-vite version
yarn info vite version
yarn info vue version
yarn info vue-router version
yarn info workbox-build version
```

The refresh script remains the preferred option because it is package-manager-neutral and produces a stable summary.

## Source priority

Use sources in this order:

1. Repo-local Quasar config, `package.json`, lockfile, boot files, SSR/PWA files, and tests.
2. Official Quasar docs and Quasar CLI with Vite upgrade guide.
3. Official Vite, Vue, Vue Router, and Workbox docs for their own behavior.
4. Official npm metadata, GitHub releases, migration guides, and changelogs.
5. Community posts, StackOverflow answers, and issue comments only as troubleshooting leads.

Do not let community examples override the current Quasar docs or the installed `@quasar/app-vite` version.

## Freshness triggers

Re-check official sources when the task includes:

- "latest", "current", "upgrade", "migration", "security", "CVE", or "breaking"
- Quasar CLI, Vite, Vue, Vue Router, Workbox, Node, or package-manager changes
- SSR middleware, PWA InjectManifest, BEX bridge, Electron/Capacitor/Cordova mode behavior, or `quasar.config` format
- a production-only mismatch between dev and build output

## Live snapshot captured on April 24, 2026

From the npm registry:

- `quasar` -> `2.19.3` (published April 6, 2026)
- `@quasar/app-vite` -> `2.6.0` (published April 6, 2026)
- `vite` -> `8.0.10` (published April 23, 2026)
- `vue` -> `3.5.33` (published April 22, 2026)
- `vue-router` -> `5.0.6` (published April 22, 2026)
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

## Package-manager guidance for this skill

- Quasar supporting Bun does not mean a Yarn repo should switch to Bun.
- If a project uses Yarn workspaces or contains `yarn.lock`, prefer Yarn for installs and scripts.
- Use registry-inspection commands only for version discovery; do not infer the repo's package-manager contract from them.

## Helpful doc endpoints

- Vite provides `vite.dev/llms.txt` and `vite.dev/llms-full.txt` for optimized documentation retrieval.
- Vite stable docs live on `vite.dev`; `main.vite.dev` is useful for upcoming changes but may be ahead of the release you are actually using.
- Quasar docs remain authoritative for API usage, but package and release data may move faster than the docs site. Pair Quasar docs with release notes or npm version checks when the user asks for the latest.
