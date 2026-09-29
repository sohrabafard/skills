# Build requirements and binary choices

For current branch selection and dated source precedence, consult [version and branch](../10-version-and-branch.md) and [the source ledger](../SOURCES.md).

## The build requirement, which comes before everything else

QUIC needs a TLS library that exposes the BoringSSL-compatible QUIC API. HAProxy's own TLS-stack
documentation, read 2026-07-29, gives this matrix:

| TLS stack | QUIC support | What it costs |
|---|---|---|
| **AWS-LC** | full, including 0-RTT | recommended by the vendor for estates that upgrade frequently |
| **quictls** | full, including 0-RTT | an OpenSSL fork; you track its releases separately |
| **WolfSSL** | full, but needs build options that distributions do not enable by default | you build and maintain it yourself |
| **LibreSSL** | partial; does not implement everything HAProxy needs | not a production answer |
| **stock OpenSSL** | version/build dependent | the current 3.4 manual distinguishes pre-3.5.2 compatibility from newer QUIC APIs; validate the exact build |

Update checked 2026-09-29: the 3.4 manual documents OpenSSL 3.5.2 and later
separately; the July matrix is not a blanket verdict on every OpenSSL 3.x build.
Source: https://docs.haproxy.org/3.4/configuration.html#limited-quic.

For builds using the compatibility path, the documented fallback is the **`limited-quic`** global option, which
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
2. **Use `limited-quic` only with a compiled compatibility layer**
   (`+QUIC +QUIC_OPENSSL_COMPAT`). It cannot add missing build features. Accept
   losing 0-RTT and verify frontend parsing on that binary.
3. **Do not offer HTTP/3.** Serve HTTP/2 over TCP and remove the `quic4@` bind and the `Alt-Svc`
   header. This is the answer when neither of the first two is available, and it is a legitimate
   outcome — HTTP/3 is an optimisation, not a correctness requirement.

Shipping a `quic4@` bind against a build with no QUIC does not fail quietly: the process exits at
startup and `haproxy -c -f` reports the unsupported address. When a QUIC-capable frontend is configured but clients remain on HTTP/2, read [Frontend HTTP/3](./20-frontend-http3.md) for UDP reachability and advertisement checks.
