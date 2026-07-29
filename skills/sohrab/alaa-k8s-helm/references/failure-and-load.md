# Failure and Load, Expressed in Kubernetes Objects

This file holds only the Kubernetes expression of a reliability decision. `/alaa-reliability-sla` (`$alaa-reliability-sla`) decides **why** a timeout, retry, backoff, circuit breaker, backpressure, or degradation mechanism exists and what shape it takes; bring the number from there and encode it here. `/alaa-services-contract` (`$alaa-services-contract`) owns any shared name or default those numbers are written against.

Every rule below is checkable against a rendered manifest, and `scripts/check_manifests.py` asserts the subset a static file can prove.

## 1. Rollout arithmetic: `replicas`, `maxSurge`, `maxUnavailable`, and the PDB

These four values interact, and three of the four combinations that people write by hand cannot make progress.

Let `R` be `spec.replicas`, `U` be `maxUnavailable` resolved to a pod count, `S` be `maxSurge` resolved to a pod count, and `A` be the PDB's `minAvailable` resolved to a pod count (a PDB with `maxUnavailable: M` behaves as `minAvailable = R - M`).

- **Deadlock condition:** the rollout cannot start when `R - U < A` and `S == 0`. The Deployment controller may take `U` pods down; the eviction API refuses to let availability fall below `A`. With no surge there is nowhere to place a replacement first. **Fix by setting `S >= 1`, not by deleting the PDB.**
- **A PDB is only meaningful when `R >= 2`.** With `R == 1` and `minAvailable: 1`, every voluntary disruption is blocked forever, including a node drain the platform initiated, which turns a routine maintenance into a stuck node.
- **Concrete safe defaults for a stateless Deployment**: `R >= 3`, `maxUnavailable: 0`, `maxSurge: 1`, `minAvailable: R - 1`. This makes a rollout strictly additive: a new pod becomes ready before an old one is removed.
- **StatefulSet**: `maxSurge` does not exist. Use `podManagementPolicy: OrderedReady` and accept that the rollout is serial; set `minAvailable: R - 1` and nothing tighter.
- **A PDB does not survive a direct delete.** Deleting a Pod or a Deployment bypasses eviction entirely. A PDB constrains drains and evictions, not `kubectl delete`.

## 2. Shutdown: `terminationGracePeriodSeconds`, `preStop`, and the endpoint-removal race

When a Pod is deleted, two things start at the same time and are not ordered with respect to each other: the kubelet sends `SIGTERM`, and the endpoint controller removes the Pod from its EndpointSlice. Every proxy, ingress controller, and client that caches endpoints keeps sending traffic for as long as its own propagation takes. A process that exits promptly on `SIGTERM` therefore returns connection resets for that window, and those are the 502s that appear on every rolling update.

The encoding:

1. Give the container a `preStop` sleep at least as long as endpoint propagation on the cluster. Measure it rather than guessing: delete one Pod and time how long a client keeps reaching it. In the absence of a measurement, 5 seconds is the smallest defensible value and the manifest must say it is unmeasured.
2. Set `terminationGracePeriodSeconds` to `preStop sleep + the application's own longest in-flight request + 2 seconds`. If that exceeds the platform's own pod deletion budget, the application must shed longer requests instead.
3. Make the application stop accepting new connections on `SIGTERM` and finish in-flight ones. A `preStop` hook does not do this for it.
4. Make the readiness probe fail as soon as shutdown begins, so that anything that re-reads readiness stops routing immediately.

`terminationGracePeriodSeconds` shorter than the `preStop` sleep is always a defect: the kubelet's `SIGKILL` timer starts when the hook starts, so the hook is cut off and the process never gets its grace.

## 3. Probe thresholds derived from measured behaviour

A probe threshold is a claim about how long the application takes. Derive it, do not copy it.

- **`readinessProbe`** controls traffic eligibility only. Every container in a Deployment or StatefulSet that serves traffic has one. `initialDelaySeconds` stays at 0 when a `startupProbe` exists.
- **`startupProbe`** protects slow boots. Set `failureThreshold × periodSeconds` to at least twice the slowest cold start observed, including cache warm-up and migration waits. Use this instead of inflating the liveness threshold, because an inflated liveness threshold also delays recovery from a real hang for the whole life of the pod.
- **`livenessProbe`** restarts a stuck process, and that is all it is for.
  - It must not call a downstream dependency. A liveness probe that checks the database converts a database outage into a cluster-wide restart storm, and the restarts prevent the connection pool from ever recovering.
  - `failureThreshold × periodSeconds` must exceed the longest self-recovery the application can perform on its own, for example a GC pause or a reconnect backoff. When that time is unknown, omit the liveness probe and say why; a missing liveness probe costs a manual restart, a wrong one costs an outage.
  - `timeoutSeconds` defaults to 1 second, which is shorter than many healthy handlers under load. Set it explicitly.

