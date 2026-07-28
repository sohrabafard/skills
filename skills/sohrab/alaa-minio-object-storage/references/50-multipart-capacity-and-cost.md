# Multipart, capacity and cost

This file owns what a multipart upload costs the process performing it and what a bucket costs the account holding
it. Read it before choosing a part size, before sizing the disk or memory of an uploading process, and before
setting a quota.

## Multipart mechanics

A multipart upload is three calls: `CreateMultipartUpload` returns an upload ID, `UploadPart` writes numbered
parts, and `CompleteMultipartUpload` assembles them into one object. Until the completion call returns, **no object
exists at the destination key** — a listing shows nothing and a `GET` returns not-found. The parts, however, are
already stored and already billed
`[source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html, read: unverified as of
2026-07-27]`.

Two consequences follow. **Never infer from an absent object that no upload is in progress**; ask
`ListMultipartUploads`. And **every bucket that receives multipart uploads needs the abort rule** in
`20-lifecycle-and-retention.md`, because a client that never calls completion or abort leaves those parts forever.

The documented S3 limits are a 5 MiB minimum for every part except the last, a 5 GiB maximum part, 10,000 parts per
upload, and a 5 TiB maximum object
`[source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html, read: unverified as of 2026-07-27]`.

## Choosing a part size

The part count is `ceil(objectSize / partSize)` and must not exceed the parts limit, so **the minimum viable part
size is `maxObjectSize / 10000`** — 512 KiB per 5 GiB of object, 5 MiB per 50 GiB. Below that the upload fails at
part 10,001, late, after the bytes were already sent.

Above the minimum, a larger part means fewer requests and a cheaper retry-free path; a smaller part means less
memory in flight and a cheaper retry when one part fails. **State the largest object size the endpoint accepts
first**, then choose the smallest part size that keeps the part count inside the limit for that size, then round up
to whatever the buffering budget below allows.

**Read the part size from `STORAGE_PART_SIZE_BYTES` and the bounds from `STORAGE_MIN_PART_SIZE_BYTES`,
`STORAGE_MAX_PART_SIZE_BYTES` and `STORAGE_MAX_PARTS`, and validate the part size against those bounds before the
client is constructed.** Every one of those four numbers is a provider limit that differs between MinIO and
ArvanCloud, so each is an environment value with a stated default rather than a constant in code —
`05-environment-contract.md` owns them and `/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`)
`references/15-environment-contract-deltas.md` states where Arvan's differ.

## The local cost of an in-flight upload

A server-side uploader buffers parts before sending them. The demand is:

```
bytes in flight per upload = partSize x concurrentPartUploads x bufferedParts
```

That number, times the number of simultaneous uploads a process accepts, is the local disk or memory the process
needs. **Read the concurrency from `STORAGE_UPLOAD_CONCURRENCY`, whose stated default is 4**, because the value
that fits a development container and the value that fits a production node are different numbers and neither is a
property of the code. **Every deployment performing multipart uploads states where those bytes live and bounds how many uploads
may be in flight**, because the failure mode is a full disk or an OOM kill that takes down every request on the
process, not just the upload that caused it.

**Give the temp location a real volume or a sized tmpfs, and never let it default to the container's writable
layer**, which is usually small, unmonitored, and shared with the log output.

On the fleet's only object-storage consumer, no part-size or concurrency override appears anywhere in the
repository, so the upstream library defaults are in effect: a 5 MiB minimum part, a 50 MiB preferred part, a 5 GiB
maximum part, 10,000 parts, a 5 TiB maximum object, ten concurrent part uploads and twenty buffered parts. That is
approximately 1 GiB of local temp demand per in-flight upload, on a container with no volume, no tmpfs and no
disk-pressure guard `[source: tusd-upload-platform repository — the absence of any override was verified this
session; the upstream default values were taken from the tusd v2.8.0 S3 store and are marked unverified because the
module source was out of scope for this session, read: 2026-07-27 for the repository, unverified for the upstream
defaults]`.

Part sizing driven by the tus protocol, and the temp-disk formula as an upload-plane concern, belong to
`/tusd-upload-platform` (`$tusd-upload-platform`). This file owns the storage-side limits those choices must fit
inside.

## The two-copy window

A finalization step that copies an object from a staging key to a final key holds both copies until the staging key
is deleted. **Size the bucket for the peak of both**, and make the staging-key deletion a step that cannot be
skipped — either an explicit delete in the same unit of work, or a lifecycle rule filtered to the staging prefix.
Where the copy is server-side, the bytes never traverse the application, but both objects are still billed.

## Quota, capacity and what a full store looks like

**Set a bucket quota where the store supports one**, so a runaway producer fails its own writes instead of filling
the volume under every other bucket.

A full store returns a server error on write, not a specific "disk full" code, so it presents as an intermittent
5xx and gets misdiagnosed as a network problem. `90-failure-classes.md` carries the diagnosis. Track free capacity
as a leading signal — see `95-observability.md`.

## The cost model

Four things cost money, and only the first is intuitive:

1. Bytes stored, including every noncurrent version and every uploaded part of an incomplete multipart upload.
2. Requests, priced per thousand, which makes a chatty listing loop more expensive than the data it lists.
3. Egress, which is where a download path that proxies through the application costs twice — once out of the store
   and once out of the service.
4. Lifecycle transitions between storage classes, priced per object, which makes a transition rule uneconomic for
   many small objects.

**Estimate all four before promising a cost**, and state which one dominates. A bucket whose cost is dominated by
requests is not fixed by a cheaper storage class.

Complexity budgets for a loop, listing or fan-out that grows with tenants or objects belong to
`/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`).
