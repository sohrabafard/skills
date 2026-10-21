---
name: alaa-sms-provider-magfa
description: "Magfa SMS provider contract (HTTP v2, REST/JSON) for Alaa services: wire shapes, sender and recipient rendering, uid-based duplicate prevention, delivery-status polling, and error-code classes. Use when implementing, reviewing, debugging or testing a Magfa SMS driver or adapter — Basic auth with USERNAME/DOMAIN, send with parallel senders/recipients/messages arrays, the 100-recipient cap, uids and the mid lookup after a timeout, statuses polling, inbound messages, balance, encodings and segments, per-item result parsing, and Magfa error codes. Do not use for Mediana/IPPanel (alaa-sms-provider-mediana) or Bale Safir (alaa-bale-provider); not for queue, outbox or consumer design (alaa-async-messaging); not for retry legality or backoff values (alaa-reliability-sla)."
---

# Alaa SMS Provider — Magfa HTTP v2

## Scope and owners

This skill owns one vendor: the Magfa HTTP v2 API — its wire shapes, rendering, idempotency mechanism, status model and error codes. Route everything else:

- Retry legality, backoff, idempotency doctrine, ambiguity doctrine → `/alaa-reliability-sla`
- Timeout and retry-budget values, metric and event names, the notification envelope → `/alaa-services-contract`
- Queues, workers, outbox, DLQ, replay → `/alaa-async-messaging`
- Secret storage and rotation, threat classes → `/alaa-security-review`
- Mediana/IPPanel → `/alaa-sms-provider-mediana`; Bale Safir → `/alaa-bale-provider`
- Go or PHP client shape → `/alaa-golang`, `/alaa-php-clean-code`; test layering → `/alaa-testing-strategy`

## Role: one driver behind a channel-neutral adapter

A Magfa client is a driver behind the notification service's channel-neutral adapter. The driver translates only: request building, authentication, response parsing, and error-code classification. Line selection, fallback, retry scheduling, quiet hours and suppression stay in the caller's core; a driver containing policy is a defect.

A sender line (a `senders` value) belongs to exactly one Magfa account. Configuration selects the line; the line determines this driver and the account credentials. Never send a line through another account's credentials — Magfa rejects it with code `20`.

## Provenance

Source: `https://messaging.magfa.com/ui/?public/wiki/api/http_v2`, read 2026-10-20 from the rendered page. Facts marked `NEEDS_MAGFA_CONFIRMATION` are absent from that page. Before a production change relies on a fact, re-verify it against the live page and record the URL and read date in the same edit. Repository code, committed fixtures and account documentation outrank this file; when they disagree and you cannot resolve it, mark `NEEDS_MAGFA_CONFIRMATION` and stop rather than guess.

## Configuration and authentication

Read every value from configuration; ship the vendor URL only as a documented default. Use the target repository's existing names when it has them.

```text
MAGFA_SMS_API_BASE_URL=https://sms.magfa.com/api/http/sms/v2
MAGFA_SMS_USERNAME=<username>
MAGFA_SMS_DOMAIN=<domain>
MAGFA_SMS_SERVICE_PASSWORD=<secret>
```

- Send `Authorization: Basic base64("USERNAME/DOMAIN:SERVICE_PASSWORD")` on every call. The service password is generated in the panel under account management → password and security → service passwords; it is never the panel login password.
- The panel can enable a source-IP allowlist; an unlisted IP fails with code `29`. Register a static egress IP before cutover.
- HTTPS only, UTF-8 only, `Accept: application/json` on every call. Gzip is optional both ways (`Content-Encoding: gzip`, `Accept-Encoding: gzip`).

## Endpoints

| Method | HTTP | Path | Purpose |
|---|---|---|---|
| `send` | POST | `/send` | send to at most 100 recipients |
| `mid` | GET | `/mid/{uid}` | provider message id for a client `uid` |
| `statuses` | GET | `/statuses/{mid1,mid2,...}` | final status, at most 100 ids |
| `messages` | GET | `/messages` or `/messages/{count}` | inbound messages, at most 100 |
| `balance` | GET | `/balance` | remaining credit |

