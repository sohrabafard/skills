# Consumer acknowledgement timeout and cancellation

## Consumer acknowledgement timeout and cancellation

In RabbitMQ 4.3, acknowledgement timeouts apply to quorum queues (and its JMS queues), not classic
queues or streams. For AMQP 0.9.1 with negotiated `consumer_cancel_notify`, the broker sends `basic.cancel`
to the timed-out consumer and leaves the channel open; without it, channel closure remains the fallback.
Earlier broker behavior must be checked against that release. Source: [4.3 release notes](https://www.rabbitmq.com/blog/2026/04/23/rabbitmq-4.3-release),
verified 2026-09-29. Cancellation returns do not advance the 4.3 delivery count; see `../40-dead-letter-and-replay.md`.

Inspect the installed client's capability negotiation and cancellation handler. An open channel or
connection does not prove an active subscription. Recover the cancelled subscription through bounded recovery or exit
non-zero for supervisor recovery; expose cancellation and loss of active consumption without payload or
credential logging. Test timeout, cancellation, resubscription and the no-capability fallback before rollout.
Do not claim an older pinned driver implements recovery without source and runtime evidence.
