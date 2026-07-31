# Sources

Provenance ledger for this skill. It says which source answers which question, what was confirmed against a vendor page and when, and how to research when the answer is not here.

Last re-verified: **2026-07-29**. Every Arvan URL below was fetched on that date.

## The finding that shapes everything else

**ArvanCloud publishes no Kubernetes version and no CaaS API version.** The Cloud Container pages carry none, and the developer API-usage page (https://docs.arvancloud.ir/en/developer-tools/api/api-usage) documents no CaaS versioning scheme and no OpenAPI reference. The `1.25` this skill's vendored spec carries cannot be confirmed against any Arvan statement.

That is why the Step 1 discovery in `SKILL.md` exists and why it outranks every file here: the only authoritative answer about the platform's API surface comes from the platform.

## Freshness triggers

Re-check the primary sources when the question touches current Arvan behaviour, API availability, namespace RBAC, service exposure, public IP or domain behaviour, storage behaviour, scaling, GitLab Runner on Kubernetes, registry pulls, a security-sensitive change, or a current troubleshooting signature. Also re-check when `bash scripts/summarize-openapi.sh --check` exits non-zero, because that means the vendored spec and the matrix no longer agree.

## Order of precedence

1. Live discovery on the target cluster: `kubectl api-versions`, `kubectl api-resources`, `kubectl auth can-i`, quota and LimitRange.
2. Current Arvan official documentation.
3. The vendored OpenAPI baseline, when live access is unavailable, and only as the more restrictive of the two lines.
4. Official Kubernetes, Helm, and GitLab documentation.
5. This skill's own references and assets.

A number written in this skill never outranks a number the cluster reports.

## Confirmed against Arvan's own pages on 2026-07-29

| Claim | Page |
|---|---|
| Resource consumption is declared per container, and "the values of Limits and Requests must be the same" | https://docs.arvancloud.ir/en/cloud-container/create-app/manifest |
| Omitted resources default to 1 CPU core and 2 GB of RAM, and a 1:2 CPU-to-RAM ratio is recommended | same page |
| Horizontal scaling "is only applicable to stateless applications", and with Persistent Storage enabled "you cannot use manual or automatic scaling" | https://docs.arvancloud.ir/en/cloud-container/manage-app/scaling |
| The container filesystem is ephemeral and is deleted on every restart | https://docs.arvancloud.ir/en/cloud-container/disk/ |
| Disk size can only be increased, detaching restarts the application, and deleting is irreversible | same page |
| The public-IP feature "leverages the Kubernetes Load Balancer feature" | https://docs.arvancloud.ir/en/cloud-container/manage-app/dedicated-ip |
| No annotation is documented for the public-IP or domain workflow | same page — this is an absence, and it is why the annotation pattern in `references/arvan-constraints.md` is marked observed rather than confirmed |

## Confirmed against Kubernetes and Helm on 2026-07-29

| Claim | Page |
|---|---|
| `autoscaling/v2beta2` was removed in Kubernetes 1.26, which makes it the line discriminator | https://kubernetes.io/blog/2022/11/18/upcoming-changes-in-kubernetes-1-26/ and https://kubernetes.io/docs/reference/using-api/deprecation-guide/ |
| The supported Kubernetes minors are 1.36, 1.35, and 1.34 | https://kubernetes.io/releases/ |
| Every other version fact this skill relies on | `/alaa-k8s-helm` (`$alaa-k8s-helm`) `references/version-awareness.md`, which is the single home for version numbers across both skills |

## Confirmed against GitLab on 2026-07-29

| Claim | Page |
|---|---|
| Runner registration tokens are the legacy workflow; authentication tokens carry a `glrt-` prefix; from GitLab 17.0 an administrator or group owner can disable the legacy workflow, after which registration returns `410 Gone - runner registration disallowed` | https://docs.gitlab.com/ci/runners/new_creation_workflow/ |
| GitLab Runner chart 0.53 and later configure pull secrets as `image_pull_secrets` in `config.toml`; 0.52 and earlier used `runners.imagePullSecrets` in `values.yaml` | https://docs.gitlab.com/runner/install/kubernetes_helm_chart_configuration/ |

Runner configuration itself is owned by `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`). These two rows are recorded here only because this skill's `$SKILL_DIR/assets/values.secret.yaml.example` and its RBAC guidance touch them.

## Arvan documentation map

- Cloud Container getting started: https://docs.arvancloud.ir/en/cloud-container/
- Build an application: https://docs.arvancloud.ir/en/cloud-container/create-app/ — from a container image: https://docs.arvancloud.ir/en/cloud-container/create-app/container-image — from a manifest: https://docs.arvancloud.ir/en/cloud-container/create-app/manifest
- Manage an application: https://docs.arvancloud.ir/en/cloud-container/manage-app/
- Connect to an application, covering Service and Ingress: https://docs.arvancloud.ir/en/cloud-container/connect-app/
- Disks: https://docs.arvancloud.ir/en/cloud-container/disk/
- Configs, Secrets, image secrets, SSH keys, webhooks: https://docs.arvancloud.ir/en/cloud-container/manage-app/config
- Scaling: https://docs.arvancloud.ir/en/cloud-container/manage-app/scaling
- Domain: https://docs.arvancloud.ir/en/cloud-container/manage-app/domain
- Public IP: https://docs.arvancloud.ir/en/cloud-container/manage-app/dedicated-ip
- One-click Helm catalogs: https://docs.arvancloud.ir/en/cloud-container/catalogs
- CLI: https://docs.arvancloud.ir/en/developer-tools/cli/
- Manifest examples: https://github.com/arvancloud/paas-examples

## Kubernetes, Helm, and CI sources

- Kubernetes docs: https://kubernetes.io/docs/ — API reference: https://kubernetes.io/docs/reference/kubernetes-api/
- Kubernetes releases and support windows: https://kubernetes.io/releases/
- Deprecated API migration guide: https://kubernetes.io/docs/reference/using-api/deprecation-guide/
- Helm docs: https://helm.sh/docs/
- GitLab Runner Kubernetes executor: https://docs.gitlab.com/runner/executors/kubernetes/
- GitLab Runner Helm chart configuration: https://docs.gitlab.com/runner/install/kubernetes_helm_chart_configuration/

## Rules for research

- Prefer a primary source: Arvan, Kubernetes, Helm, or GitLab documentation, in that order for the question at hand.
- Record the date and the version alongside anything you take from a page, because Arvan's documentation is not versioned and drift is otherwise undetectable by reading.
- Put the URL in the deliverable whenever a decision rests on something found online.
- Use community posts, Stack Overflow answers, and issue comments only for concrete troubleshooting, and only after live discovery, events, logs, and the official pages have been checked. They are never platform policy.
- Never paste a token, a kubeconfig, or a values file into a search query or a shared command.
