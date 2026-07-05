# Mediana SMS Provider Examples

Use these examples for tests, docs, Postman requests, Insomnia requests, and implementation reviews. Replace secrets with environment variables or placeholders before committing.

## Recommended environment setup

```bash
export MEDIANA_SMS_API_BASE_URL="${MEDIANA_SMS_API_BASE_URL:-https://edge.ippanel.com/v1}"
export MEDIANA_SMS_SEND_URL="${MEDIANA_SMS_SEND_URL:-$MEDIANA_SMS_API_BASE_URL/api/send}"
export MEDIANA_SMS_CANCEL_URL="${MEDIANA_SMS_CANCEL_URL:-$MEDIANA_SMS_API_BASE_URL/api/send/cancel}"
export MEDIANA_SMS_PRICE_URL="${MEDIANA_SMS_PRICE_URL:-$MEDIANA_SMS_API_BASE_URL/api/send/calculate-price}"
export MEDIANA_SMS_URL_SEND_ENDPOINT="${MEDIANA_SMS_URL_SEND_ENDPOINT:-$MEDIANA_SMS_API_BASE_URL/api/send/webservice}"
export MEDIANA_SMS_API_TOKEN="<secret>"
export MEDIANA_SMS_FROM_NUMBER="+983000505"
```

The exact variable names may follow the repository convention, but the endpoint must be configurable.

## 1. Webservice SMS

```bash
curl --location "$MEDIANA_SMS_SEND_URL" \
  --header "Authorization: $MEDIANA_SMS_API_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{
    "sending_type": "webservice",
    "from_number": "'"$MEDIANA_SMS_FROM_NUMBER"'",
    "message": "متن پیام",
    "params": {
      "recipients": [
        "+989120000000"
      ]
    }
  }'
```

JSON body:

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

Expected response shape:

```json
{
  "data": {
    "message_outbox_ids": [1123544244]
  },
  "meta": {
    "status": true,
    "message": "انجام شد",
    "message_parameters": [],
    "message_code": "200-1"
  }
}
```

## 2. SMS OTP through pattern

Use this when OTP must be sent as SMS through an approved Mediana/IPPanel pattern.

```bash
curl --location "$MEDIANA_SMS_SEND_URL" \
  --header "Authorization: $MEDIANA_SMS_API_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{
    "sending_type": "pattern",
    "from_number": "'"$MEDIANA_SMS_FROM_NUMBER"'",
    "code": "<pattern-code>",
    "recipients": [
      "+989120000000"
    ],
    "params": {
      "code": "458921"
    }
  }'
```

JSON body:

```json
{
  "sending_type": "pattern",
  "from_number": "+983000505",
  "code": "<pattern-code>",
  "recipients": ["+989120000000"],
  "params": {
    "code": "458921"
  }
}
```

## 3. Pattern SMS with several variables

```json
{
  "sending_type": "pattern",
  "from_number": "+983000505",
  "code": "course-ticket-template-code",
  "recipients": ["+989120000000"],
  "params": {
    "user": "test",
    "course": "test",
    "content_title": "test",
    "content_link": "test",
    "ticket_url": "test"
  }
}
```

Do not use these variable names unless the approved Mediana pattern actually defines them.

## 4. Voice OTP / VOTP

```bash
curl --location "$MEDIANA_SMS_SEND_URL" \
  --header "Authorization: $MEDIANA_SMS_API_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{
    "sending_type": "votp",
    "message": "45852",
    "params": {
      "recipients": [
        "+989120000000"
      ]
    }
  }'
```

JSON body:

```json
{
  "sending_type": "votp",
  "message": "45852",
  "params": {
    "recipients": ["+989120000000"]
  }
}
```

## 5. Peer-to-peer SMS

```json
{
  "sending_type": "peer_to_peer",
  "from_number": "+983000505",
  "params": [
    {
      "recipients": ["+989120000000", "+989350000000"],
      "message": "پیام اول"
    },
    {
      "recipients": ["+989130000000"],
      "message": "پیام دوم"
    }
  ]
}
```

## 6. Scheduled webservice SMS

`send_time` must be UTC.

```json
{
  "sending_type": "webservice",
  "from_number": "+983000505",
  "message": "متن پیام زمان‌بندی‌شده",
  "params": {
    "recipients": ["+989120000000"]
  },
  "send_time": "2026-07-05 10:30:00"
}
```

## 7. File SMS, multipart

```bash
curl --location "$MEDIANA_SMS_SEND_URL" \
  --header "Authorization: $MEDIANA_SMS_API_TOKEN" \
  --header 'Accept: application/json' \
  --form 'sending_type="file"' \
  --form 'from_number="+983000505"' \
  --form 'message="متن پیام"' \
  --form 'files[]=@"/path/to/your/file.csv"' \
  --form 'send_time="2026-07-05 10:30:00"' \
  --form 'other_recipients[]="+989120000000"'
```

## 8. Cancel scheduled message

```bash
curl --location "$MEDIANA_SMS_CANCEL_URL" \
  --header "Authorization: $MEDIANA_SMS_API_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{
    "message_outbox_id": 1148303263
  }'
```

## 9. Calculate SMS price

```bash
curl --location "$MEDIANA_SMS_PRICE_URL" \
  --header "Authorization: $MEDIANA_SMS_API_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{
    "number": "+983000505",
    "message": "تست"
  }'
```

## 10. URL send endpoint, only when required

```bash
curl -X GET "$MEDIANA_SMS_URL_SEND_ENDPOINT?from=+983000505&message=متن پیام&to=+989120000000&apikey=$MEDIANA_SMS_API_TOKEN"
```

Prefer JSON `webservice` sends unless legacy URL behavior is explicitly required.

## Invalid examples to reject before sending

### Bale payload accidentally used for Mediana

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

Reason: Mediana uses `sending_type`, `from_number`, `message`, `params`/`recipients`, and `Authorization`; this is a Bale Safir shape.

### Wrong recipient format

```json
{
  "sending_type": "webservice",
  "from_number": "+983000505",
  "message": "متن پیام",
  "params": {
    "recipients": ["09120000000"]
  }
}
```

Reason: normalize to `+989120000000` before sending.

### Pattern using webservice recipient nesting

```json
{
  "sending_type": "pattern",
  "from_number": "+983000505",
  "code": "pattern-code",
  "params": {
    "recipients": ["+989120000000"],
    "code": "458921"
  }
}
```

Reason: pattern recipients must be top-level `recipients`, while `params` is for pattern variables.

### Pattern with multiple recipients

```json
{
  "sending_type": "pattern",
  "from_number": "+983000505",
  "code": "pattern-code",
  "recipients": ["+989120000000", "+989130000000"],
  "params": {"code": "458921"}
}
```

Reason: the official pattern endpoint allows only one recipient per request.
