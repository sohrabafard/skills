# Bale Safir wire contract

Read this before building, changing, or reviewing a Safir request or response shape.

## Choosing a variant

| You want | Send |
|---|---|
| Plain text, or a media caption | `message_data.message.text` |
| A one-time code | `message_data.otp_message.otp`, ASCII digits, no surrounding text |
| A pre-approved template | `message_data.template_message`, with the panel's exact variable names |
| A file, captioned or not | `upload_file`, persist `file_id`, then `message.file_id` |
| Buttons under a message | `message.reply_markup.inline_keyboard` |
| A protected message | `message_data.is_secure: true`, on `message` or `template_message` only |

Exactly one primary variant per `message_data`. Field-level detail for each row is below.

## Provenance and freshness

Every table below carries a provenance line. The convention is
`[source: <url or "not recorded">; read: <YYYY-MM-DD or "unverified as of YYYY-MM-DD">]`.

Every fact below was re-read on 2026-10-20 against the official Safir documentation,
https://docs.bale.ai/safir. The page shows no revision date, only "© بله ۱۴۰۴". The API host is not a
documentation source: `GET` on https://safir.bale.ai and its `/docs`, `/swagger` and `/openapi.json` paths
returned HTTP 404 on 2026-10-20.

Where this skill is stricter than Safir, the text says so: that rule is an Alaa safety rule, not a vendor
fact. What Safir does not document is listed under "Not documented".

The freshness rule that governs these lines is in `SKILL.md` under "Provenance". Record the URL and the
read date together when re-verifying, because a fact re-verified without a recorded date is unverified
again on the next read.

## Endpoints

| Purpose | Method | Default URL | Content type |
|---|---|---|---|
| Send a message | `POST` | `$BALE_SAFIR_BASE_URL/api/v3/send_message` | `application/json` |
| Upload a file | `POST` | `$BALE_SAFIR_BASE_URL/api/v3/upload_file` | `multipart/form-data`, field `file` |

Both requests carry the `api-access-key` header. Documented maximum upload size is 500 MB.

`[source: https://docs.bale.ai/safir; read: 2026-10-20]`

## Request envelope

| Field | Type | Required | Notes |
|---|---|---|---|
| `api-access-key` header | string | yes | Issued after you create a "Safir" in the Bale business panel. |
| `request_id` body | string | yes for every production send | Idempotency key. See the body of this skill, which owns the derivation rule. |
| `bot_id` body | integer | yes | Numeric id of your registered bot; Safir shows its name to the recipient. Numeric, never a string. |
| `phone_number` body | string | yes | `989xxxxxxxxx`. See `40-phone-and-conformance.md`. |
| `message_data` body | object | yes | Exactly one primary variant, plus the optional `is_secure` modifier. |

Safir's own documentation marks `request_id` optional but recommends always sending it, and states that a
repeated `request_id` is not sent again. It does not state the deduplication window, its scope, or the
response to a duplicate; see "Not documented". This skill requires it for production sends, and the
reason is in the body under "Idempotency". A vendor-optional field that this platform requires is recorded
in both places on purpose: the vendor column states what Safir accepts, the body states what Alaa sends.

`[source: https://docs.bale.ai/safir; read: 2026-10-20]`

## MessageData

| Field | Type | Required | Notes |
|---|---|---|---|
| `message` | `Message` | no | Text, media, copy affordance, or inline buttons. |
| `otp_message` | `OTPMessage` | no | OTP presentation. |
| `template_message` | `TemplateMessage` | no | Pre-approved template addressed by id. |
| `is_secure` | boolean | no | Password-protected message. Secure-message modifier, not a primary variant. |

Safir's own `MessageData` table lists `message`, `otp_message` and `is_secure`; `template_message` appears
in its examples but not in that table.

Exactly one of `message`, `otp_message`, or `template_message` is present. This is an Alaa safety rule;
Safir states no such limit. Two primary variants in one `message_data` is rejected by
`scripts/validate_bale_payload.py`, because the vendor documentation does not state which one wins and an
agent that guesses ships a message nobody reviewed.

