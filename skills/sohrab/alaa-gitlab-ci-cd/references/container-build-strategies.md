# Container build strategies

How an image build is expressed as a job on a runner. What goes *into* the image
— base image choice, layer order, multi-stage boundaries, minimisation, and any
Compose file — belongs to `/alaa-docker-production` (`$alaa-docker-production`).

## Table of contents

- Choose the build path
- Rootless BuildKit
- Shell runner against a host daemon
- Docker-in-Docker
- Podman and Buildah
- Kaniko
- Why this order differs from GitLab's own
- Registry authentication and build cache
- Strategy checklist

## Choose the build path

Answer these before writing YAML: does the job need Docker *daemon* behaviour, or
only an OCI image build? Is the runner privileged? Is the host dedicated or
shared? Is the cache registry-backed, local, or deliberately absent?

Then pick, in this order:

1. **Rootless BuildKit** on a Kubernetes runner. No privileged container, no
   daemon.
2. **Podman or Buildah** where the platform or policy fits them better.
3. **Shell runner against a host Docker daemon**, when the four preconditions
   below all hold.
4. **Docker-in-Docker**, when the job genuinely needs daemon behaviour and a
   privileged runner exists for it.

## Rootless BuildKit

Use when the job only builds and pushes an OCI image, the platform is Kubernetes
or another restricted environment, and there is no requirement for daemon
semantics. Baseline:
`assets/templates/k8s-buildkit-rootless.gitlab-ci.yml`.

Notes that decide whether it works:

- The image has an entrypoint; set `entrypoint: [""]` or the job script never
  runs.
- `BUILDKITD_FLAGS: --oci-worker-no-process-sandbox` is what makes it work without
  privileges.
- Registry authentication is a `~/.docker/config.json` written at job start.
  Write it under `umask 077` and remove it in `after_script`, so the same block is
  still correct if it is copied onto a shell runner where the workspace persists.

## Shell runner against a host daemon

This is the path a fleet takes when the build host already runs a daemon and
BuildKit-in-Kubernetes is not available. It is the least isolated path here: the
job runs as the runner user, and that user is in the `docker` group, which is
equivalent to root on the host.

Use it only when **all four** hold, and state them in the answer:

1. The host serves no other tenant's jobs.
2. The runner is tagged and only the intended projects carry that tag.
3. The jobs that use it run on protected refs only.
4. The daemon is not exposed on a network socket.

If any one fails, use rootless BuildKit instead. Baseline:
`assets/templates/shell-runner-host-daemon.gitlab-ci.yml`.

Three things this path gets wrong most often:

- **The build directory persists.** Registry credentials written to
  `~/.docker/config.json` outlive the job. Log out in `after_script`.
- **`BUILDKIT_INLINE_CACHE=1` with no `--cache-from` writes a cache nothing
  reads.** Every build is cold and the setting looks like it is working. Pair it
  with `--cache-from type=registry,ref=...`, or drop it.
- **Two pipelines pushing the same tag race.** Give the job a `resource_group`
  named after the registry repository it writes.

Where the job needs to know whether a tag already exists before pushing — the
idempotency check that makes a re-run safe — express that as a script step whose
failure fails the job, not as a `|| true`.

## Docker-in-Docker

Use only when the job needs daemon behaviour: a Docker CLI workflow that expects a
daemon, a daemon-specific integration test, or tooling that cannot move to
BuildKit or Podman inside this task.

DinD requires a privileged runner. That is not a preference: without
`privileged = true` the service container cannot start. Therefore:

- Use a **dedicated** privileged runner fleet with its own node selector.
- Restrict it to protected refs and trusted projects.
- Prefer TLS (port 2376, `DOCKER_TLS_CERTDIR`, `DOCKER_CERT_PATH`) and keep the
  service alias, the port and the certificate directory consistent with each
  other, or the CLI reports only "Cannot connect to the Docker daemon".

If a platform constraint makes any of these impossible, the choice is between not
using DinD and getting an explicit exception from `/alaa-security-review`
(`$alaa-security-review`), which owns that decision. Do not ship the
unhardened form on request alone.

Do not mount the host `docker.sock` into a container. It gives the job the
daemon's full authority on the host with none of the shell-runner path's stated
preconditions.

Baseline: `assets/templates/k8s-dind-tls.gitlab-ci.yml`.

## Podman and Buildah

Daemonless OCI builds. Podman fits where the environment already supports it;
Buildah fits OpenShift and other locked-down container platforms. Use them when
the platform forbids privileged DinD and image builds are still required. State
the platform assumptions explicitly, because support depends on cluster policy,
SELinux labelling and which devices the pod may open.

## Kaniko

Do not use Kaniko. GitLab's own documentation states that kaniko is no longer a
maintained project and directs users to Docker, Buildah or Podman. If an existing
pipeline uses it, say that the tool is unmaintained and give the replacement
rather than repairing the Kaniko job.

## Why this order differs from GitLab's own

GitLab's `using_docker_build` page documents shell executor, then
Docker-in-Docker — which it calls "the recommended approach when your runner
supports privileged mode" — then socket binding, then Windows pipe binding, and
lists BuildKit and Buildah under alternatives for when privileged mode is
unavailable.

This skill inverts that and puts rootless BuildKit first. The reason is the
threat model, not a disagreement about mechanics: on a fleet where a single
compromised build container must not be able to reach the node, "a privileged
runner is available" is not a reason to use one. State this divergence when an
answer recommends BuildKit over DinD, so the next reader does not "correct" it
back to the vendor's order without knowing why it was inverted.

## Registry authentication and build cache

- Authenticate with `CI_REGISTRY_USER` and `CI_REGISTRY_PASSWORD`, or with a
  short-lived credential from `id_tokens:`. Pipe the password through
  `--password-stdin` so it never reaches the process table or the job log.
- Keep cache image names separate from release image names, so a cache push can
  never be mistaken for a release:
  - release: `$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA`
  - branch cache: `$CI_REGISTRY_IMAGE:buildcache-$CI_COMMIT_REF_SLUG`
- Import and export the cache deliberately. A cache that is exported and never
  imported is pure cost.
- Do not assume a local layer cache survives on a Kubernetes executor. It does
  not; see `cache-artifacts-and-pinning.md`.

## Strategy checklist

- Does the job truly need a Docker daemon, or only an image build?
- Is the runner privileged, and if so is it dedicated and node-isolated?
- Is the host shared with another tenant?
- Is the cache registry-backed, local, or deliberately absent — and is it
  imported as well as exported?
- Are registry credentials written with `--password-stdin`, and removed when the
  job ends?
- Is the release tag distinct from the cache tag?
- Would another engineer be able to state this design's isolation boundary after
  one read?
