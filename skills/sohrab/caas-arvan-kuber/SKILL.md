---
name: caas-arvan-kuber
description: Arvan CaaS platform facts for Kubernetes and Helm workloads - the namespace-scoped API surface, alias-versus-canonical namespace RBAC identity, the requests-equal-limits admission parity, panel-managed domain, public IP and disk lifecycle, and the exposure annotations Arvan does not document. Use it only when a manifest, chart, or deployment decision would be different on Arvan than on a stock Kubernetes cluster at the same minor version. Do not use it for generic Kubernetes or Helm authoring, validation, or debugging, which alaa-k8s-helm owns, including when the target cluster happens to be Arvan. Do not use it to write GitLab Runner configuration or to decide pipeline gates. Do not invent undocumented Arvan behaviour when live discovery can answer the question.
---

# Arvan CaaS platform facts

## The deciding test, stated in the same words on both sides of this seam

Load `/caas-arvan-kuber` (`$caas-arvan-kuber`) only when the answer depends on a fact that is true of Arvan CaaS and false of stock Kubernetes at the same minor version; otherwise load `/alaa-k8s-helm` (`$alaa-k8s-helm`), including when the target cluster happens to be Arvan.

Being on Arvan is not by itself a reason to load this skill. The four facts that pass the test are the namespace-only API surface, alias-versus-canonical namespace RBAC identity, the requests-equal-limits admission parity, and the panel-managed domain, public-IP, and disk lifecycle. Each is stated once, in `references/arvan-constraints.md`.

## Step 1, before anything else: find out which line the target is on

Arvan publishes no Kubernetes version anywhere, and the vendored spec this skill carries describes a 1.25-era surface. The platform may still be on that line or may have moved. **Never assume which; discover it.** This needs only read access:

```bash
kubectl api-versions | tr -d '\r' | sort > /tmp/arvan-api-versions.txt
grep -qx 'autoscaling/v2beta2'                  /tmp/arvan-api-versions.txt && echo 'PINNED LINE: at most Kubernetes 1.25'
grep -qx 'flowcontrol.apiserver.k8s.io/v1beta3' /tmp/arvan-api-versions.txt && echo 'at most Kubernetes 1.31'
grep -qx 'resource.k8s.io/v1'                   /tmp/arvan-api-versions.txt && echo 'CURRENT LINE: Kubernetes 1.34 or newer'
kubectl version -o json 2>/dev/null | grep -i gitVersion    # authoritative when the server allows it
kubectl api-resources --namespaced=false -o name 2>&1 | head  # empty or forbidden means a namespace-only surface
kubectl auth can-i --list -n NS                               # what this identity may actually do
```

`autoscaling/v2beta2` is the discriminator: it was removed upstream in Kubernetes 1.26, so a server that still serves it is on the pinned line and a server that does not is not. Name the answer in the deliverable before writing a manifest, because a manifest built for the wrong line is accepted by one cluster and rejected by the other.

`bash scripts/verify-cluster.sh NS [runner-serviceaccount]` runs this plus the RBAC evidence in one read-only pass and **exits non-zero** when a required API or permission is absent.

## Source precedence

Live discovery outranks every local file, because a local file describes a snapshot and the cluster is the fact.

1. Live discovery on the target (the commands above, plus quota and LimitRange).
2. `references/arvan-capability-matrix.md` — two columns: the pinned line, the current upstream stable, and where they differ.
3. `references/arvan-constraints.md`, then `references/arvan-rbac-namespace-facts.md`.
4. `references/arvan-caas-openAPI-1.25.json` — **machine-readable only, roughly 1.5 MB. Never open it. `scripts/summarize-openapi.sh` is its only permitted reader.**

## Companion boundaries, and when not to use this skill

| Owner | Decides |
|---|---|
| `/alaa-k8s-helm` (`$alaa-k8s-helm`) | chart and manifest authoring, validation, runtime debugging; owns the gate register at its `references/validation-workflows.md` and ships `scripts/check_manifests.py`. Build and validate there, apply the Arvan facts from here. |
| `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) | GitLab Runner configuration in full: the `[runners.kubernetes]` block, `image_pull_secrets`, helper-image pinning, the manager-versus-executor pull split. This skill states no runner setting. |
| `/alaa-docker-production` (`$alaa-docker-production`) | how the image is built and hardened, and tag and digest policy. |
| `/alaa-reliability-sla` (`$alaa-reliability-sla`) | every timeout, retry, and degradation value, including Helm's `--wait --timeout` and its relation to the CI job timeout. |
| `/alaa-security-review` (`$alaa-security-review`) | fail-closed doctrine, and the handling of any artifact holding a decoded Secret. |
| `/alaa-observability-soc` (`$alaa-observability-soc`), `/alaa-services-contract` (`$alaa-services-contract`) | whether a signal is required, and every shared name and value. |
| `/alaa-testing-strategy` (`$alaa-testing-strategy`) | what a smoke test must assert. |
| `/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`), `/alaa-minio-object-storage` (`$alaa-minio-object-storage`) | the bucket, endpoint, policy, and credentials behind an S3 Secret; this skill keeps only its Kubernetes expression. |
| `/alaa-bash-shell` (`$alaa-bash-shell`), `/alaa-makefile` (`$alaa-makefile`) | helper scripts and local invocation; keep discovery helpers non-mutating. |
| `/alaa-prompting-guide` (`$alaa-prompting-guide`) `references/50-effort-and-thinking.md` | model and reasoning effort. No model name appears in this skill, because one written into a skill goes stale silently and is copied forward because it looks authoritative. |

Two runner-adjacent rules stay here because they are Arvan consequences, not runner settings: a job must not rely on `kubectl create namespace`, `kubectl get namespace`, or `helm --create-namespace` unless discovery proves the runner holds that scope; and an RBAC denial inside a job is an alias-versus-canonical identity question before it is a permissions question.

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

Scripts: `verify-cluster.sh` (read-only discovery that fails on a missing capability), `render-helm.sh` (deterministic render, mode-0600 output, removed on exit), `summarize-openapi.sh` (`--check` fails when the matrix and the spec have drifted apart). Each takes `--help` and `--self-test` and exits `0` clean, `1` findings, `2` could not run. Assets: the two operator templates, emitted when the scope is production or stateful, and `assets/values.secret.yaml.example`.

## Definition of done

1. The discovered line is named in the deliverable, with the command output that established it.
2. `python3 alaa-k8s-helm scripts/check_manifests.py rendered.yaml --profile arvan` exits 0.
3. Every kind used appears in the discovered line's column of the capability matrix, or the deliverable says why discovery overrode it.
4. The exposure mode is explicit and matches what the cluster already uses.
5. No decoded secret exists outside a mode-0600 file removed on exit, and every filename that can hold one is in the repository's ignore rules.
6. An RBAC-sensitive change states both namespace forms and the principal evaluated.
7. Stateful storage and scaling constraints reach the operator README and RUNBOOK.
