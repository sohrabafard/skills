# Pools, logs, profiling and metrics

`tune.idle-pool.shared {on|full|off}` replaces the deprecated
`tune.takeover-other-tg-connections` in 3.4. Default `on` shares within a thread
group; `full` crosses groups at a possible contention cost; `off` isolates threads
and may cause excessive closes without an appropriate `pool-low-conn`.
`pool-max-conn`, `pool-low-conn` and `pool-purge-delay` still apply per server;
they are not removed. Check pool occupancy, origin connection count, file
descriptors and retry errors under load before changing reuse. Connection-bound
identity remains incompatible with indiscriminate reuse.

`tune.h2.log-errors {stream|connection|none}` defaults to `stream`; reducing it
can hide protocol failures. `show profiling memory` gains execution-context
attribution in 3.4; capture the configured profiling state, overhead and access
policy before a bounded investigation. The exporter adds
`haproxy_sticktable_local_updates`; first inspect real exposition and scope
parameters, then route alert/catalog decisions to their owners. `set-dumpable libs`
can embed matching executables/libraries in a core: the dump can also contain
secrets. 3.4.6 adds log `+utf8` handling; this is a maintenance addition, not a
3.4.0 capability. See [observability](../60-observability-and-runtime.md) for emission
and control-plane mechanics.
