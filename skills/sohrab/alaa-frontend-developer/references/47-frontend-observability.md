# Frontend Observability

Names and levels are not decided here.

- Event names, log fields, metric names, error codes and the envelope they travel in:
  `/alaa-services-contract` (`$alaa-services-contract`)
  `references/20-operational-and-observability-contract.md` and `references/24-metric-registry.md`.
- Whether a signal is required, at what level, with what retention and what alert:
  `/alaa-observability-soc` (`$alaa-observability-soc`) `references/10-signal-model.md`,
  `references/20-instrumentation-gates.md`, `references/40-alerting-slo-retention.md`.
- The Quasar-side emission surface: `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`)
  `references/36-client-observability-contract.md`.
- The Vue-shaped wiring — `app.config.errorHandler`, `onErrorCaptured`, an HTTP interceptor:
  `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`)
  `references/74-observability-binding.md`.

This file states what a browser client is obliged to emit, and the three ways browsers make that hard.

## The four required client signals

| Signal | Emitted when |
|---|---|
| unhandled error and unhandled rejection | `window.onerror`, `unhandledrejection`, and every component error boundary — an error caught and shown to the user is still reported |
| Web Vitals field data | `onLCP`, `onINP`, `onCLS` from the `web-vitals` library on real sessions, with the attribution build where the culprit matters — see `41-lighthouse-and-web-vitals.md` |
| request outcome | one event per request class carrying status, duration and outcome, including aborted and deadline-fired outcomes from `46-resilience-and-degradation.md` |
| connection state | connect, disconnect and reconnect for every WebSocket or SSE stream — `40-performance-and-realtime.md` |

Deleting one of these is a change to the observability contract, not a cleanup. A `console.log` is not one
of them and does not ship.

## Trace context to the gateway

A browser-initiated request that crosses into the platform propagates trace context in the `traceparent`
header so the client span joins the server trace. Three rules:

1. **Propagate only to your own origins.** Sending `traceparent` to a third-party origin leaks internal
   identifiers and trips CORS preflight; the allowlist is explicit.
2. **Adding the header makes the request preflighted.** A cross-origin call that was simple becomes an
   `OPTIONS` round trip, so the server must permit the header or every call fails. Verify this before
   enabling propagation, not after.
3. **The browser is not the trust anchor.** A trace id from the browser is correlation, never identity or
   authorization — `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`)
   `references/20-claims-headers-and-sentinels.md`.

## What must never be in a client event

A token, a password, a national id, a full phone number, a presigned URL, a message payload, or free-text
the user typed. A client event is shipped over the public internet to a collector and stored; treat every
field as published. What counts as sensitive is `/alaa-security-review` (`$alaa-security-review`)
`references/50-credentials-and-cryptography.md`.

## Sampling and volume

Errors are not sampled. Web Vitals and request-outcome events are sampled at the rate the observability
skill sets. A per-render or per-keystroke event is a volume incident: aggregate in the client and emit
once per interaction, and never emit inside a `watch` that fires on every reactive change.

## Diagnosability of the UI itself

A screen a user cannot describe is a screen operations cannot debug: a stable, visible correlation id on
an error state turns a support ticket into a trace lookup. Its placement and wording are
`/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`) `references/28-ui-diagnosability.md`; the id
itself comes from the response envelope defined by `/alaa-services-contract`
(`$alaa-services-contract`).

## Verification

An observability change is proven by an emitted event observed at the collector, not by reading the code
that emits it. Capture the event as evidence per `50-qa-and-verification.md`.
