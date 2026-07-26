# Running the workers

Read this when writing or changing a worker command line, a worker Deployment, a replica count, or a
recycle limit. The mode decision itself is in `SKILL.md`; this file is the mechanics once the mode is
chosen. Package flag defaults are in `references/driver-facts.md` and every one of them needs overriding.

## Command lines

```
php artisan queue:work rabbitmq --queue=high,default --sleep=1 --tries=5 \
  --timeout=<T> --max-jobs=<J> --max-time=<S> --backoff=1,5,10,30

php artisan rabbitmq:consume rabbitmq --queue=high --prefetch-count=<P> --prefetch-size=0 \
  --tries=5 --timeout=<T> --sleep=1 --memory=<M> --max-time=<S> --json
```

`<T>`, `<J>`, `<S>`, `<M>` and `<P>` are per-service values, not constants. `<T>` is bounded from both
sides by the two relationships in `SKILL.md`; `<P>` by the prefetch rule there. `<J>` and `<S>` exist only
to bound memory drift in a long-lived PHP process and must be large enough that a worker completes many
jobs per lifetime — a recycle limit low enough to restart the worker inside one poison message's retry
window turns failure class 8 into a tight crash loop. Values:
`alaa-services-contract references/22-failure-load-and-deprecation-contract.md`.

`--json` on `rabbitmq:consume` emits machine-readable worker output; use it wherever a log pipeline parses
worker lines rather than a human reads them.

`ext-pcntl` must be present in the runtime image. Without it `supportsAsyncSignals()` is false, which
disables both the SIGALRM job timeout and graceful signal handling — so `--timeout` stops being enforced
and every rollout becomes a hard kill mid-job. Image contents: `/alaa-docker-production`
(`$alaa-docker-production`).

## Deployment shape

- Web and worker are separate Deployments, always. Never a sidecar in the web pod: a worker that shares a
  pod with the web container shares its lifecycle, its memory limit and its rollout.
- `QUEUE_CONNECTION=rabbitmq` set through `envConfig`, not baked into the image.
- One queue per Deployment in consume mode, because one process consumes one queue. A second queue means a
  second Deployment, not a second `--queue` value.
- `terminationGracePeriodSeconds` per `SKILL.md` constraint 4. Getting it wrong is failure class 5, which
  shows up on every rollout rather than randomly.
- Chart keys, probe shapes, resource blocks and rollout strategy belong to `/alaa-k8s-helm`
  (`$alaa-k8s-helm`). The worker profile for the `platform-app-php` chart is
  `assets/helm/values.worker.rabbitmq.yaml.example`. Arvan-specific defaults, including
  requests-equals-limits, are `/caas-arvan-kuber` (`$caas-arvan-kuber`).

## Choosing the replica count

The prohibition "not guessed" needs a rule, so here it is. Compute, do not tune blindly:

`required consumers = arrival rate (messages/s) x p99 handler duration (s) x headroom factor`

Measure arrival rate as the broker's publish rate for the queue over the busiest ten minutes, and p99
handler duration from the worker's own job-duration metric — not from a local run. The headroom factor and
the target utilisation are platform values in the contract file above.

Then pick the scaling mechanism from an observable condition, in this order:

1. **Fixed `replicaCount`** when the measured arrival rate varies by less than roughly a factor of two
   across the day. A fixed count is the default because it has no controller to misconfigure and no
   scale-to-zero cold start.
2. **HPA on CPU** only when handler work is CPU-bound and CPU utilisation tracks queue depth. It does not
   for an IO-bound handler, where a backlog produces idle CPU and the HPA scales the wrong way.
3. **KEDA on queue depth** when arrival rate is bursty by more than roughly a factor of two and the handler
   is IO-bound. The scaling signal is the broker's ready-message count for that one queue, never total
   vhost depth, and never CPU.

Whichever is chosen, record the measured arrival rate and p99 duration in the change alongside the number,
so the next reviewer can recompute it instead of re-guessing. Autoscaler resource shapes:
`/alaa-k8s-helm`.

## Verification before a rollout is called done

1. Dispatch one job; confirm it appears in the queue, is consumed, and the ready count returns to its prior
   value. Confirm the broker's consumer count equals the replica count.
2. Force a failure; confirm a `failed_jobs` row appears and, where a dead-letter route is configured, that
   the message lands in the dead-letter queue.
3. Delete a worker pod mid-job; confirm the job runs again and that the side effect applied exactly once.
   This is the required redelivery test in `SKILL.md` executed against real infrastructure.
4. Run at the measured peak arrival rate for long enough to cross one `--max-jobs`/`--max-time` recycle;
   confirm ready depth returns to baseline afterwards and that redelivery rate stays flat.

What makes each of these a test rather than a demonstration, and which of them belongs in CI:
`alaa-testing-strategy references/40-proof-strength.md` (`/alaa-testing-strategy`,
`$alaa-testing-strategy`).
