# Client-Side tus Implementation

## Goal

Use the browser only for resumable upload transport and user-facing upload UX. Keep authorization, backend selection, object keys, provider credentials, and final business state in the application/control plane.

For Vue-specific implementation, always read `references/vue-frontend.md` before generating code or reviewing frontend behavior.

## Recommended Flow

1. Vue calls the backend upload-session API through the gateway.
2. Backend validates trusted context and returns safe upload session fields.
3. Vue starts `tus-js-client` through the public gateway-facing endpoint.
4. Gateway enforces auth and ownership for creation, resume, offset, and termination methods.
5. Vue shows progress and upload completion.
6. Product UI polls or subscribes to application asset state until scanning, relay, or processing completes.

## Browser-Only Boundary

When Vue.js, Quasar, and Vite are used:

- keep tus upload code in browser-only composables, components, or boot files,
- do not touch `window`, `File`, `Blob`, `navigator`, or local storage during SSR,
- register Quasar boot files with `server: false` when they initialize upload helpers,
- lazy-load upload UI when that reduces SSR coupling,
- keep service workers away from upload routes.

Use:

- `assets/client/useTusUpload.ts` for the Vue composable,
- `assets/client/useUploadQueueStore.ts` for a Pinia-style multi-upload queue,
- `assets/client/TusUploadPanel.vue` for a Vue single-file component example,
- `assets/client/uploadTelemetry.ts` for safe telemetry helpers,
- `assets/client/quasar.boot.uploads.ts` for Quasar boot registration,
- `assets/client/quasar.boot.sentry.ts` for client-safe Sentry redaction,
- `assets/client/quasar.config.snippet.ts` for client-only boot and PWA notes.

## tus-js-client Defaults

Use these defaults unless product or infrastructure constraints require a different trade-off:

- explicit bounded `retryDelays`,
- `removeFingerprintOnSuccess: true`,
- `storeFingerprintForResuming` only when `tus.canStoreURLs` is true and the security model allows local URL storage,
- `findPreviousUploads()` plus `resumeFromPreviousUpload()` for resumability,
- per-request `X-Request-Id`,
- safe metadata from the app-issued upload session and normalized to strings,
- no `parallelUploads` unless concatenation support and gateway behavior have been tested,
- no custom `chunkSize` unless a server/proxy/body-size limit or stream input requires it.

## Retry and Resume Policy

Treat these as non-retryable by default:

- `401` and `403`: auth or permission failure,
- `404`: unknown upload resource,
- `410`: expired upload resource.

Allow bounded retry for transient network failures, `409` offset conflicts, and `423` lock-style responses when tus-js-client and server behavior are verified.

Clear stored upload URLs on success, logout, account switch, and project switch.

## UX Guidance

Expose states clearly:

- ready to upload,
- creating upload session,
- uploading,
- paused,
- retrying,
- tus upload completed,
- processing final asset,
- final asset ready,
- failed permanently,
- expired or permission revoked,
- cancelled.

Do not equate tus completion with final asset readiness when server-side scan, relay, transcode, or provider registration still runs.

## Operational Checklist

Before calling the browser implementation production-ready, verify:

- SSR pages do not import browser-only upload code on the server path,
- PWA mode does not cache or intercept upload requests,
- resume works after refresh and short disconnect,
- auth failures surface correctly without infinite retries,
- raw upload URLs and auth material are absent from Sentry and browser logs,
- CORS exposes the headers the UI needs,
- cancel behavior matches whether tus termination is enabled on the server,
- UI has a safe path from upload completion to final asset readiness.
