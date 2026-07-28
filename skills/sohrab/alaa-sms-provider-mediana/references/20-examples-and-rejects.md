# Mediana / IPPanel Edge — examples, rejects, and the required tests

Read this when you are writing a fixture, a curl command, a Postman or Insomnia request, or a test that must reject a payload.

Every request here uses environment variables for credentials and endpoints. Never commit a real token, a real sender, a real recipient, a real OTP, or a real pattern variable value. Field tables and rules live with each mode in `references/10-send-contract.md`, `references/12-multipart-and-file-sends.md`, `references/15-targeting-and-bulk-sends.md` and `references/18-cancel-price-and-url-send.md`; this file holds only the runnable shapes.

## Environment

```bash
export MEDIANA_SMS_API_BASE_URL="${MEDIANA_SMS_API_BASE_URL:-https://edge.ippanel.com/v1}"
export MEDIANA_SMS_SEND_URL="${MEDIANA_SMS_SEND_URL:-$MEDIANA_SMS_API_BASE_URL/api/send}"
export MEDIANA_SMS_CANCEL_URL="${MEDIANA_SMS_CANCEL_URL:-$MEDIANA_SMS_API_BASE_URL/api/send/cancel}"
export MEDIANA_SMS_PRICE_URL="${MEDIANA_SMS_PRICE_URL:-$MEDIANA_SMS_API_BASE_URL/api/send/calculate-price}"
export MEDIANA_SMS_API_TOKEN="<secret>"
export MEDIANA_SMS_FROM_NUMBER="+983000505"
```

## Requests

### `webservice`

```bash
curl --location "$MEDIANA_SMS_SEND_URL" \
  --header "Authorization: $MEDIANA_SMS_API_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{
    "sending_type": "webservice",
    "from_number": "+983000505",
    "message": "Your order has shipped.",
    "params": { "recipients": ["+989123830000"] }
  }'
```

Scheduled variant: add `"send_time": "2026-07-05 10:30:00"` at the top level, in UTC.

### `pattern`, carrying an SMS OTP

```bash
curl --location "$MEDIANA_SMS_SEND_URL" \
  --header "Authorization: $MEDIANA_SMS_API_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{
    "sending_type": "pattern",
    "from_number": "+983000505",
    "code": "<pattern-code>",
    "recipients": ["+989123830000"],
    "params": { "code": "458921" }
  }'
```

Multi-variable variant, with names taken from the approved pattern rather than invented:

```json
{
  "sending_type": "pattern",
  "from_number": "+983000505",
  "code": "<pattern-code>",
  "recipients": ["+989123830000"],
  "params": {
    "user": "<name>",
    "course": "<course>",
    "ticket_url": "<url>"
  }
}
```

### `votp`

```json
{
  "sending_type": "votp",
  "message": "45852",
  "params": { "recipients": ["+989123830000"] }
}
```

### `peer_to_peer`

```json
{
  "sending_type": "peer_to_peer",
  "from_number": "+983000505",
  "params": [
    { "recipients": ["+989123830000", "+989123830001"], "message": "First group message" },
    { "recipients": ["+989123830002"], "message": "Second group message" }
  ]
}
```

### `file`, multipart

```bash
curl --location "$MEDIANA_SMS_SEND_URL" \
  --header "Authorization: $MEDIANA_SMS_API_TOKEN" \
  --header 'Accept: application/json' \
  --form 'sending_type="file"' \
  --form 'from_number="+983000505"' \
  --form 'message="Your statement is ready."' \
  --form 'files[]=@"/path/to/recipients.csv"' \
  --form 'other_recipients[]="+989123830000"'
```

### `peer_to_peer_file`, multipart

```bash
curl --location "$MEDIANA_SMS_SEND_URL" \
  --header "Authorization: $MEDIANA_SMS_API_TOKEN" \
  --header 'Accept: application/json' \
  --form 'sending_type="peer_to_peer_file"' \
  --form 'from_number="+983000505"' \
  --form 'send_time="2026-04-25 10:10:10"' \
  --form 'files[]=@"/path/to/rows.csv"'
```

