# Upstream Deltas and Live Checks

Use this file for any "latest", upgrade, migration, or maintenance task.

## Table of contents

- Refresh workflow
- Source priority
- Freshness triggers
- Live snapshot (captured 2026-06-16)
- The `@quasar/app-vite` v2-vs-v3 split (read this first for any config/CLI task)
- `@quasar/app-vite` v3 breaking changes
- Quasar 2.20.x framework notes
- Quasar v3 (UI framework) status
- Vite 8 migration risks
- Vue Router 5 notes
- Vue 3.5 SSR-relevant features
- Workbox 7.4.x notes
- Dual-runtime maintenance rules (Claude Opus + GPT-5/Codex)
- Package-manager guidance
- Helpful doc endpoints

## Refresh workflow

For version-sensitive work, run a live check before answering:

```bash
node scripts/check-upstream-versions.mjs
```

Manual fallback commands:

```bash
npm view @quasar/app-vite dist-tags   # currently: beta + latest (no dedicated v2 tag)
npm view "@quasar/app-vite@^2" version # the v2 maintenance line, by explicit semver
npm view quasar version
npm view vite version
npm view vue version
npm view vue-router version
npm view pinia version
npm view workbox-build version
```

In a Yarn-based repo you may keep the command style aligned with the project (`yarn info <pkg> version`), but the script is preferred because it is package-manager-neutral and produces a stable summary.

## Source priority

Use sources in this order:

1. Repo-local `quasar.config`, `package.json`, lockfile, boot files, SSR/PWA files, and tests. The installed `@quasar/app-vite` version is the single most important fact — it decides whether v2 or v3 guidance applies.
2. Official Quasar docs and the Quasar CLI with Vite upgrade guide.
3. Official Vite, Vue, Vue Router, Pinia, and Workbox docs for their own behavior.
4. Official npm metadata, GitHub releases, migration guides, and changelogs.
5. Community posts, StackOverflow answers, and issue comments only as troubleshooting leads.

Do not let community examples override the current Quasar docs or the installed `@quasar/app-vite` version.

## Freshness triggers

Re-check official sources when the task includes:

- "latest", "current", "upgrade", "migration", "security", "CVE", or "breaking"
- Quasar CLI, Vite, Vue, Vue Router, Pinia, Workbox, Node, or package-manager changes
- SSR middleware, PWA service worker, BEX bridge, Electron/Capacitor mode behavior, or `quasar.config` format
- a production-only mismatch between dev and build output

## Live snapshot (captured 2026-06-16)

From the npm registry on 2026-06-16:

- `quasar` -> `2.20.1` (stable)
- `@quasar/app-vite` (stable / production) -> `2.6.2` (published 2026-06-03) — **the production line**
- `@quasar/app-vite` (pre-release) -> `3.0.0-rc.3` (sits on the `latest` dist-tag; dist-tags are only `beta` 3.0.0-beta.45 and `latest` 3.0.0-rc.3 — **there is no stable v3 release yet**)
- `vite` -> `8.0.16` (stable)
- `vue` -> `3.5.38` (stable)
- `vue-router` -> `5.1.0` (stable)
- `pinia` -> `3.0.4` (stable; v2 or v3 both accepted by app-vite v3)
- `workbox-build` -> `7.4.1` (stable)

**Stable-first rule:** for production, recommend stable releases. The only pre-release above is `@quasar/app-vite` v3 (RC). Note the unusual situation: the npm `latest` dist-tag points at the RC, but RC is not stable — the production app-vite line is v2.x (`2.6.2`). Do not push a production app onto v3 while it is RC; cover v3 only to support repos that already opted in or when the user explicitly asks for the pre-release.

This snapshot ages. Re-run the script before any version-sensitive answer. The previous snapshot (centered on `@quasar/app-vite` `2.6.0`, `quasar` `2.19.3`, `vite` `8.0.10`, `vue-router` `5.0.6`) drifted in under two months, so do not trust a stale snapshot.

## The `@quasar/app-vite` v2-vs-v3 split (read this first for any config/CLI task)

This is the highest-impact fact in the whole pack. There are two live CLI lines, and they have **different import paths, config formats, aliases, and folder structures**. Applying one line's shapes to the other produces code that does not run.

**Always detect the line first.** Read `@quasar/app-vite` in the repo's `package.json` (and the lockfile) before giving any config, boot, env, alias, SSR, PWA, BEX, Electron, or Capacitor advice.

