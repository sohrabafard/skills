# RabbitMQ worker failure classes

Read this when a queue misbehaves, or when writing the runbook entry or alert for a new worker. Classes 3,
5, 6 and 8 share symptoms — the diagnosis is what separates them, so never act on a symptom alone.

Per class: **symptom** observed, **diagnosis** that separates it from neighbours, **smallest retry** that
fixes it or disproves the diagnosis, **escalation**. Severity and paging: `/alaa-observability-soc`
(`$alaa-observability-soc`). Degradation doctrine: `/alaa-reliability-sla` (`$alaa-reliability-sla`)
`alaa-reliability-sla references/50-degradation.md`. Every threshold and timeout value:
`alaa-services-contract references/22-failure-load-and-deprecation-contract.md`. Broker and cluster
operations: `/caas-arvan-kuber` (`$caas-arvan-kuber`).

## 1. Broker unreachable at publish time

- **Symptom.** `AMQPIOException` or `AMQPConnectionClosedException` at `dispatch()`; queue depth flat;
  consumers idle and healthy.
- **Diagnosis.** Lazy connection, so this is TCP connect or handshake, not heartbeat loss.
  `getent hosts $RABBITMQ_HOST` separates DNS from reachability. `ACCESS_REFUSED` means credentials or vhost
  permission. `NOT_ALLOWED - vhost ... not found` means the vhost, and on Windows Git Bash usually means the
  value was path-converted (last section).
- **Smallest retry.** `Queue::connection('rabbitmq')->pushRaw('{}', 'diagnostic')` from the same pod —
  exercises connect, handshake, permission and declare without touching the application path.
- **Escalation.** Diagnostic publish fails while other services publish: the vhost user lost permissions,
  escalate to broker operations. Broker down: `SKILL.md` constraint 7 governs the request. Do not add a
  retry loop in the request path.

## 2. Connection lost mid-consume

- **Symptom.** Worker reports a lost-connection exception and restarts; in-flight jobs re-run; broker
  consumer count dips and recovers.
- **Diagnosis.** Which branch fired. `AMQPRuntimeException` from `wait()` goes to `kill(EXIT_ERROR)` —
  immediate death, no graceful stop. Any other throwable goes to `stopWorkerIfLostConnection()`, which stops
  the worker only when Laravel's `causedByLostConnection()` matches a phrase in the message; an unmatched
  message leaves the worker **running on a dead connection**, and that is the defect, not the broker.
  `queue:work` avoids it by rewrapping channel and connection close as `AMQPRuntimeException` prefixed
  `Lost connection: ` so the matcher hits.
- **Smallest retry.** Confirm `options.heartbeat` is non-zero. The underlying library default is `0`, and a
  zero heartbeat is the usual cause of a half-open connection that only surfaces minutes later.
- **Escalation.** Heartbeats on and connections still drop: an idle-connection reaper between pod and
  broker — `/alaa-k8s-helm` (`$alaa-k8s-helm`) and broker operations.

## 3. Poison message

- **Symptom.** One message fails every attempt with the same exception; a `failed_jobs` row per attempt.
- **Diagnosis.** Does the attempt count advance? Read `laravel.attempts` on the message, or `attempts` in
  the `failed_jobs` payload, across two occurrences. Advancing means Laravel is releasing normally and
  `--tries` will terminate it — this class, working as designed. Not advancing is class 8.
- **Smallest retry.** Do not requeue. Read one message non-destructively from the DLQ and re-run the handler
  against that exact payload locally; a poison message is a payload defect, so the payload is the evidence.
- **Escalation.** Make the handler classify the error as non-retryable and call `$this->fail($e)` per
  `SKILL.md` constraint 2, so the DLX takes it on the first attempt instead of burning `--tries`. Which
  errors are retryable: `alaa-reliability-sla references/20-retries.md`.

## 4. Redelivery storm

- **Symptom.** Unacked collapses to zero and ready jumps by roughly the prefetch window, repeatedly;
  handler duration and error rate normal between bursts.
- **Diagnosis.** A whole channel's unacked deliveries were requeued. Separate by close reason:
  `PRECONDITION_FAILED ... delivery acknowledgement ... timed out` is the broker's `consumer_timeout`
  against a slow handler; `CONNECTION_FORCED` is an operator action or node maintenance; no close reason
  plus a coincident pod restart is class 5. Prefetch count times p99 handler duration near
  `consumer_timeout` means the storm is self-inflicted and will recur.
- **Smallest retry.** Lower `--prefetch-count` on one replica and compare its redelivery rate against the
  others — proves the window is the cause without changing fleet throughput.
- **Escalation.** Raise `consumer_timeout` only when handler duration is legitimately long and bounded;
  otherwise split the long step out of the handler.

## 5. Job died mid-execution

- **Symptom.** No `failed_jobs` row, no completion log, message back with `redelivered` set; pod shows
  OOMKill, SIGKILL or a PHP fatal error.
- **Diagnosis.** Compare `terminationGracePeriodSeconds` against `--timeout` and p99 handler duration. A
  grace period below `--timeout` SIGKILLs a worker mid-job on **every** rollout, so this appears on every
  deploy rather than randomly. An OOMKill points at payload size or an unbounded collection in the handler.
