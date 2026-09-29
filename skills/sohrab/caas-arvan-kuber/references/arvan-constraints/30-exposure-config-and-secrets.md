# Arvan constraints: Exposure Config And Secrets

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

## 7. Config mount safety

**Generic Kubernetes, stated here because the failure is common on this platform.** Mount a Secret or ConfigMap into a dedicated directory such as `/etc/APP/config`. Mounting onto a directory the image already populates replaces its entire contents, and the application fails at startup with an error that names a missing file rather than the mount. The rule itself is owned by `/alaa-k8s-helm` `references/kubernetes-resource-patterns.md`.

### File mode of a projected Secret or ConfigMap read by a non-root process

**Generic OpenShift-versus-non-OpenShift portability, stated here only because Arvan documents no SCC-style `fsGroup` injection.** It is not an Arvan-only fact. `/alaa-k8s-helm` `references/openshift-and-managed-platforms.md` owns the mechanics: who owns a projected file, when its GID follows `fsGroup`, and which platforms inject one.

**Rule, for every chart that renders to Arvan and sets no Pod `fsGroup`, including a chart also targeting OpenShift or OKD that must not fix one:** give each projected file a non-root process reads mode `0444`, through `defaultMode` or a per-item `mode`. `0444` is the safe default whether or not Arvan injects an `fsGroup`. Use `0440` or `0400` only when the Pod sets `fsGroup` or discovery shows the platform injects one. Reason: without an `fsGroup`, a non-root process outside GID 0 reads the file only through the other-read bit, so a `0440` that works on OpenShift through its injected `fsGroup` fails on Arvan at startup with `permission denied`.

**Unverified: Arvan injects no `fsGroup`.** Arvan documents no admission mutation of `runAsUser`, `fsGroup`, or any other securityContext field, and names no Pod Security level (docs.arvancloud.ir searched 2026-09-29). That absence is not proof. Discovery, on a running Pod of the release:

```bash
kubectl -n NS get pod POD -o jsonpath='{.spec.securityContext}'   # admitted fsGroup and runAsUser, injected or not
kubectl -n NS exec POD -- id                                      # process UID, primary GID, supplementary groups
kubectl -n NS exec POD -- ls -lnL /etc/APP/config                 # numeric owner, group, and mode behind the ..data symlinks
```

An `fsGroup` in the admitted spec that the chart did not set is an injection: report it in the deliverable as observed, with the date, for the skill maintainer to record. When `exec` is forbidden, report readability as unverified rather than inferring it.

## 10. Secrets

The handling rule is generic and is owned by `/alaa-k8s-helm`; the fail-closed doctrine is owned by `/alaa-security-review`. What is specific here is the artifact this skill's own workflow produces: `scripts/render-helm.sh` writes a file containing every rendered `Secret`, creates it with mode 0600, and deletes it on exit unless `--keep` is passed. Every filename that can hold one — `rendered.yaml`, `*.rendered.yaml`, `values.secret.yaml`, `*.secret.yaml`, `*.secrets.yaml` — belongs in the consuming repository's ignore rules before the first render. `$SKILL_DIR/assets/values.secret.yaml.example` carries the list.



Provenance and source dates: [SOURCES.md](../SOURCES.md).
