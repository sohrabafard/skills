# Mediana / IPPanel Edge — failure classes and the ambiguous send

Read this when a Mediana call did not return a clean acceptance: a timeout, a refused connection, a TLS error, a non-2xx status, or a 200 whose body carries `meta.status: false`.

This file classifies **this vendor's** failures and names the smallest safe recovery for each. It states no retry count, no backoff curve, no timeout value and no breaker threshold. Retry legality and the shape of a retry belong to `/alaa-reliability-sla` (`$alaa-reliability-sla`); the Ala numbers belong to `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`.

## The four transport classes

A single "transport error" class is the defect this page exists to prevent. These four outcomes carry different information and must not share a code path.

| Outcome | What it proves | Recovery |
|---|---|---|
| DNS resolution failure, TCP connect refused, connect timeout, TLS handshake failure | The request never reached the vendor | Retry inside the caller's budget. Nothing can be duplicated, so no key is needed |
| Connection reset before the request was fully written | The vendor cannot have processed a request it did not receive | Retry inside the caller's budget |
| Read timeout or total timeout after the request was written | Nothing. The SMS may already be on its way to the subscriber | **Do not re-issue the HTTP call.** Record the attempt as ambiguous and resolve it at the envelope's `idempotency_key` |
| Connection reset after the request was written | Nothing, for the same reason | Same as a read timeout |

`alaa-reliability-sla references/20-retries.md:33` states the doctrine: a refusal is proof of non-execution, a timeout is the absence of information, and code that catches one generic transport exception has already lost the distinction. The observable consequence of losing it is duplicate messages that appear only when the vendor is slow — which is exactly when a subscriber is already waiting for an OTP and will request a second one.

The Mediana send API defines no idempotency key, so this route records `idempotent: false` and every caller sets its HTTP retry budget to `0` (`alaa-services-contract references/22-failure-load-and-deprecation-contract.md:149-151`). Deduplication happens one layer up, at the `idempotency_key` already inside the notification command envelope; adding a second mechanism beside it is forbidden by `22-…:152-153`.

## Symptom to recovery

| Symptom | Diagnosis | Smallest safe recovery | Escalate when |
|---|---|---|---|
| Connection refused or DNS failure on every attempt | The configured host or port is wrong, or egress is blocked | Print the resolved request URL and compare it to the configured base URL and path | The URL is correct and egress is open from the same host |
| The URL resolves but every send 404s | The base URL and the path were joined across the `/v1` versus `/v1/api` boundary, producing `…/v1/api/api/send` | Assert the final URL in a test; see `references/40-vendor-contract-clues.md` | The final URL is correct and still 404s |
| A read timeout on one send, others fine | One request is slow; delivery state is unknown | Mark the delivery ambiguous, do not re-issue, and let the envelope key decide | Ambiguity is not rare, which means the timeout budget is below the vendor's real latency |
| HTTP 401 or a token error in `meta` | The token is missing, wrong, expired, or revoked | Fail the send as a configuration failure and stop retrying | The configured token is the one the panel shows as active |
| 200 with `meta.status: false` and `meta.errors` | The payload is wrong | Read `meta.errors` field by field, fix the builder, add a fixture | `meta.errors` is empty and `message_code` is unrecognised |
| 200 with `meta.status: false` and no `errors` | An account-side condition such as an unapproved sender, an unapproved pattern, or exhausted credit | Check the panel for the sender, the pattern and the balance before touching the code | The panel shows all three healthy |
| A pattern send is accepted but the recipient's text has a gap | A pattern variable was undeclared, missing, or dropped by a duplicate key | Re-run the `pattern_values[] → params{}` rules in `SKILL.md` against the exact command | The mapping is correct and the panel's pattern text differs from what was approved |
| HTTP 404 on cancel | The outbox id is unknown, or the five-minute cancellation window has closed | Stop. Record that the message was sent | The id came from a send response less than five minutes old |
| HTTP 429, or a 5xx carrying a wait hint | The vendor is shedding load | Wait exactly the hint before the next attempt; guessing a shorter wait is the amplification the hint exists to prevent | Shedding persists past the caller's budget |
| A malformed or non-JSON body | An intermediary answered, or a multipart request was sent without `Accept: application/json` | Log the status, the content type and the body length — never the body | The request had the right headers and the body is still not JSON |

## What must never appear in a failure path

- Do not log the response body verbatim on a failure. It echoes recipients and message text, and a failure path is the least reviewed place in the code.
- Do not put a recipient number, an OTP, a token, or a `message_outbox_id` in a metric label or a span name. Recipients and outbox ids are unbounded and will take the metrics backend down before they help anyone.
- Do not raise a Sentry event for an expected vendor rejection. A `meta.status: false` on a bad payload is a validation result; reserve exception reporting for uncaught exceptions and programming faults.
- Do not swallow an unrecognised `message_code`. Store it verbatim on the delivery record, because it is the only token the vendor's support can act on.

## Telemetry

Emit `alaa_dependency_requests_total`, `alaa_dependency_request_duration_seconds`, `alaa_dependency_request_failures_total`, and `alaa_dependency_timeouts_total` for every Mediana call, defined at `alaa-services-contract references/24-metric-registry.md:107-110`. Do not invent a Mediana-specific family; the registry is the only place a metric name is coined.

Label those series with the send mode and the outcome class from the first table, both of which are closed sets. Requirement levels — what must be traced, what must be logged, and at which severity — are `/alaa-observability-soc` (`$alaa-observability-soc`).

## When the failure is on the queue side

A worker that cannot reach Mediana, a job that keeps failing, a dead-letter queue filling with send commands, and the replay of those commands are all `/alaa-async-messaging` (`$alaa-async-messaging`). RabbitMQ is the only broker on this fleet. Do not design an outbox, a retry queue, or a dead-letter topology in provider code, and do not describe one here; the seam already exists and duplicating it produces two mechanisms that disagree about what has been delivered.
