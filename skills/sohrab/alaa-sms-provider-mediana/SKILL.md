---
name: alaa-sms-provider-mediana
description: "Use this skill when implementing, reviewing, debugging, documenting, or testing Alaa SMS channel integrations with the Mediana/IPPanel Edge API: environment-configurable endpoints, Authorization authentication, sender/recipient formatting, webservice SMS, pattern/template SMS, SMS OTP, VOTP, peer-to-peer, file/multipart, phonebook/keyword/geolocation/job/postal-code sends, scheduling, cancellation, price calculation, response/error mapping, and provider/channel code. Do not use for Bale, Telegram, email, WhatsApp, push notifications, or generic notification architecture unless Mediana SMS behavior is in scope."
---

# Alaa SMS Provider — Mediana/IPPanel

## Purpose

Use this skill as the Mediana SMS provider contract for Alaa notification work. Mediana uses the IPPanel Edge API: `Authorization` authentication, default base URL `https://edge.ippanel.com/v1`, send endpoint `/api/send`, and a JSON response envelope with `data` and `meta`.

Keep Mediana/SMS behavior separate from Bale Safir, Telegram, email, WhatsApp, push notifications, and generic notification architecture.

## Start sequence

1. Read repo-local `AGENTS.md`, `CLAUDE.md`, or closer agent instructions before editing code.
2. Inspect existing notification, channel, SMS provider, HTTP client, config, queue, retry, OTP, pattern/template, logging, and secret-loading conventions before introducing names.
3. Read `references/mediana-ippanel-api.md` before implementing or reviewing endpoint paths, payload shape, auth, phone formatting, scheduling, response parsing, or errors.
4. Read `references/examples.md` when adding tests, fixtures, docs, curl, Postman, or Insomnia requests.
5. Read `references/vendor-go-sdk-notes.md` and `assets/vendor-sdk.go` only as a vendor example. You may improve the implementation style; do not copy its rough edges blindly.
6. Use `scripts/validate_mediana_payload.py` on JSON payload fixtures when possible. For multipart and GET URL flows, use the validator on the JSON-equivalent metadata and manually check content type and query/form encoding.

## Source authority and freshness

Use this source order:

1. Repository code, production config, fixtures, and account-specific Mediana/IPPanel docs.
2. Current official IPPanel Edge docs, especially `https://github.com/ippanelcom/Edge-Document` and `https://ippanelcom.github.io/Edge-Document/docs/`.
3. The uploaded vendor `sdk.go`, preserved as `assets/vendor-sdk.go`.
4. Clearly labeled assumptions or `NEEDS_MEDIANA_CONFIRMATION` when sources conflict.

Re-check the official docs for version-sensitive work, newly added send modes, pricing/reporting behavior, authentication changes, or any field not covered in this skill.

## Endpoint and configuration rules

- Make every Mediana endpoint environment/config driven. Do not hard-code `https://edge.ippanel.com/v1/api/send` in provider code except as a documented default fallback.
- Prefer existing repo naming. If none exists, use:
  - `MEDIANA_SMS_API_BASE_URL=https://edge.ippanel.com/v1`
  - `MEDIANA_SMS_SEND_URL=https://edge.ippanel.com/v1/api/send`
  - `MEDIANA_SMS_CANCEL_URL=https://edge.ippanel.com/v1/api/send/cancel`
  - `MEDIANA_SMS_PRICE_URL=https://edge.ippanel.com/v1/api/send/calculate-price`
  - `MEDIANA_SMS_URL_SEND_ENDPOINT=https://edge.ippanel.com/v1/api/send/webservice`
  - `MEDIANA_SMS_API_TOKEN=<secret>`
  - `MEDIANA_SMS_FROM_NUMBER=<account-approved sender/originator>`
- If the repo uses base URL plus path, keep both configurable, for example `MEDIANA_SMS_API_BASE_URL` plus `/api/send`; the final request URL must be changeable without code changes.
- Do not commit real tokens, sender numbers, recipient numbers, OTPs, pattern variables, or account-specific IDs.

## Authentication and content type rules

- Include `Authorization: <token-or-api-key>` on every authenticated API request.
- Do not prepend `Bearer` unless current account documentation or existing repo code proves this integration expects it.
- Use `Content-Type: application/json` for JSON APIs.
- Use `multipart/form-data` for file upload send variants: `file`, `keyword`, and `peer_to_peer_file`.
- Use GET query parameters only for the legacy/URL send endpoint `/api/send/webservice`; do not use it as the default provider path when JSON send is available.
- Do not use Bale Safir headers or fields such as `api-access-key`, `bot_id`, `phone_number`, `message_data`, `otp_message`, or `template_message`.

## Phone-number rules

