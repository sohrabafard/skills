# ArvanCloud reference map for this skill

This file maps canonical references used by the skill.

Last verification snapshot: **2026-02-15**

## Primary machine-readable source

- Local Arvan CaaS OpenAPI spec: `references/arvan-caas-openAPI-1.25.json`
- Derived matrix: `references/openapi-1.25-capability-matrix.md`
- RBAC namespace identity facts: `references/arvan-rbac-namespace-facts.md`

Use the OpenAPI file + live discovery as runtime authority; use links below for operational docs.

## Core docs (Cloud Container / CaaS)

- Cloud Container (Getting Started): https://docs.arvancloud.ir/en/cloud-container/
- Build Application overview: https://docs.arvancloud.ir/en/cloud-container/create-app/
- Build via Container Image: https://docs.arvancloud.ir/en/cloud-container/create-app/container-image
- Build via Manifest: https://docs.arvancloud.ir/en/cloud-container/create-app/manifest
- Manage Application: https://docs.arvancloud.ir/en/cloud-container/manage-app/
- Connect to Application (Service / Ingress concepts): https://docs.arvancloud.ir/en/cloud-container/connect-app/
- Storage (Disks / PVC semantics in panel): https://docs.arvancloud.ir/en/cloud-container/disk/
- Configs (Secret / ConfigMap / Image secret / SSH key /
  Webhook): https://docs.arvancloud.ir/en/cloud-container/manage-app/config
- Scaling (Vertical / Horizontal ~ HPA): https://docs.arvancloud.ir/en/cloud-container/manage-app/scaling
- Domain (Free domain + custom domain prerequisites): https://docs.arvancloud.ir/en/cloud-container/manage-app/domain
- Public IP (LoadBalancer behavior in panel): https://docs.arvancloud.ir/en/cloud-container/manage-app/dedicated-ip
- One-Click Helm Charts (panel Helm value patterns): https://docs.arvancloud.ir/en/cloud-container/catalogs

## Developer tools

- ArvanCLI overview: https://docs.arvancloud.ir/en/developer-tools/cli/
- Cloud Shell usage (includes `arvan paas` examples): https://docs.arvancloud.ir/fa/developer-tools/cloud-shell/usage

## Additional official examples

- ArvanCloud PaaS examples repo (k8s manifests, `arvan paas` usage): https://github.com/arvancloud/paas-examples

## Mapped help-center pages (user-facing Persian portal)

- Kubernetes for Experts: https://www.arvancloud.ir/help/fa/kuber-for-experts/
- CLI Guide: https://www.arvancloud.ir/help/fa/cat/cloud-container/cli-guide/
- HPA guide: https://www.arvancloud.ir/help/fa/hpa-container/
- Secret guide: https://www.arvancloud.ir/help/fa/container-secret/
- Kubernetes for Beginners: https://www.arvancloud.ir/help/fa/kuber-for-beginners/

## GitLab Runner / Kubernetes references (official)

- GitLab Runner Helm chart docs (Kubernetes executor, image pull
  secrets): https://docs.gitlab.com/runner/install/kubernetes_helm_chart_configuration/
- GitLab Runner Kubernetes executor docs (job pod behavior, helper/container
  pulls): https://docs.gitlab.com/runner/executors/kubernetes/
- GitLab Runner chart repository (values/templates): https://gitlab.com/gitlab-org/charts/gitlab-runner

## Quick facts confirmed from docs

- Arvan Cloud Container docs explicitly model ingress/domain/public IP flows on top of Kubernetes Service/Ingress
  concepts.
- Arvan scaling guidance distinguishes stateless horizontal scaling and warns about persistent-storage constraints in
  panel workflows.
- GitLab Runner Helm docs confirm Kubernetes executor image-pull-secret integration and chart-version caveats (0.52 vs
  0.53+ behavior).
