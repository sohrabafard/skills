# Mediana / IPPanel Edge API Reference

This reference captures the Mediana SMS provider contract used by Alaa agents. Treat it as the local contract unless current official Mediana/IPPanel documentation or repository truth proves newer account-specific behavior.

## Source snapshot

Checked sources:

- Official docs repository: `https://github.com/ippanelcom/Edge-Document`
- Official rendered docs: `https://ippanelcom.github.io/Edge-Document/docs/`
- User-uploaded vendor Go sample: `assets/vendor-sdk.go`

Key current official facts:

- Base URL: `https://edge.ippanel.com/v1`
- Main send endpoint: `POST {base_url}/api/send`
- Auth header: `Authorization: <token-or-api-key>`
- JSON response envelope: `data` plus `meta`
- API keys can be generated from the user panel and do not expire, but some sensitive endpoints only support tokens.

## Environment-driven endpoints

Use defaults only as fallbacks. Production code must read these from env/config or an equivalent repository configuration system.

```text
MEDIANA_SMS_API_BASE_URL=https://edge.ippanel.com/v1
MEDIANA_SMS_SEND_URL=https://edge.ippanel.com/v1/api/send
MEDIANA_SMS_CANCEL_URL=https://edge.ippanel.com/v1/api/send/cancel
MEDIANA_SMS_PRICE_URL=https://edge.ippanel.com/v1/api/send/calculate-price
MEDIANA_SMS_URL_SEND_ENDPOINT=https://edge.ippanel.com/v1/api/send/webservice
MEDIANA_SMS_API_TOKEN=<secret>
MEDIANA_SMS_FROM_NUMBER=<account-approved sender/originator>
```

If the repo already uses a base URL and path convention, use it. The final request URL must remain configurable without code changes.

## Common headers

### JSON requests

```text
Authorization: <token-or-api-key>
Content-Type: application/json
```

### Multipart requests

```text
Authorization: <token-or-api-key>
Content-Type: multipart/form-data
Accept: application/json
```

Do not add `Bearer` unless existing repo/account documentation proves it is required.

## Send variants summary

| Variant | Method/endpoint | Content type | Main fields | Use |
| --- | --- | --- | --- | --- |
| `webservice` | `POST /api/send` | JSON | `from_number`, `message`, `params.recipients`, optional `send_time` | Default custom/transactional SMS |
| `pattern` | `POST /api/send` | JSON | `from_number`, `code`, one-recipient `recipients`, `params`, optional `phonebook` | Approved template/pattern SMS, including SMS OTP |
| `votp` | `POST /api/send` | JSON | `message`, one-recipient `params.recipients` | Voice OTP only |
| `peer_to_peer` | `POST /api/send` | JSON | `from_number`, `params[]` with each `message` and `recipients` | Different messages to different recipient groups |
| `file` | `POST /api/send` | multipart | `from_number`, `message`, `files[]`, optional `other_recipients`, optional `send_time` | Send one message to numbers from CSV/XLSX |
| `peer_to_peer_file` | `POST /api/send` | multipart | `from_number`, `files[]`, optional `send_time` | File-driven personalized messages |
| `keyword` | `POST /api/send` | multipart | `from_number`, `message` with placeholders, `files[]`, optional `send_time` | Placeholder data from uploaded file |
| `keyword_phonebook` | `POST /api/send` | JSON | `from_number`, `message`, `params[].phonebook_id`, optional `send_time` | Placeholder data from phonebook fields |
| `phonebook` | `POST /api/send` | JSON | `from_number`, `message`, `params[]` | Send to all/selected phonebook contacts |
| `postal_code` | `POST /api/send` | JSON | `from_number`, `message`, `params[]`, optional `other_recipients`, optional `send_time` | Postal-code targeting |
| `country` | `POST /api/send` | JSON | `from_number`, `message`, `params[]`, optional `other_recipients` | Province/county/city targeting |
| `geolocation` | `POST /api/send` | JSON | `from_number`, `message`, Country V2 `params[]`, optional `other_recipients` | Newer geographic targeting |
| `job` | `POST /api/send` | JSON | `from_number`, `message`, job-category `params[]` | Job-category targeting |
| URL send | `GET /api/send/webservice` | query string | `apikey` or `username/password`, `from`, `message`, `to` | Legacy/simple URL send; not default |
| cancel scheduled | `POST /api/send/cancel` | JSON | `message_outbox_id` | Cancel a scheduled send |
| calculate price | `POST /api/send/calculate-price` | JSON | `number`, `message` | Estimate SMS price and parts |

`normal` may appear in older examples or account code. Do not introduce it for new work unless repository truth requires it.

