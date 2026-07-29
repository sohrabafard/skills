# WebOTP, SMS autofill, and device signals

You are about to build the SMS-OTP screen, wire `autocomplete="one-time-code"`, or add a device signal to an authentication flow. Scope: Quasar app-vite v3 SPA/SSR/PWA with the Vue 3 Composition API. Verified 2026-07-08 against MDN, web.dev, developer.chrome.com, Apple documentation, WICG, and vendor primary sources; refresh browser-support claims per `references/80-upstream-deltas-and-live-checks.md` §6.

Also load `references/45-browser-apis-and-permissions.md` (permission model), `references/41-step-up-and-permission-hints.md` (what the client does with a challenge and a proof), and `references/50-modern-experience.md` (where OTP sits in the wider flow).

**Boundary.** This file states what the browser does. Token issuance, cookie policy, server-side signal fusion, and the decision to challenge, step up, or block are `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`). Token storage, refresh, and protected routes are `/alaa-frontend-developer` (`$alaa-frontend-developer`), `references/21-ssr-auth-and-session-patterns.md`. Vue and TypeScript shape is `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`).

## 1. One SMS format that satisfies both Chrome and Safari

```text
<brand>: your login code is 123456.

@app.example.com #123456
```

- The final line is exact and mandatory: `@<domain> #<code>`; the domain carries no scheme, port, or path, and must equal the OTP page's exact serving origin.
- Earlier lines are free text. Include the word "code" so Safari's heuristic fallback fires.
- Chromium-only cross-origin iframe form: `@top-level.example.com #123456 @embedded.example.com`.

Never send only "Your code is 123456": origin-bound anti-phishing autofill is lost and Safari falls back to weaker heuristics.

## 2. Support (mid-2026)

| Mechanism | Works | Does not |
|---|---|---|
| WebOTP (`OTPCredential`) | Chrome/Edge/Opera/Samsung on Android (Chrome 84+); opportunistically Chrome desktop 93+ cross-device with the same Google account plus Android and Play Services | every Safari and Firefox build; neither implements it nor holds a positive standards position |
| `autocomplete="one-time-code"` | iOS/iPadOS Safari keyboard; macOS Safari through iPhone Text Message Forwarding | Android Chrome does not read SMS from this attribute alone |
| Manual entry | everywhere | — |

WebOTP is a non-Baseline WICG draft. Treat it as permanent progressive enhancement.

## 3. Production shape: one input, three layers

Use a real form with one field. Split-digit inputs break both autofill paths.

```html
<q-form @submit="verify">
  <q-input v-model="code" type="text" inputmode="numeric" pattern="[0-9]*"
    autocomplete="one-time-code" :maxlength="CODE_LENGTH" />
</q-form>
```

Start this SSR-safe enhancement when the field appears — on mount or route enter — never at app boot:

```ts
// useWebOtp.ts - client-only, feature-detected, abortable
export function useWebOtp(onCode: (code: string) => void) {
  let ac: AbortController | undefined

  onMounted(() => {
    if (!('OTPCredential' in window)) return
    ac = new AbortController()
    const timeout = setTimeout(() => ac?.abort(), 60_000) // match the backend TTL
    navigator.credentials
      .get({ otp: { transport: ['sms'] }, signal: ac.signal } as CredentialRequestOptions)
      .then((cred) => { if (cred) onCode((cred as { code: string }).code) })
      .catch(() => { /* AbortError from timeout, submit, or leave is normal */ })
      .finally(() => clearTimeout(timeout))
  })
  onUnmounted(() => ac?.abort())
  return { cancel: () => ac?.abort() } // call from manual submit
}
```

