# Container paths, process model and signals

## Paths HAProxy needs

- The official image reads `/usr/local/etc/haproxy/haproxy.cfg`. Mount the config read-only there.
- **Writable at runtime**, and each one for a stated reason:
  - `/run/haproxy` — the stats socket. Without it the Runtime API does not exist.
  - `/var/lib/haproxy` — the chroot target, when `chroot` is set.
  - `/dev/shm` — only when `shm-stats-file` is in use, and only at the path that directive names.
- Under `readOnlyRootFilesystem: true` every one of those needs an explicit writable mount. The
  failure is at startup and is legible, so this is a fast failure rather than a silent one.
- `chroot` combined with `stats socket /run/haproxy/admin.sock` works because the socket is created
  before the chroot takes effect. Moving the socket path inside the chroot breaks it. The
  interaction is not obvious and is the most common thing to get wrong when adapting
  `01-baseline-http-tls.cfg`.

## Process model and signals

- Start with `-W -db`: master-worker with the master in the foreground so the container's stdout
  is the log. The `master-worker` **global directive** is deprecated from 3.3 and the command-line
  form is the replacement.
- `SIGUSR1` — **soft stop**. Listeners close immediately; existing streams finish.
- `SIGUSR2` — reload in master-worker mode: a new worker takes the listeners, the old one finishes
  its streams and exits. The official image entrypoint prepends HAProxy arguments and runs `exec`; it does
  not translate signals. The Dockerfile declares `STOPSIGNAL SIGUSR1` for container
  stop. Choose the explicit master-worker reload signal/process target.
- `SIGTERM` — hard stop. In-flight requests are cut.
- `hard-stop-after <duration>` in `global` bounds how long a soft stop may take before the process
  exits regardless. **Scope: it is process-wide, and it applies to every soft stop and every
  reload, not only to shutdown.** Set it when any proxy in the config can hold a long-lived stream
  — a WebSocket, a `CONNECT` tunnel, a TCP proxy with a minute-scale `timeout client` — because
  without it a reload waits for the longest stream and a rollout stalls behind one idle socket. Set
  it shorter than the platform's own kill deadline, or the platform kills the process mid-drain and
  the bound achieves nothing. On Kubernetes that deadline is `terminationGracePeriodSeconds`.
