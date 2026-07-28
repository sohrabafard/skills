# S3 Compatibility Matrix

Read this before calling an S3 operation against an `arvanstorage.ir` endpoint. Every row states what ArvanCloud's own
documentation shows on the read date, not what S3 or MinIO does.

## How to read the status column

Four statuses, and the difference between the last three is the whole point of this file.

- **Supported** — an ArvanCloud page documents the operation and its content was retrieved and read.
- **Documented, unread** — a page for the operation exists under that name in ArvanCloud's documentation index, but its
  content could not be retrieved, so the operation is documented and its behaviour is not established.
- **Not documented** — searching ArvanCloud's documentation found no page. **This does not mean the operation is
  absent**; Arvan documents a subset of the S3 surface, and an undocumented operation may still work.
- **Conflicting** — two ArvanCloud sources disagree, and the row names both.

**Before depending on any row that is not Supported, run the operation against a scratch bucket in the target region
and record the result with its date.** A matrix row is documentation evidence; only a call against the live endpoint is
behaviour evidence, and the two diverge on this provider.

## The matrix

| Operation | Status | What the source shows |
|---|---|---|
| `PutObject` (single request) | Supported | Capped at 5 GB per upload request `[source: https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-27]`; operation page indexed at `.../sdk/object-storage/upload-object/` |
| `GetObject` | Documented, unread | Page indexed as "Download File from Bucket" `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/download-object/, read: 2026-07-27]` |
| `DeleteObject` | Not documented | No page found in the searches recorded in `SOURCES.md` |
| `ListObjects` / `ListObjectsV2` | Not documented | No page found; Arvan recommends third-party tools such as s3cmd for buckets with large object counts `[source: https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-27]` |
| `CreateMultipartUpload` | Supported | Documented as initiating the multipart process `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/multipart-upload/, read: 2026-07-27]` |
| `UploadPart` | Supported | Same page; the worked example sets `long partSize = 400 * (long)Math.Pow(2, 20)`, which is 419,430,400 bytes labelled as 400 MB and therefore larger than the published 400 MB ceiling — see `references/15-environment-contract-deltas.md` |
| `CompleteMultipartUpload` | Supported | Same page |
| `AbortMultipartUpload` | Supported | Same page, in the error-handling path; Arvan states the uploader must abort to release stored volume and describes no automatic cleanup |
| `ListMultipartUploads` | Not documented | Absent from the multipart page; **this is the operation that finds orphaned parts**, so budget reconciliation may have no listing to work from |
| `ListParts` | Not documented | Absent from the multipart page |
| `UploadPartCopy` | Not documented | Absent from the multipart page |
| `CopyObject` | Not documented | No page found; a server-side copy is the normal way to re-key or re-tier an object, so assume download-and-reupload until proven otherwise |
| `PutBucketLifecycleConfiguration` | Supported | Applied through the S3 API with the AWS SDK, never through the panel: a `LifecycleConfiguration` holding `Rules`, each with a `Filter`, a `Status` of `"Enabled"` and an action `[source: https://docs.arvancloud.ir/fa/developer-tools/sdk/object-storage/put-bucket-lifecycle-config/, read: 2026-07-28]`. The English page at the same path is robots-blocked; the Persian page carries the same worked example |
| `Expiration` lifecycle rule | Supported | The only rule type in Arvan's worked example: `Expiration = new LifecycleRuleExpiration { Days = 10 }` under a `LifecyclePrefixPredicate` with `Prefix = "someprefix/"` `[source: https://docs.arvancloud.ir/fa/developer-tools/sdk/object-storage/put-bucket-lifecycle-config/, read: 2026-07-28]` |
| `AbortIncompleteMultipartUpload` lifecycle rule | Not documented | The lifecycle page was read on 2026-07-28 and shows only `Expiration`, so this action is absent from the documentation rather than shown as unsupported `[source: https://docs.arvancloud.ir/fa/developer-tools/sdk/object-storage/put-bucket-lifecycle-config/, read: 2026-07-28]`. **The MinIO skill's mandatory abort rule cannot be assumed to work here**, which is why client-side abort is constraint 5 in `SKILL.md` |
| `NoncurrentVersionExpiration` lifecycle rule | Not documented | Absent from the lifecycle page read on 2026-07-28, while versioning is supported, so **a versioned Arvan bucket has no proven way to expire superseded versions** and its stored volume grows with no change in object count |
| `Transition` lifecycle rule | Not documented | Absent from the lifecycle page read on 2026-07-28, and no storage class beyond the default appears anywhere in Arvan's documentation, so treat tiering as unavailable |
| `PutBucketVersioning` | Supported | Versioning is enabled per bucket from the panel, free, and off by default `[source: https://docs.arvancloud.ir/en/object-storage/buckets/versioning, read: 2026-07-27]` |
| `GetBucketVersioning` | Documented, unread | Page indexed as "Get Object Versioning Status" `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/get-bucket-versioning/, read: 2026-07-27]` |
| `PutBucketPolicy` | Supported | AWS IAM policy shape with `Version`, `Statement`, `Sid`, `Effect`, `Principal`, `Action`, `Resource`; example uses `s3:GetObject`, `Principal: "*"`, `arn:aws:s3:::sample_bucket/user_*` `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/put-bucket-policy/, read: 2026-07-27]` |
| `GetBucketCors` | Supported | Rules expose `ID`, `MaxAgeSeconds`, `AllowedMethods`, `AllowedOrigins`, `AllowedHeaders`, `ExposeHeaders` `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/get-bucket-cors/, read: 2026-07-27]` |
| `PutBucketCors` / `DeleteBucketCors` | Not documented | Only the get operation is documented, so **a browser-direct upload flow may have no supported way to set CORS by API** and may require the panel |
| Presigned URL (GET and PUT) | Supported | Generated with the standard SDK presign call against the Arvan service URL; expiry expressed in hours with a 12-hour example, and no maximum lifetime stated `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/upload-presigned/, read: 2026-07-27]` |
| Server-side encryption | Conflicting | The product page lists "client-side and server-side encryption" `[source: https://www.arvancloud.ir/en/products/cloud-storage, read: 2026-07-27]`, and no SSE operation, header or key-management page appears in the SDK documentation. Treat SSE as unproven and encrypt client-side where the data requires it |
| Object tagging (`PutObjectTagging`) | Not documented | Bucket-level tags exist in the panel `[source: https://docs.arvancloud.ir/en/object-storage/buckets, read: 2026-07-27]`; object tagging was not found |
| Object Lock / retention | Not documented | No page found; do not promise WORM or compliance retention on Arvan |
| Bucket replication | Not documented | No page found; the product page's "multi-region" claim is about region availability, not bucket replication |
| Bucket / object ACLs | Not documented | Access is a bucket-level public toggle rather than a documented ACL API `[source: https://docs.arvancloud.ir/en/object-storage/buckets, read: 2026-07-27]` |
| Static website hosting | Supported | Configurable per bucket with index and error objects `[source: https://docs.arvancloud.ir/en/object-storage/buckets, read: 2026-07-27]` |
| Custom domain and CDN | Supported | Arvan Object Storage uses the Arvan CDN by default; a custom domain needs the domain on Arvan CDN with HTTPS active, then an ANAME for a root domain or a CNAME for a subdomain, with the host header rewritten to `bucketname.s3.<region>.arvanstorage.ir` `[source: https://docs.arvancloud.ir/en/object-storage/buckets/custom-domain, read: 2026-07-27]` |

