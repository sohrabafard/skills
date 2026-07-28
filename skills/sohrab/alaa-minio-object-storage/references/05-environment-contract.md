# The `STORAGE_*` environment contract

This file owns the name, the default and the validation of every storage value a service reads from its
environment. Read it before writing a storage value into code, before adding a storage setting to a service, and
before changing a value that differs between MinIO and ArvanCloud or between a test stack and production. It also
owns the provider profile that supplies those defaults per provider, and the order in which a baseline default, a
profile default and an explicit environment value resolve.

## Every uncertain storage value is an environment variable

**A storage value that is a guess, a provider limit, or a thing that can differ between MinIO and ArvanCloud or
between a test stack and production is read from a named environment variable, never written into code.** A value
compiled into code costs a code change, a review, a build and a deploy on the day the provider turns out to want a
different number, and that cost is paid under incident pressure. The same value read from the environment costs one
env change. Several numbers in the table below are this skill's estimate rather than a provider guarantee, so the
cheap correction path is the one that has to exist.

**Extend the `STORAGE_*` family, and add no second family for a knob the family already names.** The fleet's only
object-storage consumer already reads `STORAGE_DRIVER`, `STORAGE_ENDPOINT`, `STORAGE_REGION`, `STORAGE_BUCKET`,
`STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`, `STORAGE_USE_PATH_STYLE` and `STORAGE_TLS_ENABLED`
`[source: tusd-upload-platform repository, .env.example and internal/storage/s3_compatible.go, read: 2026-07-28]`.
This file adds names to that family and renames nothing in it. A service moving from MinIO to ArvanCloud must
change env values only, and a parallel family with different names for the same knob would turn that move back into
a code change, which is the cost this contract exists to remove.

**`/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`) `references/15-environment-contract-deltas.md` states
only the variables whose default differs on ArvanCloud**, and it uses these names unchanged. Read that file for an
`arvanstorage.ir` endpoint and this one for everything else, because a delta file that repeated the shared names
would drift from them.

## Read the evidence marker before trusting a default

Each default below carries exactly one evidence marker, and the three are not interchangeable.

- **verified from the tusd repository** — the value is what the fleet's consumer reads today, cited to the file it
  came from.
- **published by ArvanCloud and read on 2026-07-28** — a provider fact whose URL is in
  `/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`) `references/SOURCES.md`.
- **this skill's conservative estimate pending confirmation** — a placeholder that nobody has confirmed. Change it
  when a service shows what it needs. Quote it to nobody as a provider limit, because it is not one.

**Where a provider's own published numbers conflict, this contract's default is the minimum of them.** A ceiling
set to the smaller of two published figures fails early, locally and cheaply; a ceiling set to the larger fails
after the bytes have already crossed the network, so the cost is bandwidth and elapsed time on top of the error.

## The variables

