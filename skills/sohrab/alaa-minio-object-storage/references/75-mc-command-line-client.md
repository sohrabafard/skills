# The `mc` command-line client

This file owns every direct human or agent interaction with the store through MinIO's `mc` client: how an alias is
configured, which commands read and which destroy, and how a credential reaches `mc` without leaking. Read it
before running any `mc` command, before writing or changing a provisioning script, and before putting an `mc`
invocation into a runbook. The client a service's own code uses is `70-client-libraries.md`; `mc` is the operator's
and the agent's client and is never the application's. The steps a provisioner performs, in order, are
`80-topology.md`; this file owns only how those steps are expressed and what they must not do.

Spellings marked **repo-verified** were read from the fleet's own files this session. Every other spelling is
marked as needing verification, because no MinIO documentation was reachable in this session and a wrong flag
copied out of this file into a runbook is worse than a named unknown. `SOURCES.md` lists them in one place.

## Configuring an alias, and where the credential lands

An alias binds a name to an endpoint, an access key, a secret key and a signature version, so later commands
address `alias/bucket/key` instead of repeating all four. The fleet's provisioner sets one this way, and this
spelling is **repo-verified** `[source: tusd-upload-platform repository, docker-compose.yml,
docker-compose.swarm.yml and scripts/docker/smoke-compose-*.sh, read: 2026-07-27]`:

```sh
mc alias set local "$STORAGE_ENDPOINT" "$STORAGE_ACCESS_KEY" "$STORAGE_SECRET_KEY" --api S3v4
```

**Never pass an access key or a secret key as a positional argument to `mc`.** The shell expands the variable
before `mc` starts, so the plaintext secret lands in that process's `argv`, where every process in the same PID
namespace can read it from the process list and where an interactive shell writes it into its history file.
Redacting the value from the script's own output does not remove it from `argv`. The five invocations cited above
are exactly this defect; they are the fleet's current state, not a pattern to copy.

Supply the credential to `mc` by one of these two instead, in this order:

1. **The alias environment-variable form**, which carries the endpoint and the credential in one variable `mc`
   reads from its environment rather than from `argv`. The variable is named after the alias and the value embeds
   the credential in the URL. *The exact spelling needs verification* — believed to be `MC_HOST_<alias>` holding
   `https://<access-key>:<secret-key>@<endpoint>` — so confirm it against the client reference before scripting it
   `[source: https://min.io/docs/minio/linux/reference/minio-mc.html, read: unverified as of 2026-07-27]`.
2. **A configuration file written into a scoped configuration directory with mode `0600`** by the process that
   already holds the secret. This works on any `mc` release regardless of flag renames, because that file is what
   `mc alias set` writes anyway.

**Treat `mc`'s configuration directory as credential storage with the lifetime of the filesystem under it.**
`mc alias set` persists the alias, secret key included, into a configuration file, so a credential entered once is
available to every later `mc` run by that user — including one belonging to a different task, in a different
environment, against a different store. The default location is believed to be `~/.mc/config.json` and the
override flag is believed to be `--config-dir`; *both spellings need verification*
`[source: https://min.io/docs/minio/linux/reference/minio-mc.html, read: unverified as of 2026-07-27]`.

**Point every scripted `mc` run at a configuration directory it creates and removes itself.** Reason: persisted
alias state means a command whose alias argument is wrong or stale still resolves, so a cleanup written for staging
executes against production and reports success.

## The signature version

`--api S3v4` on `mc alias set` selects the S3 signature version and `S3v2` selects the legacy one; the `S3v4`
spelling is **repo-verified** from the invocation above and the `S3v2` spelling *needs verification*
`[source: https://min.io/docs/minio/linux/reference/minio-mc/mc-alias.html, read: unverified as of 2026-07-27]`.
The rule that the signature version is stated explicitly, and its equivalent in every client library, is
`70-client-libraries.md`; do not decide it here. When `mc` fails to authenticate against an endpoint a client
library reaches successfully, compare the two signature versions first — `90-failure-classes.md` class 2.

