# Browser device APIs and permissions

You are about to call an API the browser gates behind a prompt: microphone, camera, screen capture, geolocation, notifications, clipboard read, wake lock, sensors, Bluetooth, USB, or NFC. Scope: production Quasar use of those APIs, cross-browser permission behaviour, and the priming UX you own. Verified 2026-07-08 against MDN, developer.chrome.com, web.dev, webkit.org, Apple documentation, caniuse, and Playwright; re-verify fast-changing prompt behaviour per `references/80-upstream-deltas-and-live-checks.md` §6.

Also load `references/40-webotp-and-device-trust.md`, `references/30-service-worker-excellence.md`, and `references/31-ssr-pwa-and-security.md`. Route browser storage to `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`), Vue and TypeScript shape to `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`), and media playback to `/alaa-shaka-player` (`$alaa-shaka-player`).

## 1. Permission model

`navigator.permissions.query({ name })` yields `granted | denied | prompt` plus a `change` event. Always wrap it in `try/catch`: an unknown name rejects with `TypeError`, and older Safari builds and WebViews lack the API entirely. Query coverage: Chromium nearly all names; Firefox gained camera and microphone in 132 but not push or `clipboard-*`; Safari supports camera and microphone (16+), geolocation, and modern notifications and push, but not `clipboard-*`.

Permissions-Policy gates origin and iframe access: a cross-origin frame needs `allow="camera; microphone; geolocation"`, and the prompt names the top-level origin. Disable a surface you never use with `Permissions-Policy: camera=()`. Powerful APIs require HTTPS or localhost; a plain-HTTP LAN-IP dev server silently lacks `navigator.mediaDevices` and `Notification`, which reads as a code bug and is not one.

Real transient activation is required for `Notification.requestPermission()` (Firefox 72+, always Safari), `getDisplayMedia()`, `navigator.share()`, clipboard read on Safari and Firefox, fullscreen, pointer lock, `showOpenFilePicker()`, the Bluetooth/USB/Serial/HID/NFC choosers, and iOS `DeviceMotionEvent.requestPermission()`.

**Call `getUserMedia()` only inside a user-gesture handler, after the primer. Never call it during mount or route enter.** The specification does not formally require a gesture, so the call will appear to work in development and will be punished by prompt-reputation heuristics in production.

`granted` is cached history, not durable state: Chrome issues one-time grants and revokes after roughly 60 unused days through Safety Check; Firefox 115+ defaults geolocation, camera, and microphone to one-time; Safari intentionally re-prompts for camera and microphone each session, especially on iOS. Denial differs too: a Chrome deny is sticky until the user changes site settings; a Firefox dismissal without "remember" re-asks while a remembered deny sticks; Chrome's quieter notification UI collapses low-acceptance prompts and embargoes repeated dismissals.

Flow: query where supported -> primer -> request inside the gesture -> handle every outcome -> expect a future re-prompt. Never request on load, and never persist `granted` as next-session truth.

## 2. Per-API rules

Every API below is browser-only. Under SSR, call it from client-only or `onMounted` code with a capability check such as `'wakeLock' in navigator`, and initialise permission state on the client.

### Microphone and recording

`getUserMedia({ audio })` -> `MediaRecorder`. Probe `MediaRecorder.isTypeSupported()` in this order: `['audio/webm;codecs=opus', 'audio/mp4', 'audio/ogg;codecs=opus']`; record the first match and retain `recorder.mimeType`. Chrome and Firefox use webm/opus; Safari uses AAC in `audio/mp4` and has supported webm/opus since Safari 18.4. The backend must still accept `audio/mp4` for older iOS. `enumerateDevices()` labels are blank before an active grant, and Safari's `deviceId` is not stable across sessions.

iOS specifics: `AudioContext` starts suspended, so call `resume()` inside a gesture. Calls, Siri, and app switches can silently end tracks — listen to `track.onended` and `track.onmute` and offer a fresh-gesture re-record. Background and screen-locked capture stops; use Wake Lock plus a warning. Web background recording does not exist. Test the standalone PWA separately from the Safari tab, because permission scope and bugs differ. If `MediaRecorder` is missing or insufficient, use an AudioWorklet with a WASM encoder; for very old WebViews, `<input type="file" accept="audio/*" capture>`.

