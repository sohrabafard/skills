# Topic Map

Load the one file whose condition matches the task in front of you. Every row states a situation you can observe,
not a subject heading. The out-of-skill routing table lives in `SKILL.md` under "Not owned here"; this file routes
only inside the skill, so the two cannot drift.

| You are about to | Read |
|---|---|
| read a storage value from the environment, choose or change a default for one, name a new storage variable, or validate one at startup | `references/05-environment-contract.md` |
| choose the provider a deployment points at, set `STORAGE_PROVIDER_PROFILE`, add a column for a provider the fleet has not used before, or decide whether a difference between two providers is a new `STORAGE_*` knob or a branch in code | `references/05-environment-contract.md` |
| create a bucket, name one, decide how many buckets a service gets, or write or change an object key | `references/10-buckets-and-object-keys.md` |
| add or change a lifecycle rule, decide how long anything stays in a bucket, or explain a bill that grows with no matching object count | `references/20-lifecycle-and-retention.md` |
| create a storage identity, write or review a bucket or IAM policy, hand a credential to a process, or rotate one | `references/30-identity-credentials-and-access.md` |
| turn on server-side encryption or replication, decide whether a bucket may be versioned or whether versioning may be turned off again, or decide whether a plaintext hop to the store is acceptable | `references/40-encryption-tls-and-durability.md` |
| choose a multipart part size, size the disk or memory an uploading process needs, or set a bucket quota or cost budget | `references/50-multipart-capacity-and-cost.md` |
| issue a presigned URL, let a browser talk to the bucket directly, or put a CDN in front of it | `references/60-presigned-urls-and-delivery.md` |
| add, replace or configure an object-storage client library in any language, or set the S3 signature version a client signs with | `references/70-client-libraries.md` |
| set `STORAGE_USE_PATH_STYLE`, explain a bucket that answers under one addressing style and not the other, or read a TLS hostname mismatch that names a bucket | `references/70-client-libraries.md` |
| run any `mc` command, write or change a provisioning script, or put an `mc` invocation into a runbook | `references/75-mc-command-line-client.md` |
| stand the store up locally or in a deployed environment, decide shared-versus-per-service, or publish a port | `references/80-topology.md` |
| diagnose a failing storage call, decide whether to retry it, or write the runbook entry for one | `references/90-failure-classes.md` |
| decide what to measure about the store, or prove that a failure class is actually visible | `references/95-observability.md` |
| move objects or a client between MinIO and ArvanCloud, or size a multipart part against ArvanCloud's stricter 400 MB ceiling | `/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`) `references/40-migration-and-portability.md` |
| repeat a version-sensitive claim about S3, MinIO or a client SDK, or re-check a claim in this skill against its origin | `references/SOURCES.md` |

## Reading order for a new bucket

`references/10-buckets-and-object-keys.md`, then `references/30-identity-credentials-and-access.md`, then
`references/20-lifecycle-and-retention.md`, then `references/40-encryption-tls-and-durability.md`. A bucket that
exists before its policy and its lifecycle rules exist is a bucket that will still be missing them a year later,
because nothing fails while they are absent.

## Reading order for a provisioning script or a one-off operator action

`references/80-topology.md` for the steps a provisioner performs and in what order, then
`references/75-mc-command-line-client.md` for how each step is expressed and which commands must not appear in a
script at all. Read the second before running anything, not after: the destructive commands and the rule keeping a
credential out of `argv` are both there, and neither is recoverable once broken.
