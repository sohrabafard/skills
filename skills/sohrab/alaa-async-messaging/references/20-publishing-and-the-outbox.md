# Publishing and the outbox

Read this before writing a publish call, before adding or tuning an outbox relay, and whenever deciding
whether a fact has to survive the broker being unreachable. It owns the publish path, the outbox row's state
set and transitions, relay tuning, and the outbox's operational surface.

## The ordering rule

**Publish after the transaction that made the fact true commits.** A message published inside the
transaction is visible to a consumer that then reads a row the transaction has not committed, and when the
transaction rolls back the message describes something that never happened. This defect does not reproduce
under low load and does not appear in a single-file review; it appears in production as a consumer reading a
row that does not exist.

Two mechanisms satisfy the rule and there is no third:

- **The outbox.** The message is written to a durable row inside the business transaction, and a separate
  relay publishes it. Use it whenever the fact must reach a consumer at least once.
- **Commit-aware dispatch.** The framework defers the publish until after commit. Use it only when losing
  the message is acceptable, because the process can die between the commit and the publish and nothing
  records that the message was owed.

**Choosing between them is a recorded decision, not a default.** A change that introduces a durable fact
either introduces the outbox or documents the route as best-effort. Choosing silently produces the second
while everyone downstream believes the first.

## Publisher confirms

**A publish that has not been confirmed by the broker has not happened, and code must not report success for
it.** Without confirms, a publish returns as soon as the frame reaches the socket, so a broker that dies
before persisting the message loses it while the application records a success — and the loss is
undetectable from either side afterwards.

Two consequences:

- **A request-path publish does not wait on a confirm.** Waiting couples user-facing latency to broker
  latency, which is the coupling the outbox exists to remove. Durability comes from the outbox row.
- **A relay publish waits for the confirm and treats an unconfirmed publish as a failure**: the row is not
  advanced, and the next relay pass republishes it. Advancing a row on an unconfirmed publish converts a
  broker restart into silent data loss.

**Unverified this session:** `mqkit`'s publisher-confirm surface, its publish timeout behaviour, and its
behaviour on a broker nack were not readable from the mounted repository. Verify each against `mqkit` source
before writing code that depends on one, and record what you found. Do not assume the confirming publisher
exposes a timeout.

The publish timeout and the retry budget are values, and values are
`alaa-services-contract references/22-failure-load-and-deprecation-contract.md`.

## The outbox row: state set and transitions

The state set is three states and no more:

| State | Meaning | Leaves it when |
|---|---|---|
| `pending` | written inside the business transaction, not yet claimed | a relay claims it |
| `claimed` | one relay pass holds it, with the claim's own expiry | the publish is confirmed, or the claim expires |
| `published` | the broker confirmed it | the row is deleted or archived |

Rules that hold on the transitions:

- **A row is claimed with `FOR UPDATE SKIP LOCKED`, never with a read-then-update.** Two relays running the
  same read-then-update both claim the same row and publish it twice.
- **A row leaves `claimed` only after the broker confirms the publish.** The kit's relay expresses this by
  deleting the row inside the claiming transaction and committing that delete only after the acknowledgement
  (`outboxkit/queries.go:3-11`, `outboxkit/doc.go:4-6`), so a relay that dies mid-publish rolls back its
  delete and the row is claimable again.
- **A claim carries an expiry, and an expired claim returns the row to `pending`.** Without an expiry, a
  relay that dies between claim and confirm strands the row forever and the fact is never delivered.
- **A row is never deleted to clear a backlog.** Consumers tolerate at-least-once delivery, so republishing
  is safe and a deleted row is a lost fact that nothing will detect.
- The claim query itself, its index, and the transaction-pooling constraints on it are
  `alaa-data-layer references/30-concurrency-projections-and-pooling.md` — `/alaa-data-layer`
  (`$alaa-data-layer`).

## Relay tuning

Two environment keys exist and no others: `OUTBOX_BATCH` (default `100`) and `OUTBOX_TICK` (default `500ms`)
— `outboxkit/config.go:10-14`.

