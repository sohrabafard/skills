---
name: alaa-quasar-app-vite-v3
description: "Version-aware control plane for Quasar CLI + Vite on @quasar/app-vite v3, v2 maintenance, and v2-to-v3 migration. Detect the installed line first; query exact component, directive, and plugin APIs through the project-local Quasar CLI, not bundled Markdown. Covers quasar.config, env and defines, boot and routing, components and layouts, SPA/SSR/PWA/BEX/Capacitor/Electron, service workers, offline and update UX, SSR render failure, client telemetry emission, WebOTP, browser permissions, accessibility and performance budgets. Use for Quasar, quasar.config, app-vite, QTable/QImg/QLayout-style symbols, upgrades and migrations, service workers and offline, OTP autofill, getUserMedia, geolocation, or browser permissions. Not for plain Vue/Vite without the Quasar CLI, Vue/TypeScript code quality (/alaa-vue-typescript-clean-code), broad non-Quasar frontend (/alaa-frontend-developer), CI or deploy (/alaa-frontend-devops), browser storage (/alaa-indexeddb-browser-storage), or gateway auth (/alaa-trust-gateway-auth)."
---

# Alaa Quasar App-Vite v3

## Purpose and posture

Version-aware Quasar CLI + Vite control plane, v3 first. It owns v2 -> v3 decisions and deltas, local exact-API lookup, `quasar.config`/env/boot/routing/layout/composable/mode patterns, production service workers with their offline, update, and failure behaviour, WebOTP and device-trust-bounded signals, permission-gated browser APIs, and Quasar-shaped accessibility, performance, and testing guardrails.

This is not exhaustive Quasar documentation. The references own workflows, deltas, guardrails, and high-value examples; the installed project and the official Quasar sources own exact API availability and current upstream behaviour. In ✅ Do / ❌ Don't pairs, ✅ is normative and ❌ preserves a real failure.

## Version rules

- New apps use v3. Treat a production v2 migration as scheduled engineering through `references/10-v2-to-v3-migration.md`, never an opportunistic bump inside unrelated work.
- A stated blocker — Node floor, an incompatible App Extension, a frozen release window — may keep a repo pinned to `@quasar/app-vite@^2`; unpinned installs now resolve v3. Use `references/12-v2-maintenance-playbook.md` shapes there.
- **Detect the installed major before any config, import, env, alias, or mode advice.** Read `@quasar/app-vite` in `package.json`; a declared range is not proof of the installed version. v2 and v3 differ on `#q-app/wrappers` vs `#q-app`, `process.env.*` vs `import.meta.env.QUASAR_*`, legacy aliases vs `@/`, and mode folders.
- Follow the lockfile's package manager; never switch it during a Quasar task.
- **Every version number, peer range, and Node floor lives in `references/80-upstream-deltas-and-live-checks.md`.** State none from memory; run `node <skill-dir>/scripts/check-upstream-versions.mjs` first and treat exit code `2` as "could not run", not as "clean".

## Authority and exact APIs

Match authority to the question: the live repo decides behaviour, constraints, conventions, and the installed line; the bundled bridge to the project-local `quasar describe` decides exact props, events, slots, methods, directive values, and plugin options; official Quasar docs and releases decide current upstream concepts and upgrades; these references decide workflow, guardrails, and migration.

```bash
node <skill-dir>/scripts/query-installed-quasar-api.mjs --project <repo-root> QTable -p -s -e -m
```

Read `references/05-authority-and-api-lookup.md` for lookup and fallback. No MCP is required.

## Workflow and routing

1. Read repo-local `AGENTS.md`/`CLAUDE.md`, the lockfile, `package.json`, `quasar.config.*`, and only the mode folders you touch. Repo instructions override this skill.
2. For exact APIs, query the installed API before any atlas example or model memory.
3. **`references/00-topic-map.md` is this skill's only router.** Read it unless you already know the file; each file names its own "also load" pairings.

Mandatory pairings:

- Custom service worker or InjectManifest -> `references/32-pwa-injectmanifest-guard.md` **then** `references/30-service-worker-excellence.md`; verify install, update, and offline.
- SSR, `preFetch`, router, store, boot, middleware, SEO, or auth -> also `references/31-ssr-pwa-and-security.md`.
- Any platform mode -> `references/21-cli-vite-and-config.md` + `references/35-platform-modes.md`.
- Deciding what the user sees when a request, a render, or the network fails -> `references/34-frontend-failure-and-degradation.md`.
- Sending anything from the browser to a collector -> `references/36-client-observability-contract.md`.
- A permission-gated API (`getUserMedia`, geolocation, `Notification.requestPermission`, clipboard read, sensors) -> `references/45-browser-apis-and-permissions.md`: ask inside a user gesture after a primer, provide denial recovery, treat `granted` as an expiring cache.
- Data grids, virtualization, uploads, media, dialogs -> also `references/70-guardrails-a11y-performance-monorepo.md`.
- Shipping a PWA change -> `references/37-pwa-operations-record.md`.

## Companion boundary

Structured offline data — drafts, progress, outbox, cursors — is `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`); a service worker owns only Request/Response caches. Vue and TypeScript code shape is `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`); TypeScript 6 is the fleet line and TypeScript 7 is not adopted, because Quasar has not declared support. Media playback, DRM, and in-app download are `/alaa-shaka-player` (`$alaa-shaka-player`). `packages/*` boundaries, peers, and asset reachability are `/alaa-mono-package` (`$alaa-mono-package`). Digit and text normalization of user input is `/alaa-input-normalization` (`$alaa-input-normalization`). Retry, timeout, and degradation doctrine is `/alaa-reliability-sla` (`$alaa-reliability-sla`); test design and proof levels are `/alaa-testing-strategy` (`$alaa-testing-strategy`); threat classes are `/alaa-security-review` (`$alaa-security-review`); requirement levels are `/alaa-observability-soc` (`$alaa-observability-soc`) and every emitted name is `/alaa-services-contract` (`$alaa-services-contract`). Gateway auth is `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`); the browser tus client behind `QUploader` is `/tusd-upload-platform` (`$tusd-upload-platform`); list pagination is `/alaa-keyset-pagination` (`$alaa-keyset-pagination`); complexity budgets are `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`); CI and deploy are `/alaa-frontend-devops` (`$alaa-frontend-devops`) with GitLab YAML expression in `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`); model and effort questions are `/alaa-prompting-guide` (`$alaa-prompting-guide`). `references/00-topic-map.md` §3 carries the full owner table with file paths. Cite an owner; never restate its rule here.

## When NOT to use

Do not use for plain Vue or Vite without the Quasar CLI — `@quasar/vite-plugin` is not app-vite. Do not use for broad non-Quasar frontend work, Vue/TypeScript code-quality review, CI or deployment authoring, browser storage design, gateway authentication, or backend and infrastructure tasks; each has a named owner above.

## Final response contract

Report the repo evidence you read (installed line, modes, blockers); which exact-API or official source you queried when syntax mattered; the line-specific change or recommendation and why it is safe on the detected line; the commands you actually ran and their outcomes; and the modes, App Extensions, and claims you did not verify. For a migration, report every mode separately. Never claim an unrun check passed.
