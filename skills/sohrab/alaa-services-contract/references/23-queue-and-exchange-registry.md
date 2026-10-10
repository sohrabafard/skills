# Queue And Exchange Registry

This file owns two things and nothing else: the **grammar** every Ala broker name follows, and the
**registry** of every exchange and queue that exists in the fleet or is owed to it. A service that needs to
talk to another service reads the registry to learn where to publish and what to bind, instead of reading
the other service's code.

What this file does not own:
- The **domain event envelope** — the field set inside an event message — is owned by
  `20-operational-and-observability-contract.md`.
- The **scope test** that decides whether the envelope binds at all — internal framework message versus
  inter-service message — is owned by the same file, under `Scope: which messages this envelope binds`.
  Read it before registering a queue, because the answer decides which envelope column below applies.
- The **notification command payloads**, the notification envelope aliases, and the per-producer matrix are
  owned by `27-notification-service-contract.md`.
- Prefetch values, acknowledgement mechanics, publisher confirms, and DLQ replay procedure are owned by
  `/alaa-async-messaging` (`$alaa-async-messaging` in Codex). Publish timeout, retry budget, and the durable
  outbox path are owned by `22-failure-load-and-deprecation-contract.md`.
- That every consumer sets an explicit prefetch is owned by `22-failure-load-and-deprecation-contract.md`.

## Events and commands are different messages with different topologies

Two message kinds cross the broker, and confusing them is what produces a queue in the wrong repository.
Decide the kind first; the topology follows from it with no further choice.

**An event states a fact that already happened.** The producer does not know who listens, does not know how
many listeners there are, and its behaviour does not change when a listener is added or removed. An event
is published to the producer's own topic exchange `<service>.events`, and each consumer declares its own
queue and binds it. The producer declares no consumer queue, because a producer that declares one has
encoded a specific consumer's name into its own deployment and a second consumer cannot subscribe without
a producer change.

**A command states work the sender requires someone to do.** The sender knows exactly which service must
act, and the sender's own operation is incomplete until that service acts. A command is published to the
receiver's command exchange `<service>.commands` with the receiver's routing key, and it lands in a queue
the **receiver** owns and declares, because the receiver owns what work it accepts and how that work is
retried, dead-lettered, and drained.

The owner's own worked example, and it is the one to copy: `auth` telling `notification` to send an OTP is
a command. `auth` knows the receiver, and the login flow is not finished until the OTP is dispatched. It
therefore publishes to `notification.commands` with routing key `sms.send_pattern.v1`, and the message
lands in `notification.command.sms.send_pattern.v1`, a queue `notification` declares. It does not land in
a queue named for `auth`, and `auth` declares no queue for it. The mirror case: `auth.session.created.v1`
is an event, because `auth` neither knows nor cares which services react to a new session.

How to tell them apart when the message looks like both: name the message out loud. A name in the past
tense describing something that is already true (`comment.comment.created.v1`) is an event. A name in the
imperative describing work not yet done (`sms.send_pattern.v1`) is a command. If the producer would have
to be changed when a listener is added, it is a command that has been mislabelled as an event.

Observable that decides which kind a message is: search the producing repository for the receiver's service
name. A publisher whose call site names one specific receiving service is publishing a command and must use
the command topology; a publisher whose call site names only its own exchange is publishing an event.

## Naming grammar

Every name below is lowercase, uses `.` as the segment separator, and uses `_` inside a segment. A hyphen
is not a separator in any broker name, because `auth-profile.events` and `auth.events` are two namespaces
for one service and an operator cannot tell which one a binding meant.

| Kind | Grammar | Exchange type | Example |
|---|---|---|---|
| Event exchange | `<service>.events` | `topic`, durable | `auth.events` |
| Command exchange | `<service>.commands` | `direct`, durable | `notification.commands` |
| Command dead-letter exchange | `<service>.commands.dlx` | `direct`, durable | `notification.commands.dlx` |
| Command queue | `<service>.command.<family>.v<major>` | — | `notification.command.sms.send_pattern.v1` |
| Event consumer queue | `<consumer-service>.<producer-service>.<purpose>` | — | `notif.auth.user_projection` |
| Service-internal work queue | `<service>.jobs.<lane>` | — | `auth.jobs.sms` |
| Retry queue | `<queue>.retry` | — | `notif.retrieve_users.retry` |
| Dead-letter queue | `<queue>.dlq` | — | `notif.retrieve_users.dlq` |

