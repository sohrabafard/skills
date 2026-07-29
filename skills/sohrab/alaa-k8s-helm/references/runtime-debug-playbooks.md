# Runtime Debug Playbooks

## Contents

- Triage model
- Evidence collection order
- Symptom playbooks
- OpenShift-specific failure patterns
- Escalation boundaries

## Triage model

Classify the incident before proposing a fix. Identify the failing layer first; everything after it is faster.

- **spec or render** — broken YAML, bad template, wrong field
- **admission or policy** — SCC, Pod Security Admission, RBAC, quota, webhook denial
- **scheduling** — insufficient resources, taints, affinity, unbound PVC
- **image and startup** — pull error, bad command, missing config, probe failure
- **service path** — no endpoints, DNS, port mismatch, ingress or route miswire
- **storage** — PVC pending, mount error, permission denied, fsGroup mismatch
- **node or cluster** — NotReady nodes, pressure, CNI or DNS failure, API instability
- **degraded dependency** — the workload is Running and Ready, the error rate is up, and nothing restarted. This one has its own playbook in `references/failure-and-load.md`, because the fix is a reliability decision owned by `/alaa-reliability-sla` (`$alaa-reliability-sla`) rather than a Kubernetes object change.

## Evidence collection order

Cheapest high-signal evidence first.

1. current object status
2. describe output and events
3. current logs and previous logs
4. resource usage and restart history
5. service, endpoint, and DNS path
6. policy and permission checks
7. node or cluster health, only when namespace-level evidence is insufficient

```bash
kubectl get pods -n NS
kubectl describe pod POD -n NS
kubectl logs POD -n NS --all-containers --tail=200
kubectl logs POD -n NS --all-containers --previous --tail=200
kubectl get events -n NS --sort-by='.lastTimestamp'
```

On OpenShift, `oc` accepts each of these unchanged.

## Playbook: Pod Pending

Causes: unsatisfied resource requests, taints or affinity mismatch, an unbound PVC, or an admission failure that surfaces at scheduling time.

```bash
kubectl get pod POD -n NS -o wide
kubectl describe pod POD -n NS
kubectl get pvc -n NS
kubectl get nodes
```

Fixes, in increasing risk order: reduce requests or add capacity; correct affinity, tolerations, or node selectors; fix the StorageClass or PVC; remove an impossible topology constraint. A hard scheduling constraint with no matching capacity is the most common cause and the event message names the constraint.

## Playbook: CrashLoopBackOff or repeated restarts

```bash
kubectl logs POD -n NS --all-containers --tail=200
kubectl logs POD -n NS --all-containers --previous --tail=200
kubectl describe pod POD -n NS
kubectl top pod POD -n NS --containers
```

Causes: wrong command or args; missing config or Secret; permission denied on a startup path; `OOMKilled`; a liveness probe restarting a slow start; the application binding the wrong port or interface.

`lastState.terminated.reason` discriminates: `OOMKilled` means the memory limit, `Error` with a non-zero exit code means the application, and a restart with no terminated reason and a probe event means the liveness probe. Use a `startupProbe` for a slow start rather than inflating the liveness threshold; `references/failure-and-load.md` gives the derivation.

## Playbook: ImagePullBackOff or ErrImagePull

```bash
kubectl describe pod POD -n NS
kubectl get serviceaccount SA -n NS -o yaml
kubectl get secret -n NS
```

Causes: wrong image name or tag; missing or wrong `imagePullSecrets`; registry authentication failure; no egress or DNS path to the registry; a mutable tag that moved.

Fix order: verify repository and tag; verify the pull secret's name, type (`kubernetes.io/dockerconfigjson`), and that it is referenced by the Pod or its ServiceAccount; verify registry reachability from the cluster's egress path; pin by digest when a mutable tag is the cause. `/alaa-docker-production` (`$alaa-docker-production`) owns tag and digest policy.

## Playbook: readiness or liveness failure

```bash
kubectl describe pod POD -n NS
kubectl get pod POD -n NS -o yaml
```

