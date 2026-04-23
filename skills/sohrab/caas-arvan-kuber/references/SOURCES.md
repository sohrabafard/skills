# Sources

Use this file when Arvan CaaS, Kubernetes, Helm, GitLab Runner, registry, or delivery behavior must be current.

## Freshness triggers

Re-check primary sources when the user asks for latest/current Arvan behavior, platform docs, API support, namespace RBAC, service exposure, public IP/domain behavior, storage behavior, scaling/HPA behavior, GitLab Runner on Kubernetes, registry pulls, security-sensitive changes, or current troubleshooting signatures.

## First-check local and live sources

- Local OpenAPI baseline: `references/arvan-caas-openAPI-1.25.json`
- Derived capability matrix: `references/openapi-1.25-capability-matrix.md`
- RBAC namespace facts: `references/arvan-rbac-namespace-facts.md`
- Live discovery: `kubectl api-resources`, `kubectl api-versions`, `kubectl auth can-i`, namespace quota and LimitRange checks.

## First-check Arvan sources

- Cloud Container docs: https://docs.arvancloud.ir/en/cloud-container/
- Create app from container image: https://docs.arvancloud.ir/en/cloud-container/create-app/container-image
- Create app from manifest: https://docs.arvancloud.ir/en/cloud-container/create-app/manifest
- Manage app: https://docs.arvancloud.ir/en/cloud-container/manage-app/
- Connect app: https://docs.arvancloud.ir/en/cloud-container/connect-app/
- Storage: https://docs.arvancloud.ir/en/cloud-container/disk/
- Configs and secrets: https://docs.arvancloud.ir/en/cloud-container/manage-app/config
- Scaling: https://docs.arvancloud.ir/en/cloud-container/manage-app/scaling
- Domain: https://docs.arvancloud.ir/en/cloud-container/manage-app/domain
- Public IP: https://docs.arvancloud.ir/en/cloud-container/manage-app/dedicated-ip
- Helm catalogs: https://docs.arvancloud.ir/en/cloud-container/catalogs
- Arvan PaaS examples: https://github.com/arvancloud/paas-examples

## First-check Kubernetes, Helm, and CI sources

- Kubernetes docs: https://kubernetes.io/docs/
- Kubernetes API reference: https://kubernetes.io/docs/reference/kubernetes-api/
- Helm docs: https://helm.sh/docs/
- GitLab Runner Kubernetes executor: https://docs.gitlab.com/runner/executors/kubernetes/
- GitLab Runner Helm chart: https://docs.gitlab.com/runner/install/kubernetes_helm_chart_configuration/
- Docker registry and image pull behavior: https://docs.docker.com/

## Conflict resolution

1. Live Arvan cluster discovery and RBAC evidence.
2. Local Arvan OpenAPI baseline when live access is unavailable.
3. Current Arvan official docs.
4. Official Kubernetes, Helm, GitLab Runner, and Docker docs.
5. This skill's local references and assets.

## Community troubleshooting sources

Use community posts, Stack Overflow answers, and issue comments only for concrete troubleshooting after Arvan docs, live discovery, events, logs, and official Kubernetes/Helm/GitLab docs are checked. Do not use them as platform policy.
