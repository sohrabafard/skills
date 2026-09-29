# Topology

## Topology

**Every queue declares a dead-letter target in the same change that declares the queue.** A queue with no
dead-letter target either redelivers a poison message forever or drops it, and both outcomes look like a
working consumer from outside.

The shapes, with names taken from `alaa-services-contract references/23-queue-and-exchange-registry.md`:

- A live queue's dead-letter queue is `<queue>.dlq`.
- A command family's dead-letter exchange is `<service>.commands.dlx`, of type `direct`.
- A dead-letter routing key is the live routing key with `.failed` appended.
- A delayed-retry queue is `<queue>.retry`, and its dead-letter target is the **live** queue, which is what
  makes the delay work.

**A dead-letter queue declares no dead-letter target of its own.** A DLQ whose failures dead-letter again
produces a chain nobody drains, and the message's origin becomes unrecoverable after the second hop.

**A dead-letter queue has no consumer by default.** Its purpose is to hold messages for a human decision;
attaching a consumer that retries them recreates the loop the DLQ exists to break.

**Every dead-lettered message carries enough context to diagnose it without the original request**: the
original queue and routing key, the correlation or trace identifier, the delivery count, and the failure's
error code. The broker records the reason automatically; the error code has to be put there by the handler,
and its absence is what turns a DLQ into a pile of undiagnosable messages.
