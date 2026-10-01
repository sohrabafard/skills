# Drain ordering and rollout

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

When runtime backend membership is used, read `65-dynamic-backends.md` for
reconstruction: a new worker does not inherit dynamic backend definitions.


- A config change must roll the pods. A ConfigMap update lands in the mounted volume minutes later
  and reloads nothing; without a checksum annotation on the pod template the old config keeps
  serving and the deploy appears to have succeeded.
- Keep one branch-aware config per estate. Do not mix experimental 3.3 or 3.4 directives into a
  config that a 3.2 binary also loads, unless the block is behind `.if version_atleast(...)`.
- Rollback is the previous image tag plus the previous config, and both must be loadable by both
  binaries for the duration of the rollout.

What proof a rollout needs before it is allowed to proceed is decided by `/alaa-controlled-ops`.
