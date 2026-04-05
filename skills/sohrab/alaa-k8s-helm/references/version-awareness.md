# Version Awareness

## Why this file exists

This skill is expected to stay useful across changing Helm, Kubernetes, and OpenShift releases. Use this file whenever version skew, “latest” behavior, or feature availability could affect the answer.

## Current review baseline

This pack was reviewed against official docs current on 2026-04-05.

### Helm snapshot

- Helm 4 is the current major line.
- Helm docs are currently published as `4.1.1`.
- Helm 4.1.x is documented as compatible with Kubernetes 1.35 through 1.32.
- Helm 4.0.x is documented as compatible with Kubernetes 1.34 through 1.31.
- Helm 4 introduces notable changes such as Wasm-based plugins, OCI digest support, multi-document values, JSON arguments, and post-renderers implemented as plugins.

### Kubernetes snapshot

- Kubernetes docs currently track `v1.35` as the latest documentation version.
- Supported release branches are currently 1.35, 1.34, and 1.33.
- Kubernetes 1.36 is in pre-release or sneak-peek state as of this review, so do not default to 1.36-only assumptions.
- `VolumeAttributesClass` is stable in 1.34 and is useful for storage tuning when the CSI driver supports it.

### OpenShift snapshot

- OpenShift Container Platform 4.21 is current in Red Hat docs and uses Kubernetes 1.34.
- OpenShift continues to use SCCs and also includes Kubernetes Pod Security Admission.
- Route remains the platform-native external HTTP or HTTPS exposure object.

## Authoring defaults for this pack

Use these defaults unless the user’s environment says otherwise.

- Target stable Kubernetes APIs that work on 1.33–1.35.
- Prefer Helm charts that stay compatible with Helm 3.20+ and Helm 4 unless the user explicitly wants Helm 4-only features.
- Treat OpenShift 4.19–4.21 as the supported OpenShift band for portable OpenShift guidance.
- Prefer stable over alpha features.

## Feature gating rules

### Safe to use by default when available

- Chart API `v2`
- `values.schema.json`
- OCI chart distribution
- `kubectl debug` for ephemeral container workflows
- Gateway API only when the cluster clearly supports it
- `VolumeAttributesClass` only when the CSI driver and cluster support it

### Do not default to these without confirmation

- Helm 4-only workflow assumptions in mixed Helm 3 estates
- pre-release Kubernetes 1.36 features
- alpha autoscaling behavior such as configurable HPA tolerance unless the user explicitly opts in
- cluster-specific Gateway filters or experimental extensions

## Check sequence before version-sensitive advice

Run the smallest set that answers the compatibility question.

```bash
helm version
kubectl version --output=yaml
oc version
kubectl api-versions | rg 'gateway.networking.k8s.io|route.openshift.io|security.openshift.io'
```

## If freshness matters beyond this review

Re-check official vendor docs instead of trusting this snapshot. This is especially important when the user asks for:

- the latest release line
- a newly announced feature
- exact compatibility guarantees
- a breaking-change assessment for an upgrade
