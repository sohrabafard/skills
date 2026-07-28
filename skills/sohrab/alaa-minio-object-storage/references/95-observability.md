# Observability of the object store

This file owns what to measure about the store and what proves each failure class is actually visible. It states no
metric name, no log field and no event name: those are `/alaa-services-contract` (`$alaa-services-contract`), and
whether a change is obliged to carry telemetry at all is `/alaa-observability-soc` (`$alaa-observability-soc`).
**Never invent a name here**; request registration there and use what comes back.

## The cardinality rule

**Never put an object key, a presigned URL, a bucket name, a tenant identifier or a credential into a metric label
or a span attribute.** Keys and tenant identifiers are unbounded, so each distinct value creates a permanent time
series and the metric backend degrades for everything, not only for storage. Keys and presigned URLs are also
secrets by `SKILL.md` rule 7 and rule 4.

Safe dimensions are closed sets: the operation (`get`, `put`, `copy`, `delete`, `complete_multipart`), the outcome
class, and the failure class from `90-failure-classes.md`. Put the key and the row identifier in a trace or a
structured log field governed by the forbidden-field list, not in a label.

## Signals worth having, and what each one proves

| Signal | Proves |
|---|---|
| request duration by operation and outcome class | that a slow store is distinguishable from a slow application; a p99 that moves while the application's own work does not is the store |
| error count by failure class | which of the eleven classes in `90-failure-classes.md` is occurring, without reading logs |
| count and maximum age of incomplete multipart uploads | that the abort lifecycle rule is working, and that abandoned parts are not accumulating. Collect it from a periodic listing job, never from the request path |
| bucket size in bytes and object count, tracked together | the divergence that reveals invisible consumers: bytes growing while the object count is flat means versions or parts |
| free capacity of the underlying volume | the full-store failure in class 9 before it becomes write errors |
| replication lag, where replication is enabled | that the disaster-recovery posture is real rather than declared |
| time until the current credential expires | that a rotation is due before it becomes an outage |

**A signal nobody alerts on proves nothing at the moment it matters.** For each one above, either state the
threshold and where the alert goes, or state that it is diagnostic-only and why.

## Health versus readiness

**The store's own liveness endpoint proves the process is answering, not that your bucket exists or that your
credential works.** A consuming service's readiness check must exercise the bucket it will actually use, with the
credential it will actually use, and must fail readiness when that check fails — because a service that reports
ready while its storage is unreachable takes traffic it will drop.

**Keep the readiness check cheap and bounded.** A `HEAD` on the bucket with a short timeout is enough; listing
objects on every readiness probe adds load proportional to probe frequency.

The fleet's only object-storage consumer does exactly this: readiness performs a bucket-existence check with the
runtime credential, and separately validates the configured object prefix, reporting each as a named readiness
result `[source: tusd-upload-platform repository, cmd/tusd-api/main.go, read: 2026-07-27]`.

## Logging

**Log the failure class, the operation and the bucket-scoped context, and never the key, the URL or the
credential.** The fleet's consumer already keeps `object_key` and `presigned_url` on its forbidden-log-field list
alongside authorization headers and raw tokens `[source: tusd-upload-platform repository,
internal/observability/contracts.go, read: 2026-07-27]`; that list is the pattern to copy.

**Carry the correlation identifier into the storage call and back out of it**, so a storage failure joins the
request that caused it. The identifier's name and propagation shape are `/alaa-services-contract`
(`$alaa-services-contract`).

## The store's own telemetry

MinIO exposes Prometheus metrics on cluster, node and bucket scopes, with the bucket scope substantially more
expensive to scrape because it iterates bucket state, and with the endpoint requiring a token unless it is
explicitly made public
`[source: https://min.io/docs/minio/linux/operations/monitoring/collect-minio-metrics-using-prometheus.html,
read: unverified as of 2026-07-27]`.

**Scrape the cluster and node scopes at the normal interval, and the bucket scope at a much longer one.** A
per-bucket scrape at the default interval on a store with many buckets is itself a load problem.

**Protect the metrics endpoint.** Metrics disclose bucket names, object counts and capacity, which is reconnaissance
for anyone who should not have it. The gateway-proof requirement for a metrics endpoint is
`/alaa-services-contract` (`$alaa-services-contract`).

## Audit

**Enable an access or audit log where the store provides one, and record where it goes and how long it is kept.**
Without it, the question "who deleted this object" has no answer, and it is asked only after the deletion. MinIO
sends audit events to a configured webhook or log target rather than storing them itself
`[source: https://min.io/docs/minio/linux/operations/monitoring/minio-logging.html, read: unverified as of
2026-07-27]`. SOC evidence requirements and log retention belong to `/alaa-observability-soc`
(`$alaa-observability-soc`).

## What the fleet does today

The consuming service has a bucket-existence readiness check and a prefix-validity readiness check, and a
forbidden-log-field list that already covers keys and presigned URLs. It has **no signal for incomplete multipart
uploads, no signal for bucket size or free capacity, and no scrape of the store's own metrics** anywhere in its
repository `[source: tusd-upload-platform repository, read: 2026-07-27]`. The first of those three is the one that
makes the missing lifecycle rule in `20-lifecycle-and-retention.md` invisible.
