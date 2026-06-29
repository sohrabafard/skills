# Notification Service Contract (Cross-Service)

This reference is the cross-service contract for how every Ala service talks to the `notification`
service, so producers integrate the same way.

Source of truth: the `notification` repository owns its async contract in
`notification/docs/async-contracts.md` and its channel inventory in
`notification/docs/list_of_channels.md`. This reference mirrors those for cross-service consistency and
adds the `entitlement-platform` audience-resolution handshake. When this file and the notification repo
disagree, the notification repo wins — reconcile this file (or update the notification repo in the same
change) rather than improvising a variant.

Status: the notification command ingress below is implemented in the notification repo. Per-producer
onboarding and the audience-resolution-to-command bridge are completed after producer contracts are
defined; mark not-yet-built parts `reserved`.

Platform architecture context: the canonical high-level architecture (shared doc
`docs/high-level-Alaa-system-artitecture.md`, symlinked into each repo) describes the broader
notification system as still-being-evaluated components — a **Notification Core** business service
(delivery rules, user delivery state, unread, CTA metadata), a **Realtime Hub** for online SSE/WebSocket
fan-out, **Delivery Workers** for web/SMS/(future) push, and an internal **Queue/Broker** (Redis Streams
or RabbitMQ). This reference documents the *currently implemented* cross-service ingress
(`notification.commands` over RabbitMQ); the larger component split and the internal delivery backbone
are an evaluated target, not finalized. Keep producer integrations on the implemented ingress and treat
the rest as `reserved` until the notification architecture is settled.

Platform shape: most Ala services are Laravel; only the `entitlement-platform` Go services are Go. This
contract is language-neutral but Laravel-first (snake_case JSON everywhere), because PHP `json_decode`
is case-sensitive and is the majority consumer/producer runtime.

## Roles

- Producer service: publishes RabbitMQ commands to notification instead of calling it over business
  HTTP (`auth`, `content`, `comment`, `ticket`, `wa`, `entitlement-platform`, `assessment`, watchtime,
  future services).
- Notification service (the canonical **Notification Core** in the platform architecture): consumes
  commands and performs delivery/storage/user-projection work, with receipt-based deduplication.
  Online fan-out (Realtime Hub) and per-channel Delivery Workers are evaluated components, not yet a
  fixed contract.
- Audience-resolution authority: for access-derived audiences, `entitlement-platform` expands an object
  audience into explicit recipients; it owns the `notif.*` audience queues described below.

## Canonical command ingress (authoritative)

- Exchange: `notification.commands` (type `direct`). Dead-letter exchange: `notification.commands.dlx`.
- Ingress queue connection: `rabbitmq_ingress`. Receipts table: `rabbitmq_command_receipts`.
- Canonical queues and routing keys:

| Queue                                            | Routing key                 | DLQ routing key                    |
|--------------------------------------------------|-----------------------------|------------------------------------|
| `notification.command.sms.send_message.v1`       | `sms.send_message.v1`       | `sms.send_message.v1.failed`       |
| `notification.command.sms.send_pattern.v1`       | `sms.send_pattern.v1`       | `sms.send_pattern.v1.failed`       |
| `notification.command.notification.store.v1`     | `notification.store.v1`     | `notification.store.v1.failed`     |
| `notification.command.user_projection.upsert.v1` | `user_projection.upsert.v1` | `user_projection.upsert.v1.failed` |

- Producers publish to `notification.commands` with the matching routing key; the broker publish
  acknowledgement is the synchronous success boundary.

## Canonical command envelope (every command message)

A JSON object with snake_case keys everywhere, including nested objects (load-bearing: the consumer is
PHP with case-sensitive `json_decode`, so a capitalized nested key silently drops data):

