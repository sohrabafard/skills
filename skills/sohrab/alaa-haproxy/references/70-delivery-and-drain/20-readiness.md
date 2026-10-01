# Readiness and liveness

## Readiness that can actually fail

`monitor-uri <path>` makes a frontend answer that path with 200 without touching a backend.
`monitor fail if <condition>` makes it answer 503 instead. They provide one native way for an external readiness probe to observe backend
availability; conditional `http-request return` can express it too.

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