## Core send shapes

### Webservice SMS

```json
{
  "sending_type": "webservice",
  "from_number": "+983000505",
  "message": "متن پیام",
  "params": {
    "recipients": [
      "+989120000000",
      "+989350000000"
    ]
  },
  "send_time": "2025-03-12 21:20:02"
}
```

Rules:

- `from_number` must be an account-approved sender.
- `params.recipients` contains E.164 recipients. For Alaa Iranian mobile recipients, normalize to `+989xxxxxxxxx`.
- `send_time` is optional; if present, it is UTC in `YYYY-MM-DD HH:MM:SS`.

### Pattern SMS

```json
{
  "sending_type": "pattern",
  "from_number": "+983000505",
  "code": "xxxxxxxxxxxxxxx",
  "recipients": [
    "+989120000000"
  ],
  "params": {
    "code": "متن جایگذاری"
  }
}
```

Rules:

- Use `code` for the provider-assigned pattern code.
- `recipients` is top-level, not inside `params`.
- The official endpoint allows only one recipient.
- `params` keys must match placeholders in the approved pattern.
- Optional `phonebook` may be included only when the product explicitly wants to save the recipient to a phonebook:

```json
{
  "phonebook": {
    "id": 1234,
    "name": "سعید محمدی",
    "pre": "mr",
    "email": "saeed@gmail.com",
    "options": {
      "456": "1970/01/01"
    }
  }
}
```

### VOTP

```json
{
  "sending_type": "votp",
  "message": "45852",
  "params": {
    "recipients": [
      "+989120000000"
    ]
  }
}
```

Rules:

- `message` is the voice OTP code.
- Only one recipient is allowed.
- Do not use VOTP when the user asked for SMS OTP; use pattern SMS for SMS OTP.
- The official page contains a note about `from_number`, but the request body and vendor Go sample omit it. Follow repo/account truth if it differs.

## Peer-to-peer

Use when each group has its own message.

```json
{
  "sending_type": "peer_to_peer",
  "from_number": "+983000505",
  "params": [
    {
      "recipients": [
        "+989120000000",
        "+989350000000"
      ],
      "message": "پیام اول"
    },
    {
      "recipients": [
        "+989130000000"
      ],
      "message": "پیام دوم"
    }
  ]
}
```

The response returns one `message_outbox_id` per message group, not per individual recipient.

## Multipart file variants

These use `multipart/form-data`, not JSON. Validate a JSON-like metadata object in tests, but encode the actual request as form fields.

### File SMS

```bash
curl --location "$MEDIANA_SMS_SEND_URL" \
  --header "Authorization: $MEDIANA_SMS_API_TOKEN" \
  --header 'Accept: application/json' \
  --form 'sending_type="file"' \
  --form 'from_number="+983000505"' \
  --form 'message="متن پیام"' \
  --form 'files[]=@"/path/to/your/file.csv"' \
  --form 'other_recipients[]="+989120000000"'
```

### Peer-to-peer by file

```bash
curl --location "$MEDIANA_SMS_SEND_URL" \
  --header "Authorization: $MEDIANA_SMS_API_TOKEN" \
  --header 'Accept: application/json' \
  --form 'sending_type="peer_to_peer_file"' \
  --form 'from_number="+983000505"' \
  --form 'send_time="2025-04-25 10:10:10"' \
  --form 'files[]=@"/path/to/your/file.csv"'
```

CSV format for peer-to-peer-by-file:

```csv
recipient,message
09123456789,Personalized message for first recipient
09123456788,Personalized message for second recipient
```

### Keyword file SMS

```bash
curl --location "$MEDIANA_SMS_SEND_URL" \
  --header "Authorization: $MEDIANA_SMS_API_TOKEN" \
  --header 'Accept: application/json' \
  --form 'sending_type="keyword"' \
  --form 'from_number="+983000505"' \
  --form 'message="سلام {ex_B} م۱ {ex_C}"' \
  --form 'files[]=@"/path/to/your/file.xlsx"'
```

## Phonebook and keyword-phonebook

### Keyword phonebook

```json
{
  "sending_type": "keyword_phonebook",
  "from_number": "+983000505",
  "message": "تاریخ {ex_50856}\nبدهی {ex_50858}",
  "send_time": "2025-03-25 10:10:10",
  "params": [
    {
      "phonebook_id": 123654
    }
  ]
}
```

### Phonebook

```json
{
  "sending_type": "phonebook",
  "from_number": "+983000505",
  "message": "تست",
  "params": [
    {
      "phonebook_ids": ["123654"],
      "type": "all",
      "start": "1",
      "size": "2"
    },
    {
      "phonebook_id": "456987",
      "type": "detail",
      "number_ids": ["123", "456", "789"]
    }
  ]
}
```

