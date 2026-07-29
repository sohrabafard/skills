# Sources

Provenance ledger. Use it when Kubernetes, Helm, OpenShift, kubectl, oc, or managed-platform behaviour must be current, and to learn which official URL answers which question.

Last re-verified: **2026-07-29**. Every URL below was fetched on that date unless the row says otherwise. The values derived from them live in `references/version-awareness.md`; `scripts/check_versions.py` re-derives them.

## Freshness triggers

Re-check the primary sources when the user asks for latest or current behaviour, API availability, Kubernetes or Helm version compatibility, OpenShift release behaviour, deprecations, security advisories, admission policy, Gateway API status, CRD behaviour, storage or networking semantics, or upgrade risk. Also re-check when `scripts/check_versions.py` exits `1`.

## First-check sources, by question

| Question | URL |
|---|---|
| Which Kubernetes minors are supported, and when does each reach EOL? | https://kubernetes.io/releases/ |
| How far apart may kubectl, kubelet, and the control plane be? | https://kubernetes.io/releases/version-skew-policy/ |
| Was this `apiVersion` removed, and in which minor? | https://kubernetes.io/docs/reference/using-api/deprecation-guide/ |
| What changed in a specific minor? | https://kubernetes.io/releases/notes/ |
| What is the exact field or default on this object? | https://kubernetes.io/docs/reference/kubernetes-api/ |
| Which Helm release is current and what did it change? | https://github.com/helm/helm/releases |
| Which Kubernetes minors does this Helm build support? | https://helm.sh/docs/topics/version_skew/ |
| When does Helm 3 stop receiving patches? | https://helm.sh/blog/helm-v3-end-of-life/ |
| How do I write this template or chart correctly? | https://helm.sh/docs/chart_template_guide/ and https://helm.sh/docs/chart_best_practices/ |
| How does OCI chart distribution work? | https://helm.sh/docs/topics/registries/ |
| Which files does `.helmignore` actually exclude? | https://helm.sh/docs/chart_template_guide/helm_ignore_file/ |
| What is the current OpenShift line and what does it contain? | https://docs.redhat.com/en/documentation/openshift_container_platform/ |
| Are SCCs still the admission model on OpenShift? | https://docs.redhat.com/en/documentation/openshift_container_platform/4.22/html/authentication_and_authorization/index — chapter "Managing security context constraints". The historical slug `.../managing-pod-security-policies` still resolves and now serves SCC content, so do not cite it for PodSecurityPolicy; PSP was removed from Kubernetes in 1.25. |
| What replaced PodSecurityPolicy? | https://kubernetes.io/docs/concepts/security/pod-security-admission/ |
| Is Gateway API installed and what does it support? | https://gateway-api.sigs.k8s.io/ |
| How do I validate a manifest against schemas? | https://github.com/yannh/kubeconform and https://github.com/yannh/kubernetes-json-schema |
| How do I configure yamllint? | https://yamllint.readthedocs.io/ |
| What shape does a ServiceMonitor or PrometheusRule take? | https://prometheus-operator.dev/docs/api-reference/api/ |

## Conflict resolution

1. Live cluster discovery and RBAC checks on the target.
2. Official Kubernetes, Helm, and OpenShift docs for the versions the target actually runs.
3. CRD owner documentation for custom APIs.
4. This skill's local references and assets.

A number in this skill never outranks a number the cluster reports.

## Community troubleshooting sources

Use community posts, Stack Overflow answers, and issue comments only for concrete troubleshooting, and only after official docs, cluster events, logs, and API discovery have been checked. Do not use them as normative API, security, or upgrade policy.
