# Lighthouse and Core Web Vitals (score-100 contract)

Use this file for any Lighthouse, PageSpeed Insights, Core Web Vitals, or "make it faster / hit score 90+" task. Target: performance score >= 90 on mobile (the harder profile), with 100 as the design goal on key routes. Verified 2026-07-13 against the Lighthouse source (GoogleChrome/lighthouse), developer.chrome.com, and web.dev; re-verify weights and audit IDs when a new major Lighthouse ships.

This file is the canonical copy for the pack — `$alaa-quasar-app-vite-v3` and `$alaa-ui-ux-design-system` route here instead of duplicating.

## 1. How the score is computed (optimize the math, not vibes)

Metric weights (Lighthouse 12/13 — unchanged by the v13 insights migration):

| Metric | Weight | Lab measures |
|---|---|---|
| Total Blocking Time (TBT) | 30% | main-thread long tasks (>50ms) between FCP and TTI |
| Largest Contentful Paint (LCP) | 25% | when the largest above-fold element renders |
| Cumulative Layout Shift (CLS) | 25% | visual stability (impact x distance of shifts) |
| First Contentful Paint (FCP) | 10% | first text/image paint |
| Speed Index (SI) | 10% | how quickly content visually completes |

Each metric maps to 0–100 via a log-normal curve anchored on HTTPArchive data: the p10 value scores 90, the median scores 50. Control points (ms except CLS):

| Metric | Mobile: 90 / 50 | Desktop: 90 / 50 |
|---|---|---|
| FCP | 1800 / 3000 | 934 / 1600 |
| SI | 3387 / 5800 | 1311 / 2300 |
| LCP | 2500 / 4000 | 1200 / 2400 |
| TBT | 200 / 600 | 150 / 350 |
| CLS | 0.10 / 0.25 | 0.10 / 0.25 |

Consequences:

- TBT + LCP + CLS = 80% of the score. Attack in that order unless the trace says otherwise; FCP/SI usually improve for free alongside LCP fixes.
- The curve is nonlinear: moving LCP 4000 -> 2500ms buys far more than 1200 -> 900ms. Stop polishing a metric once it is comfortably past its 90-point value and move to the next-weighted one.
- Score bands: 0–49 / 50–89 / 90–100. Mobile runs on simulated throttling (slow 4G, 4x CPU) — a fast dev machine proves nothing.
- Lighthouse 13 (Oct 2025) replaced legacy opportunity audits with DevTools-aligned insight audits (`cls-culprits-insight`, `image-delivery-insight`, `render-blocking-insight`, ...). Scoring is unchanged; anything parsing Lighthouse JSON must track the new audit IDs.

## 2. Lab vs field — two scoreboards, both must pass

- Lighthouse is lab data. Google Search uses field data: CrUX at the 75th percentile — LCP <= 2.5s, INP <= 200ms, CLS <= 0.1. INP exists only in the field; TBT is its lab proxy (low TBT almost always drags INP down with it).
- Collect field data with the `web-vitals` library (`onLCP/onINP/onCLS`, use the `web-vitals/attribution` build to identify culprits) reported to your analytics/observability lane; check CrUX via PageSpeed Insights.
- When lab and field disagree, field wins: real users have slower devices, cold caches, and real interaction patterns.

## 3. TBT and INP playbook (30% + the field metric)

- Ship less JavaScript first: route-level code splitting is baseline; heavy features (charts, editors, players) behind `defineAsyncComponent` so first load pays only for the route.
- Vue 3.5+ lazy hydration for SSR: below-fold/interaction-optional islands hydrate with `defineAsyncComponent({ loader, hydrate: hydrateOnVisible() })` or `hydrateOnIdle()` — the server HTML is already visible, so deferred hydration cuts TBT without hurting LCP. Never lazy-hydrate the primary interactive element of the route.
- Break long tasks (>50ms): chunk work and `await scheduler.yield()` between chunks (fall back to `setTimeout(0)` where unsupported, knowing it loses scheduler priority).
- INP anatomy: input delay (<50ms) + processing (<100ms) + presentation (<50ms). Handler pattern: apply the visual feedback synchronously (pressed state, optimistic UI), yield, then run the heavy work; push analytics to `requestIdleCallback`.
- Third-party scripts are the classic TBT killer: load `async`/`defer`, lazy-load on visibility, use the facade pattern (static placeholder, real embed on interaction) for video/chat/map embeds; audit and delete stale tags.
- Vue reactivity cost: `shallowRef` for large structures, avoid broad deep watchers, `v-memo` for hot list rows, virtualize long lists (QVirtualScroll / vue-virtual-scroller); keep DOM under control — thousands of nodes inflate every phase of INP.