Routing keys:
- An event's routing key is the `message_type` value byte-for-byte, with no substitution.
  `20-operational-and-observability-contract.md` owns the field; this file owns its use as a routing key.
  Rewriting `.v1` to `.version-1`, `_` to `-`, or applying any other transformation is forbidden, because an
  operator holding a binding must be able to paste it into a code search and land on the producer.
- A command's routing key is the `<family>.v<major>` segment of its queue name — `sms.send_pattern.v1` for
  queue `notification.command.sms.send_pattern.v1`. The receiver's exchange is `direct`, so the routing key
  and the queue are one-to-one.
- A dead-letter routing key is the live routing key with `.failed` appended, on a `direct` DLX.

Two prohibitions with their positive replacements:
- Publishing to the AMQP default exchange (`""`) with a queue name as the routing key is forbidden. Publish
  to the owning exchange named above instead. The default exchange binds the producer to one consumer's
  queue name, so adding a second consumer requires a producer change.
- A shared exchange named `events`, or any exchange name that does not begin with an Ala service identity,
  is forbidden. Use `<service>.events`. One namespace shared by two producers means one over-broad binding
  pattern delivers another service's traffic to a consumer that cannot parse it.

Every consumer declares `<queue>.dlq` as its own dead-letter queue in the same change that declares the
queue, because a queue with no dead-letter target either redelivers a poison message forever or drops it,
and both look like a working consumer from the outside.

**A publisher binding that resolves to a log, a file, or a no-op sink outside an automated test is not a
publisher.** Its messages do not exist for any consumer while its own repository documentation says they do,
so every downstream service believes it is subscribed and receives silence. In every non-test environment
the publisher binding resolves to the broker publisher, and a service that publishes anything lists the
broker as a `required: true` check in `/api/ready`.

Observable that decides compliance for a declared topology: the exchange name, the binding pattern, and the
queue names appear in committed configuration or topology-declaration code in the owning repository; the
routing key passed at the publish call site is the same variable that carries `message_type` for an event,
or the constant matching the queue's `<family>.v<major>` segment for a command; and the publisher binding
resolves to a broker client rather than a logger.

**A service-internal work queue is still registered here, and its name still follows the grammar.** The
scope test in `20-operational-and-observability-contract.md` frees an internal message from the envelope; it
frees nothing from the name. Two services that both declare a queue called `events` or `default` on the same
vhost collide with each other regardless of what is inside the messages, and the collision surfaces as one
service consuming the other's jobs. Register the name; leave the body to the framework.

## Registering a queue before declaring it

A service may add a queue or an exchange whenever the rule above permits one. It registers the name in the
table below **before** the code that declares it merges. There is no informal path and no "add it later".

1. Add the row to the registry table with every column filled, including `Consumes`. A row whose consumer is
   unknown is a queue nobody drains, and an undrained durable queue grows until the broker refuses publishes
   for every service on the vhost.
2. Merge that row before or in the same change as the topology declaration. A name in code that is not in
   this table is a contract violation on the day it merges, not on the day someone notices.
3. Renaming or removing a registered name follows the deprecation procedure in
   `22-failure-load-and-deprecation-contract.md`; a queue name is a contract surface there.

Observable that decides compliance: for every exchange and queue name that appears in a repository's
committed topology declaration, configuration, or `.env.example`, a row with that exact name exists in the
table below. A name in a repository with no row here fails; a row here with no repository is either a `gap`
or `planned` row and says so in its `Status` column.

## Status vocabulary

Every row carries exactly one status, and each means one thing:
- `conforming` — the name exists in committed code or configuration and matches the grammar above.
- `non-conforming` — the name exists in committed code or configuration and does not match the grammar. The
  row names what it becomes.
- `gap` — the rule above requires this name to exist and no repository declares it. The row names the
  service that owes it.
- `planned` — a repository documents the name as future work in a committed design document, and no code
  declares it. A `planned` row is not a licence to bind to it.

## Registry: exchanges

