---
name: alaa-frontend-developer
description: "Use this skill when the task involves Vue, Quasar, or Vite frontend implementation in an app that follows the standard app-family contract or SSR, hydration, client-only guards, deterministic rendering, or cleanup safety. Do not use it when the task is pure Quasar API lookup with no broader frontend engineering decision."
---




# Alaa Frontend Developer

## Purpose

Use this as the default frontend engineering skill for the standard Vue 3 + Quasar + Vite app family.

This skill replaces a cluster of narrower frontend skills with one routing-first entry point that keeps context small while preserving coverage for:

- frontend implementation and repo-safe UI changes
- JavaScript and Vue engineering rules
- SSR and hydration safety
- SSR auth, session, token-storage, and protected-route patterns
- frontend-facing API contracts and data-shaping rules
- PWA, service worker, offline, and update-flow boundaries
- performance and realtime UI behavior
- QA and verification planning
- browser-debug decision flow
- package and asset-contract awareness

## Ownership

- `alaa-frontend-developer` owns app-family frontend engineering policy and cross-cutting frontend guardrails.
- `$alaa-quasar-app-vite-v3` owns everything Quasar CLI + Vite: exact Quasar APIs, `quasar.config`, platform modes, component/layout lookup, the `@quasar/app-vite` v3 stable line (production default since 3.0.1, 2026-07-07), the v2->v3 migration playbook, v2-era maintenance semantics, service-worker implementation depth, WebOTP/device-trust flows, and modern-experience decisions.
- Broader art direction, visual thesis, composition, premium hierarchy, and motion language stay outside this skill unless a concrete frontend implementation task is also in scope.
- `$playwright`, `$playwright-interactive`, and configured Playwright MCP profiles own browser mechanics and execution loops. Browser automation is opt-in: use it only when the user explicitly asks for browser, Playwright, visual, or responsive validation, a higher-priority repo rule requires it, or static analysis is no longer trustworthy for a browser-only bug. Prefer `playwright_headless` for deterministic headless browser checks and `playwright_visual` for headed visual QA when those MCP profiles are available.
- `$openai-docs` owns authoritative current OpenAI and Codex product guidance.

## When to use

Use this skill when the task includes any of the following:

- Vue, Quasar, or Vite frontend implementation in an app that follows the standard app-family contract
- SSR, hydration, client-only guards, deterministic rendering, or cleanup safety
- auth, session, login, logout, silent refresh, cookie, bearer-token, or protected-route behavior
- API envelopes, pagination, filtering, sorting, sparse payloads, or cache-validator behavior that affects frontend correctness or efficiency
- frontend behavior around PWA, service workers, offline fallback, or update UX
- performance, hydration cost, Web Vitals, or runtime efficiency
- WebSocket or SSE lifecycle, reconnect behavior, or realtime UI state
- QA planning, verification mapping, release-readiness checks, or browser-debug evidence collection
- package asset emission, dist-only package consumption, or browser-asset contract risks
- choosing which companion frontend skill to load for a mixed frontend task

## When NOT to use

Do not use this skill when:

- the task is pure Quasar API lookup with no broader frontend engineering decision
- the task is pure visual art direction with no frontend implementation constraint
- the task is browser automation mechanics only
- the task is backend-only, infra-only, or unrelated to frontend behavior

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Apply `$alaa-low-noise`.
3. Start with `references/00-topic-map.md` unless you already know the exact reference to load.
4. Load only the smallest relevant reference file.
5. Follow that file's pairing guidance before making changes.

Also load companion skills when needed:

