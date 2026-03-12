# Arvan CaaS OpenAPI 1.25 Capability Matrix

This reference is derived from the local spec file:

- `./arvann-caas-openAPI-1.25.json`

Snapshot metadata (from spec):

- `openapi`: `3.0.3`
- `info.title`: `Arvan CaaS`
- `info.version`: `1.25`
- Paths: `134`
- Operations: `299`
- Server URLs:
  - `https://napi.arvancloud.ir/caas/v2/zones/ir-tbz-sh1`
  - `https://napi.arvancloud.ir/caas/v2/zones/ir-thr-ba1`

## High-signal constraints from the spec

1) All documented paths are namespace scoped.
- `134/134` paths include `/namespaces/{namespace}`.
- No cluster-scoped endpoint paths are present in this OpenAPI document.

2) API groups exposed by the spec:
- `core/v1`
- `apps/v1`
- `autoscaling/v1`
- `autoscaling/v2`
- `autoscaling/v2beta2`
- `batch/v1`
- `coordination.k8s.io/v1`
- `discovery.k8s.io/v1`
- `events.k8s.io/v1`
- `networking.k8s.io/v1`
- `rbac.authorization.k8s.io/v1`

3) The spec includes `PATCH` support with all common Kubernetes patch content types on mutable workload resources:
- `application/apply-patch+yaml`
- `application/json-patch+json`
- `application/merge-patch+json`
- `application/strategic-merge-patch+json`

4) List APIs include standard Kubernetes query controls (`fieldSelector`, `labelSelector`, `continue`, `limit`, `resourceVersion`, `watch`).

## Supported resources (collection/item-level)

Legend:

- `C`: collection verbs
- `I`: item verbs
- `Sub`: subresources and verbs

| API resource                                   | C                 | I                      | Sub                                                                                                                                                                             |
|------------------------------------------------|-------------------|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `core/v1/configmaps`                           | `get,post,delete` | `get,put,patch,delete` | -                                                                                                                                                                               |
| `core/v1/secrets`                              | `get,post,delete` | `get,put,patch,delete` | -                                                                                                                                                                               |
| `core/v1/services`                             | `get,post,delete` | `get,put,patch,delete` | `status(get,put,patch)`, `proxy(get,post,put,patch,delete)`                                                                                                                     |
| `core/v1/pods`                                 | `get,post,delete` | `get,put,patch,delete` | `status`, `log(get)`, `exec(get,post)`, `attach(get,post)`, `portforward(get,post)`, `eviction(post)`, `ephemeralcontainers(get,put,patch)`, `proxy(get,post,put,patch,delete)` |
| `core/v1/persistentvolumeclaims`               | `get,post,delete` | `get,put,patch,delete` | `status(get,put,patch)`                                                                                                                                                         |
| `core/v1/serviceaccounts`                      | `get,post,delete` | `get,put,patch,delete` | `token(post)`                                                                                                                                                                   |
| `core/v1/endpoints`                            | `get,post,delete` | `get,put,patch,delete` | -                                                                                                                                                                               |
| `core/v1/events`                               | `get,post,delete` | `get,put,patch,delete` | -                                                                                                                                                                               |
| `core/v1/replicationcontrollers`               | `get,post,delete` | `get,put,patch,delete` | `scale(get,put,patch)`, `status(get,put,patch)`                                                                                                                                 |
| `core/v1/limitranges`                          | `get`             | `get`                  | -                                                                                                                                                                               |
| `core/v1/resourcequotas`                       | `get`             | `get`                  | `status(get)`                                                                                                                                                                   |
| `apps/v1/deployments`                          | `get,post,delete` | `get,put,patch,delete` | `scale(get,put,patch)`, `status(get,put,patch)`                                                                                                                                 |
| `apps/v1/statefulsets`                         | `get,post,delete` | `get,put,patch,delete` | `scale(get,put,patch)`, `status(get,put,patch)`                                                                                                                                 |
| `apps/v1/replicasets`                          | `get,post,delete` | `get,put,patch,delete` | `scale(get,put,patch)`, `status(get,put,patch)`                                                                                                                                 |
| `apps/v1/controllerrevisions`                  | `get`             | `get`                  | -                                                                                                                                                                               |
| `autoscaling/v1/horizontalpodautoscalers`      | `get,post,delete` | `get,put,patch,delete` | `status(get,put,patch)`                                                                                                                                                         |
| `autoscaling/v2/horizontalpodautoscalers`      | `get,post,delete` | `get,put,patch,delete` | `status(get,put,patch)`                                                                                                                                                         |
| `autoscaling/v2beta2/horizontalpodautoscalers` | `get,post,delete` | `get,put,patch,delete` | `status(get,put,patch)`                                                                                                                                                         |
| `batch/v1/jobs`                                | `get,post,delete` | `get,put,patch,delete` | `status(get,put,patch)`                                                                                                                                                         |
| `batch/v1/cronjobs`                            | `get,post,delete` | `get,put,patch,delete` | `status(get,put,patch)`                                                                                                                                                         |
| `coordination.k8s.io/v1/leases`                | `get,post,delete` | `get,put,patch,delete` | -                                                                                                                                                                               |
| `discovery.k8s.io/v1/endpointslices`           | `get`             | `get`                  | -                                                                                                                                                                               |
| `events.k8s.io/v1/events`                      | `get,post,delete` | `get,put,patch,delete` | -                                                                                                                                                                               |
| `networking.k8s.io/v1/ingresses`               | `get,post,delete` | `get,put,patch,delete` | `status(get,put,patch)`                                                                                                                                                         |
| `rbac.authorization.k8s.io/v1/roles`           | `get,post,delete` | `get,put,patch,delete` | -                                                                                                                                                                               |
| `rbac.authorization.k8s.io/v1/rolebindings`    | `get,post,delete` | `get,put,patch,delete` | -                                                                                                                                                                               |

## APIs absent from the OpenAPI 1.25 document

These should be treated as unsupported unless discovery in the live cluster proves otherwise:

- `apps/v1/daemonsets`
- `networking.k8s.io/v1/networkpolicies`
- `policy/v1/poddisruptionbudgets`
- `storage.k8s.io/v1/storageclasses`
- `rbac.authorization.k8s.io/v1/clusterroles`
- `rbac.authorization.k8s.io/v1/clusterrolebindings`
- `apiextensions.k8s.io/v1/customresourcedefinitions`
- OpenShift APIs such as:
  - `route.openshift.io/v1/routes`
  - `build.openshift.io/v1/buildconfigs`

## Agent behavior derived from this matrix

1) Prefer namespace-scoped operations and manifests.
2) Avoid cluster-scoped RBAC/resources by default.
3) If a task asks for unsupported resources (for example `NetworkPolicy`, `DaemonSet`, `PDB`), either:
- provide an Arvan-compatible fallback pattern, or
- explicitly require cluster verification and user confirmation.
4) Treat `LimitRange` and `ResourceQuota` as discovery/guardrail inputs (read-oriented in this API).
5) Keep HPA generation version-aware:
- prefer `autoscaling/v2`,
- fallback to `autoscaling/v2beta2` or `autoscaling/v1` only if discovery requires.

## Quick discovery commands to align live cluster with this matrix

```bash
kubectl api-resources --namespaced=true -o name
kubectl api-versions | grep -E "autoscaling/v2|autoscaling/v2beta2|autoscaling/v1"
kubectl api-versions | grep -i networking.k8s.io
kubectl -n <ns> get resourcequota,limitrange
kubectl -n <ns> auth can-i create deployments
kubectl -n <ns> auth can-i create rolebindings
```
