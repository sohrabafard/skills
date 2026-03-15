# Official Constraints That Should Shape the Design

Use these as hard constraints unless the user is embedding tusd programmatically and changing the design deliberately.

## Hook constraints

- Only one hook handler type can be enabled in a single tusd process.
- Hook execution order is generally not guaranteed across lifecycle events.
- The only ordering guarantees that matter are:
  - `pre-create` is always first for an upload.
  - `post-finish` starts after `pre-finish` completes.
- Blocking hooks directly affect request latency.
- HTTP hook defaults are operationally strict:
  - timeout: 15s
  - response size limit: 5 KiB
  - retries: 3 on 500 or network error with 1s backoff
- `post-finish` is not the place for long, fragile work without your own durable retry layer.
- `pre-finish` is one-shot from the client’s perspective. Do not make it the only place final business data exists.

## Authentication constraint

- Stock tusd can authenticate upload creation in `pre-create`, but does not guarantee the same actor will resume the upload later. Treat this as the reason to add gateway-side request ownership checks when security matters.

## Storage constraints

- tusd does not support multi-storage setups well in one stock process.
- The stock CLI chooses one configured backend for the process.
- If multiple backends are required dynamically, either run multiple deployments or embed tusd programmatically with multiple handlers.
- `ChangeFileInfo.Storage.Path` is only useful for filestore-style path customization, not for routing to S3 or another backend.

## Scaling constraints

- Built-in lockers are local in scope:
  - filestore uses disk-based file locks,
  - S3/GCS/Azure use in-memory locks.
- For horizontal scaling with shared storage, you still need sticky sessions or a distributed-lock design.

## S3 / MinIO constraints

- The S3-compatible backend streams to object storage, but still writes temporary multipart data to local disk.
- The finished object may not appear in the bucket until upload completion.
- tus metadata attached to final S3 objects is ASCII-only; non-ASCII characters are replaced there, even though the `.info` object still preserves original metadata.

## Proxy and network constraints

- Reverse proxies must not buffer upload requests.
- When behind a proxy, tusd must be told to respect forwarded headers.
- Graceful shutdown interrupts request bodies cleanly and gives in-flight work a bounded completion window, so deployment automation should use terminating grace periods that match tusd configuration.