| Variable | Default | Evidence for the default | Validation at startup | A wrong value causes |
|---|---|---|---|---|
| `STORAGE_PROVIDER_PROFILE` | none, and the variable is required | this skill's stated default | one of `minio`, `arvancloud`, `aws`, `generic-s3`, and startup refuses on any other value | a profile chosen by omission hands one provider's defaults to another provider's endpoint, and the first symptom is a part rejected after it crossed the network |
| `STORAGE_DRIVER` | `s3` | verified from the tusd repository | one of `s3`, `s3-compatible`, `minio` | startup refuses and no storage call is attempted, which is the cheap failure |
| `STORAGE_ENDPOINT` | none, and the variable is required | verified from the tusd repository | non-empty, and parses as an absolute URL | a client left to a provider default reaches a namespace where the bucket does not exist, and the not-found reads as data loss |
| `STORAGE_REGION` | `us-east-1` | verified from the tusd repository | non-empty | on a provider whose regions are separate namespaces the bucket is not found, and that not-found is identical to a deleted object |
| `STORAGE_BUCKET` | none, and the variable is required | verified from the tusd repository | non-empty, and a valid DNS label whenever `STORAGE_USE_PATH_STYLE` is `false` | a name that is legal path-style cannot be addressed virtual-hosted at all, so the bucket becomes unreachable on the day addressing changes |
| `STORAGE_ACCESS_KEY` | none, and the variable is required | verified from the tusd repository | non-empty, and redacted in every log line, metric label, span attribute and report | an unset key fails every call with an authentication error that looks like a revoked credential |
| `STORAGE_SECRET_KEY` | none, and the variable is required | verified from the tusd repository | non-empty, and redacted in every log line, metric label, span attribute and report | a leaked value is remediable only by rotation, so redaction is validated rather than assumed |
| `STORAGE_USE_PATH_STYLE` | `true` | verified from the tusd repository | a boolean literal | `true` against a provider that needs virtual-hosted style loses edge caching with no error, so the cost arrives as a traffic bill rather than a failed request |
| `STORAGE_TLS_ENABLED` | `false` | verified from the tusd repository, where the endpoint is a loopback development store | a boolean literal, and `true` whenever the endpoint host is not a loopback address | a plaintext hop exposes the object bytes and the signed request to every workload sharing that network |
| `STORAGE_SIGNATURE_VERSION` | `s3v4` | this skill's conservative estimate pending confirmation; ArvanCloud's own SDK examples set no signature option and therefore sign with the SDK's Signature Version 4 default `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/credentials/, read: 2026-07-28]` | one of `s3v4`, `s3` | a mismatch returns `SignatureDoesNotMatch`, which reads as a wrong secret key and sends the investigation to credential rotation instead of client configuration |
| `STORAGE_PART_SIZE_BYTES` | `16777216`, which is 16 MiB | this skill's conservative estimate pending confirmation | at least `STORAGE_MIN_PART_SIZE_BYTES` and at most `STORAGE_MAX_PART_SIZE_BYTES` | a part below the floor is rejected at upload, and a part above the ceiling is rejected only after it crossed the network |
| `STORAGE_MIN_PART_SIZE_BYTES` | `5242880`, which is 5 MiB | published by ArvanCloud and read on 2026-07-28, and the same figure appears in the AWS S3 limits this skill records as unverified | at least 1 | a floor set too low lets a part size through that the store rejects |
| `STORAGE_MAX_PART_SIZE_BYTES` | `5368709120`, which is 5 GiB | AWS S3 documented value, unverified as of 2026-07-28 | at least `STORAGE_MIN_PART_SIZE_BYTES` | a ceiling copied from AWS onto a stricter provider passes validation and fails at the store |
| `STORAGE_MAX_PARTS` | `10000` | published by ArvanCloud and read on 2026-07-28, matching the AWS figure this skill records as unverified | at least 1 | an upload exceeding it fails at part 10,001, after every earlier part was transmitted and billed |
| `STORAGE_MAX_OBJECT_BYTES` | `5000000000000`, which is 5 TB | AWS S3 documented value, unverified as of 2026-07-28 | at least `STORAGE_PART_SIZE_BYTES` | an object accepted above the store's real ceiling fails at completion, after every part was uploaded |
| `STORAGE_UPLOAD_CONCURRENCY` | `4` | this skill's conservative estimate pending confirmation | at least 1 | a high value multiplies the bytes held in flight, and the failure is an out-of-memory kill or a full disk that takes down every request on the process, not only the upload that caused it |
| `STORAGE_MULTIPART_ABORT_DAYS` | `7` | this skill's stated default, carried unchanged from `SKILL.md` constraint 2 | at least 1, and longer than the longest resumable-upload window the service offers | a window shorter than the resumable-upload window aborts an upload a user is still resuming, because the lifecycle rule cannot tell an abandoned upload from a paused one |
| `STORAGE_PRESIGN_MAX_SECONDS` | `900`, which is 15 minutes | this skill's conservative estimate pending confirmation | at least 1 and at most `604800` | a long lifetime leaves an unrevocable bearer link alive past the need it was issued for, and withdrawing it early means rotating the signing credential, which invalidates every other outstanding URL at the same time |
| `STORAGE_OBJECT_KEY_PREFIX` | empty | this skill's stated default; the fleet's consumer spells its own prefix `TUSD_OFFICIAL_TUS_STORAGE_PREFIX` with the value `tusd`, which is a service-specific name rather than a second family `[source: tusd-upload-platform repository, .env.example and internal/storage/s3_compatible.go, read: 2026-07-28]` | no leading slash, no trailing slash, and no segment taken from client input | a prefix assembled from a client-supplied value is a cross-tenant read returning a well-formed success, which is `SKILL.md` constraint 3 |