- Mediana/IPPanel examples use E.164 strings with a leading plus sign. Use Alaa Mediana canonical recipient format `+989xxxxxxxxx` for Iranian mobile recipients unless existing production code proves a different account-specific format.
- Normalize user-entered Iranian mobile numbers before building payloads:
  - `09123830000` -> `+989123830000`
  - `989123830000` -> `+989123830000`
  - `+989123830000` -> `+989123830000`
  - Persian/Arabic digits -> ASCII digits before validation
- Reject or normalize away spaces, hyphens, parentheses, zero-width characters, and other display separators.
- Keep sender/originator numbers config-driven. Sender examples include numeric lines such as `+983000505` and account sender labels such as `+98BANK`; do not apply recipient mobile validation to `from_number`.

## Core message variants

### Webservice SMS

Use for normal/custom transactional SMS unless repo truth chooses another type.

```json
{
  "sending_type": "webservice",
  "from_number": "+983000505",
  "message": "متن پیام",
  "params": {
    "recipients": ["+989120000000"]
  }
}
```

Rules:
- `from_number`, `message`, and `params.recipients` are required.
- `send_time` is optional and must be UTC in `YYYY-MM-DD HH:MM:SS`.
- The docs also mention older/alternate `normal` behavior in some contexts; do not use `normal` unless repo truth requires it.

### Pattern/template SMS

Use for approved Mediana/IPPanel patterns. This is the SMS equivalent of a template flow, but the API field is `code`, not `template_id`.

```json
{
  "sending_type": "pattern",
  "from_number": "+983000505",
  "code": "pattern-code",
  "recipients": ["+989120000000"],
  "params": {"code": "458921"}
}
```

Rules:
- The pattern must already exist and be approved in the provider panel.
- `code` is the provider-assigned pattern code.
- `recipients` is top-level and the official send-pattern endpoint allows only one recipient per request.
- `params` keys must exactly match variables defined in the approved pattern.
- Optional `phonebook` can save the recipient to a phonebook when explicitly required; do not add it silently.
- Do not invent variable names. Use repository metadata, panel data, or user-provided examples. If unavailable, use `NEEDS_MEDIANA_PATTERN_CONFIRMATION`.

### SMS OTP

For SMS OTP, prefer an approved `pattern` send unless product requirements explicitly call for free-form `webservice` SMS.

Rules:
- Keep OTP as a string, preferably ASCII digits.
- Never log raw OTPs.
- Pattern variable names come from the approved Mediana pattern, commonly `code` only when the panel pattern uses that placeholder.

### VOTP

Use only when the requested product behavior is voice OTP.

```json
{
  "sending_type": "votp",
  "message": "45852",
  "params": {
    "recipients": ["+989120000000"]
  }
}
```

Rules:
- `message` is the OTP code string.
- Only one recipient is allowed.
- The official example and uploaded Go SDK omit `from_number`; do not add it unless repo/account truth requires it.
- Do not use VOTP when the product requirement is SMS pattern OTP.

## Extended send variants

The latest IPPanel Edge docs list additional send modes. Implement them only when product requirements explicitly need them, and read `references/mediana-ippanel-api.md` first:

- `peer_to_peer`: JSON; multiple message/recipient groups under `params`.
- `peer_to_peer_file`: multipart; file-driven peer-to-peer send with `files[]`.
- `file`: multipart; one message to recipients from CSV/XLSX plus optional `other_recipients`.
- `keyword`: multipart; file-driven dynamic placeholders in message text.
- `keyword_phonebook`: JSON; keyword placeholders from phonebook fields.
- `phonebook`: JSON; send to whole phonebooks or selected phonebook number IDs.
- `postal_code`: JSON; demographic/geographic send by postal-code filters.
- `country`: JSON; geographic send by province/county/city and operator ranges.
- `geolocation`: JSON; newer Country V2 shape with `province_id`, `county_id`, `city_id`, `pre`, `gender`, `from_age`, `to_age`, and `operator`.
- `job`: JSON; send by job category and operator ranges.

Bulk targeting modes such as `postal_code`, `country`, `geolocation`, `job`, `phonebook`, `keyword`, and file-based sends can create large outreach campaigns. Do not implement or trigger live sends for these without explicit product, legal/compliance, and account-owner approval.

## Cancel and price endpoints

- Cancel scheduled message: `POST /api/send/cancel` with `message_outbox_id`. The docs state scheduled messages can only be canceled at least 5 minutes before their scheduled send time.
- Calculate price: `POST /api/send/calculate-price` with `number` and `message`; response includes `mci_price`, `other_price`, and `parts`.
- Make both URLs env/config driven just like the send URL.

## Implementation rules

