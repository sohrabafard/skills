# ACME and TLS certificate compression

3.4 extends ACME with DNS-PERSIST-01, External Account Binding
(`eab-key-id`, `eab-mac-key`, `eab-mac-alg`) and IP-address SANs. The CA must support
the selected challenge/account flow; DNS ownership and secrets remain external
prerequisites. There is no implicit enrollment. Inspect the exact ACME section,
account-key persistence, challenge publication and certificate-store attachment
before enabling issuance. Test issuance, renewal, failure, restart and replica
coordination in an isolated account; parsing proves none of them. Existing
[TLS guidance](../25-tls-and-mtls.md) routes the issuer/deployment decision.

`tune.ssl.certificate-compression {auto|off}` is new in 3.4, for both TLS sides.
Default `auto` follows the TLS library; the 3.4.6 manual specifies OpenSSL >=3.2.0.
The directive does not prove that peers negotiate RFC 8879 or that the library was
built with the required algorithms. Check the linked library in `haproxy -vv` and
measure handshake bytes/latency with a capable peer. `off` disables acceptance and
emission; this feature compresses the certificate handshake, not HTTP bodies.