### Camera, geolocation, notifications, clipboard

**Camera and display.** `getUserMedia({ video: { facingMode: 'user' | 'environment' } })`; an iOS preview `<video>` needs `playsinline`. `getDisplayMedia()` is desktop-only — absent on iOS Safari through 26.x and on Android — and every call reopens the picker. Region and Element Capture are Chromium-only. Mobile screen sharing requires a native shell through Capacitor.

**Geolocation.** Set a finite `timeout`; the default is infinite, which is an unbounded spinner. Error 1 `PERMISSION_DENIED` gets recovery UI; error 2 `POSITION_UNAVAILABLE` gets a bounded retry with backoff and `maximumAge`; error 3 `TIMEOUT` gets a retry or a degraded path. Retry counts and backoff come from `/alaa-reliability-sla` (`$alaa-reliability-sla`), `references/20-retries.md`. `watchPosition` can error and then recover, so do not tear it down on the first error. With iOS Precise Location off, accuracy is roughly 1-5 km despite `enableHighAccuracy`, and the permission chain is OS -> Safari -> site. Background web geolocation does not exist; fall back to a server-side coarse default plus a manual city picker.

**Notifications and push.** Request only from a click; Firefox and Safari require it and Chrome punishes violations. iOS push requires iOS 16.4+ and a Home-Screen install: detect `matchMedia('(display-mode: standalone)')` and show an install primer before requesting. Notification actions and images are Chromium-only. Push, badging, and Declarative Web Push are `references/30-service-worker-excellence.md`.

**Clipboard.** Gesture-based `writeText` is universal. Silent `read` is Chromium-only behind a permission prompt; Firefox 127+ shows a contextual Paste confirmation and Safari an inline Paste button. Never depend on cross-browser silent read.

### Capability table — feature-detect every row

| API | Mid-2026 reality |
|---|---|
| Wake Lock `navigator.wakeLock.request('screen')` | Baseline: Chrome 84+/Safari 16.4+/Firefox 126+; no prompt; released automatically when the tab hides, so reacquire on `visibilitychange`; essential for exams and recording |
| Fullscreen | desktop and Android; **on iPhone Safari, video elements only** — no iPhone exam lockdown |
| Screen Orientation `lock()` | Chromium and Firefox on Android; no iOS Safari; use a CSS fallback |
| Vibration | Android only, sticky activation; enhancement only |
| Web Share `share()` | Safari, Chromium, Firefox on Windows and Android; gesture-required; clipboard or link fallback |
| `showOpenFilePicker` and siblings | Chromium desktop only; fall back to `<input type="file">` and a download anchor |
| OPFS `navigator.storage.getDirectory()` | universal, no prompt; large local blobs; pair with `persist()` |
| `navigator.storage.persist()` | Firefox prompts; Chrome and Safari decide silently from engagement, install, and push heuristics. Call it after real engagement and check `persisted()`. Eviction and the platform storage-lifetime limits are `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`), `references/32-eviction-and-recovery.md`; anything a user cannot recreate is also synced server-side |
| Bluetooth / USB / HID / Serial / NFC | Chromium only; NFC is Chrome on Android only; the chooser is a gesture-required permission; iOS requires Capacitor |
| Web MIDI | Chromium prompts for all access since roughly 124, not only sysex; absent in Safari |
| Speech Recognition | Chromium server-default; Chrome 139+ supports local `processLocally: true` plus `SpeechRecognition.available()` and `install()` — runtime-check the language tag you need; Safari is webkit-prefixed; Firefox has not shipped it; keep an own-ASR fallback for a critical flow |
| Speech Synthesis | universal, no prompt; the first iOS `speak()` needs a gesture; voices load asynchronously via `voiceschanged`; which voices exist depends on the OS |
| Motion and Orientation | iOS 13+ requires a gesture and `DeviceMotionEvent.requestPermission()` — guard with `typeof ... === 'function'`; Chromium is policy-gated with no prompt |
| Idle Detection / Battery / Generic Sensors | Chromium only; Mozilla and WebKit are negative; never make one a cross-browser core dependency |

## 3. UX: what you can customize

A browser prompt cannot be styled, reworded, or moved. What you own is the pre-prompt primer and the post-denial recovery.

