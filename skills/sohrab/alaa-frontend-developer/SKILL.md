---
name: alaa-frontend-developer
description: "Frontend engineering policy and routing hub for the Vue 3 + Quasar + Vite app family: SSR and hydration determinism, cleanup safety, SSR auth and session posture, PWA and service-worker policy, the canonical Lighthouse and Core Web Vitals playbook, and the client-side half of resilience, security, observability, configuration and input contracts. Use when implementing or reviewing frontend code in such an app; when a UI symptom may really come from SSR, hydration, auth, caching, backend query shape or bundle cost; and when choosing which frontend companion skill to load. Do not use it for exact Quasar API or quasar.config lookup (/alaa-quasar-app-vite-v3), Vue and TypeScript code quality (/alaa-vue-typescript-clean-code), visual design, RTL layout or Persian typography (/alaa-ui-ux-design-system), CI, Docker or deploy (/alaa-frontend-devops), browser storage mechanics (/alaa-indexeddb-browser-storage), or browser automation mechanics (/playwright)."
---

# Alaa Frontend Developer

Execution contract for frontend work in the standard Vue 3 + Quasar + Vite app family. Every line here is a gate or a route. The only override is a repo-local `AGENTS.md` rule or an explicit user instruction that contradicts a named line; cite the file and line you are overriding.

## When NOT to use

Stop and route when the change touches **only** one of these, with no SSR, hydration, auth-posture, service-worker-policy or Web-Vitals decision in it: an exact Quasar API or `quasar.config` key; Vue or TypeScript code quality; a visual or UX decision; a CI, container or deploy step; browser storage mechanics; browser-automation mechanics. The ownership table below names the owner and the file for each.

## Owned here

SSR and hydration determinism and cleanup safety; which auth and session posture the repo is on and the client-side half of it; PWA and service-worker **policy** — what may change and what must not; the canonical Lighthouse and Core Web Vitals model in `references/41-lighthouse-and-web-vitals.md`, which two siblings route into instead of restating; the browser-automation gate and browser-debug evidence discipline; and the client-side expression of every contract below.

Do not use it for pure Quasar API lookup, pure visual design, browser-automation mechanics, or a task with no frontend surface.

## Ownership — one table, route and never restate

| The subject is | Load and enter at |
|---|---|
| exact Quasar API, `quasar.config`, platform modes, v2→v3 migration, SW depth, WebOTP, installed versions | `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`) `references/00-topic-map.md` |
| TypeScript, SOLID, decomposition, Pinia shape, Vue patterns, strictness gates | `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`) `references/00-topic-map.md` |
| visual design, tokens, motion, failure-state design, RTL layout, Persian typography | `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`) `references/00-topic-map.md` |
| CI gates, artifact identity, serving, caching, public path, deploy failure | `/alaa-frontend-devops` (`$alaa-frontend-devops`) `references/00-topic-map.md` |
| `packages/*` boundaries, exports maps, peer deps, asset reachability, release gates, `dist/ssr` paths | `/alaa-mono-package` (`$alaa-mono-package`) `references/00-topic-map.md` |
| browser storage mechanics, quota, eviction, migrations, request cache, drafts, outbox, offline media | `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`) `references/00-topic-map.md` |
| video or audio playback, DRM, in-app download, ads, player analytics | `/alaa-shaka-player` (`$alaa-shaka-player`) `references/00-topic-map.md` |
| a documentation-only diff, JSDoc, `NOTE:` annotations, annotation staleness | `/alaa-frontend-doc-annotations` (`$alaa-frontend-doc-annotations`) `references/10-annotation-boundaries.md` |
| the digit and text normalization form | `/alaa-input-normalization` (`$alaa-input-normalization`) `references/20-browser-binding.md` |
| test design, layers, doubles, proof levels | `/alaa-testing-strategy` (`$alaa-testing-strategy`) `references/40-proof-strength.md` |
| timeout, retry, backoff, breaker, shedding, degradation, idempotency | `/alaa-reliability-sla` (`$alaa-reliability-sla`) `references/00-topic-map.md` |
| threat classes, review triggers, fail-closed doctrine | `/alaa-security-review` (`$alaa-security-review`) `references/25-browser-trust-and-output.md` |
| log fields, metric names, envelope keys, error codes, SDK consumption | `/alaa-services-contract` (`$alaa-services-contract`) `references/60-frontend-sdk-consumption-contract.md` |
| the requirement level of any telemetry, and its budgets | `/alaa-observability-soc` (`$alaa-observability-soc`) `references/20-instrumentation-gates.md` |
| the quality bar itself | `/alaa-project-constitution` (`$alaa-project-constitution`) `references/quality-bar.md` |
| cursor and keyset pagination contract | `/alaa-keyset-pagination` (`$alaa-keyset-pagination`) `references/40-wire-contract-limits-and-errors.md` |
| complexity budgets, structure choice, the N+1 family | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) `references/10-complexity-budget.md` |
| boundary and seam design before implementation | `/alaa-system-design` (`$alaa-system-design`) `references/10-boundary-and-seam.md` |
| identifier codec parity — run the harness, do not reason about it | `/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`) `scripts/codec-conformance.sh` |
| the permission bitmap and its decoder | `/alaa-permission-generator` (`$alaa-permission-generator`) `assets/permission-bitmap/permission-bitmap.ts` |
| gateway verification, trusted headers, downstream trust | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) `references/20-claims-headers-and-sentinels.md` |
| object storage, presigned URLs, `STORAGE_*`, resumable upload | `/alaa-minio-object-storage` (`$alaa-minio-object-storage`), `/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`), `/tusd-upload-platform` (`$tusd-upload-platform`) |
| query shape, index, or aggregate cost behind a slow screen | `/alaa-data-layer` (`$alaa-data-layer`), `/alaa-laravel-architecture` (`$alaa-laravel-architecture`) |
| real-browser execution, or a stateful debugging loop | `/playwright` (`$playwright`), `/playwright-interactive` (`$playwright-interactive`); profile choice in this skill's `references/70-companion-skill-routing.md` |
| authoritative OpenAI or Codex product behaviour | `/openai-docs` (`$openai-docs`) |
| model and effort selection | `/alaa-prompting-guide` (`$alaa-prompting-guide`) `references/50-effort-and-thinking.md` |

