# Topologies

Three shapes cover every upload plane this skill governs. Pick one from `20-decision-matrix.md`, then read only that section.

## A — direct to object storage

The final artifact belongs in your own object store and is served from your own origin or CDN.

1. The client asks the control plane for an upload plan.
2. The control plane authorizes, persists an intent row, and returns the plan.
3. The client creates a tus upload and transfers bytes through the front door.
4. Creation-time authorization runs before any byte is accepted.
5. The tus layer streams parts to object storage.
6. Completion writes the durable record and enqueues whatever must happen next.

**Strengths.** One hop, lowest latency, and the storage endpoint can also be the delivery origin.

**What it costs.** S3 mode still buffers parts on local disk — about 1 GiB per in-flight upload at upstream defaults, see `35-storage-lifecycle.md`. One process binds one backend. Horizontal scale needs stickiness or a lock you own.

## B — local staging, then asynchronous relay

Users must ultimately land in a provider-controlled service whose credentials must never reach the browser and whose hooks you cannot use.

1. The client asks the control plane for permission and a plan with target `upstream`.
2. The client transfers to the staging plane through the front door.
3. Bytes land on staging disk.
4. Completion writes a durable relay job or outbox row and returns immediately.
5. A worker uploads the staged file to the provider using service-owned credentials.
6. The worker persists the provider's asset identifier.
7. After verification the worker marks the asset ready and schedules cleanup of the staged file.

**Why this shape wins whenever it applies.** Credentials stay server-side; authorization, validation and ownership stay yours; the relay retries independently of the client; and moderation, scanning or normalisation can run before anything is published.

**The state set.** Persist state in the control plane, never infer it from the transfer layer: `created`, `uploading`, `uploaded`, `relay_queued`, `relaying`, `ready`, `failed`, `terminated`. Client-visible states are a different, shorter list; it lives in `assets/client/uploadStates.ts` and nowhere else.

**Failures.** Every one of these has a defined response in `50-failure-modes.md`; do not invent a local one.

**Cleanup.** Staging disk is finite and a relay that succeeds leaves a file behind. Retention values, the reaper contract and the disk-pressure thresholds are in `35-storage-lifecycle.md`. Cleanup retries independently of publication, because a cleanup failure must not un-publish a ready asset.

## C — one embedded service with more than one store

One deployable unit, custom Go, more than one backend selected per request.

**Shape.** Embed the library. Build one handler per composer. Route by path, tenant, target or policy record. Supply your own lock strategy if instances share storage.

**Why it is not the default.** You inherit routing correctness, lock correctness, metrics registration, size limits, shutdown budget and upgrade friction. `20-decision-matrix.md` lists what the binary sets that the library does not; every unset item becomes a defect. The Ala service is a live example, and its outstanding items are in `15-ala-service.md`.

## Scaling and locking

1. Start with one instance per plane and measure before scaling anything.
2. Add front-door rate limiting, control-plane autoscaling and worker capacity before scaling the transfer layer, because the transfer layer is rarely the first thing to saturate.
3. If the transfer layer must scale horizontally over shared storage, add stickiness first. Stickiness is an operational mitigation with a known failure mode — an instance restart loses affinity and the next `PATCH` finds no local lock — not a lock design.
4. Move to a distributed lock only when the traffic pattern makes stickiness insufficient and the team accepts owning lock correctness, including the behaviour when the lock store itself is unavailable.

## Path customisation

Only the filestore path can be shaped directly, through `ChangeFileInfo.Storage.Path`. Use it for deterministic local layout such as tenant, date and identifier partitioning. It cannot redirect an S3-backed upload to a different backend or a different bucket, and code written as if it can fails silently by writing to the configured backend anyway.