| Field              | Required    | Notes                                                                                                     |
|--------------------|-------------|-----------------------------------------------------------------------------------------------------------|
| `message_id`       | yes         | UUIDv7; the logical message id, not the broker delivery                                                   |
| `message_type`     | yes         | canonical fully-qualified family (e.g. `notification.command.sms.send_message.v1`); legacy alias `family` |
| `message_version`  | yes         | positive int; inferred from the `.vN` suffix if omitted                                                   |
| `occurred_at`      | yes         | RFC3339; defaults to now if omitted                                                                       |
| `producer_service` | yes         | stable `services.name` value; legacy aliases `service_name` / `service_id`                                |
| `correlation_id`   | recommended | tracing id; defaults to `message_id` when omitted                                                         |
| `causation_id`     | optional    | parent id for fan-out debugging                                                                           |
| `idempotency_key`  | yes         | legacy alias `dedupe_key`                                                                                 |
| `payload`          | yes         | plain JSON object — never a serialized Laravel job                                                        |

- Idempotency: ingress deduplicates by `message_id` and by `(message_type, idempotency_key)`; duplicate
  deliveries increment a counter and do not re-run the business action.
- Compatibility aliases (`family`, `dedupe_key`, `service_id`/`service_name`) exist only for the
  migration window; new producers must send the canonical fields.
- The command envelope is NOT project-scoped. Targeting is by explicit recipients in the payload, not
  by a `project_id` field.

## Command families (payload shapes)

- `notification.command.sms.send_message.v1` — `{ message, users: [{ id, mobile }], provider_public_id? }`.
- `notification.command.sms.send_pattern.v1` —
  `{ pattern_code, user: { id, mobile }, pattern_values: [{ key, value }], provider_public_id? }` (exactly one target
  user; `pattern_values` keys must match the stored pattern).
- `notification.command.notification.store.v1` — `{ owner_id, message_public_id }` (`producer_service` becomes the
  stored `service_id`).
- `notification.command.user_projection.upsert.v1` — `{ user_id, first_name, last_name, mobile, national_code }`; the
  canonical path for any service to keep notification's user projection (and ownership) resolvable.

## Recipient model (current) vs channel addressing (reserved)

- Current/implemented: explicit recipients in the payload (`users[]` or `user`).
- Channel/audience addressing is a notification-owned concept tracked in
  `notification/docs/list_of_channels.md` and is NOT part of the implemented command contract today.
  Mirror of the current channel inventory (do not emit channels that are not in that source):
    - auth: `p:<project_id>:user#<user_id>`, `p:<project_id>:ostan#<ostan_id>`,
      `p:<project_id>:shahrestan#<shahrestan_id>`, `p:<project_id>:bakhsh#<bakhsh_id>`,
      `p:<project_id>:shahr#<shahr_id>`, `p:<project_id>:shobe#<shobe_id>`
    - content: `p:<project_id>:course#<course_id>`, `p:<project_id>:set#<set_id>`,
      `p:<project_id>:content#<content_id>` (the content channel applies when a user has access only to
      that content)
    - Status: reserved/planning. When channel addressing is implemented, update this section and the
      notification channel document in the same change.

## Audience-resolution handshake (entitlement-platform)

Separate from the notification command ingress above. These `notif.*` queues are owned and declared by
`entitlement-platform`; they turn an access-derived object audience into explicit recipients. They use
the entitlement-owned envelope below (snake_case, with `schema_version`/`command_id`/`project_id`), not
the notification command envelope.

- `notif.retrieve_users` (consumed by the entitlement `expansion-worker`): `schema_version`,
  `command_id`, `project_id` (UUIDv7), `notification_id`?, `target_type`, `object_type`
  (`course`|`set`|`content`), `content_id`?/`set_id`?/`course_id`?, `need_mobile`, `requested_at`.
- `notif.expand_users` (published by entitlement; consumed by the audience/expansion provider):
  `schema_version`, `command_id`, `project_id`, `notification_id`?, `principal_type`, `principal_key`,
  `need_mobile`, `reason` (`{ type, ref }`).