Two owners appear to apply: `references/70-companion-skill-routing.md`.

## Non-negotiable gates

1. **SSR determinism.** No hydration mismatch, no browser global on an SSR render path, no per-request state in a module-level singleton. A change that reintroduces one is reverted, not documented.
2. **TypeScript under `strict`.** All new and modified frontend code is TypeScript. JavaScript is permitted only in a file already inside the repo's `allowJs` set.
3. **No client-side authorization decision.** A permission read in the browser selects what to render; the server decides what is allowed. A route guard, a `v-if`, or a decoded bitmap is never the enforcement point.
4. **No token in persistent browser storage.** Do not add a new write of an access token to `localStorage` or `sessionStorage`; hold it in a module-scoped variable owned by exactly one auth module.
5. **Browser automation is opt-in.** Open it only when the user asks for browser, visual or responsive validation; when a repo rule requires reproduction; or when one static pass is complete and you can name the one observation source cannot produce — exact console warning text, a computed style value, or an HTTP status. State that observation first.
6. **No service-worker strategy drift.** Do not add or widen a runtime-cache route matcher, change placeholder substitution, or alter registration and lifecycle orchestration unless that change is what was asked for.
7. **No second envelope and no second error format.**
8. **A performance budget breach blocks merge.** It clears only by a recorded exception in the repo's budget config naming the route, the new ceiling, and the approving maintainer.
9. **Proof before "done".** Select the proof level for the change surface and run it. A repo with no runner for that level is a blocking finding, not a waiver.

## Router

One router, one hop: `references/00-topic-map.md`. Every row there states a situation observable before acting. Do not route from this file.

## Also load — these fire even when the user named one surface only

| The diff touches | Also load |
|---|---|
| SSR, hydration, a router guard, a store, a boot file, any browser-only API | `references/20-vue-js-ssr-patterns.md` |
| login, logout, refresh, a token, a protected route, an SSR request carrying identity | `references/21-ssr-auth-and-session-patterns.md` |
| a service worker, an offline path, an update prompt | `references/30-pwa-sw-and-offline.md` |
| a text input, a submit path, a validator, a formatter | `references/22-input-validation-and-normalization.md` |
| content a user or a third party supplied, or a permission read in a component | `references/25-frontend-security.md` |
| a `fetch`, a mutation, a retry, or state that can be stale or partial | `references/46-resilience-and-degradation.md` |
| a client-side event, an error report, or a trace header | `references/47-frontend-observability.md` |
| a `VITE_*` name or any other injected value | `references/48-config-and-environment.md` |
| a date, a number, or a currency formatted during SSR | `references/55-i18n-locale-and-rtl.md` |
| a claim that something is tested, or a change about to be called done | `references/05-proof-and-tests.md` |
| Lighthouse, PageSpeed, Web Vitals, LCP/INP/CLS/TBT, or "hit 90" | `references/41-lighthouse-and-web-vitals.md`; attack by weight, TBT 30% → LCP 25% → CLS 25%; production build, mobile throttling, three runs, median |
| a UI symptom that is really backend query shape, count cost, or missing aggregation | `references/45-api-and-data-shaping.md` |
| an animation, a transition, or a CSS feature that may not ship everywhere | `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`) `references/70-motion-contract.md` and `references/72-modern-css-baseline-tiers.md`; `prefers-reduced-motion` is a blocking gate |

## Workflow and maintenance

Read the repo-local `AGENTS.md`; apply `/alaa-low-noise` (`$alaa-low-noise`); inspect the existing pattern first; name the root cause before choosing a fix; make the smallest change that removes it; run the proof level gate 9 selects.

In this skill: search keys and retired-name aliases are in `references/00-topic-map.md`; sources and maintenance in `references/95-sources-and-maintenance.md`. It ships no scripts.