- Call `credentials.get()` before the SMS arrives. On resend, keep the pending request; only one may be pending per origin.
- Abort on manual submit, on unmount or route leave, and on a timeout aligned with the OTP TTL.
- **Do not auto-submit a WebOTP-filled code.** Fill the field, leave the submit control to the user, and keep manual entry enabled. Chrome's consent is user-mediated and the user is entitled to see the value before it is spent.
- The layering order is `one-time-code` -> feature-detected WebOTP -> manual entry, and manual entry is never disabled.
- **The code is normalized to ASCII digits before submit.** A user pasting or typing non-ASCII digits must not produce a request the backend rejects. The normalization form is `/alaa-input-normalization` (`$alaa-input-normalization`), `references/20-browser-binding.md`; the same rule covers the phone-number field. Do not write a local digit-folding helper.
- `OTPCredential` and `navigator.credentials` are browser-only. Feature-detect inside `onMounted`, never in SSR `setup()`.
- A cross-origin widget needs iframe `allow="otp-credentials"`, the two-origin SMS line, Chromium, and exactly one nesting level. Prefer a top-level OTP page.
- Field errors, retry limits, and the resend affordance follow `references/34-frontend-failure-and-degradation.md` §2 — an OTP screen with a spinner and no error branch strands the user.

Origin binding blocks autofill on a phishing domain; it does not block a user from typing the code into one. SMS remains phishable and SIM-swappable: use it for first contact, then offer passkeys (§5).

## 4. Device signals: bounded, and never an authority

A browser fingerprint is weak and decaying. It is never an authentication factor, never a sole gate, and never a stable identity.

Platform reality: Safari's Advanced Fingerprinting Protection adds Canvas, WebGL, Audio, and geometry noise beyond Private Browsing since Safari 26; Firefox 145+ randomizes canvas under fingerprint protection; every engine reduces or freezes the user agent, and Safari 26 froze the iOS UA string; UA Client Hints are Chromium-only and server-opt-in. Raw hashes are meant to drift.

Library facts: FingerprintJS OSS v5 is MIT since October 2025 and commercially usable; v4 is BSL 1.1 and non-production. BotD (MIT) is a trivially bypassed first-pass filter, never a control.

Privacy floor: fingerprinting and assigned device identifiers are terminal-equipment access under ePrivacy Article 5(3) (EDPB Guidelines 2/2023 v2, October 2024). Consent is required unless the processing is strictly necessary for the service the user requested; a fraud-prevention basis requires deployment-specific legal review. Disclose it, bound its retention, and support erasure. This is a constraint on what the browser may collect, not a legal opinion; the deployment's basis is recorded outside this skill.

**What the browser does**, and nothing more:

1. Read the opaque device identifier the server set, and mirror it into browser storage **only to detect clearing**. A mismatch between the cookie and the mirror is a risk signal, never an identity. The mirror carries no token and no authority — `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`), `references/61-authority-boundary.md`.
2. Send the raw-ish signal vector and the bot verdict alongside the identifier, and let the server decide.
3. Render the server's decision. Never equality-gate on a fingerprint, never treat a stored fingerprint as identity, never block solely because a signal changed, and never collect a signal without a disclosed policy.

**Cookie attributes, identifier rotation, signal fusion, and the choice between silent pass, re-challenge, step-up, and block are the gateway's** — `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`). Storage lifetime limits that make a script-set mirror unreliable, including the Safari script-storage cap, are `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`), `references/32-eviction-and-recovery.md`. What the client does when the server answers with a step-up challenge is `references/41-step-up-and-permission-hints.md`.

## 5. Prefer stronger primitives

- **Passkeys / WebAuthn** are supported in every engine in 2026, sync through iCloud Keychain and Google Password Manager, and are device-bound on security keys. Origin-bound signatures give phishing-resistant binding, and Related Origin Requests (`/.well-known/webauthn`) cover multi-domain brands. A synced passkey proves credential possession, not one physical device; pair it with the server's device identifier when strict per-device trust is required.
- **Private Access Tokens / Privacy Pass** (Apple since iOS 16; consumed by Cloudflare and Fastly) attest a real human without fingerprinting. Use them at the edge, before any client-side bot scoring.

Recommended order: first-contact SMS OTP -> passkey enrollment offer -> passkey as the primary trusted-device signal, with the device identifier and signal score kept as fraud telemetry for passkey-less devices only.

Search: `OTPCredential`, `one-time-code`, `otp-credentials`, `@domain #code`, `WebOTP`, `credentials.get`, `AbortController`, `passkey`, `WebAuthn`, `Related Origin Requests`, `Private Access Tokens`, `FingerprintJS`, `BotD`, `device identifier mirror`.
