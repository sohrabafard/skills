# QUIC and HTTP/3

## The build requirement, which comes before everything else

QUIC needs a TLS library that exposes the BoringSSL-compatible QUIC API. HAProxy's own TLS-stack
documentation, read 2026-07-29, gives this matrix:

| TLS stack | QUIC support | What it costs |
|---|---|---|
| **AWS-LC** | full, including 0-RTT | recommended by the vendor for estates that upgrade frequently |
| **quictls** | full, including 0-RTT | an OpenSSL fork; you track its releases separately |
| **WolfSSL** | full, but needs build options that distributions do not enable by default | you build and maintain it yourself |
| **LibreSSL** | partial; does not implement everything HAProxy needs | not a production answer |
| **stock OpenSSL 3.x** | **not usable for production QUIC** | OpenSSL 3.5 added its own QUIC API, which is not the one every other library implements |

For stock OpenSSL there is one documented fallback: the **`limited-quic`** global option, which
uses a keylog-callback path to give basic **server-side** QUIC. It costs **0-RTT resumption** and
the performance work that the real API allows. It is a way to serve HTTP/3 without changing the TLS
library; it is not equivalent to having one.

**`limited-quic` gives frontend HTTP/3 only.** Verified against a 3.4.0 build made with
`USE_QUIC=1 USE_QUIC_OPENSSL_COMPAT=1` on OpenSSL 3.0.13, on 2026-07-29: the frontend `quic4@`
bind is accepted once `limited-quic` is set, and a `server ... quic4@` line on the same binary is
rejected with

```
'server be_h3_origin/app1' : The SSL stack does not provide a support for QUIC server 'app1'
```

Without `limited-quic` the frontend bind itself is rejected, and HAProxy names the option in the
message:

```
Binding [...] for frontend fe_h3: this SSL library does not support the QUIC protocol.
A limited compatibility layer may be enabled using the "limited-quic" global option if desired.
```

The build flag that selects this path is `USE_QUIC_OPENSSL_COMPAT`, and `haproxy -vv` reports it
in the feature list as `+QUIC_OPENSSL_COMPAT` beside `+QUIC`. A config using backend HTTP/3 should
therefore assert the absence of that token, not merely the presence of QUIC; the
`# Requires-build: QUIC !QUIC_OPENSSL_COMPAT` header in `14-http3-backend-3.3.cfg` is how
`scripts/check_examples.py` is told to skip it rather than report a false defect.

## What to do when `haproxy -vv` reports no QUIC

`haproxy -vv` reports the build options and the TLS library. When QUIC is absent, there are
exactly three correct outcomes and "ship it and see" is not among them:

1. **Change the binary.** Use an image built against AWS-LC or quictls. This is the answer for a
   new deployment, because it is the only one that gets 0-RTT.
2. **Add `limited-quic`** to `global` and accept losing 0-RTT. This is the answer when the TLS
   library is fixed by a platform decision you do not own.
3. **Do not offer HTTP/3.** Serve HTTP/2 over TCP and remove the `quic4@` bind and the `Alt-Svc`
   header. This is the answer when neither of the first two is available, and it is a legitimate
   outcome — HTTP/3 is an optimisation, not a correctness requirement.

Shipping a `quic4@` bind against a build with no QUIC does not fail quietly: the process exits at
startup and `haproxy -c -f` reports the unsupported address. The quiet failure is the network one,
below.

## Frontend HTTP/3

`03-quic-http3.cfg`. Three things must all be true or clients silently stay on HTTP/2:

- a `quic4@` (or `quic6@`) `bind` line exists alongside the TCP listener;
- **UDP on that port is open end to end**, including every firewall, security group and cloud load
  balancer in the path. A path that passes TCP 443 and drops UDP 443 is the single most common
  cause of an HTTP/3 rollout that appears to do nothing;
- an `Alt-Svc` response header advertises the endpoint, because most clients do not attempt QUIC
  unless told the server speaks it.

**Keep the TCP listener.** HTTP/3 is advertised, never required: a client that cannot reach UDP
must have somewhere to fall back to, and that fallback is what makes a QUIC misconfiguration a
performance event rather than an outage.

Confirm the rollout from the `alpn` or protocol field in the access log, not from the config. The
config proves the listener exists; only the log proves a client used it.

## Backend HTTP/3

`14-http3-backend-3.3.cfg`. 3.3 and later, still experimental, so
`expose-experimental-directives` must precede its first use. `server ... quic4@<addr>` sends HTTP/3
to the origin.

Two differences from the frontend case:

- The UDP path to the **origin** is a different firewall rule from the client-side one and is
  frequently forgotten.
- **There is no fallback.** If the origin does not speak HTTP/3 the server stays down and the
  backend loses that capacity outright. That fails hard rather than silently, which is the safer
  shape, but it is not what an operator expects from an "enable HTTP/3" change.

An experimental directive can change name or behaviour across branches, so a config that starts on
3.3 may not start on 3.4 or 3.5. Re-run `haproxy -c -f` against the new binary **as part of** the
upgrade, not after it.

## Tuning and naming

`tune.quic.*` settings bound memory and stream behaviour, and **the namespace has been
reorganised twice**: 3.3 renamed the `tune.quic.frontend.*` family to `tune.quic.fe.*` and renamed
`no-quic` to `tune.quic.listen`, and 3.4 reorganised again — `tune.quic.fe.stream.data-ratio` and
`tune.quic.mem.tx-max` on 3.4 are not the names 3.2 or 3.3 accepted. A name written for one branch
is an `unknown keyword` startup error on another.

Do not copy a `tune.quic.*` line out of a document. Enumerate what the binary in front of you
actually has:

```
haproxy -dKcfg -c -f /dev/null | grep tune.quic
```

A mixed estate puts any such block behind `.if version_atleast(3.4)` or the equivalent for its own
branches. `03-quic-http3.cfg` deliberately ships no tuning line for this reason.

3.4 adds QMux, experimental QUIC over TCP, for networks that block UDP entirely. It is a different
mechanism from `limited-quic`: QMux changes the transport, `limited-quic` changes the TLS
integration.

Whether the latency improvement HTTP/3 buys is worth the operational surface is a service-level
question and belongs to `/alaa-reliability-sla` (`$alaa-reliability-sla`).
