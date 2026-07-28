# Mediana / IPPanel Edge — the send contract

Read this when you are building or reviewing a request against `POST /api/send`, or parsing anything this API returns.

## Provenance

Every vendor fact in this file comes from the IPPanel Edge documentation and the vendor Go sample preserved in `references/40-vendor-contract-clues.md`.

- Documentation repository: `https://github.com/ippanelcom/Edge-Document`
- Rendered documentation: `https://ippanelcom.github.io/Edge-Document/docs/`
- **read: unverified as of 2026-07-27.** No session that produced or revised this file had network access to those URLs, so no read date can be asserted.

Treat every table below as a local contract that has not been re-verified against the vendor. Before shipping a mode this repository has never sent, open the rendered documentation, confirm the field list, and replace the provenance line above with the URL and the date you actually read. An undated vendor fact looks authoritative and gets copied forward; that is how a provider skill rots.

Repository code, production configuration, committed fixtures, and account-specific documentation outrank this file wherever they disagree. When they disagree and you cannot resolve it, mark the point `NEEDS_MEDIANA_CONFIRMATION` and stop rather than guessing.

## Endpoints and configuration

Every URL is read from configuration. These are default constants, not literals to embed in a call site.

```text
MEDIANA_SMS_API_BASE_URL=https://edge.ippanel.com/v1
MEDIANA_SMS_SEND_URL=https://edge.ippanel.com/v1/api/send
MEDIANA_SMS_CANCEL_URL=https://edge.ippanel.com/v1/api/send/cancel
MEDIANA_SMS_PRICE_URL=https://edge.ippanel.com/v1/api/send/calculate-price
MEDIANA_SMS_URL_SEND_ENDPOINT=https://edge.ippanel.com/v1/api/send/webservice
MEDIANA_SMS_API_TOKEN=<secret>
MEDIANA_SMS_FROM_NUMBER=<account-approved sender>
```

Use the target repository's existing configuration names when it already has them, and keep the final request URL changeable without a code change either way. The `/v1` versus `/v1/api` base-URL trap is stated in `SKILL.md`; the vendor sample that causes it is in `references/40-vendor-contract-clues.md`.

## Headers

| Request kind | Headers |
|---|---|
| JSON | `Authorization: <token>` and `Content-Type: application/json` |
| Multipart | `Authorization: <token>`, `Content-Type: multipart/form-data`, `Accept: application/json` |
| GET URL send | credential in the query string — disqualified for authenticated production traffic; see `references/18-cancel-price-and-url-send.md` |

An API key generated from the user panel does not expire, and some sensitive endpoints accept a token only. `[source: rendered documentation, read: unverified as of 2026-07-27]`

## Every send mode, and where each is documented

All send modes post to the same endpoint and are selected by `sending_type`.

| `sending_type` | Content type | Main fields | Documented in |
|---|---|---|---|
| `webservice` | JSON | `from_number`, `message`, `params.recipients`, optional `send_time` | this file |
| `pattern` | JSON | `from_number`, `code`, top-level one-element `recipients`, `params`, optional `phonebook` | this file |
| `votp` | JSON | `message`, one-element `params.recipients` | this file |
| `peer_to_peer` | JSON | `from_number`, `params[]` of `{message, recipients}` | this file |
| `file` | multipart | `from_number`, `message`, `files[]`, optional `other_recipients`, optional `send_time` | `references/12-multipart-and-file-sends.md` |
| `peer_to_peer_file` | multipart | `from_number`, `files[]`, optional `send_time` | `references/12-multipart-and-file-sends.md` |
| `keyword` | multipart | `from_number`, `message` with placeholders, `files[]`, optional `send_time` | `references/12-multipart-and-file-sends.md` |
| `keyword_phonebook` | JSON | `from_number`, `message`, `params[].phonebook_id`, optional `send_time` | `references/15-targeting-and-bulk-sends.md` |
| `phonebook` | JSON | `from_number`, `message`, `params[]` | `references/15-targeting-and-bulk-sends.md` |
| `postal_code` | JSON | `from_number`, `message`, `params[]`, optional `other_recipients`, optional `send_time` | `references/15-targeting-and-bulk-sends.md` |
| `country` | JSON | `from_number`, `message`, `params[]`, optional `other_recipients` | `references/15-targeting-and-bulk-sends.md` |
| `geolocation` | JSON | `from_number`, `message`, Country V2 `params[]`, optional `other_recipients` | `references/15-targeting-and-bulk-sends.md` |
| `job` | JSON | `from_number`, `message`, job-category `params[]` | `references/15-targeting-and-bulk-sends.md` |

`[source: rendered documentation and the vendor Go sample, read: unverified as of 2026-07-27]`

`normal` appears in older examples and in some account code. Send `webservice` for new work. Send `normal` only when a committed fixture or provider client in the target repository already sends it; cite that file and line in the change.

