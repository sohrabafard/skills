# Constraints

These are properties of the tus protocol and of tusd, register (a). They are constraints in the strict sense: no configuration removes them, and a design that assumes one away fails at runtime rather than at review. They apply to the binary and to the embedded library alike, because both are the same handler.

When a constraint appears to be absent in a specific service, that is register (c) and it is in `15-ala-service.md`.

## Hooks

- **One hook handler type per process.** Choosing a transport is exclusive; there is no fallback chain.
- **Ordering is guaranteed only twice.** `pre-create` is first for an upload, and `post-finish` starts after `pre-finish` completes. Nothing else is ordered, so code must not require `post-create` to be observed before `post-finish`.
- **A blocking hook's latency is the client's latency.** There is no way to make a blocking hook asynchronous while keeping its decision.
- **HTTP hook transport limits are fixed defaults**: 15 s timeout, 5 KiB response, 3 retries on a 5xx or network error with 1 s backoff. The response limit means a hook cannot return a large body to the client.
- **A completion hint reaches the client once.** The client may miss it, so it can never be the only copy of anything.

## Authentication

- **The handler cannot guarantee that the actor who created an upload is the actor who resumes it.** Nothing in the protocol carries identity on `PATCH` beyond the URL. This is the reason per-method ownership checks exist, and no hook configuration substitutes for them.

## Size

- **An unset `MaxSize` means unlimited.** Every size check in the handler is gated on `MaxSize > 0`, so the absence of configuration is not a conservative default.
- **`Tus-Max-Size` is advertisement.** The handler emits it from `MaxSize`; a service that sets the header itself has made a claim the handler will not enforce.
- **The store's own ceiling is the last one.** With `s3store`, `MaxObjectSize` defaults to 5 TiB.

## Storage

- **One process binds one backend for its lifetime.** Selecting a backend per request requires more than one handler or more than one deployment.
- **`ChangeFileInfo.Storage.Path` shapes a filestore path only.** It cannot redirect an S3-backed upload to another backend or bucket; code that assumes it can writes to the configured backend anyway, silently.
- **S3 mode uses local disk.** Roughly `MaxBufferedParts × PreferredPartSize` per in-flight upload, about 1 GiB at defaults, plus concatenation temp files.
- **A finished object appears in the bucket only at completion.** Before that it exists as multipart parts and is not readable by anything downstream.
- **Metadata attached to a finished S3 object is ASCII-only.** Non-ASCII characters are replaced there, though the `.info` object preserves the original.
- **`.info` and `.part` are reserved sidecar names** under the configured prefix.

## Scaling

- **Built-in lockers are local.** Filestore uses disk-based file locks; S3, GCS and Azure use in-memory locks. Neither reaches another instance.
- **Horizontal scale over shared storage requires stickiness or a lock you own.** There is no upstream distributed locker.

## Protocol

- **`Upload-Metadata` travels in a header.** Keys are ASCII, values are Base64 on the wire, and the whole header is subject to the front door's header size limit — which is a much smaller number than the body limit and is frequently the real constraint on how much metadata an upload can carry.
- **Servers must validate metadata.** It is untrusted input arriving in a header, which makes it a header-smuggling surface as well as a data-validation one.
- **Resume depends on `HEAD` returning the current `Upload-Offset` and `PATCH` honouring it.** Any hop that rewrites, caches or buffers either one breaks resume without breaking anything visible.
- **Creation-with-upload and checksum are extensions**, not baseline. Enabling either requires client, front door, handler and store to support it.
- **`Upload-Expires` is the only way the server tells a client that resuming has a deadline.** Without it a client with a retention policy behind it retries into a 404.

## Runtime

- **Reverse proxies must not buffer upload requests.**
- **The handler builds `Location` from the request as it sees it** unless it is configured to respect forwarded headers. One of the two must be true, and only one.
- **Graceful shutdown gives in-flight work a bounded window.** The orchestrator's termination grace period must exceed that window, or shutdown truncates uploads that would have completed.
- **`PATCH`, `HEAD`, `OPTIONS` and `DELETE` must survive the front door unchanged** for any tus feature the product uses.
