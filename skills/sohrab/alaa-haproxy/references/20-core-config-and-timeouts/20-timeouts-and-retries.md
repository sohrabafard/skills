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

`retries N` defaults to retrying failed new connection attempts. `retry-on`
extends the triggering failures and can replay an HTTP request; it requires the
workload's replay/idempotency decision from `/alaa-reliability-sla`.
`option redispatch` allows breaking persistence to select another usable server;
without an argument, this normally applies on the last retry, not every attempt.
Health and available-server state also affect selection. Do not promise that all
retries use the same failed server or that a retry is a safe request replay.

This package's examples pair retries with redispatch as a reviewable engineering
pattern, enforced by HP-EX-009. That is not an upstream parsing restriction.
