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

**No fact in this file has a recorded read date.** The facts were transcribed from vendor documentation
that was pasted into a session, and neither the URL nor the date survived into this skill. That is why
every line below reads `unverified as of 2026-07-27` rather than carrying a date: an invented date is
worse than an admitted gap, because it silences the freshness rule for a year.

The freshness rule that governs these lines is in `SKILL.md` under "Provenance". Record the URL and the
read date together when re-verifying, because a fact re-verified without a recorded date is unverified
again on the next read.

## Endpoints

| Purpose | Method | Default URL | Content type |
|---|---|---|---|
| Send a message | `POST` | `$BALE_SAFIR_BASE_URL/api/v3/send_message` | `application/json` |
| Upload a file | `POST` | `$BALE_SAFIR_BASE_URL/api/v3/upload_file` | `multipart/form-data`, field `file` |

Both requests carry the `api-access-key` header. Documented maximum upload size is 500 MB.

`[source: not recorded; read: unverified as of 2026-07-27]`

## Request envelope

| Field | Type | Required | Notes |
|---|---|---|---|
| `api-access-key` header | string | yes | Organisation key from Bale Business Panel. |
| `request_id` body | string | yes for every production send | Idempotency key. See the body of this skill, which owns the derivation rule. |
| `bot_id` body | integer | yes | Numeric id of the sender bot or business arm. Numeric, never a string. |
| `phone_number` body | string | yes | `989xxxxxxxxx`. See `40-phone-and-conformance.md`. |
| `message_data` body | object | yes | Exactly one primary variant, plus the optional `is_secure` modifier. |

Safir's own documentation marks `request_id` optional. This skill requires it for production sends, and the
reason is in the body under "Idempotency". A vendor-optional field that this platform requires is recorded
in both places on purpose: the vendor column states what Safir accepts, the body states what Alaa sends.

`[source: not recorded; read: unverified as of 2026-07-27]`

## MessageData

| Field | Type | Required | Notes |
|---|---|---|---|
| `message` | `Message` | no | Text, media, copy affordance, or inline buttons. |
| `otp_message` | `OTPMessage` | no | OTP presentation. |
| `template_message` | `TemplateMessage` | no | Pre-approved template addressed by id. |
| `is_secure` | boolean | no | Secure-message modifier. Not a primary variant. |

Exactly one of `message`, `otp_message`, or `template_message` is present. Two primary variants in one
`message_data` is rejected by `scripts/validate_bale_payload.py`, because the vendor documentation does not
state which one wins and an agent that guesses ships a message nobody reviewed.

`[source: not recorded; read: unverified as of 2026-07-27]`

## Message

| Field | Type | Required | Notes |
|---|---|---|---|
| `text` | string | no | Message body, or the caption of a media message. |
| `file_id` | string | no | Value returned by `upload_file`. |
| `copy_text` | string | no | Adds a copy affordance for the given value. |
| `reply_markup` | `ReplyMarkup` | no | Inline keyboard attached to the message. |

A `Message` carries at least one of `text`, `file_id`, or `copy_text`; a `Message` with only
`reply_markup` has no visible content.

`[source: not recorded; read: unverified as of 2026-07-27]`

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

Each button carries exactly one of `url`, `web_app`, or `copy_text`. Safir documents no callback buttons,
so a button carrying `callback_data` is a Telegram payload that reached the wrong provider.

`[source: not recorded; read: unverified as of 2026-07-27]`

## OTPMessage

| Field | Type | Required | Notes |
|---|---|---|---|
| `otp` | string | yes | ASCII digits only. |

Safir renders the OTP itself, including the sender bot name and a copy affordance. Send `otp_message` with
no surrounding text: wrapping an OTP in a normal text message loses that rendering and the user sees a
plain message where they expected the OTP card.

The digits are ASCII. Persian-Indic (`U+06F0`-`U+06F9`), Arabic-Indic (`U+0660`-`U+0669`) and superscript
digits are not ASCII digits, and a language-level "is this a digit" check accepts all three — Python's
`str.isdigit()` returns `True` for every one of them. Match `^[0-9]{4,8}$` explicitly instead.

`[source: not recorded; read: unverified as of 2026-07-27]`

## TemplateMessage

Templates are created in Bale Business Panel, approved by Bale support, then addressed by id.

| Field | Type | Required | Notes |
|---|---|---|---|
| `template_id` | string | yes | Id Bale assigned to the approved template. |
| `text_fields` | object | yes | Template variable name to string value. Keys match the template's variable names exactly. |

Take field names from repository metadata, Bale panel data, or a user-provided example. Where none of the
three is available, stop and report `NEEDS_BALE_TEMPLATE_CONFIRMATION` naming the template id, because a
guessed variable name renders as an empty substitution that no test catches and the recipient reads.

Preserve the exact spelling and case of each variable.

`[source: not recorded; read: unverified as of 2026-07-27]`

## The secure-message modifier

`message_data.is_secure: true` marks a secure normal message or a secure template message.

The vendor documentation shows secure text, secure media and secure template. It shows no secure OTP.
Send `otp_message` without `is_secure`. To enable secure OTP, verify the combination against live Safir
documentation first and record the URL and read date in this file; `scripts/validate_bale_payload.py`
rejects the combination until that happens, so the check and the document cannot drift apart silently.

`[source: not recorded; read: unverified as of 2026-07-27]`

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

`[source: not recorded; read: unverified as of 2026-07-27]`

## Responses

`send_message` success carries a `message_id`. Two shapes are documented and both occur:

```json
{ "message_id": "523e6875-7c41-491b-8460-04b33039d7fc", "error_data": null }
```

```json
{ "message_id": "BvQjaR.fIKt7kH.EXTddgYduJ2" }
```

Treat `message_id` present with `error_data` absent, null, or empty as success. Treat `message_id` present
with a non-empty `error_data` as a partial result, not a success — see `30-failure-classes.md`.

`upload_file` success is `{"file_id": "..."}`; its failure shape nests a single `error` object rather than
an `error_data` array.

`[source: not recorded; read: unverified as of 2026-07-27]`

## ErrorInfo

| Field | Type | Notes |
|---|---|---|
| `phone_number` | string | The recipient this error belongs to. |
| `code` | integer | Safir error code. |
| `description` | string | Human-readable description. |

`[source: not recorded; read: unverified as of 2026-07-27]`

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

`[source: not recorded; read: unverified as of 2026-07-27]`
