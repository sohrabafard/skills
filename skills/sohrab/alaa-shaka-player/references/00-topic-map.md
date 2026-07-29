# Topic map — the only router in this skill

`SKILL.md` is always loaded. Nothing below loads until its row matches what is actually in front of you.
Every row names an **observable situation** — a line you are about to write, a symptom you are looking at,
a value you are about to change. If you cannot decide whether a row matches by looking at the screen, the
row is broken and fixing it comes before using it.

One file answers most tasks; two is normal. Loading ten means the task was never scoped.

## Before you write any Shaka line

| You are about to | Read |
|---|---|
| write a version number, a "latest" claim, a release date, or cite an upstream URL for a Shaka behaviour | `05-provenance-and-freshness.md` |
| decide which files the player work splits into, or hand a player lane to a parallel agent | `10-architecture-and-module-seams.md` |
| write `import ... from "shaka-player..."`, touch `quasar.config.*` or `vite.config.*` for the player, see `shaka is not defined`, or wire the transmux worker | `12-bundling-and-vite-loading.md` |
| put the player instance in a `ref()`, `reactive()` or Pinia store; write `onMounted`/`onBeforeUnmount` around a player; or see a Proxy-shaped failure at load time | `11-vue-quasar-binding.md` |
| write or review a `player.configure({...})` block, or see a magic number in one | `15-configure-surface-and-safe-defaults.md` |

## The capability areas

| You are about to | Read |
|---|---|
| call `new shaka.Player`, `attach`, `load`, `unload`, `detach`, `destroy`, `preload`, or set a start position | `20-core-lifecycle.md` |
| load a `.m3u8` or `.mpd`, see `LoadMode.SRC_EQUALS`, branch on Safari, or carry `useNativeHlsOnSafari` forward from v4 | `22-streaming-formats-and-native-hls.md` |
| cap or floor quality, write anything under `abr.*` or `restrictions.*`, disable ABR to pin a variant, or explain "why does HD take so long" | `24-adaptive-bitrate-and-restrictions.md` |
| build a quality, audio or subtitle menu; call `selectVariantTrack`/`selectAudioTrack`/`selectTextTrack`; or find a language choice lost after the next `load()` | `26-tracks-audio-video-text.md` |
| side-load a `.vtt` or `.srt`, style or reposition captions, set `subtitleDelay`, write a `TextDisplayer`, or see captions render but ignore your CSS | `28-subtitles-and-text-displayer.md` |
| set `playbackRate`, add a speed menu, implement fast-forward or rewind buttons, call `trickPlay`, or clamp the playable window | `30-playback-speed-seek-trickplay.md` |
| load a live manifest, draw a DVR scrubber, chase the live edge, tune latency, or see a live stream buffer after every chunk | `32-live-and-low-latency.md` |
| ship anything that will run on a mobile or lossy network: retry budgets, buffering goals, stalls, gap jumping, `streaming.failureCallback`, offline/online transitions | `35-unstable-networks-and-resilience.md` |
| change the playing asset, move to the next episode, build a playlist or a wall-clock schedule, or write `destroy()` then `new shaka.Player()` to change source | `37-switching-source.md` |
| register a request or response filter, add an auth header, rewrite a URL, wrap or unwrap a licence, or refresh a token that expires mid-session | `40-networking-engine-and-filters.md` |
| put a signed, presigned or tokenised URL into a manifest, a share link, a component prop or a stored offline asset | `42-media-url-trust-and-presigned.md` |
| write anything under `drm.*`, integrate Widevine, PlayReady or FairPlay, set robustness, or see a 6xxx error code | `45-drm.md` |
| implement in-app download, call `shaka.offline.Storage`, pick tracks to store, show download progress, or store with a persistent licence | `50-offline-and-in-app-download.md` |
| request a VAST or VMAP tag, integrate IMA or MediaTailor, insert an interstitial, render ad chrome, or handle an ad that never starts | `55-ads-vast-vmap-and-ima.md` |
| call `getStats()`, compute watch time, rebuffer ratio, startup time or a QoE figure, or decide what a playback event should carry | `60-analytics-and-getstats.md` |
| use `shaka.ui.Overlay`, choose control-panel elements, register a custom button, theme with `--shaka-*`, or translate a UI string | `65-ui-library-skin-and-localisation.md` |
| write a `catch` around `load()`, an `error` listener, a `failureCallback`, or map a numeric Shaka code to a user-facing message | `70-error-taxonomy-and-codes.md` |
| decide whether a feature works on iOS Safari, a smart TV, a console or Chromecast; or write a device-conditional default | `75-platform-and-browser-matrix.md` |
| change the pinned `shaka-player` version, upgrade from v4 LTS, prepare for v6, or see a deprecation warning in the console | `80-version-migration-and-release-deltas.md` |

## When something is already broken

| You are seeing | Read |
|---|---|
| a concrete symptom — SSR crash, stuck ad, silent captions, memory growth after route change, FairPlay stalling on one path only | `85-troubleshooting-by-symptom.md` |
| a claim that the player work is "done", "verified" or "tested", or you must choose between a headless and a visual run | `90-qa-modes-and-checklist.md` |

## Rows that are not optional when they match

- `35-unstable-networks-and-resilience.md` — Shaka's shipped `maxAttempts` default is `2` and on VOD every
  streaming failure is fatal by default. A player shipped without an explicit resilience policy is shipped
  broken on a mobile network, not merely untuned.
- `42-media-url-trust-and-presigned.md` — a presigned media URL is a transferable read grant. Deciding its
  lifetime locally, or letting it reach a component prop or a share link, has no safe default.
- `05-provenance-and-freshness.md` — every upstream fact in this skill carries a URL and a read date. A
  Shaka fact asserted here without one is not a fact yet.

## What is not in this skill

Retry and degradation doctrine (`/alaa-reliability-sla`, `$alaa-reliability-sla`); event, field and metric
names (`/alaa-services-contract`, `$alaa-services-contract`); IndexedDB quota, eviction and persistence
(`/alaa-indexeddb-browser-storage`, `$alaa-indexeddb-browser-storage`); Vue and Pinia shape
(`/alaa-vue-typescript-clean-code`, `$alaa-vue-typescript-clean-code`); skin art direction
(`/alaa-ui-ux-design-system`, `$alaa-ui-ux-design-system`); test design (`/alaa-testing-strategy`,
`$alaa-testing-strategy`); lane spawning (`/alaa-cc-orchestrator`, `$alaa-cc-orchestrator` and
`/alaa-codex-orchestrator`, `$alaa-codex-orchestrator`).