Focus on probe path, port, and scheme; the application's bind address; startup time against probe timing; a TLS mismatch between probe and listener; and dependency readiness the probe should not be testing.

Do not resolve a probe failure by deleting the probe. Resolve it by correcting the probe when the probe is wrong, and by correcting the application or the threshold when it is not. `references/failure-and-load.md` states which thresholds are derivable and how.

## Playbook: service connectivity failure

```bash
kubectl get svc -n NS
kubectl get endpointslices -n NS
kubectl get pod -n NS --show-labels
kubectl exec -n NS SOURCE_POD -- sh -c 'getent hosts SERVICE || nslookup SERVICE'
bash scripts/network_debug.sh NS POD
```

Causes: selector mismatch, wrong `targetPort`, no ready endpoints, NetworkPolicy denial, DNS failure, or an application listening only on localhost.

When the Service exists with no endpoints, fix labels or readiness first and do not touch the ingress layer yet.

## Playbook: ingress, route, or gateway failure

Check in this order: backend Service, endpoints, port mapping, TLS mode and hostname, then controller-specific events or logs.

```bash
kubectl describe ingress NAME -n NS
oc describe route NAME -n NS
```

Route-specific causes: a wrong service target-port name; a TLS termination mode mismatch across `edge`, `reencrypt`, and `passthrough`; a healthy internal Service behind a wrong host or path policy. The termination modes themselves are defined once in `references/openshift-and-managed-platforms.md`.

## Playbook: PVC pending, mount failure, or permission denied

```bash
kubectl get pvc -n NS
kubectl describe pvc PVC -n NS
kubectl describe pod POD -n NS
```

Causes: missing or wrong StorageClass; access-mode mismatch against the driver; requested size beyond quota or driver limits; fsGroup or UID mismatch on the mounted volume; on OpenShift, an arbitrary-UID assignment against image paths that are not group-writable.

When the failure is permissions inside a mounted filesystem on OpenShift, fix the image's ownership model before requesting a broader SCC.

## Playbook: rollout stuck

```bash
kubectl rollout status deployment/NAME -n NS
kubectl describe deployment NAME -n NS
kubectl get rs -n NS
kubectl get pdb -n NS
```

Causes: new Pods failing; `maxUnavailable` and `maxSurge` values that conflict with capacity or with the PDB; PDB blocks; image pull or probe failure; a selector mistake.

The deadlock condition and the arithmetic that resolves it are in `references/failure-and-load.md`. Do not delete the PDB to unblock a rollout; that removes the protection the drain will need next.

## Playbook: SCC, PSA, or permission denial on OpenShift

Indicators: an admission message naming an SCC or pod security; Pods that are accepted on vanilla Kubernetes and rejected on OpenShift; writes to paths that assume a fixed UID; containers binding low ports or requesting privilege.

```bash
oc auth can-i use scc/anyuid -n NS
oc describe pod POD -n NS
oc get events -n NS --sort-by='.lastTimestamp'
kubectl get ns NS -o jsonpath='{.metadata.labels}'
```

The last command shows the Pod Security Admission labels, which are a second, independent gate; a workload can pass SCC and fail PSA. The safest fix is to make the image and manifest satisfy the restrictive path in `references/openshift-and-managed-platforms.md`, not to request a broader SCC.

## Cluster-level tools

Use a cluster-level snapshot only when namespace evidence is insufficient.

```bash
bash scripts/cluster_health.sh
python3 scripts/pod_diagnostics.py POD -n NS
bash scripts/network_debug.sh NS POD
```

On OpenShift, node-level investigation uses `oc debug node/NODE` followed by `chroot /host`. Recommend it only after confirming the user's access surface.

## Escalation boundaries

Escalate to the cluster operator or platform owner when the likely cause is a missing CRD installation, a CNI or DNS or ingress-controller outage, a StorageClass or CSI driver failure, an SCC grant or namespace policy change, node pressure or kernel or kubelet issues, or `MachineConfig` and runtime tuning on OpenShift. State the evidence that points there, so the escalation carries its own proof.
