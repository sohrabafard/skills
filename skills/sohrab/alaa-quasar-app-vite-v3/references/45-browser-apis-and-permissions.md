# Browser device APIs and the permission model

Scope: using device/browser APIs (audio recording, camera, geolocation, notifications, clipboard, wake lock, sensors, and the rest) in production Quasar apps — and mastering the permission model across browsers, versions, and devices, including the priming UI you can customize and the browser prompt you cannot. Verified 2026-07-08 against MDN, developer.chrome.com, web.dev, webkit.org, Apple docs, caniuse, and Playwright docs. Browser prompt behavior changes fast — re-verify claims after that date.

Also load: `40-webotp-and-device-trust.md` (OTP/credential APIs), `30-service-worker-excellence.md` (push/badging/background sync), `31-ssr-pwa-and-security.md` (SSR guards); route structured storage to `$alaa-indexeddb-browser-storage` and Vue code shape to `$alaa-vue-typescript-clean-code`.

## 1. The permission model (learn this before any API)

- **`navigator.permissions.query({ name })`** returns `granted | denied | prompt` plus a `change` event. Always wrap in `try/catch` — unsupported names reject with `TypeError`, and older Safari/WebViews lack `navigator.permissions` entirely. Engine coverage differs: Chromium queries almost everything; Firefox added `camera`/`microphone` only in Fx 132 and cannot query `push` or `clipboard-*`; Safari queries `camera`/`microphone` (16+), `geolocation`, `notifications`/`push` on modern versions, but not `clipboard-*`.
- **Permissions-Policy** gates powerful features per origin and per iframe: cross-origin iframes get nothing unless the embedder grants `allow="camera; microphone; geolocation"` — and the prompt attributes to the top-level origin. Hard-disable surfaces that must never prompt with header syntax like `Permissions-Policy: camera=()`.
- **Secure context is mandatory** (HTTPS or localhost). A LAN-IP dev server over plain HTTP silently lacks `navigator.mediaDevices`, `Notification`, etc.
- **Transient activation (a real user gesture) is required** for: `Notification.requestPermission()` (Firefox 72+, Safari always), `getDisplayMedia()`, `navigator.share()`, clipboard read (Safari/Firefox), fullscreen, pointer lock, `showOpenFilePicker()`, Bluetooth/USB/Serial/HID/NFC choosers, and iOS `DeviceMotionEvent.requestPermission()`. `getUserMedia` doesn't formally require it, but requesting outside a gesture is an anti-pattern browsers punish.
- **`granted` is a cache, not a state.** Auto-expiry is now the norm: Chrome offers one-time grants ("Allow this time") and Safety Check auto-revokes permissions from sites unused ~60 days; Firefox 115+ defaults geolocation/camera/mic to one-time grants; Safari re-prompts camera/mic per session by design (especially iOS). Every flow must survive re-prompting.
- Denial semantics: Chrome `denied` is sticky until the user edits site settings; Firefox dismiss-without-remember re-asks, deny-with-remember sticks; Chrome's quieter UI collapses notification prompts for sites with bad acceptance rates and embargoes repeated dismissals.

✅ Do — treat the flow as: query (if supported) → primer UI → request inside the gesture → handle all three outcomes → expect to do it again next session.

❌ Don't — request any permission on page load, or cache `granted` in storage and assume it holds next visit; both patterns are now actively punished by browsers.

## 2. Per-API production notes

All of these are browser-only: in SSR, touch them solely inside `onMounted`/client-only code behind capability checks (`'wakeLock' in navigator`), and keep permission state in a client-initialized store.

### Microphone / audio recording (the exam-recording path)

- Stack: `getUserMedia({ audio })` → `MediaRecorder` (probe `MediaRecorder.isTypeSupported()` in order `['audio/webm;codecs=opus', 'audio/mp4', 'audio/ogg;codecs=opus']`, record with the first hit, store the actual `recorder.mimeType`). Verified codec reality: Chrome/Firefox record webm/opus; Safari records `audio/mp4` (AAC) and supports `audio/webm;codecs=opus` **since Safari 18.4** — so webm/opus is finally cross-browser, but the backend must still accept `audio/mp4` for older iOS.
- `enumerateDevices()` labels stay empty until a grant is active; never persist Safari `deviceId`s as stable identifiers.
- iOS Safari hard rules: `AudioContext` starts suspended — `resume()` inside a gesture; calls/Siri/app-switching can end tracks silently — listen to `track.onended`/`mute` and offer re-record on a fresh gesture; backgrounding/screen lock stops capture — pair with Wake Lock and warn the user; there is **no background recording on the web**. Test the installed (standalone) PWA case separately — its permission scope and bugs differ from Safari tabs.
- Fallbacks: AudioWorklet + WASM encoder when MediaRecorder is missing/insufficient; `<input type="file" accept="audio/*" capture>` for ancient WebViews.

