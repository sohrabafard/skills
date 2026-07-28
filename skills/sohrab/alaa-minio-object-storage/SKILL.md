---
name: alaa-minio-object-storage
description: "Object-storage platform policy for the Ala fleet's MinIO and S3-compatible buckets: bucket and object-key design, tenant scoping inside the key, lifecycle policy including the incomplete-multipart abort rule, versioning, encryption, replication, bucket-policy shape, credential supply and rotation, TLS and addressing style, presigned URLs, and the failure classes of an unreachable or half-written store. Use when shaping a bucket, building an object key, adding a lifecycle rule, granting or rotating storage credentials, issuing a presigned URL, serving a user's download, naming a `STORAGE_*` value or provider profile, running an `mc` command, or deciding what a service does when the store is down. Do not use it to choose between Postgres and Redis (/alaa-data-layer), for a Dockerfile or Compose file (/alaa-docker-production), for Kubernetes or Helm (/alaa-k8s-helm), or for tus upload-plane behaviour (/tusd-upload-platform)."
---

# Alaa MinIO Object Storage

You own the object store as a platform component: the bucket, the key namespace inside it, the policy attached to
it, the identity that reaches it, the transport that carries the bytes, and what a consuming service does when it
fails. A defect here is a cross-tenant read returning `200`, a credential nobody can rotate, or a bill that grows
from parts no listing shows. You do not own the upload protocol above the store, the database beside it, or the
substrate under it.

## When not to use, and when object storage is the wrong store

Object storage holds immutable opaque byte sequences, addressed by a key the server computes, read and written
whole. Put the fact in Postgres instead whenever it must be queried by anything other than its key, updated in
place, read inside a transaction, or joined to another fact; that decision belongs to `/alaa-data-layer`
(`$alaa-data-layer`), which owns store selection. Do not load this skill for a change touching no bucket, no
object key, no storage credential and no storage policy.

## Constraints that hold on every task

1. **An application identity never holds root or administrative credentials for the object store.** Root deletes
   every bucket, rewrites every policy and reads every tenant's objects, so one compromised application becomes
   total data loss. Give each service an identity whose policy names exactly the bucket and key prefixes it uses.
2. **Every bucket receiving multipart uploads carries a lifecycle rule that aborts incomplete multipart uploads,
   and that rule states a maximum age.** Parts of an interrupted upload stay allocated and billed and appear in no
   object listing, so nothing else will ever remove them. Use seven days where no fleet value is registered, and
   ask `/alaa-services-contract` (`$alaa-services-contract`) to register one.
3. **Every object key takes its tenant scope from the trusted request context, never from client input.** The
   store applies no tenant filter of its own, so a key assembled from a client-supplied value is a cross-tenant
   read returning a well-formed success. Build the key server-side from the project the gateway asserted.
4. **Credentials reach the process from configuration, never from a committed file, and appear in no log line,
   exception message, URL, metric label, span attribute, report or command line.** A credential in git history or
   in a log outlives whatever carried it, so the only remedy left is rotation. A credential on a command line is
   the same defect by a quieter route: the shell expands it before the program starts, so it sits in that
   process's `argv`, where the process list exposes it and the shell's history file records it. Pass it in the
   environment instead, or in a file whose mode restricts it.
5. **Credentials are rotatable without a code change**, so the process re-reads them from their source on restart
   or refreshes them from a credential provider. A credential captured once at client construction turns a leak
   into a redeploy decision taken under incident pressure.
6. **Transport is TLS on every path whose endpoint host is not a loopback address.** A SigV4 `Authorization`
   header authenticates a request and encrypts nothing, so a plaintext hop exposes the object bytes and the signed
   request to every workload sharing that network.
7. **Serve a user's download of their own file through a presigned URL whose lifetime is bounded by
   `STORAGE_PRESIGN_MAX_SECONDS`, or through the application, and never by making the bucket publicly readable.**
   A file that lands in the store has to reach the user who is entitled to it, so this constraint names the path
   that carries it rather than forbidding the wrong one and stopping there. Public read is an unbounded,
   unauthenticated and unrevocable grant over every object in the bucket: it cannot be narrowed to one object, it
   asks the reader for nothing, and it cannot be withdrawn from anyone who already knows a key. A presigned URL is
   scoped to one object and one operation and it expires on its own, which is why it is the replacement rather
   than a softer version of the same thing. Put genuinely public content, such as a logo or a published document,
   in a separate bucket whose entire contents are intended to be public, so no policy mistake can widen the
   private one. `references/60-presigned-urls-and-delivery.md` owns the download path in full.
8. **The object store is never the source of truth for a fact a database also holds.** A listing is not a
   transaction and a `HEAD` is not a lock, so a service reading existence from the store races its own writes and
   cannot roll back.
9. **Read every storage value that is a guess, a provider limit, or a thing that can differ between MinIO and
   ArvanCloud or between a test stack and production from a named `STORAGE_*` environment variable, give it a
   default this skill states, and validate it before the storage client is constructed.** A number compiled into
   code costs a code change, a review, a build and a deploy on the day the provider turns out to want a different
   one, and that day arrives under incident pressure. `STORAGE_PROVIDER_PROFILE` selects the bundle of defaults a
   provider needs, every variable still overrides its profile default from its own environment value, and no
   service branches on the profile name, because a branch turns adopting a fourth provider into a code change in
   every service. `references/05-environment-contract.md` owns the names, the
   defaults, the profile table, the evidence behind each default and the validation, and `/alaa-arvan-object-storage`
   (`$alaa-arvan-object-storage`) `references/15-environment-contract-deltas.md` states only where ArvanCloud's
   default differs.

