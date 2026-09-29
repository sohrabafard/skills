# Connection capacity and reuse

Open this procedure when the task matches its trigger. The topic map routes to this file.

For current version-sensitive claims, follow the dated [source ledger](../SOURCES.md).

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