- exact Quasar API/config/platform behavior, v3 builds, a v2->v3 migration, v2 maintenance, SW depth, or WebOTP/device trust -> `$alaa-quasar-app-vite-v3`
- visual ambition or art direction -> stay in this skill only when it also requires Vue, Quasar, Vite, SSR, or implementation constraints
- explicit browser validation or reproduction -> `$playwright` or `$playwright-interactive`; when MCP browser tools are configured, route deterministic non-visual checks to `playwright_headless` and headed visual QA to `playwright_visual`
- Ala gateway or trusted-header auth model -> `$alaa-trust-gateway-auth`
- CI, Docker, artifact, or deployment contract risks -> `$alaa-frontend-devops`
- package boundary or asset emission risks -> `$alaa-mono-package`
- shared Crockford Base32 or UUIDv7 codec parity across frontend, backend, shell, or edge layers -> `$alaa-crockford-base32-codecs`
- documentation-only annotation pass -> `$alaa-frontend-doc-annotations`
- OpenAI or Codex docs, examples, or maintenance guidance -> `$openai-docs`

## Routing map

- Standard app-family contract, boundaries, monorepo rules, SSR auth/session boundaries, and workflow defaults:
  - `references/10-contract-and-boundaries.md`
- SSR auth, session, token-storage, refresh, BFF, and gateway-aware frontend patterns:
  - `references/21-ssr-auth-and-session-patterns.md`
- Vue, JavaScript, SSR, hydration, lifecycle, reactivity, and JSDoc defaults:
  - `references/20-vue-js-ssr-patterns.md`
- Modern CSS platform features (container queries, :has(), View Transitions, scroll-driven animations, @starting-style, popover, anchor positioning, oklch/light-dark theming) and the classy-motion contract (durations, easing, stagger, reduced-motion, compositor-only rules):
  - `references/25-modern-css-and-motion.md`
- PWA, service worker, offline fallback, update flow, and safe SW change boundaries:
  - `references/30-pwa-sw-and-offline.md`
- Performance, runtime efficiency, Web Vitals, WebSocket, and SSE patterns:
  - `references/40-performance-and-realtime.md`
- Frontend-facing API contracts, pagination, caching, sparse payloads, and DB-aware data-shaping:
  - `references/45-api-and-data-shaping.md`
- QA planning, verification mapping, release readiness, and evidence capture:
  - `references/50-qa-and-verification.md`
- UI-spec, design-safe implementation, browser-debug flow, and UX edge cases:
  - `references/60-design-browser-debug-and-ux.md`
- Companion skill ownership and pairing rules:
  - `references/70-companion-skill-routing.md`
- Mapping from deleted skill names and old shared-doc topics:
  - `references/80-legacy-skill-coverage.md`
- Live upstream deltas, prompt-maintenance rules, and skill-maintenance workflow:
  - `references/90-upstream-deltas-and-maintenance.md`

## Mandatory cross-topic rules

Apply these even when the user names only one surface:

- Any SSR, hydration, router, store, boot, auth, or browser-only API task:
  - Also load `references/20-vue-js-ssr-patterns.md`.
- Any auth, session, token storage, silent refresh, protected-route, or gateway-backed frontend task:
  - Also load `references/21-ssr-auth-and-session-patterns.md`.
  - If trusted headers, gateway verification, or downstream auth context matter, pair with `$alaa-trust-gateway-auth`.
- Any service worker, offline, update UX, or caching task:
  - Also load `references/30-pwa-sw-and-offline.md`.
  - If Quasar config or InjectManifest shape matters, pair with `$alaa-quasar-app-vite-v3`.
  - For implementation depth (Workbox recipes, update-UX code, SW debugging, push/badging), pair with `$alaa-quasar-app-vite-v3`.
- Any animation, transition, motion polish, or modern-CSS-feature task:
  - Also load `references/25-modern-css-and-motion.md`.
  - Treat `prefers-reduced-motion` support as a blocking gate, not polish.
- Any package, asset, dist-output, or missing-chunk task:
  - Also load `references/10-contract-and-boundaries.md`.
  - Pair with `$alaa-mono-package` when `packages/*` or package outputs are involved.
- Any API contract, pagination, filter, sort, sparse-field, or cache-validator task:
  - Also load `references/45-api-and-data-shaping.md`.