## Bucket commands

| Command | Effect | Destructive |
|---|---|---|
| `mc mb <alias>/<bucket>` | creates a bucket, failing when it exists | no |
| `mc mb -p <alias>/<bucket>` | creates a bucket, succeeding when it exists | no |
| `mc ls <alias>` / `mc ls <alias>/<bucket>/<prefix>` | lists buckets, or keys under a prefix | no |
| `mc stat <alias>/<bucket>` | reports one bucket's or one object's metadata | no |
| `mc du <alias>/<bucket>` | reports bytes on disk, which an object listing does not show | no |
| `mc rb <alias>/<bucket>` | removes a bucket | **yes** |

`mc mb -p` and `mc stat` are **repo-verified**; the rest *need verification*
`[source: https://min.io/docs/minio/linux/reference/minio-mc.html, read: unverified as of 2026-07-27]`.

**Use `mc mb -p` in any script that can run twice.** Reason: plain `mc mb` fails when the bucket already exists,
which turns the second deployment of an unchanged stack into a failed provisioning step.

**Never put `mc rb` in a script.** Re-running the script that created the bucket does not restore its objects, so
a bucket removal is an operator action taken by hand against a named alias after the owner has authorised that
exact bucket.

## Policy and anonymous access

`mc` sets the bucket's anonymous-access posture and its policy document. The subcommand was renamed between
releases: the current name is believed to be `mc anonymous` with `set`, `get` and `list` verbs, and `mc policy` is
believed to survive as the older name in some releases. **Both spellings need verification before use**
`[source: https://min.io/docs/minio/linux/reference/minio-mc/mc-anonymous.html, read: unverified as of
2026-07-27]`. Determine which one the pinned image accepts by running it with `--help` inside that image before
writing it into a script, because a script written against the other name fails at deploy time.

**Set the anonymous-access posture to none explicitly, on every bucket, at provisioning time.** MinIO and AWS
differ on what an unconfigured bucket allows, so a bucket that is private because nobody ran the command is private
by accident and stays that way only until someone runs a different one. This is `SKILL.md` rule 7, and the policy
document's shape is `30-identity-credentials-and-access.md`.

**Never grant anonymous download on a bucket holding user-supplied bytes.** Under anonymous read the object key
becomes the only credential, and keys leak through logs, referrer headers and browser history; serve those bytes
through the application or a presigned URL instead, per `60-presigned-urls-and-delivery.md`.

## Lifecycle rules

`mc ilm` is how the abort-incomplete-multipart rule that `20-lifecycle-and-retention.md` makes mandatory actually
reaches a MinIO bucket, and the fleet runs no `mc ilm` command anywhere. The family covers adding a rule, listing
the rules in force, removing one, and importing or exporting the whole configuration as a JSON document; *exact
verb and flag spellings need verification*
`[source: https://min.io/docs/minio/linux/reference/minio-mc/mc-ilm.html, read: unverified as of 2026-07-27]`.

**Apply a lifecycle configuration as a JSON document through `mc ilm` import rather than as a series of
flag-driven rule additions.** The JSON field names are the S3 API names — `AbortIncompleteMultipartUpload` with
`DaysAfterInitiation`, `NoncurrentVersionExpiration`, `Expiration` — and those are stable across `mc` releases,
while the equivalent command flags have been renamed between releases and a renamed flag fails the deployment that
first meets it. Keep the document in the repository beside the provisioning script so the applied rules are
reviewable in a diff.

**Read the lifecycle configuration back after applying it and fail the provisioning step on any difference.**
Reason: a zero exit proves the command was accepted, and only a read-back proves the rule is in force on the
bucket the application will use.

## Versioning, replication and encryption

