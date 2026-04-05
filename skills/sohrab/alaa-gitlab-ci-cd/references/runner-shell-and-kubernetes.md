# Runner shell and Kubernetes executors

## Table of contents

- Shell runner operating model
- Shell runner hardening
- Kubernetes executor operating model
- Helm and embedded TOML
- Kubernetes RBAC and namespace design
- Kubernetes executor hardening
- Read-only and restricted clusters
- Troubleshooting checklist

## Shell runner operating model

Shell runner executes jobs directly on the host as the runner service account. That is simple and fast, but the isolation boundary is weak.

Use shell runners only when all of these are true:

- The host is trusted.
- The projects are trusted.
- Host-level access is acceptable.
- You need host-native tools or extremely low overhead.

Good fits:

- Internal automation on a controlled server.
- Deployment jobs that need local host tooling.
- Build jobs that require direct host integration and are not multi-tenant.

## Shell runner hardening

Use this baseline:

- Dedicate the host to trusted workloads.
- Use explicit runner tags and pin jobs to them.
- Avoid `GIT_STRATEGY: fetch` on shared or less-trusted hosts.
- Set explicit `builds_dir` and `cache_dir` when filesystem placement matters.
- Keep the runner user out of powerful host groups unless the workflow genuinely needs them.
- Treat membership in `docker`, `libvirt`, `vboxusers`, or similar groups as privileged access.
- Keep deploy credentials protected and limit protected jobs to protected refs.

## Kubernetes executor operating model

The Kubernetes executor creates a pod per job. A typical pod contains the build container plus helper and service containers as needed.

Use the Kubernetes executor when you need:

- Stronger isolation than a shell runner.
- Elastic capacity.
- Cluster-native scheduling.
- Per-job pods and easier cleanup.

## Helm and embedded TOML

The GitLab Runner Helm chart is the standard way to run Kubernetes executor runners.

Important rule:

- `values.yaml` is YAML.
- `runners.config` inside that YAML is embedded TOML.

Do not write YAML syntax inside `runners.config`.

Use `assets/templates/values-k8s-runner.yaml` as the baseline structure.

## Kubernetes RBAC and namespace design

Decide namespace behavior first:

### Fixed namespace

Use when:

- Simpler RBAC matters more than isolation.
- The runner serves a small number of trusted workloads.
- Namespace sprawl would be a problem.

### Namespace per job

Use when:

- Stronger isolation is needed.
- The cluster and RBAC policy can create and delete namespaces safely.

When you enable namespace-per-job behavior, call out the RBAC requirement explicitly.

## Kubernetes executor hardening

Use these defaults whenever possible:

- Dedicated runner namespace.
- Dedicated service account.
- Explicit runner tags.
- `allowed_images`, `allowed_services`, and `allowed_pull_policies`.
- Dedicated node selectors for privileged runners or daemon-based builds.
- Separate privileged and unprivileged runner fleets.
- Explicit `poll_timeout` and cleanup expectations for slower clusters.

If the runner is privileged:

- Treat it as high-risk.
- Keep it off general-purpose nodes.
- Use protected projects or protected refs.
- Avoid mixing untrusted workloads onto the same runner fleet.

## Read-only and restricted clusters

Some clusters enforce read-only or restricted security contexts.

In those environments:

- Ensure writable locations for logs and scripts.
- Consider `logs_base_dir` and `scripts_base_dir`.
- Provide writable volumes or `emptyDir` mounts where required.
- Validate container `HOME`, temp paths, and credential file paths.
- Do not assume root or privileged mode is available.

## Troubleshooting checklist

### Job never starts

Check:

- Runner tags vs job tags.
- Runner paused or offline state.
- Project visibility or scope.
- Protected ref vs protected runner mismatch.

### Pod created slowly or times out

Check:

- `poll_timeout`.
- Cluster capacity.
- API server latency.
- Admission webhooks.
- Image pull time or registry access.

### Pod starts but scripts fail immediately

Check:

- Image entrypoint and shell availability.
- Writable filesystem assumptions.
- Secret mount paths.
- Service container health.
- DNS or network policy.

### DinD or daemon-based build fails on Kubernetes

Check:

- Runner privileged mode.
- Correct DinD service alias and port.
- TLS vs non-TLS variables.
- Shared cert volume or socket volume if the design requires it.
- Node isolation for privileged workloads.
