# Repo assessment, stop conditions, and the migration plan

You are about to review a Quasar repository you did not write, or produce a migration-readiness assessment or plan document. This file owns two artifacts — the repository assessment you emit before any nontrivial plan, and the migration plan template — plus the conditions that stop a migration.

The delta set is `references/80-upstream-deltas-and-live-checks.md` §4. The migration sequence and failure recovery are `references/10-v2-to-v3-migration.md`. Do not restate either here.

## 1. Repository assessment — emit before planning

Read the lockfile, `package.json`, `quasar.config.*`, the mode folders that exist, and the CI and test scripts. Then emit this block. A field you could not determine is written as `unknown`, never guessed.

```md
Repo assessment:
- Package manager (from the lockfile):
- @quasar/app-vite (installed, not the declared range):
- quasar (UI):
- vue / vue-router / pinia:
- Node (engines field, CI image, Docker image):
- Modes present: SPA / SSR / PWA / Capacitor / Cordova / Electron / BEX
- Env model: process.env / import.meta.env / mixed
- Alias style: @/ / legacy / mixed
- Workbox mode and whether a custom service worker exists:
- Testing harnesses and CI entry points:
- App Extensions declared:
- Risk flags:

Plan:
1. ...

Validation (commands, per mode):
- ...

v3-readiness notes:
- ...
```

## 2. Stop conditions — do not continue the migration while any holds

Each is observable from the repository. Report it and stop; do not work around it.

- An App Extension in `package.json` has no release declaring `compatibleWith('@quasar/app-vite', '^3.0.0')`.
- The CI image or the Docker base image runs a Node version outside the target's engine range.
- The repository has an uncommitted or unreviewed lockfile diff before the migration starts.
- A `vite.config.*` exists in a Quasar CLI app — the app is either not a CLI app or has a configuration that the migration will silently break. The distinction is `references/13-examples-review-style.md` §1.
- `.quasar/` contains hand edits. It is generated; edits there are lost by `quasar prepare` and hide the real configuration.
- The repository is a production v2 repository and the change in front of you is not a scheduled migration. Then this is `references/12-v2-maintenance-playbook.md` work, not this file's.

## 3. Review checks by area

Run the areas that apply to the change. Each line is a check with an observable answer, not a preference.

**v2 production safety.** No app-vite v3 upgrade arrived incidentally. No unreviewed lockfile churn. No new `vite.config.*`. No edits under `.quasar/`. No browser-only code on an SSR server path. No secret in a client-prefixed variable. No request or user state in a module global. Build and test commands match the modes that actually exist.

**v3 readiness.** New imports use `@/`. **Add no alias other than `@/`; if an existing import cannot resolve through `@/`, leave the existing alias untouched and record it under "migration debt" in §4.** Env access is direct and static, so a codemod can rewrite it — never destructured, never dynamically indexed, never logged as a whole object. v3-only syntax stays on the migration branch. `#q-app/wrappers` -> `#q-app` is noted for the migration, not forced onto a v2 repository. Node and `vue-router` requirements are checked against the installed versions before the branch is cut.

**SSR.** `window`, `document`, `localStorage`, `sessionStorage`, and `navigator` appear only inside client guards or mounted hooks. API-client factories carry the request's headers and cookies. The app, router, and store instances are per request. Hydration-sensitive values are deterministic or client-only. Meta goes through `useMeta`. Server assets and runtime secrets stay server-side. The render middleware classifies every throw per `references/34-frontend-failure-and-degradation.md` §1.

**PWA.** The service worker and the main-thread registration are separate files. **No private, authentication, or payment endpoint appears in any cache route** — the invariant and its one documented exception path are `references/30-service-worker-excellence.md` §7. Media is not precached; it belongs to `/alaa-shaka-player` (`$alaa-shaka-player`), `references/50-offline-and-in-app-download.md`. The update UX and the offline matrix exist and are recorded per `references/37-pwa-operations-record.md`. A production build has been through the five verifications in `references/32-pwa-injectmanifest-guard.md` §6.

**Tests.** Lint and typecheck run in CI. Unit tests cover the changed logic. Component tests mount the required Quasar, router, and Pinia plugins. The Quasar-shaped regressions in `references/75-testing-ci-playbook.md` exist for the modes that ship. Every affected mode builds.

## 4. Migration plan template

```md
# app-vite v3 Migration Plan

## Current state
- @quasar/app-vite (installed):
- quasar:
- Node (dev / CI / Docker):
- package manager:
- modes:

## Blocking requirements
- Node and runtime images:
- vue-router:
- App Extensions with no v3 release:
- CI images:

## Required source migrations
- #q-app/wrappers -> #q-app:
- aliases -> @/:
- process.env -> import.meta.env.QUASAR_*:
- quasar.config build and env changes:
- per-mode package.json:
- src-pwa/sw move and sourceFiles value:
- SSR server choice and middleware:
- Capacitor config:

## Migration debt (each item: what, why it stayed, when it is removed)
-

## Risk assessment
- Production risk:
- SSR and PWA risk:
- CI/CD risk:
- rollback plan:

## Validation matrix (one row per shipped mode)
| Mode | dev | build | runtime check | result |
|---|---|---|---|---|
```

Search: `repo assessment`, `readiness`, `stop condition`, `blocking app extension`, `migration debt`, `migration plan`, `validation matrix`, `review checklist`.
