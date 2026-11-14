---
name: alaa-sms-provider-magfa
description: "Magfa HTTP v2 SMS API integration: authentication, request and response formats, uid/mid duplicate handling, delivery status and error codes. Use only when implementing, reviewing, debugging or testing communication with Magfa for SMS delivery. Do not use for general SMS/OTP flows, provider selection or other providers. Use /alaa-async-messaging for queues, outboxes and workers; /alaa-reliability-sla for retry policy; /alaa-sms-provider-mediana for Mediana; and /alaa-bale-provider for Bale."
---

# Alaa SMS Provider — Magfa HTTP v2

## When NOT to use

Use this skill only for communication with the Magfa HTTP v2 SMS API: wire shapes, rendering, duplicate prevention, delivery status and error codes. A mention of SMS or OTP alone does not trigger it. The caller's application owner decides general SMS and OTP flows and provider selection. Route other decisions to their owners:

- Retry legality, backoff, idempotency doctrine and ambiguity doctrine → `/alaa-reliability-sla`
- Timeout and retry-budget values, metric and event names, and the notification envelope → `/alaa-services-contract`
- Queues, workers, the outbox, the DLQ and replay → `/alaa-async-messaging`
- Secret storage and rotation, and threat classes → `/alaa-security-review`
- Mediana or IPPanel → `/alaa-sms-provider-mediana`; Bale Safir → `/alaa-bale-provider`
- Go client shape → `/alaa-golang`; PHP client shape → `/alaa-php-clean-code`; test layering → `/alaa-testing-strategy`

## Role: one driver behind a channel-neutral adapter

A Magfa client is a driver behind the notification service's channel-neutral adapter. The driver only translates: it builds the request, authenticates, parses the response and classifies the error code. Line selection, fallback, retry scheduling, quiet hours and suppression stay in the caller's core. A driver that contains policy is a defect.

A sender line (a `senders` value) belongs to exactly one Magfa account. Configuration selects the line, and the line determines this driver and the account credentials. Never send a line through another account's credentials, because Magfa rejects it with code `20`.

## Provenance

Source: `https://messaging.magfa.com/ui/?public/wiki/api/http_v2`, read 2026-10-20 from the rendered page. Facts marked `NEEDS_MAGFA_CONFIRMATION` are absent from that page. Before a production change relies on a fact, re-verify it against the live page and record the URL and read date in the same edit. Repository code, committed fixtures and account documentation outrank this skill. When they disagree with this skill and you cannot resolve the disagreement, mark the fact `NEEDS_MAGFA_CONFIRMATION` and stop. Do not guess.

## Configuration and authentication

Read every value from configuration. Ship the vendor URL only as a documented default. Use the target repository's existing names when it has them.

```text
MAGFA_SMS_API_BASE_URL=https://sms.magfa.com/api/http/sms/v2
MAGFA_SMS_USERNAME=<username>
MAGFA_SMS_DOMAIN=<domain>
MAGFA_SMS_SERVICE_PASSWORD=<secret>
```

- Send `Authorization: Basic base64("USERNAME/DOMAIN:SERVICE_PASSWORD")` on every call. The panel generates the service password under account management → password and security → service passwords. It is never the panel login password.
- The panel can enable a source-IP allowlist. A call from an unlisted IP fails with code `29`. Register a static egress IP before cutover.
- Use HTTPS only and UTF-8 only. Send `Accept: application/json` on every call. Gzip is optional in both directions (`Content-Encoding: gzip`, `Accept-Encoding: gzip`).

## Endpoints

When you build a request path, read `references/10-endpoints-and-send-fields.md`. It lists the five methods (`send`, `mid`, `statuses`, `messages`, `balance`), their HTTP verbs, paths and per-call limits.

Every response carries a top-level `status`: `0` is success, and any other value is an error code. Parse the body of every response before you decide anything. The transport status alone is not acceptance.

## Send

Send JSON with `Content-Type: application/json`. The vendor also accepts form encoding, but Alaa sends JSON. When you build a `send` body, read `references/10-endpoints-and-send-fields.md` for each field's type and its vendor and Alaa requirement. Always send `uids`, with one client id per message (see Idempotency). Omit `udhs`. Omit `encodings` or send `0`.

