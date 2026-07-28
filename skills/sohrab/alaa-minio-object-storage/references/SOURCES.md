# Source map and freshness

Read this before repeating any version-sensitive or upstream claim from this skill.

## The provenance convention used throughout

Every upstream API fact in this skill carries an inline marker of the form
`[source: <url>, read: unverified as of 2026-07-27]`. **Unverified means exactly that: the URL was written from
memory and was not fetched.** No network access to AWS or MinIO documentation was available in the session that
created this skill, so no upstream claim here has been checked against its primary source, and no read date is
recorded for one. Fetch the source before acting on any of them where the cost of being wrong is data loss, an
outage, or a security decision.

Facts read from the fleet's only object-storage consumer carry
`[source: tusd-upload-platform repository, <file>, read: 2026-07-27]`. Those **were** read from source in that
session. They describe **one consumer's current state**, several items of which are defects; they are never
platform policy and never a precedent.

## Source order

1. **The service's own repository**: its storage adapter and client, its Compose and Swarm files, its provisioning
   container, its `.env.example`, its readiness checks, and its forbidden-log-field list. Repository truth outranks
   every statement in this skill.
2. **The running bucket's actual configuration**, read back with the store's own client. A provisioning script
   records what someone intended to apply; only the store records what is applied. The difference between the two
   is the most common finding on this subject.
3. **Official AWS S3 documentation**, for every API-level claim:
   - User guide: https://docs.aws.amazon.com/AmazonS3/latest/userguide/
   - API reference: https://docs.aws.amazon.com/AmazonS3/latest/API/
   - Bucket naming rules:
     https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html
   - Bucket and object limits: https://docs.aws.amazon.com/AmazonS3/latest/userguide/BucketRestrictions.html
     and https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html
   - Multipart upload overview: https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html
   - Aborting incomplete multipart uploads with lifecycle:
     https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-abort-incomplete-mpu-lifecycle-config.html
   - Lifecycle management: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html
   - `PutBucketLifecycleConfiguration`:
     https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketLifecycleConfiguration.html
   - Versioning: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html
   - `PutBucketVersioning`: https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketVersioning.html
   - `GetBucketVersioning`: https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketVersioning.html
   - Lifecycle configuration examples, including noncurrent-version expiration:
     https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-configuration-examples.html
   - Error responses and error codes: https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html
   - Replication: https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html
   - Server-side encryption: https://docs.aws.amazon.com/AmazonS3/latest/userguide/serv-side-encryption.html
   - Object lock: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html
   - Policy actions: https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-actions.html
   - Presigned URLs: https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html
   - Signed POST policy conditions:
     https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-HTTPPOSTConstructPolicy.html
   - Performance and prefix scaling:
     https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html
   - `AssumeRole` and session tokens: https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html
   - SDK data-integrity and checksum defaults:
     https://docs.aws.amazon.com/sdkref/latest/guide/feature-dataintegrity.html
4. **Official MinIO documentation**, for every claim about a self-hosted store, because MinIO's defaults differ
   from S3's on encryption, on public access and on erasure coding:
   - https://min.io/docs/minio/linux/
   - `mc` client reference, including global flags, the configuration directory and the alias environment form:
     https://min.io/docs/minio/linux/reference/minio-mc.html
   - `mc alias`: https://min.io/docs/minio/linux/reference/minio-mc/mc-alias.html
   - `mc ilm`: https://min.io/docs/minio/linux/reference/minio-mc/mc-ilm.html
   - `mc anonymous`: https://min.io/docs/minio/linux/reference/minio-mc/mc-anonymous.html
   - `mc admin`: https://min.io/docs/minio/linux/reference/minio-mc-admin.html
   - Server-side encryption:
     https://min.io/docs/minio/linux/administration/server-side-encryption.html
   - Erasure coding: https://min.io/docs/minio/linux/operations/concepts/erasure-coding.html
   - Metrics:
     https://min.io/docs/minio/linux/operations/monitoring/collect-minio-metrics-using-prometheus.html
   - Logging and audit: https://min.io/docs/minio/linux/operations/monitoring/minio-logging.html
