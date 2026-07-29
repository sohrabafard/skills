# The `shaka.util.Error` taxonomy and the complete code list

All rows `verified` at v5.2.3, read 2026-07-28, from `lib/util/error.js` (1,287 lines) and
`docs/tutorials/errors.md`. **155 codes exist at v5.2.3.**

Retry shape, backoff, ceilings and degradation are doctrine owned by `/alaa-reliability-sla`
(`$alaa-reliability-sla`). This file owns which Shaka mechanism handles which category and what each
code means.

## Structure

| Field | Type | Notes |
|---|---|---|
| `severity` | `shaka.util.Error.Severity` | `RECOVERABLE = 1`, `CRITICAL = 2` |
| `category` | `shaka.util.Error.Category` | see below |
| `code` | `shaka.util.Error.Code` | see the list |
| `data` | `Array<*>` | The constructor's rest args. **Per-code shape, undocumented in general.** |
| `handled` | boolean | Initialised `false`; set `true` in a failure callback to stop propagation. |
| `message` | string | Compiled: `'Shaka Error <code>'`. Debug/uncompiled: `'Shaka Error CATEGORY.CODE_NAME (data)'`. |

**The critical subtlety, stated verbatim in the source:**

> *"The `@extends {Error}` annotation below is a type-only declaration for the Closure Compiler; this
> class does **not** actually extend the native `Error` at runtime… In particular,
> `(new shaka.util.Error(...)) instanceof Error` is **`false`**. This is intentional: it lets
> application code tell an unhandled native error apart from a Shaka-specific error by checking
> `instanceof Error` before checking `instanceof shaka.util.Error`."*

So **check `instanceof Error` first**. A value that passes it is a Shaka crash, not a Shaka error.

Severity, verbatim:

- `RECOVERABLE`: *"An error occurred, but the Player is attempting to recover from the error. If the
  Player cannot ultimately recover, it still may not throw a CRITICAL error. For example, retrying for
  a media segment will never result in a CRITICAL error (the Player will just retry forever)."*
- `CRITICAL`: *"A critical error that the library cannot recover from. These usually cause the Player
  to stop loading or updating. **A new manifest must be loaded to reset the library.**"*

## Categories and the mechanism that handles each

| Name | Value | Which Shaka mechanism handles it |
|---|---|---|
| `NETWORK` | 1 | The retry domain: `retryParameters`, the cancelable `retry` event, `streaming.failureCallback`. |
| `TEXT` | 2 | Survivable when `streaming.ignoreTextStreamFailures = true`. |
| `MEDIA` | 3 | `VIDEO_ERROR` (3016) is recovered via `streaming.allowMediaSourceRecoveries`. |
| `MANIFEST` | 4 | Load-time. Mostly terminal for the load. |
| `STREAMING` | 5 | `streaming.failureCallback`. |
| `DRM` | 6 | `drm.failureCallback` + `retryLicensing()`. |
| `PLAYER` | 7 | Lifecycle. Mostly terminal. |
| `CAST` | 8 | Session-level. |
| `STORAGE` | 9 | Offline. Terminal for that operation. |
| `ADS` | 10 | Ads fail independently of content — preserve that with a watchdog (`55-…`). |

> **There is no upstream field or table marking a category "recoverable".** Recoverability is
> expressed **per error instance** via `error.severity`, and it is **mutable** — the default streaming
> failure callback literally assigns `error.severity = RECOVERABLE` before retrying. Any statement of
> the form "category X is recoverable" is an `inferred` claim, not a documented fact. `not documented`
> — searched `lib/util/error.js`, `docs/tutorials/errors.md`, `externs/shaka/error.js` on 2026-07-28;
> no recoverability table exists.

## The complete code list

