# Kubernetes Resource Patterns

## Contents

- Controller selection
- Services and exposure
- Reliability and disruption controls
- Storage patterns
- Security defaults
- Scheduling and scaling
- Practical recommendations by object

## Controller selection

### Pod

Use a naked Pod only for:

- debug or ephemeral investigation
- a one-off batch task that does not need retries or scheduling history
- tutorials or very small internal examples

Do not use a naked Pod for normal production apps. It has no rollout management, no stable owner controller, and poor recovery behavior.

### Deployment

Use for stateless apps, APIs, web frontends, and most workers.

Good defaults:

- RollingUpdate strategy
- readiness probe
- liveness probe when the app can actually self-heal
- startup probe for slow boots
- resource requests and limits
- ServiceAccount only when needed

### StatefulSet

Use for stateful apps with stable identity or per-replica storage.

Use it when you need:

- ordered startup or shutdown
- stable network identity
- one PVC per replica
- durable ordinal identity

Do not switch casually between Deployment and StatefulSet once data or identity is involved.

### DaemonSet

Use for one Pod per node patterns such as:

- log shippers
- node agents
- host networking helpers
- storage or security agents

### Job and CronJob

Use for finite or scheduled execution.

Prefer them over long-running Deployments for migrations, backups, batch imports, and scheduled maintenance.

## Services and exposure

### Service types

#### ClusterIP

Default choice for internal traffic. Use this for almost every app first.

Best for:

- app-to-app traffic inside the cluster
- backends behind Ingress, Gateway API, or Route
- databases and internal APIs

#### Headless Service

Use `clusterIP: None` when the client must discover individual Pod identities, commonly with StatefulSets.

#### NodePort

Use only when you specifically need node-level port exposure and cannot rely on a proper load-balancer or ingress path. It is rarely the best production default.

#### LoadBalancer

Use when the platform can provision an external load balancer for the Service and you need direct L4 exposure. Good for TCP or UDP services and some edge cases where HTTP routing is not enough.

#### ExternalName

Use for DNS aliasing to an external service. Do not use it as a general networking shortcut inside the cluster.

### Service recommendations

- Prefer named ports.
- Keep `selector` labels stable.
- Ensure `targetPort` maps to the actual container port.
- Use readiness probes so Services only send traffic to ready Pods.
- Use ClusterIP unless there is a clear reason to expose more broadly.

### Ingress

Use for standard Kubernetes HTTP or HTTPS exposure when an Ingress controller exists and the requirements are simple to moderate.

Use Ingress when:

- the platform is vanilla Kubernetes
- you need host- and path-based routing
- a standard controller already exists

### Gateway API

Use when the cluster supports it and the routing needs are more advanced than basic Ingress, especially when traffic ownership and policy boundaries need clearer separation.

Use Gateway API when:

- the controller supports it
- you need richer routing roles or policy attachment
- you need a more future-facing L4 or L7 API than classic Ingress

Do not assume Gateway API is installed. Check first.

### OpenShift Route

Use Route for platform-native OpenShift HTTP or HTTPS exposure.

Use Route when:

- the target is OpenShift
- you need `edge`, `passthrough`, or `reencrypt` TLS handling
- the platform’s router is the supported exposure path

Do not render Routes on vanilla Kubernetes.

## Reliability and disruption controls

### Probes

Use the right probe for the right job.

- **readinessProbe**: controls traffic eligibility
- **livenessProbe**: restarts a stuck process
- **startupProbe**: protects slow-starting apps from premature liveness failures

Recommendations:

- use readiness on almost all long-running services
- use startup probes for apps with long initialization
- avoid aggressive liveness probes that turn dependency outages into restart storms

### PodDisruptionBudget

Use PDBs for workloads that must survive voluntary disruptions such as node drains or upgrades.

Good candidates:

- highly available Deployments with at least 2 replicas
- StatefulSets where availability matters during maintenance

Poor candidates:

- single-replica apps that cannot meet the budget anyway
- workloads that are routinely deleted or recreated by operators or batch logic

Important nuance:

- PDBs constrain many voluntary disruptions, but deleting Pods or Deployments directly can bypass their protection.

### Rolling update behavior

For Deployments, align these with capacity and PDBs:

- `maxUnavailable`
- `maxSurge`
- readiness timing
- startup timing

A “valid” rollout can still deadlock if these values conflict.

## Storage patterns

### PersistentVolumeClaim

Use PVCs for durable state. Decide these fields deliberately:

- requested size
- storage class
- access mode
- volume mode when block devices matter

### Access mode guidance

- `ReadWriteOnce`: normal default for single-node writable storage
- `ReadWriteMany`: only when the driver supports shared writable access
- `ReadOnlyMany`: shared read-only access
- `ReadWriteOncePod`: strongest single-pod write guarantee when supported

### Storage recommendations

- use PVCs for data that must survive Pod recreation
- do not mount persistent storage for caches unless the cache actually needs persistence
- confirm storage class and expansion support before promising resize workflows
- remember that driver semantics matter more than YAML alone
- if advanced volume tuning is needed on modern Kubernetes, check whether `VolumeAttributesClass` is supported by the CSI driver

## Security defaults

### Pod and container security context

Prefer restrictive defaults.

Typical baseline:

- `runAsNonRoot: true`
- `allowPrivilegeEscalation: false`
- drop all capabilities unless one is required
- `readOnlyRootFilesystem: true` when the app can support it
- `seccompProfile.type: RuntimeDefault`

Do not hardcode `runAsUser` unless there is a strong reason. It hurts portability, especially on OpenShift.

### ServiceAccount and RBAC

Create a ServiceAccount only when the workload needs identity beyond the default one.

Grant the minimum namespace-scoped RBAC needed. ClusterRole and ClusterRoleBinding are cluster-admin territory unless the environment explicitly delegates them.

## Scheduling and scaling

### Resource requests and limits

Use requests and limits unless the user explicitly wants a different policy.

Why:

- scheduling accuracy
- better cluster fairness
- predictable HPA behavior
- fewer surprise evictions and CPU-throttling blind spots

### Affinity, anti-affinity, and topology spread

Use them deliberately.

- use anti-affinity or topology spread for availability-sensitive replicas
- use node affinity only when the node-class requirement is real
- do not add hard scheduling constraints without confirming capacity exists

### HorizontalPodAutoscaler

Use HPA when there is a real scaling signal and enough observability to tune it.

Good HPA inputs:

- CPU for CPU-bound stateless services
- memory only when memory correlates with useful saturation behavior
- custom metrics when they are trustworthy and maintained

Do not bolt on an HPA without requests. HPA decisions depend on requests and measured metrics.

## Practical recommendations by object

### Pod

- avoid for production services
- use only for debug, one-offs, or tightly constrained examples

### Service

- default to ClusterIP
- use named ports
- keep selectors explicit and stable

### Ingress

- use for standard HTTP routing on vanilla Kubernetes
- prefer Gateway API when advanced routing is required and the cluster supports it

### Route

- use on OpenShift for platform-native external HTTP or HTTPS exposure

### PDB

- use for multi-replica, disruption-sensitive apps
- skip when the workload cannot satisfy the budget

### PVC

- use for durable state
- validate storage class, access mode, and permission model before rollout
