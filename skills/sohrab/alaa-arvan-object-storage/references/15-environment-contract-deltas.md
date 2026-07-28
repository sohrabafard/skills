# Environment Contract: the ArvanCloud Deltas

Read this when a service's `STORAGE_ENDPOINT` points at an `arvanstorage.ir` host. The variable names, the
validation rules, the evidence markers and every default not restated here are
`/alaa-minio-object-storage` (`$alaa-minio-object-storage`) `references/05-environment-contract.md`, which owns the
family. **Use the names in that file unchanged on ArvanCloud**, because a service that moves from MinIO to Arvan
must change env values only, and a second set of names would turn that move into a code change.

Only the values that differ appear below. Where a row is absent from this file, the baseline default governs.

**The delta table below is ArvanCloud's column of the provider-profile table, and it appears in full nowhere else
in this skill.** The mechanism that reads it — what a profile is, the resolution order, the three rules that keep it
safe, the evidence markers and the other providers' columns — is
`/alaa-minio-object-storage` (`$alaa-minio-object-storage`) `references/05-environment-contract.md` under "The
provider profile". Read that file before changing how a value is chosen, and this one before changing which value
Arvan gets, because a mechanism restated here would drift from the file that owns it.

## The deltas

| Variable | Baseline default | ArvanCloud default | Evidence for the ArvanCloud default | A wrong value causes |
|---|---|---|---|---|
| `STORAGE_PROVIDER_PROFILE` | required, no default | `arvancloud` | this skill's stated default: `arvancloud` is the profile whose column carries the values in this table | another profile hands AWS's 5 GiB part ceiling and MinIO's path-style default to an Arvan endpoint, so a part is rejected after it crossed the network and edge caching is lost with no error at all |
| `STORAGE_ENDPOINT` | required, no default | `https://s3.ir-thr-at1.arvanstorage.ir` for Simin, or `https://s3.ir-tbz-sh1.arvanstorage.ir` for Shahriar | published by ArvanCloud and read on 2026-07-28 `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/, read: 2026-07-28]` | a bucket is reachable only at its own region's endpoint, so the other endpoint returns a not-found identical to a deleted object |
| `STORAGE_REGION` | `us-east-1` | `ir-thr-at1`, paired with the endpoint it belongs to | published by ArvanCloud and read on 2026-07-28 `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/, read: 2026-07-28]` | the AWS-shaped baseline region reaches a namespace where the bucket does not exist |
| `STORAGE_USE_PATH_STYLE` | `true` | `false` | published by ArvanCloud and read on 2026-07-28: the Virtual Host format `[bucketname].s3.[region].arvanstorage.ir` is stated as required for CDN caching `[source: https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-28]` | `true` loses edge caching with no error, so the cost arrives as a traffic bill rather than a failed request |
| `STORAGE_TLS_ENABLED` | `false` | `true` | this skill's stated default, following `/alaa-minio-object-storage` (`$alaa-minio-object-storage`) constraint 6, because no `arvanstorage.ir` host is a loopback address | a plaintext hop to a public endpoint exposes the object bytes and the signed request across the open internet |
| `STORAGE_MAX_PART_SIZE_BYTES` | `5368709120`, which is 5 GiB | `400000000` | published by ArvanCloud and read on 2026-07-28 as a 400 MB part ceiling, taken at its smaller reading `[source: https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-28]` | a part size copied from an AWS or MinIO guide is rejected only after the bytes crossed the network |
| `STORAGE_MAX_OBJECT_BYTES` | `5000000000000`, which is 5 TB | `4000000000000`, which is 4 TB | derived below from ArvanCloud's own conflicting published numbers by the minimum rule | an object accepted above the reachable ceiling fails at completion, after every part was uploaded and billed |
| `STORAGE_SIGNATURE_VERSION` | `s3v4` | `s3v4`, the same value on different evidence | this skill's conservative estimate pending confirmation: ArvanCloud publishes no statement that v4 is required or that v2 is accepted, and every reachable ArvanCloud SDK example sets no signature option at all, which signs v4 by SDK default `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/credentials/, read: 2026-07-28]` `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/multipart-upload/, read: 2026-07-28]` | a mismatch returns `SignatureDoesNotMatch`, which reads as a wrong secret key and sends the investigation to key rotation |
| `STORAGE_MULTIPART_ABORT_DAYS` | `7` | `7`, and the client-side abort is mandatory alongside it | published by ArvanCloud and read on 2026-07-28: the abort is described as the uploader's job with no automatic cleanup `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/multipart-upload/, read: 2026-07-28]`, and Arvan's support for the `AbortIncompleteMultipartUpload` lifecycle action is unverified | relying on the lifecycle rule alone leaves abandoned parts billed on a store that may never run the rule |

## Why the object ceiling is 4 TB

