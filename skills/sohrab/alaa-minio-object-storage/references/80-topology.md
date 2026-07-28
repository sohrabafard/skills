# Topology: local and deployed

This file owns where the store runs, who reaches it, and which ports exist. Read it before standing a store up,
before attaching one to a shared network, and before publishing a port.

## The local store is a test convenience, and production is a real store reached from configuration

**Treat the MinIO container declared in a Compose or Swarm file as a development and test convenience, and point
production at a real MinIO or S3-compatible store whose endpoint, bucket, region and credentials arrive as
environment values.** The local container exists so a test can run without a network dependency and so a developer
can see bytes land somewhere; it is not a description of how the service is deployed. The production values are
`STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_REGION`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`, and
`references/05-environment-contract.md` owns their defaults and their validation.

Four consequences follow, and each one is a mistake that is easy to make while reading a repository.

1. **Read a Compose file's credentials, published ports and root-user posture as properties of a test stack.** A
   root user in a Compose file says what the test store was stood up with, and it says nothing about which
   identity the production store issues, because a different operator provisions that one.
2. **Write no rule about production from evidence found only in a Compose file.** A Compose file is evidence about
   the stack that file stands up, so a claim about production drawn from it is an inference presented as an
   observation, and it will be repeated later as though it had been checked.
3. **Name the environment a storage finding is about, every time you record one.** A finding written without its
   environment is read as a production defect by the next person, which spends an incident budget on a test-stack
   artefact, or is dismissed as "only development" when it is real.
4. **Ask what identity the production store issues rather than assuming it matches the test stack.** The question
   is answerable by whoever provisions that store, and leaving it unasked is what makes a test-stack observation
   quietly become a production assumption.

**Point the local store at the same variable names production uses, and change only their values.** A test stack
configured through a different set of names proves nothing about whether production's configuration path works,
and the first time anyone finds out is the first deployment.

## Shared store or one per service

**Give a service its own bucket, and decide the store separately.** The two questions are usually conflated: bucket
isolation is a policy decision that costs nothing, while a separate store instance is an operational decision that
costs a volume, a backup, a monitor and an upgrade path.

Run a **shared store** when several services need the same durability posture and the same operational owner, and
per-service buckets with per-service identities give the isolation. Run a **per-service store** when one service's
capacity or throughput would starve the others, when its data has a different regulatory posture, or when it must
be able to fail without taking the others with it.

**Whichever you choose, the bucket policy and the scoped identity are not optional.** A store reachable from a
shared network is reachable by every service on that network, so "it is only development" is precisely the
condition under which the missing policy gets copied into production.

The fleet's only object-storage consumer runs its **test-stack** MinIO **per service**: image
`minio/minio:RELEASE.2025-09-07T16-13-09Z-cpuv1`, command `server /data --console-address ":9001"`, volume
`minio_data:/data`, aliased `tusd-minio` on the service network and **also attached to `alaa-shared-network`**. The
Swarm stack is identical at `replicas: 1` with no distributed-mode erasure set
`[source: tusd-upload-platform repository, docker-compose.yml and docker-compose.swarm.yml, read: 2026-07-27]`.

## Exposure

**Publish the store's API port only on the interface an operator actually needs, and do not publish the console port
at all in a deployed environment.** A management console reachable from outside the host is an authentication
surface with root-equivalent power over every bucket.

**Check the exposure of the store against the exposure of the service it serves.** The fleet's consumer publishes
MinIO's `9000` and `9001` on all interfaces while the API those buckets exist for is bound to loopback
`[source: tusd-upload-platform repository, docker-compose.yml, read: 2026-07-27]`. The storage plane is therefore
more reachable than its consumer, which inverts the intended trust ordering: an attacker who cannot reach the
service can still reach the bytes.

## Development topology

A development store is worth having only if it behaves like the deployed one on the axes that break code. Stand it
up with:

1. **A pinned image tag, never `latest`**, so a store upgrade is a commit rather than a Monday-morning surprise.
2. **A named volume**, so a container restart does not silently empty the bucket and turn a data bug into a
   "works after restart" mystery.
3. **A health check that proves the process answers**, used as a dependency condition for anything that provisions
   or consumes the bucket.
4. **A one-shot provisioner** that is idempotent and non-destructive, running after the health check passes.

## What a provisioner must do

A provisioner that only creates the bucket leaves every other bucket-level setting at the store's default, and
those defaults are where the cross-store differences live. **Provision in this order, and verify after each step:**

1. Create the bucket if absent.
2. Apply the access policy, explicitly including block-public-access.
3. Apply versioning if the bucket needs it.
4. Apply server-side encryption if the bucket needs it.
5. Apply the lifecycle configuration, including the abort-incomplete-multipart rule.
6. Read the applied configuration back and fail loudly on any difference.

**Never make the provisioner destructive.** It runs on every deployment, including the one where an environment
variable was wrong.

The fleet's provisioner is a one-shot `minio/mc:RELEASE.2025-08-13T08-35-41Z-cpuv1` container running `mc alias
set`, then `mc mb -p`, then `mc stat`. It is correctly idempotent and correctly non-destructive, and it sets **no
policy, no versioning, no encryption and no lifecycle**
`[source: tusd-upload-platform repository, docker-compose.yml, read: 2026-07-27]`. Steps 2 through 6 above are the
gap.

## Deployed topology

**Point production at a store whose durability posture was chosen deliberately, and not at a single-node,
single-drive instance.** A single node with a single drive has no erasure coding and no replica, so the loss of
one disk is the loss of every object, and the local development store is exactly that shape.

**A single-node, single-drive store is not a production durability posture.** It has no erasure coding and no
replica, so the loss of one disk is the loss of every object. For production either use a managed S3-compatible
service, or run a multi-node erasure-coded deployment sized against the failure count it must survive
`[source: https://min.io/docs/minio/linux/operations/concepts/erasure-coding.html, read: unverified as of
2026-07-27]`.

**State the recovery story before the store holds anything that matters**: what a disk failure costs, what an
operator's mistaken delete costs, and which of `40-encryption-tls-and-durability.md`'s protections is the one that
recovers it.

## Not owned here

Container image construction, Compose and Swarm file expression, registry and secret mechanics:
`/alaa-docker-production` (`$alaa-docker-production`). Kubernetes manifests, Helm charts, StatefulSets and storage classes:
`/alaa-k8s-helm` (`$alaa-k8s-helm`), with Arvan specifics in `/caas-arvan-kuber` (`$caas-arvan-kuber`). Canonical
shared-infrastructure names and ports: `/alaa-services-contract` (`$alaa-services-contract`).
