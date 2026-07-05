# Bale Safir API Reference

This reference captures the Bale Safir message-sending contract used by Alaa agents. Treat it as the local contract
unless current official Bale documentation or repository truth proves a newer behavior.

## Source and authority

- Safir is Bale's RESTful message-sending service for Bale bots or business arms.
- Every API request requires the organization's `api-access-key` header.
- The user-provided Alaa rule for outgoing phone numbers is stricter than one example in the pasted docs: always send
  digits only, starting with `98`, without `+`.
- Do not infer unsupported fields from Telegram or other bot APIs.

## Base endpoints

### Send message

```text
Protocol: HTTPS
Method: POST
Type: JSON
URL: https://safir.bale.ai/api/v3/send_message
Headers:
  api-access-key: secret API access key
  Content-Type: application/json
```

### Upload file

```text
Protocol: HTTPS
Method: POST
Type: multipart/form-data
URL: https://safir.bale.ai/api/v3/upload_file
Headers:
  api-access-key: secret API access key
Form field:
  file: multipart file, maximum 500 MB
```

## Send message input envelope

| Field                   | Type    | Required | Notes                                                                                                                    |
|-------------------------|---------|----------|--------------------------------------------------------------------------------------------------------------------------|
| `api-access-key` header | string  | yes      | Organization API key from Bale Business Panel. Do not log or commit.                                                     |
| `request_id` body       | string  | no       | Idempotency key. Reusing the same value prevents duplicate send for repeated requests. Recommended for production sends. |
| `bot_id` body           | integer | yes      | Numeric ID of the sender bot/arm.                                                                                        |
| `phone_number` body     | string  | yes      | Destination phone in Alaa-canonical form: `98` plus 10 digits, no `+`, no leading `0`, no separators.                    |
| `message_data` body     | object  | yes      | Contains one primary message variant plus optional modifiers.                                                            |

## Phone number contract

Outgoing Safir payloads must use:

```text
^989[0-9]{9}$
```

Examples:

| User input      | Outgoing `phone_number`                  |
|-----------------|------------------------------------------|
| `09123830000`   | `989123830000`                           |
| `+989123830000` | `989123830000`                           |
| `989123830000`  | `989123830000`                           |
| `۰۹۱۲۳۸۳۰۰۰۰`   | `989123830000` after digit normalization |

Reject or normalize away spaces, hyphens, zero-width joiners, Persian digits, Arabic digits, and other formatting
characters before sending. Do not send `0912...`, `+98912...`, or `912...` in the API payload.

## MessageData

| Field              | Type                        | Required | Notes                                                                                           |
|--------------------|-----------------------------|----------|-------------------------------------------------------------------------------------------------|
| `message`          | object of `Message`         | no       | Normal text/media/copy/inline-button message.                                                   |
| `otp_message`      | object of `OTPMessage`      | no       | OTP special message.                                                                            |
| `template_message` | object of `TemplateMessage` | no       | Template message. The pasted table omitted it, but the same Bale docs and user examples use it. |
| `is_secure`        | boolean                     | no       | Set `true` for secure message or secure template payloads.                                      |

Use exactly one of `message`, `otp_message`, or `template_message` for normal sends. `is_secure` may accompany `message`
or `template_message`.

## Message

| Field          | Type                    | Required | Notes                                          |
|----------------|-------------------------|----------|------------------------------------------------|
| `text`         | string                  | no       | Text body or media caption.                    |
| `file_id`      | string                  | no       | ID returned by `upload_file`.                  |
| `copy_text`    | string                  | no       | Adds a copy affordance for the provided value. |
| `reply_markup` | object of `ReplyMarkup` | no       | Inline keyboard attached to the message.       |

A practical payload should include at least one visible content field such as `text`, `file_id`, or `copy_text`.

## ReplyMarkup

| Field             | Type                                     | Required | Notes                                                               |
|-------------------|------------------------------------------|----------|---------------------------------------------------------------------|
| `inline_keyboard` | array of array of `InlineKeyboardButton` | yes      | Outer array is rows; each inner array is one row of inline buttons. |

## InlineKeyboardButton

| Field       | Type                   | Required | Notes                  |
|-------------|------------------------|----------|------------------------|
| `text`      | string                 | yes      | Display text.          |
| `url`       | string                 | no       | Opens a URL.           |
| `web_app`   | object of `WebAppInfo` | no       | Opens a Bale mini-app. |
| `copy_text` | string                 | no       | Copies text.           |

At least one of `url`, `web_app`, or `copy_text` must be set. Prefer exactly one per button.