ArvanCloud publishes four numbers that cannot all hold at once, and one of them is published twice at two different
sizes.

1. A maximum object size via multipart of 5 TB `[source: https://docs.arvancloud.ir/en/object-storage/limits/,
   read: 2026-07-28]`.
2. A maximum part size of 400 MB, same source.
3. A maximum of 10,000 parts per upload, same source.
4. A worked multipart example in ArvanCloud's own SDK documentation that sets
   `long partSize = 400 * (long)Math.Pow(2, 20); // 400 MB`, which is 419,430,400 bytes
   `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/multipart-upload/, read:
   2026-07-28]`. That is 400 mebibytes labelled as 400 megabytes, so the vendor's prose ceiling and the vendor's
   own code disagree by 19,430,400 bytes.

**Where the provider's published numbers conflict, this skill's default is the minimum of them, because a ceiling
set to the smaller figure fails locally before any byte is sent and a ceiling set to the larger figure fails after
the whole part crossed the network.** Applying that rule twice:

```
part ceiling      = min(400,000,000, 419,430,400)          = 400,000,000 bytes
derived object    = 400,000,000 x 10,000                   = 4,000,000,000,000 bytes
published object  =                                          5,000,000,000,000 bytes
effective ceiling = min(4,000,000,000,000, 5,000,000,000,000) = 4,000,000,000,000 bytes
```

**Carry 4 TB, which is 4,000,000,000,000 bytes, as the effective ceiling, and design nothing above it until open
question 5 in `references/SOURCES.md` is answered.** The advertised 5 TB is unreachable with any part size Arvan
accepts: reaching 5 TB in 10,000 parts needs parts of at least 500,000,000 bytes, and Arvan's ceiling is 400 MB.

**Leave `STORAGE_MIN_PART_SIZE_BYTES` at the baseline 5,242,880 bytes on ArvanCloud, and do not lower it to
5,000,000.** Arvan publishes the floor as 5 MB with the same megabyte ambiguity `[source:
https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-28]`, and 5,242,880 is accepted under both
readings while 5,000,000 is accepted under only one. The principle is the same one that produced the 4 TB ceiling:
take the figure that cannot be wrong in the direction that costs a transmitted part.

## The profile is a set of defaults, and never a branch

**No service reads `STORAGE_PROVIDER_PROFILE` to decide what to do on ArvanCloud, in any language and at any
layer.** A branch on `arvancloud` means every service holding one needs a code change on the day the fleet adopts a
fourth provider, which is the cost the profile exists to remove; a service reads the resolved `STORAGE_*` values
instead and behaves the same everywhere.

**When Arvan needs behaviour that no existing knob expresses, add a new `STORAGE_*` variable to
`/alaa-minio-object-storage` (`$alaa-minio-object-storage`) `references/05-environment-contract.md` with a default
in every profile column, and write no branch.** Constraint 5 of this skill's `SKILL.md` is the live example: the
client-side multipart abort is mandatory on Arvan and optional elsewhere, so the shape that carries it is a boolean
variable defaulted on in the `arvancloud` column and off where a lifecycle rule is proven, added to the file that
owns the family. The variable costs one row there and one env value per environment that disagrees with its
profile; the branch costs a code change in every service, forever.

## What is still unsettled here

**Whether ArvanCloud accepts path-style addressing at all is unverified**, which is open question 2 in
`references/SOURCES.md`. **Set `STORAGE_USE_PATH_STYLE` to `false` on Arvan, and record the reason beside the
value when a specific failure forces it to `true`**, because path-style loses edge caching silently rather than
returning an error, so nothing in the request path reports the cost.

**Whether Signature Version 2 is accepted is unverified**, which is open question 1. **Change
`STORAGE_SIGNATURE_VERSION` only after a client has been observed reaching the endpoint successfully with the new
value, and never as a way of clearing an authentication error**, because flipping it can replace one signing
failure with a different one and leave the real cause in place.

**No maximum presigned-URL lifetime is published for ArvanCloud.** The only figure in Arvan's documentation is a
12-hour example `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/upload-presigned/, read:
2026-07-28]`, which is an example rather than a limit. **Leave `STORAGE_PRESIGN_MAX_SECONDS` at the baseline 900
seconds on Arvan**, because an unpublished ceiling is not evidence that a longer link is honoured, and the
consequence of guessing high is an unrevocable bearer credential outliving its need.

## Not owned here

Variable names, validation rules, evidence markers, every baseline default, and the provider-profile mechanism
with its resolution order and its other providers' columns: `/alaa-minio-object-storage`
(`$alaa-minio-object-storage`) `references/05-environment-contract.md`. The full Arvan limit table and the cost
model those numbers feed: `references/30-limits-quotas-and-cost.md`. Endpoint, region and credential doctrine:
`references/10-connection-identity-and-addressing.md`.
