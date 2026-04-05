# Alaa K8s + Helm Topic Map

## Use this file first

Open this file before reading any other reference. It tells you the smallest set of files to load for the current task.

## Task routing

### Create a Helm chart from scratch
Read:
- `references/authoring-workflows.md`
- `references/kubernetes-resource-patterns.md`
- `references/version-awareness.md`

Also read `references/openshift-and-managed-platforms.md` if the chart must work on OpenShift or Arvan Cloud Container.

### Convert existing YAML to Helm
Read:
- `references/authoring-workflows.md`
- `references/kubernetes-resource-patterns.md`
- `references/validation-workflows.md`

Also read `references/openshift-and-managed-platforms.md` if the source contains `Route`, SCC-related settings, or arbitrary-UID constraints.

### Explain or review an existing chart
Read:
- `references/authoring-workflows.md`
- `references/validation-workflows.md`
- `references/version-awareness.md`

### Validate raw Kubernetes YAML
Read:
- `references/validation-workflows.md`
- `references/kubernetes-resource-patterns.md`

Also read `references/openshift-and-managed-platforms.md` if the YAML contains OpenShift resources or targets a managed namespace platform.

### Validate a Helm chart or upgrade path
Read:
- `references/validation-workflows.md`
- `references/version-awareness.md`
- `references/kubernetes-resource-patterns.md`

### Debug a failing pod, service, ingress, route, or rollout
Read:
- `references/runtime-debug-playbooks.md`
- `references/networking-observability-and-tuning.md`

Also read `references/openshift-and-managed-platforms.md` if SCC, Routes, `oc`, or managed-platform restrictions might matter.

### Decide between Service, Ingress, Gateway API, Route, PDB, or PVC
Read:
- `references/kubernetes-resource-patterns.md`
- `references/openshift-and-managed-platforms.md` when external exposure is OpenShift-specific

### Answer OpenShift vs Kubernetes questions
Read:
- `references/openshift-and-managed-platforms.md`
- `references/version-awareness.md`

### Answer Arvan Cloud Container questions
Read:
- `references/openshift-and-managed-platforms.md`
- `references/version-awareness.md`

### Networking, observability, or tuning question
Read:
- `references/networking-observability-and-tuning.md`
- `references/runtime-debug-playbooks.md` if there is an active incident

## Working rule

Read only what the task needs. The default order is:

1. topic map
2. one primary workflow file
3. one platform or object-pattern file if needed
4. version-awareness only when compatibility matters

## Script map

- `scripts/check_tools.sh`: inventory required and optional tools by lane
- `scripts/validate_chart_structure.sh`: fast chart structure audit
- `scripts/detect_crd_wrapper.sh`: detect CRDs and OpenShift resources in YAML
- `scripts/cluster_health.sh`: broad cluster snapshot for triage
- `scripts/pod_diagnostics.py`: deep pod-focused evidence collection
- `scripts/network_debug.sh`: pod-to-service and DNS/network debugging helper