Every response carries a top-level `status`: `0` is success, anything else is an error code. Parse the body on every response before deciding anything; the transport status alone is not acceptance.

## Send

Send JSON with `Content-Type: application/json` (the vendor also accepts form encoding; Alaa sends JSON).

| Field | Type | Vendor | Alaa | Notes |
|---|---|---|---|---|
| `senders` | string[] | required | required | sender lines |
| `recipients` | string[] | required | required | at most 100 |
| `messages` | string[] | required | required | full UTF-8 text |
| `uids` | long[] | optional | **required** | one client id per message; see Idempotency |
| `encodings` | int[] | optional | omit or `0` | `0` auto (default), `2` Farsi, `5` 8-bit, `6` binary |
| `udhs` | string[] | optional | omit | Alaa sends no UDH |

- Always send equal-length `senders`, `recipients`, `messages` and `uids` arrays, repeating the sender and text per recipient. The vendor also allows a one-to-many shape, but its pairing with `uids` is undocumented, and equal arrays leave nothing to guess. Length mismatches fail with `101`–`110`.
- Split above 100 recipients before sending; the vendor rejects larger requests.
- Sender forms accepted: `3000xxxxxx`, `983000xxxxxx`, `+983000xxxxxx`. The sender must belong to the account (`20`) and carry verified end-user information (`34`).
- Recipient forms accepted: `09xxxxxxxxx`, `989xxxxxxxxx`, `+989xxxxxxxxx`, `9xxxxxxxxx`. Render `989xxxxxxxxx`, because the response echoes recipients in that form. Produce it from the platform's single normaliser called with the target provider: Mediana renders `+989…`, Bale `989…`, so a normaliser without a provider parameter is a defect.
- Text: any non-ASCII character makes the message UCS2. One Farsi part holds 70 characters, 67 per part when split; Latin 160 and 153. More than 265 parts fails with `30`; an invalid character fails with `35`. Cost is per part.

Response:

```json
{
  "status": 0,
  "messages": [
    { "status": 13, "userId": "1223", "recipient": "98912xxxxxxx" },
    { "status": 0, "id": 111111111, "userId": 1224, "parts": 3, "tariff": 160.00, "alphabet": "UCS2", "recipient": "98913xxxxxxx" }
  ]
}
```

- A top-level `0` does not mean every item was accepted. Evaluate each item: `status: 0` with an `id` is accepted — persist `id` (the `mid`), `parts`, `tariff` and `alphabet`; any other item status is classified by the error table.
- Match items to deliveries by `userId` (your `uid`), never by array position or recipient, because one recipient can appear twice. The vendor example shows `userId` as both string and number; parse both.
- A non-zero top-level `status` with an empty `messages` array rejects the whole request; classify it by the error table.

## No pattern mode

HTTP v2 has no pattern or template mode as of the read date. OTP and every other message are sent as full text rendered by the caller. Never invent a pattern field. If Magfa adds one, verify its fields on the live page, record the URL and date, and add it as a new mode. Which line types may carry OTP traffic is an account and contract fact; confirm it with the account, not from this skill.

## Idempotency: `uid` and `mid`

**`uid` is the delivery's durable numeric id: persisted before the first call and unchanged across every retry of that delivery.** Never derive it from recipient or text, because a content-derived key collapses two legitimate OTPs into one and the user cannot log in. It must be unique within the Magfa account; when several services share one account, partition the id space or send only through one service.

| Outcome | What it proves | Action |
|---|---|---|
| DNS failure, connect refused, TLS failure, reset before the request was fully written | Not executed | Retry inside the caller's budget, same `uid` |
| Read timeout or reset after the request was written | Nothing | **Do not re-issue `send`.** Call `GET /mid/{uid}` |
| Item or top-level `15`, `23` | Vendor says resend | Call `GET /mid/{uid}` first, then resend only if not found; for an OTP see the exception below |

