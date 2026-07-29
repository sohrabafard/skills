# The Kubernetes and Helm Delivery Gate Register

This file is the register. For each gate it states the **predicate** it asserts, the **command** that evaluates it, and the **artifact** the command inspects. It decides which checks must pass before a Kubernetes or Helm change is applied; it writes no `.gitlab-ci.yml`, no other provider YAML, and no Dockerfile.

- `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) owns how each gate below is placed on a runner and decides no gate.
- `/alaa-docker-production` (`$alaa-docker-production`) owns how the image a chart references is built and hardened, and decides no gate.
- `/alaa-makefile` (`$alaa-makefile`) owns making a local Make target return the same verdict as the runner for the same gate.
- `/caas-arvan-kuber` (`$caas-arvan-kuber`) contributes Arvan-only predicates to this register and owns no gate placement.
- `/alaa-testing-strategy` (`$alaa-testing-strategy`) decides what a chart test must assert. This register decides only that the test exists, is packaged, and runs.

## How to use the register

Run gates in the listed order: each one is cheaper than the one after it and its failures explain theirs. A gate marked **mandatory** blocks the change. A gate marked **conditional** blocks the change when its stated condition holds and is skipped, with the skip named in the report, otherwise.

Report-only mode applies when the user said validate, lint, audit, or review; fix mode applies when the user said repair, refactor, generate, or patch. Both run the same gates.

## The register

| # | Gate | Predicate | Command | Artifact | Level |
|---|---|---|---|---|---|
| 0 | Tooling present | Every tool the lane needs is on `PATH` | `bash scripts/check_tools.sh helm` (or `yaml`, `debug`, `all`) | the machine | mandatory |
| 1 | Chart structure | `Chart.yaml`, `values.yaml`, and `templates/` exist; `Chart.yaml` declares `apiVersion: v2`, a name, and a version; `values.schema.json` parses | `bash scripts/validate_chart_structure.sh CHART` | chart directory | mandatory for charts |
| 2 | YAML syntax and style | The file parses and obeys the shared style rules | `yamllint -c assets/.yamllint FILE` | raw YAML, and rendered output; never Helm templates, which are not YAML until rendered | mandatory |
| 3 | Resource classification | Every document's `apiVersion` is classified as Kubernetes, OpenShift, or custom, and no document failed to parse | `bash scripts/detect_crd_wrapper.sh FILE` | raw or rendered YAML | mandatory |
| 4 | Dependency sanity | Every dependency in `Chart.yaml` resolves and is locked | `helm dependency list CHART` then `helm dependency build CHART` | chart directory | conditional: the chart declares dependencies |
| 5 | Chart lint | Helm's own template and metadata checks pass with no error | `helm lint CHART -f values.yaml` | chart directory | mandatory for charts |
| 6 | Render | The chart renders with default values and with each realistic override set | `helm template REL CHART -f values.yaml > rendered.yaml` | chart directory to rendered YAML | mandatory for charts |
| 7 | Schema validation | Every document validates against the API schema for the target minor | `kubeconform -strict -summary -kubernetes-version 1.36.0 rendered.yaml` | rendered or raw YAML | mandatory |
| 8 | Skill rules | No container omits `resources`; no workload container omits a `readinessProbe`; the security baseline holds; no host-level field is set; every Service `targetPort` resolves | `python3 scripts/check_manifests.py rendered.yaml` | rendered or raw YAML | mandatory |
| 9 | Upgrade identity | No `spec.selector` and no `volumeClaimTemplates[].metadata.name` changed against the currently deployed release | `python3 scripts/check_manifests.py new.yaml --baseline current.yaml` | two rendered YAML sets | mandatory when a release already exists |
| 10 | Server dry-run | Admission, webhooks, quota, and unknown fields accept the manifest on the real cluster | `kubectl apply --dry-run=server -f rendered.yaml` | rendered YAML against the live API | mandatory when API access exists |
| 11 | Diff | The change set against the live cluster is the change set intended | `kubectl diff -f rendered.yaml`, or `helm diff upgrade REL CHART -f values-prod.yaml` when the plugin is installed | rendered YAML against live objects | conditional: read access to the target namespace |
| 12 | Permission | The identity that will apply the change can create or patch every kind in it | `kubectl auth can-i create deployment -n NS`, and the exact verb for each sensitive kind, for example `oc auth can-i use scc/anyuid -n NS` | RBAC on the target | mandatory |
| 13 | Chart tests packaged | `templates/tests/` survives `helm package` and the test runs | `helm package CHART` then `tar tzf CHART-VERSION.tgz \| grep templates/tests/`, then `helm test REL` after install | packaged chart | conditional: the chart ships tests |
| 14 | Version drift | The version claims in this skill still match the vendors' pages | `python3 scripts/check_versions.py` | `references/version-awareness.md` | conditional: the answer depends on a version |

### Gate 7, when a schema is missing

`kubeconform -ignore-missing-schemas` turns an unvalidated document into a pass, so it is not a substitute for validation. When a schema is missing:

1. Fetch the CRD from the cluster: `kubectl get crd NAME -o json`.
2. Extract `spec.versions[].schema.openAPIV3Schema` into a schema directory and pass it with `-schema-location`.
3. Only when no cluster is reachable may the resource be reported as unvalidated, and the report must name the kind and say the gate was skipped.

A successful kubeconform pass never proves semantic correctness for a CRD. Identify the owning operator and check the `spec` shape against its documentation.

### Gate 10, why server-side and not client-side

Server-side dry-run evaluates admission plugins, validating and mutating webhooks, quota, and unknown-field rejection against the cluster that will receive the object. Client-side dry-run evaluates none of these. When only client-side is available, say so in the report; do not describe the manifest as validated.

### Gate 12, verbs that need an exact check

`create route`, `use scc/NAME`, `create pvc`, `create rolebinding`, `create clusterrole`, and `create customresourcedefinition` fail for identities that can create Deployments. Check each one that the change needs.

## Release-risk review

Gates catch what a machine can assert. Read the diff for these as well, because no shipped checker asserts them:

- Service port changes that break an Ingress or Route backend reference
- renamed resources that leave orphans behind
- deleted hooks or tests that previously guarded rollout behaviour
- default value changes that alter exposure or security posture
- PDB, `maxUnavailable`, and `maxSurge` combinations that cannot make progress — `references/failure-and-load.md` gives the arithmetic
- PVCs that cannot bind in the target storage class
- probes that will flap under the application's real startup time
- Services whose selector matches no Pod
- changes that require cluster-scoped dependencies the applying identity cannot create

## OpenShift and custom resources

When the group ends with `.openshift.io`, validate against platform expectations rather than generic Kubernetes rules, and read `references/openshift-and-managed-platforms.md`. Common groups: `route.openshift.io/v1`, `security.openshift.io/v1`, `image.openshift.io/v1`, `build.openshift.io/v1`, `project.openshift.io/v1`, `operator.openshift.io/v1`, `config.openshift.io/v1`.

## Report format

### 1. Validation summary
Target type and path, version surface, access surface, gates run, gates skipped and the condition that caused each skip.

### 2. Blocking errors
Anything that prevents render, admission, or likely startup. Cite the gate number.

### 3. Deployment risks
Anything that passes the gates but can break rollout, traffic, persistence, or upgrade. Cite the gate number or "release-risk review".

### 4. Best-practice gaps
Security, portability, and maintainability gaps that are not immediate blockers.

### 5. Exact next actions
The next command or patch that confirms the diagnosis or resolves the issue with the least risk.
