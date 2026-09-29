# Arvan CaaS constraints

This reference set is the single normative statement of every Arvan platform constraint. Each rule appears here once and nowhere else in this skill. Where a rule is generic Kubernetes rather than Arvan, this file names the owner instead of restating it.

Each rule carries its status: **confirmed by Arvan** with the page that says so, **observed** with what was seen and when, or **unverified**. Treat an unverified rule as a hypothesis to test with discovery, not as a constraint to enforce.

Step 1 in `SKILL.md` establishes observable capabilities and permissions separately from server version; unknown discovery remains unknown. Read `references/arvan-capability-matrix.md` for the per-kind answer.

## 1. Resources are mandatory and parity is enforced

When setting CPU/memory requests and limits or checking parity, read [resource parity](arvan-constraints/10-resource-parity.md) for the required resource and equality rules.

### CPU written as decimal cores, and why this is style rather than a constraint

When writing a CPU quantity or deciding whether decimal cores are required, read [the CPU style note](arvan-constraints/10-resource-parity.md#cpu-written-as-decimal-cores-and-why-this-is-style-rather-than-a-constraint) to distinguish style from a platform constraint.


## 2. Scaling is stateless-only

When scaling a workload or deciding whether it may use an HPA with persistent state, read [stateful storage](arvan-constraints/20-stateful-storage.md) for the stateless-only boundary.

## 3. Disk lifecycle

When sizing, expanding or retiring a PVC, read [stateful storage](arvan-constraints/20-stateful-storage.md) for the disk lifecycle.

## 4. Exposure has three modes, and one uses annotations Arvan does not document

When choosing public-IP, ingress or internal exposure, read [exposure, config and secrets](arvan-constraints/30-exposure-config-and-secrets.md) for platform modes and evidence.

## 5. Namespace scope

When defining namespace-scoped permissions or resources, read [namespace and panel scope](arvan-constraints/40-namespace-and-panel-scope.md) for scope boundaries.

## 6. Panel behaviour

When interpreting Arvan panel behavior, read [namespace and panel scope](arvan-constraints/40-namespace-and-panel-scope.md) for observed panel limitations.

## 7. Config mount safety

When mounting configuration, deciding secret exposure, or choosing the file mode of a Secret or ConfigMap a non-root process reads, read [exposure, config and secrets](arvan-constraints/30-exposure-config-and-secrets.md) for mount and secret safety.

## 8. Node affinity for CPU generation

When selecting node affinity for CPU generation, read [node placement and portability](arvan-constraints/50-node-placement-and-portability.md) for placement evidence.

## 9. Portability toggles

When deciding whether a portability toggle is safe on Arvan, read [node placement and portability](arvan-constraints/50-node-placement-and-portability.md) for supported portability settings.

## 10. Secrets

When creating or mounting a secret, read [exposure, config and secrets](arvan-constraints/30-exposure-config-and-secrets.md) for secret constraints.

## 11. Failure map for delivery on Arvan

When diagnosing a failed delivery, read [the delivery failure map](arvan-constraints/60-delivery-failure-map.md) to separate confirmed constraints from observations and unknowns.