`[source: https://docs.bale.ai/safir; read: 2026-10-20]`

## Message

| Field | Type | Required | Notes |
|---|---|---|---|
| `text` | string | no | Message body, or the caption of a media message. |
| `file_id` | string | no | Value returned by `upload_file`. |
| `copy_text` | string | no | Adds a copy affordance for the given value. |
| `reply_markup` | `ReplyMarkup` | no | Inline keyboard attached to the message. |

Safir marks all four fields optional. As an Alaa rule, a `Message` carries at least one of `text`,
`file_id`, or `copy_text`; a `Message` with only `reply_markup` has no visible content.

`[source: https://docs.bale.ai/safir; read: 2026-10-20]`

## ReplyMarkup and InlineKeyboardButton

| Field | Type | Required | Notes |
|---|---|---|---|
| `reply_markup.inline_keyboard` | array of arrays of `InlineKeyboardButton` | yes | Outer array is rows; each inner array is one row. |

| Button field | Type | Required | Notes |
|---|---|---|---|
| `text` | string | yes | Display label. |
| `url` | string | no | Opens a URL. |
| `web_app` | `WebAppInfo` | no | Opens a Bale mini-app. `WebAppInfo` carries one required field, `url`. |
| `copy_text` | string | no | Copies the given text. |

Safir requires at least one of `url`, `web_app`, or `copy_text` and does not say whether a button may
carry more than one. As an Alaa rule, each button carries exactly one; the validator warns on more. Safir
documents no callback buttons, so a button carrying `callback_data` is a Telegram payload that reached the
wrong provider.

`[source: https://docs.bale.ai/safir; read: 2026-10-20]`

## OTPMessage

| Field | Type | Required | Notes |
|---|---|---|---|
| `otp` | string | yes | Safir supports numeric codes only, "for now". Alaa rule: ASCII digits only. |

Safir delivers the OTP through its official `@verification_code_bot` in a fixed format: the code, a security
warning, the sender bot's name, and a copy button. No customisation is documented. Send `otp_message` with
no surrounding text: wrapping an OTP in a normal text message loses that rendering and the user sees a
plain message where they expected the OTP card.

Safir states no character set or length. ASCII digits matching `^[0-9]{4,8}$` is this skill's safety rule,
not a vendor fact. Persian-Indic (`U+06F0`-`U+06F9`), Arabic-Indic (`U+0660`-`U+0669`) and superscript
digits are not ASCII digits, and a language-level "is this a digit" check accepts all three — Python's
`str.isdigit()` returns `True` for every one of them. Match `^[0-9]{4,8}$` explicitly instead.

`[source: https://docs.bale.ai/safir; read: 2026-10-20]`

## TemplateMessage

Templates are created in Bale Business Panel, approved by Bale support, then addressed by id. Template
messages are a separately priced category.

| Field | Type | Required | Notes |
|---|---|---|---|
| `template_id` | string | yes | Id Bale assigned to the approved template. |
| `text_fields` | object | yes | Template variable name to string value. Keys match the template's variable names exactly, or the request fails. |

Take field names from repository metadata, Bale panel data, or a user-provided example. Where none of the
three is available, stop and report `NEEDS_BALE_TEMPLATE_CONFIRMATION` naming the template id, because
Safir fails a request whose keys do not match the template's variable names exactly.

Preserve the exact spelling and case of each variable.

`[source: https://docs.bale.ai/safir; read: 2026-10-20]`

## The secure-message modifier

`message_data.is_secure: true` marks a secure normal message or a secure template message. Safir describes
it as a password-protected message.

The vendor documentation shows secure text, secure media and secure template. It shows no secure OTP.
Its `is_secure` description says the flag applies regardless of message type, but no example combines it
with `otp_message`, so the combination stays unverified. Send `otp_message` without `is_secure`. To enable
secure OTP, verify the combination against live Safir documentation first and record the URL and read date
in this file; `scripts/validate_bale_payload.py` rejects the combination until that happens, so the check
and the document cannot drift apart silently.