**1xxx NETWORK** — `UNSUPPORTED_SCHEME` 1000 · `BAD_HTTP_STATUS` 1001 · `HTTP_ERROR` 1002 ·
`TIMEOUT` 1003 · `MALFORMED_DATA_URI` 1004 · `REQUEST_FILTER_ERROR` 1006 ·
`RESPONSE_FILTER_ERROR` 1007 · `MALFORMED_TEST_URI` 1008 · `UNEXPECTED_TEST_REQUEST` 1009 ·
`ATTEMPTS_EXHAUSTED` 1010 · `SEGMENT_MISSING` 1011.

**2xxx TEXT** — `INVALID_TEXT_HEADER` 2000 · `INVALID_TEXT_CUE` 2001 ·
`UNABLE_TO_DETECT_ENCODING` 2003 · `BAD_ENCODING` 2004 · `INVALID_XML` 2005 ·
`INVALID_MP4_TTML` 2007 · `INVALID_MP4_VTT` 2008 · `UNABLE_TO_EXTRACT_CUE_START_TIME` 2009 ·
`INVALID_MP4_CEA` 2010 · `TEXT_COULD_NOT_GUESS_MIME_TYPE` 2011 ·
`CANNOT_ADD_EXTERNAL_TEXT_TO_SRC_EQUALS` 2012 · `TEXT_ONLY_WEBVTT_SRC_EQUALS` 2013 ·
`MISSING_TEXT_PLUGIN` 2014 · `UNSUPPORTED_EXTERNAL_THUMBNAILS_URI` 2017.

**3xxx MEDIA** — `BUFFER_READ_OUT_OF_BOUNDS` 3000 · `JS_INTEGER_OVERFLOW` 3001 · `EBML_OVERFLOW` 3002 ·
`EBML_BAD_FLOATING_POINT_SIZE` 3003 · `MP4_SIDX_WRONG_BOX_TYPE` 3004 ·
`MP4_SIDX_INVALID_TIMESCALE` 3005 · `MP4_SIDX_TYPE_NOT_SUPPORTED` 3006 ·
`WEBM_CUES_ELEMENT_MISSING` 3007 · `WEBM_EBML_HEADER_ELEMENT_MISSING` 3008 ·
`WEBM_SEGMENT_ELEMENT_MISSING` 3009 · `WEBM_INFO_ELEMENT_MISSING` 3010 ·
`WEBM_DURATION_ELEMENT_MISSING` 3011 · `WEBM_CUE_TRACK_POSITIONS_ELEMENT_MISSING` 3012 ·
`WEBM_CUE_TIME_ELEMENT_MISSING` 3013 · `MEDIA_SOURCE_OPERATION_FAILED` 3014 ·
`MEDIA_SOURCE_OPERATION_THREW` 3015 · `VIDEO_ERROR` 3016 · `QUOTA_EXCEEDED_ERROR` 3017 ·
`TRANSMUXING_FAILED` 3018 · `CONTENT_TRANSFORMATION_FAILED` 3019 · `TRANSMUXING_NO_VIDEO_DATA` 3023 ·
`STREAMING_NOT_ALLOWED` 3024 · `BUFFER_WRITE_OUT_OF_BOUNDS` 3025.

v5.0 note: `MEDIA_SOURCE_OPERATION_THREW` (3015) now includes media-element error details in
`error.data[1]`, or a brief explanation string.

