# Migration from 3.3 to 3.4

## 3.3 to 3.4

Confirmed 2026-07-29 against `https://www.haproxy.com/blog/announcing-haproxy-3-4`.

Breaking: the stats page no longer shows the HAProxy version; re-enable with `stats show-version`
if a tool parses it.

Deprecated: `compression direction` (two words), legacy `filter compression`,
OpenTracing (scheduled for removal in 3.5), and `tune.takeover-other-tg-connections`
(replaced by `tune.idle-pool.shared`). For experimental OpenTelemetry build and
component prerequisites, read `15-capabilities-3.4.md`; an official image tag alone
does not establish the replacement is present. Tracing policy belongs to
`/alaa-observability-soc`.

Introduced in 3.4.0, with prerequisites and activation in `15-capabilities-3.4.md`: backends that can be added and removed at runtime without
a reload; QMux, experimental QUIC over TCP for networks that block UDP; JWE decryption and AES-CBC
at the proxy; ACME DNS-PERSIST-01, External Account Binding and IP addresses in SANs; extended
HTTP/1 glitch detection; `http-request set-timeout` extended to connect, queue and tarpit;
reusable health-check sections; `tune.bufsize.large` and `tune.bufsize.small`; `cpu-affinity` and
`cpu-policy ... threads-per-core`.

Patch corrections matter: 3.4.3 corrected custom timeout initialization on backend
switching; 3.4.4 added `be-unpublished` and fixed JWE key-length validation;
3.4.5 reverted `filter-sequence`; 3.4.6 fixes a QUIC RESET_STREAM crash and adds
log `+utf8`. Read the maintenance/backport ledger in `SOURCES.md`. These are not
all 3.4.0 introductions. `random` as the default algorithm, backend H3, automatic
SNI, kTLS and experimental shared stats already existed in 3.3.
