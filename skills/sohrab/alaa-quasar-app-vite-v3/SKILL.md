---
name: alaa-quasar-app-vite-v3
description: "The complete Quasar CLI + Vite skill: building, upgrading, and modernizing Quasar apps on @quasar/app-vite v3 (the stable production line since 3.0.1, 2026-07-07), plus maintaining v2 repos and migrating them. Covers quasar.config, env, boot/routing, components/layouts/directives/plugins, platform modes (SPA/SSR/PWA/BEX/Capacitor/Electron), full-featured service workers and offline, update UX, WebOTP/SMS OTP autofill, device fingerprinting and device trust, browser device APIs and the permission model (audio recording, camera, geolocation, notifications, clipboard, wake lock, sensors; permission priming UX and cross-browser prompt behavior), testing/CI, a11y/performance guardrails, and the v2 -> v3 migration playbook. Use when the user mentions Quasar, quasar.config, app-vite, QTable/QImg/QLayout-style symbols, a Quasar upgrade/migration, service worker or offline work in a Quasar app, OTP autofill, getUserMedia/recording, geolocation, or browser permissions. Do not use for plain Vue/Vite apps without Quasar CLI."
---

# Alaa Quasar App-Vite v3

## Purpose

The single skill for Quasar CLI + Vite work. It absorbed the former `quasar-skill-packe` (exact Quasar API/config/component shapes) and `alaa-app-vite-quasar` (v2-era semantics and the verified v2->v3 delta list), and leads with the v3 era:

- `@quasar/app-vite` **v3 is the stable production line** (3.0.1 since 2026-07-07); v2 (last stable 2.6.2) is the maintenance line (~until 2027-06) covered here for not-yet-migrated repos.
- v2 -> v3 migration decision, playbook, and verified delta checklist
- exact Quasar shapes: `quasar.config`, env, boot files, routing, components, layouts, directives, plugins, composables, utils, platform modes
- production-grade service workers: offline strategies, update lifecycle UX, performance, debugging, push/badging/background sync
- SMS OTP reading (WebOTP + `one-time-code`), device fingerprinting bounded to device trust, passkey-forward posture
- browser device APIs and the permission model: audio recording, camera, geolocation, notifications, clipboard, wake lock, sensors — cross-browser prompt behavior, permission priming UX, denial recovery, and the web-vs-Capacitor permission split
- testing/CI, a11y/performance guardrails, and modern-experience decisions

Written for both Claude/Opus and GPT/Codex agents. High-value rules use ✅ Do / ❌ Don't pairs: the ✅ side is the instruction, the ❌ side is a realistic mistake kept as a guardrail.

## Version posture (the rule that dates fastest)

- New apps: scaffold on **v3**. Production apps on v2: migration is a scheduled engineering task, planned via `references/10-v2-to-v3-migration.md` — never an opportunistic bump inside an unrelated change.
- v2 repos with blockers (Node floor, incompatible App Extensions, frozen release windows) stay legitimate: keep them pinned to `@quasar/app-vite@^2` (an unpinned install now pulls v3) and use the v2 shapes in `references/12-v2-maintenance-playbook.md`.
- **Detect the installed major first** — the highest-impact rule in this skill. Read `@quasar/app-vite` in `package.json` before giving any config/import/env advice. The lines differ in import paths (`#q-app` vs `#q-app/wrappers`), env (`import.meta.env.QUASAR_*` vs `process.env.*`), aliases (`@/` only vs legacy set), and folder layout.
- Respect the repo's package manager (lockfile); never switch it as part of a Quasar task.
- Refresh version truth before version-sensitive work:

```bash
node scripts/check-upstream-versions.mjs
```

Snapshot 2026-07-08: `@quasar/app-vite` 3.0.1 (stable, `latest`) / v2 2.6.2 (maintenance); quasar 2.21.1; @quasar/extras 2.0.2; vite 8.1.3; vue 3.5.39; vue-router 5.1.0; pinia 3.0.4; workbox-build 7.4.1. Node for v3: `^22.22.0 || ^24 || ^26 || ^28 || ^30`.

