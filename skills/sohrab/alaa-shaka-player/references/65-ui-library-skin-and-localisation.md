# The UI library, custom elements, theming and localisation

All rows `verified` at v5.2.3, read 2026-07-28, from `ui/ui.js`, `ui/controls.js`, `ui/element.js`,
`ui/localization.js`, `ui/externs/ui.js`, `ui/*.less` and `docs/tutorials/ui*.md`.

Colour, type, spacing, motion and the design decisions of a skin belong to
`/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`). This file owns only the mechanisms that
make those decisions reachable.

## Current position

The UI ships as a **separate bundle** (`shaka-player.ui.js`) plus a stylesheet. Two setup styles:
declarative (`data-shaka-player-container` + the `shaka-ui-loaded` event) or programmatic
(`new shaka.ui.Overlay(player, container, videoElement)`). **As of 5.2.0 there are two CSS outputs.**

## API surface

| Name | Notes |
|---|---|
| `new shaka.ui.Overlay(player, videoContainer, videoElement)` | Programmatic setup. |
| `ui.getControls()` → `shaka.ui.Controls` | |
| `ui.configure(config, value?)` / `ui.getConfiguration()` | Two-form, like `player.configure`. |
| `ui.destroy(forceDisconnect = false)` | `async`. Disposes the Controls **and the Player the UI created**. |
| `ui.setEnabled(enabled)`, `ui.isMobile()`, `isCast()`, `isSmartTV()` | |
| `ui.setTextWatermark(text, options)` / `removeWatermark()` | For non-subtitle overlay text — the tutorial explicitly steers metadata display here rather than to a TextDisplayer. |
| `controls.getPlayer()` / `getLocalPlayer()` | The first is a **cast-enabled proxy**; the second is the local instance. |
| `controls.getVideo()` / `getLocalVideo()` | Same distinction. |
| `controls.getVideoContainer()` / `getControlsContainer()` | |
| `controls.getLocalization()` → `shaka.ui.Localization` | |
| `controls.getAdManager()` / `getQueueManager()` / `getMediaSession()` | |
| `controls.getClientSideAdContainer()` / `getServerSideAdContainer()` | `55-ads-vast-vmap-and-ima.md` |
| `controls.showAdUI()` / `hideAdUI()` / `showUI()` / `hideUI()` / `isOpaque()` | |
| `controls.toggleFullScreen()` / `isFullScreenSupported()` / `isFullScreenEnabled()` | `async` toggle. |
| `controls.togglePiP()` / `isPiPAllowed()` / `isPiPEnabled()` | `async` toggle. |
| `controls.takeScreenshot(format = 'png', imageQuality = 1)` / `copyVideoFrameToClipboard(...)` | Format + quality args **new in 5.2.0**. |
| VR | `canPlayVR()`, `isPlayingVR()`, `getVRNorth()`, `getVRFieldOfView()`, `setVRFieldOfView()`, `toggleStereoscopicMode()`, `incrementYaw/Pitch/Roll()` |
| `shaka.ui.Controls.registerElement(name, factory)` | Control-panel / overflow / context-menu elements. |
| `shaka.ui.Controls.registerBigElement(name, factory)` | For `bigButtons`. |
| `shaka.ui.Controls.registerSeekBar(factory)` | Replace the seek bar wholesale. |
| Cast | `controls.setCastReceiver()`, `getCastProxy()`, `getCastReceiver()`, `allowCast()`, `isCastAllowed()` |

Declarative DOM attributes: `data-shaka-player-container`, `data-shaka-player`,
`data-shaka-player-cast-receiver-id`, `data-shaka-player-cast-android-receiver-compatible`,
`data-shaka-player-vr-canvas`. Document events: **`shaka-ui-loaded`** and
**`shaka-ui-load-failed`** (whose `errorEvent.detail.reasonCode` is a
`shaka.ui.Overlay.FailReasonCode`). Controls events: `error`, `caststatuschanged`, `uiupdated`.

## Control-panel elements

