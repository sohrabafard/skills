# Alaa K8s + Helm Topic Map

## Use this file first

This is the only router in the skill. Open it before any other reference. It maps a task phrasing to the smallest set of files to load, and it lists every script.

## Task routing

### Create a Helm chart from scratch
Read:
- `references/authoring-workflows.md`
- `references/kubernetes-resource-patterns.md`
- `references/version-awareness.md`

Also read `references/openshift-and-managed-platforms.md` when the chart must work on OpenShift or on a managed namespace platform.
Also read `references/failure-and-load.md` when the workload has more than one replica, holds state, or serves traffic during a rollout.

### Convert existing YAML to Helm
Read:
- `references/authoring-workflows.md`
- `references/kubernetes-resource-patterns.md`
- `references/validation-workflows.md`

Also read `references/openshift-and-managed-platforms.md` when the source contains `Route`, SCC-related settings, or arbitrary-UID constraints.

### Explain or review an existing chart
Read:
- `references/authoring-workflows.md`
- `references/validation-workflows.md`
- `references/version-awareness.md`

### Validate raw Kubernetes YAML
Read:
- `references/validation-workflows.md`
- `references/kubernetes-resource-patterns.md`

Also read `references/openshift-and-managed-platforms.md` when the YAML contains OpenShift resources or targets a managed namespace platform.

### Validate a Helm chart or an upgrade path
Read:
- `references/validation-workflows.md`
- `references/version-awareness.md`
- `references/kubernetes-resource-patterns.md`

Also read `references/failure-and-load.md` when the upgrade changes replica count, rollout strategy, probes, or `terminationGracePeriodSeconds`.

### Debug a failing pod, service, ingress, route, or rollout
Read:
- `references/runtime-debug-playbooks.md`
- `references/networking-observability-and-tuning.md`

Also read `references/openshift-and-managed-platforms.md` when SCC, Routes, `oc`, or managed-platform restrictions might matter.
Also read `references/failure-and-load.md` when the rollout is stuck, the incident began during a deploy, or requests fail only while pods are terminating.

### Decide between Service, Ingress, Gateway API, Route, PDB, or PVC
Read:
- `references/kubernetes-resource-patterns.md`
- `references/openshift-and-managed-platforms.md` when the exposure is OpenShift-specific
- `references/failure-and-load.md` for the PDB value itself

### Answer OpenShift versus Kubernetes questions
Read:
- `references/openshift-and-managed-platforms.md`
- `references/version-awareness.md`

### Answer Arvan Cloud Container questions
This skill does not own Arvan CaaS platform facts. Load `/caas-arvan-kuber` (`$caas-arvan-kuber`) only when the answer depends on a fact that is true of Arvan CaaS and false of stock Kubernetes at the same minor version; otherwise stay in `/alaa-k8s-helm` (`$alaa-k8s-helm`) and use the generic managed-namespace-platform posture in `references/openshift-and-managed-platforms.md`.

### Networking, observability, or tuning question
Read:
- `references/networking-observability-and-tuning.md`
- `references/runtime-debug-playbooks.md` when there is an active incident

### Set a probe threshold, a PDB value, `maxSurge`, `maxUnavailable`, or a grace period
Read:
- `references/failure-and-load.md`

### Check whether a version claim in this skill is still true
Read:
- `references/version-awareness.md` for the rules and the current pinned values
- `references/SOURCES.md` for which official URL answers which question and the conflict-resolution order

Run `python3 scripts/check_versions.py` to compare the pinned values against the vendors' own pages.

## Working rule

Read only what the task needs. The default order is:

1. this topic map
2. one primary workflow file
3. one platform or object-pattern file when the target is not vanilla Kubernetes
4. `references/version-awareness.md` only when compatibility matters

## Script map

Every script accepts `--help` and `--self-test`, and every script uses the same exit codes: `0` clean, `1` findings, `2` could not run.

- `scripts/check_manifests.py`: gate a rendered manifest set on resources, probes, security context, host-level fields, port mapping, and, with `--baseline`, selector and storage-identity drift
- `scripts/check_versions.py`: compare the pinned values in `references/version-awareness.md` against the vendors' own release pages
- `scripts/check_tools.sh`: inventory required and optional tools by lane
- `scripts/validate_chart_structure.sh`: fast chart structure audit
- `scripts/detect_crd_wrapper.sh`: classify resources in YAML as Kubernetes, OpenShift, or custom
- `scripts/cluster_health.sh`: broad read-only cluster snapshot for triage
- `scripts/pod_diagnostics.py`: deep pod-focused evidence collection
- `scripts/network_debug.sh`: pod-to-service and DNS debugging helper

`scripts/detect_crd.py` is the implementation behind `detect_crd_wrapper.sh` and is not called directly.
