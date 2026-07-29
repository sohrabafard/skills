# Authoring Workflows

## Contents

- Choose the right packaging surface
- Gather requirements before writing YAML
- Helm chart workflow
- Raw manifest workflow
- Converting raw YAML to Helm
- Delivery checklist

## Choose the right packaging surface

Use the smallest deployment surface that fits the job.

- **Raw YAML**: a single environment, a small number of objects, or platform-owned manifests where reuse is low.
- **Helm application chart**: repeatable installs, environment overrides, optional features, upgrade management, or distribution.
- **Helm library chart**: several charts share helpers, labels, naming logic, or partial templates.

Do not convert a one-off manifest into a chart unless the user asked for packaging or reuse.

## Gather requirements before writing anything

Collect these first. A missing one is the usual cause of a low-quality manifest.

- runtime image, command, and exposed ports
- persistent versus ephemeral data needs
- expected replica behaviour and disruption tolerance
- internal-only versus external exposure
- secret and config sources
- identity and RBAC needs
- scaling signals and limits
- target platform: vanilla Kubernetes, OpenShift, or managed namespace platform
- access level: cluster-admin, namespace admin, developer, or container-only
- the cluster's Kubernetes minor, or the minimum minor the output must support

When the user did not provide a detail, make the smallest safe assumption, state it in the output, and name the command that would settle it.

## Helm chart workflow

### 1. Confirm the version and compatibility target

Detect the real client and cluster surface before using any version-sensitive feature.

```bash
helm version
kubectl version --output=yaml
oc version
kubectl api-versions | grep -E 'gateway.networking.k8s.io|route.openshift.io'
```

The chart API is `apiVersion: v2`. Every other version number, including the Kubernetes band, the Helm band, and the Helm 3 end-of-life date, lives in `references/version-awareness.md`.

### 2. Start with a clean chart skeleton

A production application chart normally contains:

- `Chart.yaml`
- `values.yaml`
- `values.schema.json`
- `templates/_helpers.tpl`
- one or more workload templates
- a Service template when traffic is needed
- optionally PDB, HPA, Ingress, Route, PVC, ServiceAccount, RBAC, NetworkPolicy
- `templates/tests/` when the chart ships a smoke test
- `templates/NOTES.txt` only when it carries real operational value
- `.helmignore`

Bundled starting points: `assets/.helmignore`, `assets/_helpers-template.tpl`, `assets/values-schema-template.json`, `assets/.yamllint`.

`assets/.helmignore` anchors every directory pattern to the chart root with a leading slash. Helm matches an unanchored directory pattern at any depth, so an unanchored `tests/` would strip `templates/tests/` out of the packaged chart and silently delete the smoke test the delivery checklist requires.

### 3. Model values deliberately

Values reflect operational decisions, not raw API fields.

- Keep selectors and identity fields stable and unconfigurable.
- Expose replica count, image, resources, probes, service ports, storage size, routing, and feature flags.
- Group related settings: `image`, `service`, `ingress`, `route`, `persistence`, `resources`, `autoscaling`, `securityContext`, `probes`.
- Write `values.schema.json` before the templates, so bad input fails at `helm template` rather than at admission. `assets/values-schema-template.json` requires `image` and `resources` at the root and requires `cpu` and `memory` inside both `requests` and `limits`, so a chart cannot ship resource-less containers through the schema.
- Replace a family of microscopic booleans with one structured object.

### 4. Template the workload first

Choose the controller from the workload's identity and lifetime; `references/kubernetes-resource-patterns.md` holds the full decision rules and is the only place they are stated.

Workload template defaults that must exist unless the user rejects one explicitly and in writing:

- the recommended `app.kubernetes.io/*` labels
- stable selectors
- `resources.requests` and `resources.limits` on every container
- a `readinessProbe` on every container that serves traffic
- a `startupProbe` for a slow-starting application
- the restrictive security context from `references/openshift-and-managed-platforms.md`
- named container ports
- `terminationGracePeriodSeconds` derived as `references/failure-and-load.md` describes, not copied
- a checksum annotation on config or secret content when a change to it must trigger a rollout

### 5. Add exposure and supporting resources only when justified

Typical order: Service, then Ingress or Gateway API or Route when external access is required, then PVC when durable data is required, then ServiceAccount and RBAC when the workload calls the API, then PDB for a multi-replica workload, then HPA when the scaling signal is understood, then NetworkPolicy when the traffic contract is known.

Add an HPA only when `resources.requests.cpu` is set, because HPA utilisation is a percentage of the request. Add a PDB only when replicas are at least 2. `references/failure-and-load.md` gives the arithmetic for both.

### 6. Make charts upgrade-safe

Upgrade safety outranks template cleverness.

- Preserve immutable selectors and StatefulSet volume-claim names. `scripts/check_manifests.py --baseline` asserts this.
- Do not rename a resource without stating the migration and the deletion order.
- Separate install-time hooks from steady-state resources.
- Use chart tests for smoke checks; `/alaa-testing-strategy` (`$alaa-testing-strategy`) decides what those checks must assert.
- Keep default values conservative: an unconfigured install produces a workload that starts, serves nothing publicly, and stores nothing durably.
- Distribute through an OCI registry.

### 7. Validate before delivery

Run the gates in `references/validation-workflows.md`. That file is the register, and it names which gates are mandatory for a chart.

## Raw manifest workflow

Use this when Helm adds nothing.

1. **Pick the controller** using the same rules as the chart workflow.
2. **Build the minimum coherent object set.** API or web app: Deployment, Service, optional Ingress or Route, ConfigMap or Secret, optional HPA and PDB. Queue worker: Deployment, ConfigMap or Secret, optional PDB. Stateful application: StatefulSet, headless Service, PVC, optional regular Service, optional PDB. Node agent: DaemonSet, ServiceAccount, RBAC.
3. **Keep manifests portable**: served API versions only, the recommended labels, requests and limits on every container, probes derived from measured behaviour, named ports, and none of the restricted fields listed in `references/openshift-and-managed-platforms.md`.
4. **When the user wants an explanation**, read the YAML back in this order: which resource family it is, what behaviour it creates, which fields are identity-critical or immutable, which fields are platform-sensitive, and where the operational risk lives.

## Converting raw YAML to Helm

Parameterise only what varies across environments or releases.

Good candidates: image repository and tag, replica count, resources, ports, ingress or gateway or route hostnames, persistence size and storage class, feature toggles, environment variables, and external secret references.

Keep fixed: selectors, controller type, label keys, names derived from helpers, and API versions unless platform compatibility genuinely requires a branch.

When one manifest set must work on both Kubernetes and OpenShift, use explicit toggles — `ingress.enabled`, `route.enabled`, `gateway.enabled` — and render at most one of them by default. Render two exposure objects only when the user asked for parallel exposure.

## OpenShift-safe authoring

The restricted fields, the arbitrary-UID rules, and the restrictive path are stated once, in `references/openshift-and-managed-platforms.md`. Read that file when OpenShift or any managed platform is in scope; do not restate its rules in a chart's documentation.

## Delivery checklist

Before handing off generated output, confirm all of the following:

- the controller matches the workload's identity and lifetime
- selectors are stable, and unchanged against the deployed release
- every Service `targetPort` resolves to a declared container port
- every container declares resources; every traffic-serving container declares a readiness probe
- persistence is explicit rather than accidental
- the access assumptions are stated, and each was proved with an `auth can-i` call
- the platform-specific constraints that apply were addressed and named
- the gates in `references/validation-workflows.md` were run, and their output is in the deliverable
