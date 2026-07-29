# Rate Limiting, Stick Tables and Peers

## The rate-limit key must be the identity the trust boundary establishes

Not `src` by default. `src` is the address of whatever opened the TCP connection, which is the
client only when the client opened it.

| Topology | Correct key | What must also be true |
|---|---|---|
| clients reach the listener directly | `src` | `accept-proxy` is **absent** from the `bind` line |
| a PROXY-protocol load balancer in front | `src` | `accept-proxy` is present **and** the listener is unreachable from anything but that load balancer |
| an `X-Forwarded-For` load balancer in front | the right-most **untrusted** hop | never `req.hdr(x-forwarded-for)` unqualified: the client supplies the left-hand entries |

Both wrong answers fail in a way the config check cannot see:

- **`src` behind a load balancer with no `accept-proxy`** collapses every client into one table
  entry per load-balancer address. The first such address to cross the threshold returns 429 to
  everyone behind it. The limiter becomes a self-inflicted outage and it fires precisely under
  load, which is the one moment it must not.
- **`accept-proxy` on a listener untrusted clients can reach** hands the client a free choice of
  source address, because the PROXY header is an unauthenticated assertion HAProxy trusts
  unconditionally. The attacker gets a fresh table entry per forged address and bypasses the limit
  entirely, and can also drive a chosen victim's penalty counter to the deny threshold.

**Every listener carrying `accept-proxy` must be unreachable except from its specific upstream.**
That obligation lands in a NetworkPolicy, a security group or a firewall — not in the HAProxy
config, which cannot express it. `examples/kubernetes/haproxy-networkpolicy.yaml` is where this
bundle expresses it. Whether the control is adequate is decided by `/alaa-security-review`
(`$alaa-security-review`).

## Sizing a stick table, and what happens when it is full

`stick-table type ip size <N> expire <T> store <counters>`.

- `size` is a **count of entries**, not bytes. Size it for the peak number of **distinct keys**
  that can be live within `expire`, which is unrelated to the peak request rate.
- Each entry costs roughly the key size plus the stored counters; the practical planning number is
  tens of bytes to a few hundred bytes per entry, so a `500k` IP table with three counters is on
  the order of tens of megabytes of resident memory. Measure it with `show table` under load
  rather than trusting an estimate.
- **At saturation HAProxy evicts the least recently used entry.** That is the attacker who has
  just gone quiet for a moment. An undersized table therefore does not report an error — it
  quietly forgets the thing it was tracking, and the abuser returns to a clean counter.
- `expire` must be comfortably longer than the measurement window in the counters. `expire 30m`
  with `http_req_rate(10s)` keeps a penalty counter alive for thirty minutes, which is deliberate
  for a penalty and wrong for a rate.

`show table <name>` on the Runtime API dumps entries and is how you confirm the key is what you
think it is. Run it once against real traffic before trusting any limiter.

## Peers: what replication does and does not do

`12-peers-global-rate-limit.cfg` is the worked file and its header states the three preconditions.
This section states the mechanism.

### Peers replicate. They do not sum.

A node pushes an updated entry to its connected peers, and a receiving peer applies the received
value to its local entry. **There is no aggregation step.** The vendor's own product boundary
confirms it: HAProxy Enterprise ships a Global Profiling Engine whose entire purpose is the
summation that peers does not perform — it takes two requests seen on one balancer and three on
another and pushes the total of five to both. If plain peers summed counters, that module would
have nothing to do.

The consequence: **a threshold in a peered config is a per-node threshold.** A cluster of N nodes
admits up to N times it. Set the per-node value to `global_budget / node_count` and state the node
count the file assumes, as a comment in the file, because nothing else in the system records it.

### When a peer is unreachable, the limit fails open by exactly the node count

Each node keeps counting only what it sees. A client spreading requests across two nodes is
measured at roughly half its true rate on each, so the admitted rate rises toward `2 x threshold`
while every node believes it is enforcing `threshold`. On three nodes it is `3 x`.

**Nothing in the config, the access log or the metrics reports this.** The rate looks normal
because each node's view of it is normal. The one command that shows it is:

```
echo "show peers" | socat stdio /run/haproxy/admin.sock
```

A healthy remote entry reads `(remote,active)` with a recent `last_acked` and rising `tx_hbt` and
`rx_hbt` heartbeat counters. A dead session does not. **Alert on the peer session, not on the
request rate**, because the request rate is the signal that will not move.

On reconnect there is no catch-up: peers exchange current entry state, not a journal, so requests
admitted during the partition are simply gone from the counters. In the other direction, an
`expire` that outlives the measurement window means a stale penalty counter replicated from a
recovering peer can re-block a client that has behaved for the whole partition.

### Deciding what to do about it

`alaa-haproxy` states the mechanical fact — a peer outage multiplies the admitted rate by the node
count — and does not decide the response. Ask the discriminating question: **when this dependency
cannot answer, does proceeding without it let something through that must not get through?**

- If the limiter protects a backend from overload, the answer is availability. Degradation and
  fail-open doctrine are decided by `/alaa-reliability-sla` (`$alaa-reliability-sla`).
- If the limiter is the only control in front of a credential endpoint, the answer is yes,
  something gets through. Fail-closed doctrine is decided by `/alaa-security-review`
  (`$alaa-security-review`).

### A stick-table limit with peers is a damper, not a quota

It converges somewhere between the busiest node's local rate and the true total, it loses
increments when two nodes update the same key concurrently, and it multiplies on partition. That
is enough to blunt abuse and it is not enough to enforce a contractual quota. **If the requirement
is a hard global quota, open-source HAProxy peers cannot provide it.** The requirement then needs
a shared counter store and a design, which is `/alaa-system-design` (`$alaa-system-design`).

## Peers preconditions, restated as rules

Three, each of which fails silently:

1. **The local peer must be identifiable.** HAProxy activates a `peers` section only when one of
   its entries matches the local peer name — the machine hostname by default, overridden by the
   `localpeer` keyword in the `global` section or by the `-L` command-line option. When nothing
   matches, HAProxy does not activate the section: it neither dials nor listens. The config still
   passes `haproxy -c -f`, the process still starts, the table is still created, and the limit
   still works per node in isolation, with no error anywhere. With Kubernetes-generated pod names
   the hostname never matches a hand-written peer name, so `localpeer` or `-L` is mandatory there.
2. **The table identity must match on every node.** Peers replicate a table by name, `type` and
   `size`. A mismatch has the table refused for sync while everything else runs normally.
   Declaring the table inside the `peers` section makes the shared identity one reviewable line.
3. **The peers port must be authenticated.** The peers protocol carries no authentication of its
   own, and anything that reaches the port can write stick-table entries — raise a victim's
   penalty counter to the deny threshold, or lower an attacker's counter to evade the limit. Put
   TLS with mutual verification on the `bind` line and on every remote `server` line, and restrict
   the port to the peer set at the network layer as well.

`scripts/check_defaults_scope.py` does not cover these; `scripts/check_examples.py` asserts that
any shipped config with a `peers` section sets `localpeer` and puts `ssl` on the peers `bind`.
