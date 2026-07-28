# Buckets and object keys

This file owns how many buckets exist, what they are called, and how a key inside one is assembled. Read it before
creating a bucket or writing the code that computes a key.

## How many buckets

**One bucket per service per environment.** Separate tenants by key prefix inside that bucket, never by giving each
tenant its own bucket. A bucket is an account-level resource with an account-level count limit, and every bucket
needs its own policy, its own lifecycle rules and its own monitoring, so per-tenant buckets make every one of those
tasks scale with the tenant count. The default S3 limit is 100 buckets per account, raisable on request
`[source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/BucketRestrictions.html, read: unverified as of 2026-07-27]`.

**Give a distinct bucket to data with a distinct policy.** Two datasets belong in two buckets when they need
different lifecycle windows, different encryption keys, different replication targets, or different public-access
posture — because all four are bucket-level settings and a single bucket cannot hold two answers.

## Naming a bucket

1. **Choose a name that is lowercase, 3 to 63 characters, and built from letters, digits and hyphens.** Bucket
   naming rules forbid uppercase and underscores, and a name that violates them fails at creation on S3 while
   sometimes succeeding on a self-hosted store, which produces a bucket that cannot be migrated
   `[source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html, read: unverified as of 2026-07-27]`.
2. **Never put a dot in a bucket name.** Virtual-host-style addressing puts the bucket name in the hostname, and a
   dotted name breaks the wildcard certificate, so TLS fails for that bucket and only that bucket.
   `70-client-libraries.md` states the certificate arithmetic under "The addressing style".
3. **Treat the name as permanent.** A bucket cannot be renamed, and the name appears in every policy document,
   every endpoint URL, every backup manifest and every runbook, so changing it later means a copy of all data.
4. **Register the name with `/alaa-services-contract` (`$alaa-services-contract`) before first use**, because a
   bucket name is a shared-infrastructure identifier and that skill owns canonical names.

## Composing an object key

A key is a single opaque string; the slashes in it are a display convention, not directories. Compose it from
segments the server controls, in this order:

1. **A fixed namespace segment** naming what wrote the object, so two subsystems writing into one bucket cannot
   collide. Example shape: `uploads`, `exports`, `thumbnails`.
2. **The tenant segment**, taken from the trusted request context. This is the constraint in `SKILL.md` rule 3: the
   object store applies no tenant predicate, so if the tenant segment can be influenced by the caller then a key
   built from it is a cross-tenant read that returns a well-formed success.
3. **The entity identity**, from the database row that owns the object.
4. **A per-object identifier** that is unique for the lifetime of the bucket, so a retry of a write cannot silently
   overwrite a different object.

**Never build a key segment from a client-supplied filename, path or metadata value.** Percent-encode nothing and
sanitise nothing as a substitute: strip the client value out of the key entirely and keep the original filename in
the database row, because a key is compared byte-for-byte and every sanitiser eventually meets an encoding it did
not anticipate.

**Reject `.` and `..` as key segments** even though the store treats them literally. Anything that later mirrors the
bucket to a filesystem — a backup, a local cache, an extraction step — resolves them as traversal.

**Keep the key under 1024 bytes of UTF-8**, which is the documented S3 key-length limit
`[source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html, read: unverified as of 2026-07-27]`.
A key assembled from several identifiers plus a filename reaches that limit sooner than it looks.

**Do not encode a fact in the key that the database also holds**, beyond what is needed to compute the key from the
row. A key carrying a status, a version number or a timestamp becomes wrong the moment the fact changes, and an
object cannot be renamed — only copied and deleted.

## The reserved-prefix guard

When a service reads an object prefix from configuration, validate it at startup against the set of namespace
segments the service itself computes, and refuse to start — or report not-ready — when the configured prefix
collides with one of them, is empty, or contains `.` or `..` or a character outside the allowed set. Reason: a
configured prefix that shadows a server-owned namespace puts externally-written objects where the service's own
cleanup planner computes keys, so a routine cleanup deletes live data with no error anywhere.

The fleet's only object-storage consumer implements exactly this guard and surfaces it through readiness: the
configured tus prefix is rejected when its first segment is one of `tmp`, `final` or `extracted`, or when any
segment is empty, `.` or `..`, or contains a character outside letters, digits, `-`, `_` and `.`
`[source: tusd-upload-platform repository, cmd/tusd-api/main.go, read: 2026-07-27]`. Generalise that guard; do not
copy its specific segment list.

## What the fleet does today

Keys in the fleet's only object-storage consumer are `<configured-prefix>/<uploadID>` for objects the tus library
writes, and `tmp|final|extracted/<assetID>/<componentID>/<uploadID>` for objects the service writes itself. **No key
carries a project or tenant segment**, so tenant isolation rests entirely on the database and the router, and a
key-construction defect becomes a cross-tenant read with no storage-layer backstop
`[source: tusd-upload-platform repository, internal/storage/s3_compatible.go, read: 2026-07-27]`. That is an
observation of one consumer, not a pattern to copy.

## Prefix distribution

S3 scales request rate per prefix, so keys that share a long common prefix and differ only in a trailing sequence
concentrate load on one partition
`[source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html, read: unverified as of 2026-07-27]`.
Where request rate against one prefix is expected to exceed a few thousand per second, put a high-entropy segment
early in the key. Below that rate, keep the key readable: a prefix scheme adopted for a load that never arrives
makes every debugging session harder and buys nothing.

Complexity budgets for a listing or a fan-out that grows with tenants or objects belong to
`/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`).
