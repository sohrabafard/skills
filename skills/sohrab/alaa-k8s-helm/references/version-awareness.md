# Version Awareness

This is the only file in the skill that contains a version number. Every other file points here. When a number below disagrees with the target cluster, the cluster wins.

## Rules that do not rot

These outlive any snapshot. Apply them before reading the pinned values.

1. **Kubernetes supports the three most recent minor releases.** Each minor gets roughly one year of patch support. Anything older than the third-newest minor receives no upstream patches, including security patches.
   Re-derive: https://kubernetes.io/releases/
2. **Version skew, relative to `kube-apiserver`.** `kubectl` is supported within one minor older or newer. `kubelet` and `kube-proxy` may be up to three minors older and must never be newer (two minors for pre-1.25 components). `kube-controller-manager`, `kube-scheduler`, and `cloud-controller-manager` may be one minor older and must never be newer. In an HA control plane, `kube-apiserver` instances must be within one minor of each other, which narrows every other window.
   Re-derive: https://kubernetes.io/releases/version-skew-policy/
   **What to conclude from `kubectl version`:** if the client minor is more than one away from the server minor, stop and say so before emitting YAML, because client-side schema validation and `kubectl diff` will disagree with the server.
3. **Helm compatibility is `n-3` against the Kubernetes client libraries the binary was compiled against**, not against a frozen table. Read the release note of the Helm version in use to learn which client-library minor it carries, then subtract three.
   Re-derive: https://helm.sh/docs/topics/version_skew/ and the release note at https://github.com/helm/helm/releases
4. **Helm does not guarantee forward compatibility.** Running Helm against a Kubernetes minor newer than the client libraries it was compiled against is unsupported; upgrade Helm rather than assuming it works.
5. **An `apiVersion` is available only when the target serves it.** `kubectl api-versions` is the authority; a schema bundle is not.

## Pinned values, verified 2026-07-29

Re-derive all of these with `python3 scripts/check_versions.py`. Each row names the command or URL that regenerates it.

| Value | As of 2026-07-29 | Re-derive with |
|---|---|---|
| Latest Kubernetes minor | 1.36 (latest patch 1.36.2, released 2026-06-09) | https://kubernetes.io/releases/ |
| Supported Kubernetes minors | 1.36 (EOL 2027-06-28), 1.35 (EOL 2027-02-28), 1.34 (EOL 2026-10-27) | https://kubernetes.io/releases/ |
| Kubernetes minors that are end of life | 1.33 and older; 1.33 reached EOL 2026-06-28 | https://kubernetes.io/releases/ |
| Current Helm major | 4; latest 4.2.0, released 2026-05-14, compiled against Kubernetes client libraries v1.36 | https://github.com/helm/helm/releases |
| Helm 4.2.0 Kubernetes band | 1.36 through 1.33, by the `n-3` rule above | rule 3 plus the 4.2.0 release note |
| Latest Helm 3 | 3.21.0, released 2026-05-14 | https://github.com/helm/helm/releases |
| Helm 3 end of life | **2027-02-10**. Bug fixes stop at the final 3.x feature release on 2026-09-09; only security fixes are issued between 2026-09-09 and 2027-02-10; Kubernetes client-library updates are not backported during that window; after 2027-02-10 there are no further 3.x releases of any kind | https://helm.sh/blog/helm-v3-end-of-life/ |
| Current OpenShift line | 4.22 | https://docs.redhat.com/en/documentation/openshift_container_platform/ |
| OpenShift 4.22 Kubernetes version | 1.35, per the release-highlight write-ups; Red Hat's own 4.22 release-notes page did not render this pairing on 2026-07-29, so confirm it against the cluster with `oc version` before relying on it | `oc version` on the target |

### What this means for authoring

- **Default Kubernetes band: 1.34 through 1.36.** Emit only API versions served across all three unless the target cluster is known.
- **Default OpenShift band: 4.20 through 4.22**, or state it as "the three most recent OCP minors" and re-derive.
- **Chart API is `v2`.** Chart API `v1` is Helm 2 shaped and is not emitted.
- **Charts stay installable on both Helm 3.21+ and Helm 4** until 2027-02-10. After that date, target Helm 4 only and say so in the chart's README, because Helm 3 receives no Kubernetes client-library patches after 2026-09-09 and no releases at all after 2027-02-10.

### Helm flag names that changed between 3 and 4

`--atomic` was renamed to `--rollback-on-failure` in Helm 4. Helm 4 keeps the legacy `--atomic` binding on `helm upgrade` with a deprecation warning and **removed it from `helm install`**, so `helm install --atomic` fails with an unknown-flag error on Helm 4, and `helm upgrade --rollback-on-failure` fails on Helm 3. Any command a skill or template emits selects the flag from the detected major:

```bash
if helm version --template '{{.Version}}' | grep -q '^v4'; then rb=--rollback-on-failure; else rb=--atomic; fi
```

## API deprecations and removals this skill must know

Re-derive the whole table: https://kubernetes.io/docs/reference/using-api/deprecation-guide/

| API version | Status | Replacement |
|---|---|---|
| `policy/v1beta1` PodSecurityPolicy | **Removed in 1.25** | Pod Security Admission namespace labels; see `references/openshift-and-managed-platforms.md` |
| `autoscaling/v2beta2` HorizontalPodAutoscaler | **Removed in 1.26** | `autoscaling/v2` |
| `flowcontrol.apiserver.k8s.io/v1beta3` | **Removed in 1.32** | `flowcontrol.apiserver.k8s.io/v1` |
| Service `.spec.externalIPs` | **Deprecated and being removed from 1.36**, because the field trusts every cluster user (CVE-2020-8554) | a `LoadBalancer` Service, or Ingress or Gateway API; enable the `DenyServiceExternalIPs` admission plugin to block new use |
| `autoscaling/v2`, `policy/v1`, `networking.k8s.io/v1`, `rbac.authorization.k8s.io/v1`, `gateway.networking.k8s.io/v1` | Current and not deprecated as of 2026-07-29 | none needed |

## Feature gating

### Safe to emit when the cluster serves them

- Chart API `v2`, `values.schema.json`, OCI chart distribution
- `kubectl debug` for ephemeral-container workflows
- `VolumeAttributesClass`: GA since 1.34, and only when the CSI driver supports it. Confirm with `kubectl get volumeattributesclass` and the driver's own documentation.
- Gateway API: only when `kubectl api-resources --api-group=gateway.networking.k8s.io` returns rows. Note that several experimental route kinds still live in `gateway.networking.k8s.io/v1alpha2`, which `scripts/detect_crd.py` classifies as custom.
- Dynamic Resource Allocation `resource.k8s.io/v1`: GA since 1.34.

### Do not emit without an explicit statement from the user

- Helm 4-only template functions in an estate that still runs Helm 3
- alpha feature gates of any kind, including configurable HPA tolerance
- cluster-specific Gateway filters or vendor extensions

## Check sequence before version-sensitive advice

Run the smallest set that answers the question.

```bash
helm version
kubectl version --output=yaml
oc version
kubectl api-versions | grep -E 'gateway.networking.k8s.io|route.openshift.io|security.openshift.io'
python3 scripts/check_versions.py
```

`scripts/check_versions.py` compares the "Pinned values" table above against the vendors' own pages and exits `1` when they have moved apart, so the drift is a finding rather than a discovery. When the network is unavailable it exits `2`, which is not a clean verdict.
