# Authoring Workflows

## Contents

- Choose the right packaging surface
- Gather requirements before writing YAML
- Helm chart workflow
- Raw manifest workflow
- Converting raw YAML to Helm
- OpenShift-safe authoring defaults
- Delivery checklist

## Choose the right packaging surface

Use the smallest deployment surface that fits the job.

- **Raw YAML**: best for a single environment, a small number of objects, or platform-owned manifests where reuse is low.
- **Helm application chart**: best when the user needs repeatable installs, environment overrides, optional features, upgrade management, or distribution.
- **Helm library chart**: best when several charts need to share helpers, labels, naming logic, or reusable partial templates.

Do not force Helm onto a tiny one-off manifest unless the user asked for packaging or reuse.

## Gather requirements before writing anything

Collect these inputs first. Missing one of them usually creates low-quality manifests.

- runtime image, command, and exposed ports
- persistent vs ephemeral data needs
- expected replica behavior and disruption tolerance
- internal-only vs external exposure
- secrets and config sources
- identity and RBAC needs
- scaling signals and limits
- target platform: vanilla Kubernetes, OpenShift, or managed namespace platform
- access level: cluster-admin, namespace admin, developer, or container-only
- cluster version or minimum supported version

If the user did not provide details, make the smallest safe assumptions and state them briefly in the output.

## Helm chart workflow

### 1. Confirm version and compatibility targets

Before using Helm-specific features, detect the actual client and cluster surface.

Recommended checks:

```bash
helm version
kubectl version --output=yaml
oc version
kubectl api-versions | rg 'gateway.networking.k8s.io|route.openshift.io'
```

Default chart target:

- Chart API: `apiVersion: v2`
- Helm runtime compatibility: prefer Helm 3.20+ and Helm 4 compatibility unless the user explicitly wants Helm 4-only behavior
- Kubernetes API compatibility: prefer stable APIs that work on Kubernetes 1.33–1.35 and OpenShift 4.19–4.21

### 2. Start with a clean chart skeleton

A production-ready application chart normally includes:

- `Chart.yaml`
- `values.yaml`
- `values.schema.json`
- `templates/_helpers.tpl`
- workload template(s)
- Service template when traffic is needed
- optional PDB, HPA, Ingress, Route, PVC, ServiceAccount, RBAC, NetworkPolicy
- `templates/NOTES.txt` only when it adds real operational value
- `.helmignore`

Use these bundled assets when helpful:

- `assets/.helmignore`
- `assets/_helpers-template.tpl`
- `assets/values-schema-template.json`

### 3. Model values deliberately

Prefer values that reflect operational decisions, not every raw field in the Kubernetes API.

Good values design principles:

- keep selectors and identity fields stable and mostly unconfigurable
- expose replica count, image, resources, probes, service ports, storage size, routing, and feature flags
- use nested groups for related areas such as `image`, `service`, `ingress`, `route`, `persistence`, `resources`, `autoscaling`
- add `values.schema.json` early so bad input fails fast
- avoid dozens of microscopic booleans when one structured object would be clearer

### 4. Template the workload first

Start with the controller that matches the workload.

- **Deployment**: stateless applications, web services, APIs, workers without stable identity
- **StatefulSet**: stable network identity, ordinal identity, or persistent per-replica data
- **DaemonSet**: node-local agents such as log shippers, CNIs, or node exporters
- **Job / CronJob**: finite or scheduled work
- **Pod**: only for debug, tutorials, or tightly controlled one-offs

Workload template defaults that should almost always exist:

- recommended labels
- stable selectors
- resource requests and limits unless the user explicitly rejects them
- readiness and liveness probes where applicable
- startup probe for slow-starting apps
- non-root security context by default
- named container ports
- `terminationGracePeriodSeconds` appropriate to the app
- checksum annotations for config or secret-driven rollouts when relevant

### 5. Add exposure and supporting resources only when justified

Typical order:

1. Service
2. Ingress, Gateway API, or Route if external access is required
3. PVC if durable data is required
4. ServiceAccount and RBAC if the workload talks to the API or cloud identities
5. PDB for high-availability workloads
6. HPA only when the scaling signal is understood
7. NetworkPolicy when the traffic contract is known

Do not add HPA, PDB, or NetworkPolicy blindly. Add them when the workload semantics support them.

### 6. Make charts upgrade-safe

Upgrade safety matters more than template cleverness.

- preserve immutable selectors
- avoid renaming resources without a migration plan
- keep PVC names and StatefulSet identity stable
- separate install-time hooks from steady-state resources
- use chart tests for smoke checks, not full integration suites
- keep default values conservative
- prefer OCI distribution unless the user is locked into classic repositories

### 7. Validate before delivery

Read `references/validation-workflows.md` and run the relevant flow before final delivery.

## Raw manifest workflow

Use this when Helm is unnecessary.

### 1. Pick the controller

Use the same controller rules as the chart workflow.

### 2. Build the minimum coherent object set

Common sets:

- API or web app: Deployment + Service + optional Ingress or Route + ConfigMap/Secret + optional HPA/PDB
- queue worker: Deployment + ConfigMap/Secret + optional PDB
- stateful DB-like app: StatefulSet + headless Service + PVC + optional regular Service + optional PDB
- node agent: DaemonSet + ServiceAccount + RBAC

### 3. Keep manifests portable

- use stable API versions
- use recommended labels
- set resource requests and limits
- use probes appropriately
- prefer named ports
- avoid host-level privileges unless the platform and access level support them

### 4. If the user wants explanations

When reading existing YAML, explain it in this order:

1. what resource family it is
2. what behavior it creates
3. which fields are identity-critical or immutable
4. which fields are platform-sensitive
5. where the operational risk lives

## Converting raw YAML to Helm

Do not parameterize everything. Parameterize only the parts that vary across environments or releases.

Good candidates:

- image repository and tag
- replica count
- resources
- ports
- ingress, gateway, or route hostnames
- persistence size and storage class
- optional feature toggles
- env vars and external secret references

Usually keep fixed:

- selectors
- controller type
- label keys
- core names derived from helpers
- API versions unless platform compatibility truly requires branching

If a manifest set must work on both Kubernetes and OpenShift, prefer explicit toggles such as:

- `ingress.enabled`
- `route.enabled`
- `gateway.enabled`

Do not render both Ingress and Route by default unless the user explicitly wants parallel exposure.

## OpenShift-safe authoring defaults

When OpenShift compatibility matters, design the image and manifests for stricter admission.

- Do not assume a fixed runtime UID.
- Avoid `runAsUser` unless you know the SCC allows it and the image needs it.
- Prefer listening on ports like `8080` or `8443` inside the container; expose `80` or `443` through Service, Ingress, or Route.
- Keep writable directories owned by group `0` and make group permissions mirror user permissions in the image build.
- Avoid `privileged`, `hostPath`, `hostPID`, `hostIPC`, and `hostNetwork` unless the workload truly needs them and the user has the policy surface.
- Prefer Route objects for external HTTP or HTTPS on OpenShift when the user wants platform-native exposure.

## Delivery checklist

Before handing off generated output, confirm all of the following:

- controller choice matches the workload
- selectors are stable and correct
- Service ports line up with container ports
- resources and probes exist where appropriate
- persistence is explicit rather than accidental
- access assumptions are stated
- OpenShift-specific constraints are addressed when relevant
- validation commands are provided or already run
