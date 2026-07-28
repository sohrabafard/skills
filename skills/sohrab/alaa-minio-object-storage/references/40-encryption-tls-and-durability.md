# Encryption, TLS, versioning and replication

This file owns the four bucket-level protections and what each one actually protects against. Read it before
turning any of them on, and before accepting a plaintext hop to the store.

## Transport

**Use TLS on every path whose endpoint host is not a loopback address.** A SigV4 `Authorization` header
authenticates the request and encrypts nothing, so on a plaintext hop the object bytes and the entire signed
request are readable by anything on that network segment. A container network on a shared host is not an exception:
every other workload attached to it sees the traffic.

**Set the endpoint scheme and the TLS flag from one source.** A configuration that carries both an
`http://…` endpoint and a `tls_enabled` flag can express two contradictory answers, and the one that wins is
whichever the client library consults. Derive the flag from the scheme, or reject the combination at startup.

**Read the flag from `STORAGE_TLS_ENABLED` and the endpoint from `STORAGE_ENDPOINT`, and reject a startup where
`STORAGE_TLS_ENABLED` is `false` and the `STORAGE_ENDPOINT` host is not a loopback address.** Both values differ
between a test stack and production, which is why they are environment values with stated defaults in
`05-environment-contract.md`, and rejecting the combination at startup is what stops a development default from
travelling into production unnoticed.

**Set `STORAGE_USE_PATH_STYLE` to `true` against a self-hosted store, and to `false` against a provider that
needs virtual-hosted addressing.** Virtual-host style puts the bucket in the hostname,
which needs wildcard DNS and a wildcard certificate that a single-node MinIO deployment usually does not have
`[source: https://min.io/docs/minio/linux/integrations/aws-cli-with-minio.html, read: unverified as of
2026-07-27]`. `70-client-libraries.md` owns the addressing style in full — what each style is, what breaks under
each, and how each client selects it — and `05-environment-contract.md` carries its default per provider profile.

**Verify the certificate.** A client configured to skip verification accepts any endpoint that answers, which turns
a DNS or routing mistake into a silent credential disclosure rather than a connection error.

## Encryption at rest

Server-side encryption comes in three shapes: keys the store manages (SSE-S3), keys a key-management service
manages with an audit trail and revocability (SSE-KMS), and keys the client supplies per request (SSE-C)
`[source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/serv-side-encryption.html, read: unverified as of
2026-07-27]`. On MinIO the equivalent needs an external key service; without one, what is called encryption at rest
is whatever the underlying volume provides `[source:
https://min.io/docs/minio/linux/administration/server-side-encryption.html, read: unverified as of 2026-07-27]`.

**Enable server-side encryption on every bucket holding user-supplied bytes**, because it removes the class of
incident where a decommissioned disk or a snapshot copy discloses object contents.

**Do not treat encryption at rest as access control.** A request carrying a valid credential gets plaintext back;
the store decrypts transparently. Encryption at rest does nothing about the stolen-credential case, which is what
`30-identity-credentials-and-access.md` is for. Stating this explicitly matters because "the bucket is encrypted"
is the sentence most often used to close a security question it does not answer.

**Decide the key custody question before enabling KMS-managed keys.** Where the key lives determines who can make
every object unreadable, and a key deleted by mistake is data loss that no backup of the bucket recovers.

## Bucket versioning

This is one of two unrelated things people call "the version API". This one decides whether the store keeps
superseded objects. The other is the S3 signature version, which decides how a request is signed, and it is
`70-client-libraries.md`. Confusing them produces different damage: a wrong signature version gives a client that
cannot authenticate, and a wrongly versioned bucket gives a bill that never stops growing.

Versioning keeps every overwritten and deleted object as a noncurrent version, so an accidental overwrite or delete
is recoverable and a delete becomes a delete marker rather than a removal
`[source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html, read: unverified as of
2026-07-27]`. It is set per bucket with `PutBucketVersioning` and read back with `GetBucketVersioning`, and the
`mc` equivalents are in `75-mc-command-line-client.md`
`[source: https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketVersioning.html and
https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketVersioning.html, read: unverified as of 2026-07-27]`.

### It has three states and only one transition is reversible

A bucket is unversioned until it is enabled; from enabled it can be suspended; **it can never return to
unversioned** `[source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html, read: unverified as
of 2026-07-27]`.

