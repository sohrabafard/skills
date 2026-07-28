# The Ala `tusd` Service — Register (c)

Everything here was read from the Ala `tusd` repository on 2026-07-27. Paths are repository-relative. Where this file and `25-upstream-library.md` disagree, this file wins inside that repository.

## What it is, and what it is not

It is a bespoke Go service, `module alaa/tusd`, Go 1.25.0, that **embeds the official tusd handler as a library**. It imports `github.com/tus/tusd/v2` at the version recorded in `10-source-map.md` — `pkg/handler`, `pkg/s3store`, `pkg/filestore`, `pkg/memorylocker` — and builds `tusdhandler.NewHandler(...)` in process at `internal/httpapi/official_tusd_creation.go:65-84`.

It is **not** a deployment of the tusd binary. No CLI flag describes it, `-max-size` and `-behind-proxy` do not exist for it, and advice phrased as flags is wrong here.

It is **not** a consumer of the shared Go HTTP kit. There is no chi and no Fiber; routing is a hand-written `switch` over method and path in `internal/httpapi/router.go:74-107`, served by `net/http`. Do not assume kit middleware, kit body caps or kit observability are present.

Five binaries: `tusd-api`, `tusd-migrate`, `tusd-dispatch-outbox`, `tusd-process-assets`, `tusd-healthcheck`.

## Upstream features it declined

| Upstream feature | Status here | Consequence |
|---|---|---|
| HTTP, gRPC, file and plugin hook transports | none wired | there is no hook endpoint to secure, reach or time out |
| `PreFinishResponseCallback` | not set | there is no `pre-finish`; nothing decorates the completion response |
| `PreUploadTerminateCallback` | not set | there is no `pre-terminate`; termination policy is enforced in the router instead |
| `MaxSize` | never set | uploads are unbounded up to `s3store.MaxObjectSize`, 5 TiB |
| `RespectForwardedHeaders` | not set | the public upload URL depends entirely on the front door rewriting `Location` |
| `s3store.RegisterMetrics` | never called | no `tusd_*` metric is exported |
| `GET` on a tus resource | not routed | download through the tus path is impossible, which is the intended posture |
| Creation-with-upload, checksum | not offered | clients must not send `Upload-Concat` or `Upload-Checksum` |

## The routes

| Route | Purpose |
|---|---|
| `GET /api/health` | liveness only, no dependency checks |
| `GET /api/ready` | four checks: `database`, `object_storage`, `outbox`, `tus_storage`; RabbitMQ is deliberately excluded so a broker outage does not fail the upload plane closed |
| `GET /metrics` | Prometheus text; see the defect below |
| `POST /api/v1/upload-assets` | create one logical asset and its component upload intents |
| `POST /uploads/files` | tus creation, delegated to the embedded handler after the blocking pre-create callback |
| `POST /api/v1/upload-assets/{id}/complete` | finish the asset after every component has transferred |
| `OPTIONS /uploads/files` | tus discovery |
| `HEAD`, `PATCH`, `DELETE /uploads/files/{id}` | tus protocol, authorized before delegation |
| `GET`/`POST /api/v1/internal/upload-assets/...` | internal lifecycle API for target services and workers |

## The client contract

This is the flow a browser or mobile client actually follows. It is not the generic session flow, and guessing it produces a client that cannot upload.

1. `POST /api/v1/upload-assets` with the target `service`, a `purpose`, an `asset_kind` and a `components` array. The response is an **asset plan**: `asset_id`, `status=created`, and per component a `component_id`, an `upload_intent_id`, a `tus_creation_url` and a `tus_creation_metadata` map.
2. For each component, `POST` to the tus creation URL — `/uploads/files` — carrying `Upload-Metadata` with `ala_upload_intent_id` and, when the plan supplies one, `ala_component_id` (`internal/domain/contracts.go:30-32`).
3. **The `Location` header of that response is the real tus resource id.** The plan's `upload_url` field is the Ala intent URL and is not a tus resource. Using it for `PATCH` produces a 404.
4. `Upload-Length` must equal the component's declared size exactly. A mismatch returns `409 UPLOAD_LENGTH_MISMATCH` (`internal/httpapi/official_tusd_creation.go:179-185`).
5. `HEAD`, `PATCH` and `DELETE` require `Tus-Resumable: 1.0.0`. Its absence returns `412 TUS_RESUMABLE_REQUIRED` (`router.go:877` region, `requireTusResumable`).
6. `POST /api/v1/upload-assets/{asset_id}/complete` once every component has transferred. Byte transfer alone does not make the asset usable.

An expired intent returns `410 UPLOAD_INTENT_EXPIRED`; an unknown one returns `404 UPLOAD_INTENT_INVALID`.

**Multi-component assets** — HLS packages, split archives — are first-class in the plan and have no client treatment today. A client uploading one is responsible for creating one tus resource per component, tracking them independently, and calling `complete` only after all of them finish. Design that explicitly; there is no server-side aggregation of partial progress a client can poll.

## Capabilities the rest of this skill routes to, but that live here

