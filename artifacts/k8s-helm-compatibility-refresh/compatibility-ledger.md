# Compatibility ledger

Observed 2026-09-26 by the read-only research lane and lead. Upstream claims below
are separate from installed binaries, actual consumers and this skill's authoring
policy. No cluster discovery, installation or consumer migration occurred.

| Surface | Previous skill snapshot | Current official evidence | Local proof | Authoring decision |
|---|---|---|---|---|
| Kubernetes | Latest 1.36.2; authoring 1.34-1.36 | Release page lists 1.37.0, 1.36.4, 1.35.8 and maintained branches 1.37/1.36/1.35 | kubectl client 1.36.1 only; consumer/server unknown | Preserve 1.34 floor and add 1.37 awareness; never infer consumer upgrades |
| Kubernetes 1.34 | Supported, EOL 2026-10-27 | Outside page's stated latest-three maintained branches, but published EOL remains 2026-10-27 | Unknown consumers | Record documentation tension; do not call it already EOL or remove compatibility |
| Helm 4 | 4.2.0 and client minor 1.36 | Stable 4.3.0; tagged client-go v0.37.0; official band 1.34-1.37 | Installed 4.2.3, tag client-go v0.36.1, band 1.33-1.36 | Version-condition command and validation guidance; runtime 4.3 coverage absent |
| Helm 3 | 3.21.0; compatibility 3.21+ | Stable 3.22.0; tagged client-go v0.37.0; band 1.34-1.37. 3.21.x band remains 1.33-1.36 | No Helm 3 binary observed | Preserve older client/consumer route; no calendar-triggered support removal |
| Helm lifecycle | Final feature release and security window wording | Final 3.22 minor limited to Kubernetes client-library updates; distinguish that final update from subsequent security-only maintenance | Not runtime proof | Explain lifecycle without granting a migration or dropping consumers |
| OpenShift | Historical 4.22 and uncertain 1.35 pairing | Not revalidated in this Kubernetes/Helm refresh | No oc command observed; target unknown | Preserve historical uncertainty and target-specific confirmation; no new release claim |

## Official source observations

- Kubernetes branches, patches and EOL: https://kubernetes.io/releases/ ; specific
  minor: https://kubernetes.io/releases/1.37/ . Latest 1.37.0 released 2026-08-26.
- Component skew: https://kubernetes.io/releases/version-skew-policy/ . Keep component
  and HA-specific bounds; a client observation does not establish server skew.
- API removals: https://kubernetes.io/docs/reference/using-api/deprecation-guide/ .
  PSP removal 1.25, HPA v2beta2 removal 1.26, flowcontrol v1beta3 removal 1.32.
- Stable versus preview Helm: https://github.com/helm/helm/releases . Stable tags
  4.3.0/3.22.0 are releases; RC entries and scheduled 4.4.0/4.3.1/3.22.1 are not
  evidence of a stable release.
- Helm bands: https://helm.sh/docs/topics/version_skew/ and
  https://helm.sh/docs/v3/topics/version_skew/ . Both majors derive n-3 from their
  compiled Kubernetes client minor, without a forward-compatibility guarantee.
- Tagged dependency evidence: https://raw.githubusercontent.com/helm/helm/v4.3.0/go.mod ,
  https://raw.githubusercontent.com/helm/helm/v3.22.0/go.mod and
  https://raw.githubusercontent.com/helm/helm/v4.2.3/go.mod .
- Lifecycle: https://helm.sh/blog/helm-v3-end-of-life/ . Security-only interval follows
  the final Kubernetes-library update minor on 2026-09-09 and ends 2027-02-10;
  dates must not become support-removal authority.
- Helm install alias: https://raw.githubusercontent.com/helm/helm/v4.2.3/pkg/cmd/install.go
  and https://raw.githubusercontent.com/helm/helm/v4.3.0/pkg/cmd/install.go register
  `atomic` as deprecated alias for `RollbackOnFailure`; it was not removed.
- Helm upgrade alias: https://raw.githubusercontent.com/helm/helm/v4.3.0/pkg/cmd/upgrade.go .
  Major-specific preferred flags remain `--atomic` for Helm 3 and
  `--rollback-on-failure` for Helm 4. Generated help hides deprecated aliases.
- Helm 3 CLI: https://docs.helm.sh/docs/v3/helm/helm_install/ and
  https://docs.helm.sh/docs/v3/helm/helm_upgrade/ .
- Service externalIPs: https://kubernetes.io/blog/2026/05/14/kubernetes-v1-36-deprecation-and-removal-of-service-externalips/ .
  Deprecated in 1.36; kube-proxy support disabled no earlier than 1.40, full disable
  no earlier than 1.43. Correct the inaccurate removal claim without weakening the
  existing security rejection predicate.
- VolumeAttributesClass: https://kubernetes.io/docs/concepts/storage/volume-attributes-classes/
  has a 1.36 stable banner while its body describes GA in 1.34 and opt-out until
  locked in 1.36. The 1.34 announcement confirms GA:
  https://kubernetes.io/blog/2025/09/08/kubernetes-v1-34-volume-attributes-class/ .
  Preserve CSI/served-API preconditions and the distinction, not a fabricated date.
- Writer's bounded follow-up confirmed configurable HPA tolerance stable since
  1.37 and first available in 1.33 at
  https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/#tolerance
  on 2026-09-26. Preserve explicit user selection and version-specific feature-gate
  and served-field confirmation on older targets.

## Demonstrated checker defects and decision

Writer reproduced with in-process calls before edits: stable Helm `v4.3.0` plus
`v4.4.0-rc.1` selects `4.4.0`; Kubernetes `1.37.1` plus `1.38.0-alpha.1` selects
`1.38`; pinned `2027-02-10` accepts `February 10th, 2028`. Repair only these
freshness correctness defects and meaningful offline regression fixtures, preserving
read-only operation and exit semantics 0/1/2. Keep fixture maintenance distinct from
live release proof. No extra script behavior change is selected.

## Preserved behavior

Namespace/RBAC/least privilege, OpenShift arbitrary UID/nonroot restrictions,
resource identity, target-served API checks, chart validation, failure handling
and generic Kubernetes versus Arvan ownership remain mandatory. Source conflicts
are recorded rather than resolved by dropping old consumer paths. Installed skill
activation, actual consumer compatibility and measured quality remain unproven.