**4xxx MANIFEST** — `UNABLE_TO_GUESS_MANIFEST_TYPE` 4000 · `DASH_INVALID_XML` 4001 ·
`DASH_NO_SEGMENT_INFO` 4002 · `DASH_EMPTY_ADAPTATION_SET` 4003 · `DASH_EMPTY_PERIOD` 4004 ·
`DASH_WEBM_MISSING_INIT` 4005 · `DASH_UNSUPPORTED_CONTAINER` 4006 · `DASH_PSSH_BAD_ENCODING` 4007 ·
`DASH_NO_COMMON_KEY_SYSTEM` 4008 · `DASH_MULTIPLE_KEY_IDS_NOT_SUPPORTED` 4009 ·
`DASH_CONFLICTING_KEY_IDS` 4010 · `RESTRICTIONS_CANNOT_BE_MET` 4012 ·
`HLS_PLAYLIST_HEADER_MISSING` 4015 · `INVALID_HLS_TAG` 4016 · `HLS_INVALID_PLAYLIST_HIERARCHY` 4017 ·
`DASH_DUPLICATE_REPRESENTATION_ID` 4018 · `HLS_MULTIPLE_MEDIA_INIT_SECTIONS_FOUND` 4020 ·
`HLS_REQUIRED_ATTRIBUTE_MISSING` 4023 · `HLS_REQUIRED_TAG_MISSING` 4024 ·
`HLS_COULD_NOT_GUESS_CODECS` 4025 · `HLS_KEYFORMATS_NOT_SUPPORTED` 4026 ·
`DASH_UNSUPPORTED_XLINK_ACTUATE` 4027 · `DASH_XLINK_DEPTH_LIMIT` 4028 ·
`CONTENT_UNSUPPORTED_BY_BROWSER` 4032 · `CANNOT_ADD_EXTERNAL_TEXT_TO_LIVE_STREAM` 4033 ·
`NO_VARIANTS` 4036 · `PERIOD_FLATTENING_FAILED` 4037 · `INCONSISTENT_DRM_ACROSS_PERIODS` 4038 ·
`HLS_VARIABLE_NOT_FOUND` 4039 · `HLS_MSE_ENCRYPTED_MP2T_NOT_SUPPORTED` 4040 ·
`HLS_MSE_ENCRYPTED_LEGACY_APPLE_MEDIA_KEYS_NOT_SUPPORTED` 4041 · `NO_WEB_CRYPTO_API` 4042 ·
`CANNOT_ADD_EXTERNAL_THUMBNAILS_TO_LIVE_STREAM` 4045 · `AES_128_INVALID_IV_LENGTH` 4048 ·
`AES_128_INVALID_KEY_LENGTH` 4049 · `DASH_CONFLICTING_AES_128` 4050 · `DASH_UNSUPPORTED_AES_128` 4051 ·
`DASH_INVALID_PATCH` 4052 · `HLS_EMPTY_MEDIA_PLAYLIST` 4053 ·
`DASH_MSE_ENCRYPTED_LEGACY_APPLE_MEDIA_KEYS_NOT_SUPPORTED` 4054 ·
`CANNOT_ADD_EXTERNAL_CHAPTERS_TO_LIVE_STREAM` 4055 · `WEBTRANSPORT_NOT_AVAILABLE` 4056 ·
`WEBTRANSPORT_INITIALIZATION_FAILED` 4057 · `MSF_VOD_CONTENT_NOT_SUPPORTED` 4058 ·
`HLS_INVALID_KEY_IV_FOR_GCM` 4059 · `HLS_INVALID_GCM_SEGMENT` 4060 · `DASH_INVALID_JSON` 4061 ·
`MSF_NO_CATALOG` 4062 · `DASH_UNSUPPORTED_ESSENTIAL_PROPERTY` 4063 · `MSF_CATALOG_TIMEOUT` 4064.

**`NO_WEB_CRYPTO_API` (4042)** is the code an insecure origin produces for encrypted content, and it
is the practical "you are not on https" signal in a client.

**5xxx STREAMING** — `STREAMING_ENGINE_STARTUP_INVALID_STATE` 5006. *(The only code left in this
category at 5.2.3 — streaming failures surface as NETWORK or MEDIA codes routed through
`streaming.failureCallback`.)*

**6xxx DRM** — see `45-drm.md`.

**7xxx PLAYER** — `LOAD_INTERRUPTED` 7000 · `OPERATION_ABORTED` 7001 · `NO_VIDEO_ELEMENT` 7002 ·
`OBJECT_DESTROYED` 7003 · `CONTENT_NOT_LOADED` 7004 · `SRC_EQUALS_PRELOAD_NOT_SUPPORTED` 7005 ·
`PRELOAD_DESTROYED` 7006 · `QUEUE_INDEX_OUT_OF_BOUNDS` 7007.

