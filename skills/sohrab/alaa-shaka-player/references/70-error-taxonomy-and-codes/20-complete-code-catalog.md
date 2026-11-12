For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

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
`HLS_INVALID_KEY_IV_FOR_GCM` 4059 · `HLS_INVALID_GCM_SEGMENT` 4060 · ~~`DASH_INVALID_JSON` 4061~~ *(removed in 5.3.0)* ·
~~`MSF_NO_CATALOG` 4062~~ *(removed in 5.3.0)* · `DASH_UNSUPPORTED_ESSENTIAL_PROPERTY` 4063 · `MSF_CATALOG_TIMEOUT` 4064 ·
`MSF_CONNECTION_CLOSED` 4065 · `MSF_SUBSCRIBE_FAILED` 4066 · `MSF_UNSUPPORTED_COMPRESSION` 4067 ·
`MSF_UNSUPPORTED_CATALOG_VERSION` 4068 · `MKV_INVALID_FILE` 4069 · `MKV_MISSING_INDEX` 4070 ·
`MKV_NO_SUPPORTED_TRACKS` 4071 *(4065 to 4071 are absent at 5.2.13 and present at 5.3.4; see "Changes in 5.3" below)*.

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

## Changes in 5.3 (read 2026-11-12)

Do not reuse codes 4061 and 4062 for new meanings in your own tables. Shaka marks both `RETIRED` in
`lib/util/error.js` at 5.3.4 (npm tarball `shaka-player@5.3.4`, local read).

| Code | Name | Status | Source |
|---|---|---|---|
| 4061 | `DASH_INVALID_JSON` | Removed. The DASH JSON support left the experimental build ([#10705](https://github.com/shaka-project/shaka-player/issues/10705)). | [CHANGELOG at v5.3.4](https://github.com/shaka-project/shaka-player/blob/v5.3.4/CHANGELOG.md), 5.3.0 section |
| 4062 | `MSF_NO_CATALOG` | Removed. The reason is not stated upstream. The `.d.ts` diff 5.2.13 to 5.3.4 shows the removal. | `lib/util/error.js` at tag v5.3.0 marks it `RETIRED` (read 2026-11-12) |
| 4065 | `MSF_CONNECTION_CLOSED` | Added. MoQT session ended before load finished. `data[0]` is the reason. | `error.js` at 5.3.4 |
| 4066 | `MSF_SUBSCRIBE_FAILED` | Added. Publisher refused a needed track. `data[0]` track name, `data[1]` reason. | `error.js` at 5.3.4 |
| 4067 | `MSF_UNSUPPORTED_COMPRESSION` | Added. Payload compression is unsupported (GZIP needs `DecompressionStream`). `data[0]` is the compression value. | `error.js` at 5.3.4 |
| 4068 | `MSF_UNSUPPORTED_CATALOG_VERSION` | Added. `data[0]` is the declared version. | `error.js` at 5.3.4 |
| 4069 | `MKV_INVALID_FILE` | Added. Not a valid Matroska or WebM file. `data[0]` is the URI. | `error.js` at 5.3.4 |
| 4070 | `MKV_MISSING_INDEX` | Added. No Cues element, so byte-range seeking is impossible. `data[0]` is the URI. | `error.js` at 5.3.4 |
| 4071 | `MKV_NO_SUPPORTED_TRACKS` | Added. No playable track, for example DTS only. `data[0]` is the URI. | `error.js` at 5.3.4 |

All seven are defined in `lib/util/error.js` at tag v5.3.0 (read 2026-11-12). MKV is experimental-build
only (CHANGELOG 5.3.0, #10667). MSF appears experimental-only too: `moqt` and `matroska` strings occur in
`dist/shaka-player.experimental.js` but not in `dist/shaka-player.ui.js` at 5.3.4 (local grep, not
upstream). A standard UI-bundle consumer should not see 4065 to 4071 (inferred from the experimental-only scope).
