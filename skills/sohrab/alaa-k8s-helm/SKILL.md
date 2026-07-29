---
name: alaa-k8s-helm
description: Unified Kubernetes, Helm, OpenShift, and kubectl or oc skill for generating, refactoring, validating, explaining, upgrading, and debugging Helm charts, Kubernetes manifests, and OpenShift workloads. Use it when the task involves Helm 3 or 4, Kubernetes YAML, kubectl or oc commands, Routes, SCCs, CRDs, rollout safety, service exposure, storage, or networking, including on a managed namespace platform. Do not use it for Docker-only, Terraform-only, CI-only, or cloud work that does not materially depend on Kubernetes, OpenShift, or Helm. Do not use it for ArvanCloud CaaS platform facts, the Arvan namespace-only API surface, or Arvan alias-versus-canonical namespace RBAC identity, which caas-arvan-kuber owns.
---

# Alaa K8s + Helm

Single entrypoint for Helm, Kubernetes YAML, OpenShift, and day-2 troubleshooting.

## Start here

1. Read `references/00-topic-map.md`. It is the only router in this skill: it maps a task phrasing to the smallest set of files to open across the five lanes (authoring, validation, runtime debugging, platform fit, networking and tuning), and it lists the scripts.
2. Establish the **version surface** (`helm version`, `kubectl version --output=yaml`, `oc version`, `kubectl api-versions`) and the **access surface** (cluster-admin, namespace admin, developer, container-only) before writing anything.
3. Open only the files the topic map names.

## When NOT to use

- Docker-only, Terraform-only, CI-only work, cloud architecture that does not materially depend on Kubernetes, OpenShift, or Helm, and application logic whose fix is not tied to workload runtime behaviour.
- Arvan CaaS platform facts. Load `/caas-arvan-kuber` (`$caas-arvan-kuber`) only when the answer depends on a fact that is true of Arvan CaaS and false of stock Kubernetes at the same minor version; otherwise load `/alaa-k8s-helm` (`$alaa-k8s-helm`), including when the target cluster happens to be Arvan.

## Default operating model

- **Version-aware first**: every version number this skill uses lives in `references/version-awareness.md` and nowhere else. Read it when compatibility, skew, or "latest" behaviour affects the answer; re-derive it with `scripts/check_versions.py`.
- **Access-aware first**: never assume cluster-admin. `references/openshift-and-managed-platforms.md` states what each of the four access surfaces unlocks and which `auth can-i` call proves it; run that call before recommending a cluster-scoped object or a node-level action.
- **Emit only API versions the target serves**: emit an `apiVersion` only when `kubectl api-versions` on the target reports it. When the cluster is unknown, emit only versions served on every supported Kubernetes minor named in `references/version-awareness.md`, and state that floor in the output.
- **Namespace-safe by default**: generate namespaced resources. Emit a cluster-scoped resource only after `kubectl auth can-i create RESOURCE` returns `yes` for the identity that will apply it.
- **Evidence before edits**: for debugging, collect status, describe output, events, logs, and access errors before proposing a fix.
- **OpenShift-safe by default**: when the target might be OpenShift or an OpenShift-like managed platform, assume arbitrary UID, non-root execution, stricter admission, and no node access until a command proves otherwise.
- **Report-only when asked to audit**: when the user said validate, lint, review, or audit, return findings and change nothing. When the user said fix, generate, refactor, or patch, make the change and rerun the gates.

## Guardrails

