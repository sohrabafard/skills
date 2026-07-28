# Source map

Read this before repeating a claim about broker behaviour, kit behaviour, or a framework queue API that a
version could change. It states where truth lives and in what order, and what obliges a re-check.

## Source order

1. **Repository truth**, which outranks everything below it for what this deployment actually does: the
   service's queue configuration, its topology declaration code, its `.env.example`, its worker command or
   Deployment, its tests, and its runbooks.
2. **Kit source** for anything `mqkit`, `outboxkit` or `jobkit` does. Read the package source, not a
   decision log and not a summary: the kit carries knobs that were ratified and never implemented, and
   `20-publishing-and-the-outbox.md` records four such absences in `outboxkit` alone. Ratified is not
   implemented.
3. **The fleet contract** for every name and every value:
   `alaa-services-contract references/22-failure-load-and-deprecation-contract.md` for values,
   `alaa-services-contract references/23-queue-and-exchange-registry.md` for broker names and topology
   grammar, and `alaa-services-contract references/24-metric-registry.md` for metric names —
   `/alaa-services-contract` (`$alaa-services-contract`).
4. **Official broker documentation**, for behaviour the repository does not settle:
   - RabbitMQ documentation: https://www.rabbitmq.com/docs
   - Dead-letter exchanges: https://www.rabbitmq.com/docs/dlx
   - Consumer prefetch: https://www.rabbitmq.com/docs/consumer-prefetch
   - Heartbeats: https://www.rabbitmq.com/docs/heartbeats
   - Quorum queues: https://www.rabbitmq.com/docs/quorum-queues
   - Publisher confirms: https://www.rabbitmq.com/docs/confirms
5. **Official framework documentation** for the Laravel queue plane, at the version the service runs:
   https://laravel.com/docs — queues, events, and Horizon. For the RabbitMQ transport package's own
   behaviour, switch to `/alaa-laravel-job-rabbitmq` (`$alaa-laravel-job-rabbitmq`), which owns it.
6. **Community posts and answers**, for locating an official term or recognising a symptom only. They are
   never authority for broker safety, acknowledgement semantics, retry behaviour, or current version
   behaviour.

**Record the source and the date beside any fact you take from level 4 or 5.** An undated external fact
looks authoritative and gets copied forward, which is how a skill rots without anyone noticing.

## Freshness triggers — verify before acting

- The task names `latest`, `current`, `upgrade`, a CVE, or a broker or framework major version.
- The task changes prefetch, heartbeat, delivery limit, quorum-queue policy, dead-lettering, publisher
  confirms, or reconnect behaviour.
- The task depends on a kit capability: whether `mqkit` exposes a publish timeout, how it reports a nack,
  what `outboxkit` does on a failing publish. **`mqkit`'s publisher-confirm surface, its timeout behaviour
  and its nack behaviour were not verified when this file was written** — check kit source and record what
  you find.
- The task depends on an environment key existing. `OUTBOX_BATCH` and `OUTBOX_TICK` exist; `MQ_PREFETCH` was
  reported as ratified and not implemented and was not re-derived. Verify the key is read by the code before
  configuring it.
- A queue or exchange name is being added, renamed, or removed: the registry procedure in
  `alaa-services-contract references/23-queue-and-exchange-registry.md` applies before the code merges.

## Kafka and other log-structured brokers

This fleet runs RabbitMQ only, so no upstream documentation for another broker is a source for a design
decision here. `10-transport-and-topology.md` states the rule and the kit-change-request path for a design
that genuinely needs one. Reading another broker's documentation to understand a concept is fine; citing it
as the basis for a topology on this fleet is not.
