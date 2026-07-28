# Bale Safir examples, responses, and rejects

Read this when writing tests, fixtures, documentation, Postman or Insomnia requests, or a concrete curl
example.

Every example reads credentials and the host from the environment:

```bash
export BALE_SAFIR_BASE_URL='https://safir.bale.ai'
export BALE_SAFIR_API_ACCESS_KEY='<from the secret store, never committed>'
```

Every request example carries `request_id`, because every production send does. The values below are
illustrative UUIDv7 strings; the real value is the delivery's durable public id.

## Requests

### 1. Normal text message

```bash
curl --location "$BALE_SAFIR_BASE_URL/api/v3/send_message" \
  --header "api-access-key: $BALE_SAFIR_API_ACCESS_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "request_id": "01936c7e-1f2a-7b3c-8d4e-5f6a7b8c9d0e",
    "bot_id": 1,
    "phone_number": "989123830000",
    "message_data": { "message": { "text": "Your class starts in one hour." } }
  }'
```

### 2. OTP message

```bash
curl --location "$BALE_SAFIR_BASE_URL/api/v3/send_message" \
  --header "api-access-key: $BALE_SAFIR_API_ACCESS_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "request_id": "01936c7e-2a3b-7c4d-8e5f-6a7b8c9d0e1f",
    "bot_id": 2040665828,
    "phone_number": "989123830000",
    "message_data": { "otp_message": { "otp": "123456" } }
  }'
```

`123456` is a synthetic OTP. Never put a real OTP in a fixture, a test, or a bug report.

### 3. Template message

The workflow: define the template in Bale Business Panel, define its variables, wait for Bale to approve it
and assign a `template_id`, then send that id with exact variable values in `text_fields`.

```bash
curl --location "$BALE_SAFIR_BASE_URL/api/v3/send_message" \
  --header "api-access-key: $BALE_SAFIR_API_ACCESS_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "request_id": "01936c7e-3b4c-7d5e-8f6a-7b8c9d0e1f2a",
    "bot_id": 1,
    "phone_number": "989123830000",
    "message_data": {
      "template_message": {
        "template_id": "t1",
        "text_fields": {
          "user": "Sara",
          "course": "Algebra 1",
          "content_title": "Session 4",
          "content_link": "https://example.invalid/c/4",
          "ticket_url": "https://example.invalid/t/9"
        }
      }
    }
  }'
```

### 4. Inline URL button

```json
{
  "request_id": "01936c7e-4c5d-7e6f-8a7b-8c9d0e1f2a3b",
  "bot_id": 123456789,
  "phone_number": "989123830000",
  "message_data": {
    "message": {
      "text": "Tap below for details.",
      "reply_markup": {
        "inline_keyboard": [
          [{ "text": "Open the site", "url": "https://example.invalid" }]
        ]
      }
    }
  }
}
```

### 5. Secure text message

```json
{
  "request_id": "01936c7e-5d6e-7f7a-8b8c-9d0e1f2a3b4c",
  "bot_id": 123456789,
  "phone_number": "989123830000",
  "message_data": {
    "is_secure": true,
    "message": { "text": "Your statement is ready." }
  }
}
```

### 6. Media message, after upload

Step 1 uploads the file:

```bash
curl --location "$BALE_SAFIR_BASE_URL/api/v3/upload_file" \
  --header "api-access-key: $BALE_SAFIR_API_ACCESS_KEY" \
  --form 'file=@"/path/to/file.jpg"'
```

Step 2 sends the returned `file_id`. Persist it before sending, so a step-2 failure is retryable without
re-uploading:

```json
{
  "request_id": "01936c7e-6e7f-7a8b-8c9d-0e1f2a3b4c5d",
  "bot_id": 123456789,
  "phone_number": "989123830000",
  "message_data": {
    "message": { "text": "This week's schedule.", "file_id": "987141dd2672149" }
  }
}
```

## Responses

Validate these with `--mode response`. Feeding a response to the request validator produces errors that
mean nothing.

Success, both documented shapes:

```json
{ "message_id": "523e6875-7c41-491b-8460-04b33039d7fc", "error_data": null }
```

```json
{ "message_id": "BvQjaR.fIKt7kH.EXTddgYduJ2" }
```

Partial result. `message_id` is present and `error_data` is not empty, so this is not a success — take the
outcome per recipient and see `30-failure-classes.md` class 8:

```json
{
  "message_id": "523e6875-7c41-491b-8460-04b33039d7fc",
  "error_data": [
    { "phone_number": "989123830001", "code": 17, "description": "user is not a Bale user" }
  ]
}
```

`upload_file` success and failure:

```json
{ "file_id": "987141dd2672149" }
```

```json
{ "error": { "phone_number": "989123830000", "code": 4, "description": "invalid input" } }
```

## Rejects

Each of these must fail before it reaches the wire. `scripts/validate_bale_payload.py` rejects every one.

Trunk-zero number that was never normalised:

```json
{ "request_id": "r", "bot_id": 1, "phone_number": "09123830000",
  "message_data": { "message": { "text": "wrong phone form" } } }
```

E.164 with the plus sign, which is Mediana's form and not Safir's:

```json
{ "request_id": "r", "bot_id": 1, "phone_number": "+989123830000",
  "message_data": { "message": { "text": "wrong phone form for this channel" } } }
```

Two primary variants in one `message_data`:

```json
{ "request_id": "r", "bot_id": 1, "phone_number": "989123830000",
  "message_data": { "message": { "text": "hi" }, "otp_message": { "otp": "123456" } } }
```

Telegram fields that Safir does not define:

```json
{ "request_id": "r", "bot_id": 1, "phone_number": "989123830000",
  "chat_id": 99, "parse_mode": "MarkdownV2", "disable_notification": true,
  "message_data": { "message": { "text": "hi" } } }
```

A non-ASCII OTP, which a `str.isdigit()` check accepts and Safir does not:

```json
{ "request_id": "r", "bot_id": 1, "phone_number": "989123830000",
  "message_data": { "otp_message": { "otp": "۱۲۳۴۵۶" } } }
```

A missing `request_id`, and a whitespace-only one:

```json
{ "bot_id": 1, "phone_number": "989123830000",
  "message_data": { "message": { "text": "no idempotency key" } } }
```

```json
{ "request_id": "   ", "bot_id": 1, "phone_number": "989123830000",
  "message_data": { "message": { "text": "whitespace is not a key" } } }
```

A Mediana payload that reached the Bale client:

```json
{ "sending_type": "pattern", "from_number": "+983000505", "recipients": ["+989123830000"] }
```
