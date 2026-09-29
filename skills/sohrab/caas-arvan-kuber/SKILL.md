---
name: caas-arvan-kuber
description: Arvan CaaS platform facts for Kubernetes and Helm workloads - the namespace-scoped API surface, alias-versus-canonical namespace RBAC identity, the requests-equal-limits admission parity, panel-managed domain, public IP and disk lifecycle, and the exposure annotations Arvan does not document. Use it only when a manifest, chart, or deployment decision would be different on Arvan than on a stock Kubernetes cluster at the same minor version. Do not use it for generic Kubernetes or Helm authoring, validation, or debugging, which alaa-k8s-helm owns, including when the target cluster happens to be Arvan. Do not use it to write GitLab Runner configuration or to decide pipeline gates. Do not invent undocumented Arvan behaviour when live discovery can answer the question.
---

# Arvan CaaS platform facts

## The deciding test, stated in the same words on both sides of this seam

Load `/caas-arvan-kuber` only when the answer depends on a fact that is true of Arvan CaaS and false of stock Kubernetes at the same minor version; otherwise load `/alaa-k8s-helm`, including when the target cluster happens to be Arvan.

Being on Arvan is not by itself a reason to load this skill. The four facts that pass the test are the namespace-only API surface, alias-versus-canonical namespace RBAC identity, the requests-equal-limits admission parity, and the panel-managed domain, public-IP, and disk lifecycle. Each is stated once, in `references/arvan-constraints.md`.

## Step 1, before anything else: find out which line the target is on

The reviewed Arvan sources establish no current server version; the vendored spec describes a 1.25-era surface. **Discover the server version and required capabilities separately.** This needs only read access:

```bash
kubectl api-versions | tr -d '\r' | sort > /tmp/arvan-api-versions.txt
grep -qx 'autoscaling/v2beta2' /tmp/arvan-api-versions.txt && echo 'Legacy API observed; removed upstream in 1.26'
grep -qx 'resource.k8s.io/v1'  /tmp/arvan-api-versions.txt && echo 'API observed; stable upstream since 1.34'
kubectl version -o json                                      # inspect serverVersion, not clientVersion
kubectl api-resources --namespaced=false -o name              # catalog visibility is not authorization
kubectl auth can-i --list -n NS                               # what this identity may actually do
```

An absent API proves no version range: APIs can be disabled or discovery unavailable. A visible kind grants no permission to use it; empty or forbidden discovery proves no namespace-only platform boundary. Report server version as unknown when unavailable, preserve discovery errors, and verify every required kind and verb before relying on it.

`bash scripts/verify-cluster.sh NS [runner-serviceaccount]` collects this evidence without minting tokens or impersonating. With the optional ServiceAccount, the current context must already authenticate as that exact namespace/ServiceAccount principal; unavailable or mismatched identity blocks with exit `2`. A denied or absent required capability returns `1`; unavailable required proof returns `2`. Without that argument, the result covers only the caller.

## Source precedence

Live discovery outranks every local file, because a local file describes a snapshot and the cluster is the fact.

1. Live discovery on the target (the commands above, plus quota and LimitRange).
2. `references/arvan-capability-matrix.md` — two columns: the pinned line, the current upstream stable, and where they differ.
3. `references/arvan-constraints.md`, then `references/arvan-rbac-namespace-facts.md`.
4. `references/arvan-caas-openAPI-1.25.json` — **machine-readable only, roughly 1.5 MB. Never open it. `scripts/summarize-openapi.sh` is its only permitted reader.**

## Companion boundaries, and when not to use this skill

| Owner | Decides |
|---|---|
| `/alaa-k8s-helm` | chart and manifest authoring, validation, runtime debugging; owns the gate register at its `references/validation-workflows.md` and ships `scripts/check_manifests.py`. Build and validate there, apply the Arvan facts from here. |
| `/alaa-gitlab-ci-cd` | GitLab Runner configuration in full: the `[runners.kubernetes]` block, `image_pull_secrets`, helper-image pinning, the manager-versus-executor pull split. This skill states no runner setting. |
| `/alaa-docker-production` | how the image is built and hardened, and tag and digest policy. |
| `/alaa-reliability-sla` | every timeout, retry, and degradation value, including Helm's `--wait --timeout` and its relation to the CI job timeout. |
| `/alaa-security-review` | fail-closed doctrine, and the handling of any artifact holding a decoded Secret. |
| `/alaa-observability-soc`, `/alaa-services-contract` | whether a signal is required, and every shared name and value. |
| `/alaa-testing-strategy` | what a smoke test must assert. |
| `/alaa-arvan-object-storage`, `/alaa-minio-object-storage` | the bucket, endpoint, policy, and credentials behind an S3 Secret; this skill keeps only its Kubernetes expression. |
| `/alaa-bash-shell`, `/alaa-makefile` | helper scripts and local invocation; keep discovery helpers non-mutating. |
| `/alaa-prompting-guide` `references/50-effort-and-thinking.md` | model and reasoning effort. No model name appears in this skill, because one written into a skill goes stale silently and is copied forward because it looks authoritative. |