`604800` seconds is seven days, recorded as the SigV4 presigned ceiling and unverified as of 2026-07-28. Confirm it
against the signing SDK in use before raising `STORAGE_PRESIGN_MAX_SECONDS` anywhere near it.

## The provider profile

**Select one provider profile per deployment with `STORAGE_PROVIDER_PROFILE`, take each variable's default from that
profile's column below, and override any of those defaults by setting that variable's own environment value.** Every
provider behaves differently and ArvanCloud is not the only S3 provider this fleet may use, so the alternative is
eleven provider-shaped values copied by hand into every environment file of every service, where one stale copy is a
part ceiling nobody notices until an upload fails after the bytes crossed the network.

The value is spelled `STORAGE_PROVIDER_PROFILE` rather than `STORAGE_PROVIDER` because the name states what the
value is for: a profile is a bundle of defaults and a provider is an identity, and an identity in a variable invites
the branch rule 1 forbids.

**Set `STORAGE_PROVIDER_PROFILE` in every environment in the same change that adds the resolver**, because the
variable is required and a service whose environment omits it does not start.

### Rule 1: a provider profile supplies defaults and nothing else, and never becomes a branch in code

**A provider profile supplies defaults for the variables in the profile table and nothing else, so no service in any
language and at any layer reads `STORAGE_PROVIDER_PROFILE` to decide what to do.** The moment behaviour hangs off
the profile name, adding a fourth provider means a code change in every service carrying such a branch, which is
exactly the cost this mechanism exists to remove. A service reads resolved `STORAGE_*` values and does not read the
profile name at all.

**When a provider genuinely needs behaviour that no knob expresses, add a new `STORAGE_*` variable to the table
above with a default in every profile column, and leave the branch unwritten.** A new variable costs one row in this
file and one env value in each environment that disagrees with its profile; a branch costs a code change in every
service, repeated for every provider adopted afterwards.

### Rule 2: resolution order is explicit and logged at boot

**Resolve every `STORAGE_*` value in the order baseline default, then profile default, then explicit environment
value, each step overriding the one before it, and record in the startup line which of the three supplied each
resolved value.** An operator debugging a wrong endpoint needs to know whether the profile or the environment set
it, and a silent default is indistinguishable from a misconfiguration, so a startup line that prints a value without
its source sends the investigation to the wrong file.

The baseline default is the Default column of the variables table above, and it governs every variable the profile
table does not carry. A profile column governs every variable that column carries. An explicit environment value
governs wherever it is set.

### Rule 3: an unknown profile name fails at boot

**Refuse to start on a `STORAGE_PROVIDER_PROFILE` value that names no column in the profile table, and fall back to
no profile, not even the neutral one.** A typo in a provider name would otherwise select AWS defaults silently
against a MinIO endpoint and fail later, at the first multipart upload, far from the cause, and the operator reading
that failure has no reason to suspect the profile name because nothing reported it as unrecognised.

### The evidence marker on every profile cell

Each cell carries exactly one marker, and the five are not interchangeable.

