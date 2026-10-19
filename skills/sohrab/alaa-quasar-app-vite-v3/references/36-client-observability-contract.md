# Client observability contract

Read when sending browser telemetry or initializing Sentry for Quasar SPA or SSR. This file owns emission
wiring, transport, scrubbing and collector-failure behavior; the owners below decide required classes,
names and rates.

**This file names nothing.** Every event name, field name, metric name, attribute key, and envelope key comes from `/alaa-services-contract`, `references/20-operational-and-observability-contract.md` and `references/24-metric-registry.md`; the frontend consumption shape is `references/60-frontend-sdk-consumption-contract.md`. Every requirement level — what is mandatory, what is sampled, what is prohibited, and the quantitative budgets — comes from `/alaa-observability-soc`, `references/20-instrumentation-gates.md`, `references/30-quantitative-budgets.md`, `references/60-sentry-and-profiling.md`. **Request a name from those skills; never invent one and never abbreviate one.** If the name you need does not exist there, that is a contract gap to raise, not a naming decision to make in the browser.

Web Vitals *scoring* and Lighthouse interpretation are `/alaa-frontend-developer`, `references/41-lighthouse-and-web-vitals.md`. That is measurement; this file is production emission.

## 1. Applicable browser signals

Before adding or removing a signal, apply `alaa-observability-soc references/20-instrumentation-gates.md`
under Browser client signals. It owns the conditional requirement classes; this file owns their Quasar
wiring. Use the services registries above for payload names. A missing approved name is a contract gap,
not permission to invent one or silently omit an applicable signal.

For each applicable class, preserve its emission seam and safe diagnostic content; the registry owns
the wire spellings:

| Seam | Diagnostic content after scrubbing |
|---|---|
| Browser/Vue error capture and component boundaries | Error type, safe message, stack, route name, release and available correlation identifier; report a caught user-visible failure once |
| Finalized `web-vitals` callbacks (`onLCP`, `onINP`, `onCLS`) | Registered metric, value, navigation type and route name; use attribution when needed to identify the culprit |
| HTTP facade/interceptor | Bounded request class, status, duration and outcome, including abort and deadline |
| WS/SSE lifecycle | Connect, disconnect and reconnect transition |
| Window-side registration hooks | Transition, worker build identifier and previous state |
| Accepted update without expected takeover, or a precached asset 404 after activation | Failed transition and worker build identifier |

**A user action is not an observability event.** Product analytics is a separate pipeline with a separate consent basis; do not mix it into the error or vitals transport.

## 2. Transport

- **`navigator.sendBeacon()` is the default for anything emitted during page unload or visibility change** — the final vitals flush, the last lifecycle transition. It survives document teardown, it cannot be aborted, it returns only whether the payload was queued, and its payload is size-limited by the browser. Never use it for anything whose failure you must observe.
- **`fetch(url, { keepalive: true })` is used when a response is needed** or when a header the beacon cannot set is required. `keepalive` has its own body-size ceiling; a payload over it fails silently, so batch below the ceiling rather than sending one large envelope.
- **A plain `fetch` without `keepalive` is used only while the document is visible**, and it carries a deadline like every other request (`references/34-frontend-failure-and-degradation.md` §2).
- **Emission never blocks a user interaction.** Send after the interaction has been committed; never `await` an emission inside an event handler on the path to a UI update.
- **Emit from the window, not from the service worker,** unless the event is about the service worker itself. A service worker that emits application telemetry duplicates events across tabs and outlives the session that produced them.

## 3. Sampling, and what never leaves the browser

- Apply the Browser client signals owner above for which classes permit sampling; resolve other rates
  through `alaa-observability-soc references/30-quantitative-budgets.md` and approved target policy.
  Missing required rates remain a contract gap; do not invent one.
- A web-vitals sample is emitted at most once per metric per page view; send the browser's final value.
- **The following never leave the browser in any emission:** any value from `localStorage`, `sessionStorage`, IndexedDB, or Cache Storage; cookie contents; `Authorization` header values or any token; form field values, including a field the user has not submitted; the query string of any URL — send the route pattern, not the resolved URL with its parameters; free-text the user typed; any national identifier, phone number, or email address. When an error message may contain a user value, send the error type and the stack and drop the message rather than sending it unscrubbed.
- **The route identifier is the router's route name or path pattern, never `window.location.href`.** A resolved URL carries identifiers in its path and query.
- **Scrub before the transport, not at the collector.** A scrubbing function that runs in the sender is the only one that guarantees the value never crossed the network; the live `client` does this in `src/observability/sentryEventScrub.ts`.

## 4. When the collector is unreachable

