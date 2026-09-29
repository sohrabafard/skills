# Arvan constraints: Namespace And Panel Scope

## 5. Namespace scope

**Derived from the vendored spec.** Use this restrictive baseline until live discovery and authorization establish a different tenant scope.

- The target namespace already exists. Do not emit `Namespace`, do not pass `--create-namespace`, and do not make a deployment depend on `kubectl get namespace` succeeding: a namespace-scoped identity can be forbidden from reading the Namespace object while being able to perform every namespaced operation it needs.
- Use `Role` and `RoleBinding`. `ClusterRole` and `ClusterRoleBinding` are unavailable to a tenant.
- Which other kinds exist is line-dependent; `references/arvan-capability-matrix.md` holds both columns.

## 6. Panel behaviour

**Plausible, from Arvan's manifest page.** The panel accepts a multi-document YAML stream separated by `---`, which is why a chart's rendered output can be pasted directly. Nothing about the panel changes what a manifest must contain.



Provenance and source dates: [SOURCES.md](../SOURCES.md).