### `keyword`, multipart

```bash
curl --location "$MEDIANA_SMS_SEND_URL" \
  --header "Authorization: $MEDIANA_SMS_API_TOKEN" \
  --header 'Accept: application/json' \
  --form 'sending_type="keyword"' \
  --form 'from_number="+983000505"' \
  --form 'message="Hello {ex_B}, your balance is {ex_C}"' \
  --form 'files[]=@"/path/to/values.xlsx"'
```

### `keyword_phonebook`

```json
{
  "sending_type": "keyword_phonebook",
  "from_number": "+983000505",
  "message": "Due date {ex_50856}, amount {ex_50858}",
  "send_time": "2026-03-25 10:10:10",
  "params": [ { "phonebook_id": 123654 } ]
}
```

### `phonebook`

```json
{
  "sending_type": "phonebook",
  "from_number": "+983000505",
  "message": "Service notice",
  "params": [
    { "phonebook_ids": ["123654"], "type": "all", "start": "1", "size": "2" },
    { "phonebook_id": "456987", "type": "detail", "number_ids": ["123", "456", "789"] }
  ]
}
```

### `postal_code`

```json
{
  "sending_type": "postal_code",
  "from_number": "+98BANK",
  "message": "Branch opening notice",
  "params": [
    {
      "bank": "all",
      "postal_code": 131,
      "gender": 0,
      "age_from": 1330,
      "age_to": 1402,
      "mci": { "start": 0, "size": 1 },
      "irancell": { "start": 0, "size": 0 },
      "other": { "start": 0, "size": 0 }
    }
  ],
  "other_recipients": ["+989123830000"]
}
```

### `country`

```json
{
  "sending_type": "country",
  "from_number": "+98BANK",
  "message": "Regional notice",
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
      "mci": { "start": 10, "size": 100 },
      "irancell": { "start": 1, "size": 2 },
      "other": { "start": 2, "size": 3 }
    }
  ],
  "other_recipients": ["+989123830001"]
}
```

### `geolocation`, Country V2

```json
{
  "sending_type": "geolocation",
  "from_number": "+98BANK",
  "message": "Regional notice",
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
        { "start": 0, "size": 10, "id": 1 },
        { "start": 0, "size": 20, "id": 2 }
      ]
    }
  ],
  "other_recipients": ["+989123830001"]
}
```

### `job`

```json
{
  "sending_type": "job",
  "from_number": "+98PRO",
  "message": "Professional notice",
  "params": [
    {
      "main_category_id": 1,
      "sub_category_id": 1,
      "operator": [ { "start": 0, "size": 3373, "id": 2 } ]
    }
  ]
}
```

### Cancel and price

```bash
curl --location "$MEDIANA_SMS_CANCEL_URL" \
  --header "Authorization: $MEDIANA_SMS_API_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{ "message_outbox_id": 1148303263 }'

curl --location "$MEDIANA_SMS_PRICE_URL" \
  --header "Authorization: $MEDIANA_SMS_API_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{ "number": "+983000505", "message": "Your order has shipped." }'
```

## Responses

Everything under this heading is a response fixture. Never feed one to a request validator; `scripts/validate_mediana_payload.py` reads request shapes only, and a response fed to it produces a misleading rejection.

### Accepted send

```json
{
  "data": { "message_outbox_ids": [1123544244] },
  "meta": {
    "status": true,
    "message": "<localized vendor message>",
    "message_parameters": [],
    "message_code": "200-1"
  }
}
```

### Refused, general

```json
{
  "data": null,
  "meta": {
    "status": false,
    "message": "<localized vendor message>",
    "message_parameters": [],
    "message_code": "400-1",
    "errors": {}
  }
}
```

### Refused, field validation

```json
{
  "data": null,
  "meta": {
    "status": false,
    "message": "<localized vendor message>",
    "message_parameters": [],
    "message_code": "400-2",
    "errors": { "message": ["<localized field message>"] }
  }
}
```

