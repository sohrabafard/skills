---
name: alaa-quasar-app-vite-v3
description: "Version-aware control plane for Quasar CLI + Vite work on @quasar/app-vite v3, v2 maintenance, and v2-to-v3 migration. Detect the installed line first; query exact component, directive, and plugin APIs through the project-local Quasar CLI, not bundled Markdown. Covers quasar.config, env, boot/routing, components/layouts, SPA/SSR/PWA/BEX/Capacitor/Electron, service workers/offline/update UX, WebOTP/device trust, browser permissions, testing/CI, accessibility, and performance. Use for Quasar, quasar.config, app-vite, QTable/QImg/QLayout-style symbols, upgrades/migrations, service workers/offline, OTP autofill, getUserMedia/recording, geolocation, or browser permissions; not plain Vue/Vite without Quasar CLI."
---

# Alaa Quasar App-Vite v3

## Purpose and posture

Version-aware Quasar CLI + Vite control plane, absorbing `quasar-skill-packe` (API/config/components) and `alaa-app-vite-quasar` (v2 semantics and verified deltas), with v3 first:

- `@quasar/app-vite` v3 is stable production (3.0.1 since 2026-07-07); v2's last stable is 2.6.2, maintained ~until 2027-06 for unmigrated repos.
- Owns v2 -> v3 decisions/playbook/deltas; local exact-API lookup; curated config/env/boot/routing/layout/composable/util/mode patterns; production SW/offline/update/performance/debugging/push/badging/background-sync; WebOTP + `one-time-code`, device-trust-bounded fingerprinting/passkey posture; permission-gated browser APIs (audio, camera, geolocation, notifications, clipboard, wake lock, sensors), priming/denial recovery/web-vs-Capacitor; testing/CI/a11y/performance/modern UX.
- Supports Claude/Opus and GPT/Codex. In ✅ Do / ❌ Don't pairs, ✅ is normative; ❌ preserves a realistic failure guardrail.

This is not exhaustive Quasar documentation: references own workflows, heuristics, deltas, guardrails, and high-value examples; the installed project and official Quasar sources own exact API availability/current upstream behavior.

## Version rules

- New apps use v3. Treat production v2 migration as scheduled engineering via `references/10-v2-to-v3-migration.md`, never an unrelated opportunistic bump.
- Legitimate blockers (Node floor, incompatible App Extensions, frozen release window) may keep v2 pinned to `@quasar/app-vite@^2`—unpinned installs now pull v3; use `references/12-v2-maintenance-playbook.md` shapes.
- **Detect the installed major first:** read `@quasar/app-vite` in `package.json` before config/import/env advice. v3/v2 differ on `#q-app`/`#q-app/wrappers`, `import.meta.env.QUASAR_*`/`process.env.*`, `@/`/legacy aliases, and folders.
- Follow the lockfile's package manager; never switch it during a Quasar task.
- Before version-sensitive work run `node scripts/check-upstream-versions.mjs`.

Snapshot 2026-07-10: `@quasar/app-vite` 3.0.1 (stable/`latest`), v2 2.6.2 (maintenance); `quasar` 2.21.1; `@quasar/extras` 2.0.2; `vite` 8.1.4; `vue` 3.5.39; `vue-router` 5.1.0; `pinia` 3.0.4; `workbox-build` 7.4.1. v3 Node: `^22.22.0 || ^24 || ^26 || ^28 || ^30`.

## Authority and exact APIs

Match authority to the question: (1) live repo for behavior/constraints/conventions/installed line; (2) bundled `scripts/query-installed-quasar-api.mjs` -> project-local `quasar describe` for exact props/events/slots/methods/directive values/plugin options; (3) official Quasar docs/releases for current upstream concepts/examples/upgrades/releases; (4) these references for reusable workflow/guardrails/migration/search vocabulary.

```bash
node <skill-dir>/scripts/query-installed-quasar-api.mjs --project <repo-root> QTable -p -s -e -m
```

Read `references/05-authority-and-api-lookup.md` for lookup/fallback. MCP is unnecessary; never block on it.