- **Smallest retry.** Bring the Deployment into line with `SKILL.md` constraint 4 and watch the next
  rollout. Rollout mechanics: `/alaa-k8s-helm`; worker profile:
  `assets/helm/values.worker.rabbitmq.yaml.example`.
- **Escalation.** A fatal error means no ack and no reject, so the attempt count did not advance — you are
  also in class 8. Worker memory growth: `/alaa-octane-performance` (`$alaa-octane-performance`).

## 6. Duplicate execution

- **Symptom.** A side effect applied twice.
- **Diagnosis.** Get two values first — `laravel.attempts` and `correlation_id`; without them these are
  indistinguishable. Then: (1) **redelivery after a lost ack** — `redelivered` true, same `correlation_id`;
  normal at-least-once, the handler is not idempotent. (2) **requeue on worker stop** — `queue:work` only;
  `redelivered` true with **unchanged** attempts and a worker stop logged at the same instant; `close()` did
  it. (3) **two consumers on a queue assumed to have one** — broker consumer count exceeds the replica
  count, or exceeds one for a queue that must be serialised. (4) **genuine double dispatch** — two
  **distinct** `correlation_id` values; a producer defect, usually a missing `after_commit` interaction or a
  retried request that dispatched twice.
- **Smallest retry.** None; retrying resolves nothing. Add the missing uniqueness at the storage layer on
  the business key — that fixes 1, 2 and 4 together — then re-run the required test in `SKILL.md`.
- **Escalation.** Idempotency contract: `alaa-reliability-sla references/60-idempotency.md`.
  Unique-constraint and upsert mechanics: `/alaa-data-layer` (`$alaa-data-layer`).

## 7. Consumer stalled with queue depth rising

- **Symptom.** Ready climbing, consumer count non-zero, unacked flat.
- **Diagnosis.** Unacked flat and **non-zero**: the handler is blocked in an untimed call, holding
  deliveries. Unacked flat at **zero** with consumers registered: the process is paused (maintenance mode
  without `--force`) or consuming a different queue than the one filling. `queue:monitor` confirms depth but
  cannot distinguish the two, because it reports ready depth only.
- **Smallest retry.** Apply `SKILL.md` constraint 11 to the call the handler is blocked in. A blocked
  handler is a handler with an untimed call in it.
- **Escalation.** Depth rising with healthy fast handlers is capacity, not failure: the scaling rule is in
  `references/running-workers.md`.

## 8. Worker crash-loop replaying one message

The class this skill exists to prevent; the rule and mechanism are `SKILL.md` constraint 3 and
`references/driver-facts.md`.

- **Symptom.** One worker restarting continuously, depth barely moving, the same `correlation_id` every
  restart, and `failed_jobs` never gaining a row.
- **Diagnosis.** Read `laravel.attempts` across two consecutive restarts. **Unchanged** confirms it: the
  count is written only by `release()`, so unchanged proves requeue or redelivery rather than release, and
  neither `--tries` nor `markJobAsFailedIfWillExceedMaxAttempts` can end such a loop. Then check for a
  delivery cap: `rabbitmqctl list_queues name arguments effective_policy_definition`.
- **Smallest retry.** Apply the delivery-limit policy. It takes effect on the next redelivery, needs no
  deploy, and the loop stopping confirms the diagnosis.
- **Escalation.** A classic queue cannot count deliveries at all; converting it is a topology change, so
  names come from `alaa-services-contract references/23-queue-and-exchange-registry.md`. Immediate
  containment: stop the consumer, `basic_get` the message to a file for evidence, reject it without requeue
  so the DLX takes it. `rabbitmq:queue-purge` destroys data and is not the answer.

## Topology mistakes that look like failures

- **`NOT_FOUND` at worker start, or a queue that fills but is never consumed.** The queue, exchange or
  binding is missing. This driver declares a queue on publish but binds only when it declares, so a
  pre-existing queue with a missing binding never receives messages. Pre-creation is `SKILL.md`
  constraint 10; the tools are `rabbitmq:exchange-declare`, `rabbitmq:queue-declare`, `rabbitmq:queue-bind`.
- **`reroute_failed` on with no failed-route topology.** The driver adds `x-dead-letter-*` only to queues it
  declares itself and never re-declares an existing one, so turning the flag on changes nothing for an
  existing queue while the reader believes DLQ is now on. Prove it with a forced failure that lands a
  message in the dead-letter queue.
- **`RABBITMQ_WORKER=horizon` in any env or values file.** Remove it; the rule is `SKILL.md` constraint 9.

## Windows Git Bash vhost path conversion

On Git Bash / MSYS a slash-valued variable in a generated wrapper is rewritten to a Windows path, so
`RABBITMQ_VHOST=/` becomes something like `C:/Program Files/Git/` and the connection fails with
`NOT_ALLOWED - vhost ... not found`. Local-only; absent in CI and Linux containers. Confirm by echoing the
variable **inside the generated wrapper**, not your own shell. The fix belongs to the wrapper generator:
`/service-runtime-kit-governance` (`$service-runtime-kit-governance`).