### Price quote

```json
{ "mci_price": 2370, "other_price": 2503, "parts": 1 }
```

`meta.message` is a localized human string. Branch on `meta.message_code` and store `meta.message` unparsed, because the vendor may reword the message at any time and a match on it fails silently.

### Ambiguous outcome

There is no fixture for this one, because the vendor sends nothing. Simulate it in tests as a client-side read timeout raised after the request was written, and assert that the code records the delivery as ambiguous, does not re-issue the request, and does not mark the send failed. Assert separately that a connection refused before the write is retried. If both assertions pass against the same code path, that path is collapsing the two events; see `references/30-failure-and-ambiguity.md`.

## Payloads a test must reject

### A Bale Safir payload sent to Mediana

```json
{
  "bot_id": 1,
  "phone_number": "989123830000",
  "message_data": { "message": { "text": "Hello" } }
}
```

Mediana takes `sending_type`, `from_number`, `message`, and `params` or `recipients`, behind an `Authorization` header. `reject_bale_shape()` in the validator catches this, and the sibling skill's validator ships the matching `reject_mediana_shape()`, so the guard holds in both directions.

### An unnormalised recipient

```json
{
  "sending_type": "webservice",
  "from_number": "+983000505",
  "message": "Your order has shipped.",
  "params": { "recipients": ["09123830000"] }
}
```

Render it through `--normalize` first; see `references/50-phone-and-conformance.md`.

### A pattern nesting its recipients

```json
{
  "sending_type": "pattern",
  "from_number": "+983000505",
  "code": "<pattern-code>",
  "params": { "recipients": ["+989123830000"], "code": "458921" }
}
```

Pattern recipients are top-level. Inside `params` the key is treated as a pattern variable, so the send is accepted with no recipient.

### A pattern with two recipients

```json
{
  "sending_type": "pattern",
  "from_number": "+983000505",
  "code": "<pattern-code>",
  "recipients": ["+989123830000", "+989123830001"],
  "params": { "code": "458921" }
}
```

The pattern endpoint takes one recipient per request.

### A pattern variable sent as a number

```json
{
  "sending_type": "pattern",
  "from_number": "+983000505",
  "code": "<pattern-code>",
  "recipients": ["+989123830000"],
  "params": { "code": 0458921 }
}
```

Values are substituted as text, so a numeric OTP loses its leading zero and the subscriber receives a code that will not verify.

### A bulk payload with unchecked selectors

```json
{
  "sending_type": "postal_code",
  "from_number": "+98BANK",
  "message": "Branch opening notice",
  "params": [ { "garbage": "unvalidated" } ]
}
```

Each targeting mode has its own closed selector set; an unrecognised key means the audience is not what the caller thinks it is.

## The required tests

Every change to Mediana code carries these, in addition to the repository's own gates. Which layer each runs at is `/alaa-testing-strategy` (`$alaa-testing-strategy`).

- Payload-builder tests for the send mode the change touched, asserting the exact JSON body or the exact multipart form fields.
- `pattern_values[] → params{}` tests for a duplicate key, a missing declared variable, an undeclared variable, and a value with a leading zero.
- Normalisation tests driven by `scripts/phone-conformance-corpus.json`, asserting both channel renderings and every rejection reason.
- Response tests for `meta.status: true`, `meta.status: false` with `meta.errors`, `meta.status: false` without them, an unrecognised `message_code`, HTTP 401, HTTP 422, HTTP 404 on cancel, and a body that is not JSON.
- Transport tests for all four classes in `references/30-failure-and-ambiguity.md`, asserting that a connect refusal and a read timeout take different paths.
- Final-URL tests proving the configured base URL and path join to exactly one `/api/send`.
- Redaction tests proving no token, recipient, OTP, or pattern value reaches a log, a trace attribute, an exception payload, or a report.
- Configuration tests proving every endpoint and the token load from configuration, with no real secret committed.
- `python3 scripts/validate_mediana_payload.py --self-test`, then the validator against every committed fixture.
