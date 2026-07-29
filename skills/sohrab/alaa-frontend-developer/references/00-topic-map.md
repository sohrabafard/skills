# Topic map — the only router in this skill

`SKILL.md` is always loaded and carries the gates. This file carries the routing. Every row names a
situation you can observe **before** you act — something visible in the diff, the request, or the failure
in front of you. If you cannot tell whether a row matches by looking at what is on screen, the row is
broken and fixing it comes before using it.

One file answers most tasks and two is normal. Loading every row means the task was never scoped.

| You are about to | Read |
|---|---|
| claim a change is tested, choose between a component test, an SSR render test and an end-to-end test, or write an assertion for a hydration mismatch | `05-proof-and-tests.md` |
| decide what the app family guarantees — build output, package consumption, workflow order, which auth boundary applies — or you are unsure whether a rule here is a constraint or a suggestion | `10-contract-and-boundaries.md` |
| add or edit a `.vue` or `.ts` file that renders on the server, write `onMounted`, a `watch`, an `AbortController`, or a `v-for` key, or clean up a listener, timer, socket or observer | `20-vue-js-ssr-patterns.md` |
| touch a login, logout, refresh, silent-refresh, protected-route or SSR request that carries identity, or decide where the access token lives | `21-ssr-auth-and-session-patterns.md` |
| add or edit a text field, a submit handler, a validator, a formatter, or an input mask; or a value typed in Persian digits failed a length, uniqueness or validation rule | `22-input-validation-and-normalization.md` |
| write `v-html`, render a URL, a filename or free text that a user or a third party supplied, read a permission in a component or a guard, open a `postMessage` listener, or put a value in the client bundle | `25-frontend-security.md` |
| edit a service worker, a caching route, an offline page, an update prompt, or the manifest; or an update reloads forever, a chunk 404s after deploy, or the offline page never appears | `30-pwa-sw-and-offline.md` |
| profile a slow route, chase a memory leak after navigation, or open, close, or reconnect a WebSocket or SSE stream | `40-performance-and-realtime.md` |
| run Lighthouse or PageSpeed, read a score, chase LCP, INP, CLS or TBT, decide whether a list must be virtualized, or set or breach a bundle budget | `41-lighthouse-and-web-vitals.md` |
| change what a screen asks the API for — envelope, filter, sort, page, sparse fields, cache validator — or a "frontend" slowness is really query shape, count cost, or a request per row | `45-api-and-data-shaping.md` |
| add a `fetch` or a mutation, write a retry, decide what a screen shows when a dependency is down, slow, partial, or offline | `46-resilience-and-degradation.md` |
| add or delete a client-side event, an error report, a Web Vitals field report, or a request header that carries trace context | `47-frontend-observability.md` |
| add, rename or read a `VITE_*` variable or any other injected value, add a feature flag, or set a public or base path | `48-config-and-environment.md` |
| decide which checks to run before calling a change done, write a manual verification plan, or write the release note for what shipped | `50-qa-and-verification.md` |
| format a date, a number, a currency or a relative time that renders during SSR, or set a locale or timezone anywhere in the render path | `55-i18n-locale-and-rtl.md` |
| open a browser to look at a bug, collect console, network or DOM evidence, or implement a design that needs measurement before hydration | `60-browser-debug.md` |
| find two companion skills that both look right, or choose between a headless and a headed browser profile | `70-companion-skill-routing.md` |
| assert a version, a "latest" or "current" fact, cite a source, or update this skill | `95-sources-and-maintenance.md` |

## Rows that are not optional when they match

- `22-input-validation-and-normalization.md` and `25-frontend-security.md` govern surfaces with no safe
  default — an unbounded input, untrusted content in a template, a permission read in the client. A
  component that decides one of them locally is wrong even when it happens to be safe today.
- `05-proof-and-tests.md` fires on the word "done", not on the decision to write a test.

## Good first searches

`hydration mismatch`, `onMounted`, `AbortController`, `deep watch`, `BFF`, `token-mediating backend`,
`silent refresh`, `localStorage`, `single-flight refresh`, `network-only`, `offline fallback`,
`controllerchange`, `SKIP_WAITING`, `WebSocket reconnect`, `backpressure`, `LCP`, `INP`, `TBT`, `CLS`,
`lighthouse`, `fetchpriority`, `bfcache`, `speculation rules`, `scheduler.yield`, `lazy hydration`,
`performance budget`, `virtualization threshold`, `cursor pagination`, `ETag`, `If-None-Match`,
`problem details`, `sparse fields`, `N+1`, `idempotency key`, `traceparent`, `VITE_`, `maxlength`,
`normalization`, `v-html`, `CSP`, `postMessage`, `Intl`, `timezone`, `release note`.

## Retired names — where that content is now

Old skill names `alaa-frontend`, `javascript-pro`, `vue-expert`, `qa-expert`, `verify-runbook`,
`performance-engineer`, `websocket-engineer`, `pwa-service-worker-maintainer`, `ssr-auth-guard`,
`api-designer`, `database-optimizer`, and old shared docs `REPO_CONTRACT.md`, `PACKAGES_GUIDE.md`,
`VUE_SSR_PATTERNS.md`, `PWA_SW_CONTRACT.md`, `PWA_RUNBOOK.md` all resolve inside the table above:
contract to `10-`, Vue and JavaScript to `20-`, auth to `21-`, service worker to `30-`, performance and
realtime to `40-` and `41-`, API and query shape to `45-`, QA and runbooks to `50-`, browser evidence to
`60-`. Do not try to resurrect a deleted local skill.

Design terms — `view transitions`, `container queries`, `oklch`, `light-dark`, `prefers-reduced-motion`,
`@starting-style`, tokens, styles, icons, RTL layout, Persian typography — belong to
`/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`) `references/00-topic-map.md`.