- Any UI change that appears "frontend-only" but is really caused by backend query shape, count cost, or missing aggregation:
  - Also load `references/45-api-and-data-shaping.md`.
  - Pair with `$alaa-laravel-architecture` or `$alaa-data-layer` when the fix crosses into server implementation.
- Any visually ambitious landing page or premium UI task:
  - Use this skill for implementation constraints, SSR safety, Quasar/Vite integration, and verification planning.
  - Treat pure art direction with no frontend implementation constraint as out of scope.
- Any explicit browser validation request, visual QA request, or browser-only reproduction:
  - Pair with `$playwright` or `$playwright-interactive`.
  - When MCP browser profiles are configured, prefer `playwright_headless` for deterministic headless smoke checks and `playwright_visual` for headed visual inspection.
  - Do not select `MCP_DOCKER` only to get a headless browser when a Playwright headless profile is available.
- Any frontend task without explicit browser permission:
  - Prefer source inspection, tests, logs, static DOM/CSS reasoning, and existing screenshots or artifacts.
  - Do not open browser automation merely because the task is frontend, Quasar, Vite, visual, or responsive.
  - If browser execution becomes necessary because static evidence is insufficient, state that pivot and the target route/check before opening it.
- Any task that depends on the `@quasar/app-vite` version line (v2 vs v3), a v3 build, a v2->v3 migration, or an exact per-line `quasar.config`/boot/component shape:
  - Require `$alaa-quasar-app-vite-v3`; v3 is the stable production line since 3.0.1 (2026-07-07), and that skill also owns the v2 maintenance semantics and the migration playbook.
- Any "latest", maintenance, migration, or skill-authoring task:
  - Load `references/90-upstream-deltas-and-maintenance.md`.
  - Use `$openai-docs` for OpenAI or Codex-specific claims.

## Search rules

When searching inside this skill pack:

- Start with exact frontend concepts:
  - `hydration`, `onMounted`, `AbortController`, `BFF`, `token-mediating backend`, `silent refresh`, `localStorage`, `network-only`, `offline fallback`, `controllerchange`, `WebSocket`, `SSE`, `LCP`, `INP`, `cursor pagination`, `ETag`, `If-None-Match`, `problem details`, `sparse fields`, `view transitions`, `startViewTransition`, `container queries`, `:has()`, `@starting-style`, `allow-discrete`, `popover`, `anchor positioning`, `oklch`, `light-dark`, `prefers-reduced-motion`, `linear()`
- Search old skill names in `references/80-legacy-skill-coverage.md` when the task uses prior terminology.
- Search the companion routing reference when multiple skills could apply and ownership is unclear.
- Refresh live package versions with `node scripts/check-upstream-versions.mjs` before version-sensitive changes.

## Companion chooser

| If the task is mainly about...                                          | Pair with                        |
|-------------------------------------------------------------------------|----------------------------------|
| CI, Docker, artifact paths, CDN, or deploy/runtime delivery             | `$alaa-frontend-devops`          |
| inline comments or JSDoc only                                           | `$alaa-frontend-doc-annotations` |
| `packages/*`, peer deps, asset emission, or workspace package contracts | `$alaa-mono-package`             |
| Quasar CLI, `quasar.config`, platform modes, exact Quasar APIs, v3 builds, v2->v3 migration, v2 maintenance, SW depth, WebOTP, device trust | `$alaa-quasar-app-vite-v3` |
| live OpenAI or Codex product behavior                                   | `$openai-docs`                   |

## Maintenance rules

- Keep this skill focused on one job: frontend engineering for the standard Vue 3 + Quasar + Vite app family.
- Prefer progressive disclosure and route to references instead of growing `SKILL.md`.
- Add scripts only when the task is deterministic and repeated enough to justify them.
- Keep descriptions precise enough for reliable implicit invocation.
- Re-test the skill against realistic prompts after changing routing or ownership boundaries.
- Repo-local `AGENTS.md` and user instructions always override this shared skill.
