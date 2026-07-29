# Browser and platform matrix

All rows `verified` at v5.2.3, read 2026-07-28, from `README.md` unless stated.

Legend: **Y** = MSE/EME path · **Native** = Apple's native HLS via `src=` · `–` = not applicable ·
`N` = not supported.

| Browser | Windows | Mac | Linux | Android | iOS ≥ 9 | iOS ≥ 17.1 | iPadOS ≥ 13 | ChromeOS | Other |
|---|---|---|---|---|---|---|---|---|---|
| Chrome | **Y** | **Y** | **Y** | **Y** | Native | Native | Native | **Y** | – |
| Firefox | **Y** | **Y** | **Y** | untested⁵ | Native | Native | Native | – | – |
| Edge (legacy) | **Y** | – | – | – | – | – | – | – | – |
| Edge Chromium | **Y** | **Y** | **Y** | untested⁵ | Native | Native | Native | – | – |
| IE | **N** | – | – | – | – | – | – | – | – |
| Safari | – | **Y** | – | – | Native | **Y** | **Y** | – | – |
| Opera | **Y** | **Y** | **Y** | untested⁵ | Native | – | – | – | – |
| Chromecast² | – | – | – | – | – | – | – | – | **Y** |
| Tizen TV³ | – | – | – | – | – | – | – | – | **Y** |
| WebOS⁶ | – | – | – | – | – | – | – | – | **Y** |
| Hisense⁷ / Vizio⁷ | – | – | – | – | – | – | – | – | **Y** |
| Xbox One | – | – | – | – | – | – | – | – | **Y** |
| PlayStation 4⁷ / 5⁷ | – | – | – | – | – | – | – | – | **Y** |
| Titan OS⁷ / TiVo OS⁷ | – | – | – | – | – | – | – | – | **Y** |

Notes, verbatim: ² *"The latest stable Chromecast firmware is tested. Both sender and receiver can be
implemented with Shaka Player."* ³ *"Tizen 2017 model is actively tested and supported by the Shaka
Player team. Tizen 2016 model is community-supported and untested by us."* ⁵ *"These are expected to
work, but are not actively tested by the Shaka Player team."* ⁶ / ⁷ *"expected to work, but are
community-supported and untested by us."*

IE11 support ended after v3.1. iOS 12 / Safari 12 support was removed in v4.0. TiVo OS and Titan OS
support arrived in 5.1.0.

## iOS and iPadOS — the platform where everything differs

Verbatim from `README.md` §"NOTES for iOS and iPadOS":

> - *"We support iOS 9+ through Apple's native HLS player. We provide the same top-level API, but we
>   just set the video's `src` element to the manifest/media. So we are dependent on the browser
>   supporting the manifests."*
> - *"Since iPadOS 13 MediaSource Extensions is supported"*
> - *"Since iPadOS 17 and iOS 17.1 ManagedMediaSource Extensions is supported"*

And from `docs/tutorials/faq.md`:

> *"Starting in v2.5, we support it through Apple's native HLS player. So you can use the same
> top-level APIs; but we are dependent on the browser handling the streaming. So we won't support DASH
> on iOS since the browser doesn't support it. In a future version, we plan to support
> `ManagedMediaSource` on iOS to achieve control over both DASH and HLS playback on iOS. See #5271…"*

> **Conflict C5.** The README says ManagedMediaSource **is** supported since iOS 17.1 / iPadOS 17; the
> FAQ says it is a **future** plan. Both ship at v5.2.3. Recorded, not resolved
> (`05-provenance-and-freshness.md`). **Branch on `player.getLoadMode()`, never on an iOS version.**

### What is required on iOS Safari

| Requirement | Grade |
|---|---|
| **HLS only** below iOS 17.1 — DASH will not play; the browser is doing the streaming. | `verified` |
| Load mode will be **`SRC_EQUALS`**, not `MEDIA_SOURCE`, on the native path. | `inferred` from the `LoadMode` enum + the native-HLS description |
| **FairPlay is the only DRM.** Modern EME `com.apple.fps`; legacy `com.apple.fps.1_0` via `shaka.polyfill.PatchedMediaKeysApple.install()`. | `verified` |
| **A FairPlay server certificate is mandatory.** | `verified` |
| **MSE + TS + FairPlay is unsupported** in both EME modes; MSE + CMAF works only with Modern EME. | `verified` |
| **EME requires a secure origin** (https or localhost). Insecure origin + encrypted content → `NO_WEB_CRYPTO_API` (4042). | `verified` |
| `preload()` returns `null` on Safari native HLS. | `verified` |
| Side-loaded text: **WebVTT only**, and only via the `src=` path (2012 / 2013 otherwise). | `verified` |
| `abr.minTimeToSwitch` defaults to **`0.5` s on Apple browsers** vs `0` elsewhere. | `verified` |
| `streaming.useNativeHlsForFairPlay` defaults `true`; disabling it is explicitly risky for multi-key streams. | `verified` |
| `mediaSource.useSourceElements` default `true`; *"Disabling it will prevent using AirPlay on MSE."* | `verified` |
| UI has `preferVideoFullScreenInVisionOS` for visionOS. | `verified` |
| **5.2.2 fix:** *"Prevent `screen.orientation` methods from being garbage collected on Safari"*. **5.1.x/5.0.x line:** *"Performance: ContentWorkarounds optimization for Safari 26.4+"*. | `verified` |