## What the fleet does today

The fleet's only object-storage consumer violates constraints 2, 3, 4, 5 and 6, and leaves 7 unproven because it
sets no bucket policy and issues no presigned URL `[source: tusd-upload-platform repository, read: 2026-07-27]`.
Its Compose and Swarm files put the application on the store's root credentials, and those files describe the
local development and test stack rather than production, so that is a constraint 1 finding against the test stack
and an open question against production — `references/80-topology.md` states the boundary and
`references/30-identity-credentials-and-access.md` carries the question. It meets the logging half of constraint 4 — its runtime config plan and its forbidden-log-field list
already redact the credential, the object key and the presigned URL — and breaks the command-line half, passing
the access key and the secret key positionally to `mc alias set` in both Compose files and three smoke scripts.
Every reference carries the evidence for its own topic with the file it came from. Those are observations of one
consumer, never platform policy, and never a precedent for a new bucket.

## Routing

Read `references/00-topic-map.md` and load only the file whose triggering condition matches the task in front of
you. Do not read the others.

## When the store fails

1. **Unreachable.** Report the storage dependency not-ready, refuse the write with a retryable error, and refuse a
   read you cannot confirm. Never convert a failed existence check into "the object is absent": that conversion is
   what deletes a tenant's data.
2. **A write whose response never arrived.** Treat it as unknown rather than failed, hold the database row
   pending, and let a reconciliation pass re-check the key. A repeated `PUT` to the same key is safe because the
   key determines the object; a repeated multipart completion is not, so re-check before completing again.
3. **A delete you cannot confirm.** Hold the row pending-deletion and retry, and never mark it deleted on an
   unconfirmed response, because that orphans bytes no query will find again. Where a lifecycle rule owns the
   removal, record that and stop retrying.

Retry counts, backoff shape, breaker thresholds and degradation policy are `/alaa-reliability-sla`
(`$alaa-reliability-sla`); this section states only what a failure is allowed to mean.

## Checker and output

`python3 scripts/check_object_storage_posture.py --root <repo>`, with `--help` for the check list and `--self-test`
for its own fixtures. It reads files lexically and contacts no object store, so a clean run proves what the
repository declares and not how the running bucket is configured.

- exit `0`: no finding. Continue to the service's own tests.
- exit `1`: findings printed with file and line. Fix each one, or record it as an accepted defect with an owner and
  a date, before shipping.
- exit `2`: bad arguments or an unreadable root, so nothing was checked. Correct the invocation and rerun.
- exit `3`: `--self-test` failed, so its verdicts are untrustworthy. Report the failing case and review by hand.

Report the bucket, the key template with its tenant segment shown, every lifecycle rule with its window, the
identity and its policy statements, the transport, encryption, versioning and replication state, and the credential
source and rotation procedure — each marked implemented, declared-but-absent, or not-applicable with a reason. Give
the checker's exit code, cite every upstream API claim with its read date, and state an unverified claim as
unverified.

## Not owned here

| You are about to | Use |
|---|---|
| choose between Postgres and Redis, design a table or index, or tune a query, pool or cache | `/alaa-data-layer` (`$alaa-data-layer`) |
| shape a retry, backoff, timeout, breaker, idempotency key or degradation policy | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| name a metric, log field, event, error code or header, or use an Ala platform value such as a timeout or retry budget | `/alaa-services-contract` (`$alaa-services-contract`) `references/22-failure-load-and-deprecation-contract.md` |
| decide whether telemetry is required, or which gate it must pass | `/alaa-observability-soc` (`$alaa-observability-soc`) |
| trigger a security review, classify a threat, or apply fail-closed doctrine | `/alaa-security-review` (`$alaa-security-review`) |
| write a Dockerfile, Compose file or Swarm stack, or harden an image | `/alaa-docker-production` (`$alaa-docker-production`) |
| write a Kubernetes manifest or a Helm chart | `/alaa-k8s-helm` (`$alaa-k8s-helm`), Arvan specifics in `/caas-arvan-kuber` (`$caas-arvan-kuber`) |
| change an HAProxy directive in front of the store | `/alaa-haproxy` (`$alaa-haproxy`) |
| decide which layer a behaviour is tested at, or what proof a claim reached | `/alaa-testing-strategy` (`$alaa-testing-strategy`) `references/40-proof-strength.md` |
| size a tus part, build an upload-session key, or retain an unfinished upload | `/tusd-upload-platform` (`$tusd-upload-platform`) |
| check work against the ten-point quality bar | `/alaa-project-constitution` (`$alaa-project-constitution`) `references/quality-bar.md` |
| point a bucket or client at an ArvanCloud endpoint, choose an Arvan region, or check whether an S3 operation works on ArvanCloud | `/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`) |
| choose a model or an effort level | `/alaa-prompting-guide` (`$alaa-prompting-guide`) |
