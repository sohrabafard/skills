# Migration and Portability Between MinIO and ArvanCloud

Read this when copying objects between MinIO and Arvan, or when one client must run against both. The fleet runs both
stores, so a client written against either is expected to work against the other with configuration changes only.

## Write the client to the portable subset

**Restrict a dual-target client to the operations marked Supported in `references/20-s3-compatibility-matrix.md`.**
Everything else is available on MinIO and unestablished on Arvan, so a client using it works in development against
MinIO and fails in production against Arvan. The portable subset established today is `PutObject`, multipart create,
upload, complete and abort, `PutBucketPolicy`, `GetBucketCors`, presigned GET and PUT, and bucket versioning.

**Carry every setting that differs between the two targets in the `STORAGE_*` environment family, never in code, and
use the same variable names against both.** `STORAGE_ENDPOINT`, `STORAGE_REGION`, `STORAGE_USE_PATH_STYLE`,
`STORAGE_TLS_ENABLED`, `STORAGE_SIGNATURE_VERSION`, `STORAGE_MAX_PART_SIZE_BYTES` and `STORAGE_MAX_OBJECT_BYTES` are
the ones that differ, and `references/15-environment-contract-deltas.md` states each Arvan default beside its shared
baseline. **This is what makes the move an env change rather than a code change**, which is the whole reason the two
skills share one family: a client that names these settings differently for each provider has to be rebuilt to move.

**Let no code path branch on a provider name.** A branch on provider acquires a second path that only one
environment ever exercises, so the untested one is discovered in production; a branch on a configuration value is
exercised by whichever environment sets it.

**Set `STORAGE_PART_SIZE_BYTES` to a value at or below 400,000,000 when one binary must serve both targets**, so the
same build satisfies Arvan's part ceiling and MinIO's larger one. See `references/30-limits-quotas-and-cost.md` for
the ceiling and `references/15-environment-contract-deltas.md` for why the byte value is that one.

**Do not rely on a MinIO-only capability without a fallback**: server-side `CopyObject`, `ListMultipartUploads`,
object tagging, object lock and replication are all documented for MinIO and undocumented for Arvan. **When one is
needed, implement the fallback path first and use the fast path only where the target is proven to support it.**

## Testing a dual-target client

**Run the integration suite against both targets before shipping, not against MinIO alone.** MinIO in a local container
is the convenient target and is the one that hides every difference in the matrix. **Where a live Arvan endpoint is
unavailable to the test lane, record which assertions were proven against MinIO only**, because a MinIO pass is not
evidence about Arvan. Proof-strength vocabulary is `/alaa-testing-strategy` (`$alaa-testing-strategy`)
`references/40-proof-strength.md`.

**Point the Arvan lane at a scratch bucket in the target region**, since a bucket is reachable only in its own region
and a test against the wrong region reports not-found rather than a configuration error.

## Copying objects between the two stores

**Copy through a client that reads from the source and writes to the destination; there is no server-side path between
them.** Both stores speak S3, but cross-store copy is a client-mediated transfer, so bandwidth, time and egress cost
belong in the migration plan.

**Size the transfer against the destination's limits, not the source's.** An object stored in MinIO with 1 GB parts is
re-uploaded to Arvan with parts of at most 400 MB, and an object larger than 4 TB may not be expressible on Arvan at
all — see `references/30-limits-quotas-and-cost.md`.

**Preserve the content type and any metadata the application reads, and verify a sample after transfer.** A tool that
copies bytes without metadata produces objects that download correctly and render wrongly, and the defect surfaces in
a browser rather than in the migration log.

**Re-check bucket names for DNS-label validity before creating the destination bucket.** A MinIO bucket name containing
an underscore or an uppercase letter is not creatable on Arvan
`[source: https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-27]`, so the migration renames the bucket
and every reference to it.

**Re-create the access configuration explicitly on the destination; nothing carries over.** Bucket policy, public
access state, CORS, versioning and lifecycle are per-bucket settings on both stores, and versioning in particular is
off by default on Arvan `[source: https://docs.arvancloud.ir/en/object-storage/buckets/versioning, read: 2026-07-27]`.

**Verify the migration by comparing object count and total size per prefix, then by fetching a sample and comparing
checksums.** A completed transfer log is not evidence that the destination is readable.

## Choosing which store a new bucket goes to

This skill does not decide between MinIO and Arvan; that is a placement decision for the owning service. Three
established differences inform it, and each is a fact rather than a recommendation:

- **Arvan is CDN-fronted by default and MinIO is not**, so public asset delivery is cheaper to build on Arvan
  `[source: https://docs.arvancloud.ir/en/object-storage/buckets/custom-domain, read: 2026-07-27]`.
- **MinIO supports scoped identities and Arvan's documented credential is account-wide**, so a workload needing
  per-service credential isolation is simpler on MinIO — see `references/10-connection-identity-and-addressing.md`.
- **Arvan's compatibility surface is partly unestablished**, so a workload depending on lifecycle expiry, server-side
  copy or object lock needs those operations proven against a live Arvan endpoint before the bucket is created there.
