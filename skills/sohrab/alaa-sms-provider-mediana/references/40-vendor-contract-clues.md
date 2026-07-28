# Mediana / IPPanel Edge — vendor contract clues and the Go sample

Read this when you are writing or reviewing a Go client for this vendor, or when two sources disagree about where the base URL ends and the path begins.

## Where these clues came from

A vendor-supplied Go sample, `ippanel/sdk.go`, was uploaded to this skill in an earlier session and shipped in this skill's assets directory until 2026-07-27. It carried no `go.mod`, no license, no SPDX identifier, no version and no commit, so its provenance could not be established and its currency could not be checked. It implemented three of the fourteen send modes, had no `context.Context`, no retry handling, no redaction, a hardcoded ten-second timeout, a `fmt.Printf` inside library code, and two comments annotating `sending_type` as `"sms"` — a value this API does not accept.

The asset was retired to `_to_delete/20260727-batch5/alaa-sms-provider-mediana/`. Every durable fact it carried is below. `git show 47b0bbef:skills/sohrab/alaa-sms-provider-mediana/assets/vendor-sdk.go` recovers the original if a question about it comes up.

**read: unverified as of 2026-07-27.** The sample's own read date was never recorded, so the facts below are corroborating evidence for the rendered documentation rather than an independent dated source.

## The base URL trap

The sample hardcoded `defaultBaseURL = "https://edge.ippanel.com/v1/api"` and posted to the path `/send`. This skill's configuration default is `MEDIANA_SMS_API_BASE_URL=https://edge.ippanel.com/v1` with the path `/api/send`. Both produce `https://edge.ippanel.com/v1/api/send`.

**Choose one boundary, write it down beside the configuration value, and assert the final URL in a test.** An agent that takes the base URL from this skill and the path from the sample builds `https://edge.ippanel.com/v1/api/api/send`, which resolves, connects, authenticates, and 404s — so it passes every check that does not actually send, and fails only in the environment where a send matters.

| Base URL | Path to join | Result |
|---|---|---|
| `…/v1` | `/api/send` | correct |
| `…/v1/api` | `/send` | correct |
| `…/v1/api` | `/api/send` | `…/v1/api/api/send`, 404 |

## Contract clues the sample corroborates

- Auth header `Authorization: <API key or token>`, with no scheme prefix.
- JSON content type `application/json`.
- One send endpoint for every mode, selected by the `sending_type` field in the body.
- `webservice`: `sending_type`, `from_number`, `message`, `params.recipients`.
- `pattern`: `sending_type`, `from_number`, **top-level** `recipients`, `code`, `params`.
- `votp`: `sending_type`, `message` carrying the code as a string, `params.recipients`, and **no** `from_number`.
- Response envelope: `data`, plus `meta` with `status`, `message`, `message_parameters` and `message_code`.

The full field tables, including the eleven modes the sample never implemented, are in `references/10-send-contract.md`.

## Writing the Go client this vendor needs

The sample is not a starting point to copy. Build the client from the field tables and hold it to these rules; the general Go rules are `/alaa-golang` (`$alaa-golang`) and this list is only what this vendor makes go wrong.

- Take a `context.Context` as the first parameter of every send method and pass it into request construction, so a cancelled notification job stops a send that has not been written yet.
- Read the base URL, the path, and the request timeout from configuration. A hardcoded ten-second timeout is a platform value living in a vendor client, and `alaa-services-contract references/22-failure-load-and-deprecation-contract.md` owns it.
- Return a typed error that distinguishes the four transport classes in `references/30-failure-and-ambiguity.md`. Returning `errors.New(string(body))` on a non-2xx, as the sample did, throws away the classification and puts recipients and message text into an error string that will be logged.
- Parse the `data`/`meta` envelope on every response, including non-2xx, before deciding anything. A status code alone is wrong on an API that reports refusal inside a 200.
- Use typed request and response structs rather than `map[string]interface{}` for `params`, so a field-name change fails at compile time instead of at the vendor.
- Never print from library code. The sample's `fmt.Printf` on a body-close failure writes to whatever stdout the worker has, outside the service's log pipeline and its redaction.
- Redact the `Authorization` header, recipients, OTP values, pattern variable values, and message text at the point they enter any error or log value, using the mask forms in `SKILL.md`.
- Cover request JSON encoding, form encoding for the multipart modes, query encoding, final URL construction, envelope parsing, and each of the four transport classes with table-driven tests.