| Capability | Believed command family | Status |
|---|---|---|
| enable, suspend or report bucket versioning | `mc version enable`, `mc version suspend`, `mc version info` | *needs verification* |
| configure or inspect bucket replication | `mc replicate add`, `mc replicate ls`, `mc replicate status` | *needs verification* |
| configure or inspect server-side encryption | `mc encrypt set`, `mc encrypt info` | *needs verification* |

`[source: https://min.io/docs/minio/linux/reference/minio-mc.html, read: unverified as of 2026-07-27]`

**Never run the versioning-enable command before reading `40-encryption-tls-and-durability.md`.** Enabling
versioning on a bucket cannot be undone — only suspended — so it is a one-way change, and which buckets may take
it is decided there rather than here.

## Object commands during an incident

Split them by what they do to the store, because an incident is exactly when that distinction gets lost.

**Read-only, safe to run while diagnosing.** `mc ls` lists keys under a prefix; `mc stat` reports one object's
size, type and metadata; `mc du` reports bytes on disk under a prefix and is the command that reveals storage an
object listing does not account for; `mc find` filters keys by name, age or size; `mc head` prints the beginning
of an object; `mc cat` prints an object's whole content to standard output.

**Writing or deleting, never run without the owner's explicit authorisation naming that exact target.** `mc cp`
copies into the store; `mc mv` copies and then deletes the source; `mc rm` deletes objects and, with a recursive
flag, every object under a prefix; `mc mirror` makes a target match a source and, with its removal flag, deletes
whatever the target has and the source does not; `mc rb` removes a bucket. Reason for requiring authorisation:
none of these has an undo, the store applies no confirmation step, and each one succeeds just as quietly against
the wrong prefix as against the right one. *All spellings in both groups need verification*
`[source: https://min.io/docs/minio/linux/reference/minio-mc.html, read: unverified as of 2026-07-27]`.

**Never run `mc cat` against an object holding user-supplied bytes.** The content goes to standard output, which
lands in terminal scrollback, in any session transcript, and in whatever log captures the command — so a
diagnostic command discloses the exact data the bucket exists to protect. Use `mc stat` for size and type, and
copy the object to a scoped local path when the bytes themselves are genuinely needed.

**Run `mc mirror` in its dry-run mode first and read the plan before running it for real.** Mirror exists to make
one side match the other, so a reversed source and target pair replaces the good side with the empty one and
reports success while doing it. *The dry-run flag spelling needs verification.*

**Never clean up after an incident with a recursive delete.** A prefix that was correct in the environment you
tested is a different prefix in the environment you are in. Delete by explicit key list, or add a lifecycle rule
filtered to that prefix and let the store do it, per `20-lifecycle-and-retention.md`.

## `mc admin`, and why an application must never reach it

`mc admin` addresses MinIO's administrative API rather than the S3 API: server and cluster information, user and
group creation, policy attachment, service restart, request tracing, and healing. *Spellings need verification*
`[source: https://min.io/docs/minio/linux/reference/minio-mc-admin.html, read: unverified as of 2026-07-27]`.

**An application identity's policy grants no administrative action.** An identity that can run `mc admin` can
create a user with full access, attach a policy to itself, restart the service, and trace every other tenant's
requests, so one compromised application process becomes control of the store rather than access to one prefix.
This is `SKILL.md` rule 1, enforced by the policy in `30-identity-credentials-and-access.md`.

**Run `mc admin` from the provisioning or operator identity only, and only for the duration of that task.** An
admin credential left in a long-lived process's environment is an admin credential in every later incident that
process is part of.

**Agree what `mc admin trace` prints before running it against a store carrying production traffic.** A trace
carries object keys and request headers — secrets under `SKILL.md` rule 4 and rule 7 — for every tenant, not only
the one under investigation.

## Scripting `mc`

