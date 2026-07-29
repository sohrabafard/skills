# TLS, mTLS and Certificates

## Loading certificates

`crt-store` (3.0 and later) declares a certificate store with a base path and named aliases;
`ssl-f-use` (3.2 and later) attaches a stored certificate to a frontend together with the TLS
policy that applies to it. Together they replace a `bind ... crt <path>` line whose policy is
implicit in global defaults.

Use them when the frontend serves **more than one certificate**, or when **one certificate needs a
different policy from the others** — a legacy tenant pinned to TLS 1.2 while everything else is
1.3-only, for example. A frontend with exactly one certificate and no per-certificate policy is
correctly written as `bind ... ssl crt <path>`; adding a store there is indirection with no
reader benefit. `01-baseline-http-tls.cfg` shows the store form; `10-prometheus-runtime-api.cfg`
shows the direct form.

Certificate material never enters git. Where it comes from — a Secret, a mounted volume, an
issuer — is decided by `/alaa-k8s-helm` (`$alaa-k8s-helm`) and `/alaa-security-review`
(`$alaa-security-review`).

## TLS version and cipher policy

Set `ssl-default-bind-options ssl-min-ver` in `global` so the floor is one line and applies to
every listener that does not override it. Keep the TLS 1.2 cipher list
(`ssl-default-bind-ciphers`) and the TLS 1.3 suite list (`ssl-default-bind-ciphersuites`)
separate: they are different negotiation mechanisms and a value placed in the wrong one is
ignored without an error.

`no-tls-tickets` disables session tickets. Write it unless someone has measured that resumption
matters for this workload, because a ticket key that is never rotated makes every session it
protected decryptable by anyone who later obtains the key, and rotation is an operational process
that must exist before tickets are turned on. If tickets are enabled, the rotation path is written
down and owned before the change ships; that is a security decision and it belongs to
`/alaa-security-review` (`$alaa-security-review`).

## SNI on the client side

`strict-sni` on a `bind` line rejects a handshake whose SNI matches no loaded certificate, rather
than serving the first certificate. Write it on any frontend serving more than one tenant: without
it, a client that asks for tenant A's name and gets tenant B's certificate has learned that tenant
B is hosted here. The cost is that a client with no SNI at all — which in practice means a very
old client or a raw IP connection — is rejected rather than served a default.

## Client certificates

`bind ... ssl ca-file <bundle> verify required` rejects the handshake when the client presents no
certificate or presents one that does not chain to the bundle. `verify optional` completes the
handshake and lets a rule decide, which is what you want when only part of the surface needs a
certificate.

Two things `verify required` does not do:

- **It says nothing about revocation.** Add `crl-file` for a CRL, or an OCSP source, if a
  compromised client certificate must stop working before it expires. Whether that is required is
  decided by `/alaa-security-review` (`$alaa-security-review`).
- **It produces no HTTP status.** A rejected client sees a TLS alert and the HTTP access log
  records nothing at all. Log `%[ssl_c_verify]` and the certificate subject on any frontend using
  client certificates, or the first report of a mass expiry will be "the site is down" with no
  server-side evidence. Which certificate fields may be logged is decided by
  `/alaa-security-review` (`$alaa-security-review`), and their log field names by
  `/alaa-services-contract` (`$alaa-services-contract`).

Terminating client authentication at HAProxy narrows the trust surface: exactly one component
validates the chain, and everything downstream trusts a header instead. That is an improvement
only if the header cannot be forged, which means every path to the downstream must pass through
this proxy and every inbound copy of that header must be deleted before it is set. See
`18-tiered-edge-gateway.cfg` for the delete-then-set pattern; `/alaa-trust-gateway-auth`
(`$alaa-trust-gateway-auth`) owns what the downstream may conclude from it.

## Backend TLS

`server ... ssl verify required ca-file <bundle>` is the form to write. `verify none` disables
certificate validation entirely and turns backend TLS into encryption without authentication,
which stops a passive observer and not an active one. Write `verify none` only when the backend
address is itself the authentication — a unix socket, or a loopback address — and say so in a
comment on the line.

The SNI sent to the backend decides which certificate the backend presents and therefore which
name is validated. Two correct shapes:

- `sni str(<fixed-name>)` — pin the name explicitly. Correct whenever one backend name serves many
  client-facing names. `19-tls-bridge-mtls-backend.cfg`.
- **`sni-auto`** (3.3 and later) — derive it from the request's `Host` header. This is the
  **default behaviour from 3.3**, so `sni-auto` states it rather than enabling it and
  `no-sni-auto` is how it is turned off. `check-sni-auto` and `no-check-sni-auto` control the same
  thing for health checks independently, because a health check has no request to derive a Host
  from.

**The consequence that must be stated wherever `sni-auto` is used:** the `Host` header is
supplied by the client, so an attacker chooses the name the origin certificate is validated
against. An unexpected `Host` becomes a backend TLS failure and a 502, visible only for the names
the origin certificate does not cover — which reads as a partial outage rather than as a
configuration error. Any frontend feeding a `sni-auto` backend allow-lists `Host` first;
`16-server-tls-sni-auto-3.3.cfg` shows the allow-list.

## ACME

In 3.2 the ACME flow is experimental. 3.3 adds DNS-01 through the Data Plane API path and lets the
Data Plane API write issued certificates to the filesystem — which the vendor documents as
suitable for a **single** load balancer, because two instances issuing independently will fight
over the account and the order. 3.4 adds DNS-PERSIST-01, External Account Binding, and IP
addresses in SANs.

For a Kubernetes estate with more than one HAProxy replica, an external issuer that writes a
Secret is the shape that composes; issuance inside the HAProxy toolchain is the shape that does
not. Which to use is a delivery decision and belongs to `/alaa-k8s-helm` (`$alaa-k8s-helm`); what
this skill owns is that HAProxy reloads to pick up a renewed certificate, or the Runtime API
`set ssl cert` plus `commit ssl cert` pair does it without one.

## Other 3.3 TLS additions

- `ssl-passphrase-cmd` runs a command to unlock a passphrase-protected private key, so the
  passphrase is not in the config. The command's own output is now the secret; whatever supplies
  it inherits the protection the key file had.
- `jwt_verify_cert` validates a JWT signature against a certificate rather than a bare public key,
  which removes a manual key-extraction step. What a verified JWT then authorises is decided by
  `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`).
- `tcp-md5sig` signs TCP segments, which matters for BGP-adjacent TCP proxying and nowhere else.
- ECH is experimental and requires `expose-experimental-directives`.