- **Transactional outbox.** Rows in `upload_outbox`, dispatched by `tusd-dispatch-outbox` to RabbitMQ with publisher confirms. API requests persist rows rather than publishing, which is why readiness checks the outbox table and not the broker.
- **Durable storage intents.** `upload_storage_intents` records intent before the object-storage side effect, so an interrupted request reconciles instead of orphaning bytes.
- **Archive extraction.** ZIP, TAR and TGZ workers under `internal/processing/` with a safety planner that decides what may be extracted. Extraction intent the planner refuses is rejected at plan time with `422 EXTRACTION_INTENT_DENIED`.
- **Lease-based worker claiming.** `FOR UPDATE SKIP LOCKED` with lease expiry columns, so an interrupted worker's work is reclaimed rather than lost.
- **Forward-only migrations.** SHA-256 checksummed, tracked in `schema_migrations`, applied under a Postgres advisory lock, one transaction each, fail-closed on checksum drift. Never edit an applied migration; add the next sequential file.
- **Internal lifecycle API.** Claim, release, mark-ready, lookup and delete for target services, gated on `X-Internal-Service`. That header is an unsigned bare string; its only protection is network placement. Treat it as a placement assumption to be verified, not as authentication.
- **Contract artifacts.** `docs/openapi/` and `docs/postman/` are part of the reviewed surface. A route change that does not update them is incomplete.

## Storage in one paragraph

Two independent S3 clients run in one process: the aws-sdk-go-v2 client that feeds tusd's `s3store` for byte transfer, and a hand-rolled SigV4 client at `internal/storage/s3_http_client.go` used for bucket checks, archive reads, extracted writes, the finalization copy and cleanup. Object keys are server-generated: tus-owned `<prefix>/<uploadID>` with `.info` and `.part` siblings, and Ala-owned `tmp/<assetID>/<componentID>/<uploadID>`, `final/…` and `extracted/…`. Full treatment, including the missing tenant scoping and the two-copy window, is in `35-storage-lifecycle.md`.

## Service defects found in this source, recorded as service defects

These are properties of the Ala repository, not gaps in this skill. Each one is a change request against that repository.

1. **Advertised cap, no enforcement.** `OPTIONS /uploads/files` sets `Tus-Max-Size: 5368709120` at `router.go:751` while `MaxSize` is never configured. The service promises 5 GiB and permits 5 TiB.
2. **Shared notification channels of capacity 1.** `createdUploads`, `completeUploads` and `terminatedUploads` are `make(chan tusdhandler.HookEvent, 1)` (`official_tusd_creation.go:54-56`), shared across every request on one handler, and upstream sends on them with a **blocking** send. The drain loop is a `select` with `default: return` (`:193-206`). One request's drain can therefore consume another request's event and process it under the wrong request context. The correct upstream pattern is one long-lived goroutine per channel owning the drain, with per-event context carried in the event rather than taken from the ambient request.
3. **Silent post-hook failures.** `syncCreatedUpload`, `syncFinishedUpload` and `syncTerminatedUpload` discard their errors (`:217`, `:233`, `:267`) and log nothing. See `45-hooks.md` for what each loss produces.
4. **Stub metrics.** `/metrics` returns three hardcoded `alaa_*` zeros (`router.go:631-649`) and is unauthenticated at the application layer. `s3store.RegisterMetrics` is never called.
5. **Unused observability contract.** `internal/observability/contracts.go` defines fifteen events with required and forbidden field lists, and `Dependencies.Events` and `Dependencies.Metrics` are never populated in `cmd/tusd-api/main.go`. There is no `slog` call and no event emission in non-test code.
6. **No inbound header stripping at the service edge.** There is no `Header.Del` anywhere in `internal/httpapi/`. The service trusts HAProxy plus loopback binding in Compose to remove client-supplied trusted headers. Verify that at the front door; the obligation belongs to `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`).
7. **No HTTP client timeout on the SigV4 path.** `NewS3CompatibleHTTPClient` falls back to `http.DefaultClient`, which has no timeout, so a hung object store hangs the caller indefinitely. It also carries no session-token support.
8. **No retention.** `upload_sessions.expires_at` gates intent reuse and frees nothing. There is no reaper, no bucket lifecycle rule and no abandoned-multipart abort, and the `upload.asset.expired` event names a "retention worker" that does not exist.
9. **Shutdown budget shorter than a legitimate request.** `ShutdownTimeout` defaults to 10 s (`cmd/tusd-api/main.go:100`), far below the duration of a large `PATCH`.
10. **MinIO exposure in Compose.** The API is loopback-bound while MinIO publishes 9000 and 9001 on all interfaces, and the application runs as the MinIO root account. Hand this to `/alaa-minio-object-storage` (`$alaa-minio-object-storage`).

## Deployment

Docker Compose and Docker Swarm only. There are no Kubernetes manifests and no Helm chart in the repository; the Kubernetes material under `docs/_agent_plans/` is uncommitted planning, not a deployed artifact. HAProxy fronts the service; its behaviour and its two defects are in `70-front-door.md`.
