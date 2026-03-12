# RabbitMQ topology & policies (ops checklist)

This document is broker-side guidance. It complements application configuration.

## Baseline hardening
- Create separate vhosts per environment (dev/staging/prod).
- Create per-app users with least-privilege permissions for their vhost.
- Disable or restrict guest/guest to localhost only.
- Enable TLS for non-local traffic where required.

## Queues, exchanges, routing
- Prefer explicit naming: <app>.<domain>.<purpose>
  Example: billing.payments.capture, notifications.email.send
- For dead-lettering:
    - Create a DLX (dead-letter exchange) per domain or app.
    - Route failures to <queue>.dlq (dead-letter queue) or a per-domain DLQ.
- For delayed retries:
    - Use TTL + DLX pattern or a delayed message exchange plugin (if approved).

## Quorum queues
For high durability and simpler HA semantics, consider quorum queues for critical workloads.
Trade-off: higher write overhead vs classic queues.

## Observability
- Enable RabbitMQ Management plugin (restrict access).
- Monitor: ready, unacked, publish rate, ack rate, consumer count, node health.
- Alert on: growing ready depth, high unacked, consumers down, disk/memory alarms.

## Operational commands (examples)
Always validate commands for your environment; examples only:

- List queues:
  rabbitmqctl list_queues name messages_ready messages_unacknowledged consumers

- Set a policy (example only):
  rabbitmqctl set_policy --apply-to queues "dlx" "^myapp\." '{"dead-letter-exchange":"myapp.dlx"}'
