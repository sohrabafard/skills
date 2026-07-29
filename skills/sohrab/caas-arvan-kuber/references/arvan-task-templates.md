# Task templates

Three scaffolds. Fill in every angle-bracketed slot before using one; a slot left unfilled is a fact nobody discovered.

Each template assumes Step 1 in `SKILL.md` has already run, because every one of them has a field that depends on the answer. A path written with a leading skill name means a file inside that skill: `/alaa-k8s-helm` (`$alaa-k8s-helm`) for the gate register and the manifest checker, `/caas-arvan-kuber` (`$caas-arvan-kuber`) for the Arvan references.

## Template 1: Helm or manifest implementation

```text
Goal: <deliverable, one sentence>
Target namespace: <ns>
Workload type: <stateless | stateful with persistent storage>

Discovered line: <pinned 1.25-era | current 1.34+ | between>
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

## Template 2: RBAC incident triage

```text
Incident: <the exact forbidden message, verbatim>
When it started: <...>
What changed just before: <... or nothing known>

Namespace forms observed:
- alias: <...>
- canonical: <... or "not observable, and here is why">

Principal under evaluation:
- system:serviceaccount:<namespace>:<name>
- which namespace form that string carries: <alias | canonical>

Evidence collected (do not skip any line; a missing one is the usual cause of a wrong conclusion):
- RoleBinding subject table: <output>
- conclusive token check for the ServiceAccount: <output, or why a token could not be minted>
- can-i for the caller: <output>
- job pod events: <output>

Reasoning, separated:
- Kubernetes guarantee that applies: <...>
- Arvan observation that may apply: <...>
- what remains uncertain: <...>

Proposed action:
- the smallest change that would make the evidence above different
- what it grants, to which exact principal, in which namespace form
- what will be observed if the hypothesis was right, and what if it was wrong
```

## Template 3: Exposure mode selection

```text
Application: <name>
Does it need to be reachable from outside the cluster? <yes | no>
  If no: exposure mode is `internal`, a ClusterIP Service, and this template ends here.

Existing pattern in this namespace:
  command: kubectl -n <ns> get svc -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.type}{"\t"}{.metadata.annotations}{"\n"}{end}'
  output: <...>
  conclusion: <a LoadBalancer with arvancloud.ir/domain exists | it does not>

Is an ingress controller present?
  command: kubectl get ingressclass
  output: <...>

Decision: <public-ip | ingress | internal>
Reason: <the observation above that decided it, not a preference>

If public-ip:
- annotations to set: arvancloud.ir/domain=<domain>
- MetalLB pool annotation needed? <yes, pool name | no, the cluster does not use pool allocation>
- these annotations are undocumented by Arvan; state that in the deliverable and give the operator
  the command to confirm the Service received an address

If ingress:
- ingressClassName: <...>
- host and path rules: <...>

TLS:
- terminated at the Arvan edge? <yes: keep in-cluster traffic on HTTP and chart TLS off | no: name the issuer>

Domain prerequisites:
- the domain is on Arvan CDN-managed DNS with the CDN active: <confirmed | not confirmed, and this is the
  operator action that must happen before the endpoint resolves>
```