### Camera and screen capture

- `getUserMedia({ video: { facingMode: 'user' | 'environment' } })`; iOS preview `<video>` needs `playsinline`.
- `getDisplayMedia()` is desktop-only (no iOS Safari through 26.x, no Android). Every call shows the picker — no persistence. Region/Element Capture are Chromium-only. Mobile screen share → Capacitor/native only.

### Geolocation

- Always pass a finite `timeout` (default is infinite). Error contract: code 1 `PERMISSION_DENIED` → recovery UI; code 2 `POSITION_UNAVAILABLE` → transient, retry with backoff + `maximumAge` cached fix; code 3 `TIMEOUT` → retry/degrade. `watchPosition` can emit errors then recover — don't tear down on the first one.
- iOS has a **Precise Location toggle**: with it off you get ~1–5 km accuracy regardless of `enableHighAccuracy`, plus a two-layer OS→Safari→site permission chain. Background geolocation is impossible on the web.
- Fallbacks: server-side IP geolocation for coarse defaults, manual city picker.

### Notifications and push

- Request only from a click (Firefox/Safari require the gesture; Chrome punishes without it). iOS: push requires iOS 16.4+ AND Home-Screen install — detect `matchMedia('(display-mode: standalone)')` and show an add-to-home-screen primer instead of a doomed request. Notification actions/images are Chromium-only persistent-notification features. Full push/badging/Declarative Web Push depth: `30-service-worker-excellence.md`.

### Clipboard

- `writeText` works everywhere with a gesture. Silent `read` exists only in Chromium (permission prompt); Firefox 127+ shows a contextual "Paste" confirmation, Safari an inline Paste button. Never design a flow that needs silent clipboard read cross-browser.

### Capability table (feature-detect every row)

| API | Reality (mid-2026) |
|---|---|
| Wake Lock `navigator.wakeLock.request('screen')` | Baseline all engines (Chrome 84+/Safari 16.4+/Firefox 126+); no prompt; auto-released on tab hide — re-acquire on `visibilitychange`. Essential during exams/recording. |
| Fullscreen | All desktop + Android; **iPhone Safari: video elements only** — never build exam lockdown on fullscreen for iPhone. |
| Screen Orientation `lock()` | Chromium/Firefox Android; not iOS Safari — CSS fallback. |
| Vibration | Android only; sticky activation; pure enhancement. |
| Web Share `share()` | Safari + Chromium + Firefox (Windows/Android); gesture required; clipboard/link fallback. |
| File pickers `showOpenFilePicker` etc. | Chromium desktop only; fallback `<input type="file">` + anchor download. |
| OPFS `navigator.storage.getDirectory()` | Universal, no prompt — right place for large local blobs; pair with `persist()`. |
| `navigator.storage.persist()` | Firefox: real prompt; Chrome/Safari: silent heuristics (engagement/installed/push-granted). Call after real engagement; check `persisted()`. Safari's 7-day ITP eviction still applies to non-persistent storage — sync exam drafts to the server. |
| Bluetooth / USB / HID / Serial / NFC | Chromium-only (NFC: Chrome Android only); chooser UI is the permission; gesture required. iOS path = Capacitor native. |
| Web MIDI | Chromium prompts for ALL access since ~124 (not just sysex); Safari absent. |
| Speech Recognition | Chromium (server-based default; on-device via `processLocally: true` + `SpeechRecognition.available()/install()` since Chrome 139 — check `fa-IR` pack availability at runtime); Safari webkit-prefixed; Firefox not shipped. Own-ASR fallback for critical flows. |
| Speech Synthesis | Universal, no prompt; iOS first `speak()` needs a gesture; voices load async (`voiceschanged`); Persian voices OS-dependent. |
| Motion/Orientation | iOS 13+: `DeviceMotionEvent.requestPermission()` from a gesture (guard `typeof ... === 'function'`); Chromium: policy-gated, no prompt. |
| Idle Detection / Battery / Generic Sensors | Chromium-only; Mozilla/WebKit negative — never a cross-browser dependency. |

## 3. Permission UX — customizing what you actually own