## Token-efficient working model

Do not load everything. Sequence:

1. Read the repo first: lockfile, `package.json`, `quasar.config.*`, and only the mode folders the task touches. Repo-local `AGENTS.md`/`CLAUDE.md` override this skill.
2. Read `references/00-topic-map.md` unless you already know the exact file; then load only that file and its "Also load" pairings.
3. For anything version-sensitive or claimed after 2026-07-08, refresh live data (`references/80-upstream-deltas-and-live-checks.md`, `references/90-maintenance-and-live-checks.md`).

## Routing map

Migration and v2 era:

- v2 -> v3 migration playbook (plan, execute, validate, rollback): `references/10-v2-to-v3-migration.md`
- Repo-scan template, v2-safety/v3-readiness checklists, and the authoritative verified delta list (§7–8): `references/11-review-and-upgrade-checklist.md`
- v2 maintenance coding contract (env, aliases, boot, routing, Pinia on v2): `references/12-v2-maintenance-playbook.md`
- Correct/wrong review-answer examples: `references/13-examples-review-style.md`

v3 config and CLI:

- v3 capability map, env contract, sharp edges, Quasar UI 2.18–2.21 digest: `references/20-v3-config-and-features.md`
- quasar.config structure, aliases, `extendViteConf`, env files, proxies, lazy loading: `references/21-cli-vite-and-config.md`
- Exact per-line config/boot/env/alias code shapes (cookbook): `references/22-cli-cookbook-and-examples.md`

SSR, PWA, service workers:

- Service worker implementation depth (strategies, update UX, performance, debugging, push/badging): `references/30-service-worker-excellence.md`
- SSR rules, hydration tools, SSR/PWA structure, auth/env-secret rules, GenerateSW vs InjectManifest: `references/31-ssr-pwa-and-security.md`
- Custom-SW change guardrails (single `__WB_MANIFEST`, safe-vs-risky edits, verification minimum): `references/32-pwa-injectmanifest-guard.md`
- SSR mental model, request isolation, SEO/useMeta, register-sw hooks, SSR+PWA takeover: `references/33-ssr-pwa-playbook.md`
- SPA vs SSR vs PWA vs BEX vs Capacitor vs Cordova vs Electron structure: `references/35-platform-modes.md`

Auth and experience:

- WebOTP, SMS autofill, fingerprinting, device trust, passkeys: `references/40-webotp-and-device-trust.md`
- Browser device APIs + permission model (recording, camera, geolocation, notifications, clipboard, wake lock, sensors; priming UX, denial recovery, permission testing, Capacitor split): `references/45-browser-apis-and-permissions.md`
- Mode selection, install UX, perceived performance, modern-experience decisions: `references/50-modern-experience.md`

Components and APIs:

- Component family routing: `references/60-components-and-layouts.md`
- Per-component playbooks and searchable index (~70 components): `references/61-component-usage-atlas.md`
- Layout shells, `view` semantics, drawers, routing-with-layouts: `references/62-layout-patterns-and-examples.md`
- Deterministic QImg delivery, placeholders, responsive sizing: `references/63-image-delivery-and-placeholders.md`
- Plugins, composables, directives, options, utils routing: `references/64-plugins-composables-directives-options-utils.md`
- Directive atlas: `references/65-directive-usage-atlas.md`
- Plugin/composable/option/util atlas: `references/66-api-usage-atlas.md`

Quality, testing, maintenance:

