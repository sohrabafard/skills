Version-sensitive claims in this topic depend on [Shaka provenance and freshness](../05-provenance-and-freshness.md).

## The player never appears, or crashes on the server

| Symptom | Cause | Fix |
|---|---|---|
| `window is not defined`, `HTMLMediaElement is not defined`, `document is not defined` in an SSR build | Shaka imported at module top level | Dynamic `import()` inside `onMounted`. Nothing under `src/boot/` imports Shaka. `../11-vue-quasar-binding.md` |
| `shaka is not defined` at runtime, or `shaka.ui is undefined` | Imported the package `main`, which is the **non-UI** build; or expected named ESM exports, which do not exist | Import `shaka-player/dist/shaka-player.ui.js` explicitly and unwrap `.default`. `../12-bundling-and-vite-loading.md` |
| TypeScript accepts `shaka.ui.Overlay` but it is `undefined` at runtime | `"types"` resolves to the **non-UI** `.d.ts` (conflict C8) | Reference `dist/shaka-player.ui.d.ts` or add an ambient declaration. `12-…` |
| Proxy-shaped failures at load time; internal Shaka values are Proxies | The Player was made reactive | Hold it in a closure-scoped `let`. `../11-vue-quasar-binding.md` |
## Playback fails to start

| Symptom | Code | Fix |
|---|---|---|
| `load()` rejects and nothing reaches the `error` listener | – | Load-time failures reject the promise. You need **both** paths. `../70-error-taxonomy-and-codes.md` |
| Manifest 404 / 5xx | `BAD_HTTP_STATUS` 1001, `HTTP_ERROR` 1002 | Check `data[1]` (status) and `data[4]` (RequestType). Cancel a hopeless VOD 404 loop via the `retry` event. `35-…` |
| Manifest type not recognised | `UNABLE_TO_GUESS_MANIFEST_TYPE` 4000 | Pass `mimeType` to `load()`. `22-…` |
| `chunk demuxer append failed` on HLS | `HLS_COULD_NOT_GUESS_CODECS` 4025 nearby | HLS without `CODECS` makes Shaka guess `avc1.42E01E` + `mp4a.40.2`, breaking audio-only and video-only streams. Fix the manifest or tune `manifest.hls.*`. `22-…` |
| Nothing plays and the track list is empty | `RESTRICTIONS_CANNOT_BE_MET` 4012, `NO_VARIANTS` 4036 | A **top-level** `restrictions` is hard and removes tracks. Use `abr.restrictions`. `24-…` |
| Encrypted content fails on `http://` | `NO_WEB_CRYPTO_API` 4042, `REQUESTED_KEY_SYSTEM_CONFIG_UNAVAILABLE` 6001 | EME requires a secure origin. `75-…`, `../45-drm.md` |
| CORS preflight fails after adding a header in a filter | `HTTP_ERROR` 1002 | The custom header must be in `Access-Control-Allow-Headers`. `40-…` |
| A filter throws | `REQUEST_FILTER_ERROR` 1006, `RESPONSE_FILTER_ERROR` 1007 | Wrap anything that can fail and decide deliberately whether to fail the request. `40-…` |