### WebAppInfo

| Field | Type   | Required | Notes                              |
|-------|--------|----------|------------------------------------|
| `url` | string | yes      | Mini-app URL opened by the button. |

## OTPMessage

| Field | Type   | Required | Notes                                                               |
|-------|--------|----------|---------------------------------------------------------------------|
| `otp` | string | yes      | OTP text. Current Safir docs state only numeric OTPs are supported. |

OTP sends use Bale's OTP presentation. Bale automatically includes the sender bot name and copy OTP affordance. Do not
add custom text around `otp_message` unless implementing an explicitly separate fallback channel.

## TemplateMessage

Template messages are created in Bale Business Panel, reviewed/approved by Bale support, and then addressed by
`template_id`.

| Field         | Type   | Required | Notes                                                                                                            |
|---------------|--------|----------|------------------------------------------------------------------------------------------------------------------|
| `template_id` | string | yes      | ID assigned by Bale to the approved template.                                                                    |
| `text_fields` | object | yes      | Mapping of template variable names to string values. Keys must exactly match the variable names in the template. |

Rules:

- Do not invent field names. Use repository metadata, Bale panel data, or user-provided examples.
- Preserve exact variable spelling and snake/camel case from the Bale template.
- Treat missing local template metadata as `NEEDS_BALE_TEMPLATE_CONFIRMATION`.

## Secure messages

Set `message_data.is_secure` to `true` for secure normal or secure template messages:

```json
{
  "message_data": {
    "is_secure": true,
    "message": {
      "text": "متن محرمانه"
    }
  }
}
```

The docs show secure text, secure media, and secure template examples. They do not show secure OTP; do not assume that
combination.

## Upload file response

Success response:

```json
{
  "file_id": "987141dd2672149..."
}
```

Error response may include:

```json
{
  "error": {
    "phone_number": "989123456789",
    "code": 4,
    "description": "..."
  }
}
```

Use the returned `file_id` in `message_data.message.file_id`.

## Send message response

Common success response:

```json
{
  "message_id": "523e6875-7c41-491b-8460-04b33039d7fc",
  "error_data": null
}
```

OTP success response in the provided docs may omit `error_data`:

```json
{
  "message_id": "BvQjaR.fIKt7kH.EXTddgYduJ2"
}
```

Handle both shapes. Treat `message_id` with absent, null, or empty `error_data` as success unless transport status or
other required response checks fail.

## ErrorInfo

| Field          | Type    | Notes                             |
|----------------|---------|-----------------------------------|
| `phone_number` | string  | Number associated with the error. |
| `code`         | integer | Safir error code.                 |
| `description`  | string  | Human-readable error description. |

## Documented error codes

| Code | Name                         | Meaning                                        |
|------|------------------------------|------------------------------------------------|
| `2`  | `InternalServerError`        | Internal server error.                         |
| `3`  | `RateLimitExceeded`          | Too many messages sent.                        |
| `4`  | `InvalidInput`               | Invalid JSON input.                            |
| `8`  | `InvalidPhone`               | Invalid phone number.                          |
| `17` | `NotBaleUser`                | Destination user does not have a Bale account. |
| `20` | `PaymentRequired`            | Insufficient credit.                           |
| `21` | `MaximumContactLimitReached` | Bot contact limit reached.                     |

Error-handling guidance:

- Preserve unknown error codes in provider results.
- Map `InvalidPhone` to normalization/validation defects where applicable.
- Map `NotBaleUser` as a deliverability/user-channel failure, not as a transient transport failure.
- Map `RateLimitExceeded` as retryable only if the caller has a bounded retry/backoff policy and idempotent
  `request_id`.
- Map `PaymentRequired` as non-retryable until account credit is fixed.

## Idempotency

`request_id` prevents duplicate sends when the same API request is repeated. Use it for production sends.

Recommended pattern:

- Generate a stable request ID from the business delivery intent, such as notification ID, recipient ID, template ID,
  and attempt-independent send ID.
- Store the generated `request_id` before the first external call.
- Reuse it on retry after timeout, 5xx, or queue retry.
- Do not reuse it across different recipients, different message bodies, different templates, or manually triggered
  resends that should create a new message.

## Security and privacy

- Redact `api-access-key` in logs, traces, exceptions, screenshots, and final reports.
- Redact OTP values by default. If a test must show an OTP, use a synthetic value such as `123456`.
- Avoid logging full phone numbers; prefer masked forms such as `98912*****00` or a stable hash.
- Keep template fields that may contain names, course titles, links, or ticket URLs out of high-cardinality metrics.
