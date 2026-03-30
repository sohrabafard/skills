# Alaa HAProxy Platform Delivery

## Containers

- The official image expects `/usr/local/etc/haproxy/haproxy.cfg`.
- Docker Hub documents that sending `HUP` to the container triggers the image wrapper's graceful reload handling.
- Prefer high container ports and publish them via the Service or host mapping instead of requiring root inside the container.
- If you need privileged ports inside the container, document why and verify the kernel and runtime support the chosen method.
- Keep writable runtime paths explicit, such as `/run/haproxy` and `/var/lib/haproxy`, especially if you enable a read-only root filesystem.

## Kubernetes production pattern

### Base pattern

- Run at least two replicas for externally visible traffic.
- Mount config from a ConfigMap and certificates or sensitive material from a Secret.
- Use a checksum annotation in Helm or a template system so config changes trigger a rollout.
- Prefer `-W -db` in container args for modern worker control and foreground logs.
- Add a `preStop` hook that begins a graceful stop before the pod disappears from Service endpoints.
- Use a PodDisruptionBudget and anti-affinity or topology spread constraints.

### Probes

- Readiness should represent whether the pod can still accept new traffic.
- Liveness should be conservative. Avoid aggressive restarts during temporary backend incidents.
- Startup probes are useful when the config is large, certificates are numerous, or the node is slow.

### Security

- Prefer a non-root container when HAProxy only binds high ports inside the pod.
- Set `allowPrivilegeEscalation: false`.
- Add `readOnlyRootFilesystem: true` only when the required runtime directories are mounted writable.
- Use a NetworkPolicy when the namespace is shared or the HAProxy pod should only talk to specific backends, DNS, and telemetry collectors.

### Observability

- Expose a dedicated metrics endpoint only on a pod-local or cluster-private port.
- If the cluster uses Prometheus Operator, pair the metrics Service with a ServiceMonitor.
- Keep Runtime API on a unix socket, not a network port.

## Helm patterns

- Treat chart values as chart-specific. Translate the patterns, not just the key names.
- Good Helm values usually expose:
  - image repository and tag
  - replica count
  - update strategy
  - resources
  - probes
  - lifecycle hooks
  - extra volumes and mounts
  - Service annotations and type
  - PodDisruptionBudget
  - autoscaling
  - ServiceMonitor or metrics toggles
- Keep config text, maps, and certificate sources separated so small changes remain reviewable.

## CI and CD gates

### Minimum gates

- print `haproxy -vv`
- run `haproxy -c -f ...` on the effective config
- render Helm templates if Helm is involved
- dry-run Kubernetes manifests with `kubectl apply --dry-run=client`

### Better gates

- validate every config example or every config fragment, not only the main file
- check that map files and certificate mounts expected by the config exist in CI fixtures
- render production and staging values separately when they differ materially
- require a rollout status check after deployment
- keep at least one GitLab CI or GitHub Actions example in-repo so agents can adapt from a known-good pattern

### Rollout safety

- prefer rolling changes with a fast rollback path
- keep one branch-aware config per estate when `3.2` and `3.3` behavior differs
- do not mix experimental `3.3` directives into a shared config consumed by `3.2`

## Layered proxy deployment patterns

### External LB -> HAProxy -> app

- The outer load balancer should terminate or pass traffic intentionally.
- If it sends PROXY protocol, HAProxy must accept it.
- Preserve or recreate request correlation IDs at the HAProxy layer.

### External LB -> HAProxy -> internal gateway -> services

- Keep each trust boundary explicit:
  - client identity
  - source IP forwarding
  - request ID
  - TLS termination point
  - mTLS re-establishment if used internally

### HAProxy as a TCP router

- Use TCP mode when the protocol is not HTTP-aware or when the backend must see the original stream untouched.
- Keep health checks protocol-appropriate. A TCP success alone may not be enough for production readiness.

## Operational checklist before deploy

- target branch confirmed: `3.2` or `3.3`
- config syntax checked with the actual binary
- runtime directories and sockets writable
- probes and drain behavior tested
- Service exposure reviewed
- metrics and logs visible from the monitoring stack
- rollback method written down
