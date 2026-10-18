# Frontend Observability

Names and levels are not decided here.

- Event names, log fields, metric names, error codes and the envelope they travel in:
  `/alaa-services-contract`
  `references/20-operational-and-observability-contract.md` and `references/24-metric-registry.md`.
- Whether a signal is required, at what level, with what retention and what alert:
  `/alaa-observability-soc` `references/10-signal-model.md`,
  `references/20-instrumentation-gates.md`, `references/40-alerting-slo-retention.md`.
- The Quasar-side emission surface: `/alaa-quasar-app-vite-v3`
  `references/36-client-observability-contract.md`.
- The Vue-shaped wiring — `app.config.errorHandler`, `onErrorCaptured`, an HTTP interceptor:
  `/alaa-vue-typescript-clean-code`
  `references/74-observability-binding.md`.

This file owns browser transport and correlation constraints. Before adding or removing a browser signal,
apply `alaa-observability-soc references/20-instrumentation-gates.md` under Browser client signals for the
conditional requirements. Quasar reference 36 above owns emission wiring; do not recreate its allowlist here.

## Trace context to the gateway

A browser-initiated request that crosses into the platform propagates trace context in the `traceparent`
header so the client span joins the server trace. Three rules:

1. **Propagate only to your own origins.** Sending `traceparent` to a third-party origin leaks internal
   identifiers and trips CORS preflight; the allowlist is explicit.
2. **Adding the header makes the request preflighted.** A cross-origin call that was simple becomes an
   `OPTIONS` round trip, so the server must permit the header or every call fails. Verify this before
   enabling propagation, not after.
3. **The browser is not the trust anchor.** A trace id from the browser is correlation, never identity or
   authorization — `/alaa-trust-gateway-auth`
   `references/20-claims-headers-and-sentinels.md`.

## What must never be in a client event

A token, a password, a national id, a full phone number, a presigned URL, a message payload, or free-text
the user typed. A client event is shipped over the public internet to a collector and stored; treat every
field as published. What counts as sensitive is `/alaa-security-review`
`references/50-credentials-and-cryptography.md`.

## Sampling and volume

Resolve sampling and volume budgets through the observability owner above. If the target's required rate
is unregistered, report the gap instead of inventing a rate. A per-render or per-keystroke event is a
volume incident: aggregate in the client and emit
once per interaction, and never emit inside a `watch` that fires on every reactive change.

## Diagnosability of the UI itself

A screen a user cannot describe is a screen operations cannot debug: a stable, visible correlation id on
an error state turns a support ticket into a trace lookup. Its placement and wording are
`/alaa-ui-ux-design-system` `references/28-ui-diagnosability.md`; the id
itself comes from the response envelope defined by `/alaa-services-contract`.

## Verification

An observability change is proven by an emitted event observed at the collector, not by reading the code
that emits it. Capture the event as evidence per `50-qa-and-verification.md`.
