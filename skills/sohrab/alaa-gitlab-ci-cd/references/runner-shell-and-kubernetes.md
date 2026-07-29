# Runner: shell and Kubernetes executors

Runner architecture and configuration. Failure triage lives in
`validation-and-debugging.md`; image pinning syntax lives in
`cache-artifacts-and-pinning.md`.

## Table of contents

- Choosing an executor
- Shell runner operating model and hardening
- Kubernetes executor operating model
- Helm values versus embedded TOML
- `concurrent` and per-runner limits
- Image pull secrets and the helper image
- Distributed cache
- RBAC and namespace design
- Restricted and read-only clusters

## Choosing an executor

| Use | When |
|---|---|
| Kubernetes executor | the default. Each job is a fresh pod, isolation is real, capacity is elastic, and cleanup is the cluster's problem |
| shell executor | the job needs a tool that only exists on a specific host, or a daemon that host already runs, **and** the host serves no other tenant, the runner is tagged so only the intended projects reach it, and the jobs that use it run on protected refs |
| Docker executor | a single host that should still give each job a container boundary |

A shell runner executes the job script directly on the host as the runner user.
The build directory persists between jobs and between projects that share the
host, so anything a job writes there — a cached credential, a `.git/config`, a
temp file — is readable by the next job that lands on it.

## Shell runner operating model and hardening

Baseline for a shell runner:

- Dedicate the host. "Trusted" means: the projects that can reach this runner are
  trusted, the branches that can reach it are trusted, host-level access by a job
  is acceptable, and no other tenant shares the host.
- Tag the runner and pin the intended jobs to that tag, so placement is a
  decision rather than a coincidence.
- Set `builds_dir` and `cache_dir` explicitly, so the persistent surface has a
  named location that can be audited and cleaned.
- Use `GIT_STRATEGY: clone` rather than `fetch` on any host that more than one
  project or more than one branch can reach; `fetch` reuses a working tree the
  previous job left behind.
- Keep the runner user out of powerful host groups. Membership in `docker`,
  `libvirt` or `vboxusers` is equivalent to root on that host — which is exactly
  what the host-daemon build path in `container-build-strategies.md` requires, and
  why that path carries four preconditions.
- Restrict deploy credentials to protected variables, and the jobs that use them
  to protected refs.

## Kubernetes executor operating model

The executor creates one pod per job. The pod contains a **build** container, a
**helper** container that clones the repository and uploads artifacts, and, on
clusters that need it, an **init-permissions** container. Service containers join
the same pod.

Three consequences that change designs:

- Everything the job writes outside a configured cache or artifact path is gone
  when the pod is.
- All the containers in the pod pull images. A registry credential that reaches
  only one of them fails the pod, not the job's script.
- Pod startup time is part of every job's duration. On a slow cluster it can
  exceed a fast job's runtime, which is an argument for fewer, larger jobs rather
  than a wide graph of small ones.

## Helm values versus embedded TOML

The GitLab Runner Helm chart is the standard deployment. `values.yaml` is YAML;
the `runners.config` value inside it is **embedded TOML**. Writing YAML syntax
inside `runners.config` produces a chart that installs and a runner that ignores
the block. `validate_runner_config.py` parses the embedded block and reports
`embedded-toml` when it is not valid TOML.

Use `assets/templates/values-k8s-runner.yaml` as the baseline. The Helm chart
itself — templating, releases, upgrade strategy — is `/alaa-k8s-helm`
(`$alaa-k8s-helm`)'s subject; this file covers only the runner's own values.

Register with a runner **authentication token** (prefix `glrt-`), through
`runnerToken` or `runnerTokenSecret`. Registration tokens are the legacy workflow
and instance administrators have been able to disable them since GitLab 17.0.

## `concurrent` and per-runner limits

`concurrent` is process-wide: the total number of jobs this runner process runs at
once, across every `[[runners]]` entry. `limit` inside a `[[runners]]` entry caps
one entry's share of that total.

Derive the number, do not copy it. Take the host's CPU count divided by the cores
the heaviest job needs; take the host's memory divided by the heaviest job's peak
resident size; use the lower of the two, and leave one slot's worth of headroom
for the runner process itself. On a Kubernetes executor the ceiling is the
cluster's schedulable capacity for the runner's namespace, not the manager pod's.

State the derivation in the answer. A `concurrent` value with no stated basis is
a number that nobody can safely change later.
`validate_runner_config.py` reports `concurrent-unset` and `concurrent-zero`.

Concurrency also interacts with cache: two jobs running at once under the same
cache key race on the archive. Give concurrently-running jobs distinct keys, or
give the readers `policy: pull`.

## Image pull secrets and the helper image

