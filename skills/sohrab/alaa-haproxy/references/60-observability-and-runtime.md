# Observability and the Runtime API

## What this file owns

The **directive half**: how a signal is emitted, where the exporter binds, what the Runtime API
exposes, how a log line is assembled. It does not own which signals are required, what alerts on
them, or what they are called.

- **Which signal is required and what gates on it** — `/alaa-observability-soc`
  (`$alaa-observability-soc`).
- **Every shared name and value** — the log field names, the metric catalog, `OTEL_*` names and
  defaults — `/alaa-services-contract` (`$alaa-services-contract`).

## The `log-format` string

Emit the fields `/alaa-services-contract` (`$alaa-services-contract`) names. The line that emits
them is written here. `option httplog` gives the default HTTP format; a `log-format` line replaces
it entirely, so a custom format must re-state everything it still wants.

Useful field expressions, with what each answers:

| Expression | Answers |
|---|---|
| `%ci:%cp` | the connection's source address, after `accept-proxy` has rewritten it |
| `%[capture.req.hdr(0)]` or `%{+Q}[req.hdr(x-request-id)]` | the correlation identifier |
| `%f` / `%b` / `%s` | frontend, backend, server that handled it |
| `%ST` | status code returned to the client |
| `%Tq/%Tw/%Tc/%Tr/%Ta` | request, **queue wait**, connect, response, total — the queue field is what separates a saturated backend from a slow one |
| `%[term_events]` | a structured record of what terminated the stream, which is the fastest path from "502s appeared" to "which side closed" |
| `%[ssl_c_verify]`, `%{+Q}[ssl_c_s_dn]` | client-certificate outcome, which the HTTP log otherwise never shows |
| `%[ssl_fc_protocol]`, `%[ssl_fc_alpn]` | negotiated TLS version and protocol, which is how an HTTP/3 rollout is confirmed |

Preserve a request identifier at the edge and pass it downstream: `http-request del-header` the
inbound copy, then `http-request set-header` a generated one, so a client cannot choose the
identifier that will appear in the application's logs.

**Do not log a full `Authorization` header, a cookie, or a request body.** The positive
replacement, when the incident needs to distinguish callers, is a stable identifier that is not a
credential: `%[req.hdr(authorization),lower,field(1,' ')]` records the scheme without the token,
and a client-certificate serial or subject identifies an mTLS caller. Which certificate fields may
be recorded at all is decided by `/alaa-security-review` (`$alaa-security-review`).

## The Prometheus exporter

Compiled in by default; confirm with `haproxy -vv`.

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
`/alaa-security-review` (`$alaa-security-review`).

`no log` on the metrics frontend keeps a 30-second scrape interval out of the access log. Without
it the metrics endpoint is the highest-volume entry in the log and buries everything else.

Some counters are gated behind the `extra-counters` scrape parameter, added in 3.0. They are
**absent** from the exposition without it, with no error, so a dashboard panel built on one of them
stays empty and reads as "no traffic". The `scope` parameter restricts the exposition to
`global`, `frontend`, `backend`, `server` or `sticktable`, which is how a large estate keeps
cardinality down.

## The Runtime API

The admin socket is a full administrative control plane: it disables servers, changes weights,
replaces certificates and dumps the stick tables. **Reaching it is equivalent to reaching the
config.** It stays a unix socket with `mode 660`; putting it on a TCP listener is the single
largest exposure change this skill can make and it goes to `/alaa-security-review`
(`$alaa-security-review`) before it is made.

First checks, in the order they answer a question:

| Command | Answers |
|---|---|
| `show info` | is this the process and build I think it is; how many connections, how much memory |
| `show stat` | per-proxy counters: `econ`, `eresp`, `qcur`, `wretr`, `scur`, `smax` |
| `show errors` | the last protocol errors, with the offending bytes — the only place a malformed request or a failed handshake is legible |
| `show events` | the ring buffer of recent events |
| `show servers state` | why a server is down and how long it has been |
| `show table <name>` | what a stick table actually contains, which is how you confirm the limiter's key |
| `show peers` | whether peer sessions are up; see `40-rate-limiting-and-peers.md` |
| `show cache` | what the object cache actually holds |
| `show stat typed` | whether each metric is volatile or persistent, which is how a `shm-stats-file` rollout is confirmed |

## Persistent stats across reloads

3.3 and later, experimental, `expose-experimental-directives` plus `shm-stats-file <path>` in
`global` and a unique `guid` on each proxy and server. `15-persistent-stats-3.3.cfg`.

- The path must be **writable**. Under `readOnlyRootFilesystem: true` that means an explicit
  writable mount at that path.
- Counters survive a **reload**. They do not survive a **restart**, and they do not survive the
  shared-memory file being removed. A dashboard built on the assumption of continuity still shows
  a discontinuity after a node restart, and that discontinuity is indistinguishable from a traffic
  drop unless the panel is annotated.
- A `guid` is a durable series identifier. Changing one renames the series and breaks history
  exactly as if the counter had reset; treat a guid change as a dashboard migration. A duplicate
  guid is a startup error.

Whether the continuity is required at all is decided by `/alaa-observability-soc`
(`$alaa-observability-soc`).

## Tracing

3.3 adds `acme` and `ssl` trace sources; 3.4 adds native OpenTelemetry and deprecates OpenTracing,
which is removed in 3.5.

Runtime tracing is expensive and it reads request content. Turn it on for a bounded investigation
with a stated end, and turn it off when that investigation ends — not "after the incident", which
is not an observable condition. The mechanical form of bounded is to write the disable command
into the incident record at the same moment you write the enable command.

Whether tracing is required, and what the trace fields are called, is decided by
`/alaa-observability-soc` (`$alaa-observability-soc`) and `/alaa-services-contract`
(`$alaa-services-contract`).