- `[repo]` — verified from the fleet's consumer `[source: tusd-upload-platform repository, .env.example and
  internal/storage/s3_compatible.go, read: 2026-07-28]`, and for the signature version `[source:
  tusd-upload-platform repository, docker-compose.yml, where the provisioner passes `mc alias set … --api S3v4`,
  read: 2026-07-27]`.
- `[arvan]` — published by ArvanCloud and read on 2026-07-28. The URL and the arithmetic behind each of these cells
  are in `/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`)
  `references/15-environment-contract-deltas.md`, which owns that column.
- `[est]` — this skill's conservative estimate pending confirmation. Quote it to nobody as a provider limit, because
  it is not one.
- `[unv]` — believed correct and **unverified as of 2026-07-28**, because no AWS or MinIO documentation was
  reachable in the session that wrote this table. Fetch the primary source before a capacity or a cost decision
  rests on one of these.
- `[open]` — no profile entry, because nobody has established the value for that provider. The baseline default in
  the variables table governs, and the numbered question below records what is missing.

**A floor may carry `[est]` and a ceiling may not.** A floor guessed too high rejects a part locally, before a byte
is sent; a ceiling guessed too high is discovered by the store after the whole part crossed the network, so a
ceiling nobody has read is `[open]` rather than a number.

### The profile table

| Variable | `minio` | `arvancloud` | `aws` | `generic-s3` |
|---|---|---|---|---|
| `STORAGE_ENDPOINT` shape | `http://<host>:9000`, one host with no region in it `[repo]` | `https://s3.<region>.arvanstorage.ir` `[arvan]` | `https://s3.<region>.amazonaws.com` `[unv]` | required, and no shape assumed `[est]` |
| `STORAGE_REGION` | `us-east-1`, a placeholder `[repo]` that MinIO is believed not to enforce `[unv]` | `ir-thr-at1` or `ir-tbz-sh1`, paired with the endpoint it belongs to `[arvan]` | required, and set to the bucket's own region `[unv]` | required, and set to the provider's own region identifier `[est]` |
| `STORAGE_USE_PATH_STYLE` | `true` `[repo]` | `false` `[arvan]` | `false` `[unv]` | `true` `[est]` |
| `STORAGE_TLS_ENABLED` | `false`, for the loopback test stack only `[repo]` | `true` `[est]` | `true` `[unv]` | `true` `[est]` |
| `STORAGE_SIGNATURE_VERSION` | `s3v4` `[repo]` | `s3v4` `[est]` | `s3v4` `[unv]` | `s3v4` `[est]` |
| `STORAGE_PART_SIZE_BYTES` | `16777216` `[est]` | `16777216` `[est]` | `16777216` `[est]` | `16777216` `[est]` |
| `STORAGE_MIN_PART_SIZE_BYTES` | `5242880` `[est]` | `5242880` `[arvan]`, taken at the mebibyte reading | `5242880` `[unv]` | `5242880` `[est]` |
| `STORAGE_MAX_PART_SIZE_BYTES` | `[open]`, question 1 | `400000000` `[arvan]` | `5368709120` `[unv]` | `400000000` `[est]` |
| `STORAGE_MAX_PARTS` | `[open]`, question 2 | `10000` `[arvan]` | `10000` `[unv]` | `10000` `[est]` |
| `STORAGE_MAX_OBJECT_BYTES` | `[open]`, question 2 | `4000000000000`, derived by the minimum rule `[arvan]` | `5000000000000` `[unv]`, question 3 | `4000000000000` `[est]` |
| `STORAGE_PRESIGN_MAX_SECONDS` | `900` `[est]`, question 4 | `900` `[est]`, question 4 | `900` `[est]`, question 4 | `900` `[est]`, question 4 |

The `minio` column sets `STORAGE_TLS_ENABLED` to `false` because that is what the fleet's consumer runs against a
loopback development store, and the validation rule below still refuses a startup where TLS is off and the endpoint
host is not a loopback address. **Selecting the `minio` profile against a remote MinIO therefore fails at boot
rather than sending plaintext**, which is the intended interaction between the two.

`STORAGE_PART_SIZE_BYTES` and `STORAGE_PRESIGN_MAX_SECONDS` carry the same value in all four columns today. They
stay in the table because both are provider-dependent in principle and identical only because nobody has read a
provider's answer, and deleting either row would hide that.

The `generic-s3` column takes the smallest figure this skill has seen published for each ceiling, which is
ArvanCloud's. **Adopt `generic-s3` for a provider whose documentation nobody has read yet**, because a ceiling set
to the smallest known figure fails locally and cheaply while a ceiling copied from AWS fails after the bytes crossed
the network.

### The cells nobody has filled

1. **MinIO's own maximum part size.** No MinIO documentation was reachable this session, so the `minio` column
   carries no ceiling and the baseline `5368709120` governs. Read MinIO's own limits before any upload sizes a part
   above 400 MB against MinIO.
2. **MinIO's own maximum part count and maximum object size.** Same session limit and same consequence: the
   baseline `10000` parts and `5000000000000` bytes govern, and neither figure was read from MinIO.
