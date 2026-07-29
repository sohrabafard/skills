# The networking engine, request and response filters

All rows `verified` at v5.2.3, read 2026-07-28, from `lib/net/networking_engine.js` and
`externs/shaka/net.js` unless stated.

## API surface

| Name | Notes |
|---|---|
| `player.getNetworkingEngine()` | → `shaka.net.NetworkingEngine`. One engine for manifests, segments, licences and more. |
| `storage.getNetworkingEngine()` | Offline `Storage` has its **own** engine. Filters on the Player's engine do **not** apply to downloads. |
| `registerRequestFilter(f)` / `unregisterRequestFilter(f)` / `clearAllRequestFilters()` | |
| `registerResponseFilter(f)` / `unregisterResponseFilter(f)` / `clearAllResponseFilters()` | |
| `NetworkingEngine.registerScheme(scheme, plugin, priority, progressSupport = false)` / `unregisterScheme(scheme)` | Statics. |
| `NetworkingEngine.defaultRetryParameters()` / `makeRequest(uris, retryParams, streamDataCallback = null)` | Statics. |
| `engine.request(type, request, context)` | → `IAbortableOperation<Response>`; use `.promise`. |
| `engine.configure(config)` / `destroy()` / `clearCommonAccessTokenMap()` | |

## `RequestType` and `AdvancedRequestType` — exact enums

`shaka.net.NetworkingEngine.RequestType`: `MANIFEST: 0`, `SEGMENT: 1`, `LICENSE: 2`, `APP: 3`,
`TIMING: 4`, `SERVER_CERTIFICATE: 5`, `KEY: 6`, `ADS: 7`, `CONTENT_STEERING: 8`, `CMCD: 9`,
`SESSION_DATA: 10`, `FINGERPRINT: 11`, `PLAYLIST: 12`, `EVENT_CALLBACK: 13`.

`shaka.net.NetworkingEngine.AdvancedRequestType`: `INIT_SEGMENT: 0`, `MEDIA_SEGMENT: 1`,
`MEDIA_PLAYLIST: 2`, `MASTER_PLAYLIST: 3`, `MPD: 4`, `// RETIRED: 'MSS': 5`, `MPD_PATCH: 6`,
`MEDIATAILOR_SESSION_INFO: 7`, `MEDIATAILOR_TRACKING_INFO: 8`, `MEDIATAILOR_STATIC_RESOURCE: 9`,
`MEDIATAILOR_TRACKING_EVENT: 10`, `INTERSTITIAL_ASSET_LIST: 11`, `INTERSTITIAL_AD_URL: 12`,
`TRACKING_EVENT: 13`.

Use `RequestType.APP` for your own side-band requests through the engine, so they inherit the retry
and abort machinery.

## Mutable request and response fields

`shaka.extern.Request`: **`uris: Array<string>`** (tried in order), `method`, `body: ?BufferSource`,
`headers: Object<string,string>`, `allowCrossSiteCredentials: boolean`, `retryParameters`,
`licenseRequestType`, `sessionId`, `drmInfo`, `initData`, `initDataType`, `streamDataCallback`,
`requestStartTime`, `timeToFirstByte`, `packetNumber`, `contentType`, **`attempt: number` (0-based)**.

