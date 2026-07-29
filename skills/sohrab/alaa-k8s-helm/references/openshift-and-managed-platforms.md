# OpenShift and Managed Platforms

## Contents

- Platform detection
- Vanilla Kubernetes, OpenShift, and managed namespace platforms
- Access surfaces and what they unlock
- Restricted-by-default fields and the restrictive path
- OpenShift security model: SCC, Pod Security Admission, and the removal of PodSecurityPolicy
- Arbitrary UID and rootless compatibility
- Routes, `oc`, and platform-native patterns
- Access matrix for common objects

## Platform detection

Detect the platform before recommending manifests or commands.

```bash
oc version
kubectl version --output=yaml
kubectl api-resources | grep -E 'route.openshift.io|security.openshift.io|image.openshift.io'
kubectl get route -A
```

- **Vanilla Kubernetes**: `kubectl` works and no OpenShift API group is served.
- **OpenShift**: `oc` works, or `route.openshift.io` and `security.openshift.io` are served.
- **Managed namespace or container platform**: manifests and charts apply, but nodes, cluster operators, and platform-wide networking do not respond. `kubectl auth can-i list nodes` returning `no` is the cheapest single signal.

## Platform comparison

### Vanilla Kubernetes

Standard APIs, Ingress or Gateway API for external HTTP, Pod Security Admission plus whatever cluster-specific policy the operator added. Chart portability is highest when the chart avoids distribution-specific kinds.

### OpenShift

An opinionated layer on top of Kubernetes. The differences that change a manifest:

- `oc` extends `kubectl`.
- `Route` provides platform-native HTTP and HTTPS exposure.
- Security Context Constraints control what a Pod may do, and remain a live admission control on the current OpenShift line.
- Kubernetes Pod Security Admission also runs, and OpenShift synchronises PSA warn and audit labels from SCC permissions in many namespaces.
- Defaults are stricter, so arbitrary-UID and non-root compatibility matter far more than on vanilla Kubernetes.
- Node and runtime tuning goes through `MachineConfig`, `KubeletConfig`, and `ContainerRuntimeConfig` rather than ad hoc node edits, and all three are cluster-admin work.

### Managed namespace or container platforms

The platform owns cluster lifecycle and node tuning; the user deploys into namespaces or projects; node access is unavailable; cluster-scoped changes are restricted; some exposure features are implemented through a panel rather than an API object.

Treat such a platform as namespace-scoped until a command proves otherwise, and discover its real surface rather than assuming one:

```bash
kubectl api-resources --namespaced=true -o name    # what this tenant can address
kubectl api-resources --namespaced=false -o name   # empty or tiny on a namespace-only platform
kubectl auth can-i --list -n NS                    # what this identity may actually do
```

For **ArvanCloud CaaS specifically**, load `/caas-arvan-kuber` (`$caas-arvan-kuber`) only when the answer depends on a fact that is true of Arvan CaaS and false of stock Kubernetes at the same minor version; otherwise stay in `/alaa-k8s-helm` (`$alaa-k8s-helm`) and use the generic posture above, including when the target cluster happens to be Arvan.

## Access surfaces and what they unlock

Four surfaces. Each row names the command that proves the surface rather than assuming it.

### Cluster-admin

Unlocks: CRDs and cluster operators, StorageClass, IngressClass, GatewayClass, ClusterRole and ClusterRoleBinding, SCC creation and broad grants, namespaces and projects, node debugging, `MachineConfig` and kubelet runtime changes.

Prove with `kubectl auth can-i create customresourcedefinitions`.

### Namespace or project admin

Unlocks: Deployment, StatefulSet, DaemonSet, Job, CronJob, Service, Ingress, Route, NetworkPolicy, PVC when the StorageClass already exists, HPA, PDB, ServiceAccount, Role, RoleBinding, ConfigMap, Secret.

Prove with `kubectl auth can-i create deployments -n NS` and, for the policy objects, `kubectl auth can-i create rolebindings -n NS`.

### Developer

Usually: read, logs, exec, rollout status, patching some workloads, creating basic namespaced resources in developer-owned namespaces.

Do not assume a developer can create Routes, RoleBindings, or PVCs. Prove each with the exact verb before promising it.

### Container-only access

This is not Kubernetes API access. Available: an application shell, files, processes, environment variables, sockets, and logs inside the container, and connectivity tests from inside the workload. Unavailable: creating or patching any object, reading cluster events or endpoints, inspecting node, StorageClass, or SCC state. There is no `auth can-i` to run, because there is no API client.

## Restricted-by-default fields and the restrictive path

This is the single list. `SKILL.md` and `references/authoring-workflows.md` point here rather than repeating it.

Emit none of the following. Each row gives the one observable condition that permits an exception; when you take an exception, name the SCC or admission policy in the output.

