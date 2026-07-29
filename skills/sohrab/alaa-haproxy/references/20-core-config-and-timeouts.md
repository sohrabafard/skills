# Core Config Structure and Timeouts

## The `defaults` association rule

**A `defaults` section applies only to the proxies that follow it, up to the next `defaults`
section, or to the proxies that name it with `from`. It is never file-wide.**

Four consequences, all of which cost a production incident when the rule is not known:

1. A `frontend`, `backend` or `listen` with no `from` inherits the **nearest preceding**
   `defaults`. A `defaults` further up the file has already been superseded.
2. A `defaults` section does not implicitly inherit from another `defaults` section. Each one
   conveys only what it directly specifies. Explicit inheritance is written `defaults b from a`.
3. A `defaults` section can be named, and a proxy selects it with `frontend fe from base`,
   `backend be from base` or `listen l from base`. Naming works on 3.2, 3.3 and 3.4.
4. From 3.3, a duplicate `defaults` **name** is a startup error. Naming is therefore cheap: the
   collision that naming could introduce is caught by the parser.

**The rule for this skill: any config file that declares a `defaults` section names every one of
them and gives every `frontend`, `backend` and `listen` an explicit `from`.** A file that
declares no `defaults` at all is exempt, because there is nothing to associate. Positional
association is not forbidden by HAProxy and it is forbidden here, because it cannot be reviewed:
the reader has to hold the whole file in their head to know which block governs a proxy.
`scripts/check_defaults_scope.py` reports a violation.

### Why this is the rule and not a preference

Composing two configs is the normal way to build one. Take a file whose `defaults` sets
`mode http`, `timeout client 30s`, `option forwardfor` and `retries 3`, append a second file
whose `defaults` sets `mode tcp` and `timeout client 1m`, and the result **parses, starts and
serves traffic**, while every proxy after the second `defaults` silently runs in TCP mode, with
different timeouts, and with no `option forwardfor`. Nothing warns.

Observed with a real binary:

```
$ haproxy -c -f concatenated.cfg
[ALERT] config : http frontend 'fe_a' (concatenated.cfg:8) tries to use incompatible
        tcp backend 'be_a' (concatenated.cfg:22) as its default backend (see 'mode').
```

That is the loud case, and it only happens when the mode mismatch crosses a `default_backend`
edge. The quiet case is the dangerous one: a `defaults`-level `http-request del-header`, a
`timeout http-request`, an `option forwardfor` or a `retries` value that an agent adds to the
`defaults` it can see at the top of the file, believing it now applies to the proxy it is
protecting, when a second `defaults` further down has already taken over. The header keeps
arriving, the timeout keeps being the wrong one, and the config is valid.

Worked example, both halves in one file, with each proxy stating its own defaults:

```
defaults http_edge
  mode http
  timeout connect 5s
  timeout client 30s
  timeout server 30s
  option forwardfor

defaults tcp_l4
  mode tcp
  timeout connect 5s
  timeout client 1m
  timeout server 1m

frontend fe_web from http_edge     # forwardfor applies here
  bind :8080
  default_backend be_web

frontend fe_db from tcp_l4         # and not here, visibly
  bind :3306
  default_backend be_db
```

## Timeouts

Set all of these explicitly. An unset timeout is not "no timeout"; it inherits or it defaults,
and which of those happened is exactly the thing the reader cannot see.

| Timeout | What it bounds | Symptom when it is wrong |
|---|---|---|
| `timeout connect` | the TCP connect to a server | too high: a dead server holds a request for the full value on every retry |
| `timeout client` | client inactivity | too low: long polling and uploads are cut mid-transfer |
| `timeout server` | server inactivity | too low: slow endpoints return 504 while completing normally at the origin |
| `timeout http-request` | receiving the complete request headers | absent: a slow-header client holds a connection indefinitely |
| `timeout http-keep-alive` | idle time between requests on a kept-alive connection | too high: idle connections consume file descriptors |
| `timeout queue` | how long a request waits for a server slot | absent: requests queue until `timeout server`, so queue pressure reads as backend slowness |
| `timeout tunnel` | WebSocket and CONNECT streams after the upgrade | absent: the stream inherits `timeout client`/`timeout server` and long-lived sockets are cut |

**What the values should be is not decided here.** A timeout value follows from the dependency's
own latency budget and from what the caller is allowed to do when it expires, and that is decided
by `/alaa-reliability-sla` (`$alaa-reliability-sla`). This skill states which timeouts exist, what
each one bounds, and how the directive is written.

## Retries and redispatch

`retries N` alone re-sends the request **to the same server**. `option redispatch` is what makes a
retry pick a different server. A config with `retries 3` and no `option redispatch` sends all
three attempts into the same failure and returns 503 with three times the latency.

Every backend in this skill's examples carries both. A retry is only safe on an idempotent
request; whether the request is idempotent, and whether retrying is the correct response at all,
is decided by `/alaa-reliability-sla` (`$alaa-reliability-sla`).

## Connection ceilings and queueing

Four limits, and each one bounds a different thing:

- `maxconn` in `global` — the process-wide connection ceiling. It sizes the file-descriptor
  requirement. Without it HAProxy uses a build default that is unrelated to the machine.
- `maxconn` on a `frontend` — the ceiling for that listener. Above it, new connections are held
  in the kernel accept queue rather than accepted, which is backpressure and is the point.
