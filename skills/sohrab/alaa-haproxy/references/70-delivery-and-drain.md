# Delivery and Drain

This file holds the **HAProxy side** of running HAProxy in a container or a pod: paths, signals,
readiness and the drain ordering. Image authorship is decided by `/alaa-docker-production`; workload, chart and NetworkPolicy authorship by `/alaa-k8s-helm` and, on Arvan CaaS, by `/caas-arvan-kuber`; change
control and rollout proof by `/alaa-controlled-ops`.

## Runtime routes

When mounting or signaling the process, read [Paths and signals](70-delivery-and-drain/10-paths-and-signals.md) for writable directories, master-worker reload and bounded soft stop.
When implementing probes, read [Readiness and liveness](70-delivery-and-drain/20-readiness.md) for backend-aware readiness, port reachability and restart-loop prevention.
When draining or rolling instances, read [Drain and rollout](70-delivery-and-drain/30-drain-and-rollout.md) for endpoint propagation, soft-stop ordering, recovery and rollback compatibility.