| Exchange | Owning service | Kind | Purpose | Publishes | Consumes | Status |
|---|---|---|---|---|---|---|
| `auth.events` | `auth` | event, topic | `auth` domain facts: sessions, tokens, profile changes | `auth` | any service that binds | `conforming` in code (`config/outbox.php:6` default), `non-conforming` in `.env.example:238`, which overrides it to `auth-profile.events` |
| `content.events` | `content` | event, topic | `content` domain facts: course, set, content changes | `content` | any service that binds | `gap` — `content` publishes to an exchange literally named `events` (`app/Support/Content/RabbitMqIntegrationEventPublisher.php:19`, `.env.example:101`) |
| `comment.events` | `comment` | event, topic | `comment` domain facts: comments, replies, likes, moderation | `comment` | any service that binds | `gap` — no exchange is configured at all (`config/queue.php:84` carries a queue name only) |
| `entitlement.events` | `entitlement-api` | event, topic | grant and entitlement facts | `entitlement-api` | any service that binds | `gap` — not declared; only `entitlement-api`'s legacy outbox relay publishes these facts, through the default exchange (see `entitlement.projector.work`) |
| `notification.commands` | `notification` | command, direct | the fleet's only cross-service ingress into `notification` | every producer service | `notification`; `notif` when it takes over a family | `conforming` |
| `notification.commands.dlx` | `notification` | command dead-letter, direct | dead-lettered commands from the queues below | broker on nack | operator replay | `conforming` |
| `projector.commands` (+ `projector.commands.dlx`) | `entitlement-projector` | command, direct | rule projection tasks, routing key `rule_projection.task.v1` | `entitlement-api` projection relay | `entitlement-projector` executor | `conforming` (`entitlement-api/docs/contracts/source-owned-rule-projection-v1/`, `internal/mq/projection.go:17-24`); production declarer unverified: the executor only passive-declares its queue (`entitlement-projector: internal/execruntime/runtime.go:585`), and `entitlement-api` declares this topology only with `ENTITLEMENT_API_PROJECTION_DECLARE_TASK_TOPOLOGY` on, for tests and local (`entitlement-api: internal/app/projection_worker.go:164-168`) |
| `entitlement.commands` (+ `entitlement.commands.dlx`) | `entitlement-api` | command, direct | rule projection receipts, routing key `rule_projection.receipt.v1` | `entitlement-projector` | `entitlement-api` projection worker | `conforming` (same sources) |
| `<service>.commands` for `auth`, `content`, `comment`, `wa` | each service | command, direct | inbound work another service requires this service to do | the requesting service | the owning service | `gap` — only `notification`, `entitlement-projector` and `entitlement-api` (projection receipts) accept commands today, so every other cross-service instruction is either an HTTP call or absent |

## Registry: queues

