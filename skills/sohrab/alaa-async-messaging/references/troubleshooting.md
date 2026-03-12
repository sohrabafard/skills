# Troubleshooting runbook (Laravel + RabbitMQ + Horizon)

## Horizon shows nothing / no workers
- Confirm Horizon is running: `php artisan horizon:status`
- Ensure Horizon dashboard is accessible and authorized.
- Confirm Redis is reachable; Horizon stores metadata in Redis.

## Jobs processed twice
Common causes:
- timeout >= retry_after (Redis queue): worker killed but job becomes available again before ack.
- consumer crash mid-job without idempotency.
  Fix:
- Ensure `timeout` is a few seconds LESS than `retry_after`.
- Make jobs idempotent.
- Add logging of attempts and job IDs.

## RabbitMQ connection drops
- Set heartbeat and timeouts.
- Ensure long-running jobs don’t block heartbeats (consider per-job I/O design).
- Validate TLS config; mismatched protocol/ports causes handshake failures.

## Throughput too low
- Increase worker concurrency (numprocs).
- Split queues; avoid long jobs starving short ones.
- For RabbitMQ: prefer push consumption (`rabbitmq:consume`) if supported.
- Reduce N+1 queries and synchronous API calls inside jobs.

## Workers leak memory / get killed
- Set worker memory limits and max-jobs/max-time where available.
- Ensure heavy libraries are not accumulating state.
- Restart workers periodically as a pragmatic mitigation.
