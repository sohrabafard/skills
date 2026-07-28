# Mediana / IPPanel Edge — cancel, price, and the URL send endpoint

Read this when you are cancelling a scheduled message, quoting a price before a send, or deciding what to do with the legacy GET send endpoint.

## Provenance

- Documentation repository: `https://github.com/ippanelcom/Edge-Document`
- Rendered documentation: `https://ippanelcom.github.io/Edge-Document/docs/`
- **read: unverified as of 2026-07-27.** No session that produced or revised this file had network access to those URLs.

## Cancel a scheduled message

`POST /api/send/cancel`, JSON, one field.

| Field | Required | Shape |
|---|---|---|
| `message_outbox_id` | yes | positive integer, taken from a send response's `data.message_outbox_ids` |

- Send one id per request. The field is singular, so cancelling a `peer_to_peer` send or a multi-recipient batch means one request per outbox id in the response.
- Cancel at least five minutes before the scheduled send time. Inside that window the vendor has already committed the message and the cancel fails. `[source: rendered documentation, read: unverified as of 2026-07-27]`
- Treat HTTP 404 as "not found or no longer cancellable" and stop. It is a terminal answer about this id, so retrying it cannot change the outcome and only burns the caller's budget.
- Record the cancel attempt and its result against the same delivery row as the send. A cancel that failed inside the five-minute window means the message went out, and the delivery record is the only place that will show it.

## Calculate a price

`POST /api/send/calculate-price`, JSON.

| Field | Required | Shape |
|---|---|---|
| `number` | yes | the sender number the send would use |
| `message` | yes | the exact message text the send would carry |

The success `data` carries `mci_price`, `other_price`, and `parts`.

- Price the exact text you intend to send, after every pattern variable has been substituted. `parts` counts message segments, and a substituted variable can push the text across a segment boundary and change the price after you quoted it.
- Treat a price as an estimate for a decision, never as a billing record. The account panel owns the charge.

## The URL send endpoint

`GET /api/send/webservice`, credential in the query string, parameters `from`, `message`, `to`, and either `apikey` or a `username`/`password` pair.

**Do not use this endpoint for authenticated production traffic. Use `POST /api/send` with the token in the `Authorization` header instead.** A GET query string is written verbatim into the web server's access log, every proxy log on the path, the browser or shell history of whoever ran it, and any error report that captures the request URL. None of those rotate the credential, and none of them are covered by the masking rules in `SKILL.md`, because masking applies to what your code emits and not to what an intermediary records.

Use it only when a legacy system outside this repository can call nothing else, and then: issue that system its own API key so revocation does not affect production sends, and record the exception and its owner in the change.

Send either `apikey` or `username` and `password`, never both. The documentation lists several accepted aliases for each query parameter; emit exactly one spelling per parameter from one place in the code, because multiple synonyms in one request are an undefined precedence.

Percent-encode `message` and every other parameter. An unencoded `&` or `#` in message text truncates the message at the vendor with no error.
