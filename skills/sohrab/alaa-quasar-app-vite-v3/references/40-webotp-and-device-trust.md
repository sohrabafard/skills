# WebOTP, SMS OTP autofill, and device trust

Scope: reading SMS OTP codes in the browser (login/verification flows) and using device signals safely for device trust. Written for Quasar app-vite v3 apps (SPA/SSR/PWA), Vue 3 Composition API. Research verified 2026-07-08 against MDN, web.dev, developer.chrome.com, Apple developer docs, WICG spec, and vendor primary sources. Refresh before trusting browser-support claims after that date.

Also load: `45-browser-apis-and-permissions.md` for the general permission model and priming UX; `50-modern-experience.md` for passkey-forward auth UX; `$alaa-vue-typescript-clean-code` for composable shape; `$alaa-trust-gateway-auth` when the auth backend contract is in scope; `$alaa-indexeddb-browser-storage` for storage classification rules.

## 1. The one SMS template that serves every mechanism

Chrome WebOTP and Safari domain-bound autofill deliberately share one format. Send OTP SMS as:

```text
<brand>: your login code is 123456.

@app.example.com #123456
```

- The last line is mandatory and exact: `@<domain> #<code>` — domain without scheme, port, or path.
- Human-readable lines above it are free text; include the word "code" so Safari's heuristic fallback also works.
- Cross-origin iframe variant (Chromium only): `@top-level.example.com #123456 @embedded.example.com`.

✅ Do — coordinate with the SMS-sending backend so the bound domain matches the exact origin serving the OTP page, and keep one template for all platforms.

❌ Don't — send unbound "Your code is 123456" SMS and expect autofill; Safari falls back to weak heuristics and origin-bound anti-phishing protection is lost.

## 2. Support reality (mid-2026) — design for the fallback chain

| Mechanism | Works on | Does not work on |
|---|---|---|
| WebOTP API (`OTPCredential`) | Chrome/Edge/Opera/Samsung on Android (Chrome 84+); Chrome desktop 93+ cross-device (needs same Google account + Android phone w/ Play services; opportunistic) | Safari (all), Firefox (all) — no implementation, no positive standards position |
| `autocomplete="one-time-code"` | iOS/iPadOS Safari keyboard suggestion; macOS Safari via iPhone Text Message Forwarding | Android Chrome does NOT read SMS from this attribute alone |
| Manual entry | Everywhere | — |

WebOTP is a WICG draft, not Baseline. Treat it as progressive enhancement forever, not a wait-for-support feature.

## 3. Production pattern (all three layers, one input)

Baseline markup — a real form, one single input (split per-digit inputs break both autofill paths):

```html
<q-form @submit="verify">
  <q-input
    v-model="code"
    type="text"
    inputmode="numeric"
    pattern="[0-9]*"
    autocomplete="one-time-code"
    :maxlength="CODE_LENGTH"
  />
</q-form>
```

WebOTP enhancement as an SSR-safe composable — call when the OTP input becomes visible (component mount / route enter), never at app boot:

```ts
// useWebOtp.ts — client-only; feature-detected; abortable
export function useWebOtp(onCode: (code: string) => void) {
  let ac: AbortController | undefined

  onMounted(() => {
    if (!('OTPCredential' in window)) return // Safari/Firefox: autocomplete covers them
    ac = new AbortController()
    // Abort when the code TTL expires; keep in sync with backend expiry.
    const timeout = setTimeout(() => ac?.abort(), 60_000)
    navigator.credentials
      .get({ otp: { transport: ['sms'] }, signal: ac.signal } as CredentialRequestOptions)
      .then((cred) => { if (cred) onCode((cred as { code: string }).code) })
      .catch(() => { /* AbortError (timeout, manual submit, route leave) is normal */ })
      .finally(() => clearTimeout(timeout))
  })
  onUnmounted(() => ac?.abort())

  // Call from the form's submit handler so a pending request never races manual entry.
  return { cancel: () => ac?.abort() }
}
```

Rules that make this production-grade:

