# Laravel queue best practices (production-oriented)

## Design jobs for at-least-once execution
Queues generally provide *at-least-once* delivery. Always assume a job can run more than once:
- Use idempotency keys for external side effects (billing, emails, notifications).
- Use database unique constraints to prevent duplicate writes.
- Prefer “insert-if-not-exists” patterns where possible.

## Keep jobs small and observable
- Pass IDs, not full Eloquent models or huge payloads.
- Decompose large work into batches or chained jobs.
- Add structured logs and (if using Horizon) tags.

## Timeouts, retries, and backoff
- Set a job timeout that matches your p95 execution time + buffer.
- Use exponential backoff for flaky dependencies; cap attempts and exceptions.
- Ensure worker timeout is *less* than broker/driver retry_after to reduce duplicate processing.

## Use after-commit where correctness matters
If dispatching from a DB transaction, ensure jobs publish after commit to avoid reading uncommitted data.

## Concurrency and queue separation
- Separate queues by workload profile and priority.
- Scale worker processes per queue based on queue depth and latency, not guesswork.
