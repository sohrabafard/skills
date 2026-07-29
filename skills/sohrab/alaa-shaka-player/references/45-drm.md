# DRM: Widevine, PlayReady, FairPlay

All rows `verified` at v5.2.3, read 2026-07-28.

## Current position

Key systems are configured through `drm.servers` (keyed by key-system id) and `drm.advanced`
(per-key-system detail). Licence wrapping uses ordinary request/response filters on
`RequestType.LICENSE`. FairPlay helpers live in `shaka.drm.FairPlay` (moved from
`shaka.util.FairPlayUtils` in v5.0). **Robustness fields are `Array<string>` since v5.0** — a bare
string carried forward from v4 will not be interpreted as you expect.

**EME requires a secure origin.** The most common cause of `REQUESTED_KEY_SYSTEM_CONFIG_UNAVAILABLE`
(6001) is, per the FAQ, *"that you are not using a secure origin"*.

## `drm.*` configuration

| Key | Default | Note |
|---|---|---|
| `drm.servers` | `{}` | key-system id → licence URL |
| `drm.clearKeys` | `{}` | keyId → key (hex or base64). **Forces the Clear Key CDM.** Debug only; *"does not provide actual content security."* |
| `drm.advanced` | `{}` | per key system, see below |
| `drm.retryParameters` | see `35-…` | identical structure to the other two budgets |
| `drm.delayLicenseRequestUntilPlayed` | `false` | |
| `drm.persistentSessionOnlinePlayback` | `false` | Try given persistent session ids before requesting a licence, and keep the session at stop. |
| `drm.persistentSessionsMetadata` | `[]` | |
| `drm.initDataTransform` | no-op since v4.0 | `function(Uint8Array, string, ?DrmInfo): Uint8Array` |
| `drm.logLicenseExchange` | `false` | **Debug builds only, no effect in release.** Never enable in production: it logs licence traffic. |
| `drm.updateExpirationTime` | `1` s | |
| `drm.preferredKeySystems` | `['com.microsoft.playready']` on **Xbox One and PlayStation 4**, `[]` elsewhere | |
| `drm.keySystemsMapping` | `{}` | |
| `drm.parseInbandPsshEnabled` | `true` on **Xbox One**, `false` elsewhere | *"required when using in-band key rotation on Xbox One"*. When true, Shaka parses PSSH from media and init segments **and ignores `encrypted` events**. |
| `drm.minHdcpVersion` | `''` (no check) | |
| `drm.ignoreDuplicateInitData` | `false` on **Tizen 2**, `true` elsewhere | Tizen 2015/2016 send duplicate `webkitneedkey` events; suppressing them stalls playback. |
| `drm.defaultAudioRobustnessForWidevine` | `'SW_SECURE_CRYPTO'`, **`''` on Android** | |
| `drm.defaultVideoRobustnessForWidevine` | `'SW_SECURE_DECODE'`, **`''` on Android** | |
| `drm.renewalIntervalSec` | `0` (off) | **PlayReady and FairPlay only — Widevine is not supported.** |
| `drm.failureCallback` | no-op | Set `error.handled = true` to stop propagation. See `35-…`. |
| `manifest.ignoreDrmInfo` | `false` | Make the parser pretend the manifest signalled no key system. |

`shaka.extern.AdvancedDrmConfiguration`:

| Field | Default | Note |
|---|---|---|
| `distinctiveIdentifierRequired` | `false` | |
| `persistentStateRequired` | `false` | **Must be `true` for persistent (offline) licences.** |
| `videoRobustness` | `[]` | **`Array<string>` since v5.0** (was a string in ≤4.13). Priority order. |
| `audioRobustness` | `[]` | same |
| `serverCertificate` | `null` | `Uint8Array`; empty (`byteLength == 0`) is treated as `null`. |
| `serverCertificateUri` | `''` | Ignored if `serverCertificate` is set. |
| `individualizationServer` | `''` | Defaults to the licence server. |
| `sessionType` | `'temporary'` | *"This doesn't affect offline storage."* |
| `headers` | `{}` | Licence-request headers — an alternative to a request filter. |

## Support matrix (upstream's own table)

