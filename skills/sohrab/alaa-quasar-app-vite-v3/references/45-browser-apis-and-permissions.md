# Browser device APIs and permissions

Scope: production Quasar use of recording, camera, geolocation, notifications, clipboard, wake lock, sensors, and other device APIs; cross-browser permissions and customizable priming UX. Verified 2026-07-08 against MDN, developer.chrome.com, web.dev, webkit.org, Apple docs, caniuse, and Playwright; re-verify fast-changing prompt behavior. Also load `40-webotp-and-device-trust.md`, `30-service-worker-excellence.md`, `31-ssr-pwa-and-security.md`; route storage to `$alaa-indexeddb-browser-storage`, Vue shape to `$alaa-vue-typescript-clean-code`.

## 1. Permission model

`navigator.permissions.query({ name })` yields `granted | denied | prompt` and `change`. Always `try/catch`: unknown names reject `TypeError`; old Safari/WebViews lack the API. Query coverage: Chromium nearly all; Firefox gained camera/mic in 132 but not push/`clipboard-*`; Safari supports camera/mic (16+), geolocation, and modern notifications/push, not `clipboard-*`. Permissions-Policy gates origin/iframe access: cross-origin frames require e.g. `allow="camera; microphone; geolocation"`; prompts name the top-level origin. Disable forbidden surfaces with `Permissions-Policy: camera=()`. Powerful APIs require HTTPS or localhost; plain-HTTP LAN-IP dev can silently lack `navigator.mediaDevices`, `Notification`, etc.

Real transient activation is required for `Notification.requestPermission()` (Firefox 72+, always Safari), `getDisplayMedia()`, `navigator.share()`, clipboard read (Safari/Firefox), fullscreen, pointer lock, `showOpenFilePicker()`, Bluetooth/USB/Serial/HID/NFC choosers, and iOS `DeviceMotionEvent.requestPermission()`. `getUserMedia()` does not formally require it, but out-of-gesture requests are punished/anti-patterns. `granted` is cached history, not durable state: Chrome one-time grants + Safety Check revocation after ~60 unused days; Firefox 115+ defaults geo/camera/mic to one-time; Safari intentionally re-prompts camera/mic each session, especially iOS. Denial differs: Chrome deny is sticky until site settings; Firefox dismiss-without-remember re-asks but remembered deny sticks; Chrome quieter notifications collapse low-acceptance prompts and embargo repeated dismissals.

Flow: query when supported → primer → request within gesture → handle all outcomes → expect future re-prompt. Never request on load or persist `granted` as next-session truth.

## 2. Per-API rules

Every API below is browser-only: under SSR use only client/onMounted code with capability checks such as `'wakeLock' in navigator`; initialize permission state client-side.

### Microphone/recording

`getUserMedia({ audio })` → `MediaRecorder`; probe `MediaRecorder.isTypeSupported()` in this order: `['audio/webm;codecs=opus', 'audio/mp4', 'audio/ogg;codecs=opus']`; record first match and retain `recorder.mimeType`. Chrome/Firefox use webm/opus; Safari uses AAC `audio/mp4` and supports webm/opus since Safari 18.4. Backend must still accept `audio/mp4` for older iOS. `enumerateDevices()` labels are blank before an active grant; Safari `deviceId` is not stable.

iOS: `AudioContext` starts suspended, so `resume()` inside a gesture. Calls/Siri/app switches may silently end tracks: listen to `track.onended`/`mute` and offer fresh-gesture re-record. Background/screen lock stops capture; use Wake Lock + warning. Web background recording does not exist. Test standalone PWA separately because permission scope/bugs differ from Safari tabs. If MediaRecorder is missing/insufficient, use AudioWorklet + WASM encoder; for ancient WebViews, `<input type="file" accept="audio/*" capture>`.

### Camera, geolocation, notifications, clipboard

**Camera/display:** `getUserMedia({ video: { facingMode: 'user' | 'environment' } })`; iOS preview `<video>` needs `playsinline`. `getDisplayMedia()` is desktop-only: absent on iOS Safari through 26.x and Android; every call reopens picker. Region/Element Capture are Chromium-only. Mobile screen sharing requires Capacitor/native. **Geolocation:** set finite `timeout` (default infinite). Error 1 `PERMISSION_DENIED`: recovery UI; 2 `POSITION_UNAVAILABLE`: transient retry with backoff + `maximumAge`; 3 `TIMEOUT`: retry/degrade. `watchPosition` can error then recover—do not stop at first error. iOS Precise Location off yields ~1–5 km accuracy despite `enableHighAccuracy`; permission chain is OS → Safari → site. Background web geolocation is impossible; fallback to server IP for coarse defaults + manual city picker. **Notifications/push:** request from click only; Firefox/Safari require it and Chrome punishes violations. iOS push requires iOS 16.4+ and Home-Screen install; detect `matchMedia('(display-mode: standalone)')` and show install primer before requesting. Notification actions/images are Chromium-only persistent features; see `30-service-worker-excellence.md` for push/badging/Declarative Web Push. **Clipboard:** gesture-based `writeText` is universal. Silent `read` is Chromium-only with permission prompt; Firefox 127+ shows contextual Paste confirmation, Safari an inline Paste button. Never depend on cross-browser silent read.

### Capability table—detect every row