- Issue `credentials.get()` BEFORE the SMS arrives (the browser buffers and matches); on resend, keep the existing pending request — one pending request per origin at a time.
- Abort on: manual submit, route leave/unmount, and a timeout aligned with the code TTL.
- Chrome shows a consent bottom-sheet; autofill is user-mediated. Auto-submit after fill only if your risk posture allows the user not to review the value.
- Never block or disable the input while waiting. Manual entry is a first-class path, not an error path.
- SSR: `OTPCredential`/`navigator.credentials` are browser-only. Feature-detect inside `onMounted`; never touch them in setup on the server path.
- Cross-origin iframe OTP (embedded login widget): requires `allow="otp-credentials"` on the iframe, the two-origin SMS line, and is Chromium-only with one nesting level. Prefer keeping the OTP step top-level.

✅ Do — layer it: `one-time-code` input everywhere → WebOTP where detected → manual always.

❌ Don't — gate the flow on WebOTP success, call `credentials.get()` on app startup, or build six single-digit boxes because they look nice; both autofill mechanisms fill one field.

Security honesty: origin binding suppresses autofill on phishing domains, but the user can still type a code into a phishing page. SMS OTP stays phishable and SIM-swappable. The 2026-correct posture is SMS OTP for first contact, then offer passkey enrollment (see section 5).

## 4. Device fingerprinting — bounded use only

Hard boundary first: a fingerprint is one weak, decaying risk signal. It is never an auth factor, never a sole gate, and never stored as if stable.

Why it decays (verified 2026 state): Safari ships Advanced Fingerprinting Protection (noise in Canvas/WebGL/Audio/geometry, extending beyond Private Browsing since Safari 26); Firefox 145+ randomizes canvas under its fingerprinting protection; UA strings are frozen/reduced in all engines (Safari 26 froze the iOS UA too; UA-Client-Hints are Chromium-only and server-opt-in). Raw client hashes drift by design.

Library posture: FingerprintJS OSS **v5 is MIT** (since Oct 2025) — usable commercially; avoid v4 (BSL 1.1, non-production only). BotD (MIT) is a first-pass bot filter, trivially bypassable, never a control. Commercial "Pro" tiers buy server-side signal fusion, not magic.

Privacy/legal floor: fingerprinting and assigned device IDs are terminal-equipment access under ePrivacy Art. 5(3) (EDPB Guidelines 2/2023 v2, Oct 2024) — consent is required unless strictly necessary for a service the user requested; fraud prevention may fit that exemption but needs a per-deployment legal decision. Disclose in the privacy policy, bound retention, support erasure/unlinking.

The architecture that actually works — assigned ID + weak signals + server-side decision:

1. On first successful auth, the server issues a random opaque device ID in a `Secure; HttpOnly; SameSite=Lax` first-party cookie (server-set cookies survive Safari ITP's 7-day cap on script-writable storage).
2. Mirror the ID in IndexedDB/localStorage only for clear-detection; a mismatch between cookie and mirror is itself a risk signal, never an identity source. Classify per `$alaa-indexeddb-browser-storage` rules (no tokens, no authority in browser storage).
3. Client sends raw-ish signals (fingerprint vector, BotD verdict) alongside the device ID; the server risk engine fuses them with IP/ASN velocity and history using fuzzy similarity, not hash equality.
4. Engine output picks the path: silent pass / OTP re-challenge / step-up (TOTP or passkey) / block. Rotate the device ID on credential change or suspected compromise.

✅ Do — treat "fingerprint changed" as "score lower", and let the server decide.

❌ Don't — compare fingerprint hashes for equality, store one in localStorage as the device identity, block login when it changes, or run fingerprinting without privacy-policy disclosure and a recorded legal basis.

## 5. The stronger primitives to prefer

- **Passkeys/WebAuthn** are the privacy-respecting device-trust primitive and are universally supported in 2026 (all engines; synced via iCloud Keychain / Google Password Manager; device-bound on security keys). Origin-bound signatures give phishing-resistant device binding — everything a fingerprint fakes, done correctly. Multi-domain brands can share passkeys via Related Origin Requests (`/.well-known/webauthn`). Note: a synced passkey proves credential possession, not a specific physical device; combine with the device-ID cookie when strict per-device trust matters.
- **Private Access Tokens / Privacy Pass** (Apple devices since iOS 16; consumed by Cloudflare/Fastly) attest "real human" without fingerprinting; use them at the edge where available before adding client bot-scoring.

Recommended flow for an OTP-first product: SMS OTP (sections 1–3) for first contact → passkey enrollment offer on success → passkey presence becomes the primary trusted-device signal → device-ID + fingerprint score remains only as fraud telemetry for passkey-less devices.
