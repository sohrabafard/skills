# Arvan CaaS namespace identity and RBAC

## Scope

This file records what is known about namespace identity and RBAC evaluation on Arvan CaaS. It stays **descriptive**: it separates what Kubernetes guarantees from what has been observed on the platform, and it names the check that settles the question. It deliberately does not prescribe a remediation, because the right remediation depends on which of the two identities the RoleBinding is meant to grant, and that is a task decision.

Nothing in Arvan's public documentation describes any of the platform observations below. They come from a live cluster.

## Terminology

- **Alias namespace**: the human-friendly name an operator types and most Helm commands use. Example: `vk`.
- **Canonical namespace**: the runtime namespace identity, which may be hash-prefixed. Example: `bcbf1234-vk`.

## What Kubernetes guarantees, on any platform

1. A ServiceAccount principal is namespace-scoped and is evaluated as `system:serviceaccount:<namespace>:<name>`.
2. A `RoleBinding` subject matches on exact kind, name, and namespace. There is no fuzzy matching and no aliasing in the authorizer.
3. An in-cluster client authenticates with its mounted ServiceAccount token and no kubeconfig.
4. `kubectl auth can-i --as=...` requires the caller to impersonate that principal before the access review is evaluated. An impersonation error is unavailable subject proof, not a subject denial.

## What has been observed on Arvan CaaS

1. The alias and canonical identities can name the same workload scope at different layers.
2. A Helm operation can target the alias namespace while a runtime authorization check evaluates the canonical namespace string.
3. A GitLab Runner pod can appear to run against alias-namespace objects while authorization is enforced against a canonical ServiceAccount identity string.
4. `RoleBinding` subjects can be rewritten or normalised between the two forms by platform components, so the subject you wrote is not necessarily the subject that is stored.
5. A Helm release can be listed successfully while a job in the same namespace fails with `forbidden`.
6. Release visibility can differ between the alias and canonical views, depending on how release metadata was stored.

## Typical symptoms

1. A CI job pod cannot be created, with `forbidden`, immediately after a chart installed successfully.
2. Helm release metadata looks healthy while the workload's own API calls fail.
3. `kubectl auth can-i --as=system:serviceaccount:...` reports a denial that reflects the caller's missing impersonation right rather than the ServiceAccount's permissions.

## The conclusive check

Use an already authorized context authenticated as the ServiceAccount. Verify its identity before attributing permission results to it:

```bash
kubectl auth whoami -o 'jsonpath={.status.userInfo.username}'
bash scripts/verify-cluster.sh NS SA
```

The username must equal `system:serviceaccount:NS:SA`, using the namespace form the server authenticates. The helper returns `2` when identity discovery is unsupported, denied, empty or mismatched; it never substitutes caller permissions for ServiceAccount proof. This can block older clusters without identity discovery, and does not raise their supported-version floor. Obtain an authorized identity-proof path before claiming the ServiceAccount is ready.

The helper creates no credential and performs no impersonation. Credential issuance is a separate authorized operation outside this read-only procedure; never paste credentials into commands, reports or logs. API catalog visibility establishes available kinds, not authorization to list their objects.

## Reasoning guardrails

1. Keep the Kubernetes guarantees and the Arvan observations separate in any explanation. The first are stable; the second can change without notice.
2. When an authorization signal is inconsistent, treat an alias-versus-canonical mismatch as a first-class hypothesis, ahead of "the Role is too narrow".
3. No single signal settles it. A visible Helm release does not prove runtime authorization, and a `--as` denial does not prove a missing permission.
4. State both namespace forms and the exact principal in the write-up, every time: `system:serviceaccount:<namespace>:<name>` for each form you observed.
5. When the canonical identity cannot be observed directly, say so explicitly rather than assuming the alias form is what the authorizer sees.
6. Do not broaden a RoleBinding to make a symptom disappear. A binding added for the wrong namespace form grants a real permission to a real principal and does not fix the mismatch.

## Evidence to collect before changing anything

```bash
kubectl -n NS get rolebinding -o custom-columns=NAME:.metadata.name,SUBJECT_KINDS:.subjects[*].kind,SUBJECT_NAMESPACES:.subjects[*].namespace,SUBJECT_NAMES:.subjects[*].name
kubectl -n NS get serviceaccount SA -o yaml
kubectl -n NS get events --sort-by=.lastTimestamp | grep -i forbidden
```

`bash scripts/verify-cluster.sh NS SA` collects discovery, permission and RoleBinding evidence in one read-only pass; collect ServiceAccount objects and events separately when needed.
