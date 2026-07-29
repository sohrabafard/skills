# Unstable networks and resilience

**The priority area.** Shaka's shipped defaults are conservative by upstream's own admission
(*"The default values are very conservative"*, `docs/tutorials/network-and-buffering-config.md`), and
two of them make a player fail on a mobile network unless you change them: `maxAttempts` is **2**, and
on **VOD every streaming failure is fatal**.

All rows `verified` at v5.2.3, read 2026-07-28.

## The whole surface, in one place

Shaka gives you **nine** independent resilience mechanisms. A player that uses one or two is not tuned:

1. Four retry budgets — `manifest`, `streaming`, `drm`, and offline `Storage`'s own engine.
2. The buffering triad — `bufferingGoal`, `rebufferingGoal`, `bufferBehind`.
3. Stall detection.
4. Gap jumping.
5. Per-variant disable-and-recover (`maxDisabledTime`).
6. MediaSource recovery (`allowMediaSourceRecoveries`).
7. `streaming.failureCallback` — the app-level streaming policy.
8. `drm.failureCallback` + `retryLicensing()` — the app-level DRM policy (**new surface**).
9. A cancellable `retry` event on the NetworkingEngine, plus a built-in `window 'online'` handler.

## 1. Retry parameters — all three structures are identical

`shaka.extern.RetryParameters` (`externs/shaka/net.js`):

| Field | Meaning | Default |
|---|---|---|
| `maxAttempts` | Maximum attempts. **Minimum supported value is 1** (one request, no retries). | **`2`** |
| `baseDelay` | Delay before the first retry, ms. | `1000` |
| `backoffFactor` | Multiplier for successive delays. | `2` |
| `fuzzFactor` | Max fuzz per delay; `0.5` = ±50%. | `0.5` |
| `timeout` | Overall request timeout, ms. `0` = unlimited. | `30000` |
| `stallTimeout` | Stall timeout, ms — bytes stopped flowing. `0` = unlimited. | `5000` |
| `connectionTimeout` | Connection timeout, ms. `0` = unlimited. | `10000` |

Used at `manifest.retryParameters`, `streaming.retryParameters`, `drm.retryParameters`. Upstream:
*"The three separate retry settings are found under `drm.retryParameters` (for license requests),
`manifest.retryParameters` (for manifest requests), and `streaming.retryParameters` (for segment
requests). All three structures are identical."*

Backoff worked example from the same tutorial, base 1 s, factor 2: `t=0` initial → `t=1` → `t=3` →
`t=7` → `t=15`. With `fuzzFactor: 0.5`, an ideal delay of 8 becomes a uniform random value in
`[4, 12]`. Upstream's own guidance: *"You should consider the default backoff and fuzz factors as a
recommendation of best practice. The base delay, timeout, and maximum number of attempts should be
customized for your application's requirements."*

**The shape of backoff, the ceiling, and when to stop are doctrine owned by `/alaa-reliability-sla`
(`$alaa-reliability-sla`), `references/20-retries.md`. This file states only where each value lives in
Shaka.** Do not invent a ceiling here; take it from there.

## 2. Buffering

| Key | Default | Meaning |
|---|---|---|
| `streaming.bufferingGoal` | `10` s | How far ahead of the playhead to fetch. **This is what absorbs an outage.** |
| `streaming.rebufferingGoal` | **`0` s** | How much must be buffered before playback may start or resume. **When `0`, the playback rate is not used to control the buffer.** |
| `streaming.bufferBehind` | `30` s | Content kept behind the playhead. *"This is a minimum; if the stream's max segment size is longer than the `bufferBehind`, then that will be used instead."* |
| `streaming.evictionGoal` | `1.0` s | Minimum overflow before eviction starts. *"Values less than 1.0 are not recommended."* |
| `streaming.avoidEvictionOnQuotaExceededError` | `false` | Do not evict on `QuotaExceededError` (3017). |
| `streaming.segmentPrefetchLimit` | `1` (low-latency: `2`) | Segments prefetched in parallel per stream; multiplied by playback rate when rate ≠ 1. `0` = sequential. |
| `streaming.prefetchAudioLanguages` / `disableAudioPrefetch` / `disableTextPrefetch` / `disableVideoPrefetch` | `[]` / `false` ×3 | |
| `streaming.stopFetchingOnPause` | `false` | Stop fetching on pause **as long as something is buffered**. |
| `streaming.loadTimeout` | `30` s | Timeout to reject `load()` in `src=` mode. |

Upstream constraint: ***"`rebufferingGoal` should always be less than `bufferingGoal`."***

