# Consuming: the acknowledgement point, prefetch, and worker lifecycle

Read this before writing or changing a consumer, before choosing a prefetch or concurrency value, and before
setting a worker's stop budget. It owns where a consumer acknowledges, what each acknowledgement route
means, how the two bounds are derived, and how a consumer behaves across a restart or a dropped connection.

## The acknowledgement point

Use [The acknowledgement point](./30-consuming-ack-and-prefetch/10-acknowledgement-point.md) when deciding when the receipt and business effect are committed relative to broker acknowledgement.

## The three routes out of a handler

Use [The three routes out of a handler](./30-consuming-ack-and-prefetch/20-handler-outcomes.md) when mapping successful, transient, and permanent outcomes to their broker route.

## Consumer-side deduplication

Use [Consumer-side deduplication](./30-consuming-ack-and-prefetch/30-consumer-deduplication.md) when designing the message receipt and idempotency-key check.

## Prefetch

Use [Prefetch](./30-consuming-ack-and-prefetch/40-prefetch.md) when setting an unacknowledged window from measured handler p99.

## Consumer concurrency

Use [Consumer concurrency](./30-consuming-ack-and-prefetch/50-consumer-concurrency.md) when setting worker concurrency and its database pool.

## Graceful stop and rolling restarts

Use [Graceful stop and rolling restarts](./30-consuming-ack-and-prefetch/60-graceful-stop-and-restarts.md) when choosing a worker drain budget or restart sequence.

## Consumer acknowledgement timeout and cancellation

Use [Consumer acknowledgement timeout and cancellation](./30-consuming-ack-and-prefetch/70-acknowledgement-timeout-and-cancellation.md) when assessing timeout behavior and subscription recovery on RabbitMQ 4.3.

## Reconnect

Use [Reconnect](./30-consuming-ack-and-prefetch/80-reconnect.md) when handling connection loss, topology redeclaration, or recovery backoff.

## Two things this file does not decide

Use [Two things this file does not decide](./30-consuming-ack-and-prefetch/90-boundaries.md) when routing Laravel worker details or retry-budget doctrine to their owners.
