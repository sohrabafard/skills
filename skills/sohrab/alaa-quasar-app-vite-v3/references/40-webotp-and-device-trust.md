# WebOTP, SMS autofill, and device trust

Scope: SMS OTP in Quasar app-vite v3 SPA/SSR/PWA (Vue 3 Composition API) and safe device signals. Verified 2026-07-08 against MDN, web.dev, developer.chrome.com, Apple docs, WICG, and vendor primary sources; refresh browser-support claims after that date. Also load `45-browser-apis-and-permissions.md`, `50-modern-experience.md`, `$alaa-vue-typescript-clean-code`, auth-backend `$alaa-trust-gateway-auth`, and storage `$alaa-indexeddb-browser-storage`.

## 1. One SMS format for Chrome and Safari

```text
<brand>: your login code is 123456.

@app.example.com #123456
```

- Final line is exact/mandatory: `@<domain> #<code>`; domain has no scheme, port, or path. The bound domain must equal the OTP page’s exact serving origin.
- Earlier lines are free text; include “code” for Safari heuristic fallback.
- Chromium-only cross-origin iframe: `@top-level.example.com #123456 @embedded.example.com`.

Never send only “Your code is 123456”: origin-bound anti-phishing autofill is lost and Safari falls back to weaker heuristics.

## 2. Support (mid-2026)

| Mechanism | Works | Does not |
|---|---|---|
| WebOTP (`OTPCredential`) | Chrome/Edge/Opera/Samsung Android (Chrome 84+); opportunistic Chrome desktop 93+ cross-device with same Google account + Android/Play Services | All Safari/Firefox; neither implements nor has positive standards position |
| `autocomplete="one-time-code"` | iOS/iPadOS Safari keyboard; macOS Safari via iPhone Text Message Forwarding | Android Chrome does not read SMS from this attribute alone |
| Manual | Everywhere | — |

WebOTP is a non-Baseline WICG draft: permanent progressive enhancement.

## 3. Production: one input, three layers

Use a real form and one field; split digits break both autofill paths:

```html
<q-form @submit="verify">
  <q-input v-model="code" type="text" inputmode="numeric" pattern="[0-9]*"
    autocomplete="one-time-code" :maxlength="CODE_LENGTH" />
</q-form>
```

Start this SSR-safe enhancement when the field appears (mount/route enter), never at app boot:

```ts
// useWebOtp.ts — client-only, detected, abortable
export function useWebOtp(onCode: (code: string) => void) {
  let ac: AbortController | undefined

  onMounted(() => {
    if (!('OTPCredential' in window)) return
    ac = new AbortController()
    const timeout = setTimeout(() => ac?.abort(), 60_000) // match backend TTL
    navigator.credentials
      .get({ otp: { transport: ['sms'] }, signal: ac.signal } as CredentialRequestOptions)
      .then((cred) => { if (cred) onCode((cred as { code: string }).code) })
      .catch(() => { /* AbortError from timeout/submit/leave is normal */ })
      .finally(() => clearTimeout(timeout))
  })
  onUnmounted(() => ac?.abort())
  return { cancel: () => ac?.abort() } // call from manual submit
}
```

- Call `credentials.get()` before SMS arrival. On resend keep the pending request; only one may be pending per origin.
- Abort on manual submit, unmount/route leave, and timeout aligned with OTP TTL.
- Chrome consent is user-mediated. Auto-submit only if risk policy permits no value review.
- Input/manual entry always stays enabled. Layer: `one-time-code` → detected WebOTP → manual.
- `OTPCredential`/`navigator.credentials` are browser-only; detect inside `onMounted`, never SSR setup.
- Cross-origin widget needs iframe `allow="otp-credentials"`, the two-origin SMS line, Chromium, and one nesting level; prefer top-level OTP.

Origin binding blocks phishing-domain autofill, not manual code entry. SMS remains phishable/SIM-swappable; use it for first contact, then offer passkeys (§5).

## 4. Fingerprinting: bounded signal only

A fingerprint is weak/decaying: never an auth factor, sole gate, or stable identity. Safari Advanced Fingerprinting Protection adds Canvas/WebGL/Audio/geometry noise (beyond Private Browsing since Safari 26); Firefox 145+ randomizes canvas under fingerprint protection; all engines reduce/freeze UA (Safari 26 froze iOS UA); UA-Client-Hints are Chromium-only/server-opt-in. Raw hashes intentionally drift.

Library facts: FingerprintJS OSS **v5 is MIT** since Oct 2025 and commercially usable; v4 is BSL 1.1/non-production-only. BotD (MIT) is a trivially bypassed first-pass bot filter, never a control. Commercial Pro tiers add server signal fusion, not certainty.

Privacy floor: fingerprinting/assigned device IDs are terminal-equipment access under ePrivacy Art. 5(3) (EDPB Guidelines 2/2023 v2, Oct 2024). Consent is required unless strictly necessary for the user-requested service; fraud prevention may qualify only after deployment-specific legal review. Disclose it, bound retention, and support erasure/unlinking.

Use assigned ID + weak signals + server decision:

1. After first successful auth, server sets a random opaque ID in `Secure; HttpOnly; SameSite=Lax` first-party cookie; server-set cookies avoid Safari ITP’s 7-day script-storage cap.
2. Mirror only to detect clearing in IndexedDB/localStorage; cookie/mirror mismatch is risk, never identity. Per `$alaa-indexeddb-browser-storage`: no token or browser authority.
3. Send raw-ish fingerprint vector/BotD verdict with ID; server fuses IP/ASN velocity/history using fuzzy similarity, never hash equality.
4. Server chooses silent pass / OTP re-challenge / TOTP or passkey step-up / block; rotate ID after credential changes or suspected compromise.

“Fingerprint changed” only lowers score. Never equality-gate, treat localStorage fingerprint as identity, block solely on change, or fingerprint without policy disclosure/recorded legal basis.

## 5. Prefer stronger primitives

- **Passkeys/WebAuthn** are universally supported in 2026 (all engines; iCloud Keychain/Google Password Manager sync; security keys device-bound). Origin-bound signatures provide phishing-resistant binding. Related Origin Requests (`/.well-known/webauthn`) support multi-domain brands. A synced passkey proves credential possession, not one physical device; pair with device-ID cookie if strict per-device trust is required.
- **Private Access Tokens / Privacy Pass** (Apple since iOS 16; consumed by Cloudflare/Fastly) attest “real human” without fingerprinting; use at the edge before client bot scoring.

Recommended: first-contact SMS OTP → passkey enrollment offer → passkey as primary trusted-device signal; device ID + fingerprint score only as fraud telemetry for passkey-less devices.