5. **The client SDK's own reference**, for signing, retry, checksum and endpoint behaviour. SDK defaults change
   between minor versions and a behaviour proven on one version is not proven on the next.
6. **Community posts and issue threads**: use to find search terms for an unfamiliar error string only. Re-check
   every operational claim against an official source and against the running store.

## What was read from the consumer repository on 2026-07-27

| Claim | File |
|---|---|
| pinned MinIO and `mc` image tags, `server /data` command, `minio_data` volume, port publication, network attachment including `alaa-shared-network`, single Swarm replica | `docker-compose.yml`, `docker-compose.swarm.yml` |
| root credentials and application credentials drawn from the same variables | `docker-compose.yml`, `docker-compose.swarm.yml` |
| provisioner runs `mc alias set`, `mc mb -p`, `mc stat` and nothing else | `docker-compose.yml` |
| the exact spelling `mc alias set <alias> <endpoint> <access> <secret> --api S3v4`, and that the access key and secret key are passed positionally in all five invocations | `docker-compose.yml`, `docker-compose.swarm.yml`, `scripts/docker/smoke-compose-upload.sh`, `scripts/docker/smoke-compose-zip-extraction.sh`, `scripts/docker/smoke-compose-tar-tgz-extraction.sh` |
| the `mc mb -p ... \|\| true` hidden-failure defect, its fix, and the static guard that now rejects it | `docs/agents/tusd-api-contract-state.md`, `scripts/docker/validate-compose-runtime.sh` |
| absence of any `mc ilm`, `mc anonymous`, `mc policy`, `mc version`, `mc encrypt`, `mc replicate`, `--json` or scoped-config-directory use | verified by searching the whole repository excluding `vendor/` and the module cache |
| plaintext endpoint and `STORAGE_TLS_ENABLED=false` | `.env.example` |
| object-key shapes, absence of a tenant segment, credentials captured at construction, redacted config plan | `internal/storage/s3_compatible.go` |
| hand-rolled SigV4 client on `http.DefaultClient` with no timeout, no retries and no `x-amz-security-token` | `internal/storage/s3_http_client.go` |
| second S3 client from the AWS SDK feeding the upload library, and no part-size or concurrency override | `internal/httpapi/official_tusd_creation.go`, `go.mod` |
| reserved-prefix guard and its readiness surfacing, bucket-existence readiness check | `cmd/tusd-api/main.go` |
| forbidden-log-field list including `object_key` and `presigned_url`, and the `upload.asset.expired` event naming a retention worker | `internal/observability/contracts.go` |
| absence of any lifecycle, versioning, encryption, replication, presigned-URL or CDN configuration | verified by searching the whole repository excluding `vendor/` and the module cache |

## Command and flag spellings needing verification

`75-mc-command-line-client.md` and `70-client-libraries.md` name capabilities whose exact spelling was written from
memory. They are listed here so one pass against the primary sources can confirm or correct all of them. **Confirm
a spelling before putting it in a script or a runbook**, because a wrong flag fails at the deployment that first
meets it rather than at review.

**Repo-verified, needing no check:** `mc alias set` with its four positional arguments, `--api S3v4`, `mc mb -p`,
`mc stat` `[source: tusd-upload-platform repository, read: 2026-07-27]`.