**Pass the JSON output flag on every `mc` invocation inside a script and parse the JSON.** Human-readable output
is not a contract: column order, wording and the presence of a summary line change between releases, so a script
that greps human output breaks on an image bump with no error naming the cause. The flag is believed to be
`--json`, with quiet and colour-suppression flags alongside it; *the exact spellings need verification*
`[source: https://min.io/docs/minio/linux/reference/minio-mc.html, read: unverified as of 2026-07-27]`.

**Check the exit status of every `mc` command and stop the script on a non-zero one.** The fleet had exactly this
defect: `mc mb -p ... || true` hid every bucket-creation failure and left the API reporting itself ready against a
bucket that did not exist. Both Compose files now fail closed on alias setup, bucket creation and the `mc stat`
read-back, and a static guard rejects the `|| true` pattern if it returns
`[source: tusd-upload-platform repository, <repo>/docs/agents/tusd-api-contract-state.md and
scripts/docker/validate-compose-runtime.sh, read: 2026-07-27]`.

**Discard `mc`'s output on the success path and print a fixed message instead.** `mc` prints the alias, endpoint,
bucket and object key, and none of those belongs in a log; on the failure path print the failing step by name and
nothing else, so the operator learns which step failed without learning the bucket. The fleet's provisioner
already does this, printing `Object storage provisioned: status=ok`
`[source: tusd-upload-platform repository, docker-compose.yml, read: 2026-07-27]`.

**Keep a provisioning script idempotent and non-destructive**, because it runs on every deployment including the
one where an environment variable was wrong. The fleet's provisioner is the good example to copy on this point: it
runs `mc alias set`, then `mc mb -p`, then `mc stat` as a read-back, checks every exit status, and removes nothing
`[source: tusd-upload-platform repository, docker-compose.yml and docker-compose.swarm.yml, read: 2026-07-27]`.
Its two defects are the credential in `argv` and stopping after bucket creation — no policy, no versioning
decision, no encryption and no lifecycle, so no abort-incomplete-multipart rule.

## `mc` against MinIO versus another S3-compatible endpoint

**Confirm every `mc` command against the endpoint it will actually run against before putting it in a runbook**,
because the three command groups fail differently. `mc admin` needs MinIO's administrative API, which AWS S3 and
most other S3-compatible stores do not implement, so those commands fail there regardless of the credential.
`mc ilm`, `mc version`, `mc replicate`, `mc anonymous` and the object commands map onto S3 APIs, so a store
implementing only part of the API fails that one subcommand rather than the connection — which reads as an `mc`
problem and is not one. Addressing and signing differ too: a self-hosted store usually needs path-style addressing
per `40-encryption-tls-and-durability.md` and the signature version stated explicitly per `70-client-libraries.md`.

## What the fleet does today

- **Every `mc alias set` in the repository passes the access key and secret key positionally**, in both Compose
  files and in three smoke scripts `[source: tusd-upload-platform repository, docker-compose.yml,
  docker-compose.swarm.yml and scripts/docker/smoke-compose-*.sh, read: 2026-07-27]`.
- **The alias is configured with the store's root credential**, because `STORAGE_ACCESS_KEY` defaults to
  `MINIO_ROOT_USER` `[source: tusd-upload-platform repository, docker-compose.yml, read: 2026-07-27]`.
- **No `mc ilm`, `mc anonymous`, `mc policy`, `mc version`, `mc encrypt` or `mc replicate` invocation exists
  anywhere in the repository**, and no `mc` invocation uses `--json` or a scoped configuration directory
  `[source: tusd-upload-platform repository, read: 2026-07-27]`.

`scripts/check_object_storage_posture.py` fires `MC_CREDENTIAL_ON_COMMAND_LINE` on the first of those, and it
reported all five on 2026-07-27 at `docker-compose.yml:132`, `docker-compose.swarm.yml:117`,
`scripts/docker/smoke-compose-upload.sh:219`, `scripts/docker/smoke-compose-zip-extraction.sh:287` and
`scripts/docker/smoke-compose-tar-tgz-extraction.sh:320`.
