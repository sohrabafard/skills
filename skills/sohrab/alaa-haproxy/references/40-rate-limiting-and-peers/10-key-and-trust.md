# Rate-limit identity and trust

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
bundle expresses it. Whether the control is adequate is decided by `/alaa-security-review`.