**OTP exception for `15` and `23`.** An OTP may be resent with the same code and the same `uid` after a short delay and without the `mid` lookup, because a duplicate copy of the same code is harmless, while the lookup path (settle delay, then a second lookup) usually outlives the code. The caller bounds it: a resend count that fits the attempt budget, a minimum remaining code lifetime, and a send-time check that the code is still current. Every other message keeps the lookup, because a duplicate of other content costs the recipient or the account. A read timeout is never covered by this exception, for an OTP either.

The `mid` lookup:

- `mid` greater than `0`: the message was accepted. Record the `mid` and stop.
- `mid` equal to `-1`: not found. The vendor presents this lookup as the duplicate guard, so treat `-1` as not sent and resend with the same `uid`. How soon after a timeout the lookup becomes reliable, and whether Magfa rejects a repeated `uid`, are `NEEDS_MAGFA_CONFIRMATION`; until confirmed, wait the caller's configured settle delay before the lookup and look up once more before resending. An OTP `15` or `23` under the OTP exception above skips this lookup.

## Delivery status (pull only)

`GET /statuses/{mid1,mid2,...}` with at most 100 comma-separated ids returns `dlrs: [{ mid, status, date }]`. HTTP v2 has no webhook; status arrives only by polling, and only within 24 hours of sending.

| Magfa `status` | Meaning | Normalized | Polling |
|---|---|---|---|
| `1` | delivered to handset | `delivered` | stop |
| `2` | not delivered to handset | `failed` | stop |
| `16` | not delivered to operator | `failed` | stop |
| `8` | delivered to operator | `sent` | continue; may become `1` or `2` |
| `0` | no status yet | `pending` | continue |
| `-1` | unknown id, or more than 24 hours since send | `expired` | stop |

- Move a delivery's state forward only; a late `8` after `1` changes nothing.
- The `date` timezone is `NEEDS_MAGFA_CONFIRMATION`; store the vendor string verbatim beside your own receive time.
- Polling cadence and budget belong to the caller.

## Inbound messages and balance

- `GET /messages/{count}` returns at most 100 `{ body, senderNumber, recipientNumber, date }`. Whether a read consumes the messages, and therefore whether two pollers race, is `NEEDS_MAGFA_CONFIRMATION`; run one poller per account. Treat `body` as untrusted user content and never log it. Use inbound only when a product requirement asks for it.
- `GET /balance` returns `balance`. Use it for monitoring and alerts, never as a pre-send gate, because a check-then-send races.

## Error codes and classes

The caller acts on the class; the driver returns the class and the raw code.

- **transient** — retry with backoff on the same line, same `uid`, after a `mid` lookup when the outcome may have executed; an OTP `15` or `23` may skip the lookup under the OTP exception.
- **recipient-terminal** — fail this recipient on this line; the caller may try another line or channel.
- **account** — stop using this account or line: open its breaker and alert an operator; never retry.
- **caller-defect** — fix the code or configuration; never retry.
- **window** — not a failure; defer to the allowed window.

