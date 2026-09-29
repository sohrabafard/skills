# Template 3: Exposure mode selection

Before using any template, complete Step 1 in [SKILL.md](../../SKILL.md); each template includes fields that depend on that discovery. The `/alaa-k8s-helm` gate register and manifest checker belong to that skill; Arvan-specific references belong to this skill.

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
