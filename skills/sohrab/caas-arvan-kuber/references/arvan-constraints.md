# Arvan CaaS constraints

The single normative statement of every Arvan platform constraint. Each rule appears here once and nowhere else in this skill. Where a rule is generic Kubernetes rather than Arvan, this file names the owner instead of restating it.

Each rule carries its status: **confirmed by Arvan** with the page that says so, **observed** with what was seen and when, or **unverified**. Treat an unverified rule as a hypothesis to test with discovery, not as a constraint to enforce.

Which of these apply at all is decided by the Step 1 line detection in `SKILL.md`. Read `references/arvan-capability-matrix.md` for the per-kind answer.

## 1. Resources are mandatory and parity is enforced

**Confirmed by Arvan** — https://docs.arvancloud.ir/en/cloud-container/create-app/manifest, checked 2026-07-29.

- Every container declares `resources.requests` and `resources.limits`, both with `cpu` and `memory`. Arvan's manifest page states that resource consumption must be specified per container.
- **`requests` must equal `limits`.** Arvan's manifest page states that "the values of Limits and Requests must be the same". This also gives the Pod Guaranteed QoS, which is what you want on a shared platform.
- **When resources are omitted, Arvan applies its own defaults of 1 CPU core and 2 GB of RAM per container.** Omitting them is therefore not "unlimited"; it is "whatever the platform decided", which is usually wrong and always unbudgeted.
- **Memory follows CPU at a ratio of 1 to 2.** Arvan's manifest page recommends "the ratio of 1 to 2 processor and RAM", and its own default (1 CPU, 2 GB) follows it.

  One function, so two inputs never get two different rules:

  ```
  memory_MiB = ceil(cpu_cores * 2 * 1024 / 64) * 64
  express it as Gi when the result is a whole multiple of 1024Mi
  ```

  | `cpu` | `memory` |
  |---|---|
  | `0.2` | `448Mi` |
  | `0.3` | `640Mi` |
  | `0.5` | `1Gi` |
  | `1` | `2Gi` |
  | `1.5` | `3Gi` |
  | `2` | `4Gi` |

  This is a starting point, not a measurement. When the workload's real memory profile is known, use the measured value and say that it deviates from the ratio and why. The complexity budget behind the number is `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`); the headroom target is `/alaa-reliability-sla` (`$alaa-reliability-sla`).

- Include `ephemeral-storage` in both `requests` and `limits` when the namespace's LimitRange declares a default or a maximum for it. `kubectl -n NS get limitrange -o yaml` shows whether it does.

### CPU written as decimal cores, and why this is style rather than a constraint

`0.2` and `200m` are the **same quantity** to the Kubernetes API: `resource.Quantity` parses both identically and serialises back to `200m`. No Arvan document states that `200m` is rejected, and no admission failure for it has been observed. So write decimal cores to match what the Arvan panel displays, and treat a chart that uses millicores as correct rather than broken. Any checker compares parsed quantities and not strings; `/alaa-k8s-helm` (`$alaa-k8s-helm`) `scripts/check_manifests.py --profile arvan` does.

## 2. Scaling is stateless-only

**Confirmed by Arvan** — https://docs.arvancloud.ir/en/cloud-container/manage-app/scaling, checked 2026-07-29.

- Horizontal scaling "is only applicable to stateless applications".
- "If your application has Persistent Storage enabled, you cannot use manual or automatic scaling." Both are disabled, not just the automatic one.

Therefore: an HPA targets a `Deployment`. A workload with a PVC gets no HPA and no replica knob in values; it gets a runbook procedure instead, and the RUNBOOK states that scaling requires detaching storage. `--profile arvan` in the shared manifest checker enforces the HPA target.

## 3. Disk lifecycle

**Confirmed by Arvan** — https://docs.arvancloud.ir/en/cloud-container/disk/, checked 2026-07-29.

- The container filesystem is ephemeral: its contents are deleted on every application restart. Anything that must survive a restart is on a disk.
- Disk size **increases only**; decreasing is not possible, and the size must be a whole number.
- **Detaching a disk restarts the application.** A detached disk keeps its data and can be reattached with a new mount path and capacity.
- **Deleting a disk is irreversible**; the data is unrecoverable.

Therefore: every disk operation is a runbooked, announced change, and the operator RUNBOOK carries the procedure before the first disk is attached, not after.

## 4. Exposure has three modes, and one uses annotations Arvan does not document

**Partly confirmed, partly observed.** Arvan's dedicated-IP page (https://docs.arvancloud.ir/en/cloud-container/manage-app/dedicated-ip, checked 2026-07-29) states that the public-IP feature "leverages the Kubernetes Load Balancer feature" and documents **no annotations at all**. The annotation pair below is field knowledge from an Arvan CaaS cluster, recorded in this skill since the 2026-02-15 verification snapshot and not re-observed since. **An undocumented vendor annotation can change without notice; verify it against the cluster before relying on it.**

| Mode | What to emit | When it is right |
|---|---|---|
| `internal` | `Service` of type `ClusterIP` | in-cluster traffic only; `ClusterIP` solves nothing for external users |
| `public-ip` | `Service` of type `LoadBalancer` plus the annotations below | a stable public HTTP or HTTPS endpoint, and the cluster already uses this pattern |
| `ingress` | `Service` of type `ClusterIP` plus an `Ingress` | the cluster has an ingress controller and the panel is not managing the entry point |

