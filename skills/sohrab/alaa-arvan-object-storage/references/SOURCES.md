# Sources and Open Questions

Read this before repeating a provider claim from this skill, or when re-checking a claim past the 90-day freshness
window in `SKILL.md` constraint 11. Every claim in this skill traces to a row below.

## Freshness

**Re-read any page in the first table whose read date is more than 90 days old before relying on its fact for a
production change, and update the read date when you do.** ArvanCloud publishes no changelog for object-storage limits
or API surface that this skill can subscribe to, so age is the only signal available that a fact may have moved.

**When a re-read changes a fact, update the fact, the read date, and every reference file that repeated it in the same
edit.** A skill with one stale copy of a corrected number is worse than one with none, because the stale copy still
reads as cited.

## Pages read for this skill

All read on 2026-07-27.

| URL | What it established |
|---|---|
| https://docs.arvancloud.ir/en/object-storage/limits/ | Every published limit; region isolation; immutable bucket name and region; bucket naming rules; virtual host required for CDN caching; multipart advice above 500 MB; retry on `5xx` |
| https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/ | The two regional endpoint hostnames and the Simin and Shahriar region names; SDK languages covered |
| https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/prerequisite/ | Unmodified AWS SDK packages are the documented clients; no signature or addressing override shown |
| https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/credentials/ | Access Key, Secret Key and endpoint URL come from the dashboard and belong to the user account; no scoped machine user documented |
| https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/multipart-upload/ | Initiate, upload part, complete and abort are documented; abort is the uploader's responsibility; no automatic cleanup described |
| https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/upload-presigned/ | Presigned URL generation via the standard SDK call; expiry in hours with a 12-hour example; no maximum lifetime stated |
| https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/put-bucket-policy/ | Bucket policy uses the AWS IAM shape; `s3:GetObject`, `Principal: "*"`, prefix-scoped resource ARN |
| https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/get-bucket-cors/ | `GetBucketCors` and the rule fields; no put or delete operation documented |
| https://docs.arvancloud.ir/en/object-storage/buckets/versioning | Versioning is per bucket, free, off by default; pre-existing objects get a null version ID; disabling keeps prior versions and lifecycle rules keep applying |
| https://docs.arvancloud.ir/en/object-storage/buckets | Private default and public toggle; the toggle does not cascade to existing objects; bucket tags; static website hosting; CDN caching settings |
| https://docs.arvancloud.ir/en/object-storage/buckets/custom-domain | Object storage uses the Arvan CDN by default; ANAME for root domain, CNAME for subdomain; host header rewritten to the bucket host; virtual-hosted object URL example |
| https://docs.arvancloud.ir/en/object-storage/dashboard | Access key, secret key and endpoint are surfaced in the dashboard; bucket public and private states are reported there |
| https://docs.arvancloud.ir/en/object-storage/ | Getting-started flow only; contained no region list or compatibility statement |
| https://www.arvancloud.ir/en/products/cloud-storage | Basic plan free allowance of 5 GB storage and 20 GB traffic; marketing claims including server-side encryption, versioning, lifecycle and multi-region |
| https://rclone.org/s3/ | Third-party corroboration of both endpoint hostnames and the Simin and Shahriar region names |

## Pages read on 2026-07-28

| URL | What it established |
|---|---|
| https://docs.arvancloud.ir/fa/developer-tools/sdk/object-storage/put-bucket-lifecycle-config/ | Lifecycle is applied through the S3 API with the AWS SDK; the worked example carries `Expiration` with `Days`, a `Filter` with a prefix predicate, and `Status: "Enabled"`; no other rule type appears. The English page at the same path is robots-blocked and the Persian page is not |
| https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/multipart-upload/ | The worked part size is `400 * (long)Math.Pow(2, 20)` = 419,430,400 bytes, labelled 400 MB and therefore above the published 400 MB ceiling; abort is called from the failure path; the client sets only `ServiceURL` |
| https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/credentials/ | The client is constructed with `BasicAWSCredentials` and `new AmazonS3Config { ServiceURL = ... }` and nothing else — no signature version, no region, no path-style flag |
| https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/upload-presigned/ | Presigned generation sets no signature version and no path-style flag; the expiry example is 12 hours; no maximum lifetime is stated |
| https://docs.arvancloud.ir/en/object-storage/limits/ | Re-read: 5 GB single upload, 5 TB multipart object, 400 MB maximum part, 5 MB minimum part, 10,000 parts, 50 buckets, 3,700,000 objects, DNS-label bucket naming, Virtual Host format `[bucketname].s3.[region].arvanstorage.ir` |
| https://docs.arvancloud.ir/en/object-storage/buckets | Re-read for the panel's bucket settings: public-access toggle, tags, CDN caching and static website hosting appear; **no lifecycle configuration appears in the panel** |
| https://rclone.org/s3/ | Re-read: ArvanCloud is a named provider with both endpoint hostnames, and rclone documents no ArvanCloud-specific signature-version or path-style override, so rclone's Signature Version 4 default applies |