The browser prompt cannot be styled, rephrased, or repositioned. The customizable layer is the **priming (soft-ask) UI before it** and the **recovery UI after denial**:

1. **Two-step ask**: user taps the feature ("ضبط پاسخ" / Start recording) → in-app primer states what, why, and scope ("microphone, only while recording, uploaded only on submit") with Continue / Not now → only on Continue call the API, still inside the gesture chain. This protects your one pre-denial shot and keeps acceptance rates high — which Chrome's quieter UI literally scores you on.
2. **Query before prompting** where supported: `granted` → skip the primer; `denied` → skip the doomed prompt and render recovery instead.
3. **Recovery UI**: there is no web API or deep link to browser site settings. Detect the browser and show only the matching recipe (Chrome: lock icon → Site settings; Firefox: lock icon → Clear permissions; Safari macOS: Settings for This Website; Safari iOS: `aA` → Website Settings, plus the OS layer under Settings → Apps → Safari). Use RTL-safe screenshots for the Persian UI.
4. **Chromium permission elements**: the generic `<permission>` element (PEPC) did not ship from its origin trial; Chrome pivoted to capability-specific elements — the **`<geolocation>` element ships around Chrome 144** and can re-surface a confirmation even from the `denied` state (real recovery, ~54% success in Chrome's case study). Adopt behind feature detection with the normal JS flow as fallback; styling is deliberately browser-constrained; Firefox/Safari have no support or commitment.
5. **Copy rules**: the browser prompt renders in the browser's UI language, which may differ from the page — write "your browser will now ask…" instead of quoting button labels; keep your primer button visually distinct from browser chrome; state revocability.

✅ Do — measure your own funnel (primer shown → accepted → API called → state after) by diffing `permissions.query`/`Notification.permission` before and after.

❌ Don't — use prompt walls, re-prompt loops after dismissal, or "you must allow notifications to continue" copy; Chrome auto-revokes and embargoes exactly these patterns, and they poison your origin's prompt reputation.

## 4. Testing and debugging

- Playwright: `context.grantPermissions([...])` (camera, microphone, geolocation, notifications, clipboard-read/write, screen-wake-lock, storage-access, local-network-access, ...) + `setGeolocation()` + `clearPermissions()` — effectively Chromium-first; WebKit/Firefox honor a subset.
- Deterministic media tests: Chromium flags `--use-fake-device-for-media-stream` (+ `--use-file-for-fake-audio-capture=answer.wav`) and `--use-fake-ui-for-media-stream`; Firefox pref `media.navigator.streams.fake`.
- DevTools: Sensors panel overrides geolocation (including "Location unavailable" to simulate error code 2) and orientation; per-site reset via the lock icon. Use permission.site to demo cross-browser prompt differences to QA.
- Not automatable — keep a manual device matrix: one-time grants, quieter UI, Safari per-session re-prompts, iPhone Safari vs iPhone installed-PWA permission scopes, Android WebView.

## 5. Capacitor / hybrid split (do not mix the models)

In Capacitor builds the web permission model is replaced by the native one: plugins expose `checkPermissions()/requestPermissions()`, prompts are OS dialogs driven by `Info.plist` usage strings (missing `NSMicrophoneUsageDescription` crashes iOS at request time) and AndroidManifest entries; push is APNs/FCM via plugin (no service worker, no VAPID, no Home-Screen constraint); Android WebView denies `getUserMedia` unless the host implements `onPermissionRequest`; and unlike the web, native CAN deep-link to the app's settings screen for denial recovery.

Architecture rule: put permissions behind a `PermissionService` port with `web` and `capacitor` adapters selected via `Capacitor.isNativePlatform()` — the priming UI is shared, the request/recovery layer is per-platform. Never promise background recording/geolocation in shared code; it exists only natively.

## 6. 2025–2026 changes worth knowing

- **Local Network Access prompt** (Chrome 141+, Sep 2025): calls to private IPs/localhost from public sites now prompt — affects on-prem/school deployments and dev tooling.
- Web MIDI always prompts in Chromium now; on-device speech recognition arrived (Chrome 139+); `<geolocation>` element (Chrome ~144) is the first shipping permission element.
- Cross-site iframes needing their own cookies/storage must use the Storage Access API (`document.requestStorageAccess()`, queryable as `storage-access`) — relevant when the app is embedded on partner domains.
- iOS remains the binding constraint: still no `getDisplayMedia`, file pickers, Bluetooth/USB/NFC on iOS Safari through 26.x — Capacitor is the escape hatch.