| Queue | Owning service | Kind | Purpose | Publishes | Consumes | Status |
|---|---|---|---|---|---|---|
| `notification.command.sms.send_message.v1` | `notification` | command | free-text SMS dispatch | any producer, routing key `sms.send_message.v1` | `notification` | `conforming` (`config/queue.php:192-198`) |
| `notification.command.sms.send_pattern.v1` | `notification` | command | template/OTP SMS dispatch | any producer, routing key `sms.send_pattern.v1` | `notification` | `conforming` (`config/queue.php:203-209`) |
| `notification.command.notification.store.v1` | `notification` | command | store an in-app inbox message | any producer, routing key `notification.store.v1` | `notification` | `conforming` (`config/queue.php:214-220`); stays on `notification` and does not migrate to `notif` |
| `notification.command.user_projection.upsert.v1` | `notification` | command | keep notification's user projection resolvable | every service that owns users | `notification` | `conforming` (`config/queue.php:225-226`) |
| `notification.command.<family>.v1.dlq` for each of the four above | `notification` | dead-letter | failed commands, routing key `<family>.v1.failed` | broker | operator replay | `conforming` |
| `projector.command.rule_projection.task.v1` (+ `.dlq`) | `entitlement-projector` | command | one rule projection task | `entitlement-api` projection relay | `entitlement-projector` executor | `conforming`; replaces `entitlement.projector.work` |
| `entitlement.command.rule_projection.receipt.v1` (+ `.dlq`) | `entitlement-api` | command | one projection receipt | `entitlement-projector` | `entitlement-api` projection worker | `conforming` |
| `entitlement.projector.work` (+ `.retry`, `.dlq`) | `entitlement-api` | command | legacy tuple-projection work | `entitlement-api` outbox relay and `projection-replay` | none since the source-owned rule projection; never add a consumer | `legacy` — removed at the AP-6 cutover (owner decision D2, `source-owned-rule-projection-v1/80-bounds-and-cutover.md`); until then a deployment running the rule projection stops the outbox relay, or the queue grows unbounded |
| `entitlement.reconciliation` (+ `.retry`, `.dlq`) | `entitlement-api` | command | `reconciliation.requested` repair trigger for the legacy projector `reconcile` lane | `entitlement-api` api role, `POST /api/v1/admin/reconciliation/run` | none: the projector `reconcile` consumer was removed 2026-10-09 (`entitlement-projector` `515cdb0`, constitution 3.0.0); never add a consumer | `legacy` — route and event deprecated by owner decision 2026-10-10 and removed at the AP-6 cutover with the legacy outbox publication; until then the route answers `202`, the message is never consumed, and the queue (no `x-max-length`) grows. Replacements: `projection-repair-rule`, `projection-reopen-task`, generation replacement, and the projector drift audit (`entitlement-api: internal/reconciliation/service.go:114`, `internal/mq/topology.go:30-35`, `docs/handoffs/mesh-145d79be-registry-inventory.md` section B; `entitlement-projector: docs/rfc/projector-bounds-defaults.md:291`) |
| `notif.retrieve_users` (+ `.retry`, `.dlq`) | `entitlement-api` | command | resolve an object audience into recipients | requester unverified; no publisher in `entitlement-api` | `entitlement-api` `expansion-worker`; it writes `.retry` and `.dlq` itself | `conforming` (`entitlement-api: internal/mq/types.go:17`, `internal/workers/expansion_worker.go:262-309`) |
| `notif.expand_users` | unverified — `entitlement-api` only publishes and does not declare it; its doc names `notification` as declarer (`entitlement-api: docs/delivery-operators/20-local-bring-up.md:109`, doc only) | command | expand one group principal into users | `entitlement-api` `expansion-worker` (default `AUTH_EXPANSION_PROVIDER_MODE=queue`) | audience/expansion provider, unverified; no reply is read from the queue | `conforming` name (`entitlement-api: internal/mq/types.go:18`, `internal/mq/topology.go:14-20`); `.retry`/`.dlq` unverified |
| `notif.recipient_chunks` | unverified — same as `notif.expand_users` | command | deliver resolved recipient chunks | `entitlement-api` `expansion-worker`, only for a job carrying a `notification_id` | reserved — no consumer is wired | `conforming` name, undrained consumer (`entitlement-api: internal/mq/types.go:19`, `internal/expansion/service.go:576-582`); `.retry`/`.dlq` unverified |
| `auth.jobs.sms` | `auth` | internal job | `auth`'s own SMS send jobs, enqueued and consumed by `auth` | `auth` | `auth` | `gap` — the queue is named `sms` today (`config/queue.php:79`, `.env.example:246`) |
| `comment.jobs.outbox` | `comment` | internal job | `comment`'s own outbox relay job | `comment` | `comment` | `gap` — the queue is named `events` today (`config/queue.php:84`, `.env.example:128`) |
| `content.jobs.outbox` | `content` | internal job | `content`'s own outbox relay job | `content` | `content` | `gap` — the queue is named `events` today (`.env.example:101`) |
| `content.jobs.progress` | `content` | internal job | learner-progress processing | `content` | `content` | `gap` — the queue is named `progress` today (`.env.example:103`) |
| `content.jobs.controlled_ops` | `content` | internal job | controlled-operations execution | `content` | `content` | `gap` — the queue is named `controlled-ops` today (`.env.example:109`) |
| `content.jobs.default` | `content` | internal job | unclassified Laravel jobs | `content` | `content` | `gap` — the queue is named `default` today (`.env.example:179`) |
| `notification.jobs.sms` | `notification` | internal job | legacy `notifications.consume` work during the migration window | `notification` | `notification` | `gap` — the queue is named `sms` today (`config/queue.php:80`) |
| `notif.notification.command.sms.send_message.v1` | `notif` | command | `notif`'s shadow queue on the existing `notification.commands` exchange | any producer | `notif` | `planned` (`notif-service-go-architecture.md:255-262`) |
| `notif.notification.command.sms.send_pattern.v1` | `notif` | command | as above, cut over last because OTP failure hurts most | any producer | `notif` | `planned` |
| `notif.notification.command.user_projection.upsert.v1` | `notif` | command | as above, cut over first because risk is lowest | any producer | `notif` | `planned` |
| `notif.notification.command.user_projection.upsert.v2` | `notif` | command | project-scoped, location-aware projection | any producer | `notif` | `planned` |
| `notif.notification.command.news.broadcast.v1` | `notif` | command | news broadcast dispatch | `news` | `notif` | `planned` |
| `notif.notification.command.news.broadcast_cancel.v1` | `notif` | command | cancel a news broadcast | `news` | `notif` | `planned` |