| Spelling or claim | File |
|---|---|
| the alias environment-variable form, believed `MC_HOST_<alias>` holding `https://<access>:<secret>@<endpoint>` | `75-…` |
| the default configuration directory, believed `~/.mc/` with `config.json`, and the `--config-dir` override | `75-…` |
| the legacy signature-version value `S3v2` | `75-…` |
| `mc ls`, `mc du`, `mc rb` | `75-…` |
| `mc anonymous` with `set`, `get` and `list`, and whether `mc policy` survives as an older alias | `75-…` |
| the `mc ilm` verbs, its import and export form, and every `mc ilm` flag name | `75-…` |
| `mc version enable`, `mc version suspend`, `mc version info` | `75-…` |
| `mc replicate add`, `mc replicate ls`, `mc replicate status` | `75-…` |
| `mc encrypt set`, `mc encrypt info` | `75-…` |
| `mc cp`, `mc mv`, `mc rm` and its recursive flag, `mc find`, `mc head`, `mc cat` | `75-…` |
| `mc mirror`, its removal flag and its dry-run flag | `75-…` |
| the `mc admin` subcommands named — `info`, `user`, `policy`, `service restart`, `trace`, `heal` | `75-…` |
| the argument order of `mc admin user add`, on which `scripts/check_object_storage_posture.py` bases its three-positional threshold | `75-…` |
| the `--json` global flag and the quiet and colour-suppression flags beside it | `75-…` |
| that `aws-sdk-go-v2` offers no SigV2 signer | `70-…` |
| the `minio-go/v7` v4-versus-v2 static-credentials constructor names | `70-…` |
| the `signature_version` option in `aws/aws-sdk-php` and its `v4` and `v2` values | `70-…` |
| that `@aws-sdk/client-s3` ignores the previous major version's `signatureVersion` option | `70-…` |
| `botocore.config.Config(signature_version=...)` and its `s3v4` and `s3` values | `70-…` |
| which error code each store returns for a signature-version mismatch | `90-…` |

## Recorded as unverified

- **Every upstream API fact in this skill.** See the convention above. The URLs listed here are believed correct
  and were not fetched.
- **The multipart default values** quoted in `50-multipart-capacity-and-cost.md` — 5 MiB minimum part, 50 MiB
  preferred part, 5 GiB maximum part, 10,000 parts, 5 TiB maximum object, ten concurrent part uploads, twenty
  buffered parts. What **was** verified is that the consumer repository sets no override, so whatever the upstream
  library's defaults are, they are what runs. Read them from the installed module before quoting the numbers.
- **Every client library name** in `70-client-libraries.md`. Package registries were not reachable; confirm the
  version installed in the service before writing an API call against it.
- **Every `mc` command and flag spelling** except the four marked repo-verified in the table above, and **every
  signature-version setting** in `70-client-libraries.md` except the `mc` flag. No MinIO, AWS or SDK documentation
  was reachable in the session that wrote them.
- **The versioning claims in `40-encryption-tls-and-durability.md`** — the three bucket states, the
  irreversibility of enabling, the delete-marker behaviour and the replication dependency. These are stated as
  hard consequences because that is how they behave on S3 as understood when this file was written; confirm them
  against `API_PutBucketVersioning.html` before enabling versioning on a bucket that will hold anything.
- **Every cell of the `aws` column in the provider profile table** in `05-environment-contract.md` — the endpoint
  shape, the addressing style, the TLS default, the signature version, the part floor and ceiling, the part count
  and the object ceiling. No AWS documentation was reachable in the session that wrote the column, so every cell
  carries `[unv]` and none was fetched. The `minio` column's three ceilings are marked `[open]` for the same reason
  and carry no number at all.
- **Every row of the addressing-style table** in `70-client-libraries.md` except the two styles themselves. The
  option names were written from memory; confirm each against the installed version before it reaches a
  configuration file.
- **Whether the running bucket differs from what the repository declares.** Nothing in this skill was checked
  against a live store.

## Freshness triggers

Verify against a primary source before acting when the task mentions:

- a new S3 or MinIO release, a managed-service migration, a CVE, or the words `latest`, `current` or `upgrade`;
- lifecycle, versioning, replication, object lock, encryption, or block-public-access, because defaults and
  available modes differ between S3 and MinIO and change between MinIO releases;
- SDK retry, checksum or signing behaviour, which changed default in recent AWS SDK releases and breaks against
  stores that implement an older set;
- any limit quoted as a number — bucket count, key length, part count, part size, object size;
- any `mc` command or flag, because the client renames subcommands between releases — `mc policy` to
  `mc anonymous` is the known case — and the image tag pinned in a repository decides which spelling works;
- the S3 signature version, because a library default that changes on an upgrade presents as an authentication
  failure rather than as a configuration change;
- the addressing style, for the same reason and with a second failure shape: a style left to a library default
  presents as a not-found or a TLS hostname mismatch rather than as a configuration change;
- a claim about what the fleet does, because the consumer repository is under active rewrite and every observation
  in this skill is dated 2026-07-27.
