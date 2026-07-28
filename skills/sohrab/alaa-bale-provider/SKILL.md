---
name: alaa-bale-provider
description: "Bale Safir messaging-provider contract for Alaa services: the send_message and upload_file wire shapes, text, OTP, template, media and secure messages, inline url/web_app/copy_text buttons, the upload two-step, api-access-key auth, 989xxxxxxxxx phone normalisation, the request_id idempotency key, Safir error codes, and failure classes. Use when implementing, reviewing, debugging, documenting or testing Bale provider or channel code, and when a Bale send is failing, timing out, rate-limited, returning error_data, duplicating messages, or down. Do not use for Telegram, email, WhatsApp, push, Bale mini-app UI, or generic notification architecture; SMS through Mediana/IPPanel is /alaa-sms-provider-mediana ($alaa-sms-provider-mediana). Do not use for retry, backoff or timeout policy — that is /alaa-reliability-sla ($alaa-reliability-sla); queue, worker and DLQ behaviour is /alaa-async-messaging ($alaa-async-messaging)."
---

# Alaa Bale Provider

## Purpose

The Bale Safir wire contract and failure behaviour for Alaa provider and channel code. Bale ships shortly,
into `auth` or into `notif` once the Go chi kit is finalised, so every rule here is live.

**The command envelope for a Bale send does not exist yet, and this skill does not invent one.** Observed:
`alaa-services-contract references/23-queue-and-exchange-registry.md:183-194` documents `auth`'s direct
Mediana path and names no Bale client; `alaa-services-contract references/27-notification-service-contract.md:86-95`
lists four command families, none for Bale. The notification contract closes that gap; a shape invented
here becomes a second source of truth the day the real one lands.

## Router

| You are about to | Read |
|---|---|
| Build a `send_message` or `upload_file` body, or look up a Safir error code | `references/10-wire-contract.md` |
| Write a test, fixture, curl or Postman request, or check a response shape | `references/20-examples-and-rejects.md` |
| Diagnose a send that failed, timed out, was throttled, or returned `error_data` | `references/30-failure-classes.md` |
| Normalise a number, explain a `code 8` `InvalidPhone`, or change either validator | `references/40-phone-and-conformance.md` |
| Commit a JSON fixture or example payload | `scripts/validate_bale_payload.py` |

## What this skill does not own

- Retry legality, backoff, budgets, idempotency mechanics → `/alaa-reliability-sla` (`$alaa-reliability-sla`)
- Timeout **values**, metric and event **names**, the command envelope → `/alaa-services-contract` (`$alaa-services-contract`)
- Telemetry requirement levels and gates → `/alaa-observability-soc` (`$alaa-observability-soc`)
- Queue, prefetch, ack point, DLQ, outbox behind an async send → `/alaa-async-messaging` (`$alaa-async-messaging`)
- Secret storage, rotation, threat classes → `/alaa-security-review` (`$alaa-security-review`)
- SMS through Mediana/IPPanel → `/alaa-sms-provider-mediana` (`$alaa-sms-provider-mediana`)
- Mini-app UI beyond the `web_app` button payload → `/alaa-frontend-developer` (`$alaa-frontend-developer`)
- Code shape → `/alaa-php-clean-code` (`$alaa-php-clean-code`), `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`)

RabbitMQ is this platform's only broker; do not design an outbox here.

## Wire rules

- Read the host from `BALE_SAFIR_BASE_URL` (default `https://safir.bale.ai`) and the key from
  `BALE_SAFIR_API_ACCESS_KEY`. Endpoints are configurable defaults, because a literal URL in a call site
  cannot be pointed at a sandbox without a code change.
- `POST $BALE_SAFIR_BASE_URL/api/v3/send_message` as `application/json`; `POST .../api/v3/upload_file` as
  `multipart/form-data` in field `file`, letting the client set the boundary.
- Put `api-access-key` on every request, and keep `bot_id` numeric.
- Send `phone_number` as `989` plus nine digits: no `+`, no leading `0`, no separators, no Persian or
  Arabic digits.