## Pages indexed but not retrieved

These pages exist in ArvanCloud's documentation under the names shown, and their content was not retrieved, so they
support a "Documented, unread" status in `references/20-s3-compatibility-matrix.md` and nothing stronger.

| URL | Indexed title |
|---|---|
| https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/upload-object/ | Upload Object to Bucket |
| https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/download-object/ | Download File from Bucket |
| https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/put-bucket-lifecycle-config/ | Configure Bucket Lifecycle Policies |
| https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/get-bucket-versioning/ | Get Object Versioning Status |

## Pages that could not be reached

Retrieval was refused by the robots policy on the target host. No alternative retrieval route was attempted, and none
should be: a fact obtained by bypassing a publisher's robots policy is not a citable source in this library.

| URL | Attempts | Fact it would have settled |
|---|---|---|
| https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/put-bucket-lifecycle-config/ | 2, not retried | Which lifecycle rule types Arvan supports. **Settled instead from the Persian page at the same path**, which is reachable |
| https://www.arvancloud.ir/help/fa/object-s3cmd/ | 1, not retried | The s3cmd configuration Arvan publishes, which would show `signature_v2` on or off and the host and bucket templates |
| https://www.arvancloud.ir/help/fa/object-s3browser/ | 1, not retried | The S3Browser account type and signature version Arvan publishes |
| https://www.arvancloud.ir/help/fa/s3cmd-encryption/ | 1 | A second s3cmd configuration block, sought as an alternative route to the `signature_v2` value |
| https://www.arvancloud.ir/help/fa/504-s3cmd/ | 1 | A third s3cmd configuration block, sought for the same value |
| https://docs.arvancloud.ir/fa/object-storage/limits | 1 | The Persian limits page, sought to check the megabyte-versus-mebibyte wording; the English page at the same path is reachable and was read |

**The whole `www.arvancloud.ir/help/` host refuses retrieval, not merely the three pages first attempted.** Every
fetch of that host returned a robots policy refusal caused by a `robots.txt` fetch timeout, which covers the s3cmd,
S3Browser, CloudBerry, BucketAnywhere and s3fs guides alike. **Seek an Arvan client-configuration fact on
`docs.arvancloud.ir` or in a third-party provider list instead, and try the Persian path when the English one is
refused**, because the two hosts and the two languages are refused independently.

## Open questions

Each is a fact this skill could not establish from a primary source. **Answer these before treating the related
behaviour as known, and record the answer with its date in this file.** An unanswered question is not a licence to
assume the AWS or MinIO behaviour.

1. **Is Signature Version 4 required, and is Version 2 accepted?** *Narrowed on 2026-07-28, still open.*
   ArvanCloud publishes no prose statement either way. What its own material shows is that every reachable SDK
   example constructs the client with credentials and `ServiceURL` alone and sets no signature option, which signs
   Signature Version 4 by SDK default `[source:
   https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/credentials/, read: 2026-07-28]` `[source:
   https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/multipart-upload/, read: 2026-07-28]`
   `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/upload-presigned/, read:
   2026-07-28]`, and that rclone ships ArvanCloud as a named provider with no signature override, so its Signature
   Version 4 default applies too `[source: https://rclone.org/s3/, read: 2026-07-28]`. **The exact setting name and
   value could not be read from any Arvan page**, because the s3cmd and S3Browser guides that print
   `signature_v2` verbatim are on `www.arvancloud.ir/help/`, a host that refuses retrieval entirely. The question
   remaining is whether v2 is *also* accepted, which matters only for a legacy client. `STORAGE_SIGNATURE_VERSION`
   carries `s3v4` as this skill's default in the meantime.