For `type: "all"`, use `phonebook_ids`. For `type: "detail"`, use `phonebook_id` plus `number_ids`.

## Targeting/bulk variants

These can create large campaigns. Use only after explicit product and compliance approval.

### Postal code

```json
{
  "sending_type": "postal_code",
  "from_number": "+98BANK",
  "message": "متن پیام",
  "params": [
    {
      "bank": "all",
      "postal_code": 131,
      "gender": 0,
      "age_from": 1330,
      "age_to": 1402,
      "mci": {"start": 0, "size": 1},
      "irancell": {"start": 0, "size": 0},
      "other": {"start": 0, "size": 0}
    }
  ],
  "other_recipients": ["+989120000000"]
}
```

### Country

```json
{
  "sending_type": "country",
  "from_number": "+98BANK",
  "message": "تست",
  "params": [
    {
      "bank": "all",
      "pre": 938,
      "province_id": 89,
      "county_id": 212,
      "city_id": 82,
      "gender": 0,
      "age_from": 1300,
      "age_to": 1401,
      "mci": {"start": 10, "size": 100},
      "irancell": {"start": 1, "size": 2},
      "other": {"start": 2, "size": 3}
    }
  ],
  "other_recipients": ["+989121111111"]
}
```

### Geolocation / Country V2

The Country V2 docs show request body `sending_type: "geolocation"` while one parameter table row still says `country`; follow the request body unless repo/account truth proves otherwise.

```json
{
  "sending_type": "geolocation",
  "from_number": "+98BANK",
  "message": "تست",
  "params": [
    {
      "province_id": 1,
      "county_id": 2,
      "city_id": 5,
      "pre": "912",
      "gender": 2,
      "from_age": 1354,
      "to_age": 1364,
      "operator": [
        {"start": 0, "size": 10, "id": 1},
        {"start": 0, "size": 20, "id": 2}
      ]
    }
  ],
  "other_recipients": ["+989121111111"]
}
```

### Job

```json
{
  "sending_type": "job",
  "from_number": "+98PRO",
  "message": "متن پیام",
  "params": [
    {
      "main_category_id": 1,
      "sub_category_id": 1,
      "operator": [
        {"start": 0, "size": 3373, "id": 2}
      ]
    }
  ]
}
```

Operator IDs shown by docs: `1` for MCI, `2` for Irancell, `13` for Others.

## URL send endpoint

Use only when explicitly requested or required by legacy integration.

```bash
curl -X GET "$MEDIANA_SMS_URL_SEND_ENDPOINT?from=+983000505&message=متن پیام&to=+989120000000&apikey=$MEDIANA_SMS_API_TOKEN"
```

Allowed auth forms are API key or username/password, not both. The docs list many accepted aliases for query parameters; keep repository code canonical instead of emitting multiple synonyms.

## Cancel scheduled message

```json
{
  "message_outbox_id": 1148303263
}
```

Endpoint:

```text
POST /api/send/cancel
```

The docs state scheduled messages can only be canceled at least 5 minutes before the scheduled send time.

## Calculate SMS price

```json
{
  "number": "+983000505",
  "message": "تست"
}
```

Endpoint:

```text
POST /api/send/calculate-price
```

Success data includes:

```json
{
  "mci_price": 2370,
  "other_price": 2503,
  "parts": 1
}
```

## Response envelope

Successful send response shape:

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

Success rule:

- HTTP success alone is not enough. Require a parseable JSON response with `meta.status == true` and expected `data` for the called operation.

Common error envelope:

```json
{
  "data": null,
  "meta": {
    "status": false,
    "message": "اطلاعات وارد شده صحیح نمی باشد",
    "message_parameters": [],
    "message_code": "400-1",
    "errors": {}
  }
}
```

Validation error example:

```json
{
  "data": null,
  "meta": {
    "status": false,
    "message": "تکمیل گزینه پیام الزامی است",
    "message_parameters": [],
    "message_code": "400-2",
    "errors": {
      "message": ["تکمیل گزینه پیام الزامی است"]
    }
  }
}
```

Recommended mapping:

| Signal | Suggested category |
| --- | --- |
| Timeout / DNS / TLS / connection failure | Transport retryable if bounded |
| Invalid/expired token | Authentication/config failure |
| `meta.status=false` with `meta.errors` | Provider validation failure |
| HTTP 404 on cancel | Scheduled message not found or no longer cancellable |
| Unknown `message_code` | Preserve provider code and message |