- **Emission is fail-open in every direction.** A collector that is down, slow, blocked by an ad blocker, or returning `5xx` never produces a visible error, never retries into a loop, and never prevents the app from rendering. Wrap every emission so a throw inside it cannot escape.
- **Do not queue telemetry into the offline outbox.** The outbox is for user-owned mutations (`/alaa-indexeddb-browser-storage`, `references/71-browser-outbox.md`). Telemetry that failed to send is dropped; a day-old vitals sample has no value and a growing telemetry queue competes for the same quota as the user's drafts.
- **Stop after repeated failure.** Use an approved bounded application policy under the Browser client
  signals owner above for the consecutive-failure limit; if absent, report that configuration gap.
  At the limit, stop emitting for the session and record that locally, avoiding an attempt per event.
- **The server half of the seam is not this file.** An SSR render failure emits from the SSR process (`references/34-frontend-failure-and-degradation.md` §1) and reaches the collector server-side; the browser does not re-report a failure it received as an HTTP status.

## 5. Wiring in a Quasar app

- Register browser error handlers in a **boot entry `{ path: '<client-boot>', server: false }`**. Setting
  `client: true` alone does not exclude SSR. Pass the boot callback's Vue `app` to the browser integration;
  the installed-line shape is `references/22-cli-cookbook-and-examples.md`.
- Read the release identifier from a build-time define (`build.define`, `references/20-v3-config-and-features.md`), not from a runtime fetch; an error emitted before the runtime config arrives would otherwise be unattributed.
- The service-worker build identifier is the same value recorded in `references/37-pwa-operations-record.md`; a lifecycle event that cannot be tied to a build cannot be used.
- Lifecycle events are emitted from the window using the `register-sw` hooks or the `workbox-window` events described in `references/30-service-worker-excellence.md` §4 — not from inside `custom-sw`.

### Sentry for SPA and SSR

Before choosing an SDK, inspect the target lockfile, installed packages, Node runtime, SSR server framework
and module format. Use the pinned `@sentry/vue` browser API; choose the matching Node/server integration
for SSR, not the browser SDK. No fleet package version or browser env-key default is registered here:
`alaa-services-contract references/21-alaa-platform-observability-directive.md` owns that authority split.

- **SPA/browser side:** initialize `@sentry/vue` from the client boot above before mount, using its `app`
  option. Route classified failures through the existing single reporting facade; do not add another
  global handler that reports the same exception. HTTP outcomes belong at the HTTP facade/interceptor;
  connection transitions at the WS/SSE lifecycle owner. A library's automatic capture does not prove
  every applicable signal is wired.
- **DSN/config:** read the approved public browser DSN, release and environment through the target's typed
  config module. A browser DSN allows event submission and can be abused; it is not a read/admin secret.
  Never let browser initialization fall back to server `SENTRY_DSN`, and never expose an auth/upload token.
  Runtime config must resolve before initialization; release identity remains available at build time.
- **SSR side:** initialize the selected server SDK at the version's documented startup point, before the
  modules it must instrument. Wire its integration to the actual SSR server framework and isolate scope
  per request; never keep user context in a shared mutable singleton. Do not copy a preload flag across
  SDK majors. Capture a render failure on the server through the existing platform exception path;
  do not report it again as a browser exception merely because HTTP returned an error.
- **Privacy:** apply `alaa-observability-soc references/60-sentry-and-profiling.md` configuration gates.
  Read the pinned SDK options before configuring collection: v11 replaces `sendDefaultPii` with
  `dataCollection` and changes defaults. A bare `sendDefaultPii: false` is no universal solution.
  Scrub error events with `beforeSend`; inspect the separate hooks and defaults of every enabled
  breadcrumb, span, log or replay path. Do not enable Pinia state capture or optional integrations by
  copying the upstream quickstart. Error-event scrubbing proves no coverage of those other paths.
- **Release proof:** source maps and their upload token follow
  `alaa-frontend-devops references/25-artifact-identity-and-provenance.md`; tokens stay in CI secrets.
  Run the controlled non-production arrival, redaction, attribution and disabled-Sentry platform-path
  checks required by the observability owner. A source-only skill edit proves no SDK installation,
  live emission, collector arrival or SSR isolation.

Official sources, read: 2026-10-18: [Vue setup](https://docs.sentry.io/platforms/javascript/guides/vue/)
([official source](https://github.com/getsentry/sentry-docs/blob/master/docs/platforms/javascript/guides/vue/index.mdx)),
[Quasar boot scoping](https://quasar.dev/quasar-cli-vite/boot-files/),
[Node SDK](https://docs.sentry.io/platforms/javascript/guides/node/),
and [JavaScript v11 migration](https://github.com/getsentry/sentry-javascript/blob/develop/MIGRATION.md).
These sources explain selection; recheck version-matched docs in the target before copying options.

Do: wire each applicable class, scrub before transport and contain emission failure.
Do not send resolved URLs, loop on a failed collector, or invent a missing registry name.

Search: `sendBeacon`, `fetch keepalive`, `onunhandledrejection`, `errorHandler`, `web-vitals`, `LCP`, `INP`, `CLS`, `sampling rate`, `PII exclusion`, `scrub`, `collector unreachable`, `release identifier`, `service worker lifecycle event`.