| Signal | `@quasar/app-vite` `^2.x` (stable / production) | `@quasar/app-vite` `^3.x` (pre-release / RC) |
| --- | --- | --- |
| Status | **Stable, production-ready** (latest `2.6.2`); in Maintenance until ~2027-06-11 | **RC, no stable release yet** (`3.0.0-rc.3`); on the `latest` dist-tag but not production-ready |
| Wrapper import | `#q-app/wrappers` | `#q-app` |
| `quasar.config` ext | `.js` `.mjs` `.ts` `.cjs` | `.js` `.ts` only |
| Quasar constants | `process.env.MODE`, `process.env.DEV`, ... | `import.meta.env.QUASAR_MODE`, `import.meta.env.QUASAR_DEV`, ... |
| Env config | `build.envFolder`, `build.envFiles` | `build.env.folder`, `build.env.file`, `build.env.clientPrefix` |
| Define | `build.rawDefine`, `build.env` | `build.define`, `build.defineEnv` |
| Path aliases | `src/`, `components/`, `boot/`, `stores/`, `app/`, ... | `@/` only (`@/components/`, `@/../`, ...) |
| Bundler under the CLI | esbuild for `/src-*` | Rolldown for `/src-*` |
| Custom SW path | `/src-pwa/custom-sw` | `/src-pwa/sw/custom-sw` |
| SSR server | Express-only scaffold | choice of Hono / Express / Fastify / Koa |
| Node floor | Node 18+ | Node 22+ (registry floor `22.22.0`) |

✅ Do — confirm the line, then give shapes for that line only.

```text
"package.json shows @quasar/app-vite ^3.0.0-rc.3, so I will use `#q-app`,
build.env.folder, and the @/ alias."
```

❌ Don't — assume v2 shapes because the model remembers them better, or mix lines.

```text
"import { defineBoot } from '#q-app/wrappers'"   // breaks a v3 repo
"import { defineBoot } from '#q-app'"             // breaks a v2 repo
```

If the repo already has a line installed, match it. If the line is genuinely unknown (or it is a greenfield production app), default to **stable v2** and state the assumption explicitly rather than guessing silently or reaching for the RC.

## `@quasar/app-vite` v3 breaking changes (summary — full playbook in `$alaa-app-vite-quasar`)

v3 is still **RC** (no stable release). This is a **summary** so you can pick the right code shape from within this pack. The **authoritative v2->v3 migration playbook, full breaking-change checklist, and v3-readiness rules live in `$alaa-app-vite-quasar`** — route there for any migration/upgrade/readiness work, and never push a stable production app onto the RC.

Shape-affecting deltas at a glance (v2 -> v3):

- Imports: `#q-app/wrappers` -> `#q-app`; aliases collapse to a single `@/` (`components/` -> `@/components/`, `app/` -> `@/../`, ...).
- Config: `quasar.config` is `.js`/`.ts` only; `build.vueOptionsAPI` defaults to `false`; `build.analyze`/`build.polyfillModulePreload` removed.
- Env: `build.envFolder`/`envFiles` -> `build.env.{folder,file}` + `build.env.clientPrefix` (default `'QCLI_'`); `process.env.QUASAR-constants` -> `import.meta.env.QUASAR_*`; `rawDefine`/`env` -> `define`/`defineEnv`.
- Folders/modes: SSR server choice (Hono/Express/Fastify/Koa) + `serve.devError()`; PWA SW under `/src-pwa/sw/`; BEX needs `/src-bex/package.json`; Capacitor `defineCapacitorConfig()`; Electron preload `#q-app/electron/preload` (`.cjs`).
- Engines/peers: Node 22+; `vue-router >= 5`, `pinia ^2 || ^3`; Vite 8 + Rolldown under the hood.

For the exact per-line `quasar.config`/boot/component shapes, use the cookbook in `11-cli-cookbook-and-examples.md`.

## Quasar 2.20.x framework notes

The framework (`quasar`) and the CLI (`@quasar/app-vite`) version independently. `quasar` is at `2.20.1`.

- 2.20.0 modernized the codebase: "UI now much smaller and faster", better Rolldown-API leverage, removed the legacy vetur build step.
- **Behavior change to flag:** `Cookies` now uses `MaxAge` instead of `expires`. Re-check cookie expiry assumptions when upgrading.
- Fixes: `QPopupProxy` no longer wrongly emits `update:modelValue`; `QDrawer` `hideOnRouteChange`; `QInput type="number"` label overlap; `QDialog` backdrop a11y.
- No new components and no deprecations in the 2.19 -> 2.20 range.

## Quasar v3 (UI framework) status

- The Quasar **UI framework** v3 is only **Planned** (roadmap: input gathering Q3-Q4 2026, release "hopefully" Q1 2027). It is not in beta or RC.
- Do not conflate it with `@quasar/app-vite` v3, which is a CLI major currently on the `latest` dist-tag but still RC (not stable). When someone says "Quasar 3", confirm whether they mean the CLI (RC) or the UI framework (planned).

## Vite 8 migration risks

From the official Vite migration guide. All of these are real for Vite 8 (`8.0.16`):

