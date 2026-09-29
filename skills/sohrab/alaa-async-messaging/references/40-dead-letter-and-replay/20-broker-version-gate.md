# Broker-version gate for the retry bound

## Broker-version gate for the retry bound

Verified 2026-09-29 against the [RabbitMQ 4.3 release notes](https://www.rabbitmq.com/blog/2026/04/23/rabbitmq-4.3-release)
and [quorum-queue poison-message handling](https://www.rabbitmq.com/docs/quorum-queues#poison-message-handling).
Check the deployed broker version, queue type, effective policy and actual AMQP method before claiming a bound.

Before 4.3, quorum delivery counts included all requeues. From 4.3, `x-acquired-count` records assignments
to consumers (not proof the consumer saw them), while `x-delivery-count` counts failed deliveries:

| Return path in RabbitMQ 4.3, AMQP 0.9.1 | Advances delivery count |
|---|---|
| `basic.reject` with requeue; consumer crash or connection loss | Yes |
| `basic.nack` with requeue; consumer acknowledgement timeout; suspected cluster node partition | No |

A quorum `delivery-limit` bounds counted failures only; exhaustion drops the message unless a DLX exists.
Never treat acquired count, Laravel attempt headers and delivery count as interchangeable. For non-counting
returns or a classic queue, require an explicit bounded application retry/disposition path under
`alaa-reliability-sla references/20-retries.md`; an unchanging delivery count is not evidence of progress.
Preserve identity and resolve uncertain effects before retrying. Prove the actual path with the broker test
in `../60-telemetry-and-proof.md`; do not silently switch nack to reject to manufacture a retry policy.
