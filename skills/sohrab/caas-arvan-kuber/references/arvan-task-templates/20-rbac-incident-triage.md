# Template 2: RBAC incident triage

Before using any template, complete Step 1 in [SKILL.md](../../SKILL.md); each template includes fields that depend on that discovery. The `/alaa-k8s-helm` gate register and manifest checker belong to that skill; Arvan-specific references belong to this skill.

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
- current-context ServiceAccount identity and permission proof: <output, or blocked reason; never mint a token during discovery>
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