- `notif.recipient_chunks` (published by entitlement): `schema_version`, `command_id`, `project_id`,
  `notification_id`?, `chunk_no`, `users[]` of `{ user_id, mobile?, reason { type, ref },
  source_grant_revision_id }`.

The nested `reason` object is `{ type, ref }` (lowercase); see entitlement-platform
`docs/api/internal-api.md`. Reserved gap: bridging resolved recipient chunks into
`notification.command.sms.*` commands is not built yet, and the notification consumer of these chunks
is reserved. These messages are an interim, not-yet-converged shape: they do not carry correlation
(`request_id`/`trace_id`) or `producer` attribution, and must gain those fields before any production
consumer is wired. The contract-complete envelope is `notification.commands` (which carries
`correlation_id`).

## Per-service notification matrix

| Service                | Runtime | Direction                                   | Contract                                                  | Status                                                                   |
|------------------------|---------|---------------------------------------------|-----------------------------------------------------------|--------------------------------------------------------------------------|
| `entitlement-platform` | Go      | audience resolution                         | entitlement-owned `notif.*` queues                        | entitlement side implemented; bridge to `notification.commands` reserved |
| `auth`                 | Laravel | producer                                    | `notification.commands` (e.g. `sms.send_pattern` for OTP) | reserved — define payloads at onboarding                                 |
| `content`              | Laravel | producer                                    | `notification.commands`                                   | reserved                                                                 |
| `comment`              | Laravel | producer                                    | `notification.commands`                                   | reserved                                                                 |
| `ticket`               | Laravel | producer                                    | `notification.commands`                                   | reserved                                                                 |
| `assessment`           | Laravel | producer                                    | `notification.commands`                                   | reserved                                                                 |
| `wa`                   | Laravel | future delivery channel inside notification | —                                                         | reserved                                                                 |
| watchtime              | Laravel | producer                                    | `notification.commands`                                   | reserved                                                                 |

Any service that owns users should also publish `user_projection.upsert.v1` to keep notification's
projection current.

## Language-specific rules

- Laravel producers (majority): publish the canonical envelope with snake_case keys; `payload` is plain
  JSON, never a serialized Laravel job; consumers read with case-sensitive `json_decode`. Pair with
  `$alaa-async-messaging` and `$alaa-laravel-job-rabbitmq`.
- Go producers (the two `entitlement-platform` Go services): every message struct must carry explicit
  snake_case `json:"..."` tags, including nested value objects; an untagged nested struct serializes
  capitalized and breaks the case-sensitive consumer. Pair with `$alaa-golang`.

## Anti-patterns

- Capitalized or Go-default JSON keys in any notification or `notif.*` message.
- Inventing queues/exchanges or a bespoke envelope instead of `notification.commands` plus the
  canonical envelope.
- Sending serialized Laravel jobs across repositories.
- Using RabbitMQ as a synchronous query/RPC layer for notification reads.
- Starting new internal business HTTP integrations with notification.
- Omitting `message_id` or `idempotency_key`.
- Leaking or logging recipient PII (`mobile`) beyond what a command needs.

## Companion routing

- `$alaa-async-messaging` and `$alaa-laravel-job-rabbitmq` for producer queue/worker design.
- `$alaa-golang` for the Go producer message structs and tags.
- `$alaa-observability-soc` for `correlation_id` / `causation_id` tracing.
- `$alaa-docs-farsi` when documenting producer integration or notification runbooks.

## Sources of truth

- `docs/high-level-Alaa-system-artitecture.md` — shared canonical platform architecture (symlinked into
  each repo); defines the evaluated Notification Core / Realtime Hub / Delivery Workers / Queue-Broker
  model and the gateway trust boundary.
- `notification/docs/async-contracts.md` — authoritative for the command ingress and envelope.
- `notification/docs/list_of_channels.md` — channel inventory.
- `entitlement-platform/docs/api/internal-api.md` — the entitlement-owned `notif.*` audience messages.