- Dependency optimization (pre-bundling) uses **Rolldown** instead of esbuild. `optimizeDeps.esbuildOptions` is deprecated and auto-maps to `optimizeDeps.rolldownOptions`.
- JS transforms and minification moved to **Oxc**. The `esbuild` config option is deprecated in favor of `oxc`; `build.minify: 'esbuild'` is deprecated.
- CSS minification uses **Lightning CSS** by default (not "Oxc CSS" — that is a common third-party error). Revert via `build.cssMinify: 'esbuild'` if needed.
- **CommonJS default-import** behavior is now more consistent and may break packages relying on old interop. Escape hatch: `legacy.inconsistentCjsInterop: true`.
- The **object form of `manualChunks` is removed** (breaking). Function form is deprecated in favor of Rolldown's `codeSplitting` option.
- `build.rollupOptions` -> `build.rolldownOptions` (and `worker.rollupOptions` -> `worker.rolldownOptions`). Old names still work via a deprecated compat layer.
- `rolldown-vite` is **merged into** Vite 8 (no longer a separate package).
- Node requirement is **unchanged** from Vite 7: 20.19+ or 22.12+. (Quasar app-vite v3 raises the effective floor to Node 22+.)
- Default browser targets raised (Chrome 111, Edge 111, Firefox 114, Safari 16.4). Watch this if you must support older browsers.
- Stricter circular-import warnings under Rolldown where Rollup was silent.

When a Quasar app fails only after a toolchain bump, check these surfaces before assuming a Quasar regression.

## Vue Router 5 notes

- Router 5 is a **"boring" major**: it merges `unplugin-vue-router` (file-based routing) into the core package with **no breaking changes for standard users**. Plain Router 4 -> 5 upgrades with zero code changes.
- The one narrow breaking change is for IIFE/CDN consumers (devtools-api no longer bundled) — irrelevant to bundler-based Quasar apps.
- File-based-routing users only rename imports: `unplugin-vue-router/vite` -> `vue-router/vite`, `unplugin-vue-router` -> `vue-router/unplugin`, data loaders -> `vue-router/experimental`.
- `@quasar/app-vite` v3 adds first-class Router 5 filename-based routing support, but the default Quasar scaffold still uses a programmatic `src/router/`, which is unaffected.

## Vue 3.5 SSR-relevant features

Baseline since Vue 3.5 (current `3.5.38`); use them to prevent or scope hydration issues:

- `useId()` — app-stable IDs consistent across server and client; the correct fix for form/aria-id hydration mismatches.
- `data-allow-mismatch` — suppress expected hydration-mismatch warnings (e.g. localized dates); optionally scope it (`text`, `children`, `class`, `style`, `attribute`).
- Lazy hydration for async components; `useTemplateRef()`; reactive props destructure.

## Workbox 7.4.x notes

- `7.4.0`/`7.4.1` are maintenance/security releases (dependency bumps, Rollup v4). No behavior change for InjectManifest/GenerateSW users. Treat as a safe bump.

## Dual-runtime maintenance rules (Claude Opus + GPT-5/Codex)

This pack is consumed by both Claude Opus 4.x and GPT-5/Codex agents. When editing the pack itself, follow `references/90-agent-authoring-and-dual-runtime.md`. The short version:

- Keep `SKILL.md` small and route to references (progressive disclosure). Keep the body well under 500 lines.
- Keep the `name` and `description` frontmatter accurate; the description is the trigger signal.
- Make every rule literal and explicitly scoped; modern Opus does not silently generalize a rule, and GPT-5/Codex burns reasoning tokens reconciling vague or contradictory rules.
- Eliminate contradictions across files. If two rules can conflict, order them into explicit precedence.
- Pair every "don't" with a concrete "do instead". Avoid ALL-CAPS `CRITICAL`/`MUST` spam; normal imperatives steer modern models better.
- Prefer instructions over scripts unless determinism or repeated live refresh earns the script (the version checker does).

## Package-manager guidance

- Quasar supporting Bun/pnpm does not mean a Yarn repo should switch. If a project uses Yarn workspaces or contains `yarn.lock`, prefer Yarn for installs and scripts.
- Use registry-inspection commands only for version discovery; do not infer the repo's package-manager contract from them.
- pnpm v11 + app-vite v3 needs the `allowBuilds` entries noted above.

## Helpful doc endpoints

- Vite ships `vite.dev/llms.txt` and `vite.dev/llms-full.txt` for LLM-optimized retrieval (both confirmed live).
- Vite stable docs live on `vite.dev`; `main.vite.dev` shows upcoming changes but may be ahead of the installed release.
- Quasar docs are authoritative for API usage, but release/version data moves faster than the docs site. Pair Quasar docs with release notes or npm checks when the user asks for the latest.
- Official upgrade guide: `quasar.dev/quasar-cli-vite/upgrade-guide/`.