2. **Is path-style addressing accepted at all, or only virtual-hosted?** *Still open as of 2026-07-28.* Arvan
   states the Virtual Host format is required for CDN caching and shows only virtual-hosted URLs `[source:
   https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-28]`, and its own SDK examples set no
   path-style flag, so they take the SDK's virtual-hosted default. **Whether a path-style request succeeds without
   the CDN is stated nowhere**, so the question is what Arvan accepts rather than what it recommends: it
   recommends and uses virtual-hosted, and acceptance of path-style is unestablished.
   `STORAGE_USE_PATH_STYLE` carries `false` on Arvan in the meantime.
3. **Which lifecycle rule types does Arvan support?** *Answered in part on 2026-07-28.* `Expiration` is
   supported and is applied through the S3 API rather than through the panel: Arvan's worked example builds a
   `LifecycleConfiguration` whose rule carries a prefix `Filter`, `Expiration` with `Days`, and `Status:
   "Enabled"` `[source: https://docs.arvancloud.ir/fa/developer-tools/sdk/object-storage/put-bucket-lifecycle-config/,
   read: 2026-07-28]`. **No lifecycle configuration appears anywhere in the panel's documented bucket settings**
   `[source: https://docs.arvancloud.ir/en/object-storage/buckets, read: 2026-07-28]`, so the S3 API is the only
   documented route. `AbortIncompleteMultipartUpload`, `NoncurrentVersionExpiration` and `Transition` are absent
   from that page, which is absence of documentation and not documented absence. **Ask Arvan whether the three
   absent actions are accepted**, because the abort rule is the one `/alaa-minio-object-storage`
   (`$alaa-minio-object-storage`) makes mandatory and the noncurrent-version rule is the only thing that would
   bound a versioned bucket's growth.
4. **How is an access key rotated, can two keys be valid at once, and how many keys may an account hold?** No rotation,
   key-count or key-lifecycle documentation was found. This determines whether a zero-downtime rotation is possible.
5. **What is the true maximum object size?** *Ruled on 2026-07-28, and still worth asking.* Arvan publishes a
   5 TB multipart maximum, a 400 MB part maximum and a 10,000 part maximum, and those three are inconsistent
   because 400 MB × 10,000 is 4 TB. A fourth figure was found this session and deepens the conflict: Arvan's own
   multipart example sets `400 * (long)Math.Pow(2, 20)` = 419,430,400 bytes and labels it 400 MB `[source:
   https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/multipart-upload/, read: 2026-07-28]`, so the
   vendor's prose and the vendor's code disagree about what one megabyte is. **Where published numbers conflict
   this skill's default is the minimum**, so the part ceiling is 400,000,000 bytes and the effective object ceiling
   is 400,000,000 × 10,000 = 4,000,000,000,000 bytes, which is 4 TB, being the smaller of that and the advertised
   5 TB. `references/15-environment-contract-deltas.md` carries the arithmetic and
   `STORAGE_MAX_OBJECT_BYTES` carries the value. **Ask Arvan which limit governs and whether MB means 10^6 or
   2^20**, because a confirmed answer either raises the ceiling or removes a conflict from the published page.
6. **What are the request-rate, connection and bandwidth limits per bucket or per account?** No published figure was
   found, so burst behaviour is unpredictable and a `503` under load cannot be classified.
7. **What are the per-gigabyte storage price, the per-gigabyte egress price and any per-request charge, beyond the
   Basic plan's free allowance?** No primary pricing table was retrieved, so no Arvan price appears in this skill.
8. **Is server-side encryption actually available, and by which mechanism?** The product page claims it and the SDK
   documentation shows no operation, header or key management for it. This is a contradiction between two ArvanCloud
   sources, not a gap.
9. **Are there regions beyond Simin and Shahriar?** The product page refers to storing data in other data centres while
   only two endpoints are documented.
10. **Is there an official ArvanCloud CLI or Terraform provider covering object storage?** Searching found only
    third-party libraries and general S3 tooling, so infrastructure-as-code for Arvan buckets has no established path.
