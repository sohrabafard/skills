---
name: caas-arvan-kuber
description: "Arvan-first Kubernetes/Helm/DevOps skill for building, validating, and operating production workloads on Arvan CaaS with OpenAPI-driven decisions, namespace-safe RBAC, and portable defaults."
---

## Mission

Produce production-grade Kubernetes, Helm, and CI/CD deliverables that work correctly on Arvan CaaS first, while staying portable to standard Kubernetes with minimal toggles.

This skill is the single source of truth for Arvan work in this repository. It includes platform constraints, practical operating patterns, and RBAC identity facts.

## Source of truth and precedence

Use sources in this order:

1) `references/arvan-caas-openAPI-1.25.json` (machine-readable API baseline)
2) Live discovery from target cluster (`kubectl api-resources`, `kubectl api-versions`, `kubectl auth can-i`)
3) `references/openapi-1.25-capability-matrix.md`
4) `references/arvan-rbac-namespace-facts.md`
5) `references/arvan-constraints.md`
6) `references/arvan-links.md` (documentation map)

If sources conflict:

- OpenAPI + live discovery override generic Kubernetes memory.
- Namespace-scoped safety overrides convenience.
- Arvan-first defaults apply unless the user explicitly asks to override.

## Internet and search usage

Agents are allowed and encouraged to use internet search when it improves correctness, especially for:

1) recently changed platform behavior, APIs, or docs,
2) troubleshooting signatures and current best practices,
3) CI/CD or registry behavior that may vary by version.

Rules for web research:

- Prefer primary/official sources first (Arvan docs, Kubernetes docs, Helm docs, GitLab docs).
- Verify dates/versions and align with the local OpenAPI baseline.
- Keep citations/links in outputs when decisions depend on online findings.
- Never leak secrets while browsing or sharing commands.

## When to use this skill

Use this skill for:

- Helm chart creation/hardening for Arvan CaaS
- Kubernetes manifest authoring for Arvan panel, GitOps, or `kubectl`
- Deployment and rollout troubleshooting on Arvan
- GitLab Runner, namespace-scoped RBAC, imagePullSecret, and identity issues
- CI/CD changes that must enforce Arvan-safe rendering and deployment gates

## Arvan-first non-negotiables

1) Every container must have explicit resources.
- Prefer Arvan-safe default parity: `requests == limits`.
- CPU values must use decimal cores (for example `0.2`) instead of millicores (`200m`).
- Memory must default to `2x` CPU and use integer `Mi` or whole `Gi` (for example `0.2 -> 400Mi`, `0.5 -> 1Gi`, `2 -> 4Gi`).
- Include `ephemeral-storage` when policy/LimitRange expects it.

2) Secrets never leak.
- Keep secrets in Kubernetes `Secret` or `values.secret.yaml` (gitignored).
- Never output secrets in logs, templates, notes, CI, or `--set`.
- Support both modes:
  - Helm-managed secret generation
  - Existing secret reference (no overwrite)

3) HPA by workload type.
- Default HPA only for stateless `Deployment`.
- Stateful/PVC-backed workloads default to manual scaling knobs and runbooked operations.

4) Namespace-scoped RBAC first.
- Prefer `Role` + `RoleBinding`.
- Avoid cluster-scoped resources unless explicitly requested and approved.
- Assume deployment happens in an existing namespace; do not add namespace creation or cluster-scoped namespace checks to Arvan CI flows.

5) Config mount safety.
- Do not mount secrets/configmaps onto busy app directories.
- Use dedicated mount directories.

6) API version selection must be discovery-aware.
- Prefer `networking.k8s.io/v1` and `autoscaling/v2`.
- Fallback only when live discovery requires.

7) CPU generation scheduling is optional and value-driven.
- Affinity presets are opt-in, not forced by default.

8) HTTP exposure needs an explicit exposure mode.
- `ClusterIP` only solves in-cluster connectivity.
- For stable public HTTP/HTTPS apps on Arvan, prefer `service.type=LoadBalancer` plus service annotations for the public domain and pool when the cluster already uses that pattern.
- A known working Arvan pattern is `LoadBalancer` service plus `arvancloud.ir/domain` and, when needed, `metallb.universe.tf/ip-allocated-from-pool`.
- Support `ingress` mode separately as `ClusterIP` plus `Ingress`; keep ingress annotations configurable and do not hardcode undocumented platform annotations as universal requirements.
- When Arvan terminates TLS at the edge, keep in-cluster ingress/service traffic on HTTP unless a real in-cluster certificate flow is required.

## OpenAPI-driven capability baseline (Arvan 1.25)

From `references/arvan-caas-openAPI-1.25.json`:

- `openapi`: `3.0.3`
- `info.title`: `Arvan CaaS`
- `info.version`: `1.25`
- Paths: `134`
- Operations: `299`
- Namespaced paths: all paths are namespaced in this spec

Supported groups/resources include:

