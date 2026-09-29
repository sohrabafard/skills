# Arvan constraints: Delivery Failure Map

## 11. Failure map for delivery on Arvan

Symptom to first hypothesis. The full symptom-keyed procedure is in `references/arvan-execution-loop.md`.

| Symptom | First hypothesis |
|---|---|
| pull or auth failure in a GitLab Runner job | executor job pod pull-secret configuration, which `/alaa-gitlab-ci-cd` owns |
| Helm render failure | chart path or an unbuilt dependency |
| `forbidden` on a namespaced call while the Helm release looks healthy | alias-versus-canonical namespace identity; read `references/arvan-rbac-namespace-facts.md` before changing any RoleBinding |
| admission denial on create | a container without resources, or `requests` not equal to `limits` |
| `permission denied` reading a mounted Secret or ConfigMap file at startup | a mode without the other-read bit and no `fsGroup`; read section 7 in `references/arvan-constraints/30-exposure-config-and-secrets.md` |
| a kind is rejected as unknown | the API may be unavailable or discovery incomplete; re-read `references/arvan-capability-matrix.md` |


Provenance and source dates: [SOURCES.md](../SOURCES.md).
