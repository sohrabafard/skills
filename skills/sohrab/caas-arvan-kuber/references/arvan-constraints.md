# Arvan CaaS constraints and portability checklist

Use this file as a fast ruleset. For API and RBAC details, also read:

- `references/openapi-1.25-capability-matrix.md`
- `references/arvan-rbac-namespace-facts.md`

## Hard constraints (apply by default)

1) Resources per container are mandatory.
- Set both `requests` and `limits`.
- On Arvan targets, default to `requests == limits`.
- CPU values must use decimal cores (for example `0.2`) instead of millicores (`200m`).
- Memory must default to `2x` CPU and use integer `Mi` or whole `Gi` (for example `0.2 -> 400Mi`, `0.5 -> 1Gi`, `2 -> 4Gi`).
- Include `ephemeral-storage` when platform policy or LimitRange requires it.

2) Secret handling must be strict.
- Keep secrets in Kubernetes Secrets or `values.secret.yaml` only.
- Never put secrets in `values.yaml`, `--set`, shell history, or CI logs.
- Support both modes:
  - chart creates secret from secret values,
  - chart references existing secret without overwrite.

3) Stateful scaling safety.
- HPA default only for stateless workloads.
- Stateful/PVC-backed workloads: no default HPA; expose manual replica/instance knobs with runbook steps.

4) Namespace-scoped RBAC first.
- Prefer `Role` + `RoleBinding`.
- Avoid cluster-scoped objects unless explicitly approved.
- In CI and runner-driven deploy flows, assume the target namespace already exists and avoid cluster-scoped namespace creation or namespace introspection.

5) Config mount path safety.
- Do not mount on busy app directories.
- Use dedicated mount subpaths (for example `/etc/<app>/config`).

## OpenAPI 1.25 constraints (high impact)

From `./arvann-caas-openAPI-1.25.json`:

- Documented paths are namespace scoped.
- Supported high-level APIs include Deployments, StatefulSets, Jobs, CronJobs, Ingress, HPA, Roles/RoleBindings.
- Collection get-only resources include `limitranges` and `resourcequotas`.

Treat these as unsupported unless live discovery proves otherwise:

- `DaemonSet`, `NetworkPolicy`, `PodDisruptionBudget`
- `StorageClass`, `ClusterRole`, `ClusterRoleBinding`, `CRD`
- OpenShift APIs (`Route`, `BuildConfig`)

## Arvan operational behavior to remember

1) Multi-document YAML (`---`) is supported in panel workflows.
2) If resources are omitted, platform defaults may be applied (for example 1 CPU / 2 GiB class defaults in docs).
3) CPU generation selection may require node affinity labels (for example `cloud-container-g2`/`g3` families).
4) Horizontal scaling in panel is stateless-oriented and can be restricted when persistent storage is enabled.
5) Custom domain flows depend on Arvan CDN-managed DNS and active CDN state.
6) `ClusterIP` is only for in-cluster access. For external HTTP/HTTPS apps, use an `Ingress` or Arvan's panel-managed domain/public-IP flow on top of the service.
7) If Arvan terminates TLS at the edge, keep in-cluster ingress/service traffic on HTTP and disable chart-managed TLS unless a real in-cluster certificate flow is required.
8) Persistent disk behavior:
- container filesystem is ephemeral,
- disk size increases only (no shrink),
- detach/delete operations are disruptive and should be runbooked.

## RBAC identity caution (alias vs canonical namespaces)

Use facts from `references/arvan-rbac-namespace-facts.md` when RBAC symptoms are inconsistent:

1) Explicitly state both namespace forms when visible:
- alias namespace (`vk` style),
- canonical/hash-prefixed namespace identity.
2) RBAC evaluation depends on exact principal identity: `system:serviceaccount:<namespace>:<name>`.
3) A successful Helm install does not prove runtime SA authorization is correct.
4) `kubectl auth can-i --as=...` denial can reflect missing impersonation rights for the caller, not only target SA permissions.
5) Treat alias/canonical mismatch as a first-class hypothesis before changing RoleBindings.

## Portability toggles (recommended)

- `openshift.enabled`
- `route.enabled` vs `ingress.enabled`
- `hpa.enabled` (default false for stateful workloads)
- `affinityPreset.cpuGeneration` (off by default)
- `privateRegistry.create` vs `privateRegistry.existingSecretName`

## Runner/CI reliability map

1) Pull/auth failures in GitLab Runner usually come from executor job pod pull-secret config.
2) Render failures are commonly chart path/dependency mistakes.
3) RBAC denies can come from namespace identity mismatch (alias vs canonical namespace forms).
4) Admission denials are often fixed by explicit resources and parity (`requests == limits`).
5) Deterministic render gates (`helm lint` + `helm template`) should run before each deploy.
