# Arvan CaaS Namespace and RBAC Facts

## Scope

This file records known behavior and constraints around namespace identity and RBAC evaluation in Arvan CaaS environments.
Keep statements factual and avoid turning them into fixed remediation playbooks.

## Terminology

- Alias namespace: human-friendly namespace name used by operators and many Helm commands (example: `vk`).
- Canonical namespace: runtime namespace identity that may be hash-prefixed (example: `bcbf1234-vk`).

## Kubernetes guarantees (platform-agnostic facts)

1) ServiceAccount principals are namespace-scoped and evaluated as `system:serviceaccount:<namespace>:<serviceaccount-name>`.
2) `RoleBinding` subjects are matched by exact kind/name/namespace identity.
3) In-cluster clients normally authenticate through mounted ServiceAccount tokens without kubeconfig.
4) `kubectl auth can-i --as=...` depends on impersonation permissions for the caller.

## Arvan CaaS observations (platform-specific behavior)

1) Alias and canonical namespace identities can represent the same workload scope at different layers.
2) Helm release operations may target alias namespaces while runtime identity checks can evaluate canonical namespace strings.
3) GitLab Runner pods can appear to run in alias namespace objects while authorization is enforced against canonical ServiceAccount identity strings.
4) RoleBinding subjects may be rewritten or normalized by platform components between alias and canonical forms.
5) A Helm release can be visible in namespace listings while runner job actions still fail with authorization errors.
6) Release visibility across alias/canonical namespace views can vary by metadata handling and platform behavior.

## Typical symptoms

1) CI job pod creation fails with `forbidden` despite successful chart installation.
2) Helm release metadata looks healthy, but runtime job execution fails on Kubernetes API calls.
3) `kubectl auth can-i --as=system:serviceaccount:...` reports denial that is caused by missing impersonation permission, not necessarily by the runner's own permissions.

## Reasoning guardrails for agents

1) Separate Kubernetes-native guarantees from Arvan-specific observations.
2) Treat alias/canonical namespace mismatch as a first-class hypothesis when RBAC symptoms are inconsistent.
3) Avoid concluding that RBAC is correct or incorrect from a single signal:
- Helm release presence alone is insufficient.
- `kubectl auth can-i --as=...` alone is insufficient.
4) State uncertainty explicitly when canonical identity cannot be observed directly.
5) Keep this reference descriptive; choose remediation in the task context, not in this file.

