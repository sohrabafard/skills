# Container build strategies

## Table of contents

- Choose the build path
- BuildKit rootless
- Docker-in-Docker
- Podman and Buildah
- Registry auth and cache
- Strategy checklist

## Choose the build path

Use this order of preference:

1. BuildKit rootless.
2. Podman or Buildah when policy or platform fit is better.
3. Docker-in-Docker only when daemon behavior is truly required.

Do not propose Kaniko for new GitLab CI/CD designs.

## BuildKit rootless

Use BuildKit rootless when:

- The job only needs to build and push OCI images.
- You want to avoid privileged runners.
- The platform is Kubernetes or another restricted environment.

Strengths:

- No Docker daemon requirement.
- Good cache support.
- Good fit for registry-based cache.
- Cleaner security story than DinD.

Baseline template:

- `assets/templates/k8s-buildkit-rootless.gitlab-ci.yml`

Key notes:

- Write a Docker config file at runtime for registry auth.
- Use registry cache import and export deliberately.
- Keep the Dockerfile and context explicit.

## Docker-in-Docker

Use DinD only when the job really needs Docker daemon behavior, such as:

- Docker CLI workflows that expect a daemon.
- Daemon-specific integration tests.
- Existing tooling that cannot be moved to BuildKit, Podman, or Buildah in the current task.

DinD requirements:

- A privileged runner.
- Strong runner isolation.
- Clear TLS or non-TLS configuration.
- Dedicated nodes or runner fleet for the riskier workloads.

Preferred baseline:

- `assets/templates/k8s-dind-tls.gitlab-ci.yml`

Design rules:

- Prefer TLS-enabled DinD.
- Keep the service alias and port aligned with the job variables.
- Use `docker build --pull` for fresher base images where appropriate.
- Separate the risky path from the safe path in the final answer.

Avoid `docker.sock` host mounts unless the user explicitly needs them and understands the host-breakout risk.

## Podman and Buildah

Use these when a daemonless OCI build path fits better than Docker:

- Podman is attractive when the environment already supports it cleanly.
- Buildah is often a good fit for OpenShift or more locked-down container platforms.

Use them when:

- The platform forbids privileged DinD.
- You still need container image builds.
- The team is comfortable with OCI-native tools instead of Docker daemon semantics.

When suggesting Podman or Buildah, mention the platform assumptions explicitly because support details vary by cluster policy, SELinux, and required devices.

## Registry auth and cache

Use these defaults across strategies:

- Authenticate with `CI_REGISTRY_USER` and `CI_REGISTRY_PASSWORD` or another approved short-lived auth path.
- Prefer registry-backed cache when runners are ephemeral.
- Avoid assuming local layer cache survives on Kubernetes executors.
- Keep cache image names separate from release image names.

Example cache naming pattern:

- Release image: `$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA`
- Branch cache image: `$CI_REGISTRY_IMAGE:buildcache-$CI_COMMIT_REF_SLUG`

## Strategy checklist

Before finalizing a build design, answer these questions:

- Does the job truly need a Docker daemon?
- Is the runner privileged or unprivileged?
- Is the runner dedicated or shared?
- Is the cache local, registry-backed, or intentionally disabled?
- Are registry auth and secret paths explicit?
- Is the chosen strategy easy to explain and operate later?
