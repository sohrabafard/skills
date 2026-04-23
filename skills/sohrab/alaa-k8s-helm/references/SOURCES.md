# Sources

Use this file when Kubernetes, Helm, OpenShift, kubectl, oc, or managed-platform behavior must be current.

## Freshness triggers

Re-check primary sources when the user asks for latest/current behavior, API availability, Kubernetes or Helm version compatibility, OpenShift release behavior, deprecations, security advisories, admission policy, Gateway API status, CRD behavior, storage or networking semantics, or upgrade risk.

## First-check Kubernetes sources

- Kubernetes documentation: https://kubernetes.io/docs/
- Kubernetes API reference: https://kubernetes.io/docs/reference/kubernetes-api/
- Kubernetes release notes: https://kubernetes.io/releases/notes/
- Kubernetes version skew policy: https://kubernetes.io/releases/version-skew-policy/
- Kubernetes deprecation guide: https://kubernetes.io/docs/reference/using-api/deprecation-guide/
- Kubernetes security concepts: https://kubernetes.io/docs/concepts/security/
- Pod Security Admission: https://kubernetes.io/docs/concepts/security/pod-security-admission/
- kubectl reference: https://kubernetes.io/docs/reference/kubectl/

## First-check Helm sources

- Helm documentation: https://helm.sh/docs/
- Helm chart template guide: https://helm.sh/docs/chart_template_guide/
- Helm chart best practices: https://helm.sh/docs/chart_best_practices/
- Helm release notes: https://github.com/helm/helm/releases
- Helm chart repository and OCI docs: https://helm.sh/docs/topics/registries/

## OpenShift and managed platform sources

- Red Hat OpenShift documentation: https://docs.redhat.com/en/documentation/openshift_container_platform/
- OpenShift CLI docs: https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/cli_tools/openshift-cli-oc
- OpenShift security and SCC docs: https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/authentication_and_authorization/managing-pod-security-policies
- Gateway API docs: https://gateway-api.sigs.k8s.io/
- Kubernetes SIGs controller-runtime docs: https://book.kubebuilder.io/reference/controller-runtime.html

## Validation tooling sources

- kubeconform: https://github.com/yannh/kubeconform
- kubernetes-json-schema: https://github.com/yannh/kubernetes-json-schema
- yamllint: https://yamllint.readthedocs.io/
- Prometheus Operator API docs: https://prometheus-operator.dev/docs/api-reference/api/

## Conflict resolution

1. Live cluster discovery and RBAC checks.
2. Official Kubernetes, Helm, and OpenShift docs for the matching versions.
3. CRD owner documentation for custom APIs.
4. This skill's local references and assets.

## Community troubleshooting sources

Use community posts, Stack Overflow answers, and issue comments only for concrete troubleshooting after official docs, cluster events, logs, and API discovery are checked. Do not use them as normative API, security, or upgrade policy.
