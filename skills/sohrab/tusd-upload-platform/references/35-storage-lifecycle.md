# Storage Lifecycle — the Upload-Plane Slice

This file owns the object-storage behaviour that follows from the tus protocol and from one upload's identity. It does not own the bucket.

**Handed to `/alaa-minio-object-storage` (`$alaa-minio-object-storage`):** bucket lifecycle policy and its rules; abandoned-multipart abort configuration; IAM policy shape and the root-credential problem; credential rotation; versioning; replication; server-side encryption; TLS to the object store; CDN origin; local MinIO topology and exposure. When a question is about the bucket rather than about one upload, that skill answers it.

**The split on retention, stated once so it cannot drift:** retention of *unfinished uploads* — how long a started-and-abandoned upload may hold bytes, who deletes it, and what is emitted when they do — is owned here. Bucket-level lifecycle policy that expires objects by age or prefix is owned there. A plane needs both; neither substitutes for the other, because a lifecycle rule cannot see whether an upload is still in progress and a reaper cannot delete what the bucket has already tiered away.

## Size limits, end to end

State the chain as a chain. Every hop has a limit; the smallest one wins, and the component that enforces it must be named.

| Hop | Limit | Enforced by |
|---|---|---|
| Browser | the file the user chose | client-side check only; any non-browser client bypasses it |
| Front door | request body cap, header size cap | the proxy; a tus `PATCH` carries a chunk, so the cap applies per chunk |
| Any service that terminates or proxies tus traffic | that platform's body cap | that service's framework |
| tus handler | `MaxSize` / `-max-size` | **unlimited when unset** |
| Object store | `s3store.MaxObjectSize`, 5 TiB by default | the store |

Four rules follow, and each has cost a real plane an outage or a bill.

1. **Set the handler's own cap on every plane.** It is the only limit that rejects at creation, before a byte is accepted, with a clear status. Every other hop fails mid-transfer.
2. **Never advertise a cap you do not enforce.** `Tus-Max-Size` is discovery metadata. A plane that advertises 5 GiB with `MaxSize` unset tells every client a falsehood and accepts 5 TiB.
3. **Chunk size is a server decision.** When `chunkSize` is unset, `tus-js-client` streams the whole remaining file in one `PATCH`, so the front door's body cap becomes the effective file-size limit and the failure appears as a mid-upload error rather than a rejection. Compute the chunk size on the server, below the smallest cap on the narrowest hop, and return it in the upload plan so it changes with deployment rather than with a client release.
4. **Raising a fleet-wide body cap to admit an upload is prohibited.** It disables a platform control on every route served by that hop. The correct move is a dedicated ingress for the upload path, with its own cap.

## Multipart part sizing and temp disk

At upstream `s3store` defaults — `PreferredPartSize` 50 MiB, `MaxBufferedParts` 20 — each in-flight upload demands roughly **1 GiB of local temporary disk**, plus a concatenation temp file where concatenation is used. "Streams to object storage" does not mean "needs no disk".

Sizing procedure:

1. Decide the maximum number of concurrent uploads one instance will accept.
2. Multiply by `MaxBufferedParts × PreferredPartSize`.
3. Add headroom for concatenation temp files if the plane allows concatenation.
4. Provision that as a real volume or tmpfs with a known size, and alert on its utilisation.
5. If the number is unaffordable, lower `MaxBufferedParts` before lowering `PreferredPartSize`, because a smaller part size raises request count against the store and can hit `MaxMultipartParts` on large files.

A plane with no dedicated volume, no tmpfs and no disk-pressure guard fills the container's writable layer and fails every concurrent upload at once. Under disk pressure the required response is to stop accepting **new** creations while letting in-flight uploads drain, because rejecting in-flight `PATCH` requests destroys work already done.

## Object keys

Keys are generated on the server from upload and asset identity. No client-supplied segment, no client-supplied bucket, no filename.

- The tus layer owns `<prefix>/<uploadID>` with `.info` and `.part` siblings. Never place your own objects where they can collide with a `.info` or `.part` name.
- The application layer owns keys built from its own identifiers, for example `tmp/<assetID>/<componentID>/<uploadID>`, `final/…` and `extracted/…`.
- **Include the tenant or project in the key prefix.** The Ala service does not: its keys carry asset and component identity but no tenant, so isolation rests entirely on Postgres. That is a working control today and a fragile one, because it makes per-tenant lifecycle rules, per-tenant cost attribution and prefix-scoped credentials impossible, and it turns any future direct-listing path into a cross-tenant read. Record it as a service defect; adding a prefix later requires a migration of existing keys.
- Include a random component in any identifier you generate. Never derive one mainly from a filename, and never let client input reach a path segment.

## Two copies, and when a finished object appears

Two properties surprise people and both change what monitoring must report:

- **A finished object appears in the bucket only at completion.** Before that, the bytes exist as multipart parts, which are not listable as the object and not readable by anything downstream. A downstream consumer that polls the bucket sees nothing until the upload finishes.
- **Finalization by server-side copy leaves two copies.** Where the design promotes a temporary object to a final key with `CopyObject`, the bucket holds both until cleanup runs. Peak storage is therefore twice the payload for the duration of that window, and a cleanup failure makes it permanent. Size the bucket for the peak, and alert on the count of temporary objects older than the expected window rather than on total bytes, because total bytes hides it.

## Retention for unfinished uploads

An upload that starts and never finishes holds bytes, holds a control-plane row, and holds multipart state at the object store. Nothing reclaims any of the three by itself.

A complete retention rule has five parts, and a rule missing any one of them is not implementable:

| Part | What it must state |
|---|---|
| Threshold | the age after last activity at which an unfinished upload is reclaimable, as a value, not "later" |
| Owner | the named job or command that performs the reclamation, and how often it runs |
| Scope | control-plane row, stored bytes, **and** the abandoned multipart upload at the object store — all three, because deleting only the row leaks the other two |
| Metric | the count of uploads eligible for reclamation and the count reclaimed per run, so a stalled reaper is visible |
| Failure behaviour | what happens when reclamation fails: retry independently, do not block other work, and alert when the eligible count grows across consecutive runs |

`Upload-Expires` is the server's statement of that threshold to the client. Send it on creation and on each `HEAD` so a resuming client can tell whether resuming is still possible instead of discovering it through a 404. A plane with a reaper and no `Upload-Expires` produces clients that retry into nothing.

**Abandoned multipart uploads accrue cost invisibly.** They do not appear in a bucket listing and a filesystem janitor cannot see them. Aborting them is part of this reclamation scope; the bucket-level lifecycle rule that catches whatever the reaper misses belongs to `/alaa-minio-object-storage` (`$alaa-minio-object-storage`).

## Disk-pressure thresholds

Set thresholds from a measured baseline; the actions are not negotiable.

| Condition | Action |
|---|---|
| Temp or staging utilisation crosses the first threshold | alert; do not change behaviour |
| Utilisation crosses the second threshold | refuse new upload creations with a retryable status; let in-flight uploads drain |
| Utilisation crosses the third threshold | refuse creation and page, because in-flight uploads will now fail on their own |
| The reaper's eligible count grows across consecutive runs | alert, because the reaper is losing to arrival rate and only capacity or a shorter threshold fixes it |