Also: *"While we are playing, we will only buffer the currently chosen stream… We also (by default) do
not clear the buffer when we adapt… There will be at most `bufferingGoal` seconds left of the old
bitrate in the buffer."* That is the direct trade-off against `24-adaptive-bitrate-and-restrictions.md`:
a large `bufferingGoal` survives longer outages **and** delays the visible effect of an ABR decision.
Choose deliberately and record which requirement decided it.

## 3–4. Stalls and gaps

| Key | Default | Meaning |
|---|---|---|
| `streaming.stallEnabled` | `true` | Run the stall detector. |
| `streaming.stallThreshold` | `1` s | Playhead motionless this long when motion is expected ⇒ stall. |
| `streaming.stallSkip` | `0.1` s, **`0` on Tizen, WebOS, Chromecast, Hisense** | Seconds to skip forward on a stall. **`0` means pause/play instead of seeking, and `0` is what upstream recommends on TV platforms.** |
| `streaming.gapDetectionThreshold` | `0.5` s | Max distance at which a gap is auto-jumped. |
| `streaming.gapPadding` | `0` in `player_configuration.js`; the typedef says `0.01` for Xbox and Legacy Edge, `2` for Tizen (**conflict C4**) | *"Based on our research (specific to Tizen), the `gapPadding` value must be greater than your GOP length."* |
| `streaming.gapJumpTimerTime` | `0.25` s | Gap polling interval. |
| `streaming.shouldFixTimestampOffset` | `false`, **`true` on Tizen, WebOS** | Fix `timestampOffset < baseMediaDecodeTime` (DASH + MP4 only). |
| `streaming.crossBoundaryStrategy` | `KEEP`, **`RESET_TO_ENCRYPTED` on Tizen 3, `RESET` on WebOS 3** | MSE reset when crossing a boundary. |
| `streaming.allowMediaSourceRecoveries` | `true` | Recover from `VIDEO_ERROR` (3016) by resetting MediaSource. |
| `streaming.minTimeBetweenRecoveries` | `5` s | |
| `streaming.maxDisabledTime` | `30` s | How long a variant is disabled after a `NETWORK HTTP_ERROR`. ***"If all variants are disabled this way, `NETWORK HTTP_ERROR` will be thrown."*** |
| `streaming.vodDynamicPlaybackRate` | `false` | Slow playback to protect the buffer on VOD. |
| `streaming.vodDynamicPlaybackRateLowBufferRate` | `0.95` | |
| `streaming.vodDynamicPlaybackRateBufferRatio` | `0.5` | Fraction of `bufferingGoal` that triggers the low rate. |

**v4.0 removal to remember:** `streaming.smallGapLimit` and `streaming.jumpLargeGaps` were removed;
**all gaps are now jumped**.

Related events: `stalldetected`, `gapjumped`, `buffering` (carries `buffering: boolean`),
`mediasourcerecovered`, `downloadfailed`, `downloadcompleted`, `downloadheadersreceived`.
Related stats: `stallsDetected`, `gapsJumped`, `bufferingTime`, `nonFatalErrorCount`.

## 7. `streaming.failureCallback` — the default is not a no-op

The config default in `player_configuration.js` is a logging stub, but `Player.defaultConfig_()`
**replaces it** with `defaultStreamingFailureCallback_`. Verbatim, `lib/player.js` L7806–7831:

```js
defaultStreamingFailureCallback_(error) {
  // For live streams, we retry streaming automatically for certain errors.
  // For VOD streams, all streaming failures are fatal.
  if (!this.isDynamic()) {
    return;
  }

  let retryDelaySeconds = null;
  if (error.code == shaka.util.Error.Code.BAD_HTTP_STATUS ||
      error.code == shaka.util.Error.Code.HTTP_ERROR) {
    // These errors can be near-instant, so delay a bit before retrying.
    retryDelaySeconds = 1;
    if (this.config_.streaming.lowLatencyMode) {
      retryDelaySeconds = 0.1;
    }
  } else if (error.code == shaka.util.Error.Code.TIMEOUT) {
    // We already waited for a timeout, so retry quickly.
    retryDelaySeconds = 0.1;
  }

  if (retryDelaySeconds != null) {
    error.severity = shaka.util.Error.Severity.RECOVERABLE;
    shaka.log.warning('Live streaming error.  Retrying automatically...');
    this.retryStreaming(retryDelaySeconds);
  }
}
```

Three consequences the implementation must handle:

1. **On VOD, every streaming failure is fatal by default.** VOD retry does not exist until you write it.
2. **Overriding `streaming.failureCallback` replaces this behaviour, including the live auto-retry.**
   Re-implement it if you still want it.
3. **Downgrading `error.severity` to `RECOVERABLE` inside the callback is the supported way** to stop a
   failure from being fatal.

