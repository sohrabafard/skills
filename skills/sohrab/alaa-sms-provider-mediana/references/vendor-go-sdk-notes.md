# Vendor Go SDK Sample Notes

The original user-uploaded sample is stored exactly as provided at:

```text
assets/vendor-sdk.go
```

Treat it as a vendor/API example, not as final production architecture.

## Contract clues from the sample

- Vendor default base URL: `https://edge.ippanel.com/v1/api`
- Send path: `/send`
- Final default send URL: `https://edge.ippanel.com/v1/api/send`
- Auth header: `Authorization: <API key/token>`
- JSON content type: `application/json`
- `SendWebservice` payload:
  - `sending_type: "webservice"`
  - `from_number`
  - `message`
  - `params.recipients`
- `SendPattern` payload:
  - `sending_type: "pattern"`
  - `from_number`
  - top-level `recipients`
  - `code`
  - `params`
- `SendVOTP` payload:
  - `sending_type: "votp"`
  - `message` containing the code string
  - `params.recipients`
- Response shape:
  - `data`
  - `meta.status`
  - `meta.message`
  - `meta.message_parameters`
  - `meta.message_code`

## Production cleanup guidance

When implementing or adapting this in a real repository, improve it where appropriate:

- Make the final send URL or base URL/path environment-driven. Do not hard-code `https://edge.ippanel.com/v1/api/send` outside config defaults.
- Add `context.Context` to public send methods and request creation.
- Avoid `interface{}` for `Data` and `Params` when the repository benefits from typed structs.
- Parse provider error envelopes on non-2xx responses instead of returning raw body strings.
- Do not print from library code; return errors to callers and use repo logging conventions at the boundary.
- Close response bodies without logging to stdout/stderr from the library.
- Make timeout, send URL/base URL, and retry/backoff policy configurable.
- Redact `Authorization`, OTP values, full recipients, and sensitive message text in logs.
- Add table-driven tests for JSON encoding, form/query encoding, phone normalization, response parsing, and error mapping.

## Keep the sample separate

Do not edit `assets/vendor-sdk.go` to fit the current repository. If a refined Go client is needed, create or update repository code in the appropriate package and keep this asset as upstream reference material.