- This vendor's wire form is `989xxxxxxxxx` and Mediana's is `+989xxxxxxxxx`, and both render one platform
  input form, so one shared normalisation function serving both channels is a defect unless it takes the
  target channel as a parameter — a number rendered for the wrong channel is rejected by the vendor at best
  and misdelivered at worst.
- Put exactly one primary variant in `message_data`; `is_secure` is a modifier, not a variant. The
  variant-selection table is the first section of `references/10-wire-contract.md`.
- Send only the fields `references/10-wire-contract.md` documents. `chat_id`, `parse_mode`, `callback_data`
  and `disable_notification` are Telegram fields Safir does not define; the validator names each one.

## Idempotency

**`request_id` is the delivery's durable public id, unchanged across every retry of that delivery.**

Never derive it from request content. A key built from recipient, template, or message body cannot
distinguish an honest retry from an intentional repeat, so it suppresses the second real operation: two
legitimate OTPs to one recipient collapse into one and the user cannot log in. Mechanics:
`alaa-reliability-sla references/60-idempotency.md`.

Scope it by **tenant or project, operation identity, and the key, all three together** — a global namespace
is a cross-tenant leak, not a duplicate-suppression bug, because one tenant's key colliding with another's
returns the first tenant's result to the second.

Persist it before the first call, so a retry after a crash finds the same value.

## Secrets

Keep `api-access-key`, OTP values, and full phone numbers out of **logs, traces, exceptions, screenshots,
and final reports** — all five, because a value redacted in logs and printed in a stack trace is not
redacted. Mask a phone number as `98912****000`, and never log an OTP or the key at any level.

## Failure behaviour

**A read timeout on `send_message` is retryable only with an unchanged `request_id`, because Safir may have
delivered.** The request bytes were written, so a timeout is the absence of information rather than
evidence of failure, and a retry carrying a fresh key is a second send — on an OTP path, two codes.

A connect refusal must not share that code path: it proves non-execution, so it is retryable with or
without a key. Code catching one broad transport exception has lost the distinction, and the duplicates
appear only when Safir is slow rather than down. `references/30-failure-classes.md` has all nine classes.

## Observability

Instrument every Safir call with the four `alaa_dependency_*` families named at `/alaa-services-contract`
(`$alaa-services-contract`) `references/24-metric-registry.md:107-110` — `requests_total`,
`request_duration_seconds`, `request_failures_total`, `timeouts_total`. Count a read timeout in the timeout
family, not only the failure family, because the ambiguous outcome is the one an operator must find.

Never label a metric with a phone number, `request_id`, `message_id`, or OTP: the first is PII and all four
are unbounded, so any of them turns a counter into a per-delivery time series.

## Validation

```bash
python3 scripts/validate_bale_payload.py --self-test
python3 scripts/validate_bale_payload.py --mode request|response FILE.json
python3 scripts/validate_bale_payload.py --normalize '0912 383 0000' --channel bale
```

Run `--self-test` before relying on any other run.

| Exit | Obliges |
|---|---|
| `0` | Continue. |
| `1` | Payload or number rejected: fix it. Never edit the validator to make it pass. |
| `2` `3` `4` | Usage error, missing file, invalid JSON: fix the invocation, path, or fixture. |
| `5` | Stop. The script is untrustworthy and every earlier green run with it is void. |
| `6` | Stop. Corpus missing or checksum mismatch; reconcile against the Mediana copy. |

Also required: payload-builder tests per variant in scope, corpus-driven normalisation tests, error-mapping
tests for the documented codes, a test proving a retry reuses the same `request_id`, and one proving
`message_id` with non-empty `error_data` is not success. Layering: `/alaa-testing-strategy`
(`$alaa-testing-strategy`).

Every send is side-effecting. Make a live send only when the user authorises it and names a test bot and a
safe recipient; then use a synthetic OTP, and record the command redacted.

## Provenance

**A vendor fact carrying no read date is re-verified against live Safir documentation before it is relied
on for a production change**, recording the URL and date in the same edit, because an undated fact looks
authoritative and gets copied forward. `references/10-wire-contract.md` marks every table
`unverified as of 2026-07-27`.

## When not to use

- Telegram, SMS, email, WhatsApp, or push, unless it is being compared with Bale.
- Notification architecture with no Bale payload, config, or routing in scope.