- A11y, performance audit, monorepo packaging, tree-shaking guardrails: `references/70-guardrails-a11y-performance-monorepo.md`
- Quasar testing extensions, test layers, CI validation: `references/75-testing-ci-playbook.md`
- Live version snapshot, v2-vs-v3 split table, Vite 8 / Router 5 / Vue 3.5 notes: `references/80-upstream-deltas-and-live-checks.md`
- Legacy `quasar-*` skill-name coverage map: `references/85-legacy-skill-coverage.md`
- Skill maintenance and freshness triggers: `references/90-maintenance-and-live-checks.md`
- Dual-runtime authoring conventions (when editing this pack): `references/91-agent-authoring-and-dual-runtime.md`

## Mandatory related-topic rules

Apply these even if the user names only one surface:

- Any custom service worker or InjectManifest change: load `references/30-service-worker-excellence.md` AND `references/32-pwa-injectmanifest-guard.md` (verification minimum: install -> update -> offline).
- Any SSR, `preFetch`, router, store, boot, middleware, SEO, or auth task: also load `references/31-ssr-pwa-and-security.md`.
- Any platform-mode task: read `references/21-cli-vite-and-config.md` and `references/35-platform-modes.md` together.
- Any offline feature storing structured data (drafts, progress, outbox): route the data design to `$alaa-indexeddb-browser-storage`; the SW owns only Request/Response caching.
- Any OTP/auth flow: token storage and refresh stay with `$alaa-frontend-developer` `references/21-ssr-auth-and-session-patterns.md` and `$alaa-trust-gateway-auth`; WebOTP code only reads the code into the form.
- Any use of a permission-gated browser API (`getUserMedia`, geolocation, `Notification.requestPermission`, clipboard read, sensors, ...): load `references/45-browser-apis-and-permissions.md` — request inside a user gesture with a priming step, handle denial with recovery UI, and treat `granted` as a cache that expires.
- Any component handling data grids, virtualization, uploads, media, dialogs, or browser APIs: also load `references/70-guardrails-a11y-performance-monorepo.md`.
- Any version-sensitive or upgrade request: read `references/80-upstream-deltas-and-live-checks.md` and refresh live data first.
- Any Vue/TS code produced: `$alaa-vue-typescript-clean-code` gates apply.
- Any motion/animation polish: follow `$alaa-frontend-developer` `references/25-modern-css-and-motion.md` (reduced-motion is blocking).
- Anything under `packages/*`: pair `$alaa-mono-package`.

## Search rules

Search exact Quasar symbols first (`QTable`, `QImg`, `useMeta`, `ClosePopup`, `Notify`, `extendViteConf`), then task phrases (`boot files`, `ssrContext`, `InjectManifest`, `build.env.folder`, `#q-app`, `OTPCredential`, `skipWaiting`, `getUserMedia`, `MediaRecorder`, `permissions.query`, `requestPermission`). The per-symbol atlas files (61, 65, 66) carry searchable indexes; `references/85-legacy-skill-coverage.md` maps old `quasar-*` skill names.

## Companion routing (surviving siblings)

- `$alaa-frontend-developer` — broad frontend engineering: SSR auth/session, API data shaping, performance/Web Vitals, QA/release readiness, modern CSS/motion.
- `$alaa-vue-typescript-clean-code` — mandatory code-quality baseline for any Vue/TS code.
- `$alaa-indexeddb-browser-storage` — browser storage, offline data, outbox/sync (this skill is its named PWA/Quasar pairing).
- `$alaa-mono-package` — `packages/*` boundaries; `$alaa-frontend-devops` — CI/Docker/deploy; `$alaa-trust-gateway-auth` — gateway auth; `$playwright`/`$playwright-interactive` — browser validation (opt-in).

## When NOT to use

- Plain Vue/Vite apps without Quasar CLI (`@quasar/vite-plugin` is not app-vite).
- Broad frontend engineering with no Quasar surface — `$alaa-frontend-developer`.
- Backend-only or infra-only tasks.

## Final response contract

Report: what the repo showed (line, modes, blockers); what you changed or recommend and why it is safe on the repo's line; validation commands actually run with outcomes; what remains (deferred modes, AEs, unverified claims). For migrations, report per mode. Never claim a check passed that did not run.
