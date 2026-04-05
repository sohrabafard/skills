# OpenShift and Managed Platforms

## Contents

- Platform detection
- Vanilla Kubernetes vs OpenShift vs managed namespace platforms
- Access surfaces and what they unlock
- OpenShift security model
- Routes, `oc`, and platform-native patterns
- Arvan Cloud Container guidance
- Access matrix for common objects

## Platform detection

Detect the platform before recommending manifests or commands.

Useful checks:

```bash
oc version
kubectl version --output=yaml
kubectl api-resources | rg 'route.openshift.io|security.openshift.io|image.openshift.io'
kubectl get route -A
```

Heuristics:

- **vanilla Kubernetes**: `kubectl` works, no OpenShift API groups or Routes.
- **OpenShift**: `oc` works or OpenShift API groups and Routes exist.
- **managed namespace/container platform**: user can deploy manifests or charts but cannot manage cluster nodes, cluster operators, or platform-wide networking.

## Platform comparison

### Vanilla Kubernetes

Typical characteristics:

- standard Kubernetes APIs
- Ingress or Gateway API for external HTTP exposure
- Pod Security Admission plus cluster-specific policies
- chart portability is higher if the chart avoids distribution-specific objects

### OpenShift

Adds an opinionated platform layer on top of Kubernetes.

Key differences that matter for this skill:

- `oc` CLI extends `kubectl`
- Route objects provide platform-native HTTP and HTTPS exposure
- SCCs still control what pods may do
- Kubernetes Pod Security Admission also exists and is reconciled with SCC-driven label synchronization
- stricter defaults make arbitrary-UID and non-root compatibility much more important
- cluster-level node tuning is often mediated through MachineConfig, KubeletConfig, and ContainerRuntimeConfig instead of ad hoc node edits

### Managed namespace or container platforms

Typical characteristics:

- the platform manages cluster lifecycle and node tuning
- users deploy images, manifests, or charts into namespaces or projects
- direct node access is unavailable
- cluster-scoped changes are restricted or unsupported
- some exposure features may be implemented through a panel or higher-level workflow

Treat these platforms as namespace-scoped until the user proves broader access.

## Access surfaces and what they unlock

### Cluster-admin

Usually required for:

- CRDs and cluster operators
- StorageClasses and IngressClasses
- GatewayClasses
- ClusterRoles and ClusterRoleBindings
- SCC creation or broad SCC grants
- namespaces or projects
- node debugging and runtime tuning
- MachineConfig or kubelet runtime changes

### Namespace or project admin

Usually sufficient for:

- Deployments, StatefulSets, DaemonSets, Jobs, CronJobs
- Services, Ingresses, Routes, NetworkPolicies
- PVCs if the storage class already exists
- HPAs, PDBs, ServiceAccounts, Roles, and RoleBindings in that namespace
- ConfigMaps and Secrets

### Developer

Often sufficient for:

- read operations
- logs and exec
- rollout status
- patching some workloads
- creating basic namespaced resources in developer-owned namespaces

Do not assume developers can create Routes, RoleBindings, or PVCs without checking.

### Container-only access

This is not Kubernetes API access.

You can usually do:

- application shell or console access
- read files, processes, env vars, sockets, and logs available inside the container
- test upstream or downstream connectivity from inside the workload

You usually cannot do:

- create or patch arbitrary Kubernetes objects
- read cluster events or endpoint objects
- inspect node, storage class, or SCC state

## OpenShift security model

### SCCs

Security Context Constraints are still a core OpenShift admission control. They govern whether a pod may run privileged, use host networking, use certain volume types, request certain capabilities, or run as certain users and groups.

Important practice rule:

- do not modify default SCCs
- create custom SCCs only when absolutely necessary and only when the user actually controls that surface

### Pod Security Admission on OpenShift

OpenShift also includes Kubernetes Pod Security Admission.

Operationally relevant points:

- Pod Security Admission can enforce, warn, and audit namespace-level pod-security labels.
- OpenShift also synchronizes PSA warning and audit labels based on SCC permissions in many namespaces.
- SCC and PSA are independent controllers. A workload that passes one may still be affected by the other.

### Arbitrary UID and rootless compatibility

Assume a stricter runtime posture than vanilla Kubernetes.

Authoring rules that keep images portable:

- do not rely on a fixed runtime UID
- avoid hardcoded ownership assumptions under `/app`, `/var/lib/...`, or `$HOME`
- keep writable paths group-owned by `0` and mirror user permissions to the group during image build
- avoid binding directly to privileged ports below 1024 unless you know the platform policy allows it
- avoid `privileged`, `hostPath`, `hostNetwork`, and `hostPID` unless the workload truly needs them and the user can use the required SCC

Prefer applications that listen on high ports such as `8080` or `8443`, then expose `80` or `443` through Service, Ingress, or Route.

## Routes, `oc`, and platform-native patterns

### Routes

Routes are OpenShift-native external exposure objects for HTTP and HTTPS workloads.

Use Route when:

- the user targets OpenShift
- they want platform-native routing
- they need OpenShift TLS termination modes such as `edge`, `reencrypt`, or `passthrough`

Use Ingress instead when portability matters more than OpenShift-native features.

### `oc` command guidance

Prefer `oc` over `kubectl` when the task depends on OpenShift-only resources or workflows.

Examples:

```bash
oc get route -n <namespace>
oc describe route <name> -n <namespace>
oc expose service/<name>
oc auth can-i use scc/anyuid -n <namespace>
oc debug node/<node>
```

### Machine configuration and tuning

Node and runtime tuning on OpenShift is usually not done by manual SSH edits. It is managed through platform objects such as:

- `MachineConfig`
- `KubeletConfig`
- `ContainerRuntimeConfig`

This is cluster-admin work. Do not promise node-level tuning on OpenShift if the user only has project access.

## Arvan Cloud Container guidance

Treat Arvan Cloud Container as a managed Kubernetes-based application platform unless the user proves deeper access.

Public product and docs signals relevant to this skill:

- direct manifest deployment is supported
- Helm is supported
- users can obtain kubeconfig and manage apps by CLI
- panel workflows exist for domains, internal networking, dedicated IP, console access, and scaling
- the platform is managed, so cluster lifecycle and hardware or node management are abstracted away

Practical guidance:

- assume namespace or project scope, not cluster-admin
- prefer Deployment, Service, Ingress, Route-like platform workflows, PVC, HPA, and ConfigMap or Secret changes over cluster-scoped objects
- do not recommend node tuning, custom CNI work, or cluster-wide operators unless the user explicitly confirms that they control those surfaces
- when the panel already manages external exposure, check whether a domain workflow creates the ingress path for you before asking the user to handcraft another public entry point
- when the user says “container access”, treat that as app-level shell or console access, not proof of kubeconfig or RBAC rights

## Access matrix for common objects

### Usually namespaced and safer to recommend first

- Deployment
- StatefulSet
- DaemonSet
- Job
- CronJob
- Service
- ConfigMap
- Secret
- ServiceAccount
- Role and RoleBinding
- Ingress
- Route
- PVC
- HPA
- PDB
- NetworkPolicy

### Usually cluster-scoped or admin-sensitive

- Namespace or Project creation
- CRD
- ClusterRole and ClusterRoleBinding
- StorageClass
- IngressClass
- GatewayClass
- SCC creation or broad grants
- MachineConfig, KubeletConfig, ContainerRuntimeConfig
- node operations

When in doubt, verify with `kubectl auth can-i` or `oc auth can-i` instead of guessing.
