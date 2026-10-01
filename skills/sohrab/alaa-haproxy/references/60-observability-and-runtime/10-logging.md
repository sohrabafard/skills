# HTTP log formats

## The `log-format` string

Emit the fields `/alaa-services-contract` names. The line that emits
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
be recorded at all is decided by `/alaa-security-review`.
