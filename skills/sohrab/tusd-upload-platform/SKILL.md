---
name: tusd-upload-platform
description: "Resumable-upload platform skill covering three registers: the official tusd server and Go library, browser clients on tus-js-client, and the Ala tusd service that embeds the tusd handler in-process. Use it to design, review, implement, or debug an upload plane - server-side size caps and the body-cap chain, retention and reaper policy for unfinished uploads, hook and callback failure posture, per-method authorization and the upload_to_* permission bits, resume-matching correctness, part sizing and temp-disk demand, object-key construction, front-door timeouts and buffering, upload telemetry, and upload incident triage. Do not use it for presigned-URL uploads, non-tus transfers, or one-off transfer advice. For bucket lifecycle policy, IAM shape, credential rotation or CDN origin use /alaa-minio-object-storage; for gateway trust use /alaa-trust-gateway-auth; for the permission bit contract use /alaa-permission-generator."
---

# tusd Upload Platform

## Mission

Make an agent correct on resumable uploads across three registers this skill keeps separate and never blends.

| Register | What it is | Whose source is authoritative |
|---|---|---|
| **(a) Upstream** | The official tusd server and its Go library `github.com/tus/tusd/v2`: flags, hooks, storage backends. Generic; valid for any consumer. | tus.io and the tusd repository at the pinned version |
| **(b) Client** | Browser upload transport through `tus-js-client`. Stops at the network boundary and owns nothing server-side. | the `tus-js-client` version in the lockfile |
| **(c) Ala** | What the Ala `tusd` repository decided on top of (a), including each upstream feature it declined. | the Ala `tusd` repository source |

**When (a) and (c) disagree, (c) wins inside the Ala repository, and the answer names which register each half came from.** An upstream default presented as Ala behaviour is a defect, and so is the reverse: the Ala service runs no tusd binary, so no CLI flag describes it.

## What this skill does not own

| Ground | Read instead | Leave when |
|---|---|---|
| Bucket lifecycle policy, abandoned-multipart abort, IAM policy shape, root credentials, rotation, versioning, replication, encryption, TLS to the object store, CDN origin, MinIO topology | `/alaa-minio-object-storage` (`$alaa-minio-object-storage`) | the question is about the bucket, not one upload |
| Who may assert a trusted header, how identity is derived, what happens when the gateway is unreachable | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) | you are deciding whether a caller may be believed |
| The permission bit contract, id allocation, bitmap decoding, generated decoders and their conformance vectors | `/alaa-permission-generator` (`$alaa-permission-generator`) | you are writing or checking a decoder |
| Header names, envelope shapes, event and metric names, Ala timeout and retry values | `/alaa-services-contract` (`$alaa-services-contract`) | you need the exact spelling of a name or a number |
| Retry legality, backoff shape, idempotency mechanics, timeout doctrine | `/alaa-reliability-sla` (`$alaa-reliability-sla`) | you are shaping a retry, not placing one |
| HAProxy directive syntax and tuning | `/alaa-haproxy` (`$alaa-haproxy`) | you are editing a proxy config file |
| Image build, Compose and Swarm delivery, Kubernetes and Helm | `/alaa-docker-production` (`$alaa-docker-production`), `/alaa-k8s-helm` (`$alaa-k8s-helm`) | the change is to delivery rather than to upload behaviour |
| Vue component structure, Pinia store shape, Quasar boot convention, SSR wiring | the frontend skill for that framework | the question is code shape, not tus behaviour |
| Go code shape, package layout, concurrency idiom | `/alaa-golang` (`$alaa-golang`) | the Go is not about tus semantics |
| Telemetry requirement levels and gates | `/alaa-observability-soc` (`$alaa-observability-soc`) | you are deciding whether a signal is required |

## When not to use

Do not use this skill for a presigned-URL upload that speaks no tus protocol, or for a one-off non-resumable form post. Do not use it to author an HAProxy directive — that is `/alaa-haproxy` (`$alaa-haproxy`). Do not use it for Vue component structure, store shape or boot-file convention, which are `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`) and `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`). Do not use it for bucket lifecycle policy, storage identity or credential rotation, which are `/alaa-minio-object-storage` (`$alaa-minio-object-storage`). Do not use it for queue or consumer mechanics, which are `/alaa-async-messaging` (`$alaa-async-messaging`).

## Binding rules

1. Set a server-side maximum upload size on every deployment that accepts client bytes. Upstream treats an unset `MaxSize` and an absent `-max-size` as unlimited, so the only remaining ceiling is `s3store.MaxObjectSize`, 5 TiB.
2. Never advertise a limit the same process does not enforce. `Tus-Max-Size` is a claim, not a control; a client that trusts it uploads until storage refuses.
3. Define retention for unfinished uploads before the plane takes traffic: an age threshold, an owning job, a metric and a stated failure behaviour. A column that only gates intent reuse is not retention, because it frees no bytes.
4. Derive chunk size on the server, below the smallest body cap on the narrowest hop, and return it with the upload plan. Raising a fleet-wide body cap to admit one upload disables a platform control on every route; the correct move is a dedicated ingress.
5. Authorize `POST`, `HEAD`, `PATCH` and `DELETE` separately, before the byte-transfer handler runs. Creation-time authorization protects creation only, because every later request presents nothing but the upload URL.
6. State the failure posture of every hook and callback individually, as "on error this call denies" or "on error this call proceeds and its record is lost". An unstated posture is read as fail-open by the next agent to arrive.
7. A call that decides whether a caller may act denies when it cannot decide. A call that only records denies nothing, and must log its own failure, because a silently discarded error leaves bytes in storage with no control-plane row.
8. Generate object keys on the server from upload and asset identity, with no client-supplied path segment and no client-supplied bucket. Client metadata never selects a tenant, a backend or a key.
9. Treat the upload URL as a capability and re-check ownership on every method that accepts it. Storing it locally is a resume feature, not an authorization decision.
10. Pin the tusd image and the tusd module to an exact release, and keep that version string in exactly one file so a bump is one edit. `latest` makes a rollback unreproducible.
11. Keep upload URLs, object keys, filenames, raw `Upload-Metadata`, trusted header values and storage credentials out of logs, metrics labels, traces, Sentry and client analytics. Join on the upload identifier and the request or trace id.
12. Read every claim about the Ala service from its source in the same session, or report it as unverified. It diverges from upstream defaults in places invisible from configuration.

## Default platform shape

Public clients reach the gateway; the gateway verifies the token, strips spoofable internal headers, injects trusted context and forwards. The control plane issues an upload plan before any byte moves and owns the durable record of it. The tus layer moves bytes and nothing else. Completion of byte transfer is not readiness: scanning, extraction, relay or registration runs afterwards, and the client learns readiness from the control plane, not from the tus response.

Choose the smallest shape that meets the requirement; justify any custom shape before proposing it.

## Routing

Every reference and asset is routed by an observable condition in `references/00-topic-map.md`. Open it first; read only rows matching the task.

## Expected output

For design or review work, return: the register each claim came from; the topology decision and its rejected alternative; the authorization decision for every tus method; the size-limit chain from client to storage with the enforcing component named at each hop; the retention rule with its threshold, owner and metric; the failure posture of every hook and callback; the storage lifecycle including any two-copy window; the observability contract; the tests that catch a regression in each; and the open risks. For debugging, lead with ranked root causes, then the exact request, response field, log line or query that confirms or eliminates each.
