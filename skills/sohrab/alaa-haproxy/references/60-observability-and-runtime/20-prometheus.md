# Prometheus exposition

## The Prometheus exporter

Build-dependent: require `+PROMEX` in `haproxy -vv`; a version alone does not enable the exporter.

```
frontend fe_metrics from <defaults-name>
  bind :8405
  no log
  http-request use-service prometheus-exporter if { path /metrics }
  http-request return status 404
```

**Where it binds is a reachability decision with two correct answers, and only two:**

- **loopback**, when the scraper shares the network namespace — a sidecar, or a host-local agent.
  `10-prometheus-runtime-api.cfg`.
- **all interfaces, with the exposure bounded outside HAProxy** by a NetworkPolicy, a security
  group or a firewall, when the scraper is remote. `examples/kubernetes/haproxy-configmap.yaml`.

Binding loopback while a Kubernetes Service or a ServiceMonitor targets that port produces a
target that is down from the first rollout and stays down, with nothing in HAProxy's logs, because
from HAProxy's side nothing is wrong. Whether the resulting exposure is acceptable is decided by
`/alaa-security-review`.

`no log` on the metrics frontend keeps a 30-second scrape interval out of the access log. Without
it the metrics endpoint is the highest-volume entry in the log and buries everything else.

Some counters are gated behind the `extra-counters` scrape parameter, added in 3.0. They are
**absent** from the exposition without it, with no error, so a dashboard panel built on one of them
stays empty and reads as "no traffic". The `scope` parameter restricts the exposition to
`global`, `frontend`, `backend`, `server` or `sticktable`, which is how a large estate keeps
cardinality down.