`shaka.extern.Response`: `uri`, `originalUri` (*"before any redirects, but after request filters are
executed"*), `data`, `status`, `headers` (**all keys lowercased**; *"For HTTP/HTTPS, may not be
available cross-origin"*), `timeMs`, `fromCache` (*"If true… should be ignored for bandwidth
estimation"*), `originalRequest`.

`shaka.extern.RequestContext`: `type` (an `AdvancedRequestType`), `stream`, `segment`, `isPreload`.

## Filters may be asynchronous, and run per attempt

Verbatim from `externs/shaka/net.js`:

> *"A request filter can run asynchronously by returning a promise; in this case, the request will not
> be sent until the promise is resolved. **If a request is attempted multiple times, this filter will
> be called for each attempt. You can check the `attempt` parameter on the request object to see which
> attempt this filter is being called on.**"*

> *"A response filter can run asynchronously by returning a promise."*

```js
// shaka.extern.RequestFilter
function(shaka.net.NetworkingEngine.RequestType,
         shaka.extern.Request,
         shaka.extern.RequestContext=): (Promise|undefined)

// shaka.extern.ResponseFilter — same shape with shaka.extern.Response
```

Async filter support has existed **since v2.1.0**. The **per-attempt** invocation is a **v5.0** change
(`docs/tutorials/license-server-auth.md`: *"The request filter is called on every request attempt
since v5.0, so you can update the credentials if needed."*). **This is the hook for refreshing an
expired credential mid-retry, and it is why a filter must read a token getter rather than capture a
token value.**

## How a filter interacts with retries

| Fact | Basis |
|---|---|
| The filter runs once **per attempt**, not once per logical request. | `externs/shaka/net.js` |
| `request.attempt` is 0-based and incremented by the engine before re-sending. | `networking_engine.js` L716 |
| On retry the engine also **moves to the next URI** in `request.uris`. | L715–719 |
| **5.2.2 fix: "net: isolate headers across retry attempts" (#10361)** — headers mutated by a filter on attempt N no longer leak into attempt N+1. Anyone relying on the old leaky behaviour changed silently on upgrade (open question 10). | CHANGELOG 5.2.2 |
| The `retry` event fires between attempts and is cancelable. | L704–713; `35-unstable-networks-and-resilience.md` |
| `networking.forceHTTP` / `forceHTTPS` rewrite the scheme engine-side (moved from `streaming.*` in v5.0). **`forceHTTPS` wins if both are set.** | `NetworkingConfiguration` |

## Failure modes

A throwing request filter surfaces as `REQUEST_FILTER_ERROR` (1006); a throwing response filter as
`RESPONSE_FILTER_ERROR` (1007). Other network codes: `UNSUPPORTED_SCHEME` 1000, `BAD_HTTP_STATUS`
1001, `HTTP_ERROR` 1002, `TIMEOUT` 1003, `MALFORMED_DATA_URI` 1004, `ATTEMPTS_EXHAUSTED` 1010,
`SEGMENT_MISSING` 1011. For `BAD_HTTP_STATUS`, `data[1]` is the HTTP status and `data[4]` is the
`RequestType`.

**A filter that throws breaks the request.** Wrap anything that can fail — a token fetch, a JSON parse
— and decide deliberately whether to fail the request or continue unauthenticated.

## Working snippet — auth, rewrite, and retry-aware refresh

```js
const net = player.getNetworkingEngine();
const RequestType = shaka.net.NetworkingEngine.RequestType;

// ---- 1. Read a token GETTER, never a captured value.
//         A captured token is fixed at registration time and can never refresh. ----
let tokenProvider = { get: async () => currentAccessToken() };

// ---- 2. Static header on licence requests ----
net.registerRequestFilter(async (type, request) => {
  if (type !== RequestType.LICENSE) return;
  request.headers['Authorization'] = 'Bearer ' + (await tokenProvider.get());
});

// ---- 3. URL rewrite. `uris` is an ARRAY: fallbacks are tried in order on retry,
//         so rewriting only uris[0] breaks the fallback chain. ----
net.registerRequestFilter((type, request) => {
  if (type !== RequestType.SEGMENT && type !== RequestType.MANIFEST) return;
  request.uris = request.uris.map((u) =>
      u.replace('https://origin.example.com/', 'https://cdn.example.com/'));
});

// ---- 4. Retry-aware credential refresh: the v5 pattern. ----
let sawLicenceAuthFailure = false;
net.addEventListener('retry', (event) => {
  const {code, data} = event.error || {};
  if (code === shaka.util.Error.Code.BAD_HTTP_STATUS &&
      Array.isArray(data) && data[1] === 401 && data[4] === RequestType.LICENSE) {
    sawLicenceAuthFailure = true;
  }
});
net.registerRequestFilter(async (type, request) => {
  if (type !== RequestType.LICENSE) return;
  // request.attempt is 0-based; > 0 means this is a retry.
  if (sawLicenceAuthFailure && request.attempt > 0) {
    await refreshAuthToken();          // the refresh happens HERE, not in component state
    sawLicenceAuthFailure = false;
  }
  request.headers['Authorization'] = 'Bearer ' + (await tokenProvider.get());
});

// ---- 5. Response filter, unwrapping a licence envelope ----
net.registerResponseFilter(async (type, response) => {
  if (type !== RequestType.LICENSE) return;
  try {
    const json = JSON.parse(shaka.util.StringUtils.fromUTF8(response.data));
    response.data = shaka.util.Uint8ArrayUtils.fromBase64(json.license).buffer;
  } catch (e) {
    // A throw here becomes RESPONSE_FILTER_ERROR (1007). Decide deliberately.
    throw e;
  }
});

// ---- 6. Cookies cross-origin ----
net.registerRequestFilter((type, request) => {
  if (type === RequestType.LICENSE) request.allowCrossSiteCredentials = true;
});

// ---- 7. A custom scheme (for example file:// under Electron) ----
shaka.net.NetworkingEngine.registerScheme('file', shaka.net.HttpXHRPlugin.parse);

// ---- 8. Offline downloads need their OWN filters: Storage has a separate engine. ----
const storage = new shaka.offline.Storage(player);
storage.getNetworkingEngine().registerRequestFilter(async (type, request) => {
  request.headers['Authorization'] = 'Bearer ' + (await tokenProvider.get());
});
```

CORS: cross-origin manifest, segment and licence requests need the usual
`Access-Control-Allow-Origin`, and any custom header you add here must appear in
`Access-Control-Allow-Headers` or the preflight fails before Shaka ever sees a response. Mixed content
(an `https` page fetching `http` segments) is blocked by the browser, not by Shaka —
`networking.forceHTTPS` rewrites the scheme rather than diagnosing it.

**Best practice.** Register every filter **before** `load()`, keep exactly one filter per concern, and
give each one a named function so `unregisterRequestFilter` can remove it. Treat `request.uris` as the
array it is.
**Common mistake.** Registering filters on `player.getNetworkingEngine()` and finding that offline
downloads return 401. `Storage` has a separate engine; the `store()` JSDoc even notes *"multiple
storage objects will be necessary if some assets require unique network filters."*
