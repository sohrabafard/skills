# Step-up challenges and permission hints in the client

You are about to render a TOTP step-up challenge, read a verification timestamp, or show or hide UI based on a permission bitmap. Three platform facts make a naively written Quasar frontend wrong. This file states only the frontend consequences.

Trust doctrine, header semantics, and proof issuance are `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`). The wire contract — error codes, endpoints, header names, and the exact response shape — is `/alaa-services-contract` (`$alaa-services-contract`), `references/32-auth-totp-and-step-up-contract.md` and `references/60-frontend-sdk-consumption-contract.md`. Token storage, refresh, and protected routes are `/alaa-frontend-developer` (`$alaa-frontend-developer`), `references/21-ssr-auth-and-session-patterns.md`. Read those for the names; read this for what the browser must and must not do with them.

## 1. The gateway is non-blocking for step-up, so the client never infers state

The gateway injects verified step-up metadata only when a proof is fully valid, and injects nothing when the proof is absent, expired, unbound, or wrongly signed. It returns no TOTP error and blocks no request in either case, because it holds no route-to-purpose map. **An absent proof and an invalid proof are therefore indistinguishable downstream, and the service denies the protected operation in both cases.**

Consequences, all unconditional:

- **Render the backend's denial; never predict it.** The client issues the request, receives the step-up error code, and shows the challenge. A client-side state machine that decides "this route needs step-up" will diverge from the service's policy the first time that policy changes, and it will be wrong in both directions — blocking an operation the service would have allowed, and allowing one it will deny.
- **Do not treat a successful request as proof that no step-up is required**, and do not cache "this route does not need step-up".
- **Preserve the original request intent across the challenge.** The user's action, its parameters, and its purpose survive the challenge and are replayed after the proof is obtained. Dropping the user back on the page with an empty form loses their work.
- **On a rate-limit response, stop retrying until the returned window expires.** Do not schedule a background retry that re-triggers the limiter.
- **On an unavailable response, fail closed** — show a controlled unavailable state and do not fall through to the unprotected path.

## 2. Two timestamps, two formats — a parser written against one reads the other wrong

The step-up response **body**'s `verified_until` is an **ISO 8601 string**. The `X-TOTP-VERIFIED-UNTIL` **header** carries the same instant as **Unix epoch seconds**, and it is backend-only metadata injected by the gateway for downstream services.

- **The browser parses the body's ISO 8601 value.** Feeding an ISO 8601 string into a numeric epoch parser yields `NaN`; feeding an epoch integer into a date parser yields 1970. Both failures present as "the proof expired immediately" and are diagnosed as a backend bug.
- **The browser never reads, synthesizes, or forwards `X-TOTP-VERIFIED-UNTIL`.** A client-supplied value in a backend-only header carries no trust and will be overwritten or rejected.
- **Cache the proof until the body's `verified_until` and no longer.** Re-challenge when it passes rather than retrying and reading the denial.

```ts
// Do: parse the body value as ISO 8601.
const verifiedUntil = new Date(response.verified_until).getTime()

// Don't: the header is epoch seconds and is backend-only.
const verifiedUntil = Number(headers.get('X-TOTP-VERIFIED-UNTIL')) * 1000
```

## 3. A permission bitmap is a UI hint, never an authorization decision

The decoded permission set drives what the UI *offers*. It never decides what the user may *do*.

- **Every action guarded by a decoded permission is also guarded server-side**, and the client renders the server's denial when the two disagree. Hiding a control is presentation; it is not access control.
- **An empty decoded set is a legitimate ready state**, not an error and not "still loading". Distinguish "decoded, empty" from "not yet fetched" explicitly; conflating them produces a UI that flickers every permission-gated control on every page load.
- **Use the canonical decoder; do not write one.** The bitmap contract and its canonical TypeScript decoder are `/alaa-permission-generator` (`$alaa-permission-generator`), `references/typescript-consumer.md` and `references/shared-consumer-contract.md`. A hand-written bit test in a Vue component drifts from the generated catalogue silently.
- **Identifiers the frontend encodes or decodes must match the fleet codec byte for byte.** The codec and its conformance harness are `/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`), `references/10-shared-codec-contract.md` and `scripts/codec-conformance.sh`. A frontend implementation that has not been run through that harness is unverified, whatever a comment in the file asserts.

## 4. Quasar wiring

- The challenge is a normal focus-taking flow: a `QDialog` containing a `QForm` with one `QInput`, exactly as in `references/40-webotp-and-device-trust.md` §3 — one field, `inputmode="numeric"`, `autocomplete="one-time-code"`, manual entry always enabled. Split-digit inputs break autofill on both paths.
- **The code the user typed is normalized to ASCII digits before it is sent.** The normalization form is `/alaa-input-normalization` (`$alaa-input-normalization`), `references/20-browser-binding.md`; the browser normalizes at submit and the backend normalizes in middleware, and the two must agree byte for byte. Do not write a local digit-folding helper.
- Retry the original request through the same SDK call that failed, so headers, deadlines, and correlation identifiers are identical; re-issuing it by hand loses them.
- The challenge dialog moves focus in and restores it out (`references/70-guardrails-a11y-performance-monorepo.md`), and its failure states follow `references/34-frontend-failure-and-degradation.md` §2.

✅ Do — issue the request, render the backend's denial, parse the body timestamp as ISO 8601, and treat the bitmap as presentation. ❌ Don't — build a client-side step-up state machine, read the backend-only header, or gate an action on the bitmap alone.

Search: `TOTP_STEP_UP_REQUIRED`, `TOTP_REQUIRED`, `TOTP_RATE_LIMITED`, `step-up`, `proof_token`, `verified_until`, `X-TOTP-VERIFIED-UNTIL`, `X-TOTP-Proof`, `permission bitmap`, `UI hint`, `challenge and retry`, `fail closed`.
