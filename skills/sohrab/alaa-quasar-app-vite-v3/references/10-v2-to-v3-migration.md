# v2 -> v3 migration playbook (`@quasar/app-vite`)

You are about to plan or execute a production `@quasar/app-vite` v2 -> v3 migration, or recover from a step of one that failed. This file owns the **sequence**, the **per-mode gate**, and the **failure classes**. The delta set itself — every renamed key, moved folder, and changed import — is stated once in `references/80-upstream-deltas-and-live-checks.md` §4; read it there and do not re-derive it from memory.

Also load `references/22-cli-cookbook-and-examples.md` (exact target shapes), `references/11-review-and-upgrade-checklist.md` (repo assessment and the plan template), `references/12-v2-maintenance-playbook.md` (v2 source semantics), and `/alaa-workflow` (`$alaa-workflow`) when a multi-phase plan artifact is warranted.

## 0. Preconditions

- Node: the engine range of the target app-vite version, read live from `references/80-upstream-deltas-and-live-checks.md` §2. Verify the developer, CI, and Docker runtimes separately; a CI image on an older Node is a mid-migration failure.
- Peers: read the declared peer block of the exact target version from `references/80-upstream-deltas-and-live-checks.md` §2, not a remembered range. The Pinia range in particular widened between v3 minors, so a remembered "pinia 2 or 3 only" claim will block a migration that would in fact succeed.
- **`vue-router` 4 -> 5 is a sub-migration.** Keep it a separate commit.
- Inventory every App Extension, including `@quasar/testing-*`. v3 accepts only `api.compatibleWith('@quasar/app-vite', '^3.0.0')`. Confirm a compatible release exists for each before scheduling; `@quasar/testing-*` v3 compatibility is UNVERIFIED here, so check each changelog live.
- Capacitor repositories replace `capacitor.config.json` with `capacitor.config.ts`/`.js` using `defineCapacitorConfig` from `'@quasar/app-vite/capacitor'` **before** the upgrade, not during it.
- `@quasar/extras` v2 is ESM-only and drops FontAwesome v5/v6, Ionicons v5-7, and MDI v3-6. Audit the icons in use, and bump it separately.

✅ Do — migrate on a branch with a written checklist, and keep `vue-router` 4 -> 5 and `@quasar/extras` 1 -> 2 as separate commits from the app-vite bump. ❌ Don't — hide the app-vite bump inside unrelated dependency work; the env, alias, and import changes touch application code and cannot be reviewed as a lockfile diff.

## 1. Sequence

1. Set `"@quasar/app-vite": "^3.0.0"`, `"vue-router": "^5"`, and the required peers in `package.json`.
2. Install with the lockfile's package manager; never switch it.
3. Apply the delta set from `references/80-upstream-deltas-and-live-checks.md` §4.
4. Run `quasar prepare`; restart the IDE and the TypeScript server.
5. Run `quasar dev`, then `quasar build`, for **every shipped mode**, fixing mode by mode.

Two shape rules that are easy to get wrong and are stated in full elsewhere: aliases collapse to a sole `@/` (a temporary `build.alias` + `ctx.appPaths` bridge is migration debt, recorded in the plan template at `references/11-review-and-upgrade-checklist.md` §3, never left permanent), and the custom service-worker path and its `sourceFiles` default are `references/32-pwa-injectmanifest-guard.md` §1 — writing the v2 value into a v3 config produces a service worker the CLI silently ignores.

## 2. Per-shipped-mode gate

1. `quasar prepare` succeeds and the IDE reports no `import.meta.env` type errors.
2. `quasar dev` runs; edit a `.env` value and prove hot reload without a restart.
3. `quasar build` succeeds; additionally start the production SSR server, inspect the PWA registration and precache, and verify a clean Capacitor or Cordova `www` output.
4. Lint, typecheck, and unit tests pass; then grep the tree for `process.env.`, `#q-app/wrappers`, legacy aliases, `envFolder`, `rawDefine`, and `extendManifestJson`.
5. Report the migrated scope, the exact commands and their results, and every blocking App Extension.

✅ Do — migrate, validate, and commit SPA first, then SSR, PWA, and native separately. ❌ Don't — treat a passing SPA dev server as completion; the major breaks cluster in SSR, PWA, Electron, and Capacitor.

## 3. Failure classes — symptom, diagnosis, smallest retry, escalation

| Symptom | Diagnosis | Smallest retry | Escalate when |
| --- | --- | --- | --- |
| `quasar prepare` fails | a config key removed in v3 is still present, or the config file extension is `.cjs`/`.mjs`/`.cts`/`.mts` | read the error's key name against the delta table; delete `.quasar/` and rerun once | the failing key is not in the delta table — that is an upstream change since the snapshot; verify live per `references/80-upstream-deltas-and-live-checks.md` §6 |
| An App Extension refuses to install or run | it declares `compatibleWith` for v2 only | check the extension's changelog for a v3 release | no v3 release exists: this is a **blocking** finding. Stop, record it in the plan, and decide between removing the extension, vendoring its output, or postponing the migration. Do not force-install it |
| `quasar build -m ssr` succeeds but the server returns 500 | a browser API is read during render, a boot file throws on the server, or a module global holds request state | run `node dist/ssr/index.js` locally and read the first stack frame | the frame is inside `@quasar/app-vite` — report upstream. Otherwise the rules are `references/31-ssr-pwa-and-security.md`, the response policy is `references/34-frontend-failure-and-degradation.md` §1 |
| The PWA registers but never updates | the service-worker source is at the v2 path, or `pwa.workboxMode` is `GenerateSW` while a custom service worker exists | check both against `references/32-pwa-injectmanifest-guard.md` §§1-2 | the paths are right and the update still does not arrive — the lifecycle is `references/30-service-worker-excellence.md` §4 |
| Capacitor or Cordova `www` contains stale or duplicated output | the per-mode `package.json` or `pnpm-workspace.yaml` is missing, so dependencies resolved from the wrong location | add the per-mode `package.json` with `"type": "module"`; add an empty per-mode `pnpm-workspace.yaml` on pnpm; rebuild | a native build still fails after a clean `www` — that is a native toolchain problem, not a Quasar one |
| `import.meta.env.QUASAR_*` is `undefined` at runtime | the variable is not client-prefixed, or the code destructures or dynamically indexes the env object | check the prefix and the access form against `references/20-v3-config-and-features.md` | the variable is correctly prefixed and still absent in one mode only — check which side the boot file is scoped to |
| One mode reports "module not found" and the others build | v3 installs mode dependencies under `/src-<mode>` | install the dependency in that mode folder | the module is a workspace package — that is `/alaa-mono-package` (`$alaa-mono-package`) |
| Type errors appear only in the editor | `.quasar/` tsconfigs are stale | run `quasar prepare` and restart the TypeScript server | they persist after both — check for a leftover `src-pwa/tsconfig.json` or a stray `declare namespace NodeJS` |

## 4. Rollback

Retain the pre-migration lockfile and branch until every shipped mode passes its gate. If the migration is paused, pin `@quasar/app-vite@^2` explicitly — an unpinned `latest` now resolves v3, so "we did not upgrade" is not a state an unpinned range preserves. A migration that has passed some modes and not others is not partially shippable: the branch either passes every shipped mode or it is not merged.

Search: `migration`, `upgrade`, `quasar prepare`, `compatibleWith`, `app extension blocking`, `per-mode gate`, `rollback`, `pin ^2`, `migration debt`, `SSR 500 after migration`, `www stale`.