**8xxx CAST** — `CAST_API_UNAVAILABLE` 8000 · `NO_CAST_RECEIVERS` 8001 · `ALREADY_CASTING` 8002 ·
`UNEXPECTED_CAST_ERROR` 8003 · `CAST_CANCELED_BY_USER` 8004 · `CAST_CONNECTION_TIMED_OUT` 8005 ·
`CAST_RECEIVER_APP_UNAVAILABLE` 8006.

**9xxx STORAGE** — see `50-offline-and-in-app-download.md`.

**10xxx ADS** — see `55-ads-vast-vmap-and-ima.md`.

> **5.2.2 fix worth knowing:** *"Fix duplicate error code 4058"* (#10372) — code 4058 was assigned
> **twice** before 5.2.2. If your telemetry holds 4058 events from ≤5.2.1, they may be two different
> errors, and any dashboard grouping on that code across the upgrade boundary is wrong.

## Reading `error.data`

Upstream's caveat: *"each type of error has its own data structure (or none at all), tread with
care"*. The two shapes worth relying on:

- `BAD_HTTP_STATUS` (1001): `data[1]` is the HTTP status; `data[4]` is the `RequestType`.
- `INDEXED_DB_ERROR` (9001): `data[0]` is the underlying error object.

**`data` for a network error contains the failing URI and its query string.** Never log or render the
whole error object (`42-media-url-trust-and-presigned.md`).

## The four error paths — you need all of them

```js
function handleError(error) {
  // 1. Native errors FIRST: shaka.util.Error is NOT instanceof Error.
  if (error instanceof Error) {
    reportCrash(error);            // Shaka crashed with an unhandled native error
    return;
  }
  // 2. Now it is a shaka.util.Error. Log code/category/severity ONLY.
  const {severity, category, code} = error;
  if (severity === shaka.util.Error.Severity.CRITICAL) {
    // Fatal: a new load() is required to reset the library.
    showFatalUi(code);
  } else {
    logNonFatal(code, category);
  }
}

const player = new shaka.Player();
await player.attach(video);

// (a) Errors AFTER load
player.addEventListener('error', (event) => handleError(event.detail));

// (b) Errors DURING load - the 'error' event does NOT cover these.
try {
  await player.load(url);
} catch (e) {
  handleError(e);
}

// (c) Streaming failures. Overriding this REPLACES the built-in live auto-retry.
//     Full policy: 35-unstable-networks-and-resilience.md
player.configure('streaming.failureCallback', (error) => { /* see 35- */ });

// (d) DRM failures
player.configure('drm.failureCallback', (error) => {
  if (error.code === shaka.util.Error.Code.LICENSE_REQUEST_FAILED) {
    error.handled = true;          // prevent fatal propagation
  }
});

// (e) Network retries - cancel a hopeless loop
player.getNetworkingEngine().addEventListener('retry', (event) => {
  const {code, data} = event.error || {};
  if (code === shaka.util.Error.Code.BAD_HTTP_STATUS &&
      Array.isArray(data) && data[1] === 404 &&
      data[4] === shaka.net.NetworkingEngine.RequestType.MANIFEST) {
    event.preventDefault();
  }
});

// (f) UI errors are a SEPARATE emitter.
controls.addEventListener('error', (event) => handleError(event.detail));
```

## Mapping a code to a user-facing message

Map on **code**, never on `message` — the compiled build's message is only `'Shaka Error <code>'`.
Keep the mapping in one table with an explicit default, so a code you have never seen still produces
a sensible message rather than an empty string. Message copy is `/alaa-ui-ux-design-system`
(`$alaa-ui-ux-design-system`), `references/35-ux-writing-and-microcopy.md`; failure-state design is
`references/15-designed-failure-states.md` there.

**Best practice.** Check `instanceof Error` *before* treating something as a `shaka.util.Error` —
Shaka designed the runtime prototype chain specifically to make that check meaningful.
**Common mistake.** Only listening to `player.addEventListener('error', …)`. Load-time failures reject
the `load()` promise and never reach that listener, so the most common failure in production —
a 404 or an unsupported manifest — is the one path with no handler.