1. **Two-step ask.** The user taps the feature -> the primer states what, why, and for how long ("microphone, only while recording, uploaded only when you submit") with Continue and Not now -> the API is called only from Continue, inside the gesture chain. This preserves the one pre-denial chance and protects the origin's prompt reputation.
2. **Query first where supported.** `granted` skips the primer; `denied` skips a prompt that cannot appear and shows recovery instead.
3. **No web API and no deep link opens site settings.** Show browser-specific instructions only: Chrome lock icon -> Site settings; Firefox lock icon -> Clear permissions; Safari macOS Settings for This Website; Safari iOS `aA` -> Website Settings, plus Settings -> Apps -> Safari. In a right-to-left interface, the instruction screenshots must be RTL-safe.
4. **Permission elements are not a general solution yet.** The generic `<permission>` element never shipped after its origin trial. Chrome pivoted to capability elements: `<geolocation>` ships around Chrome 144 and can reconfirm from `denied`. Feature-detect it, keep the JavaScript fallback, accept that the browser restricts its styling, and note that Firefox and Safari have neither support nor a commitment.
5. **Prompt language may differ from page language.** Say "your browser will now ask ..." rather than quoting a button label. Keep the primer visually distinct from browser chrome, and state that the choice is revocable.

Measure primer shown -> accepted -> API called -> resulting state, by diffing `permissions.query` and `Notification.permission`; emit that under `references/36-client-observability-contract.md`, not as ad-hoc logging. Never build a prompt wall, a dismissal loop, or an "allow notifications to continue" gate: Chrome's embargo and auto-revocation punish them and the damage lands on the origin, not the page.

## 4. Test and debug

Playwright: `context.grantPermissions([...])` (camera, microphone, geolocation, notifications, clipboard-read/write, screen-wake-lock, storage-access, local-network-access, and others), `setGeolocation()`, `clearPermissions()` — effectively Chromium-first, with a subset in WebKit and Firefox. Deterministic media: Chromium `--use-fake-device-for-media-stream`, optionally `--use-file-for-fake-audio-capture=answer.wav`, and `--use-fake-ui-for-media-stream`; Firefox `media.navigator.streams.fake`.

DevTools Sensors overrides geolocation — including "Location unavailable", which is error 2 — and device orientation; reset it from the lock icon. permission.site demonstrates cross-browser prompts. Keep a manual matrix covering one-time grants, quiet UI, Safari per-session prompts, iPhone tab versus installed PWA scope, and Android WebView.

## 5. Capacitor and the native split

Native replaces web permissions. Plugins use `checkPermissions()` and `requestPermissions()`; the OS dialog text comes from `Info.plist` strings — a missing `NSMicrophoneUsageDescription` crashes iOS at request time — and from the AndroidManifest. Push uses an APNs/FCM plugin, with no service worker, VAPID, or Home-Screen rule. Android WebView denies `getUserMedia` unless the host implements `onPermissionRequest`. Native can deep-link to app settings after a denial, which the web cannot.

Put a `PermissionService` port behind `web` and `capacitor` adapters selected with `Capacitor.isNativePlatform()`: share the primer, specialize the request and the recovery. Never promise background recording or background geolocation in shared code; those are native-only.

## 6. Changes through 2026

Chrome 141+ added a Local Network Access prompt (September 2025) gating public-site requests to private IPs and localhost — this affects school, on-premises, and development environments. Chromium Web MIDI now always prompts. Chrome 139+ added local speech recognition. Chrome around 144 ships `<geolocation>`, the first permission element.

A partner-domain cross-site frame that needs its own cookies or storage requires the Storage Access API (`document.requestStorageAccess()`, query name `storage-access`). iOS Safari through 26.x still lacks `getDisplayMedia`, file pickers, and Bluetooth/USB/NFC; use Capacitor for those.

Search: `permissions.query`, `Permissions-Policy`, `transient activation`, `getUserMedia`, `MediaRecorder`, `isTypeSupported`, `getDisplayMedia`, `watchPosition`, `PERMISSION_DENIED`, `wakeLock`, `requestPermission`, `DeviceMotionEvent`, `storage.persist`, `storage-access`, `permission primer`, `denial recovery`, `<geolocation>`, `grantPermissions`.