**Treat enabling versioning as irreversible and require the same review a schema migration gets.** Suspension is
the only way back, and a suspended bucket keeps every version it already holds and keeps paying for them, so
"suspend it if it turns out to be a problem" does not undo the cost that made it a problem.

### What changes the moment it is enabled

1. **A delete stops removing anything.** `DeleteObject` writes a delete marker and the previous version stays,
   billable and readable by a versioned request, so storage keeps growing while the object count in a plain
   listing falls. `90-failure-classes.md` class 11 is this symptom seen from the outside.
2. **A noncurrent-version expiration rule stops being optional.** Without it nothing ever removes a superseded
   version and the bucket's cost grows without bound; pair the two in the same commit, with
   `20-lifecycle-and-retention.md` owning the rule and `scripts/check_object_storage_posture.py` firing
   `VERSIONING_WITHOUT_NONCURRENT_RULE` when a repository declares one and not the other.
3. **Listing and reading change shape.** A key now names a set of versions rather than one object, so listing
   current objects and listing versions are different calls returning different things, and code that counts
   objects, computes size, or reconciles the bucket against the database must state which of the two it means.
4. **A delete now needs a version identifier to be a real delete.** Removing the bytes means deleting a specific
   version, so a reaper written against an unversioned bucket silently stops reclaiming anything the day
   versioning is enabled while continuing to report success.

### Which buckets on this fleet should have it

**Enable versioning on a bucket whose objects the application overwrites or deletes in normal operation and whose
loss would not be recoverable from another system**, because that is the only case where the recovered version is
worth what every retained version costs.

**Do not enable versioning on an upload staging bucket.** Staging objects are written once, superseded by retries,
and abandoned in bulk by interrupted uploads, so versioning turns every abandoned attempt into a permanent
noncurrent version on top of the multipart parts that already accumulate there — a cost problem wearing the
costume of a safety feature. The staging bucket's protection is the abort-incomplete-multipart rule in
`20-lifecycle-and-retention.md`, not versioning.

**Do not enable versioning on a bucket whose objects are written once and removed only by lifecycle**, because
there is no overwrite to recover from and the retained delete markers are pure cost.

**Enable versioning on both buckets of a replication pair**, for the reason the Replication section below gives.
Record in the provisioning script that replication is why versioning is on, so the noncurrent-version rule is not
later removed by someone who cannot see what versioning is there for.

## Replication

Replication copies objects to a second bucket asynchronously and requires versioning on both sides
`[source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html, read: unverified as of
2026-07-27]`.

**Replication is not a backup.** It propagates deletes and overwrites, so it protects against losing the storage
system and not against the application or an operator destroying data. Where the requirement is recovery from a bad
write, the answer is versioning plus a retention window, not replication.

**Replication needs its own identity and its own signal.** The replication role's permissions are separate from the
application's, and replication lag is invisible until someone measures it — see `95-observability.md`.

**Decide what a failed replication means before enabling it.** Asynchronous replication that nobody alerts on is a
disaster-recovery plan that has never been tested; state the recovery point objective the lag must stay inside, and
route the objective itself to `/alaa-reliability-sla` (`$alaa-reliability-sla`).

## Durability and consistency semantics

**A new object is readable immediately after a successful write, and an overwrite or delete becomes visible with
strong read-after-write consistency on S3 today**, while listing operations may still lag behind
`[source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html, read: unverified as of 2026-07-27]`.
Do not design a control flow that depends on a listing reflecting a write that just returned.

**Durability comes from redundancy the deployment actually has.** A single-node, single-drive MinIO has no erasure
coding and no replica, so its durability is the durability of one disk. That is a development posture; treat it as
one, and see `80-topology.md`.

## What the fleet does today

The fleet's only object-storage consumer runs its test stack with `STORAGE_TLS_ENABLED=false` against endpoint
`http://tusd-minio:9000`, so credentials and payloads cross that container network in the clear. **Read those two
values as the test stack's, not production's**, because production supplies its own `STORAGE_ENDPOINT` and
`STORAGE_TLS_ENABLED` from the environment — `80-topology.md` states the boundary. **`tusd-minio` is not a
loopback address, so the transport rule above is broken in the test stack too**, and the fix is the same value
change in both places. No server-side
encryption, no versioning and no replication is configured anywhere in its code, Compose files, Swarm stack or
provisioning container, and its store runs as a single replica on a single volume
`[source: tusd-upload-platform repository, .env.example, docker-compose.yml and docker-compose.swarm.yml, read:
2026-07-27]`.
