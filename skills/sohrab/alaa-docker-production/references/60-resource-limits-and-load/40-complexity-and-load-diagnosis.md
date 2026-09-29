# 40 Complexity And Load Diagnosis

When choosing a structure budget or diagnosing a load symptom, read this reference.

## 6. Complexity budgets

A container limit bounds resource use; it does not make a path scale. Whether a loop, query or
fan-out has a stated complexity bound as tenants, rows or events grow is
`/alaa-algorithms-data-structures`'s decision, and a service
that has outgrown its design needs `/alaa-system-design` rather than a
larger `memory:` value. Raising a limit to fix a growth problem hides it until the next size up.

## 7. Diagnosing a load problem

| Symptom | First check | Section |
|---|---|---|
| Container restarts with nothing in its logs | `docker inspect --format '{{.State.OOMKilled}}'` | [container resource ceilings](10-container-resource-ceilings.md#1-and-do-different-jobs) |
| Latency rises with no CPU saturation on the host | CPU throttling: `cat /sys/fs/cgroup/cpu.stat` and read `throttled_usec` | [resource ceilings](10-container-resource-ceilings.md#1-and-do-different-jobs); [process sizing](20-process-and-php-workers.md#2-the-trap) |
| Memory climbs steadily and resets on restart | Worker recycling absent: `OCTANE_MAX_REQUESTS` unset | [process and PHP workers](20-process-and-php-workers.md#2-the-trap) |
| 32 worker processes in a 2-CPU container | `nproc` auto-sizing; `OCTANE_WORKERS` unset | [process and PHP workers](20-process-and-php-workers.md#2-the-trap) |
| Random latency spikes with no traffic change | OPcache thrashing: `opcache_get_status()` shows evictions | [process and PHP workers](20-process-and-php-workers.md#3-opcache-and-jit-for-a-long-lived-worker) |
| `accept: too many open files` | `nofile` at the 1024 default | [file descriptors and pools](30-file-descriptors-and-pools.md#4-and-the-sysctls-that-matter) |
| Connections refused before the app logs anything | `net.core.somaxconn` at 128 | [file descriptors and pools](30-file-descriptors-and-pools.md#4-and-the-sysctls-that-matter) |
| Application waits on the database, database is idle | PgBouncer `max_client_conn` or `default_pool_size` too small | [file descriptors and pools](30-file-descriptors-and-pools.md#5-connection-pool-sizing-against-the-container) |
| Node process OOM-killed well under its heap size | `--max-old-space-size` sized from host memory | [process and PHP workers](20-process-and-php-workers.md#2-the-trap) |