## 4. LCP playbook (25%)

Decompose before optimizing — the four subparts point at the owner: TTFB -> resource load delay -> resource load duration -> element render delay.

- TTFB < 800ms: SSR render time, edge/CDN caching of HTML where personalization allows, compression (Brotli), HTTP/2+.
- The LCP element must be in the server HTML. A client-only hero (behind hydration, `v-if` on mounted state, or a JS-built background) moves LCP to post-hydration and caps the score.
- Kill load delay: LCP image gets `fetchpriority="high"` + eager loading (never `loading="lazy"` on it) and `<link rel="preload">` when discovered late (CSS backgrounds); `preconnect` to its origin; consider HTTP 103 Early Hints on slow origins.
- Kill load duration: AVIF/WebP, correctly sized `srcset`/`sizes`, image CDN.
- Kill render delay: minimal critical CSS (inline the above-fold subset when the repo's tooling supports it), no render-blocking third-party CSS/JS in `<head>`, `font-display: swap` so text paints.
- Next navigations: Speculation Rules prerender/prefetch for likely links (`eagerness: "moderate"` to start); gate side-effectful code on `document.prerendering` + `prerenderingchange`. Keep bfcache eligible — no `unload` listeners, no `Cache-Control: no-store` on HTML — so back/forward is instant.

## 5. CLS playbook (25% — usually the cheapest 25 points)

- Every image, video, embed, and ad slot declares dimensions or `aspect-ratio`; async content gets fixed-size skeleton/placeholder space (matches the design-side rule in `$alaa-ui-ux-design-system`).
- Fonts: metric-matched fallback via `size-adjust`/`ascent-override`/`descent-override` (or `font-display: optional` for non-brand-critical faces) so the swap does not reflow.
- Animate `transform`/`opacity` only; never height/width/top/left on live layout.
- Inject dynamic content (banners, consent, recommendations) below the viewport or in reserved space — never push existing content down.
- Debug with the `layout-shift` PerformanceObserver (`entry.sources`) or Lighthouse's `cls-culprits-insight`.

## 6. FCP and Speed Index (2 x 10% — mostly free wins)

- Non-critical CSS deferred; no `@import` chains; total CSS lean (see budgets).
- Compression + caching headers: HTML `no-cache, must-revalidate`; hashed assets `public, max-age=31536000, immutable`.
- SSR HTML should paint meaningful content immediately — skeletons rendered by the server count toward FCP/SI, spinners added by JS do not.

## 7. Performance budgets (defaults; repo rules override)

Initial route, compressed: JS < 300KB, CSS < 100KB, above-fold images < 500KB, fonts < 100KB (subset), third-party < 200KB, total < 1.5MB. Treat a budget breach like a failing test: justify it or fix it. Enforce in CI when the repo has tooling (`quasar build` size report, bundle analyzer, Lighthouse CI budgets).

## 8. Verification

- `npx lighthouse <url> --output html` (mobile default) and `--preset desktop`; run 3 times, take the median — single runs vary several points.
- Test the production build (`quasar build` + serve), never the dev server.
- After any fix, re-run the same profile and attribute the delta to the metric you targeted; record before/after scores as evidence per `50-qa-and-verification.md`.
- Field regression watch: CrUX/PSI monthly on key routes, or `web-vitals` reporting if wired.

## Anti-patterns

- Optimizing FCP polish while TBT is 800ms (weight-blind effort).
- `loading="lazy"` on the LCP image; hero rendered client-side only.
- A "perf fix" that disables SSR, breaks the SW contract (`30-pwa-sw-and-offline.md`), or strips hydration the route needs.
- Chasing lab 100 while field INP fails — or trusting a single unthrottled desktop run.
- Adding a heavy third-party script "temporarily" with no budget accounting.

## Pairing guidance

- Bottleneck workflow, hydration cost, realtime jank: `40-performance-and-realtime.md`
- Quasar build config, code-splitting shape, SSR/SW specifics: `$alaa-quasar-app-vite-v3`
- Design-side costs (image/font/effect/motion choices, skeleton sizing): `$alaa-ui-ux-design-system`
- Evidence and release gating: `50-qa-and-verification.md`

## Useful official docs

- [Lighthouse performance scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring)
- [Lighthouse scoring source (audit p10/median values)](https://github.com/GoogleChrome/lighthouse/tree/main/core/audits/metrics)
- [web.dev Core Web Vitals](https://web.dev/articles/vitals) — LCP/INP/CLS guides and optimization series
- [Lighthouse 13 insights migration](https://developer.chrome.com/blog/lighthouse-13-0)
- [web-vitals library](https://github.com/GoogleChrome/web-vitals)