- `maxconn` on a `server` — the concurrent requests that server will take. Above it, requests
  queue in HAProxy.
- `maxqueue` on a `server` — how many may wait. Beyond it, HAProxy redispatches or returns 503
  rather than queueing without bound. **A `maxconn` with no `maxqueue` is an unbounded queue**,
  and an unbounded queue converts a slow backend into a memory problem in the proxy.

`strict-maxconn` (3.2) makes `maxconn` a hard ceiling that HAProxy will not exceed even when it
would otherwise open one more connection to keep a queued request moving.

`http-request pause` holds a stream and its buffers instead of releasing them. Under a
connection-exhaustion flood it amplifies the pressure it was added to relieve. It is not the first
response to a flood; a deny is. Use `pause` only against a client whose own concurrency already
bounds what it can hold.

## Connection reuse

`http-reuse` decides whether a backend connection opened for one client may carry another
client's request:

- `never` — one backend connection per client connection. Correct when the backend derives
  identity from the connection, for example with `send-proxy-v2` carrying a client certificate.
- `safe` — reuse only connections already proven reusable by a prior successful request. This is
  the value to write when the answer is not obviously one of the other three.
- `aggressive` and `always` — reuse earlier and more widely, which raises the chance of a request
  landing on a connection the origin has already closed. Pair with `idle-ping` on the `server`
  line and with `option redispatch`, or the first request after an origin-side idle timeout fails.

The observable that says reuse is misconfigured is a rising `wretr` in `show stat` with no change
in backend error rate.

## Maps instead of ACL chains

A chain of ACLs is evaluated in order, so its cost grows with the number of rules. A map is a hash
lookup and stays flat as it grows. **Any host or path routing table that will exceed roughly a
dozen entries, or that will be edited by someone who is not editing the config, is a map file, not
an ACL chain.** Below that, an ACL chain is clearer and the cost difference is not measurable.

A map is loaded at startup and is not re-read when the file changes. A live change is `add map`,
`del map` or `set map` on the Runtime API and is lost on restart unless the file is updated too.
Complexity budgets in general are decided by `/alaa-algorithms-data-structures`
(`$alaa-algorithms-data-structures`).

## Environment variables and the preprocessor

HAProxy expands `${NAME}` in the config file, and `${NAME-default}` supplies a default. Both work
only when the whole argument is enclosed in double quotes; unquoted, `bind :${PORT-8443}` is
parsed as a port offset and fails. `"${NAME[*]}"` splits the value on spaces into separate
arguments, which is what a list-valued setting such as `compression type` needs.

**An unset variable with no default expands to nothing and produces a parse error at
`haproxy -c -f` time.** That is the fail-closed shape and it is why a value that must be supplied
gets no default.

For a value whose absence must produce a message rather than a parse error, use the preprocessor:

```
.if !defined(HAPROXY_ASSET_PREFIX)
.alert "HAPROXY_ASSET_PREFIX is not set. It is decided by alaa-frontend-devops."
.endif
```

`.if` also takes `defined(NAME)`, `feature(NAME)` for a build option and `version_atleast(X.Y)`
for a branch test, with `.elif`, `.else` and `.endif`. `version_atleast` is how one file serves a
mixed estate.

Which variable name expresses a given runtime value, when the config is generated rather than
written, is decided by `/service-runtime-kit-governance` (`$service-runtime-kit-governance`). The
`HAPROXY_*` names in this skill's examples are this skill's own convention for standalone configs.

## Diagnosing by symptom

### 502 or 503 in bursts

Look at `show stat` first: `econ` (connection errors), `eresp` (response errors), `qcur` (queue
depth) and `wretr` (retries) separate a backend that is down from a backend that is saturated.
Add `%[term_events]` to the log format when the counters do not distinguish them. Smallest first
step: confirm `option redispatch` is present, because without it a single failed server produces
this exact pattern. Escalate to `/alaa-reliability-sla` (`$alaa-reliability-sla`) when the answer
is that the backend has no capacity, because that is a degradation decision, not a proxy one.

### Tail latency spikes with normal median

Look at rule count and regex cost on the hot path, then at queue depth (`qtime` in the log), then
at CPU. Smallest first step: move any repeated ACL chain to a map. Peer sync is a candidate only
when `peers` is configured and `show peers` shows recent activity. Escalate to
`/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) when the cost is in the
shape of the lookup rather than in its constant.

### Too many open files

The ceiling is the minimum of `global maxconn` implied descriptors, the process `RLIMIT_NOFILE`,
and the container or service-manager limit. All three must be raised together; raising one is the
usual reason this recurs after it was "fixed". Smallest first step: read `ulimit -n` inside the
running container, not on the host. Container limits are decided by `/alaa-docker-production`
(`$alaa-docker-production`) and `/alaa-k8s-helm` (`$alaa-k8s-helm`).

### Backends flapping in and out of rotation

Read `show servers state`. Resolver hold times shorter than the churn rate cause this; so does a
health check stricter than the backend's own startup. Smallest first step: raise `hold valid`
before raising `resolve_retries`, because retries lengthen the outage while hold length prevents
it. Escalate to `/alaa-system-design` (`$alaa-system-design`) when the backend's addresses change
faster than any hold time can absorb.
