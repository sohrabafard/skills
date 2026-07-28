# Identity, credentials and access policy

This file owns who may reach the bucket and how the secret that proves it gets to the process and gets replaced.
Read it before creating a storage credential, before writing a bucket or IAM policy, and before any rotation.

## One identity per service per environment

**Create a named identity for each service in each environment, and give it a policy that names exactly the bucket
and the key prefixes that service reads and writes.** A shared identity makes an audit log unable to answer which
service performed a deletion, and it makes revoking one service's access an outage for all of them.

**An application identity never holds root or administrative credentials.** Root can delete every bucket, rewrite
every policy, and read every tenant's objects, so a single compromised application process becomes total data loss
with no containment step available. This is `SKILL.md` rule 1 and it is the first thing to check on any existing
deployment.

**The application identity's policy grants no bucket-administration action** — not `s3:DeleteBucket`, not
`s3:PutBucketPolicy`, not `s3:PutLifecycleConfiguration`, not `s3:PutBucketVersioning`. Those belong to the
provisioning identity, which runs at deploy time and is not present in the running application's environment,
because an application that can rewrite its own lifecycle policy can also delete the evidence of doing so.

## Shape of the policy

Grant object actions on the key prefixes, and bucket actions on the bucket with a prefix condition:

- Object actions such as `s3:GetObject`, `s3:PutObject`, `s3:DeleteObject` and `s3:AbortMultipartUpload` take a
  resource of the form `arn:aws:s3:::<bucket>/<prefix>/*`.
- `s3:ListBucket` is a **bucket-level** action whose resource is `arn:aws:s3:::<bucket>`. Granting it without a
  prefix condition lets the holder enumerate every key in the bucket, including every other tenant's key names,
  which are themselves sensitive `[source:
  https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-actions.html, read: unverified as of
  2026-07-27]`.

**Grant only the actions the client actually calls.** A multipart-uploading client needs
`s3:AbortMultipartUpload` and `s3:ListMultipartUploadParts`; a client that never deletes needs no delete action at
all. Read the client's call sites rather than copying a policy template, because a template grants the union of
every use case its author imagined.

**Block public access at the bucket, and state it explicitly rather than relying on the store's default.** MinIO and
AWS differ in what an unconfigured bucket allows, so a deployment that is private because nobody set a policy is
private by accident.

## Getting the credential to the process

Preference order, and the reason each step down is worse:

1. **A workload identity the platform mints and rotates** — an instance role, a service-account token, or an STS
   session. Nothing long-lived exists to leak.
2. **A secret manager the process reads at startup and can re-read.** The secret exists in one place with an audit
   trail, and rotation is a write there rather than a deploy.
3. **An environment variable injected by the orchestrator from a secret store.** Acceptable, and the fleet's
   current shape. The weakness is that the value is fixed for the process lifetime, so rotation requires a restart.

**Never read a credential from a file committed to a repository, and never write one into an image.** A credential
in git history or an image layer outlives every commit and every deployment that removed it, so the only remedy is
rotation — see `SKILL.md` rule 4.

## Rotation

**Rotate through a two-credential window, never in place.** Create the new credential, deploy it, verify the
service is using it, then disable the old one, then delete it. A single-credential rotation makes the gap between
"old key revoked" and "new key deployed" an outage, which is why in-place rotation gets postponed until it is
forced by an incident.

**The client must be able to pick up a new credential without a code change.** A client that reads the credential
once at construction and is never rebuilt can only be rotated by restarting the process, which is acceptable if it
is written down and practised, and is a defect if nobody has established that it works.

**Short-lived credentials require the client to send the session token.** An STS or `AssumeRole` credential is a
triple — access key, secret key, and a session token that travels as the `x-amz-security-token` header. A client
that signs with only the first two is rejected with an authentication error and cannot use temporary credentials at
all `[source: https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html, read: unverified as of
2026-07-27]`. Check for that header before promising a rotation story built on temporary credentials.

## What the fleet does today

- **In the test stack, the application runs as MinIO root.** `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` are set
  from the same variables the application consumes as `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`, and no scoped
  identity and no bucket policy appear anywhere in the repository `[source: tusd-upload-platform repository,
  docker-compose.yml and docker-compose.swarm.yml, read: 2026-07-27]`. **Record this as an observation of the test
  stack those two files stand up, and not as a production defect.** Both files configure the local development and
  test store described in `80-topology.md`, while production reads its endpoint, bucket and credentials from the
  environment, so nothing in the repository shows which identity the production store issues.
- **Whether the production store issues a scoped identity is an open question here, not a finding.** Ask whoever
  provisions that store two things: whether the value in the application's `STORAGE_ACCESS_KEY` names an identity
  distinct from the store's root, and whether a policy on that identity names the bucket and the prefixes the
  service uses. **Record the answer with the date it was given, and treat the question as unanswered until then**,
  because a question written down as though it were a defect spends attention twice — once chasing a fault that
  may not exist, and once discovering the real state was never established.
- **Credentials come from environment variables only** — no file path, no secret-manager integration, no
  `AssumeRole` — and both clients capture them at construction and are never rebuilt, so no rotation path exists
  beyond a full restart `[source: tusd-upload-platform repository, internal/storage/s3_compatible.go and
  internal/httpapi/official_tusd_creation.go, read: 2026-07-27]`.
- **The hand-rolled client sets no `x-amz-security-token` header**, so temporary credentials cannot be adopted
  there without changing the signer `[source: tusd-upload-platform repository, internal/storage/s3_http_client.go,
  read: 2026-07-27]`.
- **Credentials are handled correctly in output**: the runtime config plan redacts the endpoint, bucket, access key
  and secret key, and `object_key` and `presigned_url` sit on the service's forbidden-log-field list
  `[source: tusd-upload-platform repository, internal/storage/s3_compatible.go and
  internal/observability/contracts.go, read: 2026-07-27]`.

The migration off root, for whichever environment the answer above shows is running on it, is: create a scoped
identity, attach a policy covering the bucket and its prefixes, set the application's `STORAGE_ACCESS_KEY` and
`STORAGE_SECRET_KEY` to that identity, restart, verify with the checker in `scripts/`, then change the root
password to a value no application holds. **Run that sequence against the test stack before running it against
production**, because the test stack is the one place where a policy that grants too little costs an afternoon
rather than an outage.

Threat classification, review triggers and the fail-closed doctrine behind all of this are `/alaa-security-review`
(`$alaa-security-review`).
