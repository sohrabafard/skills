# Networking and Tuning

## Contents

- The layer model
- Fast service-path tracing
- Core debugging checkpoints
- Kubernetes-specific signals
- Tuning boundaries by access surface

## The layer model

Name the failing layer before changing anything. Most Kubernetes network incidents become tractable at that moment.

- **name resolution** — DNS turns a name into a cluster IP or an external IP
- **service virtual IP** — Service plus kube-proxy or its replacement routes to endpoints
- **endpoint selection** — EndpointSlice reflects ready backend Pods
- **pod network** — the CNI provides pod-to-pod routing
- **application listener** — the process actually listens on the expected address and port
- **edge routing** — Ingress, Gateway API, Route, or a load balancer handles external entry

Key concepts that decide which layer you are in:

- **L3/L4 versus L7** — Service, NetworkPolicy, and load balancers act at L3 or L4; Ingress, Gateway API, and Route add L7 behaviour such as hosts, paths, headers, and TLS termination.
- **SNAT and egress** — outbound traffic may be NATed by the node or by a platform egress path, so the source address the remote service sees is not the Pod IP.
- **MTU** — a mismatch produces flaky connectivity, retransmits, and timeouts that look like an application bug.
- **conntrack** — an exhausted connection-tracking table drops connections intermittently and silently.
- **readiness versus connectivity** — a Pod can be reachable by IP and still receive no Service traffic.

## Fast service-path tracing

### Internal service path, in order

1. the source Pod resolves the name
2. the Service exists
3. the Service selector matches Pods
4. the EndpointSlice contains ready backends
5. the target Pod listens on the expected port
6. NetworkPolicy allows the traffic

```bash
kubectl get svc,endpointslices -n NS
kubectl get pod -n NS --show-labels
kubectl exec -n NS POD -- sh -c 'getent hosts SERVICE || nslookup SERVICE'
```

### External HTTP path, in order

1. the backend Service works internally
2. the Ingress, Gateway, or Route points at the correct Service and port
3. host and path rules match the request
4. the TLS mode matches what the backend expects
5. the external DNS record points at the correct edge

Do not start at the public URL when the Service is already broken internally.

## Core debugging checkpoints

**DNS** — service FQDN and short-name resolution, CoreDNS or platform DNS health, `resolv.conf` search domains inside the Pod, and namespace mismatch in the lookup.

**Service and endpoints** — selector labels, `targetPort`, named-versus-numeric port mismatch, and endpoint readiness state.

**NetworkPolicy** — policies are allow-lists, not deny-lists with exceptions; the absence of a matching allow rule is a denial. Both ingress and egress policies can block traffic. Enforcement requires a CNI that implements NetworkPolicy: without one, the object exists and enforces nothing, which is indistinguishable from a permissive policy until an audit. Confirm with the CNI's own documentation, not with the object's presence.

**Application listener** — a large share of "Kubernetes networking" bugs are listener bugs. Check that the process listens on `0.0.0.0` rather than `127.0.0.1`, that the port declared in YAML matches the process, and that TLS expectations are consistent end to end.

## Kubernetes-specific signals

`/alaa-observability-soc` (`$alaa-observability-soc`) decides whether a signal is required and what gates on it. `/alaa-services-contract` (`$alaa-services-contract`) decides every metric name, label, log field, and `OTEL_*` default. Do not invent a name here.

What this skill contributes is the short list of Kubernetes-layer signals those owners do not derive from the application, and what each one means:

| Signal | Why it is Kubernetes-specific | What it distinguishes |
|---|---|---|
| container restart count and `lastState.terminated.reason` | comes from the kubelet, not the process | `OOMKilled` versus `Error` versus a liveness-probe restart, which have different fixes |
| probe failure counts by probe type | only the kubelet sees them | a readiness flap that removes traffic from a healthy Pod, versus a real fault |
| Pod pending duration | scheduling, not runtime | insufficient capacity or an unsatisfiable constraint, versus an application that will not start |
| CPU throttled seconds, alongside CPU usage | the CFS quota is a limit-enforcement artefact | latency caused by the limit rather than by the workload; usage alone never shows it |
| unavailable replicas during a rollout | the controller's view | a rollout that is progressing slowly versus one that is deadlocked, which `references/failure-and-load.md` resolves |

Everything else — request rate, error rate by status class, latency percentiles, traces, log fields — is the application's telemetry, and its names and requirement level belong to the two owners above.

## Tuning boundaries by access surface

### Feasible with namespace access

Resource requests and limits, probe timings, HPA settings, connection pool sizes in application config, worker concurrency, ingress or route timeouts where the platform delegates them, and the Service type.

Each of these needs a derivation, and `references/failure-and-load.md` gives it. Do not change one without recording the before and after measurement.

### Requires cluster-admin or the platform owner

CNI settings, MTU, kube-proxy mode, conntrack sizing, DNS architecture changes such as NodeLocal DNSCache, kubelet or container-runtime or kernel tuning, and OpenShift `MachineConfig`. On a managed platform, treat all of these as unavailable until `kubectl auth can-i list nodes` returns `yes`.

## Habits that keep tuning honest

- Isolate the layer before changing YAML.
- Test one hypothesis at a time.
- Compare a failing workload against a healthy one in the same namespace.
- Measure before and after every change, and put both numbers in the report.
- Do not tune around a broken dependency, a mismatched selector, or a wrong probe. You are in that situation when the Service has zero ready endpoints, when the selector matches no Pod, or when the probe fails on a request the application answers correctly from inside the container — all three are observable with the commands above, and none of them is fixed by a resource or timeout change.
