---
name: alaa-frontend-developer
description: "Frontend engineering policy and routing hub for the Vue 3 + Quasar + Vite app family: SSR and hydration determinism, cleanup safety, SSR auth and session posture, PWA and service-worker policy, the Lighthouse and Core Web Vitals playbook, and the client-side half of resilience, security, observability and input contracts. Use when implementing or reviewing frontend code in such an app, when a UI symptom may come from SSR, hydration, auth, caching or bundle cost, and when choosing which frontend companion skill to load. Do not use for Quasar API lookup (/alaa-quasar-app-vite-v3), Vue and TypeScript code quality (/alaa-vue-typescript-clean-code), visual design, RTL layout or Persian typography (/alaa-ui-ux-design-system), CI, Docker or deploy (/alaa-frontend-devops), browser storage (/alaa-indexeddb-browser-storage), or browser automation (/playwright)."
---

# Alaa Frontend Developer

Execution contract for frontend work in the standard Vue 3 + Quasar + Vite app family. Every line here is a gate or a route. The only override is a repo-local `AGENTS.md` rule or an explicit user instruction that contradicts a named line; cite the file and line you are overriding.

## When NOT to use

Stop and route when the change touches **only** one of these, with no SSR, hydration, auth-posture, service-worker-policy or Web-Vitals decision in it: an exact Quasar API or `quasar.config` key; Vue or TypeScript code quality; a visual or UX decision; a CI, container or deploy step; browser storage mechanics; browser-automation mechanics. The topic map names the owner and file for each.

## Owned here

SSR and hydration determinism and cleanup safety; which auth and session posture the repo is on and the client-side half of it; PWA and service-worker **policy** — what may change and what must not; the canonical Lighthouse and Core Web Vitals model in `references/41-lighthouse-and-web-vitals.md`, which two siblings route into instead of restating; the browser-automation gate and browser-debug evidence discipline; and the client-side expression of every contract below.

Do not use it for pure Quasar API lookup, pure visual design, browser-automation mechanics, or a task with no frontend surface.

## Non-negotiable gates

1. **SSR determinism.** No hydration mismatch, no browser global on an SSR render path, no per-request state in a module-level singleton. A change that reintroduces one is reverted, not documented.
2. **TypeScript under `strict`.** All new and modified frontend code is TypeScript. JavaScript is permitted only in a file already inside the repo's `allowJs` set.
3. **No client-side authorization decision.** A permission read in the browser selects what to render; the server decides what is allowed. A route guard, a `v-if`, or a decoded bitmap is never the enforcement point.
4. **Auth-state storage.** Apply `alaa-indexeddb-browser-storage references/61-authority-boundary.md` for credential-persistence prohibitions; hold the access token in a module-scoped variable owned by exactly one auth module.
5. **Browser automation is opt-in.** Open it only when the user asks for browser, visual or responsive validation; when a repo rule requires reproduction; or when one static pass is complete and you can name the one observation source cannot produce — exact console warning text, a computed style value, or an HTTP status. State that observation first.
6. **No service-worker strategy drift.** Do not add or widen a runtime-cache route matcher, change placeholder substitution, or alter registration and lifecycle orchestration unless that change is what was asked for.
7. **No second envelope and no second error format.**
8. **A performance budget breach blocks merge.** It clears only by a recorded exception in the repo's budget config naming the route, the new ceiling, and the approving maintainer.
9. **Proof before "done".** Select the proof level for the change surface and run it. A repo with no runner for that level is a blocking finding, not a waiver.

## Router

Before choosing an owner or acting on a changed frontend surface, read `references/00-topic-map.md` for
all matching mandatory reads and companion routes.

## Workflow and maintenance

Read the repo-local `AGENTS.md`; apply `/alaa-low-noise`; inspect the existing pattern first; name the root cause before choosing a fix; make the smallest change that removes it; run the proof level gate 9 selects.

In this skill: search keys and retired-name aliases are in `references/00-topic-map.md`; sources and maintenance in `references/95-sources-and-maintenance.md`. It ships no scripts.