3. **Whether AWS S3 publishes its object ceiling as 5 TB or 5 TiB.** The `aws` column carries `5000000000000`, the
   smaller reading, by the minimum rule above. Confirm it before anything is designed above 4.5 TB.
4. **The maximum presigned-URL lifetime each provider honours.** `604800` is recorded as the SigV4 ceiling and is
   unverified, ArvanCloud publishes a 12-hour example rather than a limit, and MinIO's figure was not read. Every
   column carries `900` because a lifetime nobody has confirmed is a bearer credential nobody can withdraw.
5. **Whether ArvanCloud accepts path-style addressing at all.** This is open question 2 in
   `/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`) `references/SOURCES.md`, and the `arvancloud` column
   carries `false` because virtual-hosted is the documented style, not because path-style was tested and refused.
6. **Whether MinIO enforces `STORAGE_REGION` at all.** The `minio` column carries `us-east-1` because the fleet's
   consumer sets it; whether MinIO validates the value was not read.

### Adopting a new provider

**Fill a new column from that provider's own published documentation, put a read date on every cell, and copy no
cell from another provider's column.** Two S3-compatible providers agree on the API and disagree on the limits, so a
copied ceiling is a guess wearing another provider's citation and it is discovered at the first upload large enough
to reach it.

**Add the new profile name to the validation list in the variables table in the same change**, because rule 3
refuses to start on a name the list does not carry, and a column added without its name is a profile nobody can
select.

## Validate at the boundary, before the client is constructed

**Validate every variable in the table in one function that runs before the storage client is constructed, and
refuse to start on any violation.** A storage value validated at first use fails during a user's upload instead of
during deployment, which converts a configuration mistake into an incident and hides the cause behind whatever
request happened to arrive first.

**Refuse to start when a variable marked required is unset, and substitute no default for it.** An endpoint, a
bucket or a credential invented by the process points production at something nobody chose, and the resulting
not-found is indistinguishable from deleted data.

**Emit the validated configuration once at startup with every secret replaced by a redaction marker.** An operator
who cannot see which values took effect debugs a wrong env value by reading code, and the fleet's consumer already
demonstrates the shape in its redacted runtime plan `[source: tusd-upload-platform repository,
internal/storage/s3_compatible.go, read: 2026-07-28]`.

**State the effective value and its source in the startup line, as one of `baseline`, `profile` or `env`, so a
default is distinguishable from a set value.** A number that came from this file's baseline, a number the selected
provider profile supplied and a number an operator chose need different responses when they turn out to be wrong.
Rule 2 under "The provider profile" owns the resolution order these three names describe.

## The reachable object size is derived, never configured

The largest object a multipart upload can actually assemble is:

```
reachable object bytes = STORAGE_PART_SIZE_BYTES x STORAGE_MAX_PARTS
```

**Compute that product at startup and compare it against the largest object the service accepts.** With the
defaults above the product is 16 MiB x 10,000, which is about 160 GB, far below `STORAGE_MAX_OBJECT_BYTES`. That
is the intended shape: `STORAGE_MAX_OBJECT_BYTES` records the provider's ceiling, and the product records what this
deployment's part size actually reaches.

**Raise `STORAGE_PART_SIZE_BYTES` rather than `STORAGE_MAX_PARTS` when the service must store an object larger than
the product.** The part count is a provider limit and the part size is a local choice, so raising the part size is
an env change and raising the part count is a request to the provider that will be refused.

## Not owned here

Timeout, retry, backoff and breaker values are `/alaa-reliability-sla` (`$alaa-reliability-sla`). Registration of a
fleet-wide value so two services cannot hold two different numbers is `/alaa-services-contract`
(`$alaa-services-contract`). Where these variables are set — a Compose file, a Swarm stack, a Kubernetes Secret or
a secret manager — is `/alaa-docker-production` (`$alaa-docker-production`) and `/alaa-k8s-helm`
(`$alaa-k8s-helm`). The ArvanCloud values that differ are `/alaa-arvan-object-storage`
(`$alaa-arvan-object-storage`) `references/15-environment-contract-deltas.md`.
