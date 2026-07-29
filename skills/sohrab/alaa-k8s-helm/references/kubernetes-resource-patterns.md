# Kubernetes Resource Patterns

Object-by-object decision rules: which controller, which Service type, which probe, which access mode, which security context. Each rule is stated once here; the values behind a rollout, probe, or PDB number come from `references/failure-and-load.md`.

## Contents

- Controller selection
- Services and exposure
- Probes and disruption controls
- Storage patterns
- Security defaults
- Scheduling and scaling

## Controller selection

| Controller | Use it for | Do not use it for |
|---|---|---|
| `Deployment` | stateless applications, APIs, web frontends, workers with no stable identity | anything that needs per-replica storage or ordinal identity |
| `StatefulSet` | stable network identity, ordered startup or shutdown, one PVC per replica, durable ordinal identity | a stateless service, where it only slows rollouts |
| `DaemonSet` | one Pod per node: log shippers, node agents, host networking helpers, storage or security agents | anything on a namespace-scoped managed platform, where the tenant does not own nodes |
| `Job` and `CronJob` | finite or scheduled work: migrations, backups, batch imports, scheduled maintenance | long-running services |
| bare `Pod` | debug, ephemeral investigation, a one-off batch task with no retry or history requirement | production services: there is no rollout management, no owning controller, and no recovery behaviour |

Switching a workload between `Deployment` and `StatefulSet` once data or identity exists is a migration, not an edit: the selector and the volume identity both change. Emit the new object under a new name and state the cutover order.

## Services and exposure

### Service types

- **ClusterIP** — the default for internal traffic: app-to-app calls, backends behind Ingress, Gateway API, or Route, databases, and internal APIs.
- **Headless** (`clusterIP: None`) — when the client must address individual Pod identities, normally with a StatefulSet.
- **NodePort** — only when node-level port exposure is genuinely required and no load balancer or ingress path exists. It exposes the port on every node.
- **LoadBalancer** — when the platform provisions an external load balancer and the workload needs L4 exposure, for TCP or UDP services and cases where HTTP routing is insufficient.
- **ExternalName** — DNS aliasing to an external service only. It creates no proxying and no health checking.

Never set `spec.externalIPs`: the field trusts every user in the cluster (CVE-2020-8554) and is being removed from Kubernetes 1.36. Use a `LoadBalancer` Service, an Ingress, or Gateway API instead.

### Service rules

- Use named ports, and make `targetPort` reference the container port's name rather than its number, so a port change in the workload cannot silently break the Service.
- Keep `selector` labels stable; they are matched against the Pod template's labels, not the workload's own.
- Every backend Pod carries a readiness probe, so the Service routes only to ready Pods.
- Default to ClusterIP and widen only with a stated reason.

### Ingress

Standard HTTP and HTTPS exposure when an Ingress controller is installed and routing needs are host- and path-based. Confirm the controller exists with `kubectl get ingressclass` before emitting one; an Ingress with no controller is an object that does nothing and reports nothing.

### Gateway API

Use it when `kubectl api-resources --api-group=gateway.networking.k8s.io` returns rows and the routing need exceeds Ingress: richer routing roles, policy attachment, or a separation between the platform team that owns the Gateway and the application team that owns the routes. Do not assume it is installed.

### OpenShift Route

`Route` is the platform-native OpenShift exposure object and its TLS termination modes are `edge`, `reencrypt`, and `passthrough`. The full rule, including when to use Ingress instead, is stated once in `references/openshift-and-managed-platforms.md`.

## Probes and disruption controls

- **`readinessProbe`** controls traffic eligibility. Every container that serves traffic has one.
- **`livenessProbe`** restarts a stuck process and nothing else. It must not call a downstream dependency.
- **`startupProbe`** protects a slow boot, and is the correct alternative to an inflated liveness threshold.

The thresholds themselves, the `terminationGracePeriodSeconds` and `preStop` relationship, and the `replicas`/`maxSurge`/`maxUnavailable`/PDB arithmetic are derived in `references/failure-and-load.md`. Do not copy a threshold from an example.