The observed public-IP pattern:

```yaml
service:
  type: LoadBalancer
  annotations:
    arvancloud.ir/domain: <app-domain>
    # only where the cluster allocates IPs from a MetalLB pool
    metallb.universe.tf/ip-allocated-from-pool: <pool-name>
```

**The observable test for which mode the cluster already uses**, because "when the cluster already uses that pattern" is not otherwise checkable:

```bash
kubectl -n NS get svc -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.type}{"\t"}{.metadata.annotations}{"\n"}{end}'
```

If any existing Service is `LoadBalancer` and carries `arvancloud.ir/domain`, follow the public-IP pattern. If none does and the panel shows no dedicated IP for the app, use ingress mode. If neither is available, use internal mode and say in the deliverable that external exposure is a panel action the operator must take.

**TLS.** When Arvan terminates TLS at the edge, keep in-cluster Service and Ingress traffic on HTTP and disable chart-managed TLS. Turn chart TLS on only when a real in-cluster certificate flow exists, and name the issuer.

**Domains** depend on Arvan CDN-managed DNS and an active CDN for the domain (https://docs.arvancloud.ir/en/cloud-container/manage-app/domain). A custom domain that is not on Arvan's DNS does not resolve to the app regardless of what the manifest says.

## 5. Namespace scope

**Derived from the vendored spec**, and stable across both lines because it is a tenancy decision rather than a version artefact.

- The target namespace already exists. Do not emit `Namespace`, do not pass `--create-namespace`, and do not make a deployment depend on `kubectl get namespace` succeeding: a namespace-scoped identity can be forbidden from reading the Namespace object while being able to perform every namespaced operation it needs.
- Use `Role` and `RoleBinding`. `ClusterRole` and `ClusterRoleBinding` are unavailable to a tenant.
- Which other kinds exist is line-dependent; `references/arvan-capability-matrix.md` holds both columns.

## 6. Panel behaviour

**Plausible, from Arvan's manifest page.** The panel accepts a multi-document YAML stream separated by `---`, which is why a chart's rendered output can be pasted directly. Nothing about the panel changes what a manifest must contain.

## 7. Config mount safety

**Generic Kubernetes, stated here because the failure is common on this platform.** Mount a Secret or ConfigMap into a dedicated directory such as `/etc/APP/config`. Mounting onto a directory the image already populates replaces its entire contents, and the application fails at startup with an error that names a missing file rather than the mount. The rule itself is owned by `/alaa-k8s-helm` (`$alaa-k8s-helm`) `references/kubernetes-resource-patterns.md`.

## 8. Node affinity for CPU generation

**Unverified.** Selecting a CPU generation may require a node-affinity label, and `cloud-container-g2` and `g3` have been named as families. **No label key is known, and no Arvan page documents one.** Do not emit an affinity block for this from memory. Discover the key first:

```bash
kubectl get nodes --show-labels                       # when nodes are listable
kubectl -n NS get pod -o jsonpath='{.items[0].spec.nodeSelector}'   # what existing workloads use
```

If neither returns a key, say in the deliverable that CPU-generation pinning could not be expressed, and leave `affinityPreset.cpuGeneration` off.

## 9. Portability toggles

A chart that must work on Arvan and on stock Kubernetes carries exactly these switches, each with a safe default:

| Toggle | Default | Meaning |
|---|---|---|
| `exposureMode` | `internal` | one of `public-ip`, `ingress`, `internal`, per section 4 |
| `hpa.enabled` | `false` | must stay `false` for any workload with a PVC, per section 2 |
| `ingress.enabled` / `route.enabled` | `false` | mutually exclusive; render at most one |
| `openshift.enabled` | `false` | Arvan is not OpenShift; this exists for portability only |
| `affinityPreset.cpuGeneration` | off | per section 8 |
| `privateRegistry.create` / `privateRegistry.existingSecretName` | `create: true` | create the pull Secret from values, or reference one the platform already holds; never both |

## 10. Secrets

The handling rule is generic and is owned by `/alaa-k8s-helm` (`$alaa-k8s-helm`); the fail-closed doctrine is owned by `/alaa-security-review` (`$alaa-security-review`). What is specific here is the artifact this skill's own workflow produces: `scripts/render-helm.sh` writes a file containing every rendered `Secret`, creates it with mode 0600, and deletes it on exit unless `--keep` is passed. Every filename that can hold one — `rendered.yaml`, `*.rendered.yaml`, `values.secret.yaml`, `*.secret.yaml`, `*.secrets.yaml` — belongs in the consuming repository's ignore rules before the first render. `assets/values.secret.yaml.example` carries the list.

## 11. Failure map for delivery on Arvan

Symptom to first hypothesis. The full symptom-keyed procedure is in `references/arvan-execution-loop.md`.

| Symptom | First hypothesis |
|---|---|
| pull or auth failure in a GitLab Runner job | executor job pod pull-secret configuration, which `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) owns |
| Helm render failure | chart path or an unbuilt dependency |
| `forbidden` on a namespaced call while the Helm release looks healthy | alias-versus-canonical namespace identity; read `references/arvan-rbac-namespace-facts.md` before changing any RoleBinding |
| admission denial on create | a container without resources, or `requests` not equal to `limits` |
| a kind is rejected as unknown | the discovered line does not serve it; re-read `references/arvan-capability-matrix.md` |
