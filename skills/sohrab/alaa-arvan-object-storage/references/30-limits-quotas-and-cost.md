# Limits, Quotas and Cost

Read this when sizing a part, a bucket or an object count, when a call fails at a boundary, or when explaining an Arvan
storage or traffic bill. Multipart strategy and capacity planning in general are `/alaa-minio-object-storage`
(`$alaa-minio-object-storage`) `references/50-multipart-capacity-and-cost.md`; only the Arvan numbers and the decisions
they change are here.

## The published limits

Every number in this table comes from one page
`[source: https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-28]`, except the two carried byte
values, which are derived below.

| Limit | Arvan value | AWS S3 value for contrast |
|---|---|---|
| Maximum single upload request | 5 GB | 5 GB |
| Maximum object size via multipart | 5 TB published, `4000000000000` bytes carried | 5 TB |
| **Maximum part size** | **400 MB**, carried as `400000000` bytes | **5 GB** |
| Minimum part size | 5 MB | 5 MB |
| Maximum parts per upload | 10,000 | 10,000 |
| Buckets per account, default | 50, increase on request | 100 soft |
| Objects per bucket | 3,700,000 | no documented limit |
| Bucket name length | 3 to 63 characters | 3 to 63 characters |

## What these numbers change

The 400 MB part cap is `SKILL.md` constraint 3 and is not restated here. It is the only limit in the table stricter
than AWS S3, and it is the one an agent carries over wrongly, because part sizes are usually copied from an AWS tuning
note. The failure arrives after the part has been transmitted, so the cost is bandwidth and time, not just an error.

**Compute the maximum object size your part size actually permits, and check it against the largest object the
service will store.** Part size multiplied by 10,000 is the ceiling: an 8 MB part reaches 80 GB, and reaching the
full 5 TB would need parts of at least 500 MB, which exceeds Arvan's 400 MB ceiling.

**Carry 4,000,000,000,000 bytes, which is 4 TB, as the effective object ceiling, and not the advertised 5 TB.**
Arvan's published numbers conflict, and this skill's rule is that the default is the minimum of conflicting
published figures, because the smaller value fails locally before any byte is sent while the larger fails after a
whole part crossed the network. A fourth figure deepens the conflict: Arvan's own multipart example sets
`400 * (long)Math.Pow(2, 20)`, which is 419,430,400 bytes, and labels it 400 MB `[source:
https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/multipart-upload/, read: 2026-07-28]`, so the
vendor's prose and the vendor's code disagree about the size of a megabyte.
`references/15-environment-contract-deltas.md` carries the full arithmetic, and `STORAGE_MAX_OBJECT_BYTES` and
`STORAGE_MAX_PART_SIZE_BYTES` carry the two values. **Raise open question 5 before designing for anything larger
than 4 TB.**

**Use multipart for any payload above 500 MB.** Arvan recommends multipart above that size
`[source: https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-27]`, and constraint 4 in `SKILL.md`
makes it mandatory above 5 GB.

**Plan a bucket to stay under 3,700,000 objects, and shard by a key prefix scheme decided before the first write.**
Splitting a bucket after it fills means copying objects with no documented server-side copy, per
`references/20-s3-compatibility-matrix.md`. Key-namespace design itself is `/alaa-minio-object-storage`
(`$alaa-minio-object-storage`) `references/10-buckets-and-object-keys.md`.

**Count buckets against the 50-bucket default before adopting a bucket-per-tenant design.** A bucket-per-tenant scheme
reaches the default ceiling at 50 tenants and then depends on a support request, so tenant separation by key prefix is
the shape that scales on this provider.

**Retry on `5xx` responses.** Arvan states programs must retry on `5xx`
`[source: https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-27]`. Retry counts, backoff shape and
breaker thresholds are `/alaa-reliability-sla` (`$alaa-reliability-sla`).

## Request rate limits

**No published request-rate or bandwidth-throttle limit was found** — open question 6. **Do not design a burst
workload against an assumed request ceiling; measure the endpoint's behaviour under the intended rate before
committing to it**, and treat a `503` under load as rate limiting rather than an outage until proven otherwise.

## Cost

**Storage and traffic are billed separately, and the free allowance is small.** The Basic plan is documented as 5 GB of
free object storage and 20 GB of free traffic
`[source: https://www.arvancloud.ir/en/products/cloud-storage, read: 2026-07-27]`. **No per-gigabyte storage rate,
per-gigabyte egress rate or per-request charge was found on a primary page** — open question 7 — so **quote no Arvan
storage price in a design document; state the pricing page and the date instead.**

Two cost behaviours are established and change design decisions:

1. **Abandoned multipart parts occupy billed volume until aborted.** Arvan makes the abort the uploader's
   responsibility for releasing that volume
   `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/multipart-upload/, read: 2026-07-27]`.
   **When Arvan storage usage exceeds the sum of object sizes, suspect abandoned parts first**, and see
   `references/20-s3-compatibility-matrix.md` for why they may not be enumerable.
2. **Object versions occupy billed volume, and disabling versioning does not remove the versions already created.**
   Previous versions stay accessible after versioning is disabled, and lifecycle rules keep applying to them
   `[source: https://docs.arvancloud.ir/en/object-storage/buckets/versioning, read: 2026-07-27]`. **Decide the version
   retention window at the same time as enabling versioning**, because a bucket whose versions were never expired grows
   without any change in object count.

**Traffic served through the Arvan CDN is billed as CDN traffic**, and object storage is CDN-fronted by default
`[source: https://docs.arvancloud.ir/en/object-storage/buckets/custom-domain, read: 2026-07-27]`. **Attribute a public
bucket's egress to both products when forecasting**, because the storage bill alone will understate it.