| Field | Why it is restricted | The condition that permits it |
|---|---|---|
| `securityContext.privileged: true` | disables every container isolation boundary | `oc auth can-i use scc/privileged -n NS` returns `yes`, or the user quotes the PSA level and admission policy that allow it |
| `hostNetwork: true` | shares the node's network namespace and port space | as above, plus a stated reason no Service can satisfy |
| `hostPID: true`, `hostIPC: true` | exposes other tenants' processes and IPC | as above |
| `hostPath` volume | writes to the node filesystem and pins the Pod to a node | as above; on any managed platform, treat as unavailable |
| a fixed `runAsUser` | breaks on any platform that assigns an arbitrary UID | the image genuinely requires a specific UID **and** `oc auth can-i use scc/anyuid -n NS` returns `yes` |
| a `containerPort` below 1024 | requires `NET_BIND_SERVICE` or root under most policies | never needed: listen on 8080 or 8443 in the container and map 80 or 443 at the Service, Ingress, or Route |
| `allowPrivilegeEscalation: true` | lets a process gain more privilege than its parent | no condition; set it to `false` |

**The restrictive path**, which is what "when the platform is uncertain" means concretely: no cluster-scoped object, no `Route`, no `hostPath`, no privileged container, `runAsNonRoot: true` with `runAsUser` unset, `allowPrivilegeEscalation: false`, `capabilities.drop: ["ALL"]`, `seccompProfile.type: RuntimeDefault`, and all container ports above 1024.

## OpenShift security model

### Security Context Constraints

SCCs govern whether a Pod may run privileged, use host networking, use particular volume types, request capabilities, or run as particular users and groups.

- Do not modify a default SCC. They are shared cluster state and other tenants depend on them.
- Create a custom SCC only when the workload cannot be made to fit `restricted-v2` and only when `oc auth can-i create securitycontextconstraints` returns `yes`.

### Pod Security Admission, and what happened to PodSecurityPolicy

`PodSecurityPolicy` (`policy/v1beta1`) was **removed from Kubernetes in 1.25**. Pod Security Admission became stable in the same release and is its replacement. When a repository still contains a PSP manifest, it has been inert since that cluster reached 1.25; translate it rather than reinstating it.

The replacement is three namespace labels, each set to one of the levels `privileged`, `baseline`, or `restricted`:

```yaml
metadata:
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

`enforce` rejects the Pod, `audit` records it, and `warn` returns a client warning. A workload built to the restrictive path above satisfies `restricted`.

**SCC and PSA are independent controllers. A workload that passes one may still be rejected by the other.** On OpenShift, check both when a Pod is denied.

## Arbitrary UID and rootless compatibility

Assume a stricter runtime posture than vanilla Kubernetes.

- Do not rely on a fixed runtime UID.
- Do not hardcode ownership under `/app`, `/var/lib/...`, or `$HOME`.
- Keep writable paths group-owned by `0` and mirror the user's permissions to the group during the image build. `/alaa-docker-production` (`$alaa-docker-production`) owns the image side of this.
- Set `readOnlyRootFilesystem: true` and mount an `emptyDir` at every path the process writes. When the write paths are unknown, find them before shipping: run the container with the flag set and read the failures, or `kubectl exec POD -- sh -c 'find / -xdev -newer /proc -type f 2>/dev/null | head -50'` on a running instance.

Applications listen on high ports such as 8080 or 8443; 80 and 443 are exposed by the Service, Ingress, or Route.

## Routes, `oc`, and platform-native patterns

### Routes

`Route` is the OpenShift-native external exposure object for HTTP and HTTPS. Use it when the target is OpenShift and the platform router is the supported exposure path, or when a TLS termination mode of `edge`, `reencrypt`, or `passthrough` is required. Use Ingress instead when portability across distributions matters more than platform-native behaviour. Do not render a Route on vanilla Kubernetes. The object-level detail is in `references/kubernetes-resource-patterns.md`.

### `oc` command guidance

Use `oc` rather than `kubectl` when the task depends on an OpenShift-only resource or workflow.

```bash
oc get route -n NS
oc describe route NAME -n NS
oc expose service/NAME
oc auth can-i use scc/anyuid -n NS
oc debug node/NODE
```

### Machine configuration and tuning

Node and runtime tuning on OpenShift goes through `MachineConfig`, `KubeletConfig`, and `ContainerRuntimeConfig`. This is cluster-admin work. Do not promise node-level tuning to a user who holds only project access.

## Access matrix for common objects

**Usually namespaced and safe to recommend first:** Deployment, StatefulSet, DaemonSet, Job, CronJob, Service, ConfigMap, Secret, ServiceAccount, Role, RoleBinding, Ingress, Route, PVC, HPA, PDB, NetworkPolicy.

**Usually cluster-scoped or admin-sensitive:** Namespace or Project creation, CRD, ClusterRole, ClusterRoleBinding, StorageClass, IngressClass, GatewayClass, SCC creation or broad grants, `MachineConfig`, `KubeletConfig`, `ContainerRuntimeConfig`, node operations.

On a namespace-only managed platform, several kinds in the first list may still be absent. `kubectl api-resources --namespaced=true -o name` is the answer for the actual target; the list above is the answer for a normal cluster.