## Device-conditional defaults Shaka already applies

You rarely need your own user-agent branch — Shaka's `player_configuration.js` already varies these:

| Key | Non-default platform |
|---|---|
| `streaming.stallSkip` | `0` on **Tizen, WebOS, Chromecast, Hisense** (pause/play instead of seeking) |
| `streaming.gapPadding` | typedef: `0.01` on Xbox and Legacy Edge, `2` on Tizen (conflict C4) |
| `streaming.shouldFixTimestampOffset` | `true` on **Tizen, WebOS** |
| `streaming.crossBoundaryStrategy` | `RESET_TO_ENCRYPTED` on **Tizen 3**, `RESET` on **WebOS 3** |
| `textDisplayer.suspendRenderingWhenHidden` | `false` on **Tizen, WebOS, Hisense, Vizio** |
| `abr.minTimeToSwitch` | `0.5` on **Apple browsers** |
| `drm.preferredKeySystems` | `['com.microsoft.playready']` on **Xbox One, PlayStation 4** |
| `drm.parseInbandPsshEnabled` | `true` on **Xbox One** |
| `drm.ignoreDuplicateInitData` | `false` on **Tizen 2** |
| `drm.defaultAudioRobustnessForWidevine` / `…Video…` | `''` on **Android** |
| `ads.customPlayheadTracker`, `ads.skipPlayDetection` | `true` on **Tizen, WebOS, Chromecast, Hisense, PS4, PS5, Xbox, Vizio** |
| `ads.supportsMultipleMediaElements` | `false` on the same set |
| UI `customContextMenu` | `false` on **mobile, cast, smart TV** |
| Transmux worker | **Tizen, WebOS and Hisense opt out internally** regardless of the setting |
| `streaming.liveSync.enabled` | Upstream warns of sound loss on some smart TVs when enabled |

## Capability detection, not user-agent sniffing

```js
// Static, before constructing anything:
shaka.polyfill.installAll();
const supported = shaka.Player.isBrowserSupported();          // boolean
const support   = await shaka.Player.probeSupport();          // shaka.extern.SupportType
const offline   = await shaka.offline.Storage.support();      // {basic, encrypted: {...}}

// Runtime, AFTER load() resolves - the only correct signal for what this session can do:
const native = player.getLoadMode() === shaka.Player.LoadMode.SRC_EQUALS;

const capabilities = {
  canSideLoadText:      !native && !player.isLive(),
  canPreloadNext:       !native,
  canPickExactVariant:  !native,
  canDownloadOffline:   offline.basic && !player.isLive(),
  canStorePersistentLicence: offline.encrypted['com.widevine.alpha'] === true,
  hasManifestStats:     !native,      // manifestSizeBytes/PeriodCount/GapCount are NaN otherwise
};
renderPlayerMenus(capabilities);
```

The one place a user-agent test is defensible is choosing between two Shaka *config* values that
Shaka itself does not vary — the `stallSkip` TV example in
`35-unstable-networks-and-resilience.md`. Everywhere else, `probeSupport()`, `Storage.support()` and
`getLoadMode()` answer the question directly.

## The QA matrix

Chrome · Edge · Firefox · Safari macOS · **iOS Safari** · Android Chrome · Android WebView (if
relevant) · WKWebView (if relevant), plus any TV or console target the product actually ships to.
**iOS Safari is a separate row from Safari macOS and always must be** — it is a different load mode,
a different DRM, a different text-track capability and a different preload behaviour.

**Best practice.** Derive every UI capability from `getLoadMode()`, `probeSupport()` and
`Storage.support()` after load, and store the result once per session. A menu built from a browser
name is wrong on desktop Safari, where both paths exist.
**Common mistake.** Testing "Safari" and calling iOS covered. On macOS Safari you are usually on MSE
with full track control; on iOS below 17.1 you are on `SRC_EQUALS` with none of it — the same code
path produces two different products.
