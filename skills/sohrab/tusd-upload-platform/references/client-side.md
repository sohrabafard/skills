# Client-Side tus Implementation

## Goal

Use the browser only for resumable upload transport. Keep authorization, backend selection, and business state in the application.

The recommended flow is:

1. the app asks your backend for an upload session,
2. the backend returns the allowed upload target, policy data, and correlation identifiers,
3. the browser starts `tus-js-client`,
4. the browser sends upload traffic through your gateway,
5. the app remains the source of truth for final asset state.

## Browser-Only Boundary

When Vue.js + Quasar + Vite is used:

- keep tus upload code in a browser-only composable or service,
- do not touch `window`, `File`, `Blob`, or local storage during SSR,
- register boot files with `server: false` when they initialize browser-only upload helpers,
- lazy-load upload UI when that reduces SSR coupling.

Use:

- `assets/client/useTusUpload.ts` for the composable,
- `assets/client/quasar.boot.uploads.ts` for Quasar boot registration,
- `assets/client/quasar.boot.sentry.ts` for a client-safe Sentry initialization example,
- `assets/client/quasar.config.snippet.ts` for the client-only boot and PWA notes.

## Upload Session Contract

Have the application issue an upload session before the browser starts tus traffic.

A good upload session includes:

- `endpoint` or a pre-created `uploadUrl`,
- application upload ID,
- correlation ID,
- allowed metadata fields,
- max upload size and target type,
- short-lived auth information if needed,
- expiration time,
- whether termination is allowed.

The browser should not derive tenant, target backend, or provider credentials on its own.

## Recommended `tus-js-client` Defaults

### Baseline defaults

Use these as the browser default unless the product needs a different trade-off:

- bounded `retryDelays`,
- `removeFingerprintOnSuccess: true`,
- `storeFingerprintForResuming` only when the browser can store URLs and the security model allows it,
- `findPreviousUploads()` plus `resumeFromPreviousUpload()` for resumability,
- client-generated per-request ID plus a stable per-upload correlation ID,
- `metadata` sourced from the app-issued upload session and normalized to strings.

### Retry policy

Treat these status classes as non-retryable by default in the browser:

- `401` or `403`: auth or permission failure,
- `404`: unknown upload resource,
- `410`: expired upload resource.

Handle them with product UX, not blind retries.

### Resume policy

Recommended default:

- resume within and across browser sessions when the gateway still enforces ownership,
- clear stored fingerprints on success,
- clear stored fingerprints on logout or tenant switch,
- disable cross-session resume for the highest-sensitivity products if local persistence is unacceptable.

### Creation-with-upload and parallel uploads

These are optional optimizations, not defaults.

Enable them only after end-to-end verification:

- `uploadDataDuringCreation` requires support from tusd, the gateway path, and any policy layers,
- `parallelUploads` requires full concatenation support and should only be enabled after performance measurement.

## Quasar + SSR Guidance

### Boot files

Place upload registration in a boot file only if it must be globally available.

When SSR is enabled, register it as client-only:

```ts
boot: [
  { path: 'uploads', server: false },
]
```

If upload logic is only used in a small area of the app, keep it as a local composable instead of a global boot dependency.

### Universal code rule

Any module imported by both server and browser must avoid browser-only APIs at module evaluation time.

That means:

- do not create `tus.Upload` instances outside browser event handlers or browser-only helpers,
- guard browser APIs with `typeof window !== 'undefined'`,
- avoid reading local storage during SSR render.

## Quasar + PWA Guidance

Treat service workers as a separate runtime that can break uploads if left generic.

Do not let the service worker:

- precache upload URLs,
- runtime-cache `/files/` or equivalent upload paths,
- intercept `PATCH`, `HEAD`, or `DELETE` upload traffic,
- rewrite upload failures into offline fallback pages.

If you register a custom service worker or PWA hooks, keep the upload origin and path out of caching rules.

## Sentry Guidance

Use Sentry for terminal exceptions and user-impacting failures, not for every progress event.

Recommended event hygiene:

- keep `onProgress` callback logic lightweight and exception-safe,
- tag by app upload ID, target type, and correlation ID,
- attach safe extra context such as file size bucket, retry count, and final HTTP status,
- scrub raw upload URLs and auth headers,
- keep filenames out unless the product allows them,
- initialize Sentry in a client-safe Quasar boot file when SSR is enabled.

## UX Guidance

Expose these states clearly in the UI:

- ready to upload,
- uploading,
- paused,
- retrying,
- completed,
- failed permanently,
- expired or permission revoked.

Map the common transport outcomes to product language:

- `401` or `403`: sign-in or permission problem,
- `404`: upload no longer exists,
- `409`: upload offset or state conflict,
- `410`: upload expired and must be restarted.

## Operational Checklist

Before calling the browser implementation production-ready, verify all of these:

- SSR pages do not import browser-only upload code on the server,
- PWA mode does not cache or intercept upload requests,
- resume works after refresh and after a short disconnect,
- non-retryable auth failures surface correctly to the user,
- raw upload URLs and auth material are absent from Sentry and browser logs,
- custom response headers that the UI needs are exposed through CORS,
- cancel behavior matches whether tus termination is enabled on the server.