- Always send equal-length `senders`, `recipients`, `messages` and `uids` arrays, and repeat the sender and text for each recipient. The vendor also allows a one-to-many shape, but its pairing with `uids` is undocumented. Equal arrays leave nothing to guess. A length mismatch fails with a code from `101` to `110`.
- Split a send above 100 recipients before you send it, because the vendor rejects a larger request.
- Magfa accepts these sender forms: `3000xxxxxx`, `983000xxxxxx`, `+983000xxxxxx`. The sender must belong to the account (`20`) and carry verified end-user information (`34`).
- Magfa accepts these recipient forms: `09xxxxxxxxx`, `989xxxxxxxxx`, `+989xxxxxxxxx`, `9xxxxxxxxx`. Render `989xxxxxxxxx`, because the response echoes recipients in that form. Produce it from the platform's single normaliser, called with the target provider. Mediana renders `+989…` and Bale renders `989…`, so a normaliser without a provider parameter is a defect.
- Text: any non-ASCII character makes the message UCS2. One Farsi part holds 70 characters, or 67 per part when the message is split. One Latin part holds 160 characters, or 153 per part when split. More than 265 parts fails with `30`. An invalid character fails with `35`. Cost is per part.

When you write or test the response parser, read the response example in `references/10-endpoints-and-send-fields.md`. Parse the response by these rules:

- A top-level `0` does not mean that every item was accepted. Evaluate each item. An item with `status: 0` and an `id` is accepted: persist `id` (the `mid`), `parts`, `tariff` and `alphabet`. Classify any other item status by `references/30-error-codes.md`.
- Match items to deliveries by `userId` (your `uid`), never by array position or recipient, because one recipient can appear twice. The vendor example shows `userId` as both a string and a number, so parse both.
- A non-zero top-level `status` with an empty `messages` array rejects the whole request. Classify it by `references/30-error-codes.md`.

## No pattern mode

HTTP v2 has no pattern or template mode as of the read date. OTP and every other message are sent as full text that the caller renders. Never invent a pattern field. If Magfa adds one, verify its fields on the live page, record the URL and date, and add it as a new mode. Which line types may carry OTP traffic is an account and contract fact. Confirm it with the account, not from this skill.

## Idempotency: `uid` and `mid`

**`uid` is the delivery's durable numeric id. Persist it before the first call, and keep it unchanged across every retry of that delivery.** Never derive it from the recipient or the text, because a content-derived key collapses two legitimate OTPs into one and the user cannot log in. It must be unique within the Magfa account. When several services share one account, partition the id space or send only through one service.

| Outcome | What it proves | Action |
|---|---|---|
| DNS failure, connect refused, TLS failure, reset before the request was fully written | Not executed | Retry inside the caller's budget, same `uid` |
| Read timeout or reset after the request was written | Nothing | **Do not re-issue `send`.** Call `GET /mid/{uid}` |
| Item or top-level `15`, `23` | Vendor says resend | Call `GET /mid/{uid}` first, then resend only if not found; for an OTP see the exception below |

**OTP exception for `15` and `23`.** You may resend an OTP with the same code and the same `uid` after a short delay and without the `mid` lookup, because a duplicate copy of the same code is harmless. The lookup path (a settle delay, then a second lookup) usually outlives the code. The caller bounds the resend with three limits:

1. a resend count that fits the attempt budget;
2. a minimum remaining code lifetime;
3. a send-time check that the code is still current.

Every other message keeps the lookup, because a duplicate of other content costs the recipient or the account. This exception never covers a read timeout, for an OTP either.

The `mid` lookup:

- `mid` greater than `0`: the message was accepted. Record the `mid` and stop.
- `mid` equal to `-1`: not found. The vendor presents this lookup as the duplicate guard, so treat `-1` as not sent and resend with the same `uid`. Two facts are `NEEDS_MAGFA_CONFIRMATION`: how soon after a timeout the lookup becomes reliable, and whether Magfa rejects a repeated `uid`. Until both are confirmed, wait the caller's configured settle delay before the lookup, and look up once more before you resend. An OTP `15` or `23` under the OTP exception above skips this lookup.

## Delivery status (pull only)

`GET /statuses/{mid1,mid2,...}` takes at most 100 comma-separated ids and returns `dlrs: [{ mid, status, date }]`. HTTP v2 has no webhook. Status arrives only by polling, and only within 24 hours of sending. When you map a `status` value to a normalized state or decide whether to keep polling, read `references/20-delivery-status.md`.

