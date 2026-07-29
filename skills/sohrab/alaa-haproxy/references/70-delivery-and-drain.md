# Delivery and Drain

This file holds the **HAProxy side** of running HAProxy in a container or a pod: paths, signals,
readiness and the drain ordering. Image authorship is decided by `/alaa-docker-production`
(`$alaa-docker-production`); workload, chart and NetworkPolicy authorship by `/alaa-k8s-helm`
(`$alaa-k8s-helm`) and, on Arvan CaaS, by `/caas-arvan-kuber` (`$caas-arvan-kuber`); change
control and rollout proof by `/alaa-controlled-ops` (`$alaa-controlled-ops`).

## Paths HAProxy needs

- The official image reads `/usr/local/etc/haproxy/haproxy.cfg`. Mount the config read-only there.
- **Writable at runtime**, and each one for a stated reason:
  - `/run/haproxy` — the stats socket. Without it the Runtime API does not exist.
  - `/var/lib/haproxy` — the chroot target, when `chroot` is set.
  - `/dev/shm` — only when `shm-stats-file` is in use, and only at the path that directive names.
- Under `readOnlyRootFilesystem: true` every one of those needs an explicit writable mount. The
  failure is at startup and is legible, so this is a fast failure rather than a silent one.
- `chroot` combined with `stats socket /run/haproxy/admin.sock` works because the socket is created
  before the chroot takes effect. Moving the socket path inside the chroot breaks it. The
  interaction is not obvious and is the most common thing to get wrong when adapting
  `01-baseline-http-tls.cfg`.

## Process model and signals

- Start with `-W -db`: master-worker with the master in the foreground so the container's stdout
  is the log. The `master-worker` **global directive** is deprecated from 3.3 and the command-line
  form is the replacement.
- `SIGUSR1` — **soft stop**. Listeners close immediately; existing streams finish.
- `SIGUSR2` — reload in master-worker mode: a new worker takes the listeners, the old one finishes
  its streams and exits. The official image's entrypoint maps `SIGHUP` onto this.
- `SIGTERM` — hard stop. In-flight requests are cut.
- `hard-stop-after <duration>` in `global` bounds how long a soft stop may take before the process
  exits regardless. **Scope: it is process-wide, and it applies to every soft stop and every
  reload, not only to shutdown.** Set it when any proxy in the config can hold a long-lived stream
  — a WebSocket, a `CONNECT` tunnel, a TCP proxy with a minute-scale `timeout client` — because
  without it a reload waits for the longest stream and a rollout stalls behind one idle socket. Set
  it shorter than the platform's own kill deadline, or the platform kills the process mid-drain and
  the bound achieves nothing. On Kubernetes that deadline is `terminationGracePeriodSeconds`.

## Readiness that can actually fail

`monitor-uri <path>` makes a frontend answer that path with 200 without touching a backend.
`monitor fail if <condition>` makes it answer 503 instead. Together they are the only HAProxy
directives that let an external readiness probe observe backend availability.

```
frontend fe_health from <defaults-name>
  bind :8406
  no log
  monitor-uri /haproxy-ready
  monitor fail if { nbsrv(be_app) eq 0 }
```

**A `tcpSocket` probe on the traffic port cannot fail.** HAProxy holds that listener open until
shutdown, so the probe passes while every backend is down and passes right up to the moment the
process exits. A readiness probe that cannot fail cannot drain a pod, which is the whole reason
readiness exists.

Put the health frontend on its **own port**, not on the metrics port. A probe originates from the
kubelet, which is not a pod and is therefore matched by no `namespaceSelector`; sharing the port
with metrics forces a policy that either exposes metrics to the node network or blocks the probe.

Liveness is separate and must not depend on backend health, or a backend incident becomes a
restart loop on the proxy that was still returning errors correctly. A conservative `tcpSocket`
probe on the traffic port is the right shape **for liveness**, which is the case where "the
listener is open" is exactly the question being asked.

## The drain ordering

**Fail readiness, wait for endpoint propagation, then soft-stop.** In that order.

The reason is mechanical: soft-stop **closes the listeners immediately**. If the pod is still in
the Service's endpoint list at that moment, new connections arrive at a closed listener and are
refused. Endpoint removal is asynchronous and is not complete when the `preStop` hook starts.

```
lifecycle:
  preStop:
    exec:
      command: ["/bin/sh", "-ec", "sleep 15; kill -USR1 1 || true"]
```

**Sleep first, signal second.** The reversed form — signal, then sleep — reads naturally as "begin
draining, then wait", and it produces connection refusals on every rollout. They appear to the
client as 502s that no HAProxy log explains, because from HAProxy's side the connection never
arrived.

Sizing, with every value stated rather than implied:

- the sleep must exceed **endpoint propagation time in this cluster**. Measure it; it is a
  property of the CNI and the API server load, not a constant.
- `terminationGracePeriodSeconds` must exceed **sleep + the time in-flight requests need**. In
  `examples/kubernetes/haproxy-deployment.yaml` that is 15 + drain under 45.
- `hard-stop-after`, when set, must be shorter than `terminationGracePeriodSeconds - sleep`.

## Rollout

- A config change must roll the pods. A ConfigMap update lands in the mounted volume minutes later
  and reloads nothing; without a checksum annotation on the pod template the old config keeps
  serving and the deploy appears to have succeeded.
- Keep one branch-aware config per estate. Do not mix experimental 3.3 or 3.4 directives into a
  config that a 3.2 binary also loads, unless the block is behind `.if version_atleast(...)`.
- Rollback is the previous image tag plus the previous config, and both must be loadable by both
  binaries for the duration of the rollout.

What proof a rollout needs before it is allowed to proceed is decided by `/alaa-controlled-ops`
(`$alaa-controlled-ops`).