`shaka.extern.UIConfiguration` keys: `controlPanelElements`, `topControlPanelElements`, `bigButtons`,
`overflowMenuButtons`, `contextMenuElements`, `statisticsList`, `adStatisticsList`, `playbackRates`,
`playbackRateSliderMin`, `playbackRateSliderMax`, `fastForwardRates`, `rewindRates`, `addSeekBar`,
`customContextMenu`, `castReceiverAppId`, `castAndroidReceiverCompatible`,
`clearBufferOnQualityChange`, `showUnbufferedStart`, `seekBarColors`, `volumeBarColors`,
`playbackRateBarColors`, `qualityMarks`, `trackLabelFormat`, `textTrackLabelFormat`, `fadeDelay`,
`closeMenusDelay`, `doubleClickForFullscreen`, `singleClickForPlayAndPause`,
`enableKeyboardPlaybackControls`, `enableFullscreenOnRotation`, `forceLandscapeOnFullscreen`,
`enableTooltips`, `keyboardSeekDistance`, `keyboardLargeSeekDistance`, `fullScreenElement`,
`showAudioChannelCountVariants`, `seekOnTaps`, `tapSeekDistance`, `refreshTickInSeconds`,
`displayInVrMode`, `defaultVrProjectionMode`, `preferVideoFullScreenInVisionOS`, `showAudioCodec`,
`showVideoCodec`, `castSenderUrl`, `enableKeyboardPlaybackControlsInWindow`, `alwaysShowVolumeBar`,
`shortcuts`, `menuOpenUntilUserClosesIt`, `allowTogglePresentationTime`,
`showRemainingTimeInPresentationTime`, `enableVrDeviceMotion`, `enableVrWheelZoom`, `showUIAlways`,
`showUIAlwaysOnAudioOnly`, `preferIntlDisplayNames`, `mediaSession`, `captionsStyles`,
`captionsFontScaleFactors`, `documentPictureInPicture`, `showUIOnPaused`, `showMenusOnTheRight`,
`customTrackLabel`, `showBufferingSpinner`.

Named defaults: `playbackRates` `[1, 1.25, 1.5, 2, 3]` · `playbackRateSliderMin` `0.5` ·
`playbackRateSliderMax` `3` · `fastForwardRates` `[2, 4, 8, 1]` · `rewindRates` `[-1, -2, -4, -8]` ·
`addSeekBar` `true` · `customContextMenu` `true` **except on mobile, cast and smart TV** ·
`castReceiverAppId` `''` · `castAndroidReceiverCompatible` `false` ·
`clearBufferOnQualityChange` `true` · `showUnbufferedStart` `false` · `trackLabelFormat` `LANGUAGE`.

**`controlPanelElements` names:** `time_and_duration`, `play_pause`, **`play_pause_buffering` (new in
5.2.0)**, `mute`, `volume`, `mute_volume`, `fullscreen`, `overflow_menu`, `rewind`, `fast_forward`,
`spacer`, `picture_in_picture`, `loop`, `cast`, `remote`, `quality`, `video_type`, `language`,
`playback_rate`, `captions`, `recenter_vr`, `toggle_stereoscopic`, `chapter`, `captions-position`,
`captions-size`, `skip_next`, `skip_previous`, `skip_next_always`, `skip_previous_always`,
**`queue` (new in 5.2.0)**.

**`overflowMenuButtons` / `contextMenuElements`** (identical set): `captions`, `cast`, `quality`,
`video_type`, `language`, `picture_in_picture`, `loop`, `playback_rate`, `remote`, `statistics`,
`recenter_vr`, `toggle_stereoscopic`, `ad_statistics`, `save_video_frame`, `copy_video_frame`,
`chapter`, `mute`, `captions-position`, `captions-size`, `queue`.

**`bigButtons`:** `play_pause`, `play_pause_buffering`, `mute`, `fullscreen`, `rewind`,
`fast_forward`, `picture_in_picture`, `remote`, `loop`, `skip_next`, `skip_previous`,
`skip_next_always`, `skip_previous_always`.

Rule, verbatim: *"the `overflow_menu` button needs to be part of the `controlPanelElements` layout for
the overflow menu to be available to the user."*

**Removed in v5.0:** `airplay` (use `remote`) and `addBigPlayButton` (use `bigButtons`).

## Custom control elements

Implement `shaka.extern.IUIElement`, normally by extending `shaka.ui.Element`, and register a factory
with `shaka.ui.Controls.registerElement(name, factory)`. **v4.0 breaking change: `IUIElement` plugins
must have a `release()` method, not `destroy()`.** An element that implements `destroy()` leaks.

