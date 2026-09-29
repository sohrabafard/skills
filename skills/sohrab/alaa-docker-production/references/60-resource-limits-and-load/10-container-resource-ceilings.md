# 10 Container Resource Ceilings

When sizing Compose or Swarm CPU and memory limits and reservations, read this reference.

## 1. `limits` and `reservations` do different jobs

```yaml
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 2G
        reservations:
          cpus: "1.0"
          memory: 1G
```

- **`limits`** is a ceiling enforced by cgroups on the running container. Exceeding the memory limit
  is an OOM kill by the kernel; exceeding the CPU limit is throttling, not an error, which is why
  CPU pressure shows up as latency rather than as a failure.
- **`reservations`** is what the scheduler guarantees. Without it, Swarm will place a task on a node
  with no capacity left and the task starts, competes, and performs badly with every metric
  reporting "running". `reservations` is absent from every generated service today.

Sizing rule: set `reservations` to the steady-state consumption you have measured, and `limits` to
the peak you are willing to pay for. A reservation equal to the limit wastes capacity; a reservation
of zero — which is what absence means — makes placement arbitrary.

Fleet defaults, which `service-runtime-kit` already carries as tracked values
(`README.md:113`, `contracts/service.runtime.env.example:40-47`):

| Role | `limits.cpus` | `limits.memory` | `reservations.cpus` | `reservations.memory` |
|---|---|---|---|---|
| Application (`platform-app-php`) | 2.0 | 2G | 1.0 | 1G |
| Queue worker (each) | 1.0 | 1G | 0.25 | 256M |
| Scheduler | 0.5 | 512M | 0.1 | 128M |
| PgBouncer | 0.5 | 256M | 0.1 | 64M |

Override the limits from the service `.env` with `APP_CPU_LIMIT`, `APP_MEMORY_LIMIT`,
`WORKER_CPU_LIMIT`, `WORKER_MEMORY_LIMIT`, `SCHEDULER_CPU_LIMIT`, `SCHEDULER_MEMORY_LIMIT`. Which
variables exist and what their tracked defaults are is `/service-runtime-kit-governance`'s ground; the numbers above and the requirement to also set
`reservations` are this skill's.

Measuring, so a change is a correction rather than a guess:

```
docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}'
docker inspect --format '{{.HostConfig.NanoCpus}} {{.HostConfig.Memory}}' CONTAINER
docker inspect --format '{{.State.OOMKilled}}' CONTAINER
```

`OOMKilled: true` on a container that "just restarted" is the answer to the whole investigation, and
it is the first thing to check when a container restarts with no error in its own logs.