Two runner-adjacent rules stay here because they are Arvan consequences, not runner settings: a job must not rely on `kubectl create namespace`, `kubectl get namespace`, or `helm --create-namespace` unless discovery proves the runner holds that scope; and an RBAC denial inside a job is an alias-versus-canonical identity question before it is a permissions question.

**Portable-chart routing.** When a chart targets Arvan CaaS and OpenShift or OKD, read `/alaa-k8s-helm` `references/openshift-and-managed-platforms.md` before setting `runAsUser`, `privileged`, or `hostPath`; that file owns the non-root, arbitrary-UID, and restricted-field rules. Before setting `fsGroup` or the `defaultMode` of a Secret or ConfigMap a non-root process reads, read `references/arvan-constraints.md` section 7, because Arvan documents no injected `fsGroup`. Passing Arvan checks does not prove OpenShift/OKD SCC admission or runtime compatibility; validate the rendered chart and image on each target with its deployment identity.

**Stack versus platform (D8).** This skill owns the Arvan platform facts that change a manifest or a deployment decision, and contributes Arvan-only **predicates** to the gate register in `alaa-k8s-helm references/validation-workflows.md`: no rendered container omits resources and `requests` equals `limits`; no rendered document uses a kind absent from the discovered line's column of the capability matrix; no rendered manifest references a cluster-scoped object. It owns **no gate placement and no runner configuration**.

## Reference list, with the condition that opens each file

| File | Open it when |
|---|---|
| `references/arvan-constraints.md` | writing or reviewing any manifest, chart, or values file for Arvan |
| `references/arvan-capability-matrix.md` | deciding whether a kind or `apiVersion` is available, after Step 1 |
| `references/arvan-rbac-namespace-facts.md` | an authorisation signal is inconsistent: the release looks healthy and a job is forbidden |
| `references/arvan-execution-loop.md` | starting a delivery task, or recovering from a failed delivery step |
| `references/arvan-task-templates.md` | you want a prompt scaffold for a Helm implementation, an RBAC triage, or an exposure choice |
| `references/SOURCES.md` | current Arvan, Kubernetes, Helm, or GitLab behaviour matters, or a web search is about to run |

Scripts: `verify-cluster.sh` (read-only capability and identity proof), `render-helm.sh` (new mode-0600 output, removed on exit; existing `--out` paths or unverifiable permissions block before Helm), `summarize-openapi.sh` (`--check` fails on matrix/spec drift). Each takes `--help` and `--self-test` and exits `0` clean, `1` findings, `2` could not run. Assets: the two operator templates for production or stateful scope, and `assets/values.secret.yaml.example`.

## Definition of done

1. The server-reported version or explicit unknown is named, with required API and permission evidence reported separately.
2. Resolve the loaded `/alaa-k8s-helm` skill's absolute directory and the rendered manifest's absolute path before running this check. Replace both example paths; do not infer either from the current directory. A missing checker or Python 3 stops with exit 2. The checker returns 0 for clean, 1 for findings, and 2 when it could not run; completion requires exit 0.

   ```sh
   (
     k8s_helm_root="/absolute/path/to/alaa-k8s-helm"
     rendered_yaml="/absolute/path/to/rendered.yaml"
     checker="$k8s_helm_root/scripts/check_manifests.py"
     [ -f "$checker" ] || { printf 'Missing /alaa-k8s-helm checker: %s\n' "$checker" >&2; exit 2; }
     command -v python3 >/dev/null 2>&1 || { printf 'Python 3 is required\n' >&2; exit 2; }
     python3 "$checker" "$rendered_yaml" --profile arvan
   )
   ```
3. Every kind used appears in the discovered line's column of the capability matrix, or the deliverable says why discovery overrode it.
4. The exposure mode is explicit and matches what the cluster already uses.
5. No decoded secret exists outside a mode-0600 file removed on exit, and every filename that can hold one is in the repository's ignore rules.
6. An RBAC-sensitive change states both namespace forms and the principal evaluated.
7. Stateful storage and scaling constraints reach the operator README and RUNBOOK.

For retained renders, use a caller-owned mode-0700 output directory with trusted
ancestors; do not reuse a shared build directory. The helper creates missing parents
privately, writes through one retained descriptor, and blocks on unprovable ownership,
permissions or a replaced output path. Existing files remain untouched. GNU-compatible
`stat` and `/dev/fd` are required; use a supported POSIX environment when unavailable.
