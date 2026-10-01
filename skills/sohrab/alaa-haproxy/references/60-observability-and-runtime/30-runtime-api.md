# Runtime API access and operations

## The Runtime API

The admin socket is a full administrative control plane: it disables servers, changes weights,
replaces certificates and dumps the stick tables. **Reaching it is equivalent to reaching the
config.** It stays a unix socket with `mode 660`; putting it on a TCP listener is the single
largest exposure change this skill can make and it goes to `/alaa-security-review` before it is made.

First checks, in the order they answer a question:

| Command | Answers |
|---|---|
| `show info` | is this the process and build I think it is; how many connections, how much memory |
| `show stat` | per-proxy counters: `econ`, `eresp`, `qcur`, `wretr`, `scur`, `smax` |
| `show errors` | the last protocol errors, with the offending bytes — the only place a malformed request or a failed handshake is legible |
| `show events` | the ring buffer of recent events |
| `show servers state` | why a server is down and how long it has been |
| `show table <name>` | what a stick table actually contains, which is how you confirm the limiter's key |
| `show peers` | whether peer sessions are up; see `40-rate-limiting-and-peers.md` |
| `show cache` | what the object cache actually holds |
| `show stat typed` | whether each metric is volatile or persistent, which is how a `shm-stats-file` rollout is confirmed |