- Move a delivery's state forward only. A late `8` after `1` changes nothing.
- The timezone of `date` is `NEEDS_MAGFA_CONFIRMATION`. Store the vendor string verbatim beside your own receive time.
- The caller owns the polling cadence and budget.

## Inbound messages and balance

- `GET /messages/{count}` returns at most 100 `{ body, senderNumber, recipientNumber, date }` objects. Whether a read consumes the messages is `NEEDS_MAGFA_CONFIRMATION`, and that fact decides whether two pollers race. Run one poller per account. Treat `body` as untrusted user content and never log it. Use inbound messages only when a product requirement asks for them.
- `GET /balance` returns `balance`. Use it for monitoring and alerts, never as a pre-send gate, because a check followed by a send races.

## Error codes and classes

The driver returns the class and the raw code, and the caller acts on the class. When you classify a code or write the error-mapping tests, read `references/30-error-codes.md`. It maps every documented code to its class.

- **transient**: retry with backoff on the same line with the same `uid`. Do a `mid` lookup first when the outcome may have executed. An OTP `15` or `23` may skip the lookup under the OTP exception.
- **recipient-terminal**: fail this recipient on this line. The caller may try another line or channel.
- **account**: stop using this account or line. Open its breaker and alert an operator. Never retry.
- **caller-defect**: fix the code or configuration. Never retry.
- **window**: not a failure. Defer to the allowed window.

Store an unlisted code verbatim with its recipient, treat it as terminal for that item, and alert. Never retry it, because an unknown code retried as transient turns a caller defect into provider load.

## HTTP 429 and `Retry-After`

HTTP 429 without a readable vendor status means that the gateway throttled the call before Magfa processed it. The outcome is not-sent, the class is transient, and you retry with the same `uid`. That 429 is the only throttle signal, and it is `NEEDS_MAGFA_CONFIRMATION`. Codes `15` and `23` stay transient rejections, not throttles. Read `Retry-After` on a 429 and on no other answer, including a `5xx`. Clamp the hint to the caller's maximum (Ala: `SMS_RETRY_AFTER_MAX_SECONDS`, default 60 s). The caller owns the wait, the account-wide cooldown and the provider fallback: `/alaa-services-contract` `references/33-outbound-messaging-provider-contract.md`.

## Non-negotiables

- Keep the service password, the `Authorization` header, full recipient numbers, message text and OTP values out of logs, traces, exception payloads, screenshots and reports. Mask a recipient as `98912****000`.
- Never put a recipient number, a `uid` or a `mid` in a metric label or a span name. All three are unbounded, and the first is PII.
- Emit the four `alaa_dependency_*` families from `/alaa-services-contract` `references/24-metric-registry.md` on every Magfa call, labelled only by method and outcome class. Invent no Magfa-specific family.
- Give every call an explicit timeout and retry budget from `/alaa-services-contract` `references/22-failure-load-and-deprecation-contract.md`.
- Report only unexpected faults to Sentry. A classified vendor rejection is a result, not an exception.
- Run a live send only against a test account and line, to a recipient the user named in this session, because an accepted SMS cannot be recalled.

## Required tests

- Request builder: equal-length arrays, the split at 100, the JSON shape, and the exact Basic header value.
- Normaliser corpus: `09…`, `+989…`, `9…` and Persian or Arabic digits render `989…`, and invalid input is rejected.
- Response parsing: mixed accepted and rejected items, `userId` as a string and as a number, and a non-zero top-level `status` with an empty `messages` array.
- Error mapping: every code in `references/30-error-codes.md` maps to its class, and an unlisted code is terminal.
- Ambiguity: a read timeout never re-issues `send`; `mid > 0` records acceptance; `mid = -1` resends with the same `uid`.
- Resend requests: a non-OTP `15` or `23` is looked up before any resend. An OTP `15` or `23` is resent with the same code and `uid` only inside the caller's resend-count and remaining-lifetime bounds.
- `uid` is derived from the delivery id, never from content, and is identical across retries.
- Status mapping for every row of `references/20-delivery-status.md`, including `0` and `-1`, and batching at 100 ids.
- Redaction: no password, number, text or OTP reaches a log, a trace attribute, an exception payload or a report.

## Stop

The work is done when the driver passes the tests above against fixtures, and every fact it relies on is either on the provenance page or confirmed. When a change depends on a `NEEDS_MAGFA_CONFIRMATION` fact, stop and report the fact and the decision it blocks.
