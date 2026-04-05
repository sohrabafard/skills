# Runtime Debug Playbooks

## Contents

- Triage model
- Evidence collection order
- Common incident playbooks
- OpenShift-specific failure patterns
- Escalation boundaries

## Triage model

Classify the incident before proposing a fix.

### Failure layers

- **spec or render**: broken YAML, bad template, wrong fields
- **admission or policy**: SCC, PSA, RBAC, quota, webhook denial
- **scheduling**: insufficient resources, taints, affinity, missing PVC binding
- **image and startup**: pull errors, bad command, missing config, probe failures
- **service path**: no endpoints, DNS, port mismatch, route or ingress miswire
- **storage**: PVC pending, mount errors, permission denied, fsGroup mismatch
- **node or cluster**: NotReady nodes, pressure, CNI or DNS failures, API instability

Start by identifying the failing layer. Debugging gets much faster once the layer is correct.

## Evidence collection order

Use the cheapest high-signal evidence first.

1. current object status
2. describe output and events
3. current logs and previous logs
4. resource usage and restart history
5. service, endpoint, and DNS path
6. policy and permission checks
7. node or cluster health only if namespace-level evidence is insufficient

Useful commands:

```bash
kubectl get pods -A
kubectl describe pod <pod> -n <namespace>
kubectl logs <pod> -n <namespace> --all-containers --tail=200
kubectl logs <pod> -n <namespace> --all-containers --previous --tail=200
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
```

OpenShift equivalents can use `oc` directly.

## Playbook: Pod Pending

Typical causes:

- unsatisfied resources
- taints or affinity mismatch
- PVC not bound
- image pull secret or admission issue that appears during scheduling

Check in this order:

```bash
kubectl get pod <pod> -n <namespace> -o wide
kubectl describe pod <pod> -n <namespace>
kubectl get pvc -n <namespace>
kubectl get nodes
```

Likely fixes:

- reduce requests or add capacity
- adjust affinity, tolerations, or node selectors
- fix PVC or storage class issues
- remove impossible topology constraints

## Playbook: CrashLoopBackOff or repeated restarts

Check:

```bash
kubectl logs <pod> -n <namespace> --all-containers --tail=200
kubectl logs <pod> -n <namespace> --all-containers --previous --tail=200
kubectl describe pod <pod> -n <namespace>
kubectl top pod <pod> -n <namespace> --containers
```

Common causes:

- wrong command or args
- missing config or secret
- permission denied on startup path
- OOM kill
- probe restarts masking a slow startup
- app binds the wrong port or interface

Prefer `startupProbe` for slow-starting apps instead of inflating liveness thresholds indefinitely.

## Playbook: ImagePullBackOff or ErrImagePull

Check:

```bash
kubectl describe pod <pod> -n <namespace>
kubectl get secret -n <namespace>
```

Common causes:

- wrong image name or tag
- missing pull secret
- registry auth failure
- network egress or DNS failure to registry
- immutable tags unexpectedly updated

Low-risk fix order:

1. verify repository and tag
2. verify image pull secret reference and contents
3. verify registry reachability from cluster egress path
4. pin by digest if the failure is caused by mutable tags

## Playbook: readiness or liveness failures

Check:

```bash
kubectl describe pod <pod> -n <namespace>
kubectl get pod <pod> -n <namespace> -o yaml
```

Focus on:

- probe path, port, and scheme
- application bind address
- startup time vs probe timing
- TLS mismatch
- dependency readiness such as DB or cache availability

Do not “fix” a probe failure by removing the probe unless the probe itself is objectively wrong.

## Playbook: service connectivity failure

Check the full path.

```bash
kubectl get svc -n <namespace>
kubectl get endpoints,endpointslices -n <namespace>
kubectl get pod -n <namespace> --show-labels
kubectl exec -n <namespace> <source-pod> -- sh -c 'getent hosts <service> || nslookup <service>'
```

Common causes:

- selector mismatch
- wrong target port
- no ready endpoints
- NetworkPolicy denial
- DNS issues
- app only listening on localhost

If a Service exists but has no endpoints, fix labels or readiness first. Do not debug the ingress layer yet.

## Playbook: ingress, route, or gateway failure

Check in this order:

1. backend Service
2. endpoints
3. port mapping
4. TLS mode and hostname
5. controller-specific events or logs

For Kubernetes Ingress:

```bash
kubectl describe ingress <name> -n <namespace>
```

For OpenShift Route:

```bash
oc describe route <name> -n <namespace>
```

Common Route-specific causes:

- wrong service target port name
- TLS termination mode mismatch (`edge`, `reencrypt`, `passthrough`)
- service is healthy internally but host/path policy is wrong

## Playbook: PVC pending, mount failure, or permission denied

Check:

```bash
kubectl get pvc -n <namespace>
kubectl describe pvc <pvc> -n <namespace>
kubectl describe pod <pod> -n <namespace>
```

Common causes:

- missing or wrong storage class
- access mode mismatch
- requested size beyond quota or driver limits
- fsGroup or UID mismatch on mounted volume
- OpenShift arbitrary-UID constraints with image paths not writable

If the problem is permissions inside the mounted filesystem on OpenShift, check the image and volume ownership model before requesting `anyuid`.

## Playbook: rollout stuck

Check:

```bash
kubectl rollout status deployment/<name> -n <namespace>
kubectl describe deployment <name> -n <namespace>
kubectl get rs -n <namespace>
kubectl get pdb -n <namespace>
```

Common causes:

- failing new Pods
- maxUnavailable or maxSurge values that conflict with capacity
- PDB blocks
- image pull or probe failures
- selector mistakes

## Playbook: SCC, PSA, or permission denials on OpenShift

Look for these indicators:

- admission messages mentioning SCC or pod security
- pods accepted on vanilla Kubernetes but rejected on OpenShift
- writes to paths that assume a fixed UID
- containers trying to bind low ports or run privileged

Checks:

```bash
oc auth can-i use scc/anyuid -n <namespace>
oc describe pod <pod> -n <namespace>
oc get events -n <namespace> --sort-by='.lastTimestamp'
```

The safest fix is usually to make the image and manifest compatible with the default restricted posture, not to request broader SCCs.

## Cluster-level tools

Use cluster-level snapshots only when namespace evidence is not enough.

```bash
bash scripts/cluster_health.sh
python3 scripts/pod_diagnostics.py <pod> -n <namespace>
bash scripts/network_debug.sh <namespace> <pod>
```

On OpenShift, node-level investigation often uses:

```bash
oc debug node/<node>
chroot /host
```

Only recommend node debugging when the user has the correct access surface.

## Escalation boundaries

Escalate to cluster operators or admins when the likely cause is:

- missing CRD installation
- CNI, DNS, or Ingress controller outage
- storage class or CSI driver failure
- SCC grants, custom SCC creation, or namespace policy changes
- node pressure, kernel, CRI-O, or kubelet issues
- MachineConfig or runtime tuning requirements on OpenShift
