# Retry, and who owns it

## Retry, and who owns it

**Backoff shape, jitter, cap, attempt limit and request timeout are doctrine, and doctrine is
`/alaa-reliability-sla`.** This skill states only that the row carries `attempts`
and `nextAttemptAt` so the policy can be applied, and that every value is read from configuration and named
in `/alaa-services-contract`: `outboxBatchSize` (default **25**),
`outboxSendTimeoutMs`, `outboxMaxAttempts`, `outboxBackoffBaseMs`, `outboxBackoffCapMs`,
`outboxReaperStaleAfterMs`. **No literal for any of these appears at a call site** —
`examples/outbox-pattern.ts` takes a policy object and embeds none of them.

A row reaching `outboxMaxAttempts` becomes `abandoned` **and is reported**, never silently dropped.
