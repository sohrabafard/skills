# Validation Workflows

## Contents

- Principles
- Tool checks
- Raw manifest validation
- Helm chart validation
- CRDs and OpenShift resources
- Permission and rollout checks
- Report format

## Principles

Validation should move from cheapest and broadest checks to the most environment-specific checks.

Recommended order:

1. file and structure sanity
2. YAML syntax and formatting
3. schema validation
4. rendered-output validation
5. server-side dry-run
6. permission and rollout-risk review
7. upgrade-diff review when there is an existing release

Use report-only mode when the user asked to validate, lint, audit, or review. Use fix mode when the user asked to repair or refactor.

## Tool checks

Run the lane-specific tool inventory first.

```bash
bash scripts/check_tools.sh yaml
bash scripts/check_tools.sh helm
bash scripts/check_tools.sh debug
```

The script reports required and optional tools for the chosen lane and prefers `oc` when OpenShift tooling is present.

## Raw manifest validation

### Stage 1: syntax and formatting

Use the bundled yamllint config.

```bash
yamllint -c assets/.yamllint path/to/file.yaml
```

Capture all syntax errors first. They often explain downstream schema failures.

### Stage 2: detect CRDs and OpenShift resources

```bash
bash scripts/detect_crd_wrapper.sh path/to/file.yaml
```

Use the output to classify resources into:

- standard Kubernetes
- OpenShift platform resources
- custom resources from operators or CRDs

### Stage 3: schema validation

For mostly standard Kubernetes manifests:

```bash
kubeconform -strict -summary -ignore-missing-schemas path/to/file.yaml
```

Use `-ignore-missing-schemas` only when custom or platform resources are expected. Missing schemas are not proof that a manifest is valid.

### Stage 4: server-side dry-run

Prefer server-side dry-run whenever API access exists.

```bash
kubectl apply --dry-run=server -f path/to/file.yaml
oc apply --dry-run=server -f path/to/file.yaml
```

Why server-side first:

- it catches admission issues
- it catches API deprecations and unknown fields against the actual cluster
- it checks policy and webhook behavior more accurately than client-side parsing

### Stage 5: diff and permission checks

If the user has safe read access to the target namespace, use:

```bash
kubectl diff -f path/to/file.yaml
kubectl auth can-i apply -f path/to/file.yaml
oc auth can-i create deployment -n <namespace>
```

Use exact resource verbs for sensitive changes such as `create route`, `use scc/<name>`, or `create pvc`.

## Helm chart validation

### Stage 1: chart structure

```bash
bash scripts/validate_chart_structure.sh path/to/chart
```

This catches missing files, broken `Chart.yaml`, absent values, and missing helper or schema files.

### Stage 2: dependency sanity

```bash
helm dependency list path/to/chart
helm dependency build path/to/chart
```

If the chart has no dependencies, do not force them.

### Stage 3: lint the chart

```bash
helm lint path/to/chart
```

Treat lint output as follows:

- **errors**: blocking
- **warnings**: investigate; many are deployment risks rather than style nits

### Stage 4: render with representative values

Always render at least the default values and one realistic override set.

```bash
helm template release-name path/to/chart > rendered.yaml
helm template release-name path/to/chart -f values-prod.yaml > rendered-prod.yaml
```

If the chart targets OpenShift, render both the Kubernetes path and the Route-enabled or OpenShift-enabled path when those toggles exist.

### Stage 5: validate rendered output

Run the raw manifest flow on the rendered YAML.

```bash
yamllint -c assets/.yamllint rendered.yaml
kubeconform -strict -summary -ignore-missing-schemas rendered.yaml
kubectl apply --dry-run=server -f rendered.yaml
```

### Stage 6: dry-run install or upgrade

```bash
helm install release-name path/to/chart --dry-run --debug
helm upgrade --install release-name path/to/chart --dry-run --debug
```

If the `helm-diff` plugin is present and a live release already exists, use it.

```bash
helm diff upgrade release-name path/to/chart -f values-prod.yaml
```

### Stage 7: release-risk review

Explicitly check for:

- selector changes
- Service port changes
- PVC or StatefulSet identity changes
- renamed resources
- deleted hooks or tests that previously guarded rollout behavior
- default value changes that alter exposure or security

## CRDs and OpenShift resources

Schema validation is weaker for platform-specific and custom resources. When schemas are missing, switch to doc-informed validation.

### For OpenShift resources

If the group ends with `.openshift.io`, validate against platform expectations instead of assuming generic Kubernetes rules.

Common examples:

- `route.openshift.io/v1`
- `security.openshift.io/v1`
- `image.openshift.io/v1`
- `build.openshift.io/v1`
- `project.openshift.io/v1`
- `operator.openshift.io/v1`
- `config.openshift.io/v1`

Read `references/openshift-and-managed-platforms.md` when these appear.

### For operator CRDs

Identify the owning project or operator and validate the `spec` shape against its documentation or examples. A successful kubeconform pass does not prove semantic correctness for a CRD.

## Permission and rollout checks

Validation is incomplete unless you consider access and rollout semantics.

### Permission checks

Before recommending or applying a change, verify whether the user can do it.

Examples:

```bash
kubectl auth can-i create deployment -n <namespace>
kubectl auth can-i create clusterrole
oc auth can-i use scc/anyuid -n <namespace>
```

### Rollout checks

Look for these risks even when syntax is valid:

- PDB blocks and surge settings that prevent rollout progress
- PVCs that cannot bind in the target storage class
- probes that will flap under startup behavior
- Services with selectors that match no Pods
- Routes or Ingresses pointing at the wrong Service port
- changes that require cluster-scoped dependencies the user cannot create

## Report format

Use this format for report-only validation work.

### 1. Validation summary

- target type and path
- version surface
- access surface
- checks performed
- checks skipped and why

### 2. Blocking errors

Anything that prevents render, admission, or likely startup.

### 3. Deployment risks

Anything that may pass validation but break rollout, traffic, persistence, or upgrades.

### 4. Best-practice gaps

Security, portability, and maintainability gaps that are not immediate blockers.

### 5. Exact next actions

List the next command or patch that confirms the diagnosis or resolves the issue with minimal risk.
