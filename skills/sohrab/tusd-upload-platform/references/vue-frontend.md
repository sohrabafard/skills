# Vue Frontend Integration

## Contents

- [Goal](#goal)
- [Package and Runtime](#package-and-runtime)
- [Upload Session Contract](#upload-session-contract)
- [Vue Composition Pattern](#vue-composition-pattern)
- [Pinia Queue Pattern](#pinia-queue-pattern)
- [Quasar and SSR](#quasar-and-ssr)
- [PWA and Service Worker](#pwa-and-service-worker)
- [Retry and Resume](#retry-and-resume)
- [Parallel Uploads](#parallel-uploads)
- [Metadata](#metadata)
- [UX States](#ux-states)
- [Telemetry](#telemetry)
- [Review Checklist](#review-checklist)

## Goal

Vue is a first-class part of the upload platform. The frontend owns user interaction, file selection, progress, pause/resume/cancel controls, and safe telemetry. It does not own authorization truth, tenant identity, storage routing, object keys, provider credentials, or final asset state.

## Package and Runtime

Use `tus-js-client` from npm in Vite/Quasar projects. Import it only in browser-safe modules or in code paths that cannot run during SSR. The official client supports browser environments and exposes `tus.isSupported` and `tus.canStoreURLs`; use both checks before enabling resumable UI.

Recommended package baseline:

```bash
npm install tus-js-client
```

For production, pin the installed version in lockfiles and re-check official release notes before major upgrades. Treat prereleases as test-only unless the product explicitly accepts upgrade risk.

## Upload Session Contract

The frontend should call a backend session endpoint before creating a tus upload. The response should include:

- `endpoint` or `uploadUrl`
- `appUploadId`
- `maxSizeBytes`
- `expiresAt`
- `allowedMetadata`
- `metadata` with safe string fields only
- `retryDelays`
- `resumeAcrossSessions`
- `allowTerminate`
- optional `chunkSize` only when infrastructure requires it

The response must not include trusted internal headers, storage credentials, object keys, or provider secrets.

## Vue Composition Pattern

Use a composable for one active upload. It should expose reactive state:

- `status`
- `progressPercent`
- `bytesUploaded`
- `bytesTotal`
- `uploadUrl`
- `uploadExpiresAt`
- `terminalError`
- `isActive`
- `canPause`, `canResume`, `canCancel`

Start uploads from a browser event handler after a session exists. Never instantiate `new tus.Upload(...)` at module evaluation time.

Use `assets/client/useTusUpload.ts` as the starting point.

## Pinia Queue Pattern

Use a queue store when screens can upload more than one file, navigate while uploading, or show background progress. The store should hold safe app-level fields, not raw secrets:

- app upload id
- filename display value if allowed
- size and type
- status/progress
- last safe error code
- created/updated timestamps

Keep actual `tus.Upload` instances in a non-serializable runtime map or composable-level state, not persisted Pinia state.

Use `assets/client/useUploadQueueStore.ts` as a starting point.

## Quasar and SSR

Rules:

- Register upload boot files with `server: false` when SSR is enabled.
- Do not access `window`, `File`, `Blob`, `localStorage`, or `navigator` during server render.
- Lazy-load upload UI or composables on pages that need them.
- Keep tus code out of universal route guards.
- Use server-safe DTO types in shared modules; keep browser runtime code in client-only modules.

## PWA and Service Worker

Do not let the service worker cache or rewrite upload traffic.

Exclude from precache and runtime cache:

- `/files/`
- tus `POST`, `PATCH`, `HEAD`, and `DELETE` routes
- generated upload URLs
- internal hook/control routes

Service workers must not replace upload failures with offline fallback pages. Offline UX should pause or fail the upload explicitly and allow resume when connectivity returns.

## Retry and Resume

Official tus-js-client defaults retry status codes such as `409`, `423`, and non-4xx/server-like failures, with bounded retry delays. Keep product-specific retry behavior explicit.

Recommended behavior:

- Do not retry `401` or `403` blindly. Refresh auth through normal app logic, then let the user retry or resume.
- Treat `404` and `410` as terminal for the current upload URL.
- Allow retries for `409` and `423` only with bounded delays.
- Use `findPreviousUploads()` and `resumeFromPreviousUpload()` only when local URL storage is available and the gateway still enforces ownership.
- Set `removeFingerprintOnSuccess: true` by default.
- Clear URL storage on logout, project switch, or account switch.

## Parallel Uploads

Do not enable `parallelUploads` by default. It requires tus concatenation support, gateway compatibility, storage compatibility, and more complicated frontend progress/error handling. Enable only after load tests prove it helps.

## Metadata

Allowed metadata should be small and explicit:

- `session_id`
- `filename` as display-only value when product permits it
- `filetype` as browser-declared value, not authoritative truth
- `purpose` as a safe enum

Do not send user id, project id, object key, provider id, provider token, raw JSON blobs, or unbounded text in metadata.

## UX States

Expose clear states:

- `idle`
- `creating-session`
- `ready`
- `uploading`
- `paused`
- `retrying`
- `completed-upload`
- `processing`
- `ready-asset`
- `failed`
- `expired`
- `cancelled`

Do not tell users the final asset is ready immediately after tus upload completion if scanning, relay, transcoding, or provider registration still runs.

## Telemetry

Send only safe telemetry:

- app upload id
- status
- size bucket
- retry count
- final HTTP status
- safe error code
- request id or trace id when safe

Never send Authorization headers, cookies, raw upload URLs, raw `Upload-Metadata`, internal trusted headers, provider credentials, or unreviewed filenames.

Use `assets/client/uploadTelemetry.ts` for redaction helpers.

## Review Checklist

- Vue code calls upload-session API before tus creation.
- No trusted internal headers are sent from the browser.
- SSR pages do not import browser-only tus runtime code on the server path.
- PWA/service worker excludes upload routes.
- Resume works after refresh and after network interruption.
- Logout/project switch clears unsafe stored upload URLs.
- 401/403 do not loop endlessly.
- Raw upload URLs and metadata are scrubbed from logs/Sentry.
- UI distinguishes upload completion from final asset readiness.