`shaka.ui.Element` gives subclasses these protected members: `this.parent` (`HTMLElement`),
`this.controls`, `this.eventManager` (`shaka.util.EventManager`), `this.localization`, `this.player`,
`this.video`, `this.adManager`, `this.ad` (`?shaka.extern.IAd`, kept current).

## Theming through CSS custom properties

| File | Behaviour | When |
|---|---|---|
| `dist/controls.css` | Legacy. Custom properties **resolved at build time** by `postcss-custom-properties`, fallbacks retained. Targets Chrome 38, Safari 8, Firefox 42. | Only for ancient browsers. |
| `dist/controls.modern.css` | **Preserves the custom properties, so runtime theming works.** Targets the last 2 years of browsers. | **Recommended for all modern applications.** |

Custom properties defined in the LESS sources: `--shaka-badge-active`, `--shaka-badge-color`,
`--shaka-badge-size`, `--shaka-bg`, `--shaka-bg-90`, `--shaka-bg-hover`, `--shaka-bg-menu`,
`--shaka-bg-solid`, `--shaka-controls-w`, `--shaka-font-color`, `--shaka-font-color-secondary`,
`--shaka-font-family`, `--shaka-font-size`, `--shaka-font-size-sm`, `--shaka-icon-size`,
`--shaka-icon-size-lg`, `--shaka-icon-size-sm`, `--shaka-rate-bg-active`, `--shaka-rate-border`,
`--shaka-rate-border-active`, `--shaka-rate-preset-active`, `--shaka-rate-preset-bg`,
`--shaka-rate-preset-border`, `--shaka-rate-preset-hover`, `--shaka-rate-slider`,
`--shaka-thumb-color`, `--shaka-thumb-size`, `--shaka-title-size`, `--shaka-touch-size`,
`--shaka-track-color`, `--shaka-track-h`.

**These cover controls, not caption text** (`28-subtitles-and-text-displayer.md`).

Colours CSS **cannot** reach — they are built as JS linear gradients — must go through config:
`seekBarColors` (`base`, `buffered`, `played`, `adBreaks`), `volumeBarColors`,
`playbackRateBarColors`.

## Localisation

| Fact | Note |
|---|---|
| `controls.getLocalization()` → `shaka.ui.Localization` with `changeLocale(locales)`, `insert(locale, localizations, conflictResolution)`, `resolveDictionary(dictionary)`, `resolve(id)`, `getCurrentLocales()`, `release()`. | |
| Translations ship as JSON under `ui/locales/`. **49 locale files** at v5.2.3. | |
| Lazy-loading hook: the `unknown-locales` event, with `e.locales`. | |
| **`insert()` takes a `Map`, not a plain object**: `new Map(Object.entries(translations))`. | |
| 5.2.0: *"UI: Use UI language to display languages names"*; UI config `preferIntlDisplayNames`. | |
| Locales are also selected at build time: `build/all.py --locales`. | |

## What breaks when the player is wrapped in a framework component