`player.retryStreaming(retryDelaySeconds = 0.1)` → `boolean` (L7609–7626). It returns `false` when: no
content is loaded or it is still loading; content is loaded but streaming has seen no error; or
streaming errored but could not resume. **Treat `false` as "this path is exhausted", not as a transient.**

## 9. Automatic recovery when the network returns

Shaka installs this in its constructor (L1102–1107):

```js
// If the browser comes back online after being offline, then try to play
// again.
this.globalEventManager_.listen(window, 'online', () => {
  this.restoreDisabledVariants_();
  this.retryStreaming();
});
```

**The `online` event is already handled. Do not add your own listener that also calls
`retryStreaming()` — you will double-fire.**

## The `retry` event — cancelling a hopeless loop

`shaka.net.NetworkingEngine.RetryEvent`, type string `'retry'`
(`lib/net/networking_engine.js` L27–36, L704–720):

- Property `error`: `?shaka.util.Error` — `null` when the cause was a non-Shaka error.
- **The event is cancelable.** `event.preventDefault()` inside the handler throws the error instead of
  retrying, ending the loop immediately.
- After a retry is allowed, `++request.attempt` and the request is re-sent **to the next URI** in
  `request.uris`.

## 8. DRM-side resilience

| Key / method | Meaning |
|---|---|
| `drm.failureCallback: function(!shaka.util.Error)` | Called on DRM errors such as `LICENSE_REQUEST_FAILED`. ***"Set `error.handled` to true in the callback to prevent the error from being propagated as a fatal error."*** Default: no-op. |
| `player.retryLicensing(sessionMetadata, retryDelaySeconds)` | `async`. Manual licensing retry from the callback. |
| `player.renewLicense(sessionId)` | Manual renewal. |
| `drm.renewalIntervalSec` | Default `0` (disabled). **Only supported for PlayReady and FairPlay; Widevine is not supported.** |

## Working snippet — a complete unstable-network policy

```js
// ---------- 1. Retry budgets. The default maxAttempts of 2 is too low. ----------
// Values come from /alaa-reliability-sla ($alaa-reliability-sla), 20-retries.md.
const budget = {
  maxAttempts: 6,        // minimum supported is 1
  baseDelay: 500,        // ms
  backoffFactor: 2,      // 0.5s, 1s, 2s, 4s, 8s ...
  fuzzFactor: 0.5,       // +/- 50% jitter, so clients do not stampede
  timeout: 20000,        // ms; 0 = unlimited
  stallTimeout: 5000,    // abort a request whose bytes stop flowing
  connectionTimeout: 8000,
};

player.configure({
  manifest:  {retryParameters: {...budget, maxAttempts: 8}},
  streaming: {retryParameters: budget},
  drm:       {retryParameters: {...budget, maxAttempts: 4}},
});

// ---------- 2. Buffering: survive a longer outage ----------
player.configure({
  streaming: {
    bufferingGoal: 60,      // fetch 60s ahead; the trade-off is slower visible ABR response
    rebufferingGoal: 4,     // MUST be < bufferingGoal
    bufferBehind: 30,
    evictionGoal: 1,
    segmentPrefetchLimit: 2,
    stopFetchingOnPause: false,
  },
});

// ---------- 3. Stall and gap behaviour ----------
// TV platforms want stallSkip 0 (pause/play instead of seeking).
const isTv = /Tizen|Web0S|CrKey|Hisense/i.test(navigator.userAgent);
player.configure({
  streaming: {
    stallEnabled: true,
    stallThreshold: 1,
    stallSkip: isTv ? 0 : 0.1,
    gapDetectionThreshold: 0.5,
    gapJumpTimerTime: 0.25,
    allowMediaSourceRecoveries: true,
    minTimeBetweenRecoveries: 5,
    maxDisabledTime: 30,
  },
});

// ---------- 4. Streaming failure policy. THIS REPLACES SHAKA'S BUILT-IN LIVE RETRY. ----------
let streamingRetries = 0;
const MAX_STREAMING_RETRIES = 10;   // ceiling from /alaa-reliability-sla

player.configure('streaming.failureCallback', (error) => {
  const Code = shaka.util.Error.Code;
  const retryable = new Set([
    Code.BAD_HTTP_STATUS,   // 1001
    Code.HTTP_ERROR,        // 1002
    Code.TIMEOUT,           // 1003
    Code.SEGMENT_MISSING,   // 1011
  ]);

  if (!retryable.has(error.code)) return;      // let it be fatal

  // Do not hammer while the browser knows we are offline: Shaka's own
  // 'online' listener already calls retryStreaming() when we come back.
  if (navigator.onLine === false) return;

  if (streamingRetries++ >= MAX_STREAMING_RETRIES) return;

  // Downgrading severity is what stops this becoming a fatal 'error' event.
  error.severity = shaka.util.Error.Severity.RECOVERABLE;
  const delay = Math.min(0.5 * Math.pow(2, streamingRetries), 30);   // seconds
  const resumed = player.retryStreaming(delay);
  if (!resumed) streamingRetries = MAX_STREAMING_RETRIES;            // exhausted, stop trying
});

player.addEventListener('loaded', () => { streamingRetries = 0; });

// ---------- 5. Break out of a hopeless retry loop ----------
const net = player.getNetworkingEngine();
net.addEventListener('retry', (event) => {          // shaka.net.NetworkingEngine.RetryEvent
  const {code, data} = event.error || {};
  // For BAD_HTTP_STATUS: data[1] is the HTTP status, data[4] is the RequestType.
  if (code === shaka.util.Error.Code.BAD_HTTP_STATUS &&
      Array.isArray(data) &&
      data[1] === 404 &&
      data[4] === shaka.net.NetworkingEngine.RequestType.MANIFEST &&
      !player.isLive()) {
    event.preventDefault();                          // a 404 VOD manifest will never appear
  }
});

// ---------- 6. Observability. Report QUANTITIES; names come from /alaa-services-contract. ----------
player.addEventListener('buffering',   (e) => onBuffering(e.buffering));
player.addEventListener('stalldetected', () => countStall());
player.addEventListener('gapjumped',     () => countGapJump());
player.addEventListener('mediasourcerecovered', () => countMseRecovery());
player.addEventListener('downloadfailed', (e) => {
  countDownloadFailure({
    requestType: e.requestType,
    httpStatus: e.httpResponseCode,
    aborted: e.aborted,
    shakaCode: e.error && e.error.code,
    // Do NOT record e.request.uris here: a presigned URI is a credential.
    // See 42-media-url-trust-and-presigned.md.
  });
});

// ---------- 7. DRM-side resilience ----------
player.configure('drm.failureCallback', async (error) => {
  if (error.code === shaka.util.Error.Code.LICENSE_REQUEST_FAILED) {
    error.handled = true;                            // stop it being fatal
    await refreshAuthToken();
    for (const meta of player.getActiveSessionsMetadata()) {
      await player.retryLicensing(meta, /* retryDelaySeconds= */ 1);
    }
  }
});
```