- Run the gates in `references/validation-workflows.md` before any live change. That file is the gate register and states which gate is mandatory for which artifact.
- Never emit a change to `spec.selector` on an existing Deployment, StatefulSet, DaemonSet, or Job, or to a StatefulSet's `volumeClaimTemplates[].metadata.name`. When identity must change, emit a new resource under a new name and state the cutover order: the old resource is deleted before the new one takes its traffic. `scripts/check_manifests.py --baseline` detects a violation.
- Emit none of the host-level and privilege-escalating fields listed under "Restricted-by-default fields" in `references/openshift-and-managed-platforms.md`. That file states the single observable condition under which each exception is permitted; name the SCC or admission policy in the output when you take one.
- Expose workloads through a Service plus Ingress, Gateway API, or Route. Use a bare Pod only for a one-off debug or batch case.
- Distribute charts through an OCI registry. Use a classic chart repository only when the user states that their registry cannot serve OCI artifacts.
- When the platform is uncertain, state the assumption and emit the restrictive path defined in `references/openshift-and-managed-platforms.md`.

## Companion boundaries

Each line names an owner and the condition under which that owner decides the matter.

- `/alaa-reliability-sla` (`$alaa-reliability-sla`) decides why a timeout, retry, backoff, circuit breaker, backpressure, or degradation mechanism exists and what shape it takes. `references/failure-and-load.md` holds only the Kubernetes expression of that decision.
- `/alaa-security-review` (`$alaa-security-review`) decides review triggers, threat classes, and fail-closed doctrine. Route a manifest change there when it widens an access surface, adds a Secret, or relaxes a security context.
- `/alaa-observability-soc` (`$alaa-observability-soc`) decides whether a signal is required and what gates on it; `/alaa-services-contract` (`$alaa-services-contract`) decides every shared name and value, including log fields, the `alaa_*` metric catalog, `OTEL_*` names and defaults, and the host-port table.
- `/alaa-testing-strategy` (`$alaa-testing-strategy`) decides test layering and what a smoke test must assert; this skill decides only that a chart test exists and is packaged.
- `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) decides the complexity budget behind a request, a limit, or a replica count.
- `/alaa-minio-object-storage` (`$alaa-minio-object-storage`) decides the bucket, policy, lifecycle, and credential posture behind an object-storage volume or an S3 Secret, and `/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`) decides the same for an `arvanstorage.ir` endpoint; this skill keeps only the Kubernetes expression, because a Secret, a PVC, or a CSI volume carries whatever storage policy it is handed and enforces none of it.
- `/caas-arvan-kuber` (`$caas-arvan-kuber`) decides Arvan CaaS platform facts, under the deciding test above.
- `/alaa-prompting-guide` (`$alaa-prompting-guide`) `references/50-effort-and-thinking.md` decides model and reasoning effort, and no model name appears in this skill, because a model name written into a skill goes stale silently and is copied forward because it looks authoritative.

**Stack versus platform (D8).** `references/validation-workflows.md` is the **Kubernetes and Helm delivery gate register**: this skill decides which checks must pass before a Kubernetes or Helm change is applied and what artifact each inspects, and writes no provider YAML and no Dockerfile. `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) owns how each gate is placed on a runner, including the `[runners.kubernetes]` block, and decides no gate. `/alaa-docker-production` (`$alaa-docker-production`) owns how the image a chart references is built and hardened, and decides no gate. `/alaa-makefile` (`$alaa-makefile`) owns making a local Make target return the runner's verdict. `/alaa-frontend-devops` (`$alaa-frontend-devops`) owns the frontend gate register; this file is its backend counterpart.

## Subagent strategy

Split work across agents only when the task spans more than one topic-map lane; the useful splits are inventory, validation, platform fit, and runtime. Describe a lane by the judgment it needs rather than by a tier: chart and platform orchestration decides trade-offs across releases and needs the escalated lane; read-only inventory, static validation, and log summarisation apply a fixed procedure and do not. Without multi-agent support, do the same work sequentially with the same separation.

## Deliverable rules

- Generation: return ready-to-apply YAML or chart files, plus the gate commands you ran and their output.
- Validation: separate **blocking errors**, **deployment risks**, and **best-practice gaps**, and name every gate you skipped and why.
- Debugging: end with the most likely root cause, its evidence, the next command that confirms it, and the lowest-risk fix.