Runnable requests for every mode are in `references/20-examples-and-rejects.md`.

## `webservice`

| Field | Required | Shape |
|---|---|---|
| `sending_type` | yes | `"webservice"` |
| `from_number` | yes | account-approved sender string, for example a numeric line or an alphabetic label |
| `message` | yes | the SMS text |
| `params.recipients` | yes | array of recipient strings in `+989xxxxxxxxx` form |
| `send_time` | no | UTC, `YYYY-MM-DD HH:MM:SS` |

- Nest recipients under `params.recipients`. A top-level `recipients` key on a `webservice` send is a payload defect, because that key belongs to `pattern`.
- Apply recipient validation to `params.recipients` only. `from_number` is a sender identifier that may be alphabetic, so mobile-number rules do not apply to it.
- Whether one invalid recipient rejects the whole request or only its own entry is **unverified**. Until a committed integration test proves otherwise, validate every recipient locally before sending, so the question never arises in production.

## `pattern`

| Field | Required | Shape |
|---|---|---|
| `sending_type` | yes | `"pattern"` |
| `from_number` | yes | account-approved sender string |
| `code` | yes | the provider-assigned pattern code, not a template id |
| `recipients` | yes | **top-level** array holding exactly one recipient |
| `params` | yes | object of pattern variables; see the mapping rules in `SKILL.md` |
| `phonebook` | no | object with a required `id`, plus `name`, `pre`, `email`, `options` |

- The pattern must already exist and be approved in the provider panel. The API has no create-pattern step, so an unapproved code fails at send time.
- Keep `recipients` top-level and `params` for variables only. A `recipients` key inside `params` is silently treated as a pattern variable, so the send is accepted with no recipient and no error you can see.
- Send exactly one recipient. The pattern endpoint accepts one per request, so a fan-out is N requests, each with its own idempotency handling.
- Include `phonebook` only when the product has asked to store the recipient. It writes to the account's phonebook, which is a side effect outside the message.

## `votp`

| Field | Required | Shape |
|---|---|---|
| `sending_type` | yes | `"votp"` |
| `message` | yes | the code to be spoken, as a string of ASCII digits |
| `params.recipients` | yes | array holding exactly one recipient |

- `votp` places a voice call. Use it only when the product asked for voice OTP; use `pattern` for SMS OTP.
- Omit `from_number`. The documented request body and the vendor Go sample both omit it; one documentation note mentions it, so add it only when a committed fixture in the target repository shows it, and cite that fixture.
- No Alaa command family carries `votp` today, so a `votp` send needs a product decision and a new command family first.

## `peer_to_peer`

| Field | Required | Shape |
|---|---|---|
| `sending_type` | yes | `"peer_to_peer"` |
| `from_number` | yes | account-approved sender string |
| `params` | yes | **array** of objects, each with `message` and `recipients` |

The response returns one `message_outbox_id` per group, not per recipient. Store the group boundaries you sent, because the ids cannot be mapped back to individual recipients afterwards.

## Scheduling with `send_time`

- Format `send_time` as `YYYY-MM-DD HH:MM:SS` in UTC. A local-time string is accepted by the API and delivers at the wrong hour.
- A scheduled send is cancellable up to five minutes before its scheduled time; see `references/18-cancel-price-and-url-send.md`.
- Keep the `message_outbox_ids` from the schedule response. They are the only handle on a scheduled message.

## The response envelope

Every JSON endpoint answers with `data` and `meta`.

| Field | Meaning |
|---|---|
| `data.message_outbox_ids` | array of provider outbox ids on a send; the handle for tracking and cancellation |
| `meta.status` | boolean; `true` is the only success value |
| `meta.message` | a localized human string |
| `meta.message_code` | a stable dotted-numeric code such as `200-1` or `400-2` |
| `meta.message_parameters` | array of substitution values for `meta.message` |
| `meta.errors` | object of field name to array of messages, present on validation failures |

Parsing rules:

- Require both a 2xx status and `meta.status: true` before treating a send as accepted. HTTP success alone is not acceptance, because this API reports refusal inside a 200 body.
- Branch on `meta.message_code`, never on `meta.message`. The message is a localized human string that the vendor may reword at any time, and matching on it breaks silently on the next wording change.
- Preserve an unrecognised `message_code` verbatim in the delivery record instead of collapsing it into a generic error, because the code is the only thing support can give the vendor.
- Persist `data.message_outbox_ids` on every accepted send. Without them a scheduled message cannot be cancelled and a delivery cannot be traced.
- Map an invalid or expired token to a configuration failure, not to a retryable transport failure. Retrying it burns the budget and never succeeds.

Failure classification, retry legality and the ambiguous outcome are in `references/30-failure-and-ambiguity.md`.
