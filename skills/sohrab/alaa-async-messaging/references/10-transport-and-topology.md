# Transport and topology

Read this before declaring an exchange, a queue, or a binding, and before answering "which broker should
this use". It owns the transport decision and the shape of the topology. It owns no name: every exchange,
queue and routing-key name comes from `alaa-services-contract references/23-queue-and-exchange-registry.md`.

## RabbitMQ is the only broker this fleet runs

There is one broker, and it is RabbitMQ. Events and commands are distinguished by **topology** — which
exchange a message is published to and who declares the queue — not by transport, and not by running a
second broker for one of the two kinds. The durability seam for publishing a fact is the **transactional
outbox**, described in `20-publishing-and-the-outbox.md`, not a second broker with a longer retention
window.

The evidence for the rule, so it is not re-litigated per service: `alaa-services-contract` registers every
exchange and queue the fleet has or is owed and contains no log-structured broker, no topic, no partition,
no consumer group and no offset; the `alaa-go-chi` kit ships `mqkit`, `outboxkit` and `jobkit` and no
package for any other broker; the registered async metric family is `alaa_queue_*` and `alaa_outbox_*`, and
it defines consumer lag as the age of the oldest unconsumed message, which is a queue notion rather than an
offset notion.

**When a design genuinely needs a log-structured broker, file a kit change request and stop.** Two problems
are the genuine cases, and both are properties of the requirement rather than preferences about tooling:
long-retention replay to consumers that do not exist yet, and fan-out wider than a topic exchange serves.
The path is the template at `alaa-go-chi-development assets/templates/kit-change-request.md`, reached
through `/alaa-go-chi-development` (`$alaa-go-chi-development`), filed against the kit and naming the
requirement and the retention or fan-out figure that a topic exchange cannot meet. Designing against a broker the platform does not run
produces a design nobody can deploy, and the cost lands on the service that believed the design.

## Event or command — decide the kind, and the topology follows

An **event** states a fact that already happened; the producer does not know who listens and does not change
when a listener is added. An event is published to the producer's own topic exchange, and each consumer
declares and binds its own queue.

A **command** states work the sender requires a specific service to do; the sender's operation is incomplete
until that service acts. A command is published to the receiver's command exchange, and it lands in a queue
the **receiver** declares, because the receiver owns what work it accepts and how that work is retried and
dead-lettered.

The observable that decides the kind: search the producing repository for the receiver's service name. A
publish call site that names one specific receiving service is publishing a command. A call site that names
only its own exchange is publishing an event. If the producer would need a change when a listener is added,
it is a command that has been mislabelled.

The grammar, every worked example, the registry rows, and the registration procedure are
`alaa-services-contract references/23-queue-and-exchange-registry.md`. Do not restate that grammar here and
do not invent one locally: a name that does not match the registry cannot be recorded, and an unrecorded
durable queue is one nobody drains.

## Queue type

**Declare a quorum queue for any queue whose loss of a message would require human reconstruction of state,
and a classic queue otherwise.** The observable that decides it: the queue carries a message whose effect
cannot be recomputed from another store — a command that triggers an external send, a payment, or a
notification. A quorum queue replicates the message before confirming it, at a higher write cost; a classic
queue on a failed node loses its unreplicated messages, and that loss is invisible to both producer and
consumer.

**A quorum queue's `x-delivery-limit` is set explicitly at declaration.** Redelivery is what turns a poison
message into an infinite loop, and the delivery limit is the only bound the broker itself enforces. The
value is `alaa-services-contract`'s; that one is set is this file's rule.

## Delayed retry

**Implement a delayed retry with a TTL-plus-dead-letter-exchange pair — a `<queue>.retry` queue with a
message TTL whose dead-letter target is the live queue.** It uses only core broker features, so it survives
a broker upgrade and works identically on every environment.

**A broker plugin is used only when the plugin is listed in the service's committed broker provisioning file
and that file is named in the change.** A plugin that one environment has and another does not produces a
topology that works in staging and silently drops delayed messages in production, and the failure appears as
work that never runs rather than as an error.

## Connection security

**Every broker connection uses TLS unless both endpoints are defined in one committed Compose or chart file
in the same repository, and the change names that file.** The observable is the connection URI scheme:
`amqps://` satisfies the rule everywhere; `amqp://` satisfies it only under the named-file exception. A
broker connection carries every message body in the clear, so an untrusted network segment between the two
endpoints exposes every payload the service publishes.

**Every environment has its own vhost, and every application connects with its own user holding permissions
on that vhost only.** A shared vhost lets one environment's misrouted binding consume another's messages,
and a shared user makes the audit trail unable to say which service published a message.

**The default `guest` user is removed or restricted to loopback before any service connects.** It is a
published credential with full permissions, so leaving it reachable makes every other control decorative.

**No credential, certificate or connection string is committed.** A credential in git history outlives the
commit that removed it, so the only remedy is rotation.

## Not owned here

Names and the registry: `/alaa-services-contract` (`$alaa-services-contract`). Broker cluster, vhost and
permission administration on the platform: `/caas-arvan-kuber` (`$caas-arvan-kuber`). Container and chart
expression of a broker: `/alaa-docker-production` (`$alaa-docker-production`) and `/alaa-k8s-helm`
(`$alaa-k8s-helm`).
