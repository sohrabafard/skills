# 30 File Descriptors And Pools

When setting `nofile`, sysctls, or database connection pools, read this reference.

## 4. `nofile` and the sysctls that matter

A Swoole or Node server holds one file descriptor per connection plus its own files. The default
`nofile` soft limit of 1024 is reached at roughly 900 concurrent connections and the failure is
`accept: too many open files`, which appears as connection refusals under load and nothing at all
below it.

Threshold with a number: **set `nofile` explicitly on any service expected to exceed 500 concurrent
connections, or any service whose observed peak descriptor count exceeds half the current soft
limit.** Measure it, do not assume:

```
docker compose exec platform-app-php sh -c 'ls /proc/1/fd | wc -l; cat /proc/1/limits | grep "open files"'
```

Values:

| Role | `nofile` soft | `nofile` hard | Why |
|---|---|---|---|
| Octane/Swoole application | 65535 | 65535 | One descriptor per connection plus the framework's open files |
| Node SSR | 65535 | 65535 | Same |
| Queue worker | 8192 | 8192 | A handful of connections; the limit exists to bound a descriptor leak |
| PgBouncer | 65535 | 65535 | One descriptor per client connection plus one per server connection |
| Scheduler | 4096 | 4096 | Lowest of the long-lived roles |

Where to set it, because Compose and Swarm differ:

- Compose: `ulimits: {nofile: {soft: 65535, hard: 65535}}` on the service.
- **Swarm ignores `ulimits:` entirely.** Set it in the image, or set `default-ulimits` in
  `/etc/docker/daemon.json` on every node:
  ```json
  { "default-ulimits": { "nofile": { "Name": "nofile", "Soft": 65535, "Hard": 65535 } } }
  ```
  This is host configuration and belongs in the node provisioning role, not in the repository.
  Whether it is applied through Ansible is `/ansible-generator`'s
  ground; that the value is required is this skill's.

Sysctls, one per line with its reason. Change one at a time and record which one:

| Sysctl | Value | When it matters |
|---|---|---|
| `net.core.somaxconn` | 4096 | The accept queue. At the default 128 a burst of connections is refused before the server ever sees it. Set with the server's own backlog, which must be equal or lower. |
| `net.ipv4.tcp_max_syn_backlog` | 8192 | Half-open connections during a connection burst. |
| `net.ipv4.ip_local_port_range` | `10000 65535` | Outbound port exhaustion on a service making many short-lived downstream connections. |
| `net.ipv4.tcp_tw_reuse` | 1 | Reuse of TIME_WAIT sockets for outbound connections; pairs with the above. |
| `vm.overcommit_memory` | 1 | Redis specifically: without it a background save can fail on a fork. Host-level, not per-container. |
| `kernel.shmmax` | node-dependent | PostgreSQL shared buffers on a dedicated node. |

`sysctls:` in a service applies namespaced sysctls per task. `net.core.somaxconn` and the `net.ipv4`
entries are namespaced and can be set per service; `vm.*` and `kernel.*` are not and must be set on
the host.

```yaml
    sysctls:
      net.core.somaxconn: 4096
      net.ipv4.tcp_max_syn_backlog: 8192
```

## 5. Connection pool sizing against the container

PgBouncer sits between the application and PostgreSQL and its pool must be sized against both.

```
default_pool_size   = min( postgres max_connections * 0.8 / number_of_services , app_concurrency )
max_client_conn     = sum over services of ( replicas * OCTANE_WORKERS ) * 2
pool_mode           = transaction
```

- `pool_mode = transaction` returns a server connection to the pool at the end of each transaction,
  which is what makes a pool smaller than the client count possible. It forbids session-level state:
  prepared statements across transactions, session variables and advisory locks held between
  transactions all break. This is why the fleet sets `DB_PGSQL_DISABLE_PREPARES=true` on generated
  services.
- `max_client_conn` must exceed the total number of application workers or a worker blocks waiting
  for a client slot, which looks like database slowness and is not.
- A pool larger than PostgreSQL's `max_connections` moves the failure from PgBouncer, where it is a
  queue, to PostgreSQL, where it is a connection error.

The kit's tracked defaults are `PGBOUNCER_DEFAULT_POOL_SIZE_DEFAULT=50` and
`PGBOUNCER_MAX_CLIENT_CONN_DEFAULT=1000` (`contracts/service.runtime.env.example:95-96`). With three
app replicas at two Octane workers each, plus two workers and a scheduler, the client count is 9 and
1000 is generous; the number to check is `default_pool_size` against PostgreSQL's `max_connections`
divided across every service sharing the instance. Query and index shape, and whether a query should
hold a connection at all, are `/alaa-data-layer`'s ground.