## 4. Requests, limits, and what happens at the boundary

- **CPU limits throttle; they do not kill.** A container at its CPU limit is slowed by the CFS quota, and latency percentiles move long before any metric named "CPU usage" looks wrong. Watch `container_cpu_cfs_throttled_seconds_total`, not usage. When latency is the SLO, consider a CPU request with no CPU limit, and state that decision in the chart's values so it is deliberate.
- **Memory limits kill.** Exceeding a memory limit is an immediate `OOMKilled` with no grace period and no `preStop`. Memory limit equals memory request is the only combination that makes eviction behaviour predictable.
- **Requests decide scheduling and QoS.** `requests == limits` on every container gives the Pod Guaranteed QoS and takes it out of the first eviction tier. Requests below limits give Burstable, which is evicted before Guaranteed under node pressure.
- **An HPA without CPU requests does nothing**, because CPU utilisation is a percentage of the request. Emitting an HPA with a CPU target and no request is a silently inert autoscaler.
- Deriving the numbers themselves is `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) for the complexity budget and `/alaa-reliability-sla` (`$alaa-reliability-sla`) for the headroom target. This file only says where they go.

## 5. Load amplification during rollout

Scaling and rollout multiply the load a workload places on everything behind it.

- **Connection pools multiply by replica count.** Total connections to a database are `replicas × pool size per replica`, and during a rollout with `maxSurge: 1` the peak is `(replicas + 1) × pool size`. Size the pool from the backend's connection ceiling divided by the maximum replica count the HPA permits, plus surge, not from a per-process default.
- **`maxReplicas` is a budget, not a ceiling on ambition.** Set it from the smallest downstream limit the workload can exhaust, and record which limit that is in a values comment.
- **A readiness probe that passes before warm-up finishes turns a scale-out into a latency spike**, because the new replica takes its share of traffic with a cold cache and an empty pool. Make readiness assert warm-up completion, not process liveness.
- **Cron and Job fan-out is not covered by the HPA.** A CronJob with `concurrencyPolicy: Allow` and a schedule shorter than its runtime accumulates parallel Jobs until quota stops it. Set `concurrencyPolicy: Forbid` unless overlap is intended, and always set `backoffLimit` and `activeDeadlineSeconds`.

## 6. When a chart dependency is gone

A chart that declares a dependency inherits its failure. State, per dependency, what the workload does when it is absent:

- If the workload cannot serve any request without it, the readiness probe fails and the Service stops routing. That is fail-closed and `/alaa-security-review` (`$alaa-security-review`) owns the decision when the dependency is an authorisation or policy check.
- If the workload can serve a reduced answer, readiness stays true and the degradation is reported as a metric. That is fail-open and `/alaa-reliability-sla` (`$alaa-reliability-sla`) owns it.
- The discriminating question: *when this dependency cannot answer, does proceeding without it let something through that must not get through?* If yes, fail closed.
- An `initContainer` that waits for a dependency converts a dependency outage into `Pod Pending` with no logs from the application. Give it a bounded wait and a message that names the dependency.

## 7. Degraded-dependency playbook

Symptom: the workload is Running and Ready, error rate is up, and no pod restarted.

1. Confirm the pods are actually receiving traffic: `kubectl -n NS get endpointslices -o wide` shows ready backends.
2. Rule out throttling before touching the application: `kubectl -n NS top pod --containers` alongside the throttling counter, because throttled CPU looks like a slow dependency from inside the process.
3. Identify the dependency from the application's own error output, not from the layer model: `kubectl -n NS logs POD --since=15m | grep -i 'timeout\|refused\|deadline'`.
4. Test reachability from inside the workload rather than from the ingress: `kubectl -n NS exec POD -- sh -c 'getent hosts HOST'` and a single request with a short timeout.
5. Only then decide whether the correct action is to shed load, to raise a timeout, or to fail closed — and that decision belongs to `/alaa-reliability-sla` (`$alaa-reliability-sla`). Do not raise a timeout to make an error disappear; that converts a fast failure into a queue.