| API | Mid-2026 reality |
|---|---|
| Wake Lock `navigator.wakeLock.request('screen')` | Baseline: Chrome 84+/Safari 16.4+/Firefox 126+; no prompt; tab-hide auto-release, so reacquire on `visibilitychange`; essential for exams/recording |
| Fullscreen | Desktop + Android; **iPhone Safari only video elements**—no iPhone exam lockdown |
| Screen Orientation `lock()` | Chromium/Firefox Android; no iOS Safari; CSS fallback |
| Vibration | Android-only, sticky activation; enhancement only |
| Web Share `share()` | Safari + Chromium + Firefox Windows/Android; gesture; clipboard/link fallback |
| `showOpenFilePicker` etc. | Chromium desktop only; `<input type="file">` + download anchor fallback |
| OPFS `navigator.storage.getDirectory()` | Universal/no prompt; large local blobs; pair with `persist()` |
| `navigator.storage.persist()` | Firefox prompts; Chrome/Safari silently use engagement/install/push heuristics. Call after real engagement; check `persisted()`. Safari 7-day ITP eviction still affects non-persistent storage; sync exam drafts server-side |
| Bluetooth/USB/HID/Serial/NFC | Chromium-only; NFC Chrome Android only; chooser is gesture-required permission; iOS requires Capacitor |
| Web MIDI | Chromium prompts for all access since ~124, not only sysex; Safari absent |
| Speech Recognition | Chromium server-default; Chrome 139+ supports local `processLocally: true` + `SpeechRecognition.available()/install()`—runtime-check `fa-IR`; Safari webkit-prefixed; Firefox unshipped; own-ASR fallback for critical flows |
| Speech Synthesis | Universal/no prompt; first iOS `speak()` needs gesture; voices async via `voiceschanged`; Persian voices depend on OS |
| Motion/Orientation | iOS 13+ requires gesture `DeviceMotionEvent.requestPermission()` (guard `typeof ... === 'function'`); Chromium policy-gated/no prompt |
| Idle Detection/Battery/Generic Sensors | Chromium-only; Mozilla/WebKit negative; never cross-browser core |

## 3. UX: what is customizable

Browser prompts cannot be styled, reworded, or moved. Own the pre-prompt primer and post-denial recovery:

1. Two-step ask: feature tap (e.g. “ضبط پاسخ” / Start recording) → primer states what/why/scope (“microphone, only while recording, uploaded only on submit”) with Continue/Not now → API only on Continue in the gesture chain. This preserves the pre-denial chance and Chrome prompt reputation.
2. Query first where possible: `granted` skips primer; `denied` skips doomed prompt and shows recovery.
3. No web API/deep link opens site settings. Show browser-specific instructions only: Chrome lock → Site settings; Firefox lock → Clear permissions; Safari macOS Settings for This Website; Safari iOS `aA` → Website Settings plus Settings → Apps → Safari. Persian UI screenshots must be RTL-safe.
4. Generic `<permission>` PEPC never shipped after origin trial. Chrome pivoted to capability elements: `<geolocation>` ships around Chrome 144 and can reconfirm from `denied` (~54% recovery in Chrome’s case study). Feature-detect; retain JS fallback; browser intentionally restricts styling; Firefox/Safari have no support/commitment.
5. Browser prompt language may differ from page; say “your browser will now ask…” rather than quote buttons. Keep primer visually distinct from browser chrome and state revocability.

Measure primer shown → accepted → API called → post-state by diffing `permissions.query`/`Notification.permission`. Never use prompt walls, dismissal loops, or “allow notifications to continue”; Chrome embargo/auto-revocation punishes them and harms origin reputation.

## 4. Test/debug

Playwright: `context.grantPermissions([...])` (camera, microphone, geolocation, notifications, clipboard-read/write, screen-wake-lock, storage-access, local-network-access, ...), `setGeolocation()`, `clearPermissions()`; effectively Chromium-first, subset in WebKit/Firefox. Deterministic media: Chromium `--use-fake-device-for-media-stream`, optional `--use-file-for-fake-audio-capture=answer.wav`, and `--use-fake-ui-for-media-stream`; Firefox `media.navigator.streams.fake`.

DevTools Sensors overrides geolocation (including “Location unavailable”/error 2) and orientation; reset via lock icon. permission.site demonstrates cross-browser prompts. Manual matrix: one-time grants, quiet UI, Safari per-session prompts, iPhone tab vs installed-PWA scopes, Android WebView.

## 5. Capacitor/native split

Native replaces web permissions: plugins use `checkPermissions()/requestPermissions()`; OS dialogs use `Info.plist` strings (missing `NSMicrophoneUsageDescription` crashes iOS on request) and AndroidManifest. Push uses APNs/FCM plugin—no SW/VAPID/Home-Screen rule. Android WebView denies `getUserMedia` unless host implements `onPermissionRequest`. Native can deep-link to app settings after denial.

Put a `PermissionService` port behind `web`/`capacitor` adapters selected with `Capacitor.isNativePlatform()`: share primer, specialize request/recovery. Never promise background recording/geolocation in shared code; native only.

## 6. 2025–2026 changes

Chrome 141+ Local Network Access prompt (Sep 2025) gates public-site requests to private IPs/localhost; this affects school/on-prem/dev. Chromium Web MIDI now always prompts; Chrome 139+ added local speech; Chrome ~144 `<geolocation>` is the first shipping permission element.

Partner-domain cross-site frames needing own cookies/storage require Storage Access API (`document.requestStorageAccess()`, query name `storage-access`). iOS Safari through 26.x still lacks `getDisplayMedia`, file pickers, Bluetooth/USB/NFC; use Capacitor.