- `core/v1`: pods, services, configmaps, secrets, pvc, serviceaccounts, events, endpoints, resourcequotas, limitranges
- `apps/v1`: deployments, statefulsets, replicasets
- `autoscaling/v1|v2|v2beta2`: hpa
- `batch/v1`: jobs, cronjobs
- `networking.k8s.io/v1`: ingresses
- `rbac.authorization.k8s.io/v1`: roles, rolebindings

Treat as unsupported unless discovery proves otherwise:

- `DaemonSet`
- `NetworkPolicy`
- `PodDisruptionBudget`
- `StorageClass`
- `ClusterRole`, `ClusterRoleBinding`
- `CRD` APIs
- OpenShift Route/BuildConfig APIs

Full matrix:

- `references/openapi-1.25-capability-matrix.md`

## RBAC identity facts for Arvan (merged from arvan-caas-rbac-facts)

Load this reference when RBAC signals are inconsistent:

- `references/arvan-rbac-namespace-facts.md`

Required reasoning model:

1) Distinguish alias namespace and canonical namespace identities when both appear.
2) State exact principal under RBAC evaluation: `system:serviceaccount:<namespace>:<name>`.
3) Do not treat Helm release visibility as proof of runtime API authorization.
4) Do not treat `kubectl auth can-i --as=...` alone as conclusive, because impersonation rights may be missing for the caller.
5) If uncertainty remains, mark it explicitly and request verifiable evidence before changing RBAC policy.

## Companion skills orchestration (use with this skill)

Use these skills together when applicable. `caas-arvan-kuber` sets policy; companion skills perform domain-specialized generation/validation.

### Kubernetes and Helm core

1) `helm-generator`
2) `helm-validator`
3) `k8s-yaml-generator`
4) `k8s-yaml-validator`
5) `k8s-debug`

Usage pattern:

1) Build templates/manifests with generator skill.
2) Apply Arvan constraints from this skill.
3) Validate with validator skill.
4) If runtime issues occur, use `k8s-debug` with Arvan RBAC/namespace facts.

### Bash and automation

1) `bash-script-generator`
2) `bash-script-validator`
3) `makefile-generator`
4) `makefile-validator`

Usage pattern:

- Use when creating helper scripts for render checks, rollout checks, or troubleshooting.
- Ensure scripts remain non-mutating by default for discovery stages.

### CI/CD pipelines

1) `gitlab-ci-generator` + `gitlab-ci-validator`
2) `github-actions-generator` + `github-actions-validator`
3) `jenkinsfile-generator` + `jenkinsfile-validator`

Usage pattern:

- Add deterministic gates: `helm lint`, `helm template`, optional dry-run validation.
- Keep registry credentials in secret stores, never in plain variables.
- Pin tool and image versions.

### Container build inputs

1) `dockerfile-generator`
2) `dockerfile-validator`

Usage pattern:

- Use for image hardening when Arvan deployment failures are rooted in image/runtime behavior.

## Agent prompting best practices (high-signal)

When invoking this skill, prompt and execute in this structure:

1) Objective
- Define exact artifact and scope.

2) Constraints
- List active Arvan constraints and API limits.

3) Discovery
- Capture known/unknown state.
- Run read-only checks first.

4) Plan
- Write a short implementation plan with explicit tradeoffs.

5) Implement
- Use smallest safe change set.
- Keep portability toggles explicit.

6) Validate
- Lint/render/dry-run and inspect for secret leakage.

7) Deliver
- Provide operator actions and rollback/troubleshooting commands.

Prompting anti-patterns:

- Generating unsupported APIs from memory without discovery
- Assuming cluster-admin privileges in namespace-scoped environments
- Producing templates that omit resources
- Returning stateful scaling changes without runbook and safety notes

## Prompt templates (copy and adapt)

### Template: Helm/K8s implementation

```text
Goal: <deliverable>
Target namespace: <ns>
Workload type: <stateless|stateful>
Arvan constraints to enforce:
- resources requests==limits (+ ephemeral-storage if required)
- namespace-scoped RBAC
- no secret leakage
- HPA only if stateless
Discovery summary:
- supported APIs: <...>
- quota/limitrange: <...>
- RBAC can-i: <...>
Implement:
- files to modify: <...>
Validate:
- helm lint/template or kubectl dry-run commands
Deliver:
- install/upgrade/rollback commands
```

### Template: RBAC incident triage

```text
Incident: <forbidden error excerpt>
Namespace forms observed:
- alias: <...>
- canonical: <... or unknown>
Principal evaluated:
- system:serviceaccount:<namespace>:<name>
Evidence collected:
- rolebinding subjects
- current auth can-i results
- runner/job pod events
Reasoning:
- Kubernetes guarantee vs Arvan observation vs uncertainty
Next action:
- minimal and verifiable remediation
```

## Execution loop (mandatory)

### Phase 0: Discovery

Run read-only checks first:

