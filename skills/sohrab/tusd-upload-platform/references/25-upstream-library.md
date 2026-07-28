# Upstream tusd — Register (a)

Generic knowledge about the official tusd server and the Go library, valid for any consumer. Values were read from the `github.com/tus/tusd/v2` source at the version recorded in `10-source-map.md`; re-check against the version you actually run.

The Ala service uses this library and overrides parts of it. Where this file and `15-ala-service.md` disagree, that file wins inside the Ala repository.

## The binary and the library are the same handler

`tusd` the binary is a thin main around `pkg/handler`. Every flag sets a field of `handler.Config`, so a library consumer gets the same behaviour and the same defaults — and, critically, the same *absences*. The binary sets several things for you that the library does not. An embedded service that does not set them has them unset.

| Flag on the binary | Config field | If nothing sets it |
|---|---|---|
| `-max-size` | `Config.MaxSize` | **unlimited**; every size check in `unrouted_handler.go` is gated on `MaxSize > 0` |
| `-behind-proxy` | `Config.RespectForwardedHeaders` | `Location` is built from the request as seen by the process, so a proxy must rewrite it |
| `-disable-download` | `Config.DisableDownload` | `GET` on an upload resource serves the bytes |
| `-disable-termination` | `Config.DisableTermination` | `DELETE` removes the upload |
| `-base-path` | `Config.BasePath` | the handler cannot strip its own prefix |
| `-metrics-path`, metrics registration | `s3store.RegisterMetrics` is a separate explicit call | no `tusd_s3_*` metric is exported |

## Handler configuration that decides behaviour

- `StoreComposer` binds exactly one data store for the handler's lifetime. Selecting a backend per request means more than one handler, not more than one store on one handler.
- `PreUploadCreateCallback` is **blocking**. Returning an error denies creation. This is the only place an embedded service can reject an upload before any byte is accepted.
- `PreFinishResponseCallback` is blocking and runs before the completion response is written. Use it for a small response hint only; it is one-shot from the client's point of view, so it must never be the only place a piece of business data exists.
- `PreUploadTerminateCallback` is blocking and decides whether termination proceeds.
- `NotifyCreatedUploads`, `NotifyCompleteUploads` and `NotifyTerminatedUploads` are **not callbacks**. Setting each to `true` makes the handler send on the corresponding channel — `CreatedUploads`, `CompleteUploads`, `TerminatedUploads` — and the send is a **plain blocking channel send** (`unrouted_handler.go:411`, `:578`, `:1010`, `:1255`).

**The notification-channel contract, stated as a rule because getting it wrong is silent.** The handler blocks the request until the send completes. A consumer must therefore drain each channel from a long-lived goroutine started once, not from the request path. A small buffer plus an opportunistic drain looks like it works under low concurrency and, under load, lets one request consume an event belonging to another, because the channels are per-handler and carry no request affinity. Everything the consumer needs must be read from the event, never from the ambient request. `15-ala-service.md` records a live instance of exactly this defect.

## Hook transports

Only one hook handler type can be enabled per process.

| Transport | Shape |
|---|---|
| HTTP | tusd POSTs a JSON event to a URL and reads a JSON response |
| gRPC | the same event over a typed service |
| File | one executable per event on local disk |
| Plugin | a Go plugin loaded into the tusd process |

HTTP hook defaults, which are operational limits and not policy: 15 s timeout, 5 KiB response size limit, 3 retries on a 5xx or a network error with 1 s backoff.

Ordering guarantees are narrow. Only two hold: `pre-create` is first for an upload, and `post-finish` starts after `pre-finish` completes. Everything else may interleave, so `post-create` is not guaranteed to be observed before `post-finish`.

A hook response may carry `RejectUpload` to deny creation, `StopUpload` to end an upload in progress, and an `HTTPResponse` whose status, headers and body are returned to the client. Full response shapes and failure posture are in `45-hooks.md`.

## Storage backends

| Backend | Locking | Where bytes land |
|---|---|---|
| `filestore` | disk-based file locks, local to the machine | the upload directory, plus a `.info` sidecar |
| `s3store` | none of its own; pair it with a locker | S3 multipart parts, assembled at completion |
| `memorylocker` | in-memory, local to the process | — |

Built-in lockers are process-local or machine-local. Horizontal scaling over shared storage requires stickiness or a distributed lock you own; there is no third option that upstream provides.

### `s3store` defaults, at the pinned version

| Field | Default | Why it matters |
|---|---|---|
| `MinPartSize` | 5 MiB | S3's own floor for a non-final part |
| `PreferredPartSize` | 50 MiB | the size actually used for most parts |
| `MaxPartSize` | 5 GiB | ceiling for one part |
| `MaxMultipartParts` | 10,000 | part size is raised automatically when a declared size would exceed this |
| `MaxObjectSize` | 5 TiB | the only real upload ceiling when `MaxSize` is unset |
| `MaxBufferedParts` | 20 | parts held on local disk ahead of the S3 writer |

`MaxBufferedParts × PreferredPartSize` is the local temp-disk demand **per in-flight upload**: with the defaults, about 1 GiB each. This is the single most-missed capacity fact about S3 mode, because "streams to object storage" is read as "needs no disk". Sizing and the disk-pressure response are in `35-storage-lifecycle.md`.

`ObjectPrefix` sets the key prefix. Object keys are `<prefix>/<uploadID>` with `.info` and `.part` siblings. A finished object appears in the bucket only when the multipart upload is completed.

## Protocol facts that constrain design

- `Upload-Metadata` travels in a header: keys are ASCII, values are Base64 on the wire, and the whole header is subject to the front door's header size limit.
- Metadata attached to a finished S3 object is ASCII-only; non-ASCII characters are replaced there even though the `.info` object preserves the original.
- Resume depends on `HEAD` returning the current `Upload-Offset` and on `PATCH` honouring it. A proxy or WAF that rewrites, caches or buffers either one breaks resume without breaking anything visible.
- Creation-with-upload and checksum are extensions. Enabling either requires the whole path — client, proxy, handler and store — to support it.
- Graceful shutdown interrupts request bodies cleanly and gives in-flight work a bounded window. The orchestrator's termination grace period must exceed that window, or shutdown truncates uploads that would have completed.
