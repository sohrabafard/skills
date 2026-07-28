---
name: alaa-arvan-object-storage
description: "ArvanCloud Object Storage differences layer over the fleet's shared S3 and MinIO platform policy: the regional endpoints and their isolation, virtual-hosted addressing, the account-level key model, an S3 compatibility matrix of supported, partial, absent and unverified operations, the 400 MB part ceiling and the other Arvan limits, CDN-fronted public access, and porting a bucket or client between MinIO and Arvan. Use when pointing a service at an arvanstorage.ir endpoint, choosing an Arvan region, setting a `STORAGE_*` value whose Arvan default differs from the baseline, sizing a multipart part, writing an Arvan lifecycle rule, rotating an access key, or migrating objects between the two stores. Do not use it for bucket and object-key design, lifecycle mechanics, presigned-URL policy or failure classes, which /alaa-minio-object-storage owns, or for Arvan's managed Kubernetes, which is /caas-arvan-kuber."
---

# Alaa ArvanCloud Object Storage

This skill states only what ArvanCloud Object Storage does differently from S3 and MinIO, and what breaks for an agent
who assumes AWS or MinIO behaviour. Everything shared — key design, tenant scoping, lifecycle mechanics, multipart
strategy, presigned-URL policy, credential hygiene, failure classes and observability — lives in
`/alaa-minio-object-storage` (`$alaa-minio-object-storage`) and is not repeated here.

## Read that skill first, then this one

Apply the nine constraints of `/alaa-minio-object-storage` (`$alaa-minio-object-storage`) as the baseline. Return here
when the endpoint host ends in `arvanstorage.ir`, or when the task moves data or a client between MinIO and ArvanCloud.
Where the two disagree, this skill wins for Arvan endpoints only, and every disagreement appears below with its reason.

## When not to use this skill

Do not load this skill when no endpoint host in the task ends in `arvanstorage.ir` and no data or client moves between
MinIO and ArvanCloud, because it adds provider constraints that do not apply and the shared rules already live in
`/alaa-minio-object-storage` (`$alaa-minio-object-storage`). Do not use it to decide whether object storage is the
right store for a fact at all, which is `/alaa-data-layer` (`$alaa-data-layer`). Do not use it for Arvan's managed
Kubernetes, its CaaS RBAC or its container registry, which is `/caas-arvan-kuber` (`$caas-arvan-kuber`): that skill
owns Arvan's compute platform and this one owns Arvan's object storage, and neither states a rule about the other's
surface.

## Constraints that hold on every Arvan task

