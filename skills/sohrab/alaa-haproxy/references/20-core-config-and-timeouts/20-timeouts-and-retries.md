# Timeouts and retries

Open this procedure when the task matches its trigger. The topic map routes to this file.

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
| `timeout queue` | how long a request waits for a server slot | absent: inherits `timeout connect`; set a deliberate queue budget |
| `timeout tunnel` | WebSocket and CONNECT streams after the upgrade | absent: the stream inherits `timeout client`/`timeout server` and long-lived sockets are cut |

**What the values should be is not decided here.** A timeout value follows from the dependency's
own latency budget and from what the caller is allowed to do when it expires, and that is decided
by `/alaa-reliability-sla`. This skill states which timeouts exist, what
each one bounds, and how the directive is written.

## Retries and redispatch

`retries N` alone re-sends the request **to the same server**. `option redispatch` is what makes a
retry pick a different server. A config with `retries 3` and no `option redispatch` sends all
three attempts into the same failure and returns 503 with three times the latency.

Every backend in this skill's examples carries both. A retry is only safe on an idempotent
request; whether the request is idempotent, and whether retrying is the correct response at all,
is decided by `/alaa-reliability-sla`.
