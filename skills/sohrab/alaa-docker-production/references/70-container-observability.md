# Container-level observability

Open this file when deciding how a container's output leaves it, or when a failure was not
diagnosable from what the container emitted.

**This skill owns the key, not the catalogue.** Whether a signal is required at all, and what gates
on it, is `/alaa-observability-soc` (`$alaa-observability-soc`)'s decision. What a log field, a
metric or an `OTEL_*` variable is *called*, and what its canonical default is, is
`/alaa-services-contract` (`$alaa-services-contract`)'s register. What this file states is the
container-level plumbing that makes any of it possible: where output goes, how it is bounded, and
what must be true of the container for a failure to be diagnosable at all.

---

## 1. Output goes to stdout and stderr, and nowhere else

A container writes its logs to file descriptors 1 and 2. It does not write them to a file inside the
container, because:

- with `read_only: true` the write fails, and most logging libraries swallow that failure, so the
  application appears to run with no logs at all;
- a file inside a container is deleted when the container is replaced, which is exactly when the
  logs are wanted;
- nothing collects it.

In this fleet `LOG_CHANNEL` is set to `stderr` on every generated service, which is the correct
value and the reason it appears in `environment:` rather than being left to the application's
default.

Two consequences:

- A framework that writes to `storage/logs/` by default must be configured not to. Leaving the
  default and mounting a volume for it moves the problem rather than fixing it.
- Anything that writes to a log file *and* stdout doubles the volume for no benefit.

## 2. The logging driver and its limits

```yaml
    logging:
      driver: json-file
      options:
        max-size: "20m"
        max-file: "5"
        compress: "true"
```

**The `json-file` driver has no size limit by default.** A service logging steadily fills the node's
disk, and when it does, every container on that node fails — including ones with no relationship to
the noisy service. This is the most common self-inflicted node outage in a Compose or Swarm fleet,
and the only prevention is that every long-lived service sets `max-size` and `max-file`.

Values, and the arithmetic behind them: `max-size: 20m` with `max-file: 5` bounds one container at
100 MB. Multiply by the number of containers on the node and compare with the node's free disk. For
a node running twelve containers that is 1.2 GB, which is the number to justify rather than the
per-container value.

`compress: "true"` compresses rotated files and typically reduces the retained footprint by 80%,
at the cost of CPU on rotation only.

Where a collector is deployed, the driver may instead be one the collector reads. Which driver, and
whether logs are shipped at all, is `/alaa-observability-soc` (`$alaa-observability-soc`)'s
decision. Two container-level constraints hold whichever driver is chosen:

- A driver that blocks when its destination is unreachable will block the application's writes.
  `mode: non-blocking` with a `max-buffer-size` prevents a collector outage from becoming an
  application outage. This is the fail-open case: losing telemetry is the correct degradation, and
  `/alaa-reliability-sla` (`$alaa-reliability-sla`) owns the general form of that trade.
- A non-local driver breaks `docker logs` and `docker service logs`, which are the two commands an
  operator reaches for during an incident. Where a non-local driver is used, the runbook states what
  to use instead.

Pipeline-side log shaping and routing — a Vector or similar aggregation layer — is
`/vector-rust-observability-pipelines` (`$vector-rust-observability-pipelines`)'s ground.

## 3. What the container must expose for a failure to be diagnosable

The container-level minimum, stated as things that must be true of the container rather than of the
application:

1. **Logs reach stdout/stderr and are bounded.** §1, §2.
2. **The image is identifiable from a running container.**
   `docker inspect --format '{{index .Config.Labels "org.opencontainers.image.revision"}}'` returns
   a commit. Without it, "which code is running" is unanswerable during an incident. This skill's
   `references/10-dockerfile-authorship.md` §7.
3. **The health state is queryable and has history.**
   `docker inspect --format '{{json .State.Health}}'` returns the last five probe results with their
   output. That requires a probe that prints something useful on failure. This skill's
   `references/40-healthcheck-and-lifecycle.md`.
4. **A metrics endpoint, where the service exposes one, is reachable on the container network and is
   not published to a routable address.** The fleet's generated services expose
   `OBSERVABILITY_METRICS_PATH=/metrics` on the application port; it is scraped over the shared
   Docker network and is not in the published port list.
5. **A crash is distinguishable from a stop.** `docker inspect --format '{{.State.ExitCode}}
   {{.State.OOMKilled}} {{.State.Error}}'`. Exit 137 with `OOMKilled: true` is a memory limit;
   exit 137 without it is a SIGKILL after the grace period, which is the shutdown problem in this
   skill's `references/40-healthcheck-and-lifecycle.md` §4 and not a memory problem. Conflating the
   two sends an investigation in the wrong direction for hours.

## 4. Telemetry variables are configuration this skill carries and does not decide

The generated services carry a block of roughly forty `OTEL_*`, `OBSERVABILITY_*` and `PROMETHEUS_*`
variables (`service-runtime-kit` `render-runtime.sh:1100-1159`). Every one of them is:

- **named and defaulted by** `/alaa-services-contract` (`$alaa-services-contract`) for the shared
  names, and `/service-runtime-kit-governance` (`$service-runtime-kit-governance`) for which
  generator variable expresses each;
- **required or not by** `/alaa-observability-soc` (`$alaa-observability-soc`);
- **written into the Compose file by this skill**, which means only that the interpolation form
  follows this skill's `references/25-fail-closed-interpolation.md`.

Two of them touch container behaviour directly and are worth naming here because a container author
will otherwise get them wrong:

- `OTEL_EXPORTER_OTLP_TIMEOUT` is expressed in **milliseconds** per the OpenTelemetry environment
  contract, and the fleet default is 500. A value entered as seconds is a 500-second timeout, which
  turns a slow collector into a stalled request path.
- `OBSERVABILITY_FAIL_OPEN` decides whether telemetry failure degrades telemetry or degrades the
  request. The container-level consequence of `false` is that a collector outage becomes a service
  outage. Whether it should be true is `/alaa-reliability-sla` (`$alaa-reliability-sla`)'s call.

## 5. Diagnosing

```
docker inspect --format '{{.LogPath}}' CONTAINER | xargs -r du -h
docker ps -q | xargs docker inspect --format '{{.Name}} {{.HostConfig.LogConfig.Config}}'
docker inspect --format '{{.State.ExitCode}} {{.State.OOMKilled}} {{.State.Error}}' CONTAINER
docker inspect --format '{{json .State.Health}}' CONTAINER
docker service logs --since 10m --raw SERVICE
```

| Symptom | Cause | Section |
|---|---|---|
| Node out of disk, several unrelated containers failing | A service with no `max-size` | §2 |
| Application appears to run and logs nothing | It writes to a file, and `read_only: true` made the write fail silently | §1 |
| `docker logs` is empty but the collector has entries | A non-local driver is configured | §2 |
| Application latency rises when the collector is down | A blocking driver, or `OBSERVABILITY_FAIL_OPEN=false` | §2, §4 |
| Container exits 137 and memory looks fine | SIGKILL after the grace period, not an OOM | §3 |
| Cannot tell which commit is running | No `org.opencontainers.image.revision` label | §3 |
| Metrics endpoint reachable from outside the host | It is in the published port list | §3, this skill's `references/50-network-dns-and-exposure.md` |