| Problem | Detail |
|---|---|
| **Vue reactivity destroys the Player.** | The full quote and the rules are in `11-vue-quasar-binding.md`. |
| **DOM-after-load setup.** The declarative `data-shaka-player-container` scan happens on page load. | Upstream states this is a primary reason `shaka.ui.Overlay` exists: *"One of the big use cases for this is building Shaka Player into UI frameworks that modify the DOM after the page load."* |
| **Attach ordering with the UI.** In the programmatic snippet, `new shaka.ui.Overlay(...)` is constructed **before** `await localPlayer.attach(videoElement)`. | Upstream comment: *"Now that the player has been configured to be part of a UI, attach it to the video."* |
| **Cast proxy confusion.** `controls.getPlayer()` returns a proxy routing calls to the Cast receiver while casting; `getLocalPlayer()` is the local instance. | A component caching the wrong one behaves oddly during a cast session. |
| **Do not double-create.** With DOM-based setup the UI creates the Player for you (`video['ui']`). | Constructing your own as well produces two Players contending for one element. |
| **5.2.1 fix:** *"UI: Scope form element font inheritance to the player container"* (#10353). | Previously the UI's form styling could leak into the host app. |

## Working snippet — programmatic UI, custom button, theme, locale

```js
const container = document.getElementById('player-container');
const video = document.getElementById('video');

const localPlayer = new shaka.Player();
const ui = new shaka.ui.Overlay(localPlayer, container, video);
await localPlayer.attach(video);        // AFTER constructing the Overlay

const controls = ui.getControls();
const player = controls.getPlayer();    // cast-aware proxy
// const local = controls.getLocalPlayer();  // the raw local instance

// ---------- A custom control-panel button ----------
class SkipButton extends shaka.ui.Element {
  constructor(parent, controls) {
    super(parent, controls);   // gives this.player/.video/.controls/.eventManager/.localization/.adManager/.ad
    this.button_ = document.createElement('button');
    this.button_.classList.add('my-skip-button');
    this.button_.setAttribute('aria-label', this.localization.resolve('SKIP'));
    this.button_.textContent = 'Skip';
    this.parent.appendChild(this.button_);

    // Use this.eventManager so listeners are cleaned up in release().
    this.eventManager.listen(this.button_, 'click', () => {
      this.player.load(nextManifestUri());
    });
  }
  // v4.0+ requires release(), NOT destroy(). An element with destroy() leaks.
  release() {
    this.eventManager.release();
    super.release();
  }
}
SkipButton.Factory = class {
  create(rootElement, controls) { return new SkipButton(rootElement, controls); }
};
shaka.ui.Controls.registerElement('skip', new SkipButton.Factory());

// ---------- Layout ----------
ui.configure({
  controlPanelElements: [
    'play_pause', 'time_and_duration', 'spacer',
    'mute_volume', 'skip', 'captions', 'quality', 'overflow_menu', 'fullscreen',
  ],
  overflowMenuButtons: ['language', 'playback_rate', 'chapter', 'statistics', 'cast'],
  bigButtons: ['play_pause'],
  customContextMenu: true,
  contextMenuElements: ['statistics'],
  statisticsList: ['width', 'height', 'playTime', 'bufferingTime', 'estimatedBandwidth'],
  addSeekBar: true,
  enableTooltips: true,
  keyboardSeekDistance: 10,
  keyboardLargeSeekDistance: 60,
  showMenusOnTheRight: false,           // set true for an RTL layout
  trackLabelFormat: shaka.ui.Overlay.TrackLabelFormat.LABEL_OR_LANGUAGE,
  // JS-built gradients: CSS cannot reach these.
  seekBarColors: {
    base:     'rgba(255,255,255,0.3)',
    buffered: 'rgba(255,255,255,0.54)',
    played:   'rgb(0, 200, 160)',
    adBreaks: 'rgb(255, 204, 0)',
  },
});

// ---------- Localisation: lazy-load locales ----------
const localization = controls.getLocalization();
localization.addEventListener('unknown-locales', async (e) => {
  for (const locale of e.locales) {
    const res = await fetch(`/shaka/ui/locales/${locale}.json`);
    localization.insert(locale, new Map(Object.entries(await res.json())));  // a Map, not an object
  }
});
localization.changeLocale(['fa', 'en']);

// ---------- Teardown ----------
async function teardown() {
  await ui.destroy();   // disposes Controls and the Player the UI created
}
```

```css
/* Requires controls.modern.css for these to work at runtime.
   Token values themselves come from /alaa-ui-ux-design-system. */
:root {
  --shaka-controls-w: 98%;
  --shaka-font-family: Vazirmatn, roboto, sans-serif;
  --shaka-font-color: #fff;
  --shaka-font-size: 14px;
  --shaka-bg: rgba(0, 0, 0, 0.5);
  --shaka-bg-hover: rgba(0, 0, 0, 0.75);
  --shaka-bg-menu: rgba(0, 0, 0, 0.9);
  --shaka-thumb-color: #00c8a0;
  --shaka-track-color: #fff;
  --shaka-icon-size: 24px;
  --shaka-touch-size: 48px;
}
```

**Best practice.** Ship `controls.modern.css`, theme with `--shaka-*`, and keep the Player instance
out of any reactive store. Use `this.eventManager` inside a custom element so `release()` cleans up
everything you registered.
**Common mistake.** Implementing `destroy()` on a custom UI element instead of `release()` — since
v4.0 the element leaks silently. Second: styling the seek bar in CSS. `seekBarColors` is built as a JS
gradient and CSS cannot reach it.