Not rows, verified 2026-10-10:
- `authz-sidecar` uses no broker: a synchronous HTTP checker with no AMQP module (`authz-sidecar: go.mod:5-22`, `internal/httpserver/server.go:51-55`).
- `authz-openfga` uses no broker: the engine is PostgreSQL-only (`authz-openfga: docker-compose.yml:27`). The queues its `verification/extraction-handoff/broker/` harness polls are non-runtime test fixtures.
- `entitlement-api`'s projection-worker startup probe publishes to an undeclared `entitlement.projection.probe.<uuid>` on the default exchange, unroutable by design, to prove the broker rejects a forged AMQP `user_id`; no queue exists (`entitlement-api: internal/mq/user_probe.go:20-27`).

## The `auth` to `notification` command path

`auth` has no command path to `notification` at all. It sends OTP by calling the SMS provider directly
through `app/Classes/sms/MedianaClient.php`, behind `MedianaChannel` and `MedianaPatternChannel`. That is
not a queue this registry can classify; it is the absence of one, and it is recorded here so the next agent
does not conclude from `auth`'s code that a direct provider call is the platform pattern.

The name the path will take when it is built: `auth` publishes to exchange `notification.commands` with
routing key `sms.send_pattern.v1`, landing in the existing `notification.command.sms.send_pattern.v1`
queue. `auth` declares nothing. No new name is registered, because the receiver's queue already exists —
which is the point of the command topology.

Until that change ships, `auth` is the fleet's one service that reaches an external provider on the
user-facing login path with no broker between them, so a Mediana outage is an `auth` outage.

## `notification` and `notif`

`notification` is a Laravel service and is the live owner of every command queue above. `notif` is a Go
service built on the `alaa-go-chi` kit and is its intended successor once the kit stabilises.

- `notif` is not live. Its repository is a scaffold: its own `docs/BIG_PICTURE.md` marks domain behaviour,
  storage, queues, and route families as unconfirmed until implemented, and no Go file declares a queue.
  Every `notif` row above is `planned` and is evidence of a committed design, not of a running consumer.
- The migration is family-by-family, not service-by-service: `notif` binds its own queues to the existing
  `notification.commands` exchange and shadow-processes one family at a time, comparing receipts against
  `notification` before each cutover. Producers change nothing throughout — same exchange, same routing
  keys, same envelopes — which is the property the command topology was chosen for.
- `notification.command.notification.store.v1` does not migrate. It stays on `notification`, frozen except
  for security fixes, until the in-app inbox finds its own service.
- Do not delete a `notification` row from this table when its `notif` counterpart starts consuming. Both
  rows stay until the cutover completes for that family, because during the shadow window both queues exist.

## Companion skills

- `/alaa-async-messaging` (`$alaa-async-messaging` in Codex) — prefetch, acknowledgement, publisher
  confirms, quorum-queue policy, and DLQ replay for any queue in this table.
- `/alaa-laravel-job-rabbitmq` (`$alaa-laravel-job-rabbitmq` in Codex) — Laravel producer and consumer
  wiring for the Laravel services above.
- `/alaa-golang` (`$alaa-golang` in Codex) — Go producer message structs and their snake_case tags.
- `/alaa-prompting-guide` (`$alaa-prompting-guide` in Codex) — every model and effort question.