## The three rows most likely to cost you

1. **`AbortIncompleteMultipartUpload` is absent from the lifecycle page that documents `Expiration`.** Abandoned
   parts are billed and appear in no object listing, and `ListMultipartUploads` is also undocumented, so on Arvan
   there may be neither an automatic sweeper nor a way to enumerate what to sweep. **Abort from the client on every
   failed upload**, and treat the lifecycle rule as an unproven second layer. **Apply the expiration rule anyway**,
   because that rule type is documented and it bounds the objects the abort rule would not have covered.
2. **`CopyObject` is not documented.** Any design that re-keys objects — a tenant rename, a key-scheme migration, a
   move between prefixes — must budget for download-and-reupload bandwidth and time until a server-side copy is proven
   against the live endpoint.
3. **`PutBucketCors` is not documented.** A browser-direct upload against a presigned PUT needs CORS on the bucket;
   confirm the panel can set it before designing a flow that depends on it.

## Public access and delivery

Public access is a bucket-level toggle whose off-switch does not cascade to existing objects, and every public object
is served through the Arvan CDN by default. Both rules, with their reasons and citations, are `SKILL.md` constraints 8
and 9 and are not restated here.

**After turning public access off, verify a sample of previously public keys returns a denial.** The bucket setting
alone is not evidence that the objects followed it, and this verification step is the only part of the delivery rules
that is not in the body.

The rule that a bucket of user-supplied bytes is not publicly readable at all is `/alaa-minio-object-storage`
(`$alaa-minio-object-storage`) constraint 7 and holds here; this section governs the buckets that are deliberately
public, such as static assets.
