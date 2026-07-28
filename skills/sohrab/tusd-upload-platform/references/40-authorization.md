# Authorization and the Ownership Record

This file decides who may act on an upload. It does not decide who a caller is: that is `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`), which owns the trust boundary, the derivation of identity, the list of trusted headers, and what happens when the gateway is unreachable. This file starts one step later, at "given a caller I already believe, may they do this to this upload?"

## The trust boundary in two lines

The gateway is the external boundary. It verifies the token, strips spoofable internal headers from client requests, injects trusted context, and forwards. Browser and mobile code must never send a trusted internal header, and an upload plane must never accept one that did not arrive through the gateway path.

**Verify the stripping, at the front door, before relying on it.** An upload service that performs no stripping of its own is relying entirely on a proxy rule plus a network binding. Both are real controls and both are invisible from the service's own code, so they are exactly the kind of control that survives a config refactor by accident. The Ala service performs no stripping of its own; see `15-ala-service.md`.

## Authorize every method, separately

Creation-time authorization protects creation. Every later request presents nothing but the upload URL, so the upload URL is a capability and each method that accepts it needs its own decision.

| Method | Decision required before the byte-transfer handler runs |
|---|---|
| `OPTIONS` | CORS policy for approved origins and headers only. Never expose a trusted internal header name through CORS. |
| `POST` (creation) | Identity, tenant, the upload's purpose, the declared size against the cap, and the metadata allowlist. This is the last point at which rejection costs nothing. |
| `HEAD` | Ownership, before the offset is revealed. An offset tells an attacker that an upload exists and how far it has progressed. |
| `PATCH` | Ownership, before any byte is accepted. Accepting first and checking later has already cost the storage. |
| `DELETE` | Ownership plus an explicit termination policy. If the product does not expose cancellation, disable termination rather than authorizing it. |
| `GET` | Do not route it. If download must exist, it is a separate authorization flow against the application's own asset record, not against the upload resource. |

## Consuming an `upload_to_*` permission bit

The bit contract — allocation, encoding, the decoder and its conformance vectors — belongs to `/alaa-permission-generator` (`$alaa-permission-generator`). This file owns only how an upload plane consumes one.

Four permission ids exist for uploads today, generated into the consuming service by the permission catalog: `92 upload_to_content_service`, `93 upload_to_ticket_service`, `94 upload_to_auth_service`, `95 upload_to_comment_service`.

Consumption rules:

1. **Build the permission name from the target service and require it to resolve in the generated map before matching it.** A name the generator does not know must deny, not fall through. Constructing `"upload_to_" + service + "_service"` from client input and matching it against a decoded set is safe only because an unknown name fails the resolve step first.
2. **Check the permission on creation against the client-supplied target service, and again on completion against the *stored* target service.** The stored value is the one that survived validation; re-reading the client's value at completion would let a caller change targets mid-flight.
3. **Reuse the creation permission for completion deliberately, and say so.** There is no separate completion permission, no tus-protocol permission, no extraction permission and no delete permission. That is a decision, not an omission: a caller who was allowed to create the upload is allowed to finish it, and every other operation is authorized by ownership rather than by a bit.
4. **Pin the decision with a test that fails the build when a generated name drifts.** The Ala service commits a test asserting that no generated permission name contains `extract`, `protocol`, `complete` or `delete`, so an id allocated upstream for one of those concepts breaks the build instead of silently changing behaviour. Copy that pattern; it is the only thing standing between a catalog change and an authorization change.
5. Deny with a distinct, stable code — the Ala service uses `403 UPLOAD_PERMISSION_DENIED` — so that a permission denial is separable from an ownership denial in logs and metrics.

Every trusted header that feeds this decision must be individually required with its own failure code, so an incident tells you *which* piece of context was missing rather than that authorization failed.

## The ownership record — one record, stated once

One durable row per upload. Its machine form is `assets/schemas/upload-record.schema.json`; the two must not drift.

| Group | Fields |
|---|---|
| Identity | application upload id; transfer-layer upload id; the resource path the client was given |
| Tenancy | project or tenant id; owner subject; access token id for revocation correlation |
| Intent | target service; purpose; declared size; allowlisted metadata values; storage target |
| Placement | server-generated object key or staging path |
| Progress | state; received size; last activity timestamp |
| Downstream | processing job id, provider id, final asset id, once each exists |
| Correlation | request id; trace id |
| Time | created, updated, finished, terminated, expires |

Two rules about this record:

- **The transfer layer is not the source of truth for business state.** It knows bytes and offsets. Everything a product decision depends on lives in this row.
- **Write the row before the side effect it describes.** An intent persisted first can be reconciled after a crash; a side effect performed first cannot be found.

## Upload identifiers, metadata and paths

- Give every upload identifier a random component with real entropy. Never derive one mainly from a filename, and never make one guessable across tenants, because guessing one is equivalent to holding the capability.
- Avoid identifier shapes that can collide with the transfer layer's own sidecar objects, `.info` and `.part`.
- Treat every metadata value as untrusted input: allowlist the keys, bound the lengths, normalise to strings, and reject anything outside the list rather than ignoring it.
- **No client input may reach a path segment.** A filename containing `../` must leave the stored path unchanged; `55-tests.md` names the test that proves it.
- Client-declared content type is a hint. Validate the actual type server-side before anything downstream trusts it.
- Never let client metadata select a tenant, a backend, a bucket, an object key or a provider target.

## Resume storage in the browser

Storing an upload URL locally is a resume feature. It is safe only while every method re-checks ownership, because a stored URL outlives the session that created it.

- Clear stored fingerprints on success, on logout, on account switch and on project switch.
- Match a stored fingerprint against the current upload's own application identifier before resuming it. Resuming the first stored entry unconditionally is how a project switch resumes the wrong upload.
- If the product treats upload URLs as too sensitive to persist, disable cross-session resume and say so in the plan the server returns, rather than leaving the client to decide.

## Deny cleanly

- Distinguish "not authenticated", "not permitted", "not found" and "expired" with different codes, so an incident is diagnosable.
- Return the same response for "this upload belongs to another tenant" and "this upload does not exist", so the boundary does not confirm existence.
- Log every denial with the request and trace id and the reason code, and never with the value that was rejected.
