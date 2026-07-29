# Arvan CaaS capability matrix

Two columns, always. Column A is what the **pinned line** serves — the Kubernetes 1.25-era API surface described by the vendored spec. Column B is what the **current upstream stable** serves, meaning Kubernetes 1.34 through 1.36 as recorded in `/alaa-k8s-helm` (`$alaa-k8s-helm`) `references/version-awareness.md`. Where the two agree, this file says so once. Where they differ, that difference is the reason this skill exists as something separate from `/alaa-k8s-helm` (`$alaa-k8s-helm`), and it gets the detail.

**Neither column is a substitute for discovery.** Run Step 1 in `SKILL.md` first, learn which line the target is on, then read the matching column.

## Capture stamp

- **Spec capture date: unknown.** The vendored file `references/arvan-caas-openAPI-1.25.json` carries no capture date, and Arvan publishes no version. What is known is that the document describes an API server at **Kubernetes 1.25 or older**, because it serves `autoscaling/v2beta2`, which was removed upstream in 1.26.
- **Matrix last reconciled against the spec: never, mechanically.** The generated block below was seeded on 2026-07-29 from the previous hand transcription. Run `bash scripts/summarize-openapi.sh --update` once to replace it with values read from the spec, then commit. `--check` reports any later divergence.
- **Vendor cross-check: 2026-07-29.** ArvanCloud's public documentation states no Kubernetes version and no API version on the Cloud Container pages or the developer API-usage page, so nothing in this file can be confirmed against a vendor statement. See `references/SOURCES.md`.

## Generated block

Everything between the markers is produced by `bash scripts/summarize-openapi.sh --update` and compared by `--check`. Do not hand-edit it; hand edits are exactly the drift `--check` exists to catch.

<!-- BEGIN GENERATED: summarize-openapi.sh -->
- `openapi`: `3.0.3`
- `info.title`: `Arvan CaaS`
- `info.version`: `1.25`
- Paths: `134`
- Operations: `299`
- Namespaced paths: `134/134`
- Servers:
  - `https://napi.arvancloud.ir/caas/v2/zones/ir-tbz-sh1`
  - `https://napi.arvancloud.ir/caas/v2/zones/ir-thr-ba1`

| API resource | Collection | Item | Subresources |
|---|---|---|---|
| `apps/v1/controllerrevisions` | `[get]` | `[get]` | `-` |
| `apps/v1/deployments` | `[delete,get,post]` | `[delete,get,patch,put]` | `scale=[get,patch,put]; status=[get,patch,put]` |
| `apps/v1/replicasets` | `[delete,get,post]` | `[delete,get,patch,put]` | `scale=[get,patch,put]; status=[get,patch,put]` |
| `apps/v1/statefulsets` | `[delete,get,post]` | `[delete,get,patch,put]` | `scale=[get,patch,put]; status=[get,patch,put]` |
| `autoscaling/v1/horizontalpodautoscalers` | `[delete,get,post]` | `[delete,get,patch,put]` | `status=[get,patch,put]` |
| `autoscaling/v2/horizontalpodautoscalers` | `[delete,get,post]` | `[delete,get,patch,put]` | `status=[get,patch,put]` |
| `autoscaling/v2beta2/horizontalpodautoscalers` | `[delete,get,post]` | `[delete,get,patch,put]` | `status=[get,patch,put]` |
| `batch/v1/cronjobs` | `[delete,get,post]` | `[delete,get,patch,put]` | `status=[get,patch,put]` |
| `batch/v1/jobs` | `[delete,get,post]` | `[delete,get,patch,put]` | `status=[get,patch,put]` |
| `coordination.k8s.io/v1/leases` | `[delete,get,post]` | `[delete,get,patch,put]` | `-` |
| `core/v1/configmaps` | `[delete,get,post]` | `[delete,get,patch,put]` | `-` |
| `core/v1/endpoints` | `[delete,get,post]` | `[delete,get,patch,put]` | `-` |
| `core/v1/events` | `[delete,get,post]` | `[delete,get,patch,put]` | `-` |
| `core/v1/limitranges` | `[get]` | `[get]` | `-` |
| `core/v1/persistentvolumeclaims` | `[delete,get,post]` | `[delete,get,patch,put]` | `status=[get,patch,put]` |
| `core/v1/pods` | `[delete,get,post]` | `[delete,get,patch,put]` | `attach=[get,post]; ephemeralcontainers=[get,patch,put]; eviction=[post]; log=[get]; portforward=[get,post]; proxy=[delete,get,patch,post,put]; status=[get,patch,put]` |
| `core/v1/replicationcontrollers` | `[delete,get,post]` | `[delete,get,patch,put]` | `scale=[get,patch,put]; status=[get,patch,put]` |
| `core/v1/resourcequotas` | `[get]` | `[get]` | `status=[get]` |
| `core/v1/secrets` | `[delete,get,post]` | `[delete,get,patch,put]` | `-` |
| `core/v1/serviceaccounts` | `[delete,get,post]` | `[delete,get,patch,put]` | `token=[post]` |
| `core/v1/services` | `[delete,get,post]` | `[delete,get,patch,put]` | `proxy=[delete,get,patch,post,put]; status=[get,patch,put]` |
| `discovery.k8s.io/v1/endpointslices` | `[get]` | `[get]` | `-` |
| `events.k8s.io/v1/events` | `[delete,get,post]` | `[delete,get,patch,put]` | `-` |
| `networking.k8s.io/v1/ingresses` | `[delete,get,post]` | `[delete,get,patch,put]` | `status=[get,patch,put]` |
| `rbac.authorization.k8s.io/v1/rolebindings` | `[delete,get,post]` | `[delete,get,patch,put]` | `-` |
| `rbac.authorization.k8s.io/v1/roles` | `[delete,get,post]` | `[delete,get,patch,put]` | `-` |
<!-- END GENERATED -->

