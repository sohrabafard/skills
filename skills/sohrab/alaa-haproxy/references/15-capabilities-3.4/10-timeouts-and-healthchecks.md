# Per-request timeouts and reusable health checks

3.4 extends `http-request set-timeout` to `connect`, `queue` and `tarpit`.
Connect/queue overrides require a backend-capable section; put them in the
selected backend, not a frontend. Tarpit may be overridden on either side.
Without a matching action the configured timeout applies. A constant includes its
unit; a sample expression produces milliseconds. Set bounded values from trusted
routing data, not an unrestricted client header. Changing the connect timeout
changes every attempted connection's budget; it does not make replay safe.
`cur_connect_timeout`, `cur_queue_timeout` and `cur_tarpit_timeout` expose the
effective value, while `be_*_timeout` exposes backend configuration. A 3.4.3 fix
corrected custom timeout initialization when switching backends: validate that path
on the requested patch, not only action syntax. Timeout values and replay policy
remain with `/alaa-reliability-sla`.

`healthcheck <name>` sections use `type httpchk`, `type tcp-check` or the other
documented check types. Attach them with `server ... check healthcheck <name>` or
`default-server ... healthcheck <name>`; no shared section is selected implicitly.
Use this when servers need different checks or several backends share a check.
3.4.1 fixed the `default-server` attachment and external-check interaction.
Check TLS, protocol, Host, endpoint, failure status and recovery against a real
origin: a successful TCP connection does not establish application readiness.
The distinct pattern is `examples/haproxy/21-request-budgets-healthcheck-3.4.cfg`.
