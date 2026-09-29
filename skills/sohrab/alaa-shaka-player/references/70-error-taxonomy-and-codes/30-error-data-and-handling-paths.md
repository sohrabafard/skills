For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

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
  // 2. Rejections can also be null or primitive values; do not assume a Shaka error.
  if (error === null || typeof error !== 'object' || !Number.isFinite(error.code)) {
    showGenericPlaybackFailure();
    return;
  }
  // A code-bearing object: log code/category/severity ONLY.
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
