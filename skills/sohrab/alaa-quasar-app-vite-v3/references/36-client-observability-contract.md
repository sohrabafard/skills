# Client observability contract

You are about to send something from the browser to a collector: an unhandled error, a web-vitals sample, a service-worker lifecycle transition, or a failed-update event. This file states what a Quasar frontend may emit, over which transport, at what rate, with what excluded, and how it behaves when the collector is unreachable.

**This file names nothing.** Every event name, field name, metric name, attribute key, and envelope key comes from `/alaa-services-contract` (`$alaa-services-contract`), `references/20-operational-and-observability-contract.md` and `references/24-metric-registry.md`; the frontend consumption shape is `references/60-frontend-sdk-consumption-contract.md`. Every requirement level — what is mandatory, what is sampled, what is prohibited, and the quantitative budgets — comes from `/alaa-observability-soc` (`$alaa-observability-soc`), `references/20-instrumentation-gates.md`, `references/30-quantitative-budgets.md`, `references/60-sentry-and-profiling.md`. **Request a name from those skills; never invent one and never abbreviate one.** If the name you need does not exist there, that is a contract gap to raise, not a naming decision to make in the browser.

Web Vitals *scoring* and Lighthouse interpretation are `/alaa-frontend-developer` (`$alaa-frontend-developer`), `references/41-lighthouse-and-web-vitals.md`. That is measurement; this file is production emission.

## 1. What a Quasar frontend may emit

Exactly four classes. Anything outside them needs an entry in the services contract before it is sent.

| Class | Emitted when | Carries |
| --- | --- | --- |
| Unhandled error | `window.onerror` and `window.onunhandledrejection` fire, and on a Vue `app.config.errorHandler` call | the error type, the message, the stack, the route name, the release identifier, the correlation id if one exists |
| Web-vitals sample | the browser reports a finalized LCP, INP, or CLS value for the document | the metric name from the registry, the value, the navigation type, the route name |
| Service-worker lifecycle transition | a registration reaches `installed`, `waiting`, `activated`, or `redundant`, and when `controllerchange` fires | the transition, the service-worker build identifier, the previous state |
| Failed update | the update prompt was accepted and the reload did not result in a new controller, or a precached asset returned 404 after activation | the transition that failed, the service-worker build identifier |

**A user action is not an observability event.** Product analytics is a separate pipeline with a separate consent basis; do not mix it into the error or vitals transport.

## 2. Transport

- **`navigator.sendBeacon()` is the default for anything emitted during page unload or visibility change** — the final vitals flush, the last lifecycle transition. It survives document teardown, it cannot be aborted, it returns only whether the payload was queued, and its payload is size-limited by the browser. Never use it for anything whose failure you must observe.
- **`fetch(url, { keepalive: true })` is used when a response is needed** or when a header the beacon cannot set is required. `keepalive` has its own body-size ceiling; a payload over it fails silently, so batch below the ceiling rather than sending one large envelope.
- **A plain `fetch` without `keepalive` is used only while the document is visible**, and it carries a deadline like every other request (`references/34-frontend-failure-and-degradation.md` §2).
- **Emission never blocks a user interaction.** Send after the interaction has been committed; never `await` an emission inside an event handler on the path to a UI update.
- **Emit from the window, not from the service worker,** unless the event is about the service worker itself. A service worker that emits application telemetry duplicates events across tabs and outlives the session that produced them.

## 3. Sampling, and what never leaves the browser

- **Unhandled errors are emitted at the rate set by `/alaa-observability-soc` (`$alaa-observability-soc`)**, `references/30-quantitative-budgets.md`. Apply the sample decision once per session and reuse it, so a single session's errors are either all present or all absent; per-event sampling produces unreconstructable traces.
- **Web-vitals samples are emitted at the rate set in the same file.** A vitals sample is emitted at most once per metric per page view; the browser's own final value is the one to send.
- **Service-worker lifecycle transitions are not sampled.** They are low-volume and each one explains a class of user report.
- **The following never leave the browser in any emission:** any value from `localStorage`, `sessionStorage`, IndexedDB, or Cache Storage; cookie contents; `Authorization` header values or any token; form field values, including a field the user has not submitted; the query string of any URL — send the route pattern, not the resolved URL with its parameters; free-text the user typed; any national identifier, phone number, or email address. When an error message may contain a user value, send the error type and the stack and drop the message rather than sending it unscrubbed.
- **The route identifier is the router's route name or path pattern, never `window.location.href`.** A resolved URL carries identifiers in its path and query.
- **Scrub before the transport, not at the collector.** A scrubbing function that runs in the sender is the only one that guarantees the value never crossed the network; the live `client` does this in `src/observability/sentryEventScrub.ts`.

## 4. When the collector is unreachable

- **Emission is fail-open in every direction.** A collector that is down, slow, blocked by an ad blocker, or returning `5xx` never produces a visible error, never retries into a loop, and never prevents the app from rendering. Wrap every emission so a throw inside it cannot escape.
- **Do not queue telemetry into the offline outbox.** The outbox is for user-owned mutations (`/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`), `references/71-browser-outbox.md`). Telemetry that failed to send is dropped; a day-old vitals sample has no value and a growing telemetry queue competes for the same quota as the user's drafts.
- **Stop after repeated failure.** After the consecutive-failure count set by `/alaa-observability-soc` (`$alaa-observability-soc`), stop emitting for the rest of the session and record that fact locally, so a blocked collector costs one attempt per session rather than one per event.
- **The server half of the seam is not this file.** An SSR render failure emits from the SSR process (`references/34-frontend-failure-and-degradation.md` §1) and reaches the collector server-side; the browser does not re-report a failure it received as an HTTP status.

## 5. Wiring in a Quasar app

- Register the error handlers in a **boot file scoped `{ client: true }`**, so no handler is installed in the SSR process where `window` does not exist. The boot shape is `references/22-cli-cookbook-and-examples.md`.
- Read the release identifier from a build-time define (`build.define`, `references/20-v3-config-and-features.md`), not from a runtime fetch; an error emitted before the runtime config arrives would otherwise be unattributed.
- The service-worker build identifier is the same value recorded in `references/37-pwa-operations-record.md`; a lifecycle event that cannot be tied to a build cannot be used.
- Lifecycle events are emitted from the window using the `register-sw` hooks or the `workbox-window` events described in `references/30-service-worker-excellence.md` §4 — not from inside `custom-sw`.

✅ Do — emit the four named classes, scrub in the sender, and let every failure to emit pass silently. ❌ Don't — send `window.location.href`, retry a failed emission, or invent a field name because the registry does not have one yet.

Search: `sendBeacon`, `fetch keepalive`, `onunhandledrejection`, `errorHandler`, `web-vitals`, `LCP`, `INP`, `CLS`, `sampling rate`, `PII exclusion`, `scrub`, `collector unreachable`, `release identifier`, `service worker lifecycle event`.
