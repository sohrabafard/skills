# Topologies

## Topology A: Direct to MinIO / S3-Compatible Storage

### When to use it

Use this path when the final artifact should live in your own object store and can be served from your own CDN or object URL policy.

### End-to-end flow

1. Client calls your application to request an upload session.
2. Application creates an upload policy record and returns an app token or session token.
3. Client uploads to `tusd-s3` through your gateway.
4. Gateway authenticates the request and forwards it to tusd.
5. `pre-create` hook validates actor, tenant, upload purpose, size rules, and metadata.
6. tusd streams the file to MinIO / S3-compatible storage.
7. `pre-finish` may add a small response hint such as an app asset URL.
8. `post-finish` persists or confirms the final asset record and triggers any async side effects.

### Strengths

- Lowest latency to your own storage.
- No second upload hop.
- Clean fit when your S3 endpoint is also your delivery origin or CDN origin.

### Caveats

- S3 mode still buffers temporary multipart data on local disk. Treat local temp capacity as a first-class resource.
- The stock tusd binary does not dynamically switch between storage backends inside one process.
- Horizontal scaling needs sticky sessions or a stronger custom locking design.

## Topology B: Local Staging, Then Async Relay to an Upstream tusd / Video Provider

### When to use it

Use this path when users must ultimately upload into a provider-controlled video service, but provider credentials must remain fully server-side and the provider does not offer the hooks or auth controls you need.

### End-to-end flow

1. Client asks your application for permission to upload a video.
2. Application creates an upload policy record with target `upstream_tusd`.
3. Client uploads to `tusd-staging` through your gateway.
4. `pre-create` validates actor, tenant, content rules, and target.
5. tusd writes the upload to local staging disk.
6. `post-finish` writes a durable relay job or outbox record and returns immediately.
7. Relay worker uploads the staged file to the upstream tusd service using your service-owned credentials.
8. Worker persists the upstream upload URL, provider asset URL, or provider asset ID in your application database.
9. After verification, the worker marks the asset ready and schedules staged-file cleanup.

### Why this is usually the right design

- Users never see provider credentials.
- You keep hooks, validation, and ownership logic on your side.
- You can retry relay independently of the client upload.
- You can add moderation, scanning, metadata normalization, or business workflows before publishing the provider asset.

### Required state machine

At minimum, track these states in the application:

- `initiated`
- `uploading`
- `uploaded_to_staging`
- `relay_queued`
- `relaying`
- `ready`
- `failed`
- `terminated`

Do not infer all business state from tusd alone. Persist it in the application.

### Failure model

Handle these failures explicitly:

- Client upload failed before `post-finish`: leave upload in non-ready state and expire it later.
- `post-finish` hook succeeded but relay enqueue failed: detect from outbox/job audit and recover.
- Relay upload failed after staging succeeded: retry with backoff; do not ask the client to re-upload immediately.
- Relay succeeded but publish step failed: keep provider asset reference and retry publication.
- Cleanup failed: retry cleanup independently from publish success.

### Cleanup model

Use a janitor or scheduled job for:

- stale unfinished uploads,
- failed staged uploads beyond retention,
- successfully relayed staged files,
- orphaned records whose upload or relay status has stalled.

## Topology C: One Custom Go Service With Multiple tusd Handlers

### When to use it

Use this only when the user explicitly wants one deployable unit and accepts custom code.

### Shape

- Embed tusd as a Go package.
- Create multiple handlers with different composers and backends.
- Route requests to the right handler based on path, tenant, target type, or policy record.
- Add your own lock strategy if multiple instances must safely share storage.

### Why it is not the default

- More code and more tests.
- You own routing bugs, lock correctness, and upgrade friction.
- Operational simplicity is usually worse than two plain tusd services.

## Scaling and Locking

### Stock binary baseline

If you run stock tusd behind a load balancer, assume the built-in lock reach is local to the process or local disk. For shared storage and multiple instances, add sticky sessions unless you have a stronger design.

### Recommended progression

1. Start with one instance per topology.
2. Add gateway rate limiting, autoscaling, and queue workers before scaling tusd itself.
3. If tusd must scale horizontally, prefer load-balancer stickiness first for stock binary deployments.
4. Move to a custom Go integration with distributed locking only when the traffic pattern and HA goals justify the extra ownership cost.

## Local vs S3 Path Customization

Only the filestore path can be customized directly via `ChangeFileInfo.Storage.Path`. Use this for staged uploads when you need deterministic local layout, such as tenant/date/uuid partitioning. Do not assume the same hook field can redirect S3 storage to a second backend.
