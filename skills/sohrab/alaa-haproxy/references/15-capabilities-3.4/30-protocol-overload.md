# HTTP glitches and multiplexed overload

## HTTP/1 glitches and multiplexed overload

Glitch detection predates 3.4; HTTP/1 coverage is new. Global
`tune.h1.fe.glitches-threshold` and `tune.h1.be.glitches-threshold` default to zero
(no threshold). A nonzero threshold enables closure and a graceful close is
attempted at 75% of it. `fc_glitches`/`bc_glitches` and stick-table glitch counters
help distinguish malformed peers from ordinary load. Do not relax HTTP parsing
to create test traffic on a production listener; use isolated malformed fixtures.

3.4 adds H2 frame/RST fairness controls (`tune.h2.{fe,be}.max-frames-at-once`,
`tune.h2.fe.max-rst-at-once`), whose default zero imposes no such limit.
`tune.h2.fe.max-total-streams` bounds connection lifetime with GOAWAY rather than
concurrent streams. `rq-load`/`min` on `tune.h2.fe.max-concurrent-streams` adjusts
advertised concurrency under run-queue pressure. `tune.streams-elasticity` applies
to H2 and QUIC multiplexed frontend streams; default zero disables elasticity.
Read its interaction with `maxconn` in the
[configuration manual](https://docs.haproxy.org/3.4/configuration.html#tune.streams-elasticity).
Do not invent an H3 spelling by copying `tune.h2.*`; QUIC has its own controls.
Use protocol-aware stress tests to observe SETTINGS/GOAWAY, accepted streams,
memory, legitimate gRPC/browser latency and attack fairness. Parsing cannot prove
these properties. Security severity stays with `/alaa-security-review`.