| Browser | Widevine | PlayReady | FairPlay | WisePlay | ClearKey |
|---|---|---|---|---|---|
| Chrome¹ | Y | – | – | – | Y |
| Firefox² | Y | – | – | – | Y |
| Edge (legacy)³ | – | Y | – | – | – |
| Edge Chromium | Y | Y | – | – | Y |
| **Safari** | – | – | **Y** | – | – |
| Opera | Y | – | – | – | Y |
| Chromecast | Y | Y | – | – | Y |
| Tizen TV | Y | Y | – | – | Y |
| WebOS / Hisense / Vizio / Titan / TiVo | untested⁷ | untested⁷ | – | – | untested⁷ |
| Xbox One | – | Y | – | – | – |
| PlayStation 4 / 5 | – | untested⁷ | – | – | untested⁷ |
| Huawei | – | – | – | untested⁷ | untested⁷ |

Notes, verbatim: ¹ *"Only official Chrome builds contain the Widevine CDM. Chromium built from source
does not support DRM."* ² *"DRM must be enabled by the user. The first time a Firefox user visits a
site with encrypted media, the user will be prompted to enable DRM."* ³ *"PlayReady in Edge does not
seem to work on a VM or over Remote Desktop."* ⁷ *"expected to work, but are community-supported and
untested by us."*

DASH supports all five key systems; HLS supports all five, with the note *"By default, FairPlay is
handled using Apple's native HLS player, when on Safari. We do support FairPlay through MSE/EME,
however. See the `streaming.useNativeHlsForFairPlay` configuration value."*

## FairPlay specifics

| Fact | Note |
|---|---|
| Modern EME key system: **`com.apple.fps`**. Legacy Apple Media Keys: **`com.apple.fps.1_0`**. | |
| Support matrix: `src=` CMAF ✔ both; `src=` TS ✔ both; **MSE CMAF ✔ Modern EME only**; **MSE TS ✘ both**. | |
| Legacy path: `shaka.polyfill.PatchedMediaKeysApple.install()`; `install(true)` enables `uninstall()` for mixed-provider apps. | |
| **All FairPlay content requires a server certificate** — `serverCertificate` or `serverCertificateUri`. | |
| Config-key escaping for a dotted key-system id: `player.configure('drm.advanced.com\\.apple\\.fps.serverCertificateUri', url)`. | |
| Helpers under `shaka.drm.FairPlay`: `initDataTransform`, `defaultGetContentId`, `ezdrmFairPlayRequest`, `ezdrmInitDataTransform`, `commonFairPlayResponse`. | |
| For FairPlay, `initData` is a buffer containing an `skd://` URL as UTF-8; `drmInfo.keySystemUris` holds the SKD URI set. | |
| **5.2.0:** *"HLS: Allow encrypted MSE playback with legacy Apple MediaKeys"*. Codes 4041 and 4054 exist for the unsupported combinations. | |

## Error codes, category 6

`NO_RECOGNIZED_KEY_SYSTEMS` 6000 · `REQUESTED_KEY_SYSTEM_CONFIG_UNAVAILABLE` 6001 ·
`FAILED_TO_CREATE_CDM` 6002 · `FAILED_TO_ATTACH_TO_VIDEO` 6003 · `INVALID_SERVER_CERTIFICATE` 6004 ·
`FAILED_TO_CREATE_SESSION` 6005 · `FAILED_TO_GENERATE_LICENSE_REQUEST` 6006 ·
`LICENSE_REQUEST_FAILED` 6007 · `LICENSE_RESPONSE_REJECTED` 6008 ·
`ENCRYPTED_CONTENT_WITHOUT_DRM_INFO` 6010 · `NO_LICENSE_SERVER_GIVEN` 6012 ·
`OFFLINE_SESSION_REMOVED` 6013 · `EXPIRED` 6014 · `SERVER_CERTIFICATE_REQUIRED` 6015 ·
`INIT_DATA_TRANSFORM_ERROR` 6016 · `SERVER_CERTIFICATE_REQUEST_FAILED` 6017 ·
`MIN_HDCP_VERSION_NOT_MATCH` 6018 · `ERROR_CHECKING_HDCP_VERSION` 6019 · `MISSING_EME_SUPPORT` 6020.

