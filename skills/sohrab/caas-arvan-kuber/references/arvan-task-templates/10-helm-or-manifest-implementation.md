# Template 1: Helm or manifest implementation

Before using any template, complete Step 1 in [SKILL.md](../../SKILL.md); each template includes fields that depend on that discovery. The `/alaa-k8s-helm` gate register and manifest checker belong to that skill; Arvan-specific references belong to this skill.

## Template 1: Helm or manifest implementation

```text
Goal: <deliverable, one sentence>
Target namespace: <ns>
Workload type: <stateless | stateful with persistent storage>

Server-reported version: <version | unknown>
API capabilities: <observed legacy/current APIs; no version inferred from absence>
Evidence: <the output line from the Step 1 detection>

Discovery results:
- namespaced kinds served that this work needs: <...>
- kinds this work wanted that are NOT served: <... or none>
- ResourceQuota: <... or none visible>
- LimitRange: <... including whether ephemeral-storage has a default>
- existing exposure pattern in this namespace: <public-ip | ingress | internal | none>
- can-i results for the applying identity: <...>

Arvan constraints active for this workload:
- resources on every container, requests == limits
- memory from the 1:2 function in references/arvan-constraints.md, or <measured value and why it differs>
- <HPA only if stateless; state which applies>
- exposure mode: <mode, matching the existing pattern above>
- <disk lifecycle notes, if a PVC is involved>

Implement:
- files to add or change: <...>
- portability toggles set: <...>

Validate:
- alaa-k8s-helm references/validation-workflows.md gates: <which ran, and the output>
- python3 alaa-k8s-helm scripts/check_manifests.py rendered.yaml --profile arvan

Deliver:
- install, upgrade, and rollback commands, with the Helm major detected
- README and RUNBOOK when the scope is production or stateful
```