```bash
bash .codex/skills/caas-arvan-kuber/scripts/verify-cluster.sh <namespace> [runner-serviceaccount]
```

Optional OpenAPI summary regeneration:

```bash
bash .codex/skills/caas-arvan-kuber/scripts/summarize-openapi.sh references/arvan-caas-openAPI-1.25.json
```

Additional checks:

```bash
kubectl config current-context
kubectl -n <ns> get resourcequota,limitrange
kubectl api-resources --namespaced=true -o name
kubectl api-versions | grep -E "autoscaling/v2|autoscaling/v2beta2|autoscaling/v1"
kubectl api-versions | grep -i networking.k8s.io
kubectl -n <ns> auth can-i create deployments
kubectl -n <ns> auth can-i create rolebindings
```

If shell access is unavailable:

- state assumptions clearly,
- generate conservative Arvan-safe output with toggles,
- provide explicit operator verification commands.

### Phase 1: Plan

State:

- what will change and why,
- which Arvan constraints are active,
- which OpenAPI or RBAC facts affect design.

### Phase 2: Implement

Implementation rules:

- Explicit resources on every container.
- `requests == limits` default on Arvan targets.
- Probes for app workloads.
- Stateless: `Deployment` with optional HPA.
- Stateful/PVC-backed: `StatefulSet` or operator CR, no default HPA.
- Service first; for public HTTP apps on Arvan, prefer an explicit exposure mode: `LoadBalancer/public-ip` when you want the gateway-style pattern, `ClusterIP + Ingress` when you explicitly want ingress mode.
- OpenShift Route only behind explicit toggle and API availability.
- Secrets via secret values or existing secret refs only.
- RBAC namespace-scoped by default.

### Phase 3: Validate

Helm path:

```bash
bash .codex/skills/caas-arvan-kuber/scripts/render-helm.sh <chart_dir> <namespace> [values.yaml] [values.secret.yaml] [rendered.yaml] [extra-values...]
```

Manifest path:

```bash
kubectl apply --dry-run=client -f rendered.yaml
```

Always verify:

- no secrets were printed,
- resources exist for all containers,
- APIs in manifests are supported by discovery.

### Phase 4: Deliver

Deliverables must include:

- minimal change set,
- copy/paste install/upgrade/rollback commands,
- README and RUNBOOK updates for operator handoff when scope is production/stateful.

## Arvan operation details to preserve in outputs

1) Panel accepts multi-document YAML separated by `---`.
2) Platform docs indicate resource defaults can be applied when missing.
3) Domain flows usually rely on Arvan CDN-managed DNS and active CDN.
4) Persistent storage lifecycle actions can be disruptive and must be documented.
5) Config mount path mistakes can shadow application files and cause startup failures.

## GitLab Runner on Arvan (important)

1) Job pods include multiple containers (`build`, `helper`, `init-permissions`) and all need pull access.
2) Ensure executor job pods render `image_pull_secrets`.
3) Keep helper image pinned and reachable in restricted egress environments.
4) Separate manager pod pull config from executor job pod pull config.
5) Do not rely on `kubectl create namespace`, `kubectl get namespace`, or `helm --create-namespace` in runner jobs unless live evidence proves the runner has that scope.
6) For RBAC denials, evaluate alias/canonical namespace identity mismatch before broadening privileges.

## CI/CD rules (portable + Arvan-safe)

1) Use immutable image tags and prefer digest pinning for production.
2) Keep CI tooling images pinned and mirrored where necessary.
3) Never print registry/API secrets in logs.
4) Standard validation gates before deploy:
- `helm lint`
- `helm template`
- optional schema validation (`kubeconform`/`kubeval`)
- optional `kubectl apply --dry-run=client`
5) Ensure migration/init/hook jobs also meet resource constraints.

## Definition of done

Done means:

1) Artifacts are compatible with OpenAPI/discovery constraints.
2) Containers have explicit resources with Arvan parity defaults.
3) Stateful storage and scaling constraints are documented.
4) Routing approach is explicit and compatible (`Ingress`/`LoadBalancer`; optional Route toggle only when supported).
5) Secret handling is safe end-to-end.
6) RBAC-sensitive changes consider alias/canonical namespace identity evidence.
7) Operator docs are copy/paste ready.

## Package resources (progressive disclosure)

Read only what is needed:

- `references/arvan-constraints.md`
- `references/arvan-caas-openAPI-1.25.json`
- `references/openapi-1.25-capability-matrix.md`
- `references/arvan-rbac-namespace-facts.md`
- `references/arvan-links.md`
- `assets/README.operator.md.template`
- `assets/RUNBOOK.operator.md.template`
- `assets/values.secret.yaml.example`
- `scripts/verify-cluster.sh`
- `scripts/render-helm.sh`
- `scripts/summarize-openapi.sh`
- `agents/openai.yaml`

Rule:

- Reuse assets/scripts before writing ad-hoc alternatives.
- Keep secrets out of non-secret files and terminal output.