## Where the two lines agree

These conclusions follow from the tenant's **scope**, not from a Kubernetes version, so they hold on both columns and will keep holding if Arvan upgrades.

| Conclusion | Why it is version-independent |
|---|---|
| Every documented path is namespace-scoped, and no cluster-scoped endpoint exists | a namespace-scoped tenancy model is a product decision, not an API-version artefact |
| `LimitRange` and `ResourceQuota` are readable and not writable | quota is set by the platform for the tenant in every version |
| `DaemonSet` is unavailable to the tenant | a DaemonSet places a Pod on every node, and the tenant does not own nodes |
| `StorageClass`, `ClusterRole`, `ClusterRoleBinding`, and CustomResourceDefinition are unavailable | all four are cluster-scoped |
| OpenShift kinds (`Route`, `BuildConfig`) are unavailable | Arvan CaaS is not OpenShift |
| `Deployment`, `StatefulSet`, `Job`, `CronJob`, `Service`, `Ingress`, `ConfigMap`, `Secret`, `PersistentVolumeClaim`, `ServiceAccount`, `Role`, `RoleBinding`, and `HorizontalPodAutoscaler` are available | the namespaced workload core is stable across every supported minor |

## Where the two lines differ

This is the part that matters, and it is why a single-column matrix is a defect rather than a simplification. An agent reading only column A writes a manifest a current cluster rejects; an agent reading only column B writes one the pinned line rejects.

| Subject | A: pinned line (Kubernetes 1.25 era) | B: current upstream stable (1.34 to 1.36) | What to emit |
|---|---|---|---|
| HorizontalPodAutoscaler | serves `autoscaling/v1`, `autoscaling/v2`, **and `autoscaling/v2beta2`** | serves `autoscaling/v1` and `autoscaling/v2` only; **`v2beta2` was removed in 1.26** and the API server rejects it | **`autoscaling/v2` on both lines.** It is the only version that works everywhere. Never emit `v2beta2`: it is rejected on B, and on A it buys nothing that `v2` does not already give. |
| PodSecurityPolicy | `policy/v1beta1` was already removed in 1.25, so it is absent on A too | absent | never emit it; the replacement is the Pod Security Admission namespace labels described in `alaa-k8s-helm references/openshift-and-managed-platforms.md` |
| `PodDisruptionBudget` (`policy/v1`) | absent from the spec, so unavailable to the tenant | `policy/v1` has been GA since 1.21 and is namespaced, so an upgraded Arvan may well serve it | discovery decides. On A, a workload has no drain protection and the operator RUNBOOK must say so. On B, if `kubectl api-resources \| grep poddisruptionbudgets` returns a row and `kubectl auth can-i create poddisruptionbudgets -n NS` returns `yes`, emit one and size it per `alaa-k8s-helm references/failure-and-load.md`. |
| `NetworkPolicy` (`networking.k8s.io/v1`) | absent from the spec | namespaced and normal on a modern multi-tenant platform | discovery decides. On A the answer to "how do I isolate this workload's traffic" is that the platform owns it, and the deliverable must say so rather than emit an object that does nothing. On B, emit a default-deny plus explicit allows. |
| `EndpointSlice` | read-only for the tenant | read-only for the tenant | no difference; read it during service-path tracing |
| Dynamic Resource Allocation (`resource.k8s.io/v1`) | absent | GA since 1.34 | its presence is a positive signal that the target is on B |
| `flowcontrol.apiserver.k8s.io` | `v1beta3` era | `v1` only; `v1beta3` removed in 1.32 | never referenced by a tenant manifest; useful only as a line discriminator |
| Server URLs | two zones, `ir-tbz-sh1` and `ir-thr-ba1`, under `napi.arvancloud.ir/caas/v2` | unknown; an upgrade may add or rename zones | read them from the current kubeconfig, not from this file |

## How to act when a kind is absent from the discovered line

1. Say so explicitly in the deliverable. Do not emit the object silently, and do not emit it with a comment hoping someone notices.
2. Offer the Arvan-compatible alternative where one exists: for `NetworkPolicy`, state that traffic isolation is platform-owned and name what the application must do instead; for `PodDisruptionBudget`, state that voluntary disruption is unprotected and put the manual drain procedure in the RUNBOOK; for `DaemonSet`, use a sidecar in the workload that needs the agent.
3. Where no alternative exists, ask for cluster confirmation and name the exact command that would settle it.

`python3 alaa-k8s-helm scripts/check_manifests.py rendered.yaml --profile arvan` enforces rule 1 mechanically against the pinned line's absent-kind list.
