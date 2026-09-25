# Version Awareness

This file owns release, support, compatibility and feature-version facts. Other files may carry API identifiers and synthetic fixture versions, but route compatibility decisions here. Target discovery outranks this snapshot; an upstream release does not prove a consumer upgrade.

## Rules that do not rot

These outlive any snapshot. Apply them before reading the pinned values.

1. **Kubernetes maintains the three most recent minor release branches.** Each minor gets roughly one year of patch support. Check the published EOL date as well as the branch list; when they disagree, record the discrepancy instead of inferring that a consumer is already unsupported.
   Re-derive: https://kubernetes.io/releases/
2. **Version skew, relative to `kube-apiserver`.** `kubectl` is supported within one minor older or newer. `kubelet` and `kube-proxy` may be up to three minors older and must never be newer (two minors for pre-1.25 components). `kube-controller-manager`, `kube-scheduler`, and `cloud-controller-manager` may be one minor older and must never be newer. In an HA control plane, `kube-apiserver` instances must be within one minor of each other, which narrows every other window.
   Re-derive: https://kubernetes.io/releases/version-skew-policy/
   **What to conclude from `kubectl version`:** if the client minor is more than one away from the server minor, stop and say so before emitting YAML, because client-side schema validation and `kubectl diff` will disagree with the server.
3. **Helm compatibility is `n-3` against the Kubernetes client libraries the binary was compiled against**, not against a frozen table. Read the exact release's compatibility documentation and tagged `go.mod` to identify that minor, then subtract three. The same chart may support more minors than one Helm binary can operate against.
   Re-derive: https://helm.sh/docs/topics/version_skew/ , https://helm.sh/docs/v3/topics/version_skew/ and the exact tag at https://github.com/helm/helm/releases
4. **Helm does not guarantee forward compatibility.** Running Helm against a Kubernetes minor newer than the client libraries it was compiled against is unsupported; upgrade Helm rather than assuming it works.
5. **An `apiVersion` is available only when the target serves it.** `kubectl api-versions` is the authority; a schema bundle is not.

## Pinned values, verified 2026-09-26

The checker compares only the latest stable Kubernetes minor, latest stable Helm release and Helm 3 EOL date. Revalidate the other rows manually from their named official sources; a clean checker does not verify this whole table. Preview tags and scheduled releases are not stable releases.

| Value | As of 2026-09-26 | Re-derive with |
|---|---|---|
| Latest Kubernetes minor | 1.37 (latest stable patch listed: 1.37.0, released 2026-08-26) | https://kubernetes.io/releases/ and https://kubernetes.io/releases/1.37/ |
| Maintained Kubernetes branches | 1.37, 1.36, 1.35; listed patches 1.37.0, 1.36.4, 1.35.8 | https://kubernetes.io/releases/ |
| Kubernetes 1.34 compatibility branch | The release page lists EOL 2026-10-27, although its latest-three maintained-branch list omits this minor. Preserve the authoring floor below; do not infer an earlier EOL from that omission | https://kubernetes.io/releases/ |
| Current Helm major | 4; latest 4.3.0, compiled against Kubernetes client libraries v1.37 (`k8s.io/client-go v0.37.0`) | https://github.com/helm/helm/releases/tag/v4.3.0 and https://raw.githubusercontent.com/helm/helm/v4.3.0/go.mod |
| Helm 4.3.0 Kubernetes band | 1.34 through 1.37 | https://helm.sh/docs/topics/version_skew/ and rule 3 |
| Latest Helm 3 | 3.22.0; client libraries v1.37 (`k8s.io/client-go v0.37.0`), Kubernetes band 1.34 through 1.37 | https://github.com/helm/helm/releases/tag/v3.22.0 and https://raw.githubusercontent.com/helm/helm/v3.22.0/go.mod |
| Earlier Helm compatibility path | Helm 3.21.x and 4.2.x target Kubernetes 1.33 through 1.36; the observed 4.2.3 tag carries `k8s.io/client-go v0.36.1`. Do not claim support for a newer Kubernetes minor from chart rendering alone | https://helm.sh/docs/v3/topics/version_skew/ , https://helm.sh/docs/topics/version_skew/ and https://raw.githubusercontent.com/helm/helm/v4.2.3/go.mod |
| Helm 3 end of life | **2027-02-10**. The final minor, 3.22 on 2026-09-09, is limited to Kubernetes client-library updates. Subsequent maintenance is security-only until EOL, without further client-library updates; after EOL no further 3.x releases are planned | https://helm.sh/blog/helm-v3-end-of-life/ |

### Historical OpenShift snapshot, not revalidated in this refresh

The 2026-07-29 snapshot named OCP 4.22 and an authoring band of 4.20 through 4.22. Its proposed pairing of OCP 4.22 with Kubernetes 1.35 was not confirmed by Red Hat's release-notes page. Keep that compatibility path where consumers require it, but do not describe it as the current upstream line. Confirm the target with `oc version` and its versioned documentation at https://docs.redhat.com/en/documentation/openshift_container_platform/ before relying on a pairing or selecting a different band.

### What this means for authoring

