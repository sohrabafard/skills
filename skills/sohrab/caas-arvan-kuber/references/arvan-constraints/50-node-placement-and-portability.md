# Arvan constraints: Node Placement And Portability

## 8. Node affinity for CPU generation

**Unverified.** Selecting a CPU generation may require a node-affinity label, and `cloud-container-g2` and `g3` have been named as families. **No label key is known, and no Arvan page documents one.** Do not emit an affinity block for this from memory. Discover the key first:

```bash
kubectl get nodes --show-labels                       # when nodes are listable
kubectl -n NS get pod -o jsonpath='{.items[0].spec.nodeSelector}'   # what existing workloads use
```

If neither returns a key, say in the deliverable that CPU-generation pinning could not be expressed, and leave `affinityPreset.cpuGeneration` off.

## 9. Portability toggles

A chart that must work on Arvan and on stock Kubernetes carries exactly these switches, each with a safe default:

| Toggle | Default | Meaning |
|---|---|---|
| `exposureMode` | `internal` | one of `public-ip`, `ingress`, `internal`, per section 4 |
| `hpa.enabled` | `false` | must stay `false` for any workload with a PVC, per section 2 |
| `ingress.enabled` / `route.enabled` | `false` | mutually exclusive; render at most one |
| `openshift.enabled` | `false` | Arvan is not OpenShift; this exists for portability only |
| `affinityPreset.cpuGeneration` | off | per section 8 |
| `privateRegistry.create` / `privateRegistry.existingSecretName` | `create: true` | create the pull Secret from values, or reference one the platform already holds; never both |



Provenance and source dates: [SOURCES.md](../SOURCES.md).