| Code | Meaning | Class |
|---|---|---|
| `1` | invalid recipient | recipient-terminal; repeated occurrences indicate a normaliser defect |
| `2` | invalid sender | caller-defect |
| `3` | invalid encoding for the text | caller-defect |
| `4` | invalid mclass | caller-defect |
| `6` | invalid UDH | caller-defect |
| `8` | promotional send outside 07:00–22:00 | window |
| `13` | empty content | caller-defect |
| `14` | insufficient credit | account |
| `15` | internal server error, resend | transient; OTP: same-code resend without lookup allowed |
| `16` | account inactive | account |
| `17` | account expired | account |
| `18` | invalid username or password | account |
| `19` | invalid username, password and domain combination | account |
| `20` | sender not owned by the account | caller-defect (line-to-account mapping) |
| `22` | service not enabled for the account | account |
| `23` | cannot process now, resend | transient; OTP: same-code resend without lookup allowed |
| `24` | invalid message id, or older than one day | caller-defect on `mid`/`statuses`; `expired` when older than one day |
| `25` | invalid method name | caller-defect |
| `27` | recipient on operator blacklist (promotional) | recipient-terminal |
| `28` | recipient prefix blocked at Magfa | recipient-terminal |
| `29` | source IP not allowed | account (egress IP) |
| `30` | more than 265 parts | caller-defect |
| `31` | invalid JSON | caller-defect |
| `33` | subscriber blocked this sender (opt-out, «لغو ۱۱») | recipient-terminal; record an opt-out suppression for this line |
| `34` | no verified information for this sender number | account |
| `35` | invalid character in text | caller-defect |
| `101`–`110` | array length mismatch, empty arrays, too many recipients | caller-defect |

An unlisted code is stored verbatim with its recipient, treated as terminal for that item, and alerted; never retry it, because an unknown code retried as transient turns a caller defect into provider load.

## HTTP 429 and `Retry-After`

HTTP 429 without a readable vendor status means the gateway throttled the call before Magfa processed it: outcome not-sent, class transient, retry with the same `uid`. That 429 is the only throttle signal and is `NEEDS_MAGFA_CONFIRMATION`; codes `15` and `23` stay transient rejections, not throttles. Read `Retry-After` on a 429 and on no other answer, a `5xx` included, and clamp the hint to the caller's maximum (Ala: `SMS_RETRY_AFTER_MAX_SECONDS`, default 60 s). The wait, the account-wide cooldown and the provider fallback belong to the caller: `/alaa-services-contract` `references/33-outbound-messaging-provider-contract.md`.

## Non-negotiables

- Keep the service password, the `Authorization` header, full recipient numbers, message text and OTP values out of logs, traces, exception payloads, screenshots and reports. Mask a recipient as `98912****000`.
- Never put a recipient number, `uid` or `mid` in a metric label or span name; all are unbounded and the first is PII.
- Emit the four `alaa_dependency_*` families from `/alaa-services-contract` `references/24-metric-registry.md` on every Magfa call, labelled only by method and outcome class. Invent no Magfa-specific family.
- Give every call an explicit timeout and retry budget from `/alaa-services-contract` `references/22-failure-load-and-deprecation-contract.md`.
- Report only unexpected faults to Sentry; a classified vendor rejection is a result, not an exception.
- Run a live send only against a test account and line, to a recipient the user named in this session, because an accepted SMS cannot be recalled.

## Required tests

- Request builder: equal-length arrays, split at 100, JSON shape, exact Basic header value.
- Normaliser corpus: `09…`, `+989…`, `9…` and Persian or Arabic digits render `989…`; invalid input is rejected.
- Response parsing: mixed accepted and rejected items, `userId` as string and number, non-zero top-level `status` with empty `messages`.
- Error mapping: every listed code maps to its class; an unlisted code is terminal.
- Ambiguity: a read timeout never re-issues `send`; `mid > 0` records acceptance; `mid = -1` resends with the same `uid`.
- Resend requests: a non-OTP `15` or `23` is looked up before any resend; an OTP `15` or `23` is resent with the same code and `uid` only inside the caller's resend count and remaining-lifetime bounds.
- `uid` is derived from the delivery id, never from content, and is identical across retries.
- Status mapping for every row, including `0` and `-1`, and batching at 100 ids.
- Redaction: no password, number, text or OTP reaches a log, trace attribute, exception payload or report.

## Stop

Done when the driver passes the tests above against fixtures and every fact it relies on is either on the provenance page or confirmed. When a change depends on a `NEEDS_MAGFA_CONFIRMATION` fact, stop and report the fact and the decision it blocks.
