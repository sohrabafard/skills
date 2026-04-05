# Security and hardening

## Table of contents

- Threat model by runner type
- Privileged mode and daemon risk
- Secrets and identity
- Merge request and fork risk
- Pull policy and image trust
- Token and credential handling
- Security review checklist

## Threat model by runner type

### Shell runner

Highest host-exposure risk. Use only for trusted workloads on trusted hosts.

### Kubernetes executor

Better isolation by default, but the real security posture still depends on:

- Privileged mode.
- Namespace design.
- Node isolation.
- RBAC.
- Allowed images and services.

### Shared persistent runners

Higher cross-project risk than ephemeral dedicated runners. Be careful with caches, fetch strategies, private images, and any credential that reaches the job environment.

## Privileged mode and daemon risk

Treat these as high risk:

- Privileged containers.
- Docker-in-Docker.
- Host Docker socket mounts.
- Shell runner jobs with host-level container tooling.

When you cannot avoid them:

- Use a dedicated runner fleet.
- Restrict to protected refs or trusted projects.
- Isolate nodes for Kubernetes runners.
- Keep the security note visible in the final answer.

## Secrets and identity

Preferred order:

1. OIDC-style short-lived identity with `id_tokens`.
2. Supported `secrets` integrations.
3. Protected file or masked variables when there is no better native integration.

Rules:

- Never hardcode secrets.
- Never print secret values to logs.
- Avoid `set -x` around secret-handling steps.
- Use file variables for opaque credentials when tools expect files.

## Merge request and fork risk

GitLab CI changes are code changes. Review them like code.

Before enabling sensitive behavior in merge request pipelines, verify:

- Whether the pipeline runs in the source project or parent project.
- Whether protected variables or protected runners can be exposed.
- Whether the source is a fork.
- Whether the runner fleet is trusted for this path.

If the task touches fork merge requests, protected refs, or deploy credentials, mention the risk explicitly.

## Pull policy and image trust

Use pinned images whenever possible.

For shared or less-trusted runners:

- Prefer `always` for private images.
- Avoid relying on `if-not-present` unless all users and all cached content are trusted.
- Keep a clear allowlist for job images and service images on Kubernetes runners.

## Token and credential handling

- Treat `CI_JOB_TOKEN` as sensitive.
- Keep project allowlists tight.
- Avoid broad cross-project access by default.
- Prefer project or environment scoping over global access.
- When a design needs registry auth, package auth steps tightly around the build or push action.

## Security review checklist

Before finalizing, check:

- Are secrets externalized and scoped correctly?
- Is any privileged behavior isolated and justified?
- Are runner tags and trust boundaries explicit?
- Are merge request and fork behaviors safe?
- Are images pinned and allowed deliberately?
- Is the credential path short-lived where possible?
- Would another engineer understand the risk in one read-through?
