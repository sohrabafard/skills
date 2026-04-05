# Networking, Observability, and Tuning

## Contents

- Minimal networking model every senior operator needs
- Fast service-path tracing
- Core debugging checkpoints
- Monitoring signals that matter
- Tuning boundaries and access requirements

## Minimal networking model every senior operator needs

Think in layers. Most Kubernetes network incidents become much easier when you can name the failing layer.

### Layer model

- **name resolution**: DNS turns names into cluster IPs or external IPs
- **service virtual IP**: Service and kube-proxy or the implementation route traffic to endpoints
- **endpoint selection**: EndpointSlice reflects ready backend Pods
- **pod network**: the CNI provides pod-to-pod routing
- **application listener**: the process must actually listen on the expected address and port
- **edge routing**: Ingress, Gateway API, Route, or a load balancer handles external entry

### Key concepts

- **L3/L4 vs L7**: Service, NetworkPolicy, and load balancers mostly live at L3 or L4; Ingress, Gateway API, and Route add L7 behavior such as hosts, paths, headers, and TLS termination.
- **SNAT and egress**: outbound traffic may be NATed by the node or platform egress path.
- **MTU**: mismatched MTU can create flaky connectivity, retransmits, or mysterious timeouts.
- **conntrack**: exhausted or unhealthy connection tracking can cause drops and intermittent failures.
- **readiness vs connectivity**: a pod can be reachable by IP but not ready for Service traffic.

## Fast service-path tracing

Trace requests in this order.

### Internal service path

1. source pod can resolve the name
2. Service exists
3. Service selector matches Pods
4. EndpointSlice contains ready backends
5. target Pod listens on the expected port
6. NetworkPolicy allows traffic

Useful checks:

```bash
kubectl get svc,endpoints,endpointslices -n <namespace>
kubectl get pod -n <namespace> --show-labels
kubectl exec -n <namespace> <pod> -- sh -c 'getent hosts <service> || nslookup <service>'
```

### External HTTP path

1. backend Service works internally
2. Ingress, Gateway, or Route points to the correct Service and port
3. host and path rules match the request
4. TLS mode matches the backend expectation
5. the external DNS record points to the correct edge

Do not start at the public URL if the Service is already broken internally.

## Core debugging checkpoints

### DNS

Check:

- service FQDN and short name resolution
- CoreDNS or platform DNS health
- `resolv.conf` search domains inside the Pod
- namespace mismatch in lookups

### Service and endpoints

Check:

- selector labels
- `targetPort`
- named vs numeric port mismatch
- endpoint readiness state

### NetworkPolicy

Remember:

- policies are allow lists, not deny lists with exceptions
- both ingress and egress policies can block traffic
- enforcement depends on the CNI supporting NetworkPolicy

### Application listener

A large share of “Kubernetes networking” bugs are actually app-level listener bugs.

Check:

- the app is listening on `0.0.0.0`, not just `127.0.0.1`
- the port exposed in YAML matches the process
- TLS expectations are consistent end to end

## Monitoring signals that matter

Keep the telemetry focused on signals that help explain failures.

### Workload health

- restart count
- `OOMKilled`
- probe failure counts
- pending duration
- rollout status and unavailable replicas

### Resource pressure

- CPU throttling, not just CPU usage
- memory working set and OOM events
- container filesystem saturation
- node pressure conditions

### Traffic and latency

- request rate
- error rate by status class
- latency percentiles, not just averages
- open connections and timeouts
- retransmits and dropped packets when node metrics are available

### Platform services

- CoreDNS latency or failure rate
- ingress or router 4xx and 5xx patterns
- API server errors or throttling
- CSI driver errors for storage-related incidents

### Logs, metrics, and traces together

Use all three when possible.

- **metrics** tell you when and how broadly something is failing
- **logs** tell you what failed
- **traces** tell you where latency and dependency failures accumulated

## Tuning boundaries and access requirements

### Namespace-level tuning

Usually feasible with namespace access:

- resource requests and limits
- probes and timeouts
- HPA tuning
- connection pool sizes in app config
- worker concurrency
- ingress or route timeouts where delegated
- Service type and exposure choices

### Cluster-level tuning

Usually requires cluster-admin or platform-owner access:

- CNI settings
- MTU changes
- kube-proxy mode or implementation details
- conntrack sizing
- DNS architecture changes such as NodeLocal DNSCache
- kubelet, CRI-O, or kernel tuning
- OpenShift MachineConfig or runtime configuration

On managed platforms, assume cluster-level tuning is off-limits until proven otherwise.

## Senior-operator habits

- isolate the layer before changing YAML
- prefer one hypothesis at a time
- compare failing and healthy workloads in the same namespace
- measure before and after every tuning change
- do not “tune” around a broken dependency, bad selector, or wrong probe
