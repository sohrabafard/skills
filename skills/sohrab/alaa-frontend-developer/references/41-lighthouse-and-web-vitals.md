# Lighthouse and Core Web Vitals

Use this file for any Lighthouse, PageSpeed Insights, Core Web Vitals, or "make it faster / hit 90+" task.
Target: performance score >= 90 on mobile, the harder profile, with 100 as the design goal on key routes.

**This file is the canonical copy for the fleet.** `/alaa-quasar-app-vite-v3`
(`$alaa-quasar-app-vite-v3`) and `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`) route here
instead of duplicating it. Re-verify the weights and audit IDs when a new major Lighthouse ships.

## 1. How the score is computed

Metric weights, unchanged across Lighthouse 10 through 13
([developer.chrome.com](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring),
read: 2026-07-28):

| Metric | Weight | Lab measures |
|---|---|---|
| Total Blocking Time (TBT) | 30% | main-thread long tasks (>50 ms) between FCP and TTI |
| Largest Contentful Paint (LCP) | 25% | when the largest above-fold element renders |
| Cumulative Layout Shift (CLS) | 25% | visual stability, impact × distance |
| First Contentful Paint (FCP) | 10% | first text or image paint |
| Speed Index (SI) | 10% | how quickly content visually completes |

Each metric maps to 0–100 through a log-normal curve anchored on HTTPArchive data: the good control point
scores 90, the median control point scores 50. Control points (ms except CLS) — read: unverified as of
2026-07-28; the scoring page documents the method but no longer publishes the table, so confirm against
`GoogleChrome/lighthouse/core/audits/metrics` before quoting a number to a stakeholder:

| Metric | Mobile 90 / 50 | Desktop 90 / 50 |
|---|---|---|
| FCP | 1800 / 3000 | 934 / 1600 |
| SI | 3387 / 5800 | 1311 / 2300 |
| LCP | 2500 / 4000 | 1200 / 2400 |
| TBT | 200 / 600 | 150 / 350 |
| CLS | 0.10 / 0.25 | 0.10 / 0.25 |

Consequences:

- TBT + LCP + CLS is 80% of the score. Attack in that order unless the trace says otherwise; FCP and SI
  usually improve alongside LCP fixes.
- The curve is nonlinear: LCP 4000 → 2500 ms buys far more than 1200 → 900 ms. Once a metric is
  comfortably past its 90-point value, move to the next-weighted one.
- Bands are 0–49 / 50–89 / 90–100. Mobile runs on simulated throttling, slow 4G and 4× CPU; a fast dev
  machine proves nothing.
- Lighthouse 13 replaced the legacy opportunity audits with DevTools-aligned insight audits
  (`cls-culprits-insight`, `image-delivery-insight`, `render-blocking-insight`). Scoring is unchanged;
  anything parsing Lighthouse JSON tracks the new audit IDs. 13.x is still the current major line
  (`GoogleChrome/lighthouse` releases, read: 2026-07-28) — there is no Lighthouse 14.

## 2. Lab and field are two scoreboards

Lighthouse is lab data. Search uses field data: CrUX at the 75th percentile — LCP ≤ 2.5 s, INP ≤ 200 ms,
CLS ≤ 0.1 ([web.dev/articles/vitals](https://web.dev/articles/vitals), read: 2026-07-28; all three are at
the stable lifecycle stage, which caps threshold changes at once per year). INP exists only in the field;
TBT is its lab proxy. Collect field data with `web-vitals` (`onLCP`/`onINP`/`onCLS`, and the
`web-vitals/attribution` build to name culprits), reported through `47-frontend-observability.md`. When
lab and field disagree, field wins.

## 3. TBT and INP (30% plus the field metric)

- Ship less JavaScript. Route-level code splitting is baseline; charts, editors and players go behind
  `defineAsyncComponent`.
- **Lazy hydration, Vue 3.5+, SSR only** ([vuejs.org async components](https://vuejs.org/guide/components/async.html),
  read: 2026-07-28). The strategies are `hydrateOnIdle()`, `hydrateOnVisible()`, `hydrateOnMediaQuery()`
  and `hydrateOnInteraction()`, passed as `hydrate` to `defineAsyncComponent`. Below-fold and
  interaction-optional islands defer; the route's primary interactive element never does.
- Break long tasks (>50 ms) and yield between chunks. `scheduler.yield()` is **not Baseline — limited
  availability** ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Scheduler/yield), read:
  2026-07-28), so it is used behind a capability check with `setTimeout(0)` as the fallback, knowing the
  fallback loses scheduler priority.
- INP anatomy: input delay (<50 ms) + processing (<100 ms) + presentation (<50 ms). Apply the visual
  feedback synchronously, yield, then run the heavy work; push analytics to `requestIdleCallback`.
- Third-party scripts are the classic TBT killer: `async`/`defer`, lazy-load on visibility, facade pattern
  for video, chat and map embeds, and delete stale tags.
- Vue cost: `shallowRef` for large structures, no broad deep watchers, `v-memo` on hot list rows.

## 4. Complexity and size thresholds

Doctrine — how to state a bound and find the input that grows — is `/alaa-algorithms-data-structures`
(`$alaa-algorithms-data-structures`) `references/10-complexity-budget.md`. The frontend numbers:

