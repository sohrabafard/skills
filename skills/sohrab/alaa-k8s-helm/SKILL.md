---
name: alaa-k8s-helm
description: Unified Kubernetes, Helm, OpenShift, and kubectl/oc skill for generating, refactoring, validating, explaining, upgrading, and debugging Helm charts, Kubernetes manifests, and OpenShift workloads. Use it when the task involves Helm 3 or 4, Kubernetes YAML, kubectl or oc commands, Routes, SCCs, CRDs, rollout safety, service exposure, storage, networking, or managed namespace platforms such as Arvan Cloud Container. Do not use it for generic Docker-only, Terraform-only, CI-only, or cloud work that does not materially depend on Kubernetes, OpenShift, or Helm.
---

# Alaa K8s + Helm

Use this as the single entrypoint for Helm, Kubernetes YAML, OpenShift, and day-2 troubleshooting work. The skill is designed to replace separate generator, validator, and debugger skills while keeping context usage low through routing-first instructions.

## Start here

1. Read `references/00-topic-map.md`.
2. Detect the task lane before reading anything else:
   - authoring or refactoring
   - validation or release readiness
   - runtime debugging
   - OpenShift or managed-platform fit
   - networking, observability, or tuning
3. Open only the reference files that match the lane.
4. Establish two facts early:
   - the **version surface** (`helm version`, `kubectl version`, `oc version`, API availability)
   - the **access surface** (cluster-admin, namespace admin, developer, or container-only access)

## Default operating model

- **Version-aware first**: Read `references/version-awareness.md` whenever compatibility or “latest” behavior matters.
- **Access-aware first**: Never assume cluster-admin. Confirm what the user can actually do before recommending cluster-scoped objects or node-level actions.
- **Stable by default**: Prefer stable APIs and portable patterns that work across Kubernetes 1.33–1.35 and OpenShift 4.19–4.21 unless the user explicitly asks for newer or platform-specific behavior.
- **Namespace-safe by default**: Generate namespaced resources unless cluster-scoped resources are truly required.
- **Evidence before edits**: For debugging, gather events, logs, status, and access errors before suggesting fixes.
- **OpenShift-safe by default**: When the target might be OpenShift or an OpenShift-like managed platform, assume arbitrary UID, non-root execution, stricter admission, and no node access until proven otherwise.
- **Report-only when asked to audit**: If the user asked to validate, lint, review, or audit, default to report-only. If they asked to fix, generate, refactor, or patch, make the change and rerun checks.

## Task lanes

### Authoring or refactoring

Read:
- `references/authoring-workflows.md`
- `references/kubernetes-resource-patterns.md`
- `references/openshift-and-managed-platforms.md` when Routes, SCCs, arbitrary UID, or managed PaaS constraints matter

Use this lane for:
- creating charts from scratch
- converting raw YAML to Helm
- writing raw manifests
- explaining or restructuring existing charts
- preparing reusable values models and schemas

### Validation or release readiness

Read:
- `references/validation-workflows.md`
- `references/version-awareness.md`
- `references/openshift-and-managed-platforms.md` when the rendered output contains OpenShift or platform-specific objects

Use this lane for:
- linting and schema checks
- rendered-manifest validation
- dry-run checks
- permission and rollout-risk review
- upgrade safety review

Useful scripts:
- `scripts/check_tools.sh`
- `scripts/validate_chart_structure.sh`
- `scripts/detect_crd_wrapper.sh`

Useful assets:
- `assets/.yamllint`
- `assets/.helmignore`
- `assets/values-schema-template.json`

### Runtime debugging

Read:
- `references/runtime-debug-playbooks.md`
- `references/networking-observability-and-tuning.md`
- `references/openshift-and-managed-platforms.md` when SCC, Routes, or managed platform constraints may be the cause

Use this lane for:
- failing pods
- crash loops
- image pull failures
- readiness or liveness failures
- service, ingress, route, gateway, or DNS issues
- PVC, storage, and permission problems
- rollout and disruption issues

Useful scripts:
- `scripts/cluster_health.sh`
- `scripts/pod_diagnostics.py`
- `scripts/network_debug.sh`

### OpenShift or managed-platform fit

Read:
- `references/openshift-and-managed-platforms.md`
- `references/version-awareness.md`

Use this lane when the question is really about:
- OpenShift vs vanilla Kubernetes behavior
- SCC, PSA, Routes, ImageStreams, BuildConfigs, or `oc`
- cluster access vs namespace access vs container-only access
- Arvan Cloud Container or similar managed namespace/container platforms

### Networking, observability, or tuning

Read:
- `references/networking-observability-and-tuning.md`
- `references/kubernetes-resource-patterns.md`
- `references/runtime-debug-playbooks.md` if the user already has an incident

Use this lane for:
- service-path tracing
- DNS and egress issues
- MTU, connection tracking, and latency triage
- metrics, logs, traces, and alert design
- node-level or runtime tuning questions

## Access decision rules

Treat access as one of four surfaces and tailor both commands and YAML accordingly.

- **Cluster-admin**: cluster-scoped objects, CRDs, SCC creation or grants, StorageClasses, IngressClasses, GatewayClasses, namespaces, nodes, MachineConfig, and cluster operators are on the table.
- **Namespace or project admin**: namespaced workloads, Services, Ingress, Routes, PVCs, ServiceAccounts, RoleBindings, HPAs, PDBs, and most day-2 changes are usually possible.
- **Developer**: read operations, logs, exec, rollout status, and some namespaced patches may work, but RBAC and policy objects often will not.
- **Container-only access**: focus on process, filesystem, env, application logs, and exposed endpoints. Do not assume Kubernetes API access.

Always verify uncertain permissions with `kubectl auth can-i` or `oc auth can-i` before giving an authoritative deployment path.

## Guardrails

- Prefer `helm template`, `helm lint`, `kubectl apply --dry-run=server`, `oc apply --dry-run=server`, and `kubectl diff` before live changes.
- Keep selectors stable. Do not silently change immutable selectors or StatefulSet storage identity.
- Avoid OpenShift-hostile defaults such as fixed non-portable UIDs, `privileged: true`, `hostPath`, `hostNetwork`, or binding directly to ports below 1024 unless the user explicitly controls the policy surface.
- Prefer Services plus Ingress, Gateway API, or Routes over direct Pod exposure.
- Use Pods directly only for one-off debug or batch cases. Long-running apps belong behind controllers.
- Prefer OCI registries for chart distribution unless the user is locked into classic chart repositories.

## Subagent strategy

When the environment supports multi-agent workflows, use them only when the task is broad enough to benefit.

- **Inventory agent**: inspect existing charts, manifests, CRDs, and platform signals.
- **Validator agent**: run static checks, render charts, and summarize blocking failures.
- **Platform-fit agent**: map the target to vanilla Kubernetes, OpenShift, or a managed namespace platform and flag access constraints.
- **Runtime agent**: analyze logs, events, routing, and storage evidence for incidents.

If multi-agent support is unavailable, do the same work sequentially with the same lane separation.

## Deliverable rules

- For generation tasks, return ready-to-apply YAML or chart files plus the exact validation commands you used or recommend.
- For validation tasks, separate **blocking errors**, **deployment risks**, and **best-practice gaps**.
- For debugging tasks, end with the most likely root cause, the evidence that supports it, the next command to confirm it, and the lowest-risk fix.
- When the platform is uncertain, state the assumption briefly and prefer the safer, more restrictive path.
