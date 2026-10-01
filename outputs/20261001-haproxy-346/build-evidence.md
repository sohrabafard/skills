# Cached target build evidence

Verified 2026-10-01. Command:

```sh
docker image inspect haproxy:3.4.6-alpine --format '{{.Id}}'
docker run --rm --pull never --network none --entrypoint sh haproxy:3.4.6-alpine -c 'haproxy -vv; cat /etc/alpine-release; command -v lua; ls /usr/lib/liblua*'
```

Image ID: `sha256:7af8255207ee9964ccb4eec8ce4b7a40b777769665e3ae83897fb01b24d8a43a`.
HAProxy `3.4.6-56332c5 2026/09/28`, Alpine `3.24.2`, Lua `5.4.8`, OpenSSL `3.5.8`.
Feature list includes `+LUA +QUIC +PROMEX +SLZ -ZLIB`; the multiplexer list includes `qmux`.
Filter list includes bandwidth limiting, cache, compression, FCGI, SPOE and trace; no OpenTelemetry filter.
`-OT` identifies OpenTracing, not proof about OpenTelemetry by itself.
No standalone Lua executable is present; `liblua-5.4.so.0` is present.
Docker named-pipe access required escalation; the read-only image inspection then succeeded.

Release currency: the [official release table](https://www.haproxy.org/) reported 3.4.6
(2026-09-28) as the latest 3.4 patch on this date. Target stays 3.4.6.
The [3.4 announcement](https://www.haproxy.com/blog/announcing-haproxy-3-4) and
[management manual](https://docs.haproxy.org/3.4/management.html) were opened live.

This proves one cached build's identity and compiled capabilities. It does not prove registry
tag immutability, every architecture's build, runtime protocol behavior, or gateway deployment.