`[source: https://docs.bale.ai/safir; read: 2026-10-20]`

## The upload two-step

A media message is two requests, and they fail independently.

1. `POST $BALE_SAFIR_BASE_URL/api/v3/upload_file` with the file in the `file` form field. The success
   response is `{"file_id": "..."}`.
2. `POST $BALE_SAFIR_BASE_URL/api/v3/send_message` with `message_data.message.file_id` set to that value.
   Add `message_data.message.text` only when a caption is wanted.

Persist `file_id` before step 2. A retry of step 2 reuses the stored `file_id` and does not re-upload:
re-uploading consumes bandwidth and quota for a file Safir already holds, and it produces a second
`file_id` that no row points at. `30-failure-classes.md` covers the case where step 1 succeeded and step 2
did not.

`[source: https://docs.bale.ai/safir; read: 2026-10-20]`

## Responses

`send_message` success carries a `message_id` string; treat it as opaque. Two shapes are documented and
both occur:

```json
{ "message_id": "523e6875-7c41-491b-8460-04b33039d7fc", "error_data": null }
```

```json
{ "message_id": "BvQjaR.fIKt7kH.EXTddgYduJ2" }
```

`error_data` is an array of `ErrorInfo`, or null on success. The OTP example omits the key; treat a missing
key as null.

Treat `message_id` present with `error_data` absent, null, or empty as success. Treat `message_id` present
with a non-empty `error_data` as a partial result, not a success — see `30-failure-classes.md`.

`upload_file` success is `{"file_id": "..."}`; its output table names a single `error` (`ErrorInfo`) rather
than an `error_data` array, and Safir shows no failure example. Safir's error-handling section says every
service carries `error_data` and that `send_message` can return a separate error for each number; the
two statements conflict for `upload_file`, and `--mode response` accepts either failure shape.

`[source: https://docs.bale.ai/safir; read: 2026-10-20]`

## ErrorInfo

| Field | Type | Notes |
|---|---|---|
| `phone_number` | string | The recipient this error belongs to. |
| `code` | integer | Safir error code. |
| `description` | string | Human-readable description. |

`[source: https://docs.bale.ai/safir; read: 2026-10-20]`

## Documented error codes

| Code | Name | Meaning | Class |
|---|---|---|---|
| `2` | `InternalServerError` | Internal server error. | Ambiguous: Safir may have delivered. |
| `3` | `RateLimitExceeded` | Too many messages sent. | Throttled. |
| `4` | `InvalidInput` | Invalid JSON input. | Caller defect. |
| `8` | `InvalidPhone` | Invalid phone number. | Caller defect, almost always a normalisation defect. |
| `17` | `NotBaleUser` | The recipient has no Bale account. | Terminal for this channel. |
| `20` | `PaymentRequired` | Insufficient credit. | Terminal until an operator acts. |
| `21` | `MaximumContactLimitReached` | Bot contact limit reached. | Terminal until an operator acts. |

Preserve an unrecognised code as-is, with its description and its recipient, and treat it as terminal for
that recipient. Collapsing an unknown code into a generic failure destroys the one field that identifies
what happened, and an unknown code retried as if it were transient is how a caller-side defect becomes
provider load. `30-failure-classes.md` gives the response to each class.

`[source: https://docs.bale.ai/safir; read: 2026-10-20]`

## Not documented

Safir documents exactly two operations, `send_message` and `upload_file`. It does not document any of the
following, so each is `NEEDS_BALE_CONFIRMATION`: unknown, not absent. Record a confirmed answer here with
its source and read date.

- Rate limits and throughput.
- Batch or multi-recipient sending.
- The `request_id` deduplication window, its scope, and the response to a duplicate.
- A delivery-status lookup, receipt, or webhook.
- Whether the recipient must have started the bot.
- Template variable naming rules.
- HTTP status codes, an authentication-failure code, and `Retry-After`.

`[source: https://docs.bale.ai/safir; read: 2026-10-20]`
