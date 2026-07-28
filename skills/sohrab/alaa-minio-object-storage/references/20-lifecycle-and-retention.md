# Lifecycle, retention and abandoned multipart uploads

This file owns what a bucket removes on its own and when. Read it before creating a bucket, before adding a
retention promise to a contract, and whenever storage cost grows faster than the object count.

## The rule that must exist on every bucket

**Every bucket that receives multipart uploads carries a lifecycle rule that aborts incomplete multipart uploads
after a stated number of days.** An interrupted multipart upload leaves its uploaded parts allocated in the bucket.
Those parts are billed, they are invisible to `ListObjects`, and no application code ever removes them because the
application no longer knows the upload existed. The lifecycle engine is the only mechanism that removes them
without an explicit `AbortMultipartUpload` call `[source:
https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-abort-incomplete-mpu-lifecycle-config.html, read:
unverified as of 2026-07-27]`.

The rule is expressed as an `AbortIncompleteMultipartUpload` action with a `DaysAfterInitiation` value inside a
lifecycle configuration applied with `PutBucketLifecycleConfiguration`, or through the MinIO client as an `mc ilm`
rule `[source: https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketLifecycleConfiguration.html and
https://min.io/docs/minio/linux/reference/minio-mc/mc-ilm.html, read: unverified as of 2026-07-27]`.

**Read the abort window from `STORAGE_MULTIPART_ABORT_DAYS`, whose stated default is seven days.** Seven days is
longer than any legitimate resumable upload window on this fleet and short enough that abandoned parts cost less
than a day of engineering time to notice. It is this skill's default rather than a provider guarantee, and the
window differs between a test stack and production, so it is an environment value — see
`05-environment-contract.md`. The fleet-wide value, once agreed, belongs to `/alaa-services-contract` (`$alaa-services-contract`), which
owns platform values; request registration rather than inventing a second number in a second service.

**The abort window must be longer than the longest resumable-upload window the service offers**, because the rule
cannot distinguish an abandoned upload from a paused one. Where the upload protocol above the store defines that
window, take it from `/tusd-upload-platform` (`$tusd-upload-platform`) rather than guessing.

## Writing a lifecycle configuration

1. **Give every rule an explicit ID and an explicit prefix filter.** A rule with no filter governs every object in
   the bucket, including prefixes added by a different team a year later. The ID is what an operator matches
   against the runbook when a deletion surprises someone.
2. **Apply lifecycle from the same mechanism that creates the bucket.** A bucket created by automation and
   configured by hand loses its configuration the first time the automation runs in a new environment, and nothing
   fails to signal it.
3. **Never treat a lifecycle window as a deletion guarantee.** The lifecycle engine runs asynchronously and objects
   can persist past their expiry before the scan reaches them `[source:
   https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html, read: unverified as of
   2026-07-27]`. When a contract or a regulation names a deletion deadline, delete explicitly and use lifecycle as
   the backstop that catches what the explicit path missed.
4. **Record the owner and the reason in the rule's own comment or in the provisioning script beside it**, because
   an unexplained expiry rule is the first thing someone disables during an incident.

## Retention: which layer decides

The database row is truth for whether an object should exist; the lifecycle rule is the cost backstop. Two
obligations follow.

**A reaper that deletes objects records its intent durably before it deletes.** Delete-then-update loses the object
and keeps the row when the process dies between the two; update-then-delete keeps the object and loses the pointer.
Write the intent, delete, then confirm — and see `SKILL.md` "When the store fails" for the unconfirmed-delete case.

**An event that names a retention worker obliges that worker to exist.** The fleet's only object-storage consumer
emits an `upload.asset.expired` event whose declared producer is a retention worker, and no retention worker and no
sweep of expired rows or their objects exists in the repository `[source: tusd-upload-platform repository,
internal/observability/contracts.go, read: 2026-07-27]`. A declared-but-absent producer reads to every other
service as a promise that data is being removed.

## Versioning interacts with every deletion rule

When versioning is on, a delete creates a delete marker and the previous version remains billable, so an expiration
rule that only expires current versions removes nothing from the bill.

**A versioned bucket carries a noncurrent-version expiration rule and an expired-delete-marker cleanup, and the
two are added in the same change that enables versioning.** They are not an optimisation to add later: without
them nothing ever removes a superseded version, the growth is invisible to an object listing, and by the time the
bill shows it the versions being paid for are months old. The actions are `NoncurrentVersionExpiration` with a
`NoncurrentDays` value and an expired-object-delete-marker cleanup inside the same lifecycle configuration
`[source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-configuration-examples.html, read:
unverified as of 2026-07-27]`. `scripts/check_object_storage_posture.py` fires
`VERSIONING_WITHOUT_NONCURRENT_RULE` when a repository declares versioning and declares no noncurrent-version
rule.

**State the noncurrent retention window against a stated recovery need, not a round number.** The window is how
long an accidental overwrite stays recoverable, so it is answerable — how long before someone notices — and a
value chosen without that question is either too short to recover from or paid for indefinitely.

`40-encryption-tls-and-durability.md` owns the decision to enable versioning at all and the list of buckets that
should not have it; this file owns the rules that must accompany it once it is on.

## Object lock

Object lock enforces write-once-read-many retention at the object level, must be enabled at bucket creation, and in
compliance mode cannot be shortened or removed by anyone including the account root
`[source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html, read: unverified as of
2026-07-27]`. **Enable it only against a written legal or regulatory requirement with a named owner**, because a
mistaken retention period on a compliance-mode bucket cannot be undone and the storage is paid for until it
expires.

## What the fleet does today

No lifecycle configuration of any kind exists in the fleet's only object-storage consumer: no
`PutBucketLifecycleConfiguration` call, no `AbortIncompleteMultipartUpload` rule, and no `mc ilm` invocation
anywhere in its code, its Compose files, its Swarm stack or its provisioning container. Its one-shot provisioner
sets the bucket up with `mc alias set`, `mc mb -p` and `mc stat`, and stops there
`[source: tusd-upload-platform repository, docker-compose.yml and docker-compose.swarm.yml, read: 2026-07-27]`. An
interrupted upload on that fleet therefore leaves parts that nothing aborts and nothing bounds.