FAQ guidance: **6004** — *"You need to get the license certificate from your DRM provider. This is
**not** the HTTPS certificate of the proxy."* **6008** — *"Check the DevTools network tab for the
response."* **6001** — check the origin is secure first.

## Introspection

`player.keySystem()`, `player.drmInfo()`, `player.getExpiration()`,
`player.getActiveSessionsMetadata()` (→ `Array<shaka.extern.DrmSessionMetadata>` with `sessionId`,
`sessionType`, `initData`, `initDataType`), `player.getKeyStatuses()`, `player.renewLicense(sessionId)`,
`player.retryLicensing(sessionMetadata, retryDelaySeconds)`. Events: `drmsessionupdate`,
`expirationupdated`, `keystatuschanged`. `shaka.Player.probeSupport()` returns
`shaka.extern.SupportType`, whose DRM entries carry `persistentState`, `encryptionSchemes`,
`videoRobustnessLevels`, `audioRobustnessLevels`, `minHdcpVersions`.

## Working snippet — multi-DRM with wrapping and persistence

```js
player.configure({
  drm: {
    servers: {
      'com.widevine.alpha':      'https://drm.example.com/wv',
      'com.microsoft.playready': 'https://drm.example.com/pr',
      'com.apple.fps':           'https://drm.example.com/fps',
    },
    advanced: {
      'com.widevine.alpha': {
        // ARRAYS since v5.0, in priority order. A bare string will not work as intended.
        videoRobustness: ['HW_SECURE_ALL', 'HW_SECURE_DECODE', 'SW_SECURE_DECODE'],
        audioRobustness: ['HW_SECURE_CRYPTO', 'SW_SECURE_CRYPTO'],
        persistentStateRequired: false,     // MUST be true for offline licences
        sessionType: 'temporary',
      },
      'com.microsoft.playready': { videoRobustness: ['3000', '2000'] },
      'com.apple.fps': {
        // FairPlay ALWAYS needs a server certificate.
        serverCertificateUri: 'https://drm.example.com/fps.cer',
      },
    },
    preferredKeySystems: ['com.widevine.alpha', 'com.microsoft.playready'],
    retryParameters: {maxAttempts: 4, baseDelay: 500, backoffFactor: 2, fuzzFactor: 0.5,
                      timeout: 20000, stallTimeout: 5000, connectionTimeout: 8000},
    updateExpirationTime: 1,
    logLicenseExchange: false,              // never true in a shipped build
    failureCallback: (error) => {
      if (error.code === shaka.util.Error.Code.LICENSE_REQUEST_FAILED) {
        error.handled = true;               // not fatal; we retry ourselves (35-...)
      }
    },
  },
});

// Escaped dots for a dotted key-system id in the string form:
player.configure('drm.advanced.com\\.apple\\.fps.serverCertificateUri',
                 'https://drm.example.com/fps.cer');

// Licence wrapping. The token is read from a GETTER (42-media-url-trust-and-presigned.md).
const net = player.getNetworkingEngine();
const T = shaka.net.NetworkingEngine.RequestType;

net.registerRequestFilter(async (type, request) => {
  if (type !== T.LICENSE) return;
  request.headers['Content-Type'] = 'application/octet-stream';
  request.headers['Authorization'] = 'Bearer ' + (await getToken());
});

net.registerResponseFilter((type, response) => {
  if (type !== T.LICENSE) return;
  // e.g. unwrap {"license":"<base64>"}
  const json = JSON.parse(shaka.util.StringUtils.fromUTF8(response.data));
  response.data = shaka.util.Uint8ArrayUtils.fromBase64(json.license).buffer;
});

await player.load(uri);
reportDrmSession(player.keySystem(), player.getExpiration());   // not drmInfo(): it can carry URIs
```

**Best practice.** Set `persistentStateRequired: true` in `drm.advanced.<keySystem>` **before**
attempting offline storage with a persistent licence; without it the CDM will not grant one. Probe
with `shaka.Player.probeSupport()` and `shaka.offline.Storage.support()` rather than assuming from the
browser name.
**Common mistake.** Carrying `videoRobustness: 'HW_SECURE_ALL'` forward from v4 as a bare string.
Since v5.0 these fields are `Array<string>`, and the resulting configuration silently does not request
the robustness you think it does.
