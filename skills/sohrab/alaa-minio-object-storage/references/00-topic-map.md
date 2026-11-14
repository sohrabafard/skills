# Topic Map

Load the one file whose condition matches the task in front of you. Every row states a situation you can observe,
not a subject heading. The first table routes inside this skill. The table under "Not owned here" routes work that
another skill owns.

| You are about to | Read |
|---|---|
| read a storage value from the environment, choose or change a default for one, name a new storage variable, or validate one at startup | `references/05-environment-contract.md` |
| choose the provider a deployment points at, set `STORAGE_PROVIDER_PROFILE`, add a column for a provider the fleet has not used before, or decide whether a difference between two providers is a new `STORAGE_*` knob or a branch in code | `references/05-environment-contract.md` |
| create or name a bucket, choose bucket count, or define generic key namespaces and trusted tenant prefixes, including those used by tus | `references/10-buckets-and-object-keys.md` |
| add or change a lifecycle rule, decide how long anything stays in a bucket, or explain a bill that grows with no matching object count | `references/20-lifecycle-and-retention.md` |
| create a storage identity, write or review a bucket or IAM policy, hand a credential to a process, or rotate one | `references/30-identity-credentials-and-access.md` |
| turn on server-side encryption or replication, decide whether a bucket may be versioned or whether versioning may be turned off again, or decide whether a plaintext hop to the store is acceptable | `references/40-encryption-tls-and-durability.md` |
| size a non-tus application client's parts and buffers, check provider bounds, or set bucket capacity and cost budgets | `references/50-multipart-capacity-and-cost.md` |
| size tusd parts and temp disk, or choose its upload-specific key and sidecar layout under the shared namespace rules | `/tusd-upload-platform` `references/35-storage-lifecycle.md` |
| issue a presigned URL, let a browser talk to the bucket directly, or put a CDN in front of it | `references/60-presigned-urls-and-delivery.md` |
| add, replace or configure an object-storage client library in any language, or set the S3 signature version a client signs with | `references/70-client-libraries.md` |
| set `STORAGE_USE_PATH_STYLE`, explain a bucket that answers under one addressing style and not the other, or read a TLS hostname mismatch that names a bucket | `references/70-client-libraries.md` |
| run any `mc` command, write or change a provisioning script, or put an `mc` invocation into a runbook | `references/75-mc-command-line-client.md` |
| stand the store up locally or in a deployed environment, decide shared-versus-per-service, or publish a port | `references/80-topology.md` |
| diagnose a failing storage call, decide whether to retry it, or write the runbook entry for one | `references/90-failure-classes.md` |
| decide what to measure about the store, or prove that a failure class is actually visible | `references/95-observability.md` |
| move objects or a client between MinIO and ArvanCloud, or size a multipart part against ArvanCloud's stricter 400 MB ceiling | `/alaa-arvan-object-storage` `references/40-migration-and-portability.md` |
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

## Not owned here

| You are about to | Use |
|---|---|
| choose between Postgres and Redis, design a table or index, or tune a query, pool or cache | `/alaa-data-layer` |
| shape a retry, backoff, timeout, breaker, idempotency key or degradation policy | `/alaa-reliability-sla` |
| name a metric, log field, event, error code or header, or use an Ala platform value such as a timeout or retry budget | `/alaa-services-contract` `references/22-failure-load-and-deprecation-contract.md` |
| decide whether telemetry is required, or which gate it must pass | `/alaa-observability-soc` |
| trigger a security review, classify a threat, or apply fail-closed doctrine | `/alaa-security-review` |
| write a Dockerfile, Compose file or Swarm stack, or harden an image | `/alaa-docker-production` |
| write a Kubernetes manifest or a Helm chart | `/alaa-k8s-helm`, Arvan specifics in `/caas-arvan-kuber` |
| change an HAProxy directive in front of the store | `/alaa-haproxy` |
| decide which layer a behaviour is tested at, or what proof a claim reached | `/alaa-testing-strategy` `references/40-proof-strength.md` |
| size a tus part, build an upload-session key, or retain an unfinished upload | `/tusd-upload-platform` |
| check work against the ten-point quality bar | `/alaa-project-constitution` `references/quality-bar.md` |
| point a bucket or client at an ArvanCloud endpoint, choose an Arvan region, or check whether an S3 operation works on ArvanCloud | `/alaa-arvan-object-storage` |
| choose a model or an effort level | `/alaa-prompting-guide` |
