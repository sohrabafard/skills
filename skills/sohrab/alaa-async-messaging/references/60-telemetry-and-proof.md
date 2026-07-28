# Telemetry and proof

Read this when instrumenting a publisher, a consumer or a relay, when writing the two required tests, and
when deciding what a reviewer must see before a message-plane change merges. Every metric name below is
registered in `alaa-services-contract references/24-metric-registry.md`; this file states which registered
observable proves which condition, and states no name of its own.

**Never invent a metric, log-field, event or error-code name.** Take it from `/alaa-services-contract`
(`$alaa-services-contract`) and request registration there when the one you need is missing. An invented
name diverges across services, and no dashboard or alert can read three spellings of one idea.

## Which observable proves which failure class

| Failure class in `50-failure-classes.md` | The observables that identify it |
|---|---|
| 1 broker unreachable | `alaa_queue_messages_published_total` flat; `alaa_dependency_request_failures_total` rising; `alaa_outbox_depth` rising |
| 2 consumer stuck | broker unacknowledged count high; `alaa_queue_backlog` rising; `alaa_queue_messages_consumed_total` flat; `alaa_worker_memory_bytes` rising |
| 3 poison loop | `alaa_queue_retries_total` rising with `alaa_queue_messages_consumed_total` flat |
| 4 duplicate storm | duplicate effects with the receipt duplicate counter flat; `alaa_queue_retries_total` elevated |
| 5 outbox stalled | `alaa_outbox_depth` and `alaa_outbox_oldest_age_seconds` rising; `alaa_outbox_published_total` flat |
| 6 DLQ filling | `alaa_queue_dead_letter_total` rising with the live queue draining |
| 7 replay duplicated | duplicate effects immediately after a replay, duplicate counter flat |
| 8 confirm timeout | `alaa_outbox_publish_failures_total` rising while `alaa_queue_messages_consumed_total` keeps pace |

**`alaa_outbox_oldest_age_seconds` is the single most load-bearing gauge on this plane**, because it is the
only one that separates a relay that is slow from a row that will never publish. Depth alone cannot: a
steady depth with a stuck oldest row looks healthy.

**`alaa_queue_consumer_lag_seconds` is the age of the oldest unconsumed message**, not an offset difference.
Read it as latency, and alert on it rather than on backlog depth, because depth is meaningless without the
consumption rate beside it.

## Cardinality

**Label a message-plane metric by queue name, message type, and outcome, and by nothing else.** Tenant,
project, user, message identifier, correlation identifier and error message are all unbounded in principle,
and one unbounded label multiplies every series on the metric until the metrics backend degrades for every
service sharing it.

**A tenant or a message identifier belongs in a log field or a trace attribute, where it costs one record
rather than one series.** That is also where an incident actually needs it: grouping a DLQ by tenant, as
`50-failure-classes.md` requires, is a log query, not a metric query.

## Correlation

**Propagate the trace context through the message.** A publish creates a span; the envelope carries the
trace context; the consumer continues that trace rather than starting a new one. Without it a message plane
is a hole in every trace, and the question "which request caused this consumer error" has no answer.

**Log the message identifier and the idempotency key on every consume, on both the success and the failure
path.** These are what make a duplicate investigation possible: without the key in the log, comparing two
duplicated effects cannot show whether the key derivation was the defect.

**Never log a message body containing personal data.** The body is available from the dead-letter queue when
one is genuinely needed, and a log pipeline retains it far longer than the message plane does.

Requirement levels, gates and alert authoring are `/alaa-observability-soc` (`$alaa-observability-soc`).

## The two required tests

Both ship with every change to a consumer or a dead-letter route.

**The redelivery test.** Deliver one message twice to the real handler, against a real database with the
real uniqueness constraint in place. Assert three things: exactly one business effect exists; exactly one
receipt row exists; the duplicate counter incremented by exactly one. A test that asserts only "no error on
the second delivery" passes against a handler that silently performed the effect twice.

**The dead-letter test.** Fail the handler past the delivery limit. Assert the message is present on
`<queue>.dlq` with routing key `<live-key>.failed`, that the live queue is empty, and that
`alaa_queue_dead_letter_total` incremented. A route no test has exercised is a configuration hope, and the
incident is where it gets discovered.

**Both tests run against a real broker and a real database, not a fake.** An in-memory double cannot
reproduce a delivery limit, a dead-letter route, or a uniqueness constraint, which are the only three things
these tests exist to prove. Test-layer doctrine — what makes a test a test, and which layer proves what — is
`/alaa-testing-strategy` (`$alaa-testing-strategy`).

## What a reviewer must see before this merges

A message-plane change that does not present these has not been reviewed, whatever else was read:

1. The prefetch value and the measured handler p99 it was derived from.
2. The acknowledgement route taken for each of the three outcomes: success, transient failure, permanent
   failure.
3. The dead-letter target declared for every queue the change declares.
4. The registry row for every new broker name, merged before or with this change.
5. The two tests above, passing, on the deployed version.
6. `sh scripts/check-consumer-bounds.sh --root .` at exit 0, or exit 2 with the three manual check results
   reported.