## Token-efficient workflow and routing

1. Read repo-local `AGENTS.md`/`CLAUDE.md`, lockfile, `package.json`, `quasar.config.*`, and only touched mode folders; repo instructions override this skill.
2. For exact APIs, query the installed API before atlas examples/model memory.
3. Read `references/00-topic-map.md` unless the exact file is known; load only it plus named “Also load” pairings.
4. For version-sensitive or post-2026-07-10 claims, refresh via `references/80-upstream-deltas-and-live-checks.md` and `references/90-maintenance-and-live-checks.md`.

Detailed routing is owned by `00`: exact APIs/source drift `05`; migration/v2 `10`–`13`; v3 config/CLI/shapes `20`–`22`; SSR/PWA/SW/platform modes `30`–`35`; OTP/device trust/permissions/modern UX `40`–`50`; components/layouts/directives/plugins/composables/options/utils `60`–`66`; quality/testing/live deltas/legacy/maintenance `70`–`91`.

## Mandatory pairings

- Custom SW/InjectManifest -> `references/30-service-worker-excellence.md` + `references/32-pwa-injectmanifest-guard.md`; verify install -> update -> offline.
- SSR, `preFetch`, router, store, boot, middleware, SEO, or auth -> also `references/31-ssr-pwa-and-security.md`.
- Platform mode -> `references/21-cli-vite-and-config.md` + `references/35-platform-modes.md`.
- Structured offline data (drafts/progress/outbox) -> `$alaa-indexeddb-browser-storage`; SW owns only Request/Response caches.
- OTP/auth -> `$alaa-frontend-developer` `21-ssr-auth-and-session-patterns.md` + `$alaa-trust-gateway-auth`; WebOTP only fills the form, never owns tokens/refresh.
- Permission-gated APIs (`getUserMedia`, geolocation, `Notification.requestPermission`, clipboard read, sensors, ...) -> `references/45-browser-apis-and-permissions.md`: request in a user gesture after priming, provide denial recovery, treat `granted` as expiring cache.
- Data grids, virtualization, uploads, media, dialogs, or browser-API components -> also `references/70-guardrails-a11y-performance-monorepo.md`.
- Version-sensitive/upgrade -> `80` + live refresh. Vue/TS output -> `$alaa-vue-typescript-clean-code`. Motion -> `$alaa-ui-ux-design-system` `70-motion-and-modern-css.md` (reduced motion blocks). `packages/*` -> `$alaa-mono-package`.

## Search and companions

Search symbols first: `QTable`, `QImg`, `useMeta`, `ClosePopup`, `Notify`, `extendViteConf`. For props/events/slots/methods/options, query installed APIs, then atlases `61`, `65`, `66` for intent/alternatives/gotchas/terms. Concept terms: `boot files`, `ssrContext`, `InjectManifest`, `build.env.folder`, `#q-app`, `OTPCredential`, `skipWaiting`, `getUserMedia`, `MediaRecorder`, `permissions.query`, `requestPermission`. `references/85-legacy-skill-coverage.md` maps old `quasar-*` skill names.

Companions: `$alaa-frontend-developer` (broad frontend, SSR auth/session, data shaping, Web Vitals, QA, CSS/motion); `$alaa-vue-typescript-clean-code` (mandatory Vue/TS); `$alaa-indexeddb-browser-storage` (storage/offline/outbox); `$alaa-mono-package` (`packages/*`); `$alaa-frontend-devops` (CI/Docker/deploy); `$alaa-trust-gateway-auth` (gateway auth); `$playwright`/`$playwright-interactive` (opt-in browser validation).

## When NOT to use

Do not use for plain Vue/Vite without Quasar CLI (`@quasar/vite-plugin` is not app-vite), broad non-Quasar frontend work (use `$alaa-frontend-developer`), or backend/infra-only tasks.

## Final response contract

Report repo evidence (installed line, modes, blockers); exact-API/official source queried when syntax mattered; safe line-specific change/recommendation and rationale; commands actually run/outcomes; deferred modes, AEs, and unverified claims. For migrations, report each mode. Never claim an unrun check passed.
