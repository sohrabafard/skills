# Browser Client — Register (b)

The browser moves bytes and shows progress. It owns nothing else. It does not choose a tenant, a backend, an object key, a storage credential, a size policy or the truth about whether an asset is ready.

**This file covers tus protocol behaviour in browser code and stops there.** Component structure, store shape, boot-file convention, routing and SSR wiring belong to the frontend skill for the framework in use. The client assets this skill ships carry protocol decisions inside those shapes; they are not a recommendation about the shapes.

## The flow

1. The application calls the control plane through the gateway and receives an upload plan.
2. The plan carries, per upload: where to create the tus resource, an application identifier, the declared size, the allowed metadata, the chunk size, the retry budget, the expiry, and whether termination is permitted.
3. The client creates the tus resource and **reads the resource URL from the `Location` header of that response**. A URL that appeared in the plan is an application URL and is not a tus resource; using it for `PATCH` fails.
4. The client transfers bytes, honouring the server's chunk size.
5. The client reports transfer completion to the control plane if the plane requires an explicit completion call.
6. The UI polls or subscribes for readiness. **Transfer completion is not readiness.**

The Ala service's exact route names, metadata keys and error codes for this flow are in `15-ala-service.md`, because they are register (c) and differ from the generic shape.

## The canonical state list

There is exactly one list, in `assets/client/uploadStates.ts`, with the meaning of each state beside it. Every other file — the composable, the queue store, the UI, telemetry — imports it. Four copies of this list in one skill is how a UI ends up with a state the store cannot represent, which was the state of this skill before this revision.

Two rules govern it:

- **The list is closed.** Adding a state means editing that one file, and every consumer sees the addition as a type error rather than as a silent gap.
- **Never label an asset ready on transfer completion** when scanning, extraction, relay, transcoding or registration still has to run. There are separate states for the two, and collapsing them is the most common product-visible defect on an upload plane.

## `tus-js-client` options

Defaults, applied unless a measured constraint forces otherwise; record the reason when one does.

| Option | Value | Why |
|---|---|---|
| `retryDelays` | from the plan, bounded, **with jitter** | a fixed array synchronises every client's retry after a shared outage and reproduces the load that caused it |
| `removeFingerprintOnSuccess` | `true` | a stale fingerprint after success is only a source of wrong resumes |
| `storeFingerprintForResuming` | only when `tus.canStoreURLs` is true **and** the plan permits cross-session resume | storing a capability URL is a security decision the server makes, not the client |
| `chunkSize` | **from the plan** | the server knows the smallest body cap on the path; the client does not, and unset means one `PATCH` carrying the whole file |
| `uploadDataDuringCreation` | `false` | creation-with-upload needs the whole path to support it |
| `parallelUploads` | unset | it requires concatenation support at the store and the front door, and it makes progress and error handling substantially harder |
| `metadata` | only the allowlisted keys from the plan, normalised to strings | metadata rides in a header and is untrusted input at the server |
| per-request request id | always | it is the only join key between a client failure and a server log |

Check `tus.isSupported` before offering resumable upload, and `tus.canStoreURLs` before offering cross-session resume.

## Resume matching

`findPreviousUploads()` returns every stored entry the client can see, from every previous session and every previous tenant. **Match a candidate against the current upload's own application identifier before resuming it.** Taking the first entry is the defect: after a project switch it resumes an upload belonging to the previous project.

Clear stored fingerprints on success, on logout, on account switch and on project switch. The server still re-checks ownership on every method, which is what makes local storage survivable at all — see `40-authorization.md`.

## Retry classification

| Response | Treatment |
|---|---|
| `401`, `403` | terminal for this attempt. Refresh the credential through the normal application flow, then let the user retry or resume. Never retry blindly: a loop against an authorization failure is indistinguishable from an attack. |
| `404`, `410` | terminal for this upload URL. The resource is gone or expired; start a new upload. |
| `409`, `423` | bounded retry with jitter. These mean an offset conflict or a lock, both of which usually clear. |
| network failure with no response | bounded retry with jitter, **after a `HEAD`**, because the previous `PATCH` may have been applied in full. |
| offline | a paused state, not a failure. Do not let the retry decision fall through to the terminal error handler; that is the class 3 fault in `50-failure-modes.md`. |

## SSR and service workers

- Keep tus code in browser-only modules. Never touch `window`, `File`, `Blob`, `navigator` or local storage during server render, and never construct an upload at module evaluation time.
- Register upload boot code as client-only when SSR is enabled, and keep it out of universal route guards.
- Exclude every upload route from service-worker precache and runtime caching, including the creation path, the resource paths and any control-plane upload route. A service worker that serves an offline fallback in place of a `PATCH` turns a recoverable pause into a corrupt upload.
- Build the exclusion list from the application's configured base path. A hardcoded path silently stops matching the day the path changes.

## Telemetry from the browser

Send: the application upload identifier, the state, a size **bucket**, the retry count, the final HTTP status, a safe error code, and the request or trace id.

Never send: an upload URL, an object key, a filename, raw `Upload-Metadata`, an `Authorization` header, a cookie, a trusted internal header value, or a storage credential. Redaction helpers are in `assets/client/uploadTelemetry.ts`; they take the base path as an argument so they keep working when the path changes.

Do not stream progress ticks into an error reporter. Progress belongs in analytics, sampled.

## Before calling browser work finished

Every item below has a named test in `55-tests.md`. Run them rather than reading this list as a checklist.

- SSR does not import browser-only upload code on the server path.
- No upload request is intercepted by the service worker.
- Resume works after a refresh, after a short disconnect, and does **not** work across a project switch.
- `401` and `403` do not loop.
- No URL, key, filename or credential reaches the error reporter.
- CORS exposes every header the UI reads.
- Cancel behaviour matches whether the server permits termination.
- The UI distinguishes transfer completion from asset readiness.