**PodDisruptionBudget**: use one for a workload that must survive a voluntary disruption such as a node drain or a cluster upgrade, and only when replicas are at least 2. A single-replica workload with `minAvailable: 1` blocks every drain permanently. A PDB constrains eviction; it does not constrain `kubectl delete`.

## Storage patterns

### PersistentVolumeClaim

Decide four fields deliberately: requested size, storage class, access mode, and volume mode when a block device matters.

### Access modes

- `ReadWriteOnce` — the normal default for single-node writable storage.
- `ReadWriteMany` — only when the CSI driver supports shared writable access; confirm against the driver's documentation, not the StorageClass name.
- `ReadOnlyMany` — shared read-only access.
- `ReadWriteOncePod` — the strongest single-Pod write guarantee, when the driver supports it.

### Storage rules

- Use a PVC for data that must survive Pod recreation, and only for that. A cache that can be rebuilt goes in an `emptyDir`.
- Confirm that the StorageClass sets `allowVolumeExpansion: true` before promising a resize workflow: `kubectl get storageclass NAME -o jsonpath='{.allowVolumeExpansion}'`.
- Driver semantics decide behaviour; the YAML only requests it.
- `VolumeAttributesClass` is available for live volume tuning when the cluster and the CSI driver both support it. Its version status is in `references/version-awareness.md`.

## Security defaults

### Pod and container security context

The baseline, applied to every container unless an exception is justified as `references/openshift-and-managed-platforms.md` describes:

```yaml
securityContext:
  runAsNonRoot: true
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop: ["ALL"]
  seccompProfile:
    type: RuntimeDefault
```

`readOnlyRootFilesystem: true` is the default, not an aspiration: mount an `emptyDir` at every path the process writes. When the write paths are unknown, find them with the procedure in `references/openshift-and-managed-platforms.md` before shipping.

Do not set `runAsUser`. A fixed UID breaks on any platform that assigns an arbitrary one, and `runAsNonRoot: true` already prevents root without pinning a number.

`scripts/check_manifests.py` asserts this whole block against rendered output.

### Secrets

- A Secret's `data` is base64, which is an encoding and not a protection. Anything that can read the Secret can read the value.
- Set `automountServiceAccountToken: false` on the Pod spec unless the workload calls the Kubernetes API. The default mounts a usable API token into every container.
- Never write a rendered manifest containing Secret objects to a shared or world-readable path, and never commit one. `/alaa-security-review` (`$alaa-security-review`) owns the fail-closed doctrine for handling one.
- Mount a Secret or ConfigMap into a dedicated directory such as `/etc/APP/config`. Mounting onto a directory the image already populates replaces its entire contents and produces a startup failure with no obvious cause.

### ServiceAccount and RBAC

Create a ServiceAccount only when the workload needs an identity beyond `default`. Grant the minimum namespace-scoped `Role` and `RoleBinding` the workload needs. `ClusterRole` and `ClusterRoleBinding` are cluster-admin territory unless the environment explicitly delegates them.

## Scheduling and scaling

### Requests and limits

Every container declares both. Requests decide scheduling and QoS class; limits decide throttling and OOM behaviour. The consequences at each boundary, and how to size a pool against replica count, are in `references/failure-and-load.md`. The complexity budget behind the number is `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`).

### Affinity, anti-affinity, and topology spread

- Use `topologySpreadConstraints` or pod anti-affinity for availability-sensitive replicas, so a single node or zone loss cannot take the whole workload.
- Use node affinity only when the node-class requirement is real, and name the label key.
- Do not add a hard scheduling constraint (`requiredDuringSchedulingIgnoredDuringExecution`) without first confirming that enough matching capacity exists; the failure mode is `Pod Pending` with an unschedulable event and no application error.

### HorizontalPodAutoscaler

Use `autoscaling/v2`. Good inputs: CPU for a CPU-bound stateless service, memory only when memory correlates with real saturation, custom metrics when they are trustworthy and maintained.

An HPA requires `resources.requests.cpu` on the scaled containers; without it the CPU target is a percentage of nothing and the autoscaler never acts. `maxReplicas` is a budget against the smallest downstream limit the workload can exhaust, as `references/failure-and-load.md` explains. Never combine `spec.replicas` in the workload with an enabled HPA on the same object: each fights the other on every reconcile.