## The intermittent-network checklist

| Do | Basis |
|---|---|
| Raise `maxAttempts` above `2` on all three budgets. | Upstream: attempts/timeouts *"should be customized for your application's requirements"*. |
| Keep `fuzzFactor` at `0.5`. | It exists to stop client stampedes. |
| Raise `bufferingGoal` so a short outage is absorbed; accept slower ABR reaction. | FAQ *"Why does it take so long to switch to HD?"* |
| Keep `rebufferingGoal < bufferingGoal`. | Upstream constraint. |
| Set `stallTimeout` and `connectionTimeout`, not just `timeout`, so a half-open TCP connection is abandoned quickly. | Field semantics in `RetryParameters`. |
| Rely on the built-in `window 'online'` handler; add none of your own. | `lib/player.js` L1102. |
| Cancel with the `retry` event for errors that can never succeed. | `docs/tutorials/errors.md`. |
| Remember request filters run **on every attempt** since v5.0 — that is the hook for refreshing an expired token mid-retry. | `docs/tutorials/license-server-auth.md`. See `40-networking-engine-and-filters.md`. |
| Watch `maxDisabledTime`: variants disabled by HTTP errors return after 30 s, but **if all variants get disabled the `HTTP_ERROR` becomes fatal**. | `StreamingConfiguration.maxDisabledTime`. |

## The eight failure scenarios to prove against

`90-qa-modes-and-checklist.md` carries the evidence rules; these are the scenarios:
manifest 404 · segment 5xx mid-playback · segment timeout at low bandwidth · licence 401 mid-session
(token expiry) · the device going offline and back online · every variant disabled by HTTP errors ·
`QuotaExceededError` (3017) on a long session · a `VIDEO_ERROR` (3016) MediaSource recovery.

**Best practice.** Implement `streaming.failureCallback` as an explicit **allow-list** of retryable
codes with a bounded, exponential, jittered retry, and reset the counter on `loaded`. An allow-list
fails closed on an unknown code; a deny-list retries forever on one.
**Common mistake.** Overriding `streaming.failureCallback` and thereby silently deleting Shaka's
built-in live-stream auto-retry — live streams then die on the first transient 5xx, in production,
weeks after the change that caused it.
