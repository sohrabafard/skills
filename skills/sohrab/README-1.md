# README — `.codex` Skills (Arvan‑first)

All skills in this repository live side‑by‑side under:

```
.codex/skills/<skill-name>/
```

This setup is designed for **ChatGPT Codex 5.3** to generate **production‑grade** DevOps/Kubernetes outputs that are:
- **ArvanCloud CaaS / Cloud Container compatible** (your publishing platform), and
- still **portable to standard Kubernetes** (and at most require minimal OpenShift toggles).

---

## 1) The only precedence rule (critical)

Your platform policy is the skill:

> `skills/caas-arvan-kuber/`

If any other skill guidance conflicts with Arvan requirements:

> ✅ **Arvan-first wins** (unless you explicitly request an override).

This is intentional: Arvan behaves like a standard Kubernetes environment with **stricter operational constraints**.

---

## 2) The default workflow (Generator → Arvan‑patch → Validate)

Most skills come as **generator + validator** pairs. Use them like this:

1) **Generate a baseline** (Helm chart / manifests / CI / IaC)
2) **Apply Arvan-first constraints** (resources, secrets, scaling, mounts, ingress/domain assumptions, etc.)
3) **Validate** using the relevant validator (lint/security/syntax)
4) **Iterate** until clean *without violating Arvan-first rules*
5) **Ship operator docs** (README + RUNBOOK) for production operations

---

## 3) Arvan-first rules (high-level summary)

These are the platform constraints that most often drive differences versus generic best practices:

### 3.1 Resources are mandatory (Requests == Limits, incl. ephemeral-storage)
Every container must have explicit `resources`, and **requests must equal limits** (including `ephemeral-storage`).

### 3.2 Multi-document YAML is supported
For “panel paste” deployments, bundle resources into a single YAML separated by `---`.

### 3.3 CPU generation scheduling (optional affinity)
If you need newer CPU generations, Arvan may require node affinity via platform labels.

### 3.4 Scaling: HPA for stateless by default
Arvan panel scaling is intended for **stateless** apps. When persistent storage is involved, scaling has constraints.
For stateful workloads: expose a manual `replicas/instances` knob and document safe scaling in the runbook.

### 3.5 Domain/Ingress prerequisites
Arvan domain + CDN rules can impose prerequisites (e.g., HTTP on port 80). Provide both:
- `ingress.enabled` (portable K8s)
- `service.type=LoadBalancer` (if requested)

### 3.6 Config mount pitfall
Avoid mounting config files over “busy” directories; mount into a dedicated subdirectory to prevent folder shadowing.

### 3.7 Cluster-scope avoidance
Assume namespace-scoped RBAC. Avoid CRDs/ClusterRoles unless explicitly approved.

### 3.8 API version awareness
Prefer modern APIs (`networking.k8s.io/v1`, `autoscaling/v2`) but select via discovery when possible.

---

## 4) Skill catalogue (as installed in `.codex/skills`)

### Platform / Policy
- `caas-arvan-kuber`

### Helm
- `helm-generator`
- `helm-validator`

### Kubernetes
- `k8s-yaml-generator`
- `k8s-yaml-validator`
- `k8s-debug`

> Note: Some docs may refer to a `k8s-generator` name; in this repository, the folder present is `k8s-yaml-generator`.

### Docker
- `dockerfile-generator`
- `dockerfile-validator`

### CI/CD
- `gitlab-ci-generator`, `gitlab-ci-validator`
- `github-actions-generator`, `github-actions-validator`
- `jenkinsfile-generator`, `jenkinsfile-validator`
- `azure-pipelines-generator`, `azure-pipelines-validator`

### IaC
- `terraform-generator`, `terraform-validator`
- `terragrunt-generator`, `terragrunt-validator`
- `ansible-generator`, `ansible-validator`

### Observability / Logging
- `promql-generator`, `promql-validator`
- `logql-generator`
- `loki-config-generator`
- `fluentbit-generator`, `fluentbit-validator`

### Build & Scripting
- `makefile-generator`, `makefile-validator`
- `bash-script-generator`, `bash-script-validator`

---

## 5) Recommended “Definition of Done” (production publishing)

A deliverable is considered **Arvan-ready** when:
- It deploys under namespace-scoped RBAC.
- All containers satisfy Arvan resources policy.
- Secrets are never leaked and are managed via Secrets / secret values.
- Scaling approach matches workload type (stateless vs stateful).
- Config mounts avoid folder shadowing.
- Helm rendering + linting + validators pass.
- Operator docs exist (README + RUNBOOK) and are copy/paste-ready.

---

## 6) Team note
When we must deviate from a generic approach, explicitly document the reason:

> “We follow Arvan-first policy because ArvanCloud CaaS imposes operational constraints for production publishing.”