**Set the batch so that one pass finishes well inside the tick.** Batch size multiplied by the measured p99
publish duration is the pass duration; when that exceeds the tick, passes overlap, claims contend, and
throughput falls as concurrency rises. State both numbers in the change.

**Raise the batch before shortening the tick when the backlog grows.** A shorter tick spends a database
round trip per pass on an empty table for the whole time the system is idle, which is most of the time.

### Four absences, stated as absences

`outboxkit` **has no publish timeout, no attempt counter, no backoff, and no quarantine.**
`outboxkit/relay.go:100-109` retries a failing publish forever on the tick loop. These are not knobs with
inconvenient defaults; the keys that would express them are absent from the code. Three obligations follow:

1. **Never configure a service as though those knobs exist.** A value set for a key the kit does not read
   changes nothing and reads in review as a control that is in place.
2. **A permanently failing row will be retried forever, so a permanently failing row must be prevented
   upstream**, at the point that writes it: validate the message body at write time, because the relay has
   no way to give up on it.
3. **Watch `alaa_outbox_oldest_age_seconds`**, since it is the only observable that separates a slow relay
   from a row that will never publish. `60-telemetry-and-proof.md` holds the full set.

Needing one of the four is a kit change request filed on
`alaa-go-chi-development assets/templates/kit-change-request.md`, through `/alaa-go-chi-development`
(`$alaa-go-chi-development`) — never a local reimplementation of the relay.

## The outbox operational surface

This is what an operator or an agent may do to a live outbox, and what it must never do.

| Situation | Do this | Never do this |
|---|---|---|
| Depth climbing, publish counter climbing | Nothing to the outbox: the relay is working and the broker or consumer is the constraint. Raise `OUTBOX_BATCH` only after confirming pass duration fits the tick | Delete rows to make the graph flat |
| Depth climbing, publish counter flat | Check the broker connection first, then the relay process. The relay is not publishing | Restart the relay repeatedly without reading why it stopped |
| One row `claimed` past the claim expiry, no live relay holding it | Return it to `pending` and let the normal relay take it | Publish it by hand; a hand publish bypasses the confirm and the counter |
| Oldest-row age climbing while depth is flat | One row is failing permanently. Read its body, fix the cause, and let the relay drain it | Delete the row before capturing its body — the body is the only evidence of the defect |
| Broker down, outbox filling | Nothing. This is the design working; the request path is unaffected | Fail requests, or bypass the outbox with a direct publish |
| Draining a backlog after an outage | Let the relay drain at its configured rate, and watch consumer error rate as it does | Raise the batch mid-incident so a backlog becomes a thundering herd on the consumer |

**Readiness: the outbox table is a required dependency and the broker is not.** A service reports itself not
ready when it cannot reach the outbox table, because it can no longer accept the writes that produce facts.
A service does not report itself not ready when the broker is unreachable, because the outbox is precisely
what lets it keep serving through a broker outage, and failing readiness on the broker converts a broker
outage into a service outage. This is deployed today: the `tusd` service's readiness check includes the
outbox table and deliberately excludes RabbitMQ.

## The seam every external-send skill consumes

**An external send — a provider message, an upload completion, a notification — is dispatched from a durable
row, never from inside the request that created it.** The request commits the row; a worker or relay
performs the send. A send issued inside the request makes the provider's availability the route's
availability, and a provider timeout then leaves nobody able to say whether the send happened.

**The row's public id is the idempotency key presented to the provider**, unchanged across every retry of
that send. A key derived from request content — recipient plus template plus body — collides between two
legitimate sends and suppresses the second one, which on an OTP path means a user who asked twice receives
one code. Key doctrine is `alaa-reliability-sla references/60-idempotency.md` — `/alaa-reliability-sla`
(`$alaa-reliability-sla`).

**Where a provider offers no idempotency mechanism, the row's state is the guarantee**: only a row in the
state that means "not yet sent" may dispatch, and the transition to "sent" commits before the next attempt
is possible. Without that, a redelivery re-sends and the provider has no way to refuse.