- **Default Kubernetes authoring band: 1.34 through 1.37.** Keep the existing 1.34 floor; emit only APIs and fields available throughout this band unless the target is known. A feature available only on a newer minor needs an explicit version condition. Upstream maintenance policy does not change a chart's consumer compatibility floor.
- **Known older consumers retain their explicit version path.** Validate against their actual served APIs and matching Helm binary; report upstream support separately. For Arvan platform facts, `/caas-arvan-kuber` owns the platform-specific decision. Unknown consumer versions remain unknown.
- **OpenShift compatibility follows the historical caveat above and target evidence.** A newly published OCP minor does not remove existing consumer support.
- **Chart API is `v2`.** Chart API `v1` is Helm 2 shaped and is not emitted.
- **Preserve charts' Helm 3.21+ and Helm 4 compatibility paths.** Choose a Helm build whose Kubernetes band includes the target. EOL calls for a migration decision, not automatic consumer-support removal; a breaking support change needs explicit approval and a documented migration path.
- **Separate proof levels.** Record the intended chart range, each installed client version, upstream support and actual consumer/server evidence separately. Lint or template with one Helm build proves neither another build nor cluster admission. Report missing version coverage; do not install or upgrade tools implicitly.

### Helm flag names that changed between 3 and 4

Use `--atomic` with Helm 3 and `--rollback-on-failure` with Helm 4. Tagged Helm 4.2.3 and 4.3.0 sources retain `--atomic` as a deprecated alias on both install and upgrade; generated help may hide it. Helm 3 does not accept `--rollback-on-failure`. Select the preferred flag from a successfully detected major and stop on an unknown version:

```bash
helm_version=$(helm version --template '{{.Version}}') || exit 2
case "$helm_version" in
  v3.*) rb=--atomic ;;
  v4.*) rb=--rollback-on-failure ;;
  *) printf 'Unsupported Helm version: %s\n' "$helm_version" >&2; exit 2 ;;
esac
```

Verified 2026-09-26 against https://raw.githubusercontent.com/helm/helm/v4.2.3/pkg/cmd/install.go , https://raw.githubusercontent.com/helm/helm/v4.3.0/pkg/cmd/install.go , https://raw.githubusercontent.com/helm/helm/v4.3.0/pkg/cmd/upgrade.go and https://docs.helm.sh/docs/v3/helm/helm_upgrade/ .

## API deprecations and removals this skill must know

Re-derive the whole table: https://kubernetes.io/docs/reference/using-api/deprecation-guide/

| API version | Status | Replacement |
|---|---|---|
| `policy/v1beta1` PodSecurityPolicy | **Removed in 1.25** | Pod Security Admission namespace labels; see `references/openshift-and-managed-platforms.md` |
| `autoscaling/v2beta2` HorizontalPodAutoscaler | **Removed in 1.26** | `autoscaling/v2` |
| `flowcontrol.apiserver.k8s.io/v1beta3` | **Removed in 1.32** | `flowcontrol.apiserver.k8s.io/v1` |
| Service `.spec.externalIPs` | **Deprecated in 1.36, not removed there.** Announced kube-proxy disablement is no earlier than 1.40 and full disablement no earlier than 1.43; these are earliest plans, not observed removals. The security rejection remains because of CVE-2020-8554 | a `LoadBalancer` Service, or Ingress or Gateway API; a cluster administrator can enable `DenyServiceExternalIPs` to block new use |
| `autoscaling/v2`, `policy/v1`, `networking.k8s.io/v1`, `rbac.authorization.k8s.io/v1` | Stable APIs retained across the authoring band; target discovery still decides availability | none needed |
| `gateway.networking.k8s.io/v1` | Separately installed Gateway API, not guaranteed by a Kubernetes minor | verify installed CRDs and controller support |

The externalIPs timeline was verified 2026-09-26 at https://kubernetes.io/blog/2026/05/14/kubernetes-v1-36-deprecation-and-removal-of-service-externalips/ .

## Feature gating

### Safe to emit when the cluster serves them

- Chart API `v2`, `values.schema.json`, OCI chart distribution
- `kubectl debug` for ephemeral-container workflows
- `VolumeAttributesClass`: GA since 1.34; its feature gate could still be disabled in 1.34-1.35 and is locked on from 1.36. Emit only when the target serves it and the CSI driver supports it. Confirm with `kubectl get volumeattributesclass` and the driver's own documentation. The GA announcement and current feature-gate explanation were checked 2026-09-26: https://kubernetes.io/blog/2025/09/08/kubernetes-v1-34-volume-attributes-class/ and https://kubernetes.io/docs/concepts/storage/volume-attributes-classes/ .
- Gateway API: only when `kubectl api-resources --api-group=gateway.networking.k8s.io` returns rows. Note that several experimental route kinds still live in `gateway.networking.k8s.io/v1alpha2`, which `scripts/detect_crd.py` classifies as custom.
- Dynamic Resource Allocation `resource.k8s.io/v1`: GA since 1.34.

### Do not emit without an explicit statement from the user

- Helm 4-only template functions in an estate that still runs Helm 3
- alpha feature gates of any kind
- configurable HPA tolerance: stable since 1.37 and first available in 1.33, per https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/#tolerance (verified 2026-09-26). On older targets, verify that minor's feature stage, `HPAConfigurableTolerance` gate and served field before emitting it; do not assume it works throughout the default band
- cluster-specific Gateway filters or vendor extensions

## Check sequence before version-sensitive advice

Run the smallest authorized set that answers the question. For offline authoring or prohibited cluster access, use supplied target evidence and local client versions, mark server/API evidence unknown, and do not run discovery commands:

```bash
helm version
kubectl version --client --output=yaml
python3 scripts/check_versions.py
```

When target API access is authorized, obtain the server and served-API evidence separately:

```bash
kubectl version --output=yaml
oc version
kubectl api-versions | grep -E 'gateway.networking.k8s.io|route.openshift.io|security.openshift.io'
```

`scripts/check_versions.py` compares the three stated fields against vendor pages: exit `0` means those fields match, `1` means drift, and `2` means unavailable evidence, including fetch or parse failure. It is read-only; resolve findings before version-sensitive advice and never turn unavailable evidence into a pass. `--self-test` uses fixed synthetic fixtures, not live release evidence.