1. **Pin the regional endpoint host in configuration, and let no client fall back to a default region.** A bucket is
   reachable only at its own region's endpoint `[source: https://docs.arvancloud.ir/en/object-storage/limits/, read:
   2026-07-27]`, and the wrong region returns a not-found identical to a deleted object, so the fault reads as data
   loss.
2. **Fix the region and the bucket name before creating the bucket, and treat both as permanent.** Neither can change
   afterwards `[source: https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-27]`, so the only
   correction is copying every object into a new bucket.
3. **Set `STORAGE_MAX_PART_SIZE_BYTES` to `400000000` on every Arvan endpoint, and keep every part at or below
   it.** Arvan's part ceiling is published as 400 MB `[source:
   https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-28]` where AWS S3 allows 5 GB, so a part
   size taken from an AWS or MinIO guide is rejected only after the bytes crossed the network. The value is
   `400000000` rather than `419430400` because Arvan's own example labels 400 mebibytes as 400 MB and the smaller
   reading is the one that cannot be exceeded by accident — `references/15-environment-contract-deltas.md` carries
   the arithmetic.
4. **Send any payload above 5 GB as a multipart upload**, because one upload request is capped at 5 GB `[source:
   https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-27]`.
5. **Abort a failed multipart upload from the client as well as from the lifecycle rule the MinIO skill requires.**
   Arvan makes the abort the uploader's job and describes no automatic cleanup `[source:
   https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/multipart-upload/, read: 2026-07-28]`, and
   `AbortIncompleteMultipartUpload` is absent from the lifecycle page that documents `Expiration` `[source:
   https://docs.arvancloud.ir/fa/developer-tools/sdk/object-storage/put-bucket-lifecycle-config/, read:
   2026-07-28]`, so the rule alone is not proven on this provider.
6. **Apply an Arvan lifecycle rule through the S3 API, and expect no lifecycle control in the panel.** Arvan
   documents `PutBucketLifecycleConfiguration` through the AWS SDK with an `Expiration` action, a prefix `Filter`
   and a `Status` of `"Enabled"` `[source:
   https://docs.arvancloud.ir/fa/developer-tools/sdk/object-storage/put-bucket-lifecycle-config/, read:
   2026-07-28]`, and its documented panel settings cover public access, tags, CDN caching and static website
   hosting only `[source: https://docs.arvancloud.ir/en/object-storage/buckets, read: 2026-07-28]`. An operator
   sent to the panel to set a lifecycle rule will not find one there.
7. **Treat every Arvan access key as account-wide, and separate services by Arvan account or bucket policy rather than
   by key scope.** The documented credential is one Access Key and Secret Key belonging to the user account `[source:
   https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/credentials/, read: 2026-07-27]` with no documented
   scoped machine user, so MinIO constraint 1 cannot be met by key scope and a leaked key exposes every bucket.
8. **After switching a bucket's public access off, re-check every object that was public while it was on.** The change
   "will not be applied to all of the objects present in the bucket" `[source:
   https://docs.arvancloud.ir/en/object-storage/buckets, read: 2026-07-27]`, so objects stay readable afterwards.
9. **Purge the CDN cache as part of any delete or overwrite of a publicly readable object.** Arvan Object Storage uses
   the Arvan CDN by default `[source: https://docs.arvancloud.ir/en/object-storage/buckets/custom-domain, read:
   2026-07-27]`, so a deleted object is still served from the edge until its cache entry expires.
10. **Set `STORAGE_USE_PATH_STYLE` to `false` on every Arvan endpoint, so buckets are addressed virtual-hosted as
    `<bucket>.s3.<region>.arvanstorage.ir`.** Arvan states the virtual host format is required for CDN caching
    `[source: https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-28]`, and a client forced to
    path-style loses edge caching silently instead of failing, so the cost arrives as a traffic bill.
11. **Re-read any provider fact here whose read date is more than 90 days old before relying on it for a production
    change.** ArvanCloud moves its compatibility surface and limits with no changelog this skill can follow, so an
    unchecked fact is a guess wearing a citation.

## Routing

Load only the file whose condition matches the task in front of you. Do not read the others.

| You are about to | Read |
|---|---|
| point a client at an Arvan endpoint, choose a region, set addressing style or signature version, or issue and rotate a key | `references/10-connection-identity-and-addressing.md` |
| set a `STORAGE_*` environment value for an Arvan endpoint, or choose a default that differs from the shared baseline | `references/15-environment-contract-deltas.md` |
| set `STORAGE_PROVIDER_PROFILE` for an Arvan endpoint, or decide whether an Arvan-only behaviour is a new `STORAGE_*` knob or a branch on the provider name | `references/15-environment-contract-deltas.md` |
| call an S3 operation against Arvan and need to know whether it works, works partly, or is absent | `references/20-s3-compatibility-matrix.md` |
| size a part, a bucket or an object count, hit a quota, or explain an Arvan storage or traffic bill | `references/30-limits-quotas-and-cost.md` |
| copy objects between MinIO and Arvan, or write one client that must run against both | `references/40-migration-and-portability.md` |
| repeat a provider claim from this skill, or re-check one past its 90-day freshness window | `references/SOURCES.md` |

## Configuration checker

`python3 scripts/check_arvan_storage_config.py --root <repo>`, with `--help` for the check list and `--self-test` for
its own fixtures. It reads files lexically and contacts no endpoint, so a clean run proves what the repository declares
and not how the live bucket behaves. Exit `0` no finding; exit `1` findings printed with file and line, each fixed or
recorded as an accepted defect with an owner and a date before shipping; exit `2` bad arguments or an unreadable root,
so nothing was checked and the invocation is rerun; exit `3` `--self-test` failed, so its verdicts are untrustworthy
and the failing case is reviewed by hand.

## Not owned here

| You are about to | Use |
|---|---|
| design a bucket or object key, scope a key to a tenant, write a lifecycle rule, issue a presigned URL, classify a storage failure, or measure the store | `/alaa-minio-object-storage` (`$alaa-minio-object-storage`) |
| choose between Postgres, Redis and object storage, or design a table, index or cache | `/alaa-data-layer` (`$alaa-data-layer`) |
| run a workload on Arvan's managed Kubernetes, or write an Arvan CaaS manifest, chart or RBAC binding | `/caas-arvan-kuber` (`$caas-arvan-kuber`) |
| trigger a security review, classify a threat, or apply fail-closed doctrine to a credential or public bucket | `/alaa-security-review` (`$alaa-security-review`) |
| write a Dockerfile, Compose file or Swarm stack, or harden an image | `/alaa-docker-production` (`$alaa-docker-production`) |
| write a Kubernetes manifest or a Helm chart | `/alaa-k8s-helm` (`$alaa-k8s-helm`) |
| name a metric, log field, event, error code or header, or use an Ala timeout or retry budget | `/alaa-services-contract` (`$alaa-services-contract`) |