```toml
[runners.kubernetes]
  image = "registry.example.com:5000/ci/toolchain:1.8.3"
  helper_image = "registry.example.com:5000/mirror/gitlab-runner-helper:x86_64-v19.1.2"
  image_pull_secrets = ["registry-pull"]
```

- **`image_pull_secrets`** is an array of `docker-registry` secret names in the
  runner's namespace. Every container in the job pod — build, helper and
  init-permissions — pulls, so all of them need it. The manager pod's own pull
  configuration does **not** apply to job pods: they are separate pods created by
  the executor. A design that authenticates the manager and forgets the job pods
  fails at pod creation with an image-pull error and no job log.
  `validate_runner_config.py` reports `kube-image-pull-secrets`.
- **`helper_image`** overrides the helper container's image. Left unset, it is
  pulled from GitLab's own registry at job time, which fails in a cluster with
  restricted egress. Mirror it into the registry the cluster can reach and pin the
  mirrored reference. The tag carries the architecture and the runner version
  (`x86_64-v19.1.2`); keep it in step with the runner's own version, and re-derive
  the current tag from the helper image's tag list rather than from memory.
- **`helper_image_flavor`** selects the helper's base (`alpine`, a specific
  `alpineN.NN`, or `ubuntu`). Pin a specific Alpine flavour rather than
  `alpine-latest` for the same reason any other tag is pinned.
- **`allowed_images` and `allowed_services`** are wildcard allowlists. Unset means
  `*/*:*` — every image. An entry that wildcards a whole registry or a whole
  namespace (`docker.io/library/*:*`) is an allowlist in form only; list the
  repositories the runner actually serves. `validate_runner_config.py` reports
  `kube-allowlist-too-broad`.
- **`allowed_pull_policies` and `pull_policy`.** `pull_policy` is the runner's
  own default; `allowed_pull_policies` is what a pipeline may request. A
  `pull_policy` outside the allowlist makes every job fail at pod creation —
  `validate_runner_config.py` reports `kube-pull-policy-conflict`. Prefer
  `always` on any runner more than one project can reach: with `if-not-present`, a
  layer already cached on the node under a reused tag is served to the next
  project.

## Distributed cache

Add a `[runners.cache]` block with a `Type` and its credentials on any
Kubernetes-executor runner whose pipelines use `cache:`. Without it the cache is
written to a pod that then disappears, so every cache key in every pipeline on
that runner is a no-op that still costs upload time.

```toml
[runners.cache]
  Type = "s3"
  Shared = false
  [runners.cache.s3]
    ServerAddress = "REPLACE_WITH_OBJECT_STORE_ENDPOINT"
    BucketName = "gitlab-runner-cache"
    BucketLocation = "REPLACE_WITH_REGION"
    AuthenticationType = "access-key"
```

`Shared = true` puts every project's cache in one bucket path, which is a
cross-project read path; leave it false unless a single trusted tenant uses the
runner. Bucket naming, lifecycle rules and credential rotation for the store
belong to `/alaa-minio-object-storage` (`$alaa-minio-object-storage`) or
`/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`).

`validate_runner_config.py` reports `kube-cache-not-distributed`.

## RBAC and namespace design

Decide namespace behaviour before writing anything else.

**Fixed namespace** — one namespace for every job pod. Simpler RBAC, no
cluster-scoped rights, namespace count stays constant. Correct when the runner
serves a small set of trusted projects.

**Namespace per job** (`namespace_per_job = true`) — stronger isolation, and it
requires cluster-scoped create and delete rights on namespaces. Confirm the
service account has them before shipping, and say so in the answer, because the
failure mode is every job failing at pod creation.

Give the runner a dedicated namespace and a dedicated, named service account.
Where `rbac.create` is false, name `serviceAccount.name` explicitly; otherwise the
chart falls back to the namespace default account, whose rights nobody declared.

Do not assume a runner job may create or read namespaces, or run
`helm --create-namespace`, unless live evidence shows the service account has that
scope. When a job hits an RBAC denial, check whether the namespace identity the
job used matches the one the role binding names before broadening any privilege.
What a specific managed platform permits is that platform's skill to state; for
Arvan-managed Kubernetes that is `/caas-arvan-kuber` (`$caas-arvan-kuber`).

## Restricted and read-only clusters

Where the cluster enforces a restricted or read-only container filesystem:

- Set `logs_base_dir` and `scripts_base_dir` to a writable path (`/tmp` with an
  `emptyDir`, typically).
- Check that `HOME`, the temp directory and any credential file path the job
  writes are writable.
- Do not assume root, and do not assume privileged mode is available.
- Where a privileged runner is unavoidable, put it on its own fleet with its own
  node selector and keep untrusted projects off it. `validate_runner_config.py`
  reports `kube-privileged` and `kube-privileged-node-selector`.