- Follow the existing repository provider/channel abstraction. If none exists, introduce the smallest provider boundary that can validate, send, parse, log, and test Mediana requests without coupling callers to raw IPPanel payloads.
- Put phone normalization and payload building in deterministic, unit-tested code. Do not let callers manually concatenate `+98` in multiple places.
- Keep OTP codes, API tokens, full phone numbers, message text containing personal data, and pattern variables out of logs. Redact or hash sensitive values in errors and observability.
- Treat provider sends as side-effecting. Do not run live send tests unless the user or repo explicitly authorizes live external calls and provides safe test recipients.
- Make retries bounded. Distinguish transport errors, provider validation errors, authentication errors, and accepted sends.
- If queue retries are used, store enough delivery state to avoid accidental duplicate business sends. The documented Mediana send API does not define an idempotency key like Bale `request_id`.
- For pattern sends, validate required variables when the repo has local pattern metadata. If metadata is unavailable, mark missing certainty as `NEEDS_MEDIANA_PATTERN_CONFIRMATION` instead of guessing.
- For multipart variants, validate file existence, extension, size, and row/header shape before sending. Do not generate outreach files with live user data unless the user explicitly requested that side effect.

## Vendor Go sample rules

The uploaded `sdk.go` is included as `assets/vendor-sdk.go` and summarized in `references/vendor-go-sdk-notes.md`.

Use it as a contract clue for endpoints and JSON shapes, not as production-quality code. You may cleanly reimplement or refactor it to match the target repository.

Prefer these improvements when writing Go or reviewing Go code:

- accept `context.Context` for requests
- use typed request/response structs instead of broad `interface{}` where practical
- parse provider error envelopes instead of returning raw body strings
- avoid `fmt.Printf` inside library code
- make HTTP timeout, send URL/base URL, and retry policy configurable
- redact `Authorization`, recipients, message text, and OTP values in logs
- write tests for request JSON/form/query encoding, URL construction, response parsing, and failure paths

## Response and error handling rules

- Treat non-2xx HTTP responses, timeouts, DNS/TLS failures, and connection failures as transport/provider failures.
- For 2xx responses, parse the JSON envelope and require `meta.status == true` for success.
- Success data for send APIs commonly includes `data.message_outbox_ids`, an array of provider outbox IDs. Preserve them for status tracking and scheduled-message cancellation.
- Preserve `meta.message`, `meta.message_code`, `meta.message_parameters`, and `meta.errors` when present.
- Map invalid/expired token responses to authentication/config failures.
- Map validation responses to payload/building defects unless the provider indicates account-side configuration issues.
- Preserve unknown `message_code` values instead of collapsing them into generic errors.

## Validation

Before finishing Mediana provider work, run the smallest meaningful checks available:

- payload-builder tests for the Mediana variant changed by the task
- phone normalization tests for `0912...`, `+98912...`, `98912...`, Persian digits, spaces, and invalid numbers
- response parsing tests for success, `meta.status=false`, HTTP 401, HTTP 422, HTTP 404 on cancel, malformed JSON, and timeout
- config and secret-loading tests for `MEDIANA_SMS_API_BASE_URL`, `MEDIANA_SMS_SEND_URL`, `MEDIANA_SMS_API_TOKEN`, and `MEDIANA_SMS_FROM_NUMBER` without real secrets
- multipart/query encoding tests when using file, keyword, peer-to-peer file, or URL send
- `scripts/validate_mediana_payload.py` against committed JSON examples or fixtures
- repo-native lint, type checks, and targeted tests

If live integration testing is authorized, use a dedicated test account/sender, safe test recipient, synthetic OTP, and redacted command output.

## When NOT to use

- Do not use for Bale Safir, Telegram, email, WhatsApp, push notifications, or other providers unless the task compares them with Mediana.
- Do not use for generic notification architecture when no Mediana SMS behavior, payload, config, or channel routing is in scope.
- Do not use for IPPanel account management, phonebook management, payments, package purchase, number assignment, or reports unless directly tied to Mediana SMS provider behavior.
- Do not use bulk targeting or file-based sending modes without explicit approval for the campaign and data source.

## Reference navigation

- Complete Mediana/IPPanel send contract, structures, response parsing, scheduling, cancel/price, and source notes: `references/mediana-ippanel-api.md`
- Concrete JSON/curl examples and invalid examples: `references/examples.md`
- Vendor Go SDK sample notes: `references/vendor-go-sdk-notes.md`
- Original uploaded vendor code sample: `assets/vendor-sdk.go`
- JSON fixture validator: `scripts/validate_mediana_payload.py`

## Completion checks

- Endpoint(s) are loaded from config/env and have documented defaults only.
- Mediana payloads use the correct variant shape and content type.
- Recipients are normalized to Alaa Mediana canonical `+989xxxxxxxxx` unless repo truth overrides it.
- `Authorization` is loaded from config/secrets and redacted in logs.
- Pattern code and pattern variable names come from provider/repo truth and are not guessed.
- Response handling preserves `message_outbox_ids`, `meta.status`, `meta.message`, `meta.message_code`, and `meta.errors`.
- Tests or validation cover the Mediana variant changed by the task.