| Condition | Requirement |
|---|---|
| a list whose length is not a constant, or exceeds ~100 rendered rows | virtualize (`QVirtualScroll` or equivalent); rendering every row is a defect once the row count follows data |
| total DOM nodes on a route above ~1,500 | reduce before optimizing anything else; node count inflates every phase of INP |
| a per-row computation inside a render or a `computed` over the list | must be O(1) per row; a nested scan over the same list is O(n²) and shows up as jank at the third screen of data |
| a client-side sort, filter or group over data that grows | precompute once per data change, not once per render |
| one request per row | prohibited; batch — `45-api-and-data-shaping.md` |

The design-side expression of the same limits — how many items a screen should show at all — is
`/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`) `references/65-lists-latency-and-concurrency.md`.

## 5. LCP (25%)

Decompose first: TTFB → resource load delay → resource load duration → element render delay.

- TTFB < 800 ms: SSR render time, edge or CDN caching of HTML where personalization allows, Brotli,
  HTTP/2+.
- **The LCP element must be in the server HTML.** A client-only hero moves LCP past hydration and caps the
  score.
- Load delay: `fetchpriority="high"`, eager loading, never `loading="lazy"` on the LCP image;
  `<link rel="preload">` when it is discovered late; `preconnect` to its origin. HTTP 103 Early Hints is
  worth considering on a slow origin, but it is effectively HTTP/2-and-later only and browser support is
  partial ([MDN 103](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/103), read:
  2026-07-28; per-browser matrix unverified as of 2026-07-28).
- Load duration: AVIF or WebP, correctly sized `srcset`/`sizes`, an image CDN.
- Render delay: minimal critical CSS, no render-blocking third-party CSS or JS in `<head>`,
  `font-display: swap`.
- Next navigation: Speculation Rules prerender or prefetch, `eagerness` one of `immediate`, `eager`,
  `moderate`, `conservative` — start at `moderate`
  ([developer.chrome.com/docs/web-platform/prerender-pages](https://developer.chrome.com/docs/web-platform/prerender-pages),
  read: 2026-07-28). The API is **not Baseline — limited availability**: Chrome and Edge 109+, Safari
  behind a flag, Firefox unsupported, so it is a progressive enhancement and never a correctness
  dependency. Gate side-effectful code on `document.prerendering` and `prerenderingchange`. Keep bfcache
  eligibility: no `unload` listener, no `Cache-Control: no-store` on HTML.

## 6. CLS (25% — usually the cheapest points)

Every image, video, embed and ad slot declares dimensions or `aspect-ratio`; async content gets
fixed-size skeleton space. Fonts get a metric-matched fallback via `size-adjust`, `ascent-override` and
`descent-override`, or `font-display: optional` for a non-brand face. Animate `transform` and `opacity`
only. Inject dynamic content below the viewport or into reserved space. Debug with the `layout-shift`
PerformanceObserver (`entry.sources`) or `cls-culprits-insight`.

## 7. FCP and Speed Index (2 × 10%)

Defer non-critical CSS, no `@import` chains, lean total CSS. HTML `no-cache, must-revalidate`; hashed
assets `public, max-age=31536000, immutable`. SSR HTML paints meaningful content immediately —
server-rendered skeletons count toward FCP and SI; a spinner added by JavaScript does not.

## 8. Budgets

Defaults for an initial route, compressed: JS < 300 KB, CSS < 100 KB, above-fold images < 500 KB, fonts <
100 KB subset, third-party < 200 KB, total < 1.5 MB. Repo rules override the numbers.

Gate 8 in `SKILL.md` governs a breach; the exception it requires is recorded in the repo's budget config,
beside the number it overrides. Whether a budget is required at all, and
at what level, is `/alaa-observability-soc` (`$alaa-observability-soc`)
`references/30-quantitative-budgets.md` and `/alaa-project-constitution`
(`$alaa-project-constitution`) `references/quality-bar.md`. Enforcement in CI is `/alaa-frontend-devops`
(`$alaa-frontend-devops`) `references/20-ci-gates-and-predicates.md`. The design-side asset budget is
`/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`) `references/45-render-and-asset-budgets.md`.

## 9. Verification

`npx lighthouse <url> --output html` on the mobile default and `--preset desktop`; three runs, take the
median. Test the production build, never the dev server. After a fix, re-run the same profile and
attribute the delta. Record before and after per `50-qa-and-verification.md`. Field watch: CrUX or PSI on
key routes, or `web-vitals` reporting where it is wired.

## Anti-patterns

Polishing FCP while TBT is 800 ms. `loading="lazy"` on the LCP image. A hero rendered client-side only. A
"perf fix" that disables SSR, widens the service-worker cache, or strips hydration the route needs.
Chasing a lab 100 while field INP fails. Adding a heavy third-party script "temporarily" with no budget
entry.

## Pairing

Bottleneck workflow and realtime jank: `40-performance-and-realtime.md`. Quasar build config and
code-splitting shape: `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`). Image, font, effect and
motion cost: `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`). Evidence and release gating:
`50-qa-and-verification.md`.
