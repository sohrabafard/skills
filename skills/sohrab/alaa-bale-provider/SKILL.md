---
name: alaa-bale-provider
description: "Use this skill when implementing, reviewing, debugging, documenting, or testing integrations with Bale Safir channel/message APIs: normal text messages, OTP messages, template messages, secure messages, inline buttons, file uploads, phone-number normalization, idempotency request_id, api-access-key auth, error handling, or provider/channel code for the Bale messaging app. Do not use for unrelated Telegram, SMS, email, or generic notification work unless Bale Safir behavior is involved."
---

# Alaa Bale Provider

## Purpose

Use this skill as the exact Bale Safir API contract for Alaa message-provider work. Keep Bale behavior separate from
generic notification architecture and from other providers such as SMS, Telegram, WhatsApp, or email.

## Start sequence

1. Read repo-local `AGENTS.md`, `CLAUDE.md`, or closer agent instructions before editing code.
2. Inspect existing notification, channel, provider, HTTP-client, config, queue, retry, and template conventions before
   introducing new names.
3. Read `references/bale-safir-api.md` before implementing or reviewing payload shape, phone formatting, file upload,
   errors, idempotency, or message variants.
4. Read `references/examples.md` when adding tests, fixtures, docs, Postman requests, or concrete curl examples.
5. Use `scripts/validate_bale_payload.py` on generated JSON fixtures or example payloads when possible.

## Hard API rules

- Send messages with `POST https://safir.bale.ai/api/v3/send_message` and JSON body.
- Upload files with `POST https://safir.bale.ai/api/v3/upload_file` and multipart form-data field `file`.
- Include the `api-access-key` header on every Safir request. Never hard-code or commit the key.
- Include `Content-Type: application/json` for `send_message`; let the HTTP client set multipart boundaries for
  `upload_file`.
- Keep `bot_id` numeric in the request body.
- Send `phone_number` as Alaa-canonical digits only: `98` plus the ten-digit Iranian mobile number, with no leading `0`,
  no `+`, no spaces, no hyphens, and no Persian or Arabic digits.
- Normalize user-entered numbers before building the payload. For example, `09123830000` must be sent as `989123830000`.
- Prefer `request_id` for every non-test send. Reuse the same `request_id` for retries of the same intended delivery; do
  not reuse it for different recipients or different messages.
- Put exactly one primary message variant in `message_data`: `message`, `otp_message`, or `template_message`.
  `is_secure` is an optional modifier, not a primary message variant.
- Do not invent unsupported fields such as `chat_id`, `parse_mode`, `callback_data`, `disable_notification`, or
  Telegram-style button callbacks unless current Bale docs or repo truth prove them.

## Message variant rules

### Normal text message

Use `message_data.message.text`.

```json
{
  "bot_id": 1,
  "phone_number": "989100000000",
  "message_data": {
    "message": {
      "text": "متن"
    }
  }
}
```

### OTP message

Use `message_data.otp_message.otp`. The OTP must be a numeric string. Do not wrap it in a normal text message and do not
add custom copy-button markup unless Bale docs or repo truth require a custom fallback.

```json
{
  "bot_id": 2040665828,
  "phone_number": "989100900000",
  "message_data": {
    "otp_message": {
      "otp": "123456"
    }
  }
}
```

### Template message

Use `message_data.template_message.template_id` plus `text_fields`. The template must already exist in Bale Business
Panel and the keys in `text_fields` must exactly match the variables defined for that template.

```json
{
  "bot_id": 1,
  "phone_number": "989100000000",
  "message_data": {
    "template_message": {
      "template_id": "t1",
      "text_fields": {
        "user": "test",
        "course": "test",
        "content_title": "test",
        "content_link": "test",
        "ticket_url": "test"
      }
    }
  }
}
```

### Media message

Upload the file first, then send `message_data.message.file_id`. Add `message_data.message.text` only when a caption is
intended.

### Inline buttons

Use `message.reply_markup.inline_keyboard` as an array of rows. Each button must include `text` and at least one action
from `url`, `web_app`, or `copy_text`; prefer exactly one action per button to avoid ambiguity. Bale Safir docs do not
define callback buttons.

### Secure message

Set `message_data.is_secure` to `true` only for message or template sends that should be protected. Do not apply it to
OTP unless current Bale docs or repo truth explicitly support that combination.

## Implementation rules

- Follow the existing repository provider/channel abstraction. If there is no existing abstraction, introduce the
  smallest provider boundary that can send, validate, log, and test Bale requests without coupling callers to raw Safir
  payloads.
- Keep provider config environment-driven. Prefer existing config naming conventions; when no convention exists, propose
  names such as `BALE_SAFIR_BASE_URL`, `BALE_SAFIR_API_ACCESS_KEY`, and `BALE_SAFIR_BOT_ID` and document them in the
  repo.
- Put phone normalization and payload building in deterministic, unit-tested code. Do not let callers manually
  concatenate `98` in multiple places.
- Keep OTP values, API keys, full phone numbers, and template personal data out of logs. Redact or hash sensitive values
  in errors and observability.
- Treat provider sends as side-effecting. Do not run live send tests unless the user or repo explicitly authorizes live
  external calls and provides safe test recipients.
- For queues or retries, make `request_id` stable across retry attempts and store enough state to distinguish transport
  retry from a new business send.
- For template messages, validate that required template field names are present when the repo has local template
  metadata. If metadata is unavailable, mark missing certainty as `NEEDS_BALE_TEMPLATE_CONFIRMATION` instead of
  inventing fields.

## Error handling rules

- Treat non-2xx HTTP responses, timeouts, and connection failures as transport/provider failures.
- When a Safir JSON response contains `error_data`, map each `ErrorInfo` item by `phone_number`, `code`, and
  `description`.
- Treat `message_id` with empty or null `error_data` as the success path.
- Preserve unknown Bale error codes as provider errors with raw code and description; do not collapse them into generic
  failure if the exact code is useful.
- Use the documented code map from `references/bale-safir-api.md` for known codes.

## Validation

Before finishing Bale provider work, run the smallest meaningful checks available:

- payload-builder unit tests for text, OTP, template, secure, file, and inline-button payloads
- phone normalization tests for `0912...`, `+98912...`, `98912...`, Persian digits, spaces, and invalid numbers
- error mapping tests for documented Safir error codes
- idempotency tests proving retry keeps the same `request_id`
- config and secret-loading tests without real secrets
- `scripts/validate_bale_payload.py` against committed JSON examples or fixtures
- repo-native lint, type checks, and targeted tests

If live integration testing is authorized, use a dedicated test bot, safe test phone number, synthetic OTP, and a unique
`request_id`. Record the exact command and redact secrets.

## When NOT to use

- Do not use for Telegram Bot API, SMS, email, WhatsApp, or other providers unless the task compares them with Bale.
- Do not use for generic notification architecture when no Bale Safir behavior, payload, config, or channel routing is
  in scope.
- Do not use to design Bale mini-app UI except for the `web_app` button payload needed in Safir messages.

## Reference navigation

- Complete Safir contract, structures, error codes, upload rules, and idempotency: `references/bale-safir-api.md`
- User-provided and common curl/JSON examples: `references/examples.md`
- JSON fixture validator: `scripts/validate_bale_payload.py`

## Completion checks

- Bale payloads use canonical `98` phone numbers and no extra phone characters.
- `api-access-key` is loaded from config/secrets and redacted in logs.
- `request_id` behavior is stable for retries where idempotency matters.
- Message variant selection is explicit and tests cover the variants in scope.
- Template field names are exact and not guessed.
- Error handling preserves `message_id`, `error_data`, code, description, and recipient context.
