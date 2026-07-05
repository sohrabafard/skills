# Bale Safir Examples

Use these examples for tests, docs, Postman requests, Insomnia requests, and implementation reviews. Replace secrets with environment variables or placeholders before committing.

## 1. Normal text message

### Curl

```bash
curl --location 'https://safir.bale.ai/api/v3/send_message' \
  --header 'api-access-key: *****' \
  --header 'Content-Type: application/json' \
  --data '{
    "bot_id": 1,
    "phone_number": "989100000000",
    "message_data": {
      "message": {
        "text": "متن"
      }
    }
  }'
```

### JSON body

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

## 2. OTP message

### Curl

```bash
curl --location 'https://safir.bale.ai/api/v3/send_message' \
  --header 'api-access-key: ***' \
  --header 'Content-Type: application/json' \
  --data '{
    "bot_id": 2040665828,
    "phone_number": "989100900000",
    "message_data": {
      "otp_message": {
        "otp": "123456"
      }
    }
  }'
```

### JSON body

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

Expected response shape may be:

```json
{
  "message_id": "BvQjaR.fIKt7kH.EXTddgYduJ2"
}
```

## 3. Template message

Bale template workflow:

1. Define a message template in Bale Business Panel.
2. Define variables inside that template.
3. Bale assigns a `template_id` after the template is available/approved.
4. Send `template_id` plus exact variable values in `text_fields`.
5. Bale substitutes the values and sends the rendered message.

### Curl

```bash
curl --location 'https://safir.bale.ai/api/v3/send_message' \
  --header 'api-access-key: ****' \
  --header 'Content-Type: application/json' \
  --data '{
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
  }'
```

### JSON body

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

## 4. Text message with idempotency

```json
{
  "request_id": "notif-20260705-000001-user-42-bale",
  "bot_id": 1,
  "phone_number": "989123456789",
  "message_data": {
    "message": {
      "text": "سلام، پیام تستی آلاء"
    }
  }
}
```

## 5. Text message with inline URL button

```json
{
  "request_id": "notif-inline-000001",
  "bot_id": 123456789,
  "phone_number": "989123456789",
  "message_data": {
    "message": {
      "text": "برای اطلاعات بیشتر روی دکمه زیر کلیک کنید.",
      "reply_markup": {
        "inline_keyboard": [
          [
            {
              "text": "مشاهده سایت",
              "url": "https://bale.ai"
            }
          ]
        ]
      }
    }
  }
}
```

## 6. Secure text message

```json
{
  "request_id": "secure-message-000001",
  "bot_id": 123456789,
  "phone_number": "989123456789",
  "message_data": {
    "is_secure": true,
    "message": {
      "text": "test text message"
    }
  }
}
```

## 7. Media message after upload

First upload the file:

```bash
curl --location 'https://safir.bale.ai/api/v3/upload_file' \
  --header 'api-access-key: <redacted>' \
  --form 'file=@"/path/to/file.jpg"'
```

Then send the returned `file_id`:

```json
{
  "request_id": "media-message-000001",
  "bot_id": 123456789,
  "phone_number": "989123456789",
  "message_data": {
    "message": {
      "text": "test caption",
      "file_id": "987141dd2672149..."
    }
  }
}
```

## 8. Invalid examples to reject before sending

```json
{
  "bot_id": 1,
  "phone_number": "09123830000",
  "message_data": {
    "message": {
      "text": "Wrong phone format for Safir payload"
    }
  }
}
```

```json
{
  "bot_id": 1,
  "phone_number": "+989123830000",
  "message_data": {
    "message": {
      "text": "Wrong Alaa outgoing format because of plus sign"
    }
  }
}
```

```json
{
  "bot_id": 1,
  "phone_number": "989123830000",
  "message_data": {
    "message": {
      "text": "Do not mix message variants"
    },
    "otp_message": {
      "otp": "123456"
    }
  }
}
```
